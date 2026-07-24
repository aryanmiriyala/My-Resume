#!/usr/bin/env python3
"""Targeted recent-job discovery helper.

This tool avoids scraping Google result pages. It generates high-signal search
URLs, stores discovered jobs in a VS Code-friendly CSV inbox, scores them with
deterministic rules, and exports a manual-apply report partitioned by discovery
age.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INBOX = ROOT / "jobs-inbox.csv"
DEFAULT_RESULTS_DIR = ROOT / "results"
DEFAULT_SCAN_HISTORY = ROOT / "data" / "scan-history.tsv"
ROLE_BUCKETS_PATH = ROOT / "config" / "role-buckets.json"
ATS_SOURCES_PATH = ROOT / "config" / "ats-sources.json"
FILTERS_PATH = ROOT / "config" / "filters.json"
DIRECT_ATS_TARGETS_PATH = ROOT / "config" / "direct-ats-targets.json"
H1B_SPONSOR_WATCHLIST_PATH = ROOT / "config" / "h1b-sponsor-watchlist.json"
BROAD_ATS_CACHE_DIR = ROOT / "cache" / "broad-ats-companies"
URL_PATTERN = re.compile(r'https?://[^\s<>)\"\']+')

CSV_FIELDS = ["company", "position", "posted_at", "pulled_at", "url"]
RESULT_JOB_FIELDS = [
    "fit_score",
    "status",
    "company",
    "title",
    "location",
    "source",
    "posted_at",
    "pulled_at",
    "first_discovered_at",
    "last_seen_at",
    "flags",
    "url",
    "notes",
]
SCAN_HISTORY_FIELDS = [
    "url",
    "identity_key",
    "first_seen_at",
    "last_seen_at",
    "company",
    "title",
    "source",
    "posted_at",
    "location",
    "last_status",
    "fit_score",
    "flags",
]
BROAD_ATS_DATASET_BASE = "https://raw.githubusercontent.com/Feashliaa/job-board-aggregator/main/data"
BROAD_ATS_DATASETS = {
    "greenhouse": f"{BROAD_ATS_DATASET_BASE}/greenhouse_companies.json",
    "lever": f"{BROAD_ATS_DATASET_BASE}/lever_companies.json",
    "ashby": f"{BROAD_ATS_DATASET_BASE}/ashby_companies.json",
    "workday": f"{BROAD_ATS_DATASET_BASE}/workday_companies.json",
}
DEFAULT_SEARCH_WINDOWS = ["0-6h", "0-12h", "0-24h", "0-48h"]
SLUG_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().replace(microsecond=0).isoformat()


def parse_dt(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def parse_posted_datetime(value: str, now: datetime | None = None) -> datetime | None:
    """Parse ISO timestamps and common ATS relative posted-date strings."""
    text = clean_text(value, max_length=120)
    if not text:
        return None
    now = now or utc_now()
    lowered = text.lower()
    lowered = re.sub(r"^\s*posted\s+", "", lowered).strip()

    if lowered in {"today", "just posted", "posted today"}:
        return now
    if lowered in {"yesterday", "posted yesterday"}:
        return now - timedelta(days=1)

    relative = re.search(r"(\d+)\+?\s*(minute|minutes|hour|hours|day|days|week|weeks)\s+ago", lowered)
    if relative:
        amount = int(relative.group(1))
        unit = relative.group(2)
        if unit.startswith("minute"):
            return now - timedelta(minutes=amount)
        if unit.startswith("hour"):
            return now - timedelta(hours=amount)
        if unit.startswith("day"):
            return now - timedelta(days=amount)
        if unit.startswith("week"):
            return now - timedelta(weeks=amount)

    try:
        return parse_dt(text)
    except (TypeError, ValueError):
        return None


def parse_epoch(value: Any) -> datetime:
    return datetime.fromtimestamp(int(value), tz=timezone.utc)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_json(url: str, data: bytes | None = None, method: str | None = None) -> Any:
    headers = {"User-Agent": "career-ops-job-search", "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = Request(url, data=data, headers=headers, method=method)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def quote_term(term: str) -> str:
    if " " in term or "/" in term or "-" in term or "+" in term or "." in term:
        return f'"{term}"'
    return term


def or_group(terms: list[str]) -> str:
    return "(" + " OR ".join(quote_term(term) for term in terms) + ")"


def exclusion(term: str) -> str:
    return "-" + quote_term(term)


def google_url(query: str, time_filter: str, num: int = 50) -> str:
    params = urlencode({"q": query, "num": str(num), "tbs": time_filter})
    return f"https://www.google.com/search?{params}"


def build_query(role_terms: list[str], domains: list[str], filters: dict[str, Any]) -> str:
    parts = [
        or_group(role_terms),
        or_group(filters["early_career_terms"]),
        or_group(filters["location_terms"]),
        "(" + " OR ".join(f"site:{domain}" for domain in domains) + ")",
        " ".join(exclusion(term) for term in filters["negative_terms"]),
    ]
    return " ".join(part for part in parts if part).strip()


def detect_source(url: str) -> str:
    host = urlparse(url).hostname or ""
    host = host.lower()
    if "greenhouse" in host:
        return "greenhouse"
    if "lever.co" in host:
        return "lever"
    if "ashbyhq" in host:
        return "ashby"
    if "workdayjobs" in host:
        return "workday"
    if "smartrecruiters" in host:
        return "smartrecruiters"
    if "workable" in host:
        return "workable"
    if "icims" in host:
        return "icims"
    if "jobvite" in host:
        return "jobvite"
    if "bamboohr" in host:
        return "bamboohr"
    return host or "unknown"


def normalize_text(*parts: str | None) -> str:
    return " ".join(part or "" for part in parts).lower()


def clean_text(value: Any, max_length: int = 700) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_length]


def contains_term(text: str, term: str) -> bool:
    """Match terms without substring false positives like architect/architecture."""
    needle = term.lower()
    if any(char.isalnum() for char in needle):
        pattern = r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])"
        return re.search(pattern, text) is not None
    return needle in text


ROLE_LOCATION_SUFFIXES = {
    "amer",
    "americas",
    "apac",
    "austin",
    "bengaluru",
    "bangalore",
    "boston",
    "california",
    "canada",
    "chicago",
    "dallas",
    "hyderabad",
    "india",
    "new york",
    "nyc",
    "remote",
    "remote india",
    "remote us",
    "remote usa",
    "san francisco",
    "seattle",
    "texas",
    "united states",
    "us",
    "usa",
}


def normalize_key_text(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def normalize_company_for_dedup(company: str | None) -> str:
    text = normalize_key_text(company)
    text = re.sub(r"\b(inc|llc|ltd|corp|corporation|company|co)\b", "", text)
    return re.sub(r"\s+", " ", text).strip()


def role_suffix_is_location(value: str) -> bool:
    normalized = normalize_key_text(value)
    if not normalized:
        return False
    parts = re.split(r"\s+(?:or|and)\s+|[,/|;]+", normalized)
    parts = [part.strip() for part in parts if part.strip()]
    return bool(parts) and all(part in ROLE_LOCATION_SUFFIXES for part in parts)


def normalize_role_for_dedup(title: str | None) -> str:
    text = str(title or "").lower().strip()
    while True:
        match = re.search(r"\s*[\[(]([^[\]()]+)[\])]\s*$", text)
        if not match or not role_suffix_is_location(match.group(1)):
            break
        text = text[: match.start()].rstrip()
    return normalize_key_text(text)


def job_identity_key(job: dict[str, str]) -> str:
    company = normalize_company_for_dedup(job.get("company"))
    title = normalize_role_for_dedup(job.get("title") or job.get("position"))
    if not company or not title:
        return ""
    return f"{company}::{title}"


def location_policy(filters: dict[str, Any]) -> dict[str, list[str]]:
    return filters.get("location_policy") or {}


def work_authorization_policy(filters: dict[str, Any]) -> dict[str, Any]:
    return filters.get("work_authorization_policy") or {}


@lru_cache(maxsize=4)
def sponsor_watchlist_company_names(path: Path = H1B_SPONSOR_WATCHLIST_PATH) -> frozenset[str]:
    if not path.exists():
        return frozenset()
    payload = load_json(path)
    names: set[str] = set()
    for company in payload.get("companies", []):
        names.add(normalize_company_for_dedup(company.get("name")))
        for alias in company.get("aliases", []):
            names.add(normalize_company_for_dedup(alias))
    return frozenset(name for name in names if name)


def company_in_sponsor_watchlist(company: str, watchlist_names: set[str] | frozenset[str]) -> bool:
    normalized = normalize_company_for_dedup(company)
    if not normalized:
        return False
    return any(normalized == name or normalized.startswith(f"{name} ") or name.startswith(f"{normalized} ") for name in watchlist_names)


def classify_work_authorization(
    text: str,
    company: str,
    filters: dict[str, Any],
    watchlist_names: set[str] | frozenset[str],
) -> tuple[int, list[str]]:
    policy = work_authorization_policy(filters)
    score_delta = 0
    flags: list[str] = []

    for term in policy.get("sponsorship_blocker_terms", []):
        if contains_term(text, term):
            score_delta -= 35
            flags.append("work_auth_blocker")
            break

    if company_in_sponsor_watchlist(company, watchlist_names):
        score_delta += int(policy.get("h1b_watchlist_score_bonus", 0))
        flags.append("h1b_watchlist")

    if any(contains_term(text, term) for term in policy.get("sponsorship_available_terms", [])):
        score_delta += 10
        flags.append("sponsorship_signal")

    return score_delta, flags


def classify_location(location: str, filters: dict[str, Any]) -> tuple[str, list[str]]:
    text = normalize_text(location)
    policy = location_policy(filters)
    us_terms = policy.get("us_terms", [])
    india_terms = policy.get("india_terms", [])
    remote_ambiguous_terms = policy.get("remote_ambiguous_terms", [])
    foreign_terms = policy.get("foreign_exclusion_terms", [])

    if not text:
        return "unknown", ["location_needs_review"]
    if any(contains_term(text, term) for term in us_terms):
        return "us", []
    if any(contains_term(text, term) for term in india_terms):
        return "india", ["location_india_review"]
    if any(contains_term(text, term) for term in foreign_terms):
        return "foreign", ["location_foreign"]
    if any(contains_term(text, term) for term in remote_ambiguous_terms):
        return "remote_ambiguous", ["location_needs_review"]
    if re.search(r"\b\d+\s+locations?\b", text):
        return "unknown", ["location_needs_review"]
    return "unknown", ["location_needs_review"]


@dataclass
class ScoreResult:
    score: int
    bucket: str
    flags: list[str]


def score_job(
    title: str,
    company: str,
    location: str,
    source: str,
    snippet: str,
    role_buckets: dict[str, Any],
    filters: dict[str, Any],
    ats_sources: dict[str, Any],
    explicit_bucket: str | None = None,
    sponsor_watchlist: set[str] | frozenset[str] | None = None,
) -> ScoreResult:
    text = normalize_text(title, company, location, source, snippet)
    title_text = normalize_text(title)
    watchlist_names = sponsor_watchlist if sponsor_watchlist is not None else sponsor_watchlist_company_names()
    score = 40
    flags: list[str] = []

    detected_bucket = explicit_bucket or ""
    if not detected_bucket:
        for bucket, payload in role_buckets.items():
            if any(contains_term(title_text, term) for term in payload["terms"]):
                detected_bucket = bucket
                break
    if detected_bucket:
        score += 15
    else:
        detected_bucket = "unclassified"
        flags.append("no_role_bucket_match")

    if any(contains_term(text, term) for term in filters["early_career_terms"]):
        score += 15
    else:
        flags.append("no_early_career_signal")

    location_class, location_flags = classify_location(location, filters)
    flags.extend(location_flags)
    if location_class == "us":
        score += 10
    elif location_class == "india":
        score += 6
    elif location_class == "remote_ambiguous":
        score += 4
    elif location_class == "foreign":
        score -= 25

    matched_skills = [term for term in filters["positive_skill_terms"] if contains_term(text, term)]
    score += min(20, len(matched_skills) * 2)

    if source in ats_sources.get("preferred_sources", []):
        score += 5

    work_auth_delta, work_auth_flags = classify_work_authorization(text, company, filters, watchlist_names)
    score += work_auth_delta
    flags.extend(work_auth_flags)

    for term in filters["negative_terms"]:
        if contains_term(text, term):
            score -= 15
            flags.append(f"negative:{term}")

    return ScoreResult(score=max(0, min(100, score)), bucket=detected_bucket, flags=flags)


def ensure_inbox(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    write_jobs(path, [])


def read_jobs(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            normalized = {
                "company": (row.get("company") or "").strip(),
                "position": (row.get("position") or row.get("title") or "").strip(),
                "posted_at": (row.get("posted_at") or "").strip(),
                "pulled_at": (row.get("pulled_at") or row.get("first_discovered_at") or "").strip(),
                "url": (row.get("url") or "").strip(),
            }
            if normalized["url"]:
                rows.append(normalized)
        return rows


def csv_row_from_job(job: dict[str, str]) -> dict[str, str]:
    return {
        "company": (job.get("company") or "").strip(),
        "position": (job.get("position") or job.get("title") or "").strip(),
        "posted_at": (job.get("posted_at") or "").strip(),
        "pulled_at": (job.get("pulled_at") or job.get("first_discovered_at") or iso_now()).strip(),
        "url": (job.get("url") or "").strip(),
    }


def write_jobs(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(csv_row_from_job(row))


def result_job_csv_row(job: dict[str, str]) -> dict[str, str]:
    return {
        "fit_score": (job.get("fit_score") or job.get("score") or "").strip(),
        "status": (job.get("status") or "").strip(),
        "company": (job.get("company") or "").strip(),
        "title": (job.get("title") or job.get("position") or "").strip(),
        "location": (job.get("location") or "").strip(),
        "source": (job.get("source") or "").strip(),
        "posted_at": (job.get("posted_at") or "").strip(),
        "pulled_at": (job.get("pulled_at") or job.get("first_discovered_at") or "").strip(),
        "first_discovered_at": (job.get("first_discovered_at") or job.get("pulled_at") or "").strip(),
        "last_seen_at": (job.get("last_seen_at") or "").strip(),
        "flags": (job.get("flags") or "").strip(),
        "url": (job.get("url") or "").strip(),
        "notes": (job.get("notes") or "").strip(),
    }


def write_result_jobs_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULT_JOB_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(result_job_csv_row(row))


def scan_history_path(args: argparse.Namespace) -> Path:
    return Path(getattr(args, "scan_history", DEFAULT_SCAN_HISTORY))


def read_scan_history(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = []
        for row in reader:
            normalized = {field: (row.get(field) or "").strip() for field in SCAN_HISTORY_FIELDS}
            if normalized["url"] or normalized["identity_key"]:
                rows.append(normalized)
        return rows


def write_scan_history(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = sorted(rows, key=lambda item: item.get("last_seen_at", ""), reverse=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCAN_HISTORY_FIELDS, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: (row.get(field) or "").strip() for field in SCAN_HISTORY_FIELDS})


def find_scan_history_index(
    rows: list[dict[str, str]],
    by_url: dict[str, int],
    by_identity: dict[str, int],
    job: dict[str, str],
) -> int | None:
    url = (job.get("url") or "").strip()
    identity = job_identity_key(job)
    if url and url in by_url:
        return by_url[url]
    if identity and identity in by_identity:
        return by_identity[identity]
    return None


def rebuild_scan_history_indexes(rows: list[dict[str, str]]) -> tuple[dict[str, int], dict[str, int]]:
    by_url: dict[str, int] = {}
    by_identity: dict[str, int] = {}
    for index, row in enumerate(rows):
        url = (row.get("url") or "").strip()
        identity = (row.get("identity_key") or "").strip()
        if url:
            by_url[url] = index
        if identity:
            by_identity[identity] = index
    return by_url, by_identity


def apply_scan_history(
    args: argparse.Namespace,
    tagged_jobs: list[tuple[str, list[dict[str, str]]]],
    now: datetime,
) -> dict[str, Any]:
    path = scan_history_path(args)
    rows = read_scan_history(path)
    initial_urls = {(row.get("url") or "").strip() for row in rows if row.get("url")}
    initial_identities = {(row.get("identity_key") or "").strip() for row in rows if row.get("identity_key")}
    by_url, by_identity = rebuild_scan_history_indexes(rows)
    seen_this_run: set[str] = set()
    new_count = 0
    seen_count = 0
    now_iso = now.replace(microsecond=0).isoformat()

    for status, jobs in tagged_jobs:
        for job in jobs:
            url = (job.get("url") or "").strip()
            identity = job_identity_key(job)
            run_key = identity or url
            history_index = find_scan_history_index(rows, by_url, by_identity, job)
            existed_before = bool((url and url in initial_urls) or (identity and identity in initial_identities))

            if history_index is None:
                first_seen = job.get("first_discovered_at") or now_iso
                history_row = {
                    "url": url,
                    "identity_key": identity,
                    "first_seen_at": first_seen,
                    "last_seen_at": now_iso,
                    "company": (job.get("company") or "").strip(),
                    "title": (job.get("title") or job.get("position") or "").strip(),
                    "source": (job.get("source") or "").strip(),
                    "posted_at": (job.get("posted_at") or "").strip(),
                    "location": (job.get("location") or "").strip(),
                    "last_status": status,
                    "fit_score": (job.get("fit_score") or "").strip(),
                    "flags": (job.get("flags") or "").strip(),
                }
                rows.append(history_row)
                by_url, by_identity = rebuild_scan_history_indexes(rows)
            else:
                history_row = rows[history_index]
                first_seen = history_row.get("first_seen_at") or job.get("first_discovered_at") or now_iso
                history_row.update(
                    {
                        "url": url or history_row.get("url", ""),
                        "identity_key": identity or history_row.get("identity_key", ""),
                        "first_seen_at": first_seen,
                        "last_seen_at": now_iso,
                        "company": (job.get("company") or history_row.get("company") or "").strip(),
                        "title": (job.get("title") or job.get("position") or history_row.get("title") or "").strip(),
                        "source": (job.get("source") or history_row.get("source") or "").strip(),
                        "posted_at": (job.get("posted_at") or history_row.get("posted_at") or "").strip(),
                        "location": (job.get("location") or history_row.get("location") or "").strip(),
                        "last_status": status,
                        "fit_score": (job.get("fit_score") or history_row.get("fit_score") or "").strip(),
                        "flags": (job.get("flags") or history_row.get("flags") or "").strip(),
                    }
                )
                by_url, by_identity = rebuild_scan_history_indexes(rows)

            job["first_discovered_at"] = first_seen
            job["last_seen_at"] = now_iso
            job["status"] = status
            if run_key and run_key not in seen_this_run:
                if existed_before:
                    seen_count += 1
                else:
                    new_count += 1
                seen_this_run.add(run_key)

    if rows and not getattr(args, "dry_run", False):
        write_scan_history(path, rows)

    return {
        "path": path.as_posix(),
        "new": new_count,
        "seen_before": seen_count,
        "written": bool(rows and not getattr(args, "dry_run", False)),
        "dry_run": getattr(args, "dry_run", False),
    }


def result_jobs_for_export(result: dict[str, Any]) -> list[dict[str, str]]:
    jobs_by_url: dict[str, dict[str, str]] = {}

    for row in result.get("review_candidates", []):
        job = {**row}
        job["status"] = "review"
        key = job.get("url") or f"{job.get('company')}|{job.get('title')}|{job.get('location')}"
        jobs_by_url[key] = job

    for row in result.get("imported", []):
        job = {**row}
        job["status"] = "shortlist"
        key = job.get("url") or f"{job.get('company')}|{job.get('title')}|{job.get('location')}"
        jobs_by_url[key] = job

    return sorted(jobs_by_url.values(), key=lambda item: int_or_zero(item.get("fit_score", "")), reverse=True)


def result_job_recency_datetime(job: dict[str, str], now: datetime) -> datetime | None:
    posted = parse_posted_datetime(job.get("posted_at", ""), now)
    if posted:
        return posted
    for key in ("first_discovered_at", "pulled_at"):
        try:
            return parse_dt(job.get(key, ""))
        except (TypeError, ValueError):
            continue
    return None


def result_job_bucket(job: dict[str, str], now: datetime, filters: dict[str, Any]) -> str | None:
    recency_dt = result_job_recency_datetime(job, now)
    if not recency_dt:
        return "Undated / Review"
    age = (now - recency_dt).total_seconds() / 3600
    for bucket in filters["report_buckets"]:
        if bucket["min_hours"] <= age < bucket["max_hours"]:
            return bucket["label"]
    return None


def render_jobs_by_window(title: str, rows: list[dict[str, str]], now: datetime | None = None) -> str:
    filters = load_json(FILTERS_PATH)
    now = now or utc_now()
    grouped: dict[str, list[dict[str, str]]] = {bucket["label"]: [] for bucket in filters["report_buckets"]}
    grouped["Undated / Review"] = []

    for row in rows:
        bucket = result_job_bucket(row, now, filters)
        if bucket:
            grouped.setdefault(bucket, []).append(row)

    lines = [
        f"# {title}",
        "",
        f"Generated at: `{now.replace(microsecond=0).isoformat()}`",
        "",
        "Jobs are grouped by `posted_at` when available. `first_discovered_at` or `pulled_at` is used only when posted time is missing.",
        "",
    ]
    for label, bucket_rows in grouped.items():
        lines.append(f"## {label}")
        lines.append("")
        lines.extend(render_job_table(sorted(bucket_rows, key=lambda item: int_or_zero(item.get("fit_score", "")), reverse=True)))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def make_job_record(args: argparse.Namespace) -> dict[str, str]:
    role_buckets = load_json(ROLE_BUCKETS_PATH)
    ats_sources = load_json(ATS_SOURCES_PATH)
    filters = load_json(FILTERS_PATH)
    source = args.source or detect_source(args.url)
    discovered_at = args.discovered_at or iso_now()
    result = score_job(
        title=args.title,
        company=args.company,
        location=args.location or "",
        source=source,
        snippet=args.snippet or "",
        role_buckets=role_buckets,
        filters=filters,
        ats_sources=ats_sources,
        explicit_bucket=args.role_bucket,
    )
    return {
        "first_discovered_at": discovered_at,
        "last_seen_at": iso_now(),
        "company": args.company.strip(),
        "title": args.title.strip(),
        "location": (args.location or "").strip(),
        "source": source,
        "role_bucket": result.bucket,
        "fit_score": str(result.score),
        "status": args.status.strip() or "new",
        "flags": "; ".join(result.flags),
        "url": args.url.strip(),
        "posted_at": (args.posted_at or "").strip(),
        "snippet": (args.snippet or "").strip(),
        "notes": (args.notes or "").strip(),
    }


def upsert_job_csv(inbox: Path, job: dict[str, str]) -> None:
    rows = read_jobs(inbox)
    csv_job = csv_row_from_job(job)
    for index, row in enumerate(rows):
        if row["url"] == csv_job["url"]:
            csv_job["pulled_at"] = row.get("pulled_at") or csv_job["pulled_at"]
            if row.get("posted_at") and not csv_job.get("posted_at"):
                csv_job["posted_at"] = row["posted_at"]
            rows[index] = csv_job
            break
    else:
        rows.append(csv_job)
    rows.sort(key=lambda item: item.get("pulled_at", ""), reverse=True)
    write_jobs(inbox, rows)


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def normalize_provider_job(source: str, item: dict[str, Any]) -> dict[str, str] | None:
    if source == "arbeitnow":
        posted_dt = parse_epoch(item.get("created_at", 0))
        tags = ", ".join(item.get("tags") or [])
        job_types = ", ".join(item.get("job_types") or [])
        return {
            "url": str(item.get("url") or "").strip(),
            "title": clean_text(item.get("title")),
            "company": clean_text(item.get("company_name")),
            "location": clean_text(item.get("location") or ("Remote" if item.get("remote") else "")),
            "source": source,
            "snippet": clean_text(" ".join([item.get("description") or "", tags, job_types])),
            "posted_at": posted_dt.replace(microsecond=0).isoformat(),
        }
    if source == "remoteok":
        posted = str(item.get("date") or "")
        posted_dt = parse_dt(posted) if posted else parse_epoch(item.get("epoch", 0))
        tags = ", ".join(item.get("tags") or [])
        return {
            "url": str(item.get("apply_url") or item.get("url") or "").strip(),
            "title": clean_text(item.get("position")),
            "company": clean_text(item.get("company")),
            "location": clean_text(item.get("location")),
            "source": source,
            "snippet": clean_text(" ".join([item.get("description") or "", tags])),
            "posted_at": posted_dt.replace(microsecond=0).isoformat(),
        }
    return None


def fetch_provider_jobs(source: str) -> list[dict[str, str]]:
    if source == "arbeitnow":
        payload = fetch_json("https://www.arbeitnow.com/api/job-board-api")
        return [
            job
            for item in payload.get("data", [])
            if (job := normalize_provider_job(source, item)) and job["url"] and job["title"] and job["company"]
        ]
    if source == "remoteok":
        payload = fetch_json("https://remoteok.com/api")
        return [
            job
            for item in payload[1:]
            if (job := normalize_provider_job(source, item)) and job["url"] and job["title"] and job["company"]
        ]
    raise ValueError(f"Unsupported source: {source}")




def strip_url_punctuation(url: str) -> str:
    return url.rstrip(".,;:)]}")


def extract_urls(text: str) -> list[str]:
    return [strip_url_punctuation(match.group(0)) for match in URL_PATTERN.finditer(text)]


def humanize_token(token: str) -> str:
    words = re.sub(r"[-_]+", " ", token).strip()
    return words.title() if words else token


def direct_ats_target_from_url(url: str) -> dict[str, Any] | None:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    parts = [part for part in parsed.path.split("/") if part]
    source = ""
    token = ""

    if host in {"boards.greenhouse.io", "job-boards.greenhouse.io"} and parts:
        source, token = "greenhouse", parts[0]
    elif host == "boards-api.greenhouse.io" and len(parts) >= 3 and parts[0] == "v1" and parts[1] == "boards":
        source, token = "greenhouse", parts[2]
    elif host == "jobs.lever.co" and parts:
        source, token = "lever", parts[0]
    elif host == "api.lever.co" and len(parts) >= 3 and parts[0] == "v0" and parts[1] == "postings":
        source, token = "lever", parts[2]
    elif host == "jobs.ashbyhq.com" and parts:
        source, token = "ashby", parts[0]
    elif host == "api.ashbyhq.com" and len(parts) >= 3 and parts[0] == "posting-api" and parts[1] == "job-board":
        source, token = "ashby", parts[2]
    elif host == "jobs.smartrecruiters.com" and parts:
        source, token = "smartrecruiters", parts[0]
    elif host == "api.smartrecruiters.com" and len(parts) >= 3 and parts[0] == "v1" and parts[1] == "companies":
        source, token = "smartrecruiters", parts[2]

    if not source or not token:
        return None
    token = token.strip()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", token):
        return None
    return {
        "source": source,
        "company": humanize_token(token),
        "token": token,
        "priority": 2,
        "notes": f"Discovered from ATS URL: {url}",
        "discovered_from_url": url,
    }


def load_direct_ats_targets(path: Path) -> dict[str, Any]:
    if path.exists():
        return load_json(path)
    return {
        "version": 1,
        "purpose": "Verified direct ATS targets for structured job ingestion.",
        "targets": [],
        "supported_sources": ["greenhouse", "lever", "ashby", "smartrecruiters"],
        "notes": [],
    }


def target_key(target: dict[str, Any]) -> tuple[str, str]:
    return str(target.get("source", "")).lower(), str(target.get("token", "")).lower()


def verify_direct_ats_target(target: dict[str, Any]) -> tuple[bool, int, str]:
    try:
        jobs = fetch_direct_ats_target(target)
    except Exception as exc:
        return False, 0, str(exc)
    if not jobs:
        return False, 0, "Endpoint returned zero public jobs"
    return True, len(jobs), "verified"


def render_target_discovery_report(result: dict[str, Any]) -> str:
    lines = [
        f"# Direct ATS Target Discovery - {utc_now().date().isoformat()}",
        "",
        f"Generated at: `{result['generated_at']}`",
        f"Input file: `{result['input_path']}`",
        f"Target config: `{result['targets_path']}`",
        "",
        "## Summary",
        "",
        f"- URLs found: `{result['url_count']}`",
        f"- Candidate ATS targets extracted: `{result['candidate_count']}`",
        f"- Verified targets: `{result['verified_count']}`",
        f"- Added targets: `{result['added_count']}`",
        f"- Existing targets: `{result['existing_count']}`",
        f"- Failed targets: `{result['failed_count']}`",
        "",
        "## Targets",
        "",
        "| Status | Source | Company | Token | Jobs | URL / Note |",
        "|---|---|---|---|---:|---|",
    ]
    for item in result["rows"]:
        lines.append(
            "| {status} | {source} | {company} | {token} | {jobs} | {note} |".format(
                status=md_cell(item["status"]),
                source=md_cell(item["source"]),
                company=md_cell(item["company"]),
                token=md_cell(item["token"]),
                jobs=md_cell(str(item["jobs"])),
                note=md_cell(item["note"]),
            )
        )
    return "\n".join(lines).rstrip() + "\n"


def discover_direct_ats_targets(args: argparse.Namespace) -> dict[str, Any]:
    input_path = Path(args.path)
    text = input_path.read_text(encoding="utf-8")
    urls = extract_urls(text)
    candidate_targets: dict[tuple[str, str], dict[str, Any]] = {}
    for url in urls:
        target = direct_ats_target_from_url(url)
        if target:
            candidate_targets.setdefault(target_key(target), target)

    targets_path = Path(args.targets)
    payload = load_direct_ats_targets(targets_path)
    existing = {target_key(target): target for target in payload.get("targets", [])}
    rows: list[dict[str, Any]] = []
    added_count = 0
    existing_count = 0
    verified_count = 0
    failed_count = 0

    for key, target in sorted(candidate_targets.items()):
        was_existing = key in existing
        if was_existing:
            known = existing[key]
            target["company"] = known.get("company") or target["company"]
            existing_count += 1
        if args.no_verify:
            verified, job_count, message = True, 0, "not verified (--no-verify)"
        else:
            verified, job_count, message = verify_direct_ats_target(target)
        if verified:
            verified_count += 1
            if not was_existing:
                config_target = {k: v for k, v in target.items() if k != "discovered_from_url"}
                config_target["notes"] = f"Discovered from ATS URL and verified with {job_count} public jobs."
                payload.setdefault("targets", []).append(config_target)
                existing[key] = config_target
                added_count += 1
                status = "added"
            else:
                status = "existing"
        else:
            failed_count += 1
            status = "failed"
        rows.append(
            {
                "status": status,
                "source": target["source"],
                "company": target["company"],
                "token": target["token"],
                "jobs": job_count,
                "note": target.get("discovered_from_url") or message,
            }
        )

    payload["targets"] = sorted(payload.get("targets", []), key=lambda item: (item.get("priority", 99), item.get("source", ""), item.get("company", "")))
    if added_count and not args.dry_run:
        targets_path.parent.mkdir(parents=True, exist_ok=True)
        targets_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    result = {
        "generated_at": utc_now().replace(microsecond=0).isoformat(),
        "input_path": input_path.as_posix(),
        "targets_path": targets_path.as_posix(),
        "url_count": len(urls),
        "candidate_count": len(candidate_targets),
        "verified_count": verified_count,
        "added_count": added_count if not args.dry_run else 0,
        "existing_count": existing_count,
        "failed_count": failed_count,
        "rows": rows,
    }
    return result


def normalize_direct_ats_job(target: dict[str, Any], item: dict[str, Any]) -> dict[str, str] | None:
    source = target["source"]
    company = target["company"]
    if source == "greenhouse":
        location = item.get("location") or {}
        departments = item.get("departments") or []
        department_names = ", ".join(dept.get("name", "") for dept in departments if dept.get("name"))
        return {
            "url": str(item.get("absolute_url") or "").strip(),
            "title": clean_text(item.get("title")),
            "company": company,
            "location": clean_text(location.get("name") if isinstance(location, dict) else location),
            "source": source,
            "snippet": clean_text(" ".join([item.get("content") or "", department_names])),
            "posted_at": clean_text(item.get("updated_at") or item.get("created_at")),
        }
    if source == "lever":
        categories = item.get("categories") or {}
        lists = item.get("lists") or []
        list_text = " ".join(str(part.get("content", "")) for part in lists if isinstance(part, dict))
        created = item.get("createdAt") or item.get("updatedAt") or ""
        posted_at = parse_epoch(int(created) / 1000).replace(microsecond=0).isoformat() if created else ""
        return {
            "url": str(item.get("hostedUrl") or item.get("applyUrl") or "").strip(),
            "title": clean_text(item.get("text")),
            "company": company,
            "location": clean_text(categories.get("location") if isinstance(categories, dict) else ""),
            "source": source,
            "snippet": clean_text(" ".join([item.get("descriptionPlain") or item.get("description") or "", list_text])),
            "posted_at": posted_at,
        }
    if source == "ashby":
        return {
            "url": str(item.get("jobUrl") or item.get("applyUrl") or "").strip(),
            "title": clean_text(item.get("title")),
            "company": company,
            "location": clean_text(item.get("locationName") or item.get("location") or ""),
            "source": source,
            "snippet": clean_text(item.get("descriptionPlain") or item.get("descriptionHtml") or item.get("department") or ""),
            "posted_at": clean_text(item.get("publishedAt") or item.get("updatedAt") or ""),
        }
    if source == "smartrecruiters":
        location = item.get("location") or {}
        location_text = location.get("city") or location.get("region") or location.get("country") or "" if isinstance(location, dict) else location
        return {
            "url": str(item.get("ref") or item.get("applyUrl") or "").strip(),
            "title": clean_text(item.get("name") or item.get("title")),
            "company": company,
            "location": clean_text(location_text),
            "source": source,
            "snippet": clean_text(item.get("jobAd") or item.get("description") or ""),
            "posted_at": clean_text(item.get("releasedDate") or item.get("updatedDate") or ""),
        }
    return None


def fetch_direct_ats_target(target: dict[str, Any]) -> list[dict[str, str]]:
    source = target["source"]
    token = target["token"]
    if source == "greenhouse":
        payload = fetch_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true")
        items = payload.get("jobs", [])
    elif source == "lever":
        items = fetch_json(f"https://api.lever.co/v0/postings/{token}?mode=json")
    elif source == "ashby":
        payload = fetch_json(f"https://api.ashbyhq.com/posting-api/job-board/{token}")
        items = payload.get("jobs", [])
    elif source == "smartrecruiters":
        payload = fetch_json(f"https://api.smartrecruiters.com/v1/companies/{token}/postings?limit=100")
        items = payload.get("content") or payload.get("postings") or []
    else:
        raise ValueError(f"Unsupported direct ATS source: {source}")
    jobs = []
    for item in items:
        if isinstance(item, dict):
            job = normalize_direct_ats_job(target, item)
            if job and job["url"] and job["title"] and job["company"]:
                jobs.append(job)
    return jobs


def extract_dataset_slug(source: str, item: Any) -> str:
    if isinstance(item, str):
        return item.strip()
    if not isinstance(item, dict):
        return ""
    for key in ("slug", "token", "company", "name", "id", "subdomain", "organization"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    url = item.get("url") or item.get("jobs_url") or item.get("careers_url")
    if isinstance(url, str):
        return ats_slug_from_url(source, url)
    return ""


def ats_slug_from_url(source: str, url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    parts = [part for part in parsed.path.split("/") if part]
    if source == "greenhouse" and parts:
        return parts[0]
    if source == "lever" and parts:
        return parts[0]
    if source == "ashby" and parts:
        return parts[0]
    if source == "smartrecruiters" and parts:
        return parts[0]
    if source == "workday" and "myworkdayjobs.com" in host:
        return workday_key_from_url(url)
    return ""


def workday_key_from_url(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    parts = [part for part in parsed.path.split("/") if part]
    if "myworkdayjobs.com" not in host or not parts:
        return ""
    site = parts[0]
    subdomain = host.removesuffix(".myworkdayjobs.com")
    host_parts = subdomain.split(".")
    if len(host_parts) < 2:
        return ""
    tenant = host_parts[0]
    instance = ".".join(host_parts[1:])
    return f"{tenant}|{instance}|{site}"


def company_name_from_dataset_item(source: str, slug: str, item: Any) -> str:
    if isinstance(item, dict):
        for key in ("company_name", "company", "name", "organization", "display_name"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                return clean_text(value, 120)
    if source == "workday" and "|" in slug:
        return humanize_token(slug.split("|", 1)[0])
    return humanize_token(slug)


def load_broad_ats_company_entries(
    source: str,
    cache_dir: Path,
    refresh_cache: bool = False,
) -> list[dict[str, str]]:
    if source not in BROAD_ATS_DATASETS:
        raise ValueError(f"Unsupported broad ATS source: {source}")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{source}.json"
    if refresh_cache or not cache_path.exists():
        payload = fetch_json(BROAD_ATS_DATASETS[source])
        cache_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    else:
        payload = json.loads(cache_path.read_text(encoding="utf-8"))

    if isinstance(payload, dict):
        raw_items = payload.get("companies") or payload.get("data") or payload.get("items") or []
        if not raw_items and all(isinstance(value, (str, dict)) for value in payload.values()):
            raw_items = [{"slug": key, **value} if isinstance(value, dict) else value for key, value in payload.items()]
    elif isinstance(payload, list):
        raw_items = payload
    else:
        raw_items = []

    entries: dict[str, dict[str, str]] = {}
    for item in raw_items:
        slug = extract_dataset_slug(source, item)
        if not slug:
            continue
        if source != "workday" and not SLUG_PATTERN.fullmatch(slug):
            continue
        if source == "workday" and "|" not in slug:
            continue
        entries.setdefault(
            slug.lower(),
            {
                "source": source,
                "token": slug,
                "company": company_name_from_dataset_item(source, slug, item),
            },
        )
    return sorted(entries.values(), key=lambda item: item["company"].lower())


def fetch_workday_company(entry: dict[str, str], limit: int = 20) -> list[dict[str, str]]:
    token = entry["token"]
    try:
        tenant, instance, site = token.split("|", 2)
    except ValueError:
        return []
    base_url = f"https://{tenant}.{instance}.myworkdayjobs.com"
    endpoint = f"{base_url}/wday/cxs/{tenant}/{site}/jobs"
    payload = {
        "appliedFacets": {},
        "limit": limit,
        "offset": 0,
        "searchText": "",
    }
    data = json.dumps(payload).encode("utf-8")
    response = fetch_json(endpoint, data=data, method="POST")
    items = response.get("jobPostings") or []
    jobs: list[dict[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        path = str(item.get("externalPath") or "").strip()
        url = f"{base_url}{path}" if path.startswith("/") else path
        posted = clean_text(item.get("postedOn") or item.get("startDate") or "")
        jobs.append(
            {
                "url": url,
                "title": clean_text(item.get("title")),
                "company": entry["company"],
                "location": clean_text(item.get("locationsText") or item.get("location") or ""),
                "source": "workday",
                "snippet": clean_text(" ".join(str(part) for part in item.get("bulletFields", []) if part)),
                "posted_at": posted,
            }
        )
    return [job for job in jobs if job["url"] and job["title"] and job["company"]]


def broad_entry_to_direct_target(entry: dict[str, str]) -> dict[str, str]:
    return {
        "source": entry["source"],
        "company": entry["company"],
        "token": entry["token"],
    }


def fetch_broad_ats_company(entry: dict[str, str]) -> tuple[dict[str, str], list[dict[str, str]], str]:
    try:
        if entry["source"] == "workday":
            return entry, fetch_workday_company(entry), ""
        return entry, fetch_direct_ats_target(broad_entry_to_direct_target(entry)), ""
    except Exception as exc:
        return entry, [], str(exc)


def posted_at_is_recent_or_unknown(job: dict[str, str], now: datetime, max_age_hours: int, include_undated: bool) -> bool:
    posted_at = job.get("posted_at", "")
    if not posted_at:
        return include_undated
    parsed = parse_posted_datetime(posted_at, now)
    if not parsed:
        return include_undated
    return (now - parsed).total_seconds() <= max_age_hours * 3600


def broad_seniority_risk(title: str) -> bool:
    text = normalize_text(title)
    risky_patterns = [
        r"(?<![a-z0-9])iii(?![a-z0-9])",
        r"(?<![a-z0-9])iv(?![a-z0-9])",
        r"(?<![a-z0-9])v(?![a-z0-9])",
        r"(?<![a-z0-9])expert(?![a-z0-9])",
        r"(?<![a-z0-9])lead(?![a-z0-9])",
        r"(?<![a-z0-9])senior(?![a-z0-9])",
        r"(?<![a-z0-9])sr(?![a-z0-9])",
        r"(?<![a-z0-9])staff(?![a-z0-9])",
        r"(?<![a-z0-9])principal(?![a-z0-9])",
    ]
    return any(re.search(pattern, text) for pattern in risky_patterns)


def passes_broad_shortlist_filters(record: dict[str, str], args: argparse.Namespace) -> bool:
    flags = flag_set(record)
    if "no_early_career_signal" in flags and not args.include_no_early_career_in_shortlist:
        return False
    if broad_seniority_risk(record["title"]) and not args.include_seniority_review:
        return False
    return passes_shortlist_filters(record, args)


def run_broad_ats_scan(args: argparse.Namespace) -> dict[str, Any]:
    now = utc_now()
    role_buckets = load_json(ROLE_BUCKETS_PATH)
    filters = load_json(FILTERS_PATH)
    ats_sources = load_json(ATS_SOURCES_PATH)
    selected_sources = args.sources or ["greenhouse", "lever", "ashby", "workday"]
    cache_dir = Path(args.cache_dir)

    source_stats: dict[str, dict[str, int]] = {}
    errors: list[dict[str, str]] = []
    shortlist: list[dict[str, str]] = []
    review_candidates: list[dict[str, str]] = []

    for source in selected_sources:
        source_stats[source] = {
            "companies_loaded": 0,
            "companies_scanned": 0,
            "company_errors": 0,
            "jobs_fetched": 0,
            "jobs_skipped": 0,
        }
        entries = load_broad_ats_company_entries(source, cache_dir, args.refresh_cache)
        source_stats[source]["companies_loaded"] = len(entries)
        if args.company_limit:
            entries = entries[: args.company_limit]
        if args.source_company_limit:
            entries = entries[: args.source_company_limit]
        if not entries:
            continue

        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(fetch_broad_ats_company, entry): entry for entry in entries}
            for future in as_completed(futures):
                entry, jobs, error = future.result()
                source_stats[source]["companies_scanned"] += 1
                if error:
                    source_stats[source]["company_errors"] += 1
                    if len(errors) < args.error_limit:
                        errors.append(
                            {
                                "source": source,
                                "company": entry["company"],
                                "token": entry["token"],
                                "error": error,
                            }
                        )
                    continue
                source_stats[source]["jobs_fetched"] += len(jobs)
                for job in jobs:
                    if not posted_at_is_recent_or_unknown(job, now, args.max_age_hours, args.include_undated):
                        source_stats[source]["jobs_skipped"] += 1
                        continue
                    record = make_job_record(build_namespace(job, notes=f"Imported from broad {source} ATS scan"))
                    score = score_job(
                        title=record["title"],
                        company=record["company"],
                        location=record["location"],
                        source=record["source"],
                        snippet=record["snippet"],
                        role_buckets=role_buckets,
                        filters=filters,
                        ats_sources=ats_sources,
                    )
                    record["fit_score"] = str(score.score)
                    record["role_bucket"] = score.bucket
                    record["flags"] = "; ".join(score.flags)
                    if passes_review_filters(record, args):
                        review_candidates.append(record)
                    else:
                        source_stats[source]["jobs_skipped"] += 1
                        continue
                    if passes_broad_shortlist_filters(record, args):
                        shortlist.append(record)
                        if not args.dry_run:
                            upsert_job_csv(Path(args.inbox), record)
                    elif not args.dry_run and args.write_review_to_inbox:
                        review_record = {**record, "status": "needs_review"}
                        review_record["notes"] = "Broad ATS match; review location, seniority, and fit before applying"
                        upsert_job_csv(Path(args.inbox), review_record)

    shortlist = sorted(shortlist, key=lambda item: int_or_zero(item["fit_score"]), reverse=True)[: args.limit]
    review_candidates = sorted(review_candidates, key=lambda item: int_or_zero(item["fit_score"]), reverse=True)[: args.review_limit]
    history_stats = apply_scan_history(
        args,
        [("review", review_candidates), ("shortlist", shortlist)],
        now,
    )
    return {
        "generated_at": now.replace(microsecond=0).isoformat(),
        "sources": selected_sources,
        "source_stats": source_stats,
        "imported_count": 0 if args.dry_run else len(shortlist),
        "review_count": len(review_candidates),
        "imported": shortlist,
        "review_candidates": review_candidates,
        "errors": errors,
        "history_stats": history_stats,
        "dry_run": args.dry_run,
    }


def render_broad_ats_summary(result: dict[str, Any], args: argparse.Namespace) -> str:
    lines = [
        f"# Broad ATS Scan - {utc_now().date().isoformat()}",
        "",
        f"Generated at: `{result['generated_at']}`",
        f"Inbox: `{Path(args.inbox).as_posix()}`",
        f"Dry run: `{args.dry_run}`",
        f"Max posted age: `{args.max_age_hours} hours`",
        f"Include undated postings: `{args.include_undated}`",
        f"Shortlist minimum fit score: `{args.min_score}`",
        f"Review minimum fit score: `{args.review_min_score}`",
        f"Company limit per source: `{args.source_company_limit or args.company_limit or 'none'}`",
        "Location policy: U.S. roles can enter the shortlist; India roles stay in review; other foreign roles are excluded by default.",
        "Recency grouping: 0-6, 6-12, 12-24, and 24-48 hours.",
        f"Require early-career signal for shortlist: `{not args.include_no_early_career_in_shortlist}`",
        f"Write review candidates to CSV: `{args.write_review_to_inbox and not args.dry_run}`",
        "Work authorization policy: prioritize sponsor-watchlist companies and explicit OPT/STEM OPT/E-Verify/sponsorship signals; keep no-sponsorship roles out of the shortlist inbox.",
        "",
        "## Scan History",
        "",
        f"History file: `{result.get('history_stats', {}).get('path', DEFAULT_SCAN_HISTORY.as_posix())}`",
        f"New candidates in this layer: `{result.get('history_stats', {}).get('new', 0)}`",
        f"Previously seen candidates in this layer: `{result.get('history_stats', {}).get('seen_before', 0)}`",
        f"History updated: `{result.get('history_stats', {}).get('written', False)}`",
        "",
        "## Provider Counts",
        "",
        "| Source | Companies Loaded | Companies Scanned | Company Errors | Jobs Fetched | Jobs Skipped |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for source in result["sources"]:
        stats = result["source_stats"].get(source, {})
        lines.append(
            "| {source} | {loaded} | {scanned} | {errors} | {fetched} | {skipped} |".format(
                source=source,
                loaded=stats.get("companies_loaded", 0),
                scanned=stats.get("companies_scanned", 0),
                errors=stats.get("company_errors", 0),
                fetched=stats.get("jobs_fetched", 0),
                skipped=stats.get("jobs_skipped", 0),
            )
        )
    lines.extend(["", "## Shortlist", ""])
    if args.dry_run:
        lines.append("Dry run: these were not written to the CSV inbox.")
        lines.append("")
    else:
        lines.append("These were written to the CSV inbox.")
        lines.append("")
    lines.extend(render_job_table(result["imported"]))
    lines.extend(["", "## Broader Review Candidates", ""])
    lines.append("These matched the role filters but may need location, seniority, or fit review before applying.")
    lines.append("")
    lines.extend(render_job_table(result["review_candidates"]))
    if result["errors"]:
        lines.extend(["", "## Sample Provider Errors", ""])
        lines.append("| Source | Company | Token | Error |")
        lines.append("|---|---|---|---|")
        for error in result["errors"]:
            lines.append(
                "| {source} | {company} | {token} | {message} |".format(
                    source=md_cell(error["source"]),
                    company=md_cell(error["company"]),
                    token=md_cell(error["token"]),
                    message=md_cell(error["error"][:220]),
                )
            )
    return "\n".join(lines).rstrip() + "\n"


def write_broad_ats_outputs(result: dict[str, Any], args: argparse.Namespace) -> None:
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    export_rows = result_jobs_for_export(result)
    write_result_jobs_csv(results_dir / "jobs.csv", export_rows)
    write_output(render_jobs_by_window("Broad ATS Jobs By Posted Window", export_rows), str(results_dir / "jobs-by-window.md"))
    write_output(render_broad_ats_summary(result, args), str(results_dir / "run-summary.md"))
    write_output("# Review Candidates\n\n" + "\n".join(render_job_table(result["review_candidates"])), str(results_dir / "review-candidates.md"))
    write_output("# Shortlist\n\n" + "\n".join(render_job_table(result["imported"])), str(results_dir / "shortlist.md"))


def fetch_direct_ats_jobs(args: argparse.Namespace) -> dict[str, Any]:
    now = utc_now()
    payload = load_json(Path(args.targets))
    selected_sources = set(args.sources or [])
    selected_companies = {company.lower() for company in (args.companies or [])}
    targets = payload.get("targets", [])
    fetched_by_source: dict[str, int] = {}
    skipped_by_source: dict[str, int] = {}
    shortlist: list[dict[str, str]] = []
    review_candidates: list[dict[str, str]] = []

    for target in targets:
        if selected_sources and target["source"] not in selected_sources:
            continue
        if selected_companies and target["company"].lower() not in selected_companies:
            continue
        source = target["source"]
        try:
            jobs = fetch_direct_ats_target(target)
        except Exception as exc:
            fetched_by_source[source] = fetched_by_source.get(source, 0)
            skipped_by_source[source] = skipped_by_source.get(source, 0) + 1
            continue
        fetched_by_source[source] = fetched_by_source.get(source, 0) + len(jobs)
        skipped = 0
        for job in jobs:
            if not is_recent_post(job, now, args.max_age_hours):
                skipped += 1
                continue
            record = make_job_record(build_namespace(job, notes=f"Imported from {source} direct ATS target"))
            if passes_review_filters(record, args):
                review_candidates.append(record)
            else:
                skipped += 1
                continue
            if passes_shortlist_filters(record, args):
                shortlist.append(record)
                if not getattr(args, "dry_run", False):
                    upsert_job_csv(Path(args.inbox), record)
        skipped_by_source[source] = skipped_by_source.get(source, 0) + skipped

    shortlist = sorted(shortlist, key=lambda item: int_or_zero(item["fit_score"]), reverse=True)[: args.limit]
    review_candidates = sorted(review_candidates, key=lambda item: int_or_zero(item["fit_score"]), reverse=True)[: args.review_limit]
    history_stats = apply_scan_history(
        args,
        [("review", review_candidates), ("shortlist", shortlist)],
        now,
    )
    return {
        "generated_at": now.replace(microsecond=0).isoformat(),
        "sources": sorted(fetched_by_source),
        "fetched_by_source": fetched_by_source,
        "skipped_by_source": skipped_by_source,
        "imported_count": 0 if getattr(args, "dry_run", False) else len(shortlist),
        "review_count": len(review_candidates),
        "imported": shortlist,
        "review_candidates": review_candidates,
        "history_stats": history_stats,
        "dry_run": getattr(args, "dry_run", False),
    }


def write_run_outputs(result: dict[str, Any], args: argparse.Namespace) -> None:
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    export_rows = result_jobs_for_export(result)
    write_result_jobs_csv(results_dir / "jobs.csv", export_rows)
    write_output(render_jobs_by_window("Jobs By Posted Window", export_rows), str(results_dir / "jobs-by-window.md"))
    write_output(render_run_summary(result, args), str(results_dir / "run-summary.md"))
    write_output("# Review Candidates\n\n" + "\n".join(render_job_table(result["review_candidates"])), str(results_dir / "review-candidates.md"))
    write_output(render_report(argparse.Namespace(inbox=args.inbox, output="", now="")), str(results_dir / "recent-jobs.md"))
    write_output(generate_queries(argparse.Namespace(windows=DEFAULT_SEARCH_WINDOWS)), str(results_dir / "search-links.md"))


def standard_filter_args(args: argparse.Namespace, results_dir: Path) -> dict[str, Any]:
    return {
        "inbox": args.inbox,
        "results_dir": str(results_dir),
        "limit": 50,
        "review_limit": 150,
        "min_score": 60,
        "review_min_score": 45,
        "max_age_hours": 48,
        "include_negative": False,
        "include_unclassified": False,
        "include_location_review": False,
        "include_india_in_shortlist": False,
        "include_foreign_review": False,
        "dry_run": args.dry_run,
    }


def namespace_with(base: dict[str, Any], **overrides: Any) -> argparse.Namespace:
    values = {**base, **overrides}
    return argparse.Namespace(**values)


def render_pipeline_summary(result: dict[str, Any], args: argparse.Namespace) -> str:
    lines = [
        f"# Job Discovery Pipeline - {utc_now().date().isoformat()}",
        "",
        f"Generated at: `{result['generated_at']}`",
        f"Inbox: `{Path(args.inbox).as_posix()}`",
        f"Dry run: `{args.dry_run}`",
        "",
        "## Standard Rules",
        "",
        "- Recency windows: 0-6, 6-12, 12-24, and 24-48 hours.",
        "- U.S. roles are eligible for the strict inbox shortlist.",
        "- India roles are kept in review reports by default.",
        "- Other non-U.S./non-India roles are excluded by default.",
        "- Review-only matches stay in dated reports instead of `jobs-inbox.csv`.",
        "- Scan history preserves first-seen and last-seen timestamps across runs.",
        "- F-1/OPT policy: sponsor-watchlist companies and explicit sponsorship signals are prioritized; no-sponsorship roles are not written to the shortlist inbox.",
        "",
        "## Pipeline Outputs",
        "",
        "| Layer | Shortlist | Review | New | Seen Before | Results |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for layer in result["layers"]:
        lines.append(
            "| {name} | {shortlist} | {review} | {new} | {seen} | {path} |".format(
                name=md_cell(layer["name"]),
                shortlist=layer["shortlist_count"],
                review=layer["review_count"],
                new=layer["history_new"],
                seen=layer["history_seen_before"],
                path=md_cell(layer["results_dir"]),
            )
        )
    lines.extend(
        [
            "",
            f"Search links: `{result['search_links_path']}`",
            "",
            "Use each layer's `jobs.csv`, `shortlist.md`, and `review-candidates.md` with `job-search/job-viewer.html` for grouped review.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def run_standard_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    direct_args = namespace_with(
        standard_filter_args(args, results_dir / "direct-ats"),
        targets=str(DIRECT_ATS_TARGETS_PATH),
        sources=[],
        companies=[],
        review_limit=100,
    )
    direct_result = fetch_direct_ats_jobs(direct_args)
    write_run_outputs(direct_result, direct_args)

    broad_args = namespace_with(
        standard_filter_args(args, results_dir / "broad-ats"),
        sources=["greenhouse", "lever", "ashby", "workday"],
        review_limit=150,
        include_undated=False,
        include_no_early_career_in_shortlist=False,
        include_seniority_review=False,
        write_review_to_inbox=False,
        workers=8,
        company_limit=0,
        source_company_limit=0,
        error_limit=25,
        cache_dir=str(BROAD_ATS_CACHE_DIR),
        refresh_cache=args.refresh_cache,
    )
    broad_result = run_broad_ats_scan(broad_args)
    write_broad_ats_outputs(broad_result, broad_args)

    public_args = namespace_with(
        standard_filter_args(args, results_dir / "public-search"),
        sources=["arbeitnow", "remoteok"],
        review_limit=50,
    )
    public_result = fetch_public_jobs(public_args)
    write_run_outputs(public_result, public_args)

    search_links_path = results_dir / "search-links.md"
    write_output(generate_queries(argparse.Namespace(windows=DEFAULT_SEARCH_WINDOWS)), str(search_links_path))

    result = {
        "generated_at": utc_now().replace(microsecond=0).isoformat(),
        "search_links_path": search_links_path.as_posix(),
        "layers": [
            {
                "name": "direct-ats",
                "shortlist_count": len(direct_result["imported"]),
                "review_count": len(direct_result["review_candidates"]),
                "history_new": direct_result.get("history_stats", {}).get("new", 0),
                "history_seen_before": direct_result.get("history_stats", {}).get("seen_before", 0),
                "results_dir": Path(direct_args.results_dir).as_posix(),
            },
            {
                "name": "broad-ats",
                "shortlist_count": len(broad_result["imported"]),
                "review_count": len(broad_result["review_candidates"]),
                "history_new": broad_result.get("history_stats", {}).get("new", 0),
                "history_seen_before": broad_result.get("history_stats", {}).get("seen_before", 0),
                "results_dir": Path(broad_args.results_dir).as_posix(),
            },
            {
                "name": "public-search",
                "shortlist_count": len(public_result["imported"]),
                "review_count": len(public_result["review_candidates"]),
                "history_new": public_result.get("history_stats", {}).get("new", 0),
                "history_seen_before": public_result.get("history_stats", {}).get("seen_before", 0),
                "results_dir": Path(public_args.results_dir).as_posix(),
            },
        ],
    }
    write_output(render_pipeline_summary(result, args), str(results_dir / "run-summary.md"))
    return result


def build_namespace(job: dict[str, str], status: str = "new", notes: str = "") -> argparse.Namespace:
    return argparse.Namespace(
        url=job["url"],
        title=job["title"],
        company=job["company"],
        location=job.get("location", ""),
        source=job.get("source", ""),
        role_bucket="",
        snippet=job.get("snippet", ""),
        posted_at=job.get("posted_at", ""),
        discovered_at="",
        status=status,
        notes=notes,
    )


def is_recent_post(job: dict[str, str], now: datetime, max_age_hours: int) -> bool:
    posted_at = parse_posted_datetime(job.get("posted_at", ""), now)
    if not posted_at:
        return True
    return (now - posted_at).total_seconds() <= max_age_hours * 3600


def flag_set(record: dict[str, str]) -> set[str]:
    return {flag for flag in record["flags"].split("; ") if flag}


def has_negative_flag(flags: set[str]) -> bool:
    return any(flag.startswith("negative:") for flag in flags)


def passes_review_filters(record: dict[str, str], args: argparse.Namespace) -> bool:
    flags = flag_set(record)
    if has_negative_flag(flags) and not args.include_negative:
        return False
    if "location_foreign" in flags and not getattr(args, "include_foreign_review", False):
        return False
    if "no_role_bucket_match" in flags and not args.include_unclassified:
        return False
    return int_or_zero(record["fit_score"]) >= args.review_min_score


def passes_shortlist_filters(record: dict[str, str], args: argparse.Namespace) -> bool:
    flags = flag_set(record)
    if not passes_review_filters(record, args):
        return False
    if "work_auth_blocker" in flags:
        return False
    if "location_foreign" in flags:
        return False
    if "location_india_review" in flags and not getattr(args, "include_india_in_shortlist", False):
        return False
    if "location_needs_review" in flags and not args.include_location_review:
        return False
    return int_or_zero(record["fit_score"]) >= args.min_score


def fetch_public_jobs(args: argparse.Namespace) -> dict[str, Any]:
    now = utc_now()
    sources = args.sources or ["arbeitnow", "remoteok"]
    fetched_by_source: dict[str, int] = {}
    skipped_by_source: dict[str, int] = {}
    errors: list[dict[str, str]] = []
    shortlist: list[dict[str, str]] = []
    review_candidates: list[dict[str, str]] = []

    for source in sources:
        try:
            jobs = fetch_provider_jobs(source)
        except Exception as exc:
            fetched_by_source[source] = 0
            skipped_by_source[source] = 0
            errors.append({"source": source, "error": str(exc)})
            continue
        fetched_by_source[source] = len(jobs)
        skipped = 0
        for job in jobs:
            if not is_recent_post(job, now, args.max_age_hours):
                skipped += 1
                continue
            record = make_job_record(build_namespace(job, notes=f"Imported from {source} public API"))
            if passes_review_filters(record, args):
                review_candidates.append(record)
            else:
                skipped += 1
                continue
            if passes_shortlist_filters(record, args):
                shortlist.append(record)
                if not getattr(args, "dry_run", False):
                    upsert_job_csv(Path(args.inbox), record)
            if len(review_candidates) >= args.review_limit and len(shortlist) >= args.limit:
                break
        skipped_by_source[source] = skipped
        if len(review_candidates) >= args.review_limit and len(shortlist) >= args.limit:
            break

    shortlist = sorted(shortlist, key=lambda item: int_or_zero(item["fit_score"]), reverse=True)[: args.limit]
    review_candidates = sorted(review_candidates, key=lambda item: int_or_zero(item["fit_score"]), reverse=True)[: args.review_limit]
    history_stats = apply_scan_history(
        args,
        [("review", review_candidates), ("shortlist", shortlist)],
        now,
    )

    return {
        "generated_at": now.replace(microsecond=0).isoformat(),
        "sources": sources,
        "fetched_by_source": fetched_by_source,
        "skipped_by_source": skipped_by_source,
        "imported_count": 0 if getattr(args, "dry_run", False) else len(shortlist),
        "review_count": len(review_candidates),
        "imported": shortlist,
        "review_candidates": review_candidates,
        "errors": errors,
        "history_stats": history_stats,
        "dry_run": getattr(args, "dry_run", False),
    }


def render_job_table(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return ["_No jobs matched the current filters._"]
    lines = [
        "| Fit | Company | Role | Location | Source | Link | Flags |",
        "|---:|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {fit} | {company} | {title} | {location} | {source} | {link} | {flags} |".format(
                fit=md_cell(row["fit_score"]),
                company=md_cell(row["company"]),
                title=md_cell(row["title"]),
                location=md_cell(row["location"]),
                source=md_cell(row["source"]),
                link=markdown_link("Apply", row["url"]),
                flags=md_cell(row["flags"]),
            )
        )
    return lines


def render_run_summary(result: dict[str, Any], args: argparse.Namespace) -> str:
    lines = [
        f"# Job Search Run - {utc_now().date().isoformat()}",
        "",
        f"Generated at: `{result['generated_at']}`",
        "",
        f"Inbox: `{Path(args.inbox).as_posix()}`",
        f"Dry run: `{getattr(args, 'dry_run', False)}`",
        f"Max posted age: `{args.max_age_hours} hours`",
        f"Shortlist minimum fit score: `{args.min_score}`",
        f"Review minimum fit score: `{args.review_min_score}`",
        f"Shortlist limit: `{args.limit}`",
        f"Review limit: `{args.review_limit}`",
        "Location policy: U.S. roles can enter the shortlist; India roles stay in review; other foreign roles are excluded by default.",
        "Recency grouping: 0-6, 6-12, 12-24, and 24-48 hours.",
        "Work authorization policy: prioritize sponsor-watchlist companies and explicit OPT/STEM OPT/E-Verify/sponsorship signals; keep no-sponsorship roles out of the shortlist inbox.",
        "",
        "## Scan History",
        "",
        f"History file: `{result.get('history_stats', {}).get('path', DEFAULT_SCAN_HISTORY.as_posix())}`",
        f"New candidates in this layer: `{result.get('history_stats', {}).get('new', 0)}`",
        f"Previously seen candidates in this layer: `{result.get('history_stats', {}).get('seen_before', 0)}`",
        f"History updated: `{result.get('history_stats', {}).get('written', False)}`",
        "",
        "## Provider Counts",
        "",
        "| Source | Fetched | Skipped |",
        "|---|---:|---:|",
    ]
    for source in result["sources"]:
        lines.append(f"| {source} | {result['fetched_by_source'].get(source, 0)} | {result['skipped_by_source'].get(source, 0)} |")
    lines.extend(["", "## Shortlist", ""])
    if getattr(args, "dry_run", False):
        lines.append("Dry run: these were not written to the CSV inbox.")
        lines.append("")
    else:
        lines.append("These were written to the CSV inbox.")
        lines.append("")
    lines.extend(render_job_table(result["imported"]))
    lines.extend(["", "## Broader Review Candidates", ""])
    lines.append("These are role-relevant public API matches that may need location, seniority, or fit review before applying.")
    lines.append("")
    lines.extend(render_job_table(result["review_candidates"]))
    if result.get("errors"):
        lines.extend(["", "## Provider Errors", ""])
        lines.append("| Source | Error |")
        lines.append("|---|---|")
        for error in result["errors"]:
            lines.append(
                "| {source} | {message} |".format(
                    source=md_cell(error["source"]),
                    message=md_cell(error["error"][:220]),
                )
            )
    return "\n".join(lines).rstrip() + "\n"


def generate_queries(args: argparse.Namespace) -> str:
    role_buckets = load_json(ROLE_BUCKETS_PATH)
    ats_sources = load_json(ATS_SOURCES_PATH)
    filters = load_json(FILTERS_PATH)
    windows = filters["search_windows"]
    domains = ats_sources["domains"]
    lines = [
        "# Recent Job Search Links",
        "",
        "Use these links to find fresh ATS-hosted postings. Store promising roles with `add-job`.",
        "",
    ]
    selected_windows = args.windows or list(windows)
    for _bucket, payload in role_buckets.items():
        lines.append(f"## {payload['label']}")
        query = build_query(payload["terms"], domains, filters)
        for window in selected_windows:
            if window not in windows:
                continue
            url = google_url(query, windows[window])
            lines.append(f"- [{window}]({url})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def import_json(args: argparse.Namespace) -> int:
    path = Path(args.path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise SystemExit("JSON import must be a list of job objects")
    count = 0
    for item in payload:
        namespace = argparse.Namespace(
            url=item["url"],
            title=item["title"],
            company=item["company"],
            location=item.get("location", ""),
            source=item.get("source", ""),
            role_bucket=item.get("role_bucket", ""),
            snippet=item.get("snippet", ""),
            posted_at=item.get("posted_at", ""),
            discovered_at=item.get("first_discovered_at", item.get("discovered_at", "")),
            status=item.get("status", "new"),
            notes=item.get("notes", ""),
        )
        upsert_job_csv(Path(args.inbox), make_job_record(namespace))
        count += 1
    return count


def row_recency_datetime(row: dict[str, str], now: datetime) -> datetime | None:
    posted = parse_posted_datetime(row.get("posted_at", ""), now)
    if posted:
        return posted
    try:
        return parse_dt(row["pulled_at"])
    except (KeyError, ValueError):
        return None


def fetch_recent_jobs(rows: list[dict[str, str]], now: datetime, max_age_hours: int) -> list[dict[str, str]]:
    cutoff = now.timestamp() - max_age_hours * 60 * 60
    recent = []
    for row in rows:
        recency_dt = row_recency_datetime(row, now)
        if not recency_dt:
            continue
        if recency_dt.timestamp() >= cutoff:
            recent.append(row)
    return sorted(recent, key=lambda item: row_recency_datetime(item, now) or datetime.min.replace(tzinfo=timezone.utc), reverse=True)


def age_hours(row: dict[str, str], now: datetime) -> float:
    recency_dt = row_recency_datetime(row, now)
    if not recency_dt:
        return float("inf")
    return (now - recency_dt).total_seconds() / 3600


def row_bucket(row: dict[str, str], now: datetime, filters: dict[str, Any]) -> str | None:
    age = age_hours(row, now)
    for bucket in filters["report_buckets"]:
        if bucket["min_hours"] <= age < bucket["max_hours"]:
            return bucket["label"]
    return None


def markdown_link(label: str, url: str) -> str:
    safe_label = label.replace("|", "/")
    return f"[{safe_label}]({url})"


def md_cell(value: str) -> str:
    return (value or "").replace("|", "/").replace("\n", " ").strip()


def render_report(args: argparse.Namespace) -> str:
    filters = load_json(FILTERS_PATH)
    now = parse_dt(args.now) if args.now else utc_now()
    max_report_hours = max(int(bucket["max_hours"]) for bucket in filters["report_buckets"])
    rows = fetch_recent_jobs(read_jobs(Path(args.inbox)), now, max_report_hours)
    grouped: dict[str, list[dict[str, str]]] = {bucket["label"]: [] for bucket in filters["report_buckets"]}
    for row in rows:
        label = row_bucket(row, now, filters)
        if label:
            grouped[label].append(row)

    lines = [
        f"# Recent Job Report - {now.date().isoformat()}",
        "",
        f"Generated at: `{now.replace(microsecond=0).isoformat()}`",
        "",
        f"Source inbox: `{Path(args.inbox).as_posix()}`",
        "",
        "Jobs are bucketed by `posted_at` when the source provides a parseable posted time; `pulled_at` is used only as a fallback.",
        "",
    ]

    for label, bucket_rows in grouped.items():
        lines.append(f"## {label}")
        lines.append("")
        if not bucket_rows:
            lines.append("_No jobs stored in this bucket yet._")
            lines.append("")
            continue
        lines.append("| Company | Position | Posted At | Pulled At | Link |")
        lines.append("|---|---|---|---|---|")
        for row in bucket_rows:
            lines.append(
                "| {company} | {position} | {posted_at} | {pulled_at} | {link} |".format(
                    company=md_cell(row.get("company", "")),
                    position=md_cell(row.get("position", "")),
                    posted_at=md_cell(row.get("posted_at", "")),
                    pulled_at=md_cell(row.get("pulled_at", "")),
                    link=markdown_link("Apply", row.get("url", "")),
                )
            )
        lines.append("")

    lines.append("## Search Links")
    lines.append("")
    lines.append("Use these when the inbox is empty or when doing a manual sweep:")
    lines.append("")
    lines.append(generate_queries(argparse.Namespace(windows=["0-6h", "0-12h", "0-24h", "0-48h"])))
    return "\n".join(lines).rstrip() + "\n"


def write_output(text: str, output: str | None) -> None:
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(path)
    else:
        print(text, end="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recent job discovery MVP")
    parser.add_argument("--inbox", default=str(DEFAULT_INBOX), help="CSV job inbox path")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-inbox", help="Create the CSV inbox with headers")

    pipeline = sub.add_parser("run-pipeline", help="Run the standard job-discovery pipeline with configured sources, locations, and recency windows")
    pipeline.add_argument("--dry-run", action="store_true", help="Write reports without updating jobs-inbox.csv")
    pipeline.add_argument("--refresh-cache", action="store_true", help="Refresh broad ATS company-directory caches")
    pipeline.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR / utc_now().date().isoformat() / "pipeline"))

    q = sub.add_parser("generate-queries", help="Generate recent ATS Google search links")
    q.add_argument("--windows", nargs="*", default=None, help="Window keys such as 0-6h 0-12h 0-24h 0-48h")
    q.add_argument("--output", help="Optional Markdown output path")

    add = sub.add_parser("add-job", help="Add or update one discovered job in the CSV inbox")
    add.add_argument("--url", required=True)
    add.add_argument("--title", required=True)
    add.add_argument("--company", required=True)
    add.add_argument("--location", default="")
    add.add_argument("--source", default="")
    add.add_argument("--role-bucket", default="")
    add.add_argument("--snippet", default="")
    add.add_argument("--posted-at", default="")
    add.add_argument("--discovered-at", default="")
    add.add_argument("--status", default="new")
    add.add_argument("--notes", default="")

    imp = sub.add_parser("import-json", help="Import a list of job objects into the CSV inbox")
    imp.add_argument("path")

    report = sub.add_parser("export-report", help="Export recent-job Markdown report from the CSV inbox")
    report.add_argument("--output", default=str(DEFAULT_RESULTS_DIR / utc_now().date().isoformat() / "recent-jobs.md"))
    report.add_argument("--now", default="", help="Override current time for testing")

    run = sub.add_parser("run-public-search", help="Fetch public job-board APIs, update inbox, and write run outputs")
    run.add_argument("--sources", nargs="*", choices=["arbeitnow", "remoteok"], default=["arbeitnow", "remoteok"])
    run.add_argument("--limit", type=int, default=25, help="Maximum strict shortlist jobs imported to the CSV inbox")
    run.add_argument("--review-limit", type=int, default=50, help="Maximum broader candidates written to review-candidates.md")
    run.add_argument("--min-score", type=int, default=60, help="Strict shortlist minimum score")
    run.add_argument("--review-min-score", type=int, default=50, help="Broader review-candidate minimum score")
    run.add_argument("--max-age-hours", type=int, default=48)
    run.add_argument("--include-negative", action="store_true")
    run.add_argument("--include-unclassified", action="store_true")
    run.add_argument("--include-location-review", action="store_true")
    run.add_argument("--include-india-in-shortlist", action="store_true", help="Allow India-based roles into the strict shortlist instead of review only")
    run.add_argument("--include-foreign-review", action="store_true", help="Keep non-US/non-India roles in review reports")
    run.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR / utc_now().date().isoformat()))


    discover = sub.add_parser("discover-direct-ats-targets", help="Extract and verify direct ATS targets from pasted job/search-result URLs")
    discover.add_argument("path", help="Text file containing pasted job or search-result URLs")
    discover.add_argument("--targets", default=str(DIRECT_ATS_TARGETS_PATH), help="Direct ATS target config path")
    discover.add_argument("--output", default=str(DEFAULT_RESULTS_DIR / utc_now().date().isoformat() / "direct-ats-target-discovery.md"))
    discover.add_argument("--no-verify", action="store_true", help="Extract targets without calling ATS endpoints")
    discover.add_argument("--dry-run", action="store_true", help="Write the report without updating the target config")

    direct = sub.add_parser("run-direct-ats", help="Fetch configured direct ATS targets, update inbox, and write run outputs")
    direct.add_argument("--targets", default=str(DIRECT_ATS_TARGETS_PATH), help="Direct ATS target config path")
    direct.add_argument("--sources", nargs="*", choices=["greenhouse", "lever", "ashby", "smartrecruiters"], default=[])
    direct.add_argument("--companies", nargs="*", default=[], help="Optional exact company names from the target config")
    direct.add_argument("--limit", type=int, default=50, help="Maximum strict shortlist jobs imported to the CSV inbox")
    direct.add_argument("--review-limit", type=int, default=100, help="Maximum broader candidates written to review-candidates.md")
    direct.add_argument("--min-score", type=int, default=60, help="Strict shortlist minimum score")
    direct.add_argument("--review-min-score", type=int, default=45, help="Broader review-candidate minimum score")
    direct.add_argument("--max-age-hours", type=int, default=48)
    direct.add_argument("--include-negative", action="store_true")
    direct.add_argument("--include-unclassified", action="store_true")
    direct.add_argument("--include-location-review", action="store_true")
    direct.add_argument("--include-india-in-shortlist", action="store_true", help="Allow India-based roles into the strict shortlist instead of review only")
    direct.add_argument("--include-foreign-review", action="store_true", help="Keep non-US/non-India roles in review reports")
    direct.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR / utc_now().date().isoformat() / "direct-ats"))

    broad = sub.add_parser("run-broad-ats", help="Scan broad public ATS company directories, write review reports, and optionally update inbox")
    broad.add_argument("--sources", nargs="*", choices=sorted(BROAD_ATS_DATASETS), default=["greenhouse", "lever", "ashby", "workday"])
    broad.add_argument("--limit", type=int, default=50, help="Maximum strict shortlist jobs")
    broad.add_argument("--review-limit", type=int, default=150, help="Maximum broader candidates written to review-candidates.md")
    broad.add_argument("--min-score", type=int, default=60, help="Strict shortlist minimum score")
    broad.add_argument("--review-min-score", type=int, default=45, help="Broader review-candidate minimum score")
    broad.add_argument("--max-age-hours", type=int, default=48)
    broad.add_argument("--include-undated", action="store_true", help="Include postings whose ATS feed has no parseable posted date")
    broad.add_argument("--include-negative", action="store_true")
    broad.add_argument("--include-unclassified", action="store_true")
    broad.add_argument("--include-location-review", action="store_true")
    broad.add_argument("--include-india-in-shortlist", action="store_true", help="Allow India-based roles into the strict shortlist instead of review only")
    broad.add_argument("--include-foreign-review", action="store_true", help="Keep non-US/non-India roles in review reports")
    broad.add_argument("--include-no-early-career-in-shortlist", action="store_true", help="Allow broad-scan shortlist entries without explicit early-career/new-grad/intern signals")
    broad.add_argument("--include-seniority-review", action="store_true", help="Allow seniority-risk titles such as III, Expert, Lead, Senior into the shortlist")
    broad.add_argument("--write-review-to-inbox", action="store_true", help="Also write non-shortlist review candidates to jobs-inbox.csv")
    broad.add_argument("--dry-run", action="store_true", help="Write reports without updating jobs-inbox.csv")
    broad.add_argument("--workers", type=int, default=8, help="Concurrent company fetches per source")
    broad.add_argument("--company-limit", type=int, default=0, help="Global company cap per source for quick tests")
    broad.add_argument("--source-company-limit", type=int, default=0, help="Alias for --company-limit")
    broad.add_argument("--error-limit", type=int, default=25, help="Maximum provider errors shown in the report")
    broad.add_argument("--cache-dir", default=str(BROAD_ATS_CACHE_DIR), help="Local company-directory cache")
    broad.add_argument("--refresh-cache", action="store_true", help="Refresh broad ATS company-directory caches")
    broad.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR / utc_now().date().isoformat() / "broad-ats"))
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "init-inbox":
        ensure_inbox(Path(args.inbox))
        print(Path(args.inbox))
    elif args.command == "run-pipeline":
        run_standard_pipeline(args)
    elif args.command == "generate-queries":
        write_output(generate_queries(args), args.output)
    elif args.command == "add-job":
        upsert_job_csv(Path(args.inbox), make_job_record(args))
        print("saved")
    elif args.command == "import-json":
        count = import_json(args)
        print(f"imported {count}")
    elif args.command == "export-report":
        write_output(render_report(args), args.output)
    elif args.command == "run-public-search":
        result = fetch_public_jobs(args)
        write_run_outputs(result, args)
    elif args.command == "discover-direct-ats-targets":
        result = discover_direct_ats_targets(args)
        write_output(render_target_discovery_report(result), args.output)
    elif args.command == "run-direct-ats":
        result = fetch_direct_ats_jobs(args)
        write_run_outputs(result, args)
    elif args.command == "run-broad-ats":
        result = run_broad_ats_scan(args)
        write_broad_ats_outputs(result, args)


if __name__ == "__main__":
    main()
