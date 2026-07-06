# Job Discovery

This module helps find recently discovered roles so Aryan can manually apply without searching every job portal by hand.

The MVP is intentionally targeted and dependency-free:

- Generates high-signal Google search URLs for ATS-hosted jobs.
- Stores discovered jobs in `jobs-inbox.csv`, which can be opened and edited directly in VS Code.
- Scores jobs against Aryan's target profile.
- Exports a Markdown report partitioned into `0-6`, `6-12`, `12-18`, and `18-24` hour buckets.
- Leaves final application decisions manual. Chosen jobs should then enter the main `AGENTS.md` resume and cover-letter pipeline.

Freshness is based on `first_discovered_at`, not only an ATS-provided posted date. Many ATS systems do not expose reliable posted dates, and some keep stale postings in public feeds.

## Quick Start

Generate search links:

```bash
python3 job-discovery/src/job_discovery.py generate-queries --output job-discovery/reports/search-links.md
```

Initialize the editable CSV inbox:

```bash
python3 job-discovery/src/job_discovery.py init-inbox
```

Add a promising role manually:

```bash
python3 job-discovery/src/job_discovery.py add-job \
  --url "https://jobs.ashbyhq.com/example/software-engineer-new-grad" \
  --company "Example Co" \
  --title "Software Engineer, New Grad" \
  --location "Remote, United States" \
  --snippet "Python React AWS entry-level software engineering role"
```

Export the recent-job report:

```bash
python3 job-discovery/src/job_discovery.py export-report
```

## Where Jobs Live

Use `job-discovery/jobs-inbox.csv` as the source of truth. This file is intentionally tracked and human-readable so it can be opened in VS Code, edited, sorted, and committed when useful.

Important columns:

- `first_discovered_at`: when this repo first found or added the job.
- `fit_score`: deterministic fit score from the local rules.
- `status`: use values like `new`, `reviewing`, `applied`, `rejected`, `archived`, or `needs_review`.
- `flags`: fit/risk notes from the scoring rules.
- `notes`: your manual notes about whether the job is worth applying to.

Generated Markdown reports stay under `job-discovery/reports/`. Reports are local generated files by default; regenerate them whenever the inbox changes.

## Config Files

- `config/role-buckets.json`: software, data, AI/ML, and analyst-adjacent role terms.
- `config/ats-sources.json`: ATS domains and preferred sources.
- `config/filters.json`: early-career terms, location terms, positive skill terms, exclusions, and report buckets.

## Research Notes

- `research/ats-query-chat.txt`: raw research notes from the job-search query planning conversation.

The Google `qdr` filters are useful for finding recently indexed pages, but they do not always prove the job was posted in that exact window. The report therefore uses `first_discovered_at` as the operational freshness signal and keeps job links manual-reviewable before applying.

## Current Boundaries

This first build does not scrape Google result pages. It generates search links and provides the CSV/reporting foundation. The next practical step is adding a search API ingestion path or ATS-specific providers for Greenhouse, Lever, Ashby, Workday, and SmartRecruiters.
