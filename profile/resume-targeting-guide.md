# Resume Targeting Guide

Use this guide when tailoring a resume to a specific company and role. Apply the rules in `profile/ats-recruiter-resume-guide.md` throughout the process.

## Step 1: Parse the Job Description

Extract:

- Exact posted job title
- Required languages
- Required frameworks
- Cloud requirements
- Data requirements
- AI/ML requirements
- Security/auth requirements
- Domain context
- Repeated keywords
- Nice-to-have skills
- Recruiter-screen responsibilities
- ATS-critical exact terms

Save the posting in `application-packages/<Company>/<Role>/job-description.md`.

## Step 2: Select the Resume Angle

Choose one primary angle:

- Full-stack software engineer
- Data engineer
- AI engineer / AI product engineer
- Cloud engineer
- Security-conscious software engineer
- Healthcare software engineer
- Enterprise data/platform engineer

Choose one secondary angle if useful.

## Step 3: Decide Whether to Use a Professional Summary

Use a summary when the job benefits from connecting multiple parts of Aryan's background in the first recruiter scan, especially for software roles that also value applied AI, healthcare, cloud/data engineering, full-stack systems, or cybersecurity.

Rules:

- Keep the summary to two sentences maximum. Prefer one tight sentence when the fit is obvious.
- Keep each sentence concise enough to scan quickly; do not write paragraph-style summaries.
- Make it role-specific and grounded in the job description's language.
- Include the exact posted job title once in visible summary text when truthful, using a non-misleading clause such as `<Exact Job Title>-aligned software engineer with...` or `Software engineer aligned with <Exact Job Title> responsibilities through...`.
- Lead with what Aryan brings: systems built, domains worked in, and technical strengths.
- Do not write an objective statement.
- Do not rewrite Aryan's actual past job titles, invent seniority, or repeat the posted title as a disconnected keyword.
- Do not turn the summary into a skills dump. Use only the 2-4 strongest job-description terms that are supported by bullets below.
- Do not use the summary to compensate for weak bullet alignment. The experience and project bullets still need to prove the fit.

## Step 4: Select Experience Bullets

Use `experience-master.md` and `bullet-bank.md`.

Rules:

- Start from the `Platform-Ready Description` in `experience-master.md` when writing LinkedIn experience sections, cover-letter context, or expanded application material.
- Use the `Handshake Description` in `experience-master.md` for Handshake experience entries; keep it at or below 500 characters and do not paste the longer platform-ready version into Handshake.
- Use `Reusable Bullet Options` from `experience-master.md` when the application needs company/role-specific bullets.
- Use `bullet-bank.md` when the application needs job-family bullets across multiple roles.
- Prefer bullets matching the job's required stack.
- Put job keywords into bullets only when supported by real experience.
- Preserve internship roles by default. A weakly relevant internship may be compressed or omitted when it would displace substantially stronger evidence or force unreadable formatting; record the decision in `tailoring-notes.md`.
- Do not impose a fixed bullet maximum or require matching bullet counts across roles. Let the number of distinct, job-relevant accomplishments determine the count, subject to one-page readability.
- Audit each selected bullet against the formula: action verb + what changed + technology/method + scope/domain + impact/result.
- Rewrite, combine, or remove any bullet that does not provide a clear contribution, defensible context, and result; never retain a weak bullet for visual symmetry.
- When the resume is underfilled, add evidence by quality order: a stronger verified experience bullet, a deeper project bullet explaining purpose/method/result, a missing truthful must-have keyword in context, or a compact skills category. Do not add filler, duplicate claims, broad soft-skill labels, or unsupported technologies just to occupy space.
- Keep the most recent experience strong.
- Do not force unrelated skills into a bullet.
- Do not invent metrics.
- Keep bullets concise enough for one page.
- Preserve enough technical detail for a human reviewer to understand the work. If the section gets tight, adjust layout before removing the strongest truthful details.

## Step 5: Select Projects

Use `projects-master.md`.

Rules:

- Start from each project's `Platform-Ready Description` for LinkedIn, portfolios, cover letters, or expanded project sections.
- Use each project's `Handshake Description` for Handshake project entries; keep it at or below 500 characters and preserve the most important stack, problem, and outcome.
- Use `Tech Stack`, `Positioning Angles`, and `Reusable Bullet Options` to select only the project details that match the role.
- Projects support the resume angle after experience has been protected. Include fewer projects with stronger job-aligned bullets instead of cutting internship experience to fit more projects.
- For AI roles, prioritize Travel Health Advisor - BGSU Hackathon 2025 and RocketGrader.
- For full-stack roles, include both projects if space allows.
- For data-heavy roles, consider reducing project bullets to preserve room for AAIS data engineering.
- For security/platform roles, emphasize Auth0, RBAC, JWT, SSO, PII tokenization, and AWS.
- Avoid duplicate project entries. If two names refer to the same repository or product, consolidate them under one canonical project.
- Ground project claims in repository files and implementation details, not only README language.

## Step 6: Tune Technical Skills

Use `skills-master.md`.

Rules:

- Include skills that appear in the job description and are supported by experience.
- Prefer exact job-description wording for tools and frameworks when truthful.
- Put the most relevant categories first.
- Keep the skills section compact.
- Avoid listing technologies that distract from the target role.
- List actual tools, languages, platforms, frameworks, libraries, and technical methods. Do not list broad work activities as skills unless they are expressed as concrete technical capabilities.

## Step 7: Verify Output

After approval and edits:

- Compile LaTeX.
- Confirm the resume PDF is exactly one page.
- Extract PDF text and inspect bullets.
- Confirm the exact posted job title appears once in visible summary/title text and is supported by evidence-bearing experience or project bullets.
- Confirm the Professional Summary is no more than two sentences, concise, and written in the job description's language without becoming a keyword list.
- Confirm the PDF text preserves section order and important keywords.
- Visually inspect the PDF for readability, spacing, cramped sections, canonical layout consistency, and bottom-page usage. A large unused bottom band fails this step when verified role-aligned evidence is still available.
- If the resume is too long, first tighten wording, remove repetition, and prioritize stronger evidence. Keep the canonical application-resume geometry and 11-point typography unchanged rather than creating application-specific spacing.
- Save tailoring notes.
