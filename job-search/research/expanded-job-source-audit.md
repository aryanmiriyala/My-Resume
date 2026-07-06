# Expanded Job Source Audit

The original adapter list was not complete. It covered the highest-yield tech ATS platforms, but a broad job-discovery engine needs a larger source universe.

## Confirmed / High-Priority Structured Sources

- Greenhouse: public Job Board API, no authentication for GET endpoints, supports `content=true` for full job content.
- Lever: public postings workflow is intended for custom job sites and job posting use cases.
- SmartRecruiters: developer documentation is available for platform/postings APIs.
- Workable: developer API exists for showing jobs and integrating recruiting workflows.
- BambooHR: official job summaries API exists, but it is authenticated, so public careers pages need separate parsing.
- Teamtailor and Recruitee: developer docs exist and should be treated as second-wave adapters after Greenhouse/Lever/Ashby.

## Important Enterprise / Variable Sources

These are common on company career sites but usually need tenant-specific parsers or search fallback:

- Workday
- iCIMS
- Oracle Recruiting Cloud / Oracle HCM
- SAP SuccessFactors
- Dayforce / Ceridian
- UKG
- ADP
- Jobvite
- Paylocity
- Paycom
- Rippling

## Important Job Boards / Aggregators

These are not ATS adapters, but they expand scope:

- Google Search / Google Jobs
- SerpAPI or similar search provider
- LinkedIn
- Indeed
- Glassdoor
- ZipRecruiter
- Dice
- Built In
- Wellfound
- YC Work at a Startup
- Handshake
- Simplify
- HiringCafe
- Otta / Welcome to the Jungle
- RemoteOK
- Remotive
- We Work Remotely
- Arbeitnow
- Adzuna
- USAJOBS
- Hacker News Who is Hiring

## Practical Rule

Do not rely on any single source. The system should ingest from many sources, deduplicate by canonical URL/company/title/location, then score and status the jobs. Broad sources should default to `needs_review`; direct ATS parsed roles can become `new` when they match role, location, and seniority filters.

## Implementation Direction

1. Build Greenhouse and Lever direct adapters first because they are common, structured, and high-yield.
2. Add Ashby and SmartRecruiters next for startup and modern tech coverage.
3. Add Workday/iCIMS/SAP/Oracle as enterprise parsers with conservative `needs_review` status.
4. Add search-backed import for your broad Google query so search results can discover ATS/company tokens.
5. Add source-specific boards and aggregators after deduping is solid.
6. Refresh H-1B sponsor targets from official OFLC disclosure data, then actively scan those company career pages.
