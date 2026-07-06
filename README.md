# Career Ops

This repository stores Aryan Miriyala's career source material, master resume and cover-letter documents, targeted job-application packages, job-search tooling, and application operations.

The workflow is defined in `AGENTS.md`. Future resume and cover-letter work should follow that pipeline.

Before an application package is treated as ready, run:

```bash
python3 automation/validate_application_package.py application-packages/<Company>/<Role>
```

The validator checks required application files, the one-page resume PDF rule, ATS/alignment sections in `tailoring-notes.md`, required internship experience markers, cover-letter submission artifacts, and leftover LaTeX build files.

## Structure

- `master-documents/master-resume/`: canonical general resume source and PDF.
- `master-documents/master-cover-letter/`: reusable cover-letter template.
- `profile/`: comprehensive experience, projects, skills, bullet banks, LinkedIn language, and tailoring guidance.
- `application-packages/<Company>/<Role>/`: tailored resume source, cover-letter source/artifact, job description, and notes for each application.
- `operations/`: application tracker and email-monitoring rules.
- `job-search/`: recent-job discovery tooling for ATS search links, a VS Code-editable CSV job inbox, scoring, and recency-bucket reports.
- `templates/`: reusable scaffolds for job descriptions, tailoring notes, and the new-application prompt.
- `automation/validate_application_package.py`: package validator for the application pipeline.

## Current Canonical Resume

The current June 2026 resume is the canonical resume source:

- `master-documents/master-resume/resume.tex`

Generated PDFs are build artifacts by default. Create them when needed for applications, but do not keep duplicate binary copies in the repo unless explicitly requested. Cover-letter PDFs or DOCX files may be committed when they are the requested submission artifact.

## Current Rule

There should be one master resume source: `master-documents/master-resume/resume.tex`. Tailored application resumes can be created inside `application-packages/<Company>/<Role>/` after proposed changes are approved.

Based off of [sb2nov/resume](https://github.com/sb2nov/resume/).
