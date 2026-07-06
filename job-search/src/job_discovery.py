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
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INBOX = ROOT / "jobs-inbox.csv"
DEFAULT_RESULTS_DIR = ROOT / "results"
ROLE_BUCKETS_PATH = ROOT / "config" / "role-buckets.json"
ATS_SOURCES_PATH = ROOT / "config" / "ats-sources.json"
FILTERS_PATH = ROOT / "config" / "filters.json"
DIRECT_ATS_TARGETS_PATH = ROOT / "config" / "direct-ats-targets.json"
URL_PATTERN = re.compile(r'https?://[^\s<>)\"\']+')

CSV_FIELDS = [
    "first_discovered_at",
    "last_seen_at",
    "company",
    "title",
    "location",
    "source",
    "role_bucket",
    "fit_score",
    "status",
    "flags",
    "url",
    "posted_at",
    "snippet",
    "notes",
]


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


def parse_epoch(value: Any) -> datetime:
    return datetime.fromtimestamp(int(value), tz=timezone.utc)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_json(url: str) -> Any:
    request = Request(url, headers={"User-Agent": "career-ops-job-search"})
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
) -> ScoreResult:
    text = normalize_text(title, company, location, source, snippet)
    title_text = normalize_text(title)
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

    if any(contains_term(text, term) for term in filters["location_terms"]):
        score += 10
    else:
        flags.append("location_needs_review")

    matched_skills = [term for term in filters["positive_skill_terms"] if contains_term(text, term)]
    score += min(20, len(matched_skills) * 2)

    if source in ats_sources.get("preferred_sources", []):
        score += 5

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
            rows.append({field: (row.get(field) or "").strip() for field in CSV_FIELDS})
        return rows


def write_jobs(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in CSV_FIELDS})


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
    for index, row in enumerate(rows):
        if row["url"] == job["url"]:
            job["first_discovered_at"] = row["first_discovered_at"] or job["first_discovered_at"]
            if row["status"] and row["status"] != "new":
                job["status"] = row["status"]
            if row["notes"] and not job["notes"]:
                job["notes"] = row["notes"]
            rows[index] = job
            break
    else:
        rows.append(job)
    rows.sort(key=lambda item: (int_or_zero(item.get("fit_score", "")), item["first_discovered_at"]), reverse=True)
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
                upsert_job_csv(Path(args.inbox), record)
            else:
                review_record = {**record, "status": "needs_review"}
                review_record["notes"] = "Direct ATS match; review location, seniority, and fit before applying"
                upsert_job_csv(Path(args.inbox), review_record)
        skipped_by_source[source] = skipped_by_source.get(source, 0) + skipped

    shortlist = sorted(shortlist, key=lambda item: int_or_zero(item["fit_score"]), reverse=True)[: args.limit]
    review_candidates = sorted(review_candidates, key=lambda item: int_or_zero(item["fit_score"]), reverse=True)[: args.review_limit]
    return {
        "generated_at": now.replace(microsecond=0).isoformat(),
        "sources": sorted(fetched_by_source),
        "fetched_by_source": fetched_by_source,
        "skipped_by_source": skipped_by_source,
        "imported_count": len(shortlist),
        "review_count": len(review_candidates),
        "imported": shortlist,
        "review_candidates": review_candidates,
    }


def write_run_outputs(result: dict[str, Any], args: argparse.Namespace) -> None:
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    write_output(render_run_summary(result, args), str(results_dir / "run-summary.md"))
    write_output("# Review Candidates\n\n" + "\n".join(render_job_table(result["review_candidates"])), str(results_dir / "review-candidates.md"))
    write_output(render_report(argparse.Namespace(inbox=args.inbox, output="", now="")), str(results_dir / "recent-jobs.md"))
    write_output(generate_queries(argparse.Namespace(windows=["0-6h", "0-12h", "0-18h", "0-24h"])), str(results_dir / "search-links.md"))


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
    try:
        posted_at = parse_dt(job["posted_at"])
    except (KeyError, ValueError):
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
    if "no_role_bucket_match" in flags and not args.include_unclassified:
        return False
    return int_or_zero(record["fit_score"]) >= args.review_min_score


def passes_shortlist_filters(record: dict[str, str], args: argparse.Namespace) -> bool:
    flags = flag_set(record)
    if not passes_review_filters(record, args):
        return False
    if "location_needs_review" in flags and not args.include_location_review:
        return False
    return int_or_zero(record["fit_score"]) >= args.min_score


def fetch_public_jobs(args: argparse.Namespace) -> dict[str, Any]:
    now = utc_now()
    sources = args.sources or ["arbeitnow", "remoteok"]
    fetched_by_source: dict[str, int] = {}
    skipped_by_source: dict[str, int] = {}
    shortlist: list[dict[str, str]] = []
    review_candidates: list[dict[str, str]] = []

    for source in sources:
        jobs = fetch_provider_jobs(source)
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
                upsert_job_csv(Path(args.inbox), record)
            else:
                review_record = {**record, "status": "needs_review"}
                review_record["notes"] = "Broader public API match; review location, seniority, and fit before applying"
                upsert_job_csv(Path(args.inbox), review_record)
            if len(review_candidates) >= args.review_limit and len(shortlist) >= args.limit:
                break
        skipped_by_source[source] = skipped
        if len(review_candidates) >= args.review_limit and len(shortlist) >= args.limit:
            break

    shortlist = sorted(shortlist, key=lambda item: int_or_zero(item["fit_score"]), reverse=True)[: args.limit]
    review_candidates = sorted(review_candidates, key=lambda item: int_or_zero(item["fit_score"]), reverse=True)[: args.review_limit]

    return {
        "generated_at": now.replace(microsecond=0).isoformat(),
        "sources": sources,
        "fetched_by_source": fetched_by_source,
        "skipped_by_source": skipped_by_source,
        "imported_count": len(shortlist),
        "review_count": len(review_candidates),
        "imported": shortlist,
        "review_candidates": review_candidates,
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
        f"Max posted age: `{args.max_age_hours} hours`",
        f"Shortlist minimum fit score: `{args.min_score}`",
        f"Review minimum fit score: `{args.review_min_score}`",
        f"Shortlist limit: `{args.limit}`",
        f"Review limit: `{args.review_limit}`",
        f"Include negative matches: `{args.include_negative}`",
        f"Include unclassified roles: `{args.include_unclassified}`",
        f"Include location-review roles in shortlist: `{args.include_location_review}`",
        "",
        "## Provider Counts",
        "",
        "| Source | Fetched | Skipped |",
        "|---|---:|---:|",
    ]
    for source in result["sources"]:
        lines.append(f"| {source} | {result['fetched_by_source'].get(source, 0)} | {result['skipped_by_source'].get(source, 0)} |")
    lines.extend(["", "## Shortlist Imported To CSV", ""])
    lines.extend(render_job_table(result["imported"]))
    lines.extend(["", "## Broader Review Candidates", ""])
    lines.append("These are role-relevant public API matches that may need location, seniority, or fit review before applying.")
    lines.append("")
    lines.extend(render_job_table(result["review_candidates"]))
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


def fetch_recent_jobs(rows: list[dict[str, str]], now: datetime) -> list[dict[str, str]]:
    cutoff = now.timestamp() - 24 * 60 * 60
    recent = []
    for row in rows:
        if row.get("status") == "archived":
            continue
        try:
            discovered = parse_dt(row["first_discovered_at"])
        except ValueError:
            continue
        if discovered.timestamp() >= cutoff:
            recent.append(row)
    return sorted(
        recent,
        key=lambda item: (int_or_zero(item.get("fit_score", "")), item.get("first_discovered_at", "")),
        reverse=True,
    )


def age_hours(row: dict[str, str], now: datetime) -> float:
    return (now - parse_dt(row["first_discovered_at"])).total_seconds() / 3600


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
    rows = fetch_recent_jobs(read_jobs(Path(args.inbox)), now)
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
        "Jobs are bucketed by `first_discovered_at`, which is more reliable than ATS posted dates for freshness.",
        "",
    ]

    for label, bucket_rows in grouped.items():
        lines.append(f"## {label}")
        lines.append("")
        if not bucket_rows:
            lines.append("_No jobs stored in this bucket yet._")
            lines.append("")
            continue
        lines.append("| Fit | Company | Role | Location | Source | Bucket | Status | Link | Flags | Notes |")
        lines.append("|---:|---|---|---|---|---|---|---|---|---|")
        for row in bucket_rows:
            lines.append(
                "| {fit} | {company} | {title} | {location} | {source} | {role_bucket} | {status} | {link} | {flags} | {notes} |".format(
                    fit=md_cell(row["fit_score"]),
                    company=md_cell(row["company"]),
                    title=md_cell(row["title"]),
                    location=md_cell(row["location"]),
                    source=md_cell(row["source"]),
                    role_bucket=md_cell(row["role_bucket"]),
                    status=md_cell(row["status"]),
                    link=markdown_link("Apply", row["url"]),
                    flags=md_cell(row["flags"]),
                    notes=md_cell(row["notes"]),
                )
            )
        lines.append("")

    lines.append("## Search Links")
    lines.append("")
    lines.append("Use these when the inbox is empty or when doing a manual sweep:")
    lines.append("")
    lines.append(generate_queries(argparse.Namespace(windows=["0-6h", "0-12h", "0-18h", "0-24h"])))
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

    q = sub.add_parser("generate-queries", help="Generate recent ATS Google search links")
    q.add_argument("--windows", nargs="*", default=None, help="Window keys such as 0-6h 0-12h 0-18h 0-24h")
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
    run.add_argument("--max-age-hours", type=int, default=168)
    run.add_argument("--include-negative", action="store_true")
    run.add_argument("--include-unclassified", action="store_true")
    run.add_argument("--include-location-review", action="store_true")
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
    direct.add_argument("--max-age-hours", type=int, default=720)
    direct.add_argument("--include-negative", action="store_true")
    direct.add_argument("--include-unclassified", action="store_true")
    direct.add_argument("--include-location-review", action="store_true")
    direct.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR / utc_now().date().isoformat() / "direct-ats"))
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "init-inbox":
        ensure_inbox(Path(args.inbox))
        print(Path(args.inbox))
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


if __name__ == "__main__":
    main()
