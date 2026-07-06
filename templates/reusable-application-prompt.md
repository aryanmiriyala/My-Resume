# Reusable New Application Prompt

Use this prompt when starting a new chat where the goal is to create a tailored resume and cover letter for one specific job description.

```text
I am starting a new application-package pipeline in this repo.

First, read AGENTS.md completely and follow the Application Package Generation pipeline only. Do not run the Job Discovery pipeline unless I explicitly ask for job searching.

I will provide one specific job description below. Treat that as approval to run the full application-package workflow:

1. Create or update application-packages/<Company>/<Role>/.
2. Save the posting as job-description.md.
3. Review profile/, master-documents/, templates/, and AGENTS.md before writing.
4. Build a keyword/alignment map from the job description.
5. Create tailoring-notes.md with the resume strategy, cover-letter angle, keyword targets, risks/gaps, and ATS-style alignment notes.
6. Generate a tailored one-page resume.tex and resume.pdf.
7. Generate a concise, personal, role-aligned cover-letter.md and a submission-ready cover-letter.pdf or cover-letter.docx.
8. Keep every resume and cover-letter claim grounded in the repo source materials. Do not invent metrics, tools, employers, or experience.
9. Make the resume exactly one full readable page, with no obvious blank band at the bottom and no cramped unreadable sections.
10. Preserve all internship roles by default; experience takes precedence over projects if space is tight.
11. Run the ATS-style alignment pass and record the score in tailoring-notes.md.
12. Run python3 automation/validate_application_package.py application-packages/<Company>/<Role> and fix failures.
13. Clean generated LaTeX artifacts.
14. Make a small coherent commit and push to main.
15. In the final response, include artifact paths, one-page PDF verification, validator result, ATS-style score, and commit hash.

Job description:

[paste the full job description here]

Optional context if useful:
- Application link:
- Application questions:
- Company/product interest:
- Personal connection to company, industry, mission, or team:
- Cover letter tone or emphasis:
```

## Short Version

```text
I am applying to the role below. Read AGENTS.md first and run only the Application Package Generation pipeline. Create the application package, tailor the one-page resume and cover letter, generate PDFs, run validation and ATS-style alignment, update the tracker, commit, and push. Keep all claims grounded in profile/ and master-documents/.

Job description:
[paste JD]
```
