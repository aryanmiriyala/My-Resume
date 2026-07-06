# Career Ops

This repository has two active workflows:

1. **Job Discovery**: find recently posted roles and keep a clean CSV inbox for manual review.
2. **Application Packages**: create tailored resumes, cover letters, tailoring notes, PDFs, and ATS-style alignment checks for selected roles.

The detailed operating rules live in `AGENTS.md`.

## Start Here

- Want to find jobs? Use `job-search/`.
- Want to apply to a specific job? Use `application-packages/<Company>/<Role>/`.
- Want to update the source material used in resumes, cover letters, LinkedIn, or Handshake? Use `profile/`.
- Want the canonical master resume? Use `master-documents/master-resume/resume.tex`.

## Folder Map

| Path | Purpose |
|---|---|
| `profile/` | Source-of-truth career material: experience, projects, skills, LinkedIn copy, bullet bank, resume rules, and cover-letter language. |
| `master-documents/` | Canonical master resume and reusable cover-letter template. |
| `application-packages/` | One folder per company/role with job description, tailored resume, cover letter, tailoring notes, and submission artifacts. |
| `job-search/` | Job-discovery tooling, ATS source configs, research notes, dated search results, and the clean `jobs-inbox.csv`. |
| `operations/` | Application tracker only. |
| `automation/` | Application package validation scripts. |
| `templates/` | Reusable job-description, tailoring-notes, and application-pipeline prompt templates. |

## Main Commands

Validate an application package:

```bash
python3 automation/validate_application_package.py application-packages/<Company>/<Role>
```

Run direct ATS job discovery after target boards are configured:

```bash
python3 job-search/src/job_discovery.py run-direct-ats
```

Generate search links for finding more ATS-hosted jobs:

```bash
python3 job-search/src/job_discovery.py generate-queries
```

## Canonical Resume

The current master resume source is:

- `master-documents/master-resume/resume.tex`

Tailored resumes belong inside `application-packages/<Company>/<Role>/`. Do not create duplicate master resumes.

## Generated Files

PDFs and DOCX files are usually generated artifacts. Application-package PDFs may stay when they are ready-to-submit artifacts. LaTeX build files, `.DS_Store`, `__pycache__`, and local scratch files should not be committed.

Based off of [sb2nov/resume](https://github.com/sb2nov/resume/).
