# Job Search

This module helps find recently discovered roles so Aryan can manually apply without searching every job portal by hand.

The workflow is intentionally targeted and dependency-free:

- Generates high-signal Google search URLs for ATS-hosted jobs.
- Fetches public no-key job-board API leads from Arbeitnow and RemoteOK.
- Fetches configured direct ATS targets from Greenhouse, Lever, Ashby, and SmartRecruiters.
- Scans broad public ATS company directories for Greenhouse, Lever, Ashby, and Workday in dry-run or inbox-update mode.
- Writes date-partitioned job CSVs under `results/YYYY-MM-DD/<pipeline>/jobs.csv` for review and visualization.
- Keeps `jobs-inbox.csv` as a minimal manually curated inbox when jobs are intentionally imported.
- Scores jobs against Aryan's target profile.
- Writes dated run outputs under `results/YYYY-MM-DD/`.
- Leaves final application decisions manual. Chosen jobs should then enter the main `AGENTS.md` resume and cover-letter pipeline.

Freshness is based on `first_discovered_at`, not only an ATS-provided posted date. Many ATS systems do not expose reliable posted dates, and some keep stale postings in public feeds.

## Quick Start

Run the standard job-discovery pipeline:

```bash
python3 job-search/src/job_discovery.py run-pipeline
```

This runs the configured direct ATS targets, broad ATS scan, supplemental public feeds, and search-link generation. The run writes separate reports under `job-search/results/YYYY-MM-DD/pipeline/` and automatically groups candidates by posted-time windows: 0-6, 6-12, 12-24, and 24-48 hours.

Preview without updating `jobs-inbox.csv`:

```bash
python3 job-search/src/job_discovery.py run-pipeline --dry-run
```

Refresh cached broad ATS company directories when needed:

```bash
python3 job-search/src/job_discovery.py run-pipeline --refresh-cache
```

The standard pipeline covers Greenhouse, Lever, Ashby, and Workday where public company-directory data and no-auth endpoints are available. SmartRecruiters remains supported through configured direct ATS targets. By default, only roles with explicit early-career signals and U.S. location fit are eligible for the shortlist/CSV. India-based roles are allowed into review reports. Other non-U.S./non-India roles are excluded from standard review. Review-only matches stay in dated Markdown/CSV reports instead of being added to `jobs-inbox.csv`.

Open `job-search/job-viewer.html` in a browser to interactively review dated Markdown reports or CSV files. It can load one file, multiple files, or an entire local results folder through the browser file picker without uploading anything. Use it with `results/YYYY-MM-DD/<pipeline>/jobs.csv`, `shortlist.md`, `review-candidates.md`, or `jobs-inbox.csv`. The viewer shows fit scores, job links, source files, fetched dates, and posted/discovered recency filters for 6, 12, 24, and 48 hours.

Discover and verify new direct ATS targets from pasted Google/search-result URLs:

```bash
python3 job-search/src/job_discovery.py discover-direct-ats-targets job-search/results/YYYY-MM-DD/google-result-urls.txt
```

The default run now produces two layers:

- A strict shortlist imported into `job-search/jobs-inbox.csv`.
- A broader `review-candidates.md` file with role-relevant public API matches that may need manual review for location, seniority, or fit.

This avoids polluting the active CSV with junk while still showing you more than the final shortlist. To broaden a run further, add `--include-unclassified`, `--include-location-review`, or `--include-negative`.

The standard run updates `job-search/jobs-inbox.csv` only with strict shortlist matches and writes:

- `job-search/results/YYYY-MM-DD/pipeline/run-summary.md`
- `job-search/results/YYYY-MM-DD/pipeline/search-links.md`
- `job-search/results/YYYY-MM-DD/pipeline/direct-ats/jobs.csv`
- `job-search/results/YYYY-MM-DD/pipeline/direct-ats/jobs-by-window.md`
- `job-search/results/YYYY-MM-DD/pipeline/direct-ats/shortlist.md`
- `job-search/results/YYYY-MM-DD/pipeline/direct-ats/review-candidates.md`
- `job-search/results/YYYY-MM-DD/pipeline/broad-ats/jobs.csv`
- `job-search/results/YYYY-MM-DD/pipeline/broad-ats/jobs-by-window.md`
- `job-search/results/YYYY-MM-DD/pipeline/broad-ats/shortlist.md`
- `job-search/results/YYYY-MM-DD/pipeline/broad-ats/review-candidates.md`
- `job-search/results/YYYY-MM-DD/pipeline/public-search/jobs.csv`
- `job-search/results/YYYY-MM-DD/pipeline/public-search/jobs-by-window.md`
- `job-search/results/YYYY-MM-DD/pipeline/public-search/shortlist.md`
- `job-search/results/YYYY-MM-DD/pipeline/public-search/review-candidates.md`

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

The CSV intentionally contains only the fields needed for manual review:

- `company`: company name.
- `position`: job role or position title.
- `posted_at`: posting timestamp from the source when available.
- `pulled_at`: when this repo first pulled the job into the inbox.
- `url`: direct job/application link.

Fit scoring, source details, flags, and review notes belong in dated Markdown reports, not the CSV inbox.

Dated run outputs stay under `job-search/results/YYYY-MM-DD/`. The CSV inbox is the source of truth; regenerate the report whenever the inbox changes.


## Discovery Strategy

The job-search pipeline should prioritize sources in this order:

1. Direct ATS adapters: Greenhouse, Lever, Ashby, SmartRecruiters, Workday, iCIMS, and Workable.
2. H-1B sponsor company watchlist scans from `config/h1b-sponsor-watchlist.json`.
3. Google/search fallback queries for ATS pages and company-specific career pages.
4. Supplemental public job-board APIs such as Arbeitnow and RemoteOK.

Company-specific career pages that are not backed by a known ATS should still be captured through search fallback or lightweight custom parsers and marked `needs_review` when structured data is uncertain. The detailed strategy is in `research/job-discovery-strategy.md`.

Key source configs:

- `config/source-catalog.json`: broader source universe across ATS platforms, enterprise HCM systems, startup boards, remote boards, aggregators, and search-backed sources.
- `config/ats-adapters.json`: direct ATS endpoint patterns, token rules, and adapter priorities.
- `config/h1b-sponsor-watchlist.json`: prioritized H-1B sponsor watchlist seed for active company monitoring.

## Config Files

- `config/role-buckets.json`: software, data, AI/ML, and analyst-adjacent role terms.
- `config/ats-sources.json`: ATS domains and preferred sources.
- `config/filters.json`: early-career terms, location terms, positive skill terms, exclusions, and report buckets.

Default public, direct ATS, and broad ATS runs use `--max-age-hours 48` so reports focus on jobs posted in the last two days. Review reports bucket jobs into 0-6, 6-12, 12-24, and 24-48 hour windows when posted timestamps or relative posted strings are parseable. Default `run-public-search` thresholds are `--min-score 60` for the strict CSV shortlist and `--review-min-score 50` for broader review candidates.

## Research Notes

- `research/ats-query-chat.txt`: raw research notes from the job-search query planning conversation.
- `research/job-discovery-strategy.md`: layered discovery architecture and implementation order.
- `research/expanded-job-source-audit.md`: expanded ATS, job-board, aggregator, and company-specific source audit.
- `research/direct-ats-pull-playbook.md`: exact workflow for using search to discover ATS board tokens, validating them, and ingesting structured postings.

The Google `qdr` filters are useful for finding recently indexed pages, but they do not always prove the job was posted in that exact window. The report therefore uses `first_discovered_at` as the operational freshness signal and keeps job links manual-reviewable before applying.

## Current Boundaries

This build does not scrape Google result pages. It generates search links, fetches public no-key provider data from Arbeitnow and RemoteOK, discovers direct ATS targets from pasted URLs, and fetches configured Greenhouse, Lever, Ashby, and SmartRecruiters targets through structured endpoints. Workday, iCIMS, Workable, Oracle, SAP SuccessFactors, ADP, BambooHR, Jobvite, and company-specific career pages still need dedicated adapters or manual-review imports before they can be treated as reliable structured sources.
