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
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INBOX = ROOT / "jobs-inbox.csv"
DEFAULT_REPORT_DIR = ROOT / "reports"
ROLE_BUCKETS_PATH = ROOT / "config" / "role-buckets.json"
ATS_SOURCES_PATH = ROOT / "config" / "ats-sources.json"
FILTERS_PATH = ROOT / "config" / "filters.json"

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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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
    report.add_argument("--output", default=str(DEFAULT_REPORT_DIR / f"recent-jobs-{utc_now().date().isoformat()}.md"))
    report.add_argument("--now", default="", help="Override current time for testing")
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


if __name__ == "__main__":
    main()
