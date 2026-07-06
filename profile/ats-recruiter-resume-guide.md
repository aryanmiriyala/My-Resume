# ATS and Recruiter Resume Guide

Use this guide when tailoring resumes for applicant tracking systems, recruiter screens, and hiring-manager review. These rules are grounded in career-center guidance from Yale OCS, MIT CAPD, and the University of Michigan Career Center.

## Non-Negotiable Rules

- Truth first: every keyword, tool, metric, and claim must be grounded in `experience-master.md`, `projects-master.md`, `skills-master.md`, or a verified repository/source.
- One page for the standard software resume unless Aryan explicitly approves a longer specialized version.
- One page does not mean unreadable. If the resume becomes cramped, improve layout first through margins, section spacing, and line-width decisions before shrinking text or removing high-value technical detail.
- Tailor every resume to the job description instead of using a generic all-purpose resume.
- Use a clean, consistent, ATS-readable layout with conventional section names: `Education`, `Experience`, `Projects`, and `Technical Skills`.
- Use bullets, not paragraphs, for experience and project descriptions.
- Keep formatting consistent: dates, company names, job titles, locations, and project titles should appear in the same pattern throughout.
- Do not add photos, personal demographic information, references, salary history, or unrelated details.

## Keyword Strategy

- Extract exact job-description keywords before editing: languages, frameworks, cloud tools, data tools, AI/ML terms, security/auth terms, domain terms, role responsibilities, and repeated phrases.
- Match exact wording where truthful. If the posting says `AWS Lambda`, use `AWS Lambda`, not only `serverless`.
- Put the highest-value keywords in three places when supported: skills section, experience/project bullets, and project/role stack line.
- Prefer keywords in context over keyword lists. A skill is stronger when attached to what was built, automated, secured, analyzed, or improved.
- Avoid keyword stuffing. If a tool was only lightly used or is unrelated to the role, keep it out.
- Do not claim tools from the posting that Aryan has not used. For example, do not list `Splunk` or `Datadog` unless there is verified experience.

## Professional Summary Rules

Use a professional summary only when it helps a recruiter understand the target fit faster than the experience section alone. It is useful for roles where Aryan's background crosses several connected areas, such as software engineering, applied AI, cloud/data engineering, healthcare-adjacent software, and full-stack product work.

Rules:

- Keep it to 2-3 lines maximum in the PDF.
- Write it as a value proposition, not an objective. Avoid `seeking a role where...`.
- Tailor it to the job description using truthful role keywords.
- Include the target angle, strongest technical domains, and one clear value theme.
- Avoid generic traits such as `passionate`, `hard-working`, `fast learner`, or `team player` unless the line proves them through concrete context.
- Do not repeat the Technical Skills section as a sentence. Mention only the highest-value stack or domain terms.
- If adding the summary makes the page crowded, trim the summary before shrinking the resume font.

Default structure:

`Software engineer / applied AI builder with experience in <top domains/tools>, focused on <job-relevant outcome>. Background includes <2-3 strongest proof areas>.`

## Bullet Formula

Use this default structure:

`Action verb + what was built/changed + how/technology + scope/domain + impact/result`

Strong software/data examples:

- `Automated a manual billing workflow with PySpark and AWS Glue, processing 20+ TB of insurance data for 700+ member companies.`
- `Built a full-stack health AI prototype with React, Vite, Express, MongoDB/Mongoose, and Mistral AI for travel-health guidance.`
- `Secured an AWS-hosted Lucee/CFML healthcare workflow platform by implementing anti-CSRF tokens, IP-aware audit logging, and protected access-denied flows.`

Checklist for each bullet:

- Starts with a strong action verb.
- States what was built, changed, automated, analyzed, secured, validated, or improved.
- Names the actual technology used.
- Shows scope, user, system, or domain context.
- Includes a metric when verified.
- Explains impact without exaggeration.
- Does not read like a job description responsibility.
- Uses job-description keywords in context when the keyword is truthful.

If a bullet cannot satisfy this checklist, rewrite it before compiling the final resume. If a metric is unavailable, use a truthful qualitative outcome such as reliability, traceability, security, standardization, reduced manual work, reproducibility, or clearer downstream workflows.

## Recruiter Scan Rules

Recruiters often scan quickly, so the resume must make relevance visible immediately.

- Put the strongest matching experience in the top half of the page.
- Keep recent technical roles prominent.
- Use bold sparingly for important technologies and metrics only.
- Make role alignment obvious from the first two bullets of each relevant job.
- Keep bullets concise enough to scan, usually one to two lines.
- Prioritize the role's must-have skills over impressive but unrelated material.

## ATS Formatting Rules

- Use a simple single-column layout for generated application resumes unless a template has already been tested.
- Avoid text boxes, images, icons, graphics, and decorative elements in the resume PDF.
- Avoid tables for core resume content unless the LaTeX output has been verified as text-extractable.
- Use standard section headings and chronological ordering.
- Use normal punctuation and plain text for technologies where possible.
- Generate a PDF from LaTeX, then extract and inspect the text to confirm the content is readable in order.

## Human Readability Rules

- Use a readable font size. MIT CAPD recommends no smaller than 10pt; this repo should prefer readability over squeezing in marginal content.
- Keep the resume visually scannable in 30-60 seconds.
- Treat visual density as a failure mode during PDF review, but keep the full-page rule intact. If Experience or Projects looks cramped, optimize the page through stronger concise bullets, smarter section balance, margin/spacing tuning, and better content selection instead of leaving unused space.
- Preserve internship experience before project breadth. When a one-page resume is tight, compress or remove lower-priority projects before cutting an internship role, unless Aryan explicitly approves removing that role.
- Do not use aggressive negative spacing in Experience or Projects to satisfy the one-page rule. A full page should still have readable line spacing, clear section transitions, and enough breathing room for a recruiter scan.
- Prefer fewer high-signal projects over a crowded project list when each project is reduced to a dense one-line block.
- Do not compress Education into an awkward format unless Aryan approves it.
- Prefer margin/border adjustment before font-size reduction when a resume is slightly over one page.
- Keep enough detail in Experience and Projects for a human reviewer to understand what was built, how it worked, and why it mattered.
- Technical Skills should contain actual technologies and methods, not broad responsibilities. Put responsibilities such as troubleshooting, operational support, and data investigation into bullets where they have context.

## Software / AI / Data Resume Priorities

For software engineering roles:

- Prioritize full-stack features, APIs, debugging, testing, secure auth, production support, and maintainability.
- Include JavaScript/TypeScript, Python, React/Next.js/Angular, Node/Express, SQL/PostgreSQL/MongoDB, Docker, Git, and cloud tools when relevant.

For AI engineering or applied AI roles:

- Prioritize applied AI systems, LLM/RAG workflows, prompt/evaluation work, model/API integration, retrieval, data grounding, and user-facing AI workflows.
- Show how AI improved a workflow; do not only list model names.

For data/cloud roles:

- Prioritize ETL, PySpark, AWS Glue, S3, Lambda, IAM, validation, data profiling, SQL, large-scale processing, and cross-source pipelines.
- Put scale and data-source context in bullets when verified.

For healthcare or compliance-adjacent roles:

- Prioritize secure workflows, audit logging, access control, data-entry reliability, operational reliability, and healthcare-adjacent project work.
- Avoid formal compliance claims unless explicitly verified.

## Tailoring Workflow

1. Save the job description in `application-packages/<Company>/<Role>/job-description.md`.
2. Extract keywords and role responsibilities.
3. Select a primary resume angle from `resume-targeting-guide.md`.
4. Decide whether a professional summary is useful for this specific role.
5. Choose the strongest experience bullets first, preserving internship roles by default; then choose as many matching projects as the one-page layout can support without reducing experience quality.
6. Rewrite bullets using the formula above, keeping claims grounded in source docs.
7. Tune the skills section to the job's language.
8. Audit every experience and project bullet against the bullet checklist.
9. Compile LaTeX and confirm the PDF is exactly one page.
10. Extract PDF text and verify ATS readability.
11. Visually inspect the PDF for human readability before considering it done.
12. Save `tailoring-notes.md` with keywords used, experience emphasized, and verification results.

## Common Failure Modes

- Generic resume that does not reflect the job description.
- Unsupported keywords added only to satisfy ATS matching.
- Bullets that list tasks without impact.
- Dense bullets that hide the main technology or result.
- Summary sections that consume space without adding role alignment.
- Skills sections that contain responsibilities instead of supported technologies.
- Too many unrelated skills, making the target role unclear.
- Project duplication or stale project claims that are no longer repository-grounded.
- Overstated AI claims that say `built AI` without explaining the product workflow, data flow, or user value.

## Source Notes

- Yale Office of Career Strategy recommends comparing resumes against a job description, checking ATS visibility, and using specific keywords to improve noticeability.
- Yale OCS states its resume templates are formatted to work with Applicant Tracking Systems.
- MIT CAPD recommends using the position description to decide what to include, targeting each resume to the employer/position, using consistent standard formatting, strong action verbs, specific technologies, accomplishments, and quantified impact where possible.
- MIT CAPD notes employers may use keyword scanning and recommends using relevant industry/position keywords.
- University of Michigan Career Center lists a resume summary as optional and more common with experienced professionals, but available to students when useful.
- University of Michigan Career Center recommends tailoring resumes, keeping formatting easy to skim, using bullets, quantifying when possible, and using the formula `Action Verb + What + How/Why/Impact`.
- University of Michigan also recommends using AI carefully: useful for keyword extraction and review, but final bullets must be accurate and written in Aryan's own voice.

## Sources

- Yale Office of Career Strategy, Resumes: https://ocs.yale.edu/channels/resumes/
- MIT Career Advising & Professional Development, Resumes: https://capd.mit.edu/resources/resumes/
- University of Michigan Career Center, Resume Resources: https://careercenter.umich.edu/article/resume-resources
