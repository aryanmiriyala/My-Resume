# Resume and Application Materials

This repository stores Aryan Miriyala's master resume, career source material, and targeted job-application packages.

The workflow is defined in `AGENTS.md`. Future resume and cover-letter work should follow that pipeline.

## Structure

- `source/master-resume/`: canonical general resume source and PDF.
- `source/master-cover-letter/`: reusable cover-letter template.
- `career-materials/`: comprehensive experience, projects, skills, bullet banks, and tailoring guidance.
- `applications/<Company>/<Role>/`: tailored resume source, cover-letter source/artifact, job description, and notes for each application.
- `application-management/`: application tracker and email-monitoring rules.
- `templates/`: reusable scaffolds for job descriptions and tailoring notes.

## Current Canonical Resume

The current June 2026 resume is the canonical resume source:

- `source/master-resume/resume.tex`

Generated PDFs are build artifacts by default. Create them when needed for applications, but do not keep duplicate binary copies in the repo unless explicitly requested. Cover-letter PDFs or DOCX files may be committed when they are the requested submission artifact.

## Current Rule

There should be one master resume source: `source/master-resume/resume.tex`. Tailored application resumes can be created inside `applications/<Company>/<Role>/` after proposed changes are approved.

Based off of [sb2nov/resume](https://github.com/sb2nov/resume/).
