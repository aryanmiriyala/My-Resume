# Career Ops Repo Instructions

This repository is used to maintain Aryan Miriyala's career source material, discover recent job opportunities, track applications, and generate targeted resumes and cover letters for specific job applications.

## Pipeline Separation Rule

This repo has two separate pipelines. Do not merge them unless Aryan explicitly asks to move from one pipeline into the other.

### Pipeline 1: Job Discovery

Trigger this pipeline when Aryan asks to find jobs, search job boards, discover recent postings, scan ATS feeds, update `job-search/jobs-inbox.csv`, generate Google search links, collect ATS URLs, or improve job crawling/discovery.

Job Discovery outputs belong under `job-search/` and should produce job leads, source reports, search links, direct ATS target updates, and CSV inbox updates. It does not generate tailored resumes or cover letters.

### Pipeline 2: Application Package Generation

Trigger this pipeline when Aryan provides a specific job description or says he is applying to a specific role/company.

Application Package Generation outputs belong under `application-packages/<Company>/<Role>/` and should produce the tailored resume, cover letter, tailoring notes, validation result, ATS-style score, and tracker update. It does not search broadly for additional jobs unless Aryan separately asks for job discovery.

A discovered job becomes an application only after Aryan selects it or provides the specific job description/application link for that role.

## Application Package Operating Rule

When Aryan provides a job description, treat it as a request to run the complete established application package pipeline for that role. Aryan should not need to separately ask for setup, next steps, resume generation, cover-letter generation, PDF compilation, ATS alignment, or tracker updates. Save the posting, research the company when useful, create or update the application package, draft tailoring notes, generate the tailored resume and cover letter, compile submission PDFs, run the alignment/ATS-style score, verify outputs, update the tracker, commit, and push.

Supplying a job description is approval to perform the full pipeline and generate tailored application artifacts. Do not stop at a proposal unless Aryan explicitly asks to review proposed changes first. If the job description has serious blockers, unsupported requirements, or unclear fit, proceed with truthful materials while flagging those risks in `tailoring-notes.md` and the final response.

Every final application response must include the ready artifact paths, one-page PDF verification, application validator result, and the ATS-style score. Also include an `ATS assumed score` near the end of the pipeline/final response so Aryan can quickly judge the likely resume-and-cover-letter fit for the specific job description. Do not leave Aryan to ask separately whether the resume is aligned or whether the package passed validation.

Make incremental commits for small, coherent changes so the repository stays easy to review and push to GitHub. Do not bundle unrelated resume, cover-letter, application, tracker, and source-material updates into one large commit.

## Application Pipeline Execution Contract

For every job description, start from this file as the source of truth. Do not rely on memory from the current chat, prior application habits, or an abbreviated version of the workflow. Re-read the relevant `AGENTS.md` instructions and then execute the pipeline as a checklist.

Do not mark an application package complete until all required outputs exist and have been verified:

- `application-packages/<Company>/<Role>/job-description.md`
- `application-packages/<Company>/<Role>/tailoring-notes.md`
- `application-packages/<Company>/<Role>/resume.tex`
- `application-packages/<Company>/<Role>/resume.pdf`
- `application-packages/<Company>/<Role>/cover-letter.md`
- `application-packages/<Company>/<Role>/cover-letter.pdf` or `cover-letter.docx`
- Updated `operations/application-tracker.md`
- Recorded ATS-style score and alignment pass in `tailoring-notes.md`
- Passing `automation/validate_application_package.py` result
- Cleaned generated LaTeX artifacts
- Incremental commit and push

If context is resumed, compacted, or interrupted mid-application, re-open the application folder and this file before continuing. Continue from the repository state, not from assumptions about what was already done.

## Application Package Pipeline

For every new job application:

1. Create `application-packages/<Company>/<Role>/`.
2. Save the job posting as `job-description.md`.
3. Add or update the role in `operations/application-tracker.md`.
4. Review `profile/` for relevant experience, projects, skills, and reusable bullets.
5. Apply `profile/ats-recruiter-resume-guide.md` and `profile/resume-targeting-guide.md` before proposing resume edits.
6. Build a job keyword map before writing the resume: required skills, repeated terms, responsibilities, domain language, must-have tools, nice-to-have tools, and unsupported terms to avoid. Use this map to decide the resume angle, bullet selection, projects, technical skills, and cover-letter proof points.
7. Apply `profile/cover-letter-guide.md` before drafting any cover letter. Use known personal context from `profile/` and prior application notes. Ask Aryan cover-letter personalization questions only when the letter would be materially weaker or risky without the answer:
   - What genuinely interests you about this company?
   - Do you have any personal connection to the company, product, industry, mission, or team?
   - Is there anything specific you want the hiring manager to feel after reading the letter?
8. Document the resume direction, cover-letter angle, strongest matching experience/projects, important keyword targets, unsupported keywords to avoid, and any blocking eligibility questions in `tailoring-notes.md`.
9. Create a tailored `resume.tex` from `master-documents/master-resume/resume.tex` or the latest successful one-page application resume pattern.
10. Audit every experience and project bullet against the bullet rules before compiling. Rewrite any bullet that lacks a strong action verb, truthful job-aligned technology, scope/domain context, and impact/result.
11. Generate `resume.pdf` locally from the tailored LaTeX source only when needed for submission.
12. Create `cover-letter.md` and, when submitting, generate a `cover-letter.pdf` or `cover-letter.docx`.
13. Run a resume-vs-job-description alignment pass after generating the resume. Include an ATS-style score, matched keywords, missing-but-truthful keyword opportunities, unsupported keywords intentionally omitted, and concrete next-step recommendations.
14. Add `tailoring-notes.md` explaining which experience, projects, and keywords were emphasized, plus the alignment pass and ATS-style score.
15. Run `python3 automation/validate_application_package.py application-packages/<Company>/<Role>` before marking the package ready. Fix failures instead of ignoring them. If a failure is intentional for a specific application, document the reason in `tailoring-notes.md` and the final response.
16. Update `operations/application-tracker.md` when the application is ready, applied, rejected, interviewing, or archived.

If the job description includes an eligibility, location, sponsorship, clearance, degree, or schedule constraint, flag it during the intake response before spending effort on final artifacts. Continue with the proposal unless the constraint clearly makes the role impossible.

## Job Discovery Pipeline

For job-search and job-discovery requests, do not rely only on generic public boards. Use the layered job-search workflow in `job-search/`:

1. Generate recent Google/search links for target roles and ATS domains.
2. Use search results to collect ATS-hosted job URLs, especially Greenhouse, Lever, Ashby, and SmartRecruiters links.
3. Run `discover-direct-ats-targets` on the collected URLs to extract, verify, and save company board tokens in `job-search/config/direct-ats-targets.json`.
4. Run `run-direct-ats` to pull structured postings from verified ATS feeds into `job-search/jobs-inbox.csv` and dated reports.
5. Use `run-public-search` as a supplemental source, not the main source.
6. Keep Workday, iCIMS, Workable, Oracle, SAP SuccessFactors, ADP, BambooHR, Jobvite, and company-specific pages marked as adapter/backlog sources until reliable structured ingestion is implemented and verified.

The goal is breadth plus accuracy: search discovers new company boards, direct ATS APIs provide structured job data, and the CSV remains the manual-review source of truth.

Keep `job-search/jobs-inbox.csv` minimal. It should contain only `company`, `position`, `posted_at`, `pulled_at`, and `url`. Put scoring, source metadata, fit flags, notes, snippets, and other noisy/internal details in dated Markdown reports instead of the CSV.

## Directory Conventions

- `master-documents/master-resume/`: canonical general resume source and PDF.
- `master-documents/master-cover-letter/`: reusable cover-letter template material.
- `profile/`: source-of-truth documents for experience, projects, skills, bullet banks, and cover-letter language.
- `application-packages/<Company>/<Role>/`: one complete application package per role.
- `operations/application-tracker.md`: high-level status tracker for all active and historical applications.
- `job-search/`: recent-job discovery tooling for ATS search links, `jobs-inbox.csv` local job storage, scoring, and recency-bucket reports.
- `templates/`: reusable scaffolds for application folders, notes, and the reusable prompt for starting a new application pipeline.

Do not keep duplicate master resume copies. The canonical resume source is `master-documents/master-resume/resume.tex`.

Do not commit binary/generated artifacts unless Aryan explicitly asks. This includes PDFs, DOCX files, PNG previews, and LaTeX build artifacts.

## Resume Rules

- The resume must be exactly one page: not more than one page, and not less than one full page of serious content.
- Use ATS-friendly, outcome-oriented bullets following the **STAR/CAR** and **Google XYZ** formulas: **Action Verb + What was built/changed + How/Technology used + Scope/Context + Impact/Result**.
- The bullet formula is a hard gate, not a suggestion. Every experience and project bullet must satisfy all parts of the formula:
  - **Action Verb**: Begin with a strong, active, past-tense verb (e.g., *Architected, Engineered, Optimized, Migrated, Automated, Delivered*). Avoid passive phrases like "Responsible for," "Helped with," or "Worked on."
  - **What**: Describe the specific system, feature, database, or pipeline that was built, automated, secured, or modernized.
  - **How/Technology**: Name the exact language, framework, cloud service, or architectural pattern (e.g., *Next.js, PySpark, AWS Glue, JWT, role-based access control*).
  - **Scope/Context**: Show the scale, user base, size, or domain context (e.g., *20+ TB of insurance data, 700+ member companies, 110 internal users*).
  - **Impact/Result**: State the quantifiable business or technical outcome (e.g., *reducing cloud spend by 30%, decreasing latency, maintaining 24-hour data latency*). If a verified metric is unavailable, use a truthful qualitative result (e.g., *improving data reliability, strengthening form security, standardizing data flows, or reducing manual errors*).
- **Strong vs. Weak Bullets Example**:
  | Weak (Task-Oriented) | Strong (Impact & Technology-Oriented) |
  | :--- | :--- |
  | Worked on database validation and loaded data into S3 using AWS Lambda. | Automated database validation with AWS Lambda triggers that tokenized PII using hashlib/boto3 and ingested structured JSON into S3, securing data movement and maintaining 24-hour data latency. |
  | Helped build a Next.js onboarding tracker and added SSO authentication. | Architected a full-stack Next.js onboarding tracker with PostgreSQL, Drizzle ORM, SSO, and auth middleware to centralize HR workflows and protect sensitive employee data. |
- **Section-by-Section Guidance**:
  - **Professional Summary**: Grounded in experience and limited to 2-3 lines max. Highlight years of experience, core domains (e.g., distributed systems, applied AI, data engineering), and a clear value proposition. Avoid generic buzzwords (e.g., "passionate," "fast learner") and do not repeat the skills section.
  - **Education**: Show degrees, GPA (e.g., GPA: 4.00/4.00), graduation dates, and university name. Ensure it is prominently displayed.
  - **Experience**: Place recent and most relevant experience in the top half. The first 1-2 bullets of relevant roles must align directly with the highest-priority responsibilities and keywords of the job description. Highlight systems thinking, architectural decisions, and working with constraints (e.g., scalability, reliability, security).
  - **Projects**: Use projects to support the primary resume angle and cover skill gaps not shown in the professional experience. Emphasize actual implementation details and files in the repository.
  - **Technical Skills**: Group into categorized lists (e.g., Languages, Frontend, Backend/API, Cloud/DevOps, Databases, AI/ML, Security). This is key for parser categorization. Do not list broad responsibilities (e.g., "troubleshooting") as skills.
- Do not invent metrics. Use exact numbers only when supported by the source material.
- Preserve the existing LaTeX style unless Aryan asks for a redesign.
- Keep bullets concise enough to fit the one-page layout (usually 1-2 lines on the PDF page).
- Experience takes precedence over Projects. All internship roles are core experience and should remain on tailored resumes by default, including less directly aligned internships, unless Aryan explicitly approves removing a specific role. If space is tight, cut or compress Projects, Skills, or lower-priority detail before removing an internship.
- Do not leave a tailored resume looking sparse. If there is usable space, add high-signal experience bullets, a relevant project, or stronger technical detail before considering the resume complete.
- During PDF review, explicitly check the lower half and bottom of the page for obvious unused whitespace. A final resume should feel like a complete, full one-page document with no visual gaps, while still remaining readable.
- Do not accept a visible blank band at the bottom of the rendered PDF if there is enough room for one or more readable lines of truthful, role-aligned content. Keep iterating until the page visually reads as full without clipping, overlap, or unreadable density.
- The full-page rule is a hard requirement, but fullness must be achieved intelligently. If Experience or Projects becomes visually dense, keep the resume full by rewriting bullets for higher information density, using margins and spacing deliberately, moving detail between sections, adding stronger verified content where space exists, and removing or shortening weaker content only when it improves scanability.
- Avoid aggressive negative spacing in Experience and Projects. Do not use negative project `itemsep` or large negative bullet `vspace` values just to force more content onto the page.
- Prefer fewer, stronger projects with readable descriptions over many project one-liners stacked tightly, unless the additional projects can be included without hurting scanability. Projects should support the target role and remain scannable by a human reviewer.
- The resume must be readable by a human reviewer. Do not solve length problems by making the document feel cramped or shrinking text into unreadable sizes.
- Prefer margin/border and spacing adjustments before cutting meaningful experience, changing the Education structure, or reducing font size.

## Alignment And ATS-Style Score

Every finalized application resume should include an alignment pass against the saved `job-description.md`.

Target ATS-style score is 90/100 or higher for every finalized application package. Before finalizing any package below 90, iterate on truthful keyword coverage, bullet specificity, project selection, skills ordering, and cover-letter proof points. If a score of 90+ cannot be reached without unsupported claims, keep the lower truthful score and explicitly document why in `tailoring-notes.md` and the final response.

## ATS Parser And Recruiter Screen Rules

Treat ATS alignment as structured parsing plus human review, not as magic. A strong package must be optimized for both the parser and the recruiter.

- **Single-Column Layout**: Always use a clean, single-column layout. Multi-column formats cause parsers to scramble text, leading to misinterpretation of experience.
- **No Complex Elements**: Avoid tables, images, icons, text boxes, graphics, personal logos, or decorative formatting in application resumes. These elements hide or distort text for parsers. The PDF must be text-extractable in reading order with `pdftotext`.
- **Exact Keyword Mirroring**: Use exact job-description language for critical terms when truthful. If the job description says `REST-based API development` or `AWS Glue`, use those exact phrases rather than synonyms.
- **Context-Bound Keywords**: Put each high-priority keyword in evidence-bearing context (e.g., a role bullet or project line must show what was built, secured, or improved using that technology) instead of just dumping a list of tools.
- **Standard Heading Titles**: Keep standard section headings: `Professional Summary`, `Education`, `Experience`, `Projects`, and `Technical Skills`. Creative section names confuse parser categorization.
- **Relevance Placement**: Put recent and most relevant experience in the top half of the page so both parser scoring and human skim behavior see the match quickly.
- **Mirror Qualification Hierarchy**: Mirror required qualifications first, then preferred qualifications. Required degree, location/eligibility constraints, core language requirements, and must-have tools should be visibly covered before nice-to-have tools.
- **Avoid Keyword Stuffing**: Do not repeat keywords without a defensible context. AI screeners can detect hidden text or repetitive word blocks and may penalize the application.
- **Adjacent Evidence**: Include adjacent truthful technologies only as supporting evidence, not as substitutes.
- **After Compiling Verification**: Extract resume text with `pdftotext` and scan it as an ATS would: confirm exact role title, required languages, cloud/platform terms, and top responsibilities appear in readable order.

Use this scoring model as a practical internal check, not as a guarantee of a real ATS result:

- **Keyword coverage**: 40 points for truthful coverage of important job-title, skill, tool, platform, methodology, and domain keywords.
- **Experience relevance**: 25 points for how strongly the selected experience/projects match the role's responsibilities and business context.
- **Impact and evidence**: 15 points for quantified scope, concrete outcomes, and action + technology + impact bullets.
- **Formatting and ATS parsing**: 10 points for one-page PDF, readable layout, extractable text, standard headings, and no graphics/tables that break parsing.
- **Risk and gap handling**: 10 points for avoiding unsupported claims, identifying important missing skills, and flagging eligibility/location constraints.

Record the score in `tailoring-notes.md` with:

- `ATS-style score: X/100`
- `Strong matches`
- `Gaps / intentionally omitted unsupported keywords`
- `Recommended improvements`

Do not inflate the score by adding unsupported keywords. A truthful 80/100 resume is better than a 95/100 resume with claims Aryan cannot defend.

## Cover Letter Rules

- Keep cover letters specific to the company and role.
- Before drafting, ask Aryan about personal connection, motivation, and how he feels about the company.
- Reuse verified facts from `profile/`.
- Avoid generic filler, flattery, and unsupported claims (e.g., "perfect fit," "passionate about coding").
- Emphasize the strongest match between the job description and Aryan's experience.
- Map the cover letter to the job description using **one or two deep technical proof points** showing how Aryan solved a similar problem, rather than rehashing the resume in paragraph format.
- Prefer confident, direct, warm language over exaggerated language.
- Use the cover letter to add context, motivation, judgment, and personal fit.
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

## Job Search & Discovery Strategies (Getting Ahead of the Line)

To maximize callback rates, Aryan needs to apply to roles extremely quickly—ideally within 24 to 48 hours of posting. The Job Discovery pipeline helps achieve this using a layered approach:

1. **Direct ATS Feeds**: Keep `job-search/config/direct-ats-targets.json` updated with company tokens. Run `run-direct-ats` daily to fetch structured postings directly from Greenhouse, Lever, Ashby, and SmartRecruiters.
2. **Recent Google Search Queries**:
   - Run `generate-queries` to output search links for target roles and domains.
   - Use Google Search operators with a 24-hour time filter (`qdr:d`) to find freshly indexed postings on company portals before they are listed on major job boards.
3. **Domain Verification**: When paste-url discovery yields new Greenhouse/Lever/Ashby/SmartRecruiters URLs, run `discover-direct-ats-targets` to verify them and update the config file automatically.
4. **Inbox Maintenance**: Regularly check `job-search/jobs-inbox.csv`. Keep it minimal (only company, position, posted_at, pulled_at, and url). Move approved roles into the Application Package Generation pipeline.

## Verification

After approved resume changes:

1. Compile the LaTeX file with `pdflatex -interaction=nonstopmode -halt-on-error resume.tex`.
2. Confirm the PDF page count with `pdfinfo resume.pdf`. It must be exactly 1 page.
3. Extract text with `pdftotext resume.pdf -` and check that bullets read correctly.
4. Run the resume-vs-job-description alignment pass and record the ATS-style score in `tailoring-notes.md`.
5. Run `python3 automation/validate_application_package.py application-packages/<Company>/<Role>` and address any failures.
6. Report changed files, verification results, validator result, and the ATS-style score.
7. Remove generated LaTeX build artifacts. Keep submission PDFs only when Aryan asks for final application artifacts or when the application package needs a ready-to-submit PDF.
