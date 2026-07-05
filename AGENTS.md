# Resume Repo Instructions

This repository is used to maintain Aryan Miriyala's master resume materials and generate targeted resumes and cover letters for specific job applications.

## Operating Rule

Before changing resume or cover-letter content, first show the proposed changes in chat and wait for Aryan's approval. After approval, apply the changes, generate artifacts, and verify the output.

Make incremental commits for small, coherent changes so the repository stays easy to review and push to GitHub. Do not bundle unrelated resume, cover-letter, application, tracker, and source-material updates into one large commit.

## Application Pipeline

For every new job application:

1. Create `applications/<Company>/<Role>/`.
2. Save the job posting as `job-description.md`.
3. Add or update the role in `application-management/application-tracker.md`.
4. Review `career-materials/` for relevant experience, projects, skills, and reusable bullets.
5. Apply `career-materials/ats-recruiter-resume-guide.md` and `career-materials/resume-targeting-guide.md` before proposing resume edits.
6. Apply `career-materials/cover-letter-guide.md` before drafting any cover letter. Ask Aryan cover-letter personalization questions first:
   - What genuinely interests you about this company?
   - Do you have any personal connection to the company, product, industry, mission, or team?
   - Is there anything specific you want the hiring manager to feel after reading the letter?
7. Show proposed resume and cover-letter content changes in chat and wait for approval.
8. Create a tailored `resume.tex` from `source/master-resume/resume.tex` only after approval.
9. Generate `resume.pdf` locally from the tailored LaTeX source only when needed for submission.
10. Create `cover-letter.md` and, when submitting, generate a `cover-letter.pdf` or `cover-letter.docx`.
11. Add `tailoring-notes.md` explaining which experience, projects, and keywords were emphasized.
12. Update `application-management/application-tracker.md` when the application is ready, applied, rejected, interviewing, or archived.

## Directory Conventions

- `source/master-resume/`: canonical general resume source and PDF.
- `source/master-cover-letter/`: reusable cover-letter template material.
- `career-materials/`: source-of-truth documents for experience, projects, skills, bullet banks, and cover-letter language.
- `applications/<Company>/<Role>/`: one complete application package per role.
- `application-management/application-tracker.md`: high-level status tracker for all active and historical applications.
- `application-management/email-rules.md`: application-email classification and search rules.
- `templates/`: reusable scaffolds for application folders and notes.

Do not keep duplicate master resume copies. The canonical resume source is `source/master-resume/resume.tex`.

Do not commit binary/generated artifacts unless Aryan explicitly asks. This includes PDFs, DOCX files, PNG previews, and LaTeX build artifacts.

## Resume Rules

- The resume must be exactly one page: not more than one page, and not less than one full page of serious content.
- Use ATS-friendly bullets: action verb + technical keywords + scope + impact.
- Do not invent metrics. Use exact numbers only when supported by the source material.
- Prefer concrete technologies, systems, and business/domain context over vague claims.
- Tailor keywords to the job description while keeping statements truthful.
- Preserve the existing LaTeX style unless Aryan asks for a redesign.
- When adding new skills, confirm they are supported by experience, projects, or explicit user input.
- Keep bullets concise enough to fit the one-page layout.
- The resume must be readable by a human reviewer. Do not solve length problems by making the document feel cramped or shrinking text into unreadable sizes.
- Prefer margin/border and spacing adjustments before cutting meaningful experience, changing the Education structure, or reducing font size.
- Use a professional summary only when it improves immediate role alignment. It must be 2-3 lines maximum, tailored to the job, grounded in verified experience, and written as what Aryan brings, not what Aryan wants.
- Technical Skills should list actual tools, languages, frameworks, cloud/data platforms, and technical methods. Do not list broad responsibilities such as `operational data` or `troubleshooting` as standalone skills; put those in bullets with context.
- Experience and project bullets must contain enough concrete detail for both ATS matching and human review. Keywords alone are not enough.

## Cover Letter Rules

- Keep cover letters specific to the company and role.
- Before drafting, ask Aryan about personal connection, motivation, and how he feels about the company.
- Reuse verified facts from `career-materials/`.
- Avoid generic filler and unsupported claims.
- Emphasize the strongest match between the job description and Aryan's experience.
- Prefer confident, direct language over exaggerated language.
- Do not rehash the resume. Use the cover letter to add context, motivation, judgment, and personal fit.
- Keep the cover letter under one page.
- Default to at most two full body paragraphs unless Aryan asks for a longer version.
- For job submission, produce a PDF or DOCX cover-letter artifact, not only a Markdown draft.
- Use a warm, professional, human tone.
- Mention company-specific research and personal connection when truthful.

Good cover letters should:

- Explain why this company and role are specifically interesting.
- Connect Aryan's strongest matching experience to the employer's needs.
- Add a personal or human detail when available.
- Show evidence through short examples rather than broad self-praise.
- Stay concise, specific, and easy to read.

Cover-letter guidance incorporated from a 2026 web check:

- Yale Office of Career Strategy: tailor each letter to a specific job, connect skills to employer needs, use job-description keywords truthfully, write in confident active language, keep it to one page, and use a clear opening/body/closing structure.
- Purdue OWL: use the cover letter to explain experience in a story-like format, go deeper on relevant skills, relate those skills to job requirements, show individualized tailoring, and demonstrate written communication quality.

## Application Email Monitoring

The repo may include a Gmail application-status monitor scaffold under `scripts/gmail_application_monitor/`.

Rules:

- A scheduled Gmail status check should run 4 times per day, not continuously.
- Suggested local schedule: 8:00 AM, 12:00 PM, 4:00 PM, and 8:00 PM local time.
- The monitor should classify application-related messages as `Confirmation`, `Assessment`, `Recruiter Response`, `Interview`, `Rejection`, `Offer`, or `Unknown`.
- The monitor should update `application-management/application-tracker.md` and, when useful, `applications/<Company>/<Role>/email-updates.md`.
- Do not commit Gmail credentials, OAuth tokens, raw full email bodies, or private message dumps.
- Store only sanitized metadata by default: sender, subject, date, detected company, detected role, status, and a short note.
- If uncertain, mark the tracker row as `Needs Review` rather than making an irreversible assumption.
- Gmail API push notifications are not required for this repo. Scheduled polling is the preferred default.

## Verification

After approved resume changes:

1. Compile the LaTeX file with `pdflatex -interaction=nonstopmode -halt-on-error resume.tex`.
2. Confirm the PDF page count with `pdfinfo resume.pdf`. It must be exactly 1 page.
3. Extract text with `pdftotext resume.pdf -` and check that bullets read correctly.
4. Report changed files and verification results.
5. Remove generated PDF and LaTeX build artifacts from the repo unless Aryan explicitly wants to retain them.
