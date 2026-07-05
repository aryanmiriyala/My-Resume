# Resume Targeting Guide

Use this guide when tailoring a resume to a specific company and role.

## Step 1: Parse the Job Description

Extract:

- Job title
- Required languages
- Required frameworks
- Cloud requirements
- Data requirements
- AI/ML requirements
- Security/auth requirements
- Domain context
- Repeated keywords
- Nice-to-have skills

Save the posting in `applications/<Company>/<Role>/job-description.md`.

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

## Step 3: Select Experience Bullets

Use `experience-master.md` and `bullet-bank.md`.

Rules:

- Start from the `Platform-Ready Description` in `experience-master.md` when writing LinkedIn experience sections, cover-letter context, or expanded application material.
- Use `Reusable Bullet Options` from `experience-master.md` when the application needs company/role-specific bullets.
- Use `bullet-bank.md` when the application needs job-family bullets across multiple roles.
- Prefer bullets matching the job's required stack.
- Keep the most recent experience strong.
- Do not force unrelated skills into a bullet.
- Do not invent metrics.
- Keep bullets concise enough for one page.

## Step 4: Select Projects

Use `projects-master.md`.

Rules:

- Start from each project's `Platform-Ready Description` for LinkedIn, portfolios, cover letters, or expanded project sections.
- Use `Tech Stack`, `Positioning Angles`, and `Reusable Bullet Options` to select only the project details that match the role.
- For AI roles, prioritize Travel Health Advisor and RocketGrades.
- For full-stack roles, include both projects if space allows.
- For data-heavy roles, consider reducing project bullets to preserve room for AAIS data engineering.
- For security/platform roles, emphasize Auth0, RBAC, JWT, SSO, PII tokenization, and AWS.

## Step 5: Tune Technical Skills

Use `skills-master.md`.

Rules:

- Include skills that appear in the job description and are supported by experience.
- Put the most relevant categories first.
- Keep the skills section compact.
- Avoid listing technologies that distract from the target role.

## Step 6: Verify Output

After approval and edits:

- Compile LaTeX.
- Confirm the resume PDF is exactly one page.
- Extract PDF text and inspect bullets.
- Save tailoring notes.
