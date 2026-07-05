# ATS and Recruiter Resume Guide

Use this guide when tailoring resumes for applicant tracking systems, recruiter screens, and hiring-manager review. These rules are grounded in career-center guidance from Yale OCS, MIT CAPD, and the University of Michigan Career Center.

## Non-Negotiable Rules

- Truth first: every keyword, tool, metric, and claim must be grounded in `experience-master.md`, `projects-master.md`, `skills-master.md`, or a verified repository/source.
- One page for the standard software resume unless Aryan explicitly approves a longer specialized version.
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

## Bullet Formula

Use this default structure:

`Action verb + what was built/changed + how/technology + scope/domain + impact/result`

Strong software/data examples:

- `Automated a manual billing workflow with PySpark and AWS Glue, processing 20+ TB of insurance data for 700+ member companies.`
- `Built a full-stack health AI prototype with React, Vite, Express, MongoDB/Mongoose, and Mistral AI for travel-health guidance.`
- `Secured an AWS-hosted Lucee/CFML healthcare workflow platform by implementing anti-CSRF tokens, IP-aware audit logging, and protected access-denied flows.`

Checklist for each bullet:

- Starts with a strong action verb.
- Names the actual technology used.
- Shows scope, user, system, or domain context.
- Includes a metric when verified.
- Explains impact without exaggeration.
- Does not read like a job description responsibility.

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

1. Save the job description in `applications/<Company>/<Role>/job-description.md`.
2. Extract keywords and role responsibilities.
3. Select a primary resume angle from `resume-targeting-guide.md`.
4. Choose 2-4 strongest experience bullets and 1-2 matching projects.
5. Rewrite bullets using the formula above, keeping claims grounded in source docs.
6. Tune the skills section to the job's language.
7. Compile LaTeX and confirm the PDF is exactly one page.
8. Extract PDF text and verify ATS readability.
9. Save `tailoring-notes.md` with keywords used, experience emphasized, and verification results.

## Common Failure Modes

- Generic resume that does not reflect the job description.
- Unsupported keywords added only to satisfy ATS matching.
- Bullets that list tasks without impact.
- Dense bullets that hide the main technology or result.
- Too many unrelated skills, making the target role unclear.
- Project duplication or stale project claims that are no longer repository-grounded.
- Overstated AI claims that say `built AI` without explaining the product workflow, data flow, or user value.

## Source Notes

- Yale Office of Career Strategy recommends comparing resumes against a job description, checking ATS visibility, and using specific keywords to improve noticeability.
- Yale OCS states its resume templates are formatted to work with Applicant Tracking Systems.
- MIT CAPD recommends using the position description to decide what to include, targeting each resume to the employer/position, using consistent standard formatting, strong action verbs, specific technologies, accomplishments, and quantified impact where possible.
- MIT CAPD notes employers may use keyword scanning and recommends using relevant industry/position keywords.
- University of Michigan Career Center recommends tailoring resumes, keeping formatting easy to skim, using bullets, quantifying when possible, and using the formula `Action Verb + What + How/Why/Impact`.
- University of Michigan also recommends using AI carefully: useful for keyword extraction and review, but final bullets must be accurate and written in Aryan's own voice.

## Sources

- Yale Office of Career Strategy, Resumes: https://ocs.yale.edu/channels/resumes/
- MIT Career Advising & Professional Development, Resumes: https://capd.mit.edu/resources/resumes/
- University of Michigan Career Center, Resume Resources: https://careercenter.umich.edu/article/resume-resources
