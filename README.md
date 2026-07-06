# Career Materials and Application Operations

This repository stores Aryan Miriyala's master resume, career source material, targeted job-application packages, and job-search operations tooling.

The workflow is defined in `AGENTS.md`. Future resume and cover-letter work should follow that pipeline.

Before an application package is treated as ready, run:

```bash
python3 scripts/validate_application_package.py applications/<Company>/<Role>
```

The validator checks required application files, the one-page resume PDF rule, ATS/alignment sections in `tailoring-notes.md`, required internship experience markers, cover-letter submission artifacts, and leftover LaTeX build files.

## Structure

- `source/master-resume/`: canonical general resume source and PDF.
- `source/master-cover-letter/`: reusable cover-letter template.
- `career-materials/`: comprehensive experience, projects, skills, bullet banks, and tailoring guidance.
- `applications/<Company>/<Role>/`: tailored resume source, cover-letter source/artifact, job description, and notes for each application.
- `application-management/`: application tracker and email-monitoring rules.
- `job-discovery/`: recent-job discovery tooling for ATS search links, local job storage, scoring, and recency-bucket reports.
- `templates/`: reusable scaffolds for job descriptions, tailoring notes, and the new-application prompt.
- `scripts/validate_application_package.py`: package validator for the application pipeline.

## Current Canonical Resume

The current June 2026 resume is the canonical resume source:

- `source/master-resume/resume.tex`

Generated PDFs are build artifacts by default. Create them when needed for applications, but do not keep duplicate binary copies in the repo unless explicitly requested. Cover-letter PDFs or DOCX files may be committed when they are the requested submission artifact.

## Current Rule

There should be one master resume source: `source/master-resume/resume.tex`. Tailored application resumes can be created inside `applications/<Company>/<Role>/` after proposed changes are approved.

Based off of [sb2nov/resume](https://github.com/sb2nov/resume/).
