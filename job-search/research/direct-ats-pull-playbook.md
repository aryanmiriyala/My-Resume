# Direct ATS Pull Playbook

The best current approach for this repo is not to scrape rendered job pages. Use search as a discovery layer, then pull structured job data from ATS-backed public endpoints whenever possible.

## Source Findings

- Greenhouse is the strongest structured source. Its Job Board API exposes a JSON representation of published jobs, and its documentation says job-board GET data is publicly available without authentication. Use `https://boards-api.greenhouse.io/v1/boards/<board_token>/jobs?content=true` so the feed includes full job content, department, and office data.
- Lever public postings can be discovered from `jobs.lever.co/<company>` URLs and pulled through the public postings JSON endpoint `https://api.lever.co/v0/postings/<company>?mode=json`. The official developer documentation documents posting objects with fields such as `createdAt`, `updatedAt`, and posting state, but the public job-site endpoint still needs live endpoint validation per company.
- Ashby public boards expose structured job-board JSON through `https://api.ashbyhq.com/posting-api/job-board/<org>`. Treat this as an observed public endpoint and validate every organization slug before adding it to the target config.
- SmartRecruiters publishes company posting feeds through company slugs. Use `https://api.smartrecruiters.com/v1/companies/<company>/postings?limit=100` and validate each company token before adding it.
- Workable, Workday, iCIMS, Oracle, SAP SuccessFactors, ADP, BambooHR, Jobvite, and company-specific career pages need separate adapters because their public surfaces vary more by employer. Add them only after endpoint behavior is verified.

## Pipeline

1. Generate Google search links from `job-search/src/job_discovery.py generate-queries`.
2. Open the links manually or through a search API and collect promising ATS job URLs.
3. Save those URLs into a text file, for example `job-search/results/YYYY-MM-DD/google-result-urls.txt`.
4. Run `discover-direct-ats-targets` on that file. This extracts board tokens from Greenhouse, Lever, Ashby, and SmartRecruiters URLs, validates each token by calling the structured endpoint, and merges verified targets into `job-search/config/direct-ats-targets.json`.
5. Run `run-direct-ats` to ingest jobs from all verified targets into `job-search/jobs-inbox.csv` and dated result reports.
6. Review `jobs-inbox.csv` manually before deciding which application package to create.

## Commands

```bash
python3 job-search/src/job_discovery.py generate-queries --output job-search/results/YYYY-MM-DD/search-links.md
python3 job-search/src/job_discovery.py discover-direct-ats-targets job-search/results/YYYY-MM-DD/google-result-urls.txt
python3 job-search/src/job_discovery.py run-direct-ats
```

## Why This Works Better

Search engines are useful for breadth, but their result pages are not a reliable source of structured job metadata. Direct ATS APIs are better for this repo because they return consistent fields, full descriptions, canonical apply URLs, and company-wide feeds. The search fallback should be used to discover more company boards, not as the primary job-data source.
