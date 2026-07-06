# Job Discovery Strategy

This repo should use a layered discovery system. The current public-feed scanner is useful, but it is not enough for high-volume job discovery.

## Source Priority

1. Direct ATS adapters
   - Greenhouse, Lever, Ashby, SmartRecruiters, Workday, iCIMS, and Workable should be queried directly when a company token or careers URL is known.
   - Direct ATS sources are preferred because they usually return structured job data, canonical URLs, titles, locations, departments, and sometimes posting/update dates.

2. H-1B sponsor company watchlist
   - Maintain a prioritized company list under `job-search/config/h1b-sponsor-watchlist.json`.
   - Search these companies even when they do not appear in general public feeds.
   - Treat sponsorship history as a targeting signal, not a guarantee. Every role still needs posting-level review.

3. Google/search fallback
   - Use Google queries for broad discovery across ATS domains and custom company career pages.
   - Google-backed results should be imported as `needs_review` unless they come from a parsed direct ATS adapter.

4. Public aggregator APIs
   - Arbeitnow, RemoteOK, Remotive, Adzuna, USAJOBS, and similar APIs are supplemental sources.
   - These are useful for volume but often have weaker role/location quality than direct ATS results.

## Company-Specific Career Pages

Jobs that are not backed by a known ATS should not be dropped. They should flow through a `company_specific` source path:

- Search fallback finds the career page or posting URL.
- If the page has JSON-LD `JobPosting` metadata, parse title, company, location, datePosted, employmentType, and apply URL.
- If the site has a sitemap, RSS feed, or jobs JSON endpoint, use that as a lightweight company adapter.
- If the page is plain HTML, capture the canonical URL, title, snippet, first-discovered time, and mark it `needs_review`.
- If a company-specific parser becomes valuable, promote it into a dedicated adapter.

This keeps custom startup/enterprise postings visible without pretending the parser knows more than it does.

## Filtering Rule

Ingest first, score second. Do not filter early unless the posting is clearly irrelevant or a duplicate. The inbox should preserve enough candidates for manual review, while `status` separates clean matches from review-needed matches.

Recommended statuses:

- `new`: clean shortlist candidate.
- `needs_review`: possible fit, needs location/seniority/sponsorship/manual check.
- `reviewing`: Aryan is evaluating or tailoring materials.
- `applied`: application submitted.
- `rejected`: rejected.
- `archived`: not pursuing.

## Near-Term Build Order

1. Add direct Greenhouse adapter using board tokens.
2. Add direct Lever adapter using company slugs.
3. Add direct Ashby adapter using organization slugs.
4. Add SmartRecruiters and Workday adapters.
5. Add company token discovery from Google/search results.
6. Add H-1B sponsor watchlist scans.
7. Add optional paid/search API support for Google-style broad queries.

## Research Notes

- Greenhouse Job Board API exposes public job board data without authentication for GET endpoints and supports `content=true` for full post content.
- Lever documentation points custom job site use cases to its public Postings API.
- Google Custom Search JSON API can retrieve web results programmatically, but requires a search engine ID and API key and is being phased out for existing customers by January 1, 2027.
- SerpAPI provides Google Jobs/search APIs but is a paid third-party service.
- OFLC disclosure data is the preferred official source for H-1B/LCA sponsor history and should be used to refresh the sponsor watchlist.
