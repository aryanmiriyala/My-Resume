# Job Search

This module helps find recently discovered roles so Aryan can manually apply without searching every job portal by hand.

The workflow is intentionally targeted and dependency-free:

- Generates high-signal Google search URLs for ATS-hosted jobs.
- Fetches public no-key job-board API leads from Arbeitnow and RemoteOK.
- Stores discovered jobs in `jobs-inbox.csv`, which can be opened and edited directly in VS Code.
- Scores jobs against Aryan's target profile.
- Writes dated run outputs under `results/YYYY-MM-DD/`.
- Leaves final application decisions manual. Chosen jobs should then enter the main `AGENTS.md` resume and cover-letter pipeline.

Freshness is based on `first_discovered_at`, not only an ATS-provided posted date. Many ATS systems do not expose reliable posted dates, and some keep stale postings in public feeds.

## Quick Start

Run a public job-search pass:

```bash
python3 job-search/src/job_discovery.py run-public-search
```

The default run now produces two layers:

- A strict shortlist imported into `job-search/jobs-inbox.csv`.
- A broader `review-candidates.md` file with role-relevant public API matches that may need manual review for location, seniority, or fit.

This avoids polluting the active CSV with junk while still showing you more than the final shortlist. To broaden a run further, add `--include-unclassified`, `--include-location-review`, or `--include-negative`.

This updates `job-search/jobs-inbox.csv` and writes:

- `job-search/results/YYYY-MM-DD/run-summary.md`
- `job-search/results/YYYY-MM-DD/review-candidates.md`
- `job-search/results/YYYY-MM-DD/recent-jobs.md`
- `job-search/results/YYYY-MM-DD/search-links.md`

Generate search links only:

```bash
python3 job-search/src/job_discovery.py generate-queries --output job-search/results/YYYY-MM-DD/search-links.md
```

Initialize the editable CSV inbox:

```bash
python3 job-search/src/job_discovery.py init-inbox
```

Add a promising role manually:

```bash
python3 job-search/src/job_discovery.py add-job \
  --url "https://jobs.ashbyhq.com/example/software-engineer-new-grad" \
  --company "Example Co" \
  --title "Software Engineer, New Grad" \
  --location "Remote, United States" \
  --snippet "Python React AWS entry-level software engineering role"
```

Export the recent-job report:

```bash
python3 job-search/src/job_discovery.py export-report
```

## Where Jobs Live

Use `job-search/jobs-inbox.csv` as the source of truth. This file is intentionally tracked and human-readable so it can be opened in VS Code, edited, sorted, and committed when useful.

Important columns:

- `first_discovered_at`: when this repo first found or added the job.
- `fit_score`: deterministic fit score from the local rules.
- `status`: use values like `new`, `reviewing`, `applied`, `rejected`, `archived`, or `needs_review`.
- `flags`: fit/risk notes from the scoring rules.
- `notes`: your manual notes about whether the job is worth applying to.

Dated run outputs stay under `job-search/results/YYYY-MM-DD/`. The CSV inbox is the source of truth; regenerate the report whenever the inbox changes.


## Discovery Strategy

The job-search pipeline should prioritize sources in this order:

1. Direct ATS adapters: Greenhouse, Lever, Ashby, SmartRecruiters, Workday, iCIMS, and Workable.
2. H-1B sponsor company watchlist scans from `config/h1b-sponsor-watchlist.json`.
3. Google/search fallback queries for ATS pages and company-specific career pages.
4. Supplemental public job-board APIs such as Arbeitnow and RemoteOK.

Company-specific career pages that are not backed by a known ATS should still be captured through search fallback or lightweight custom parsers and marked `needs_review` when structured data is uncertain. The detailed strategy is in `research/job-discovery-strategy.md`.

Key source configs:

- `config/ats-adapters.json`: direct ATS endpoint patterns, token rules, and adapter priorities.
- `config/h1b-sponsor-watchlist.json`: prioritized H-1B sponsor watchlist seed for active company monitoring.

## Config Files

- `config/role-buckets.json`: software, data, AI/ML, and analyst-adjacent role terms.
- `config/ats-sources.json`: ATS domains and preferred sources.
- `config/filters.json`: early-career terms, location terms, positive skill terms, exclusions, and report buckets.

Default `run-public-search` thresholds: `--min-score 60` for the strict CSV shortlist, `--review-min-score 50` for broader review candidates, and `--max-age-hours 168`. Use `--max-age-hours 24` when you want only the last day of provider-posted jobs.

## Research Notes

- `research/ats-query-chat.txt`: raw research notes from the job-search query planning conversation.

The Google `qdr` filters are useful for finding recently indexed pages, but they do not always prove the job was posted in that exact window. The report therefore uses `first_discovered_at` as the operational freshness signal and keeps job links manual-reviewable before applying.

## Current Boundaries

This build does not scrape Google result pages. It generates search links, fetches public no-key provider data from Arbeitnow and RemoteOK, and provides the CSV/results foundation. A future build can add dedicated providers for Greenhouse, Lever, Ashby, Workday, and SmartRecruiters.
