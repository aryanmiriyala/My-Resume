# Tailoring Notes - Fuze Health Graduate Software Engineer

Status: Resume and cover letter drafted after Aryan approval on 2026-07-05.

## Target Role Angle

Primary angle: Graduate software engineer with healthcare-adjacent software, cloud/data engineering, operational troubleshooting, and full-stack feature development experience.

Secondary angle: Applied AI/full-stack engineer who has worked across healthcare workflows, cloud data pipelines, secure systems, documentation-heavy technical work, and cross-functional internal tools.

## Highest-Value Keywords

- Graduate Software Engineer
- Python
- JavaScript
- AWS
- Cloud computing
- Complex data environments
- Application logs / operational data / system metrics
- Troubleshooting
- Root-cause analysis
- Issue triage
- Bug fixing
- Feature development
- QA / Operations / Engineering collaboration
- Documentation / knowledge base
- Healthcare / digital health
- Application observability

## Truth-Grounded Match Points

- AWS/data: AAIS production AWS Glue, S3, Lambda, IAM, PySpark, SQL, cross-source data pipelines, validation, and operational data workflows.
- Healthcare: APKD AWS-hosted Lucee/CFML healthcare workflow platform; Travel Health Advisor full-stack health AI project; HealthTrend healthcare data pipeline.
- Troubleshooting/reliability: APKD 404/access-denied handling, audit logging, MFI file-location fixes, duplicate-antigen crash handling, Matchgrid ordering, HTML5 form modernization.
- Feature development: SmartSolve Next.js onboarding tracker; AAIS React/Node modernization; Travel Health Advisor React/Express/MongoDB/Mistral AI project.
- Documentation/communication: BGSU research assistantship and technical training materials; cross-functional internship work.

## Avoid / Be Careful

- Do not claim Splunk or Datadog experience unless Aryan confirms direct use.
- Do not overstate formal HIPAA compliance. Use healthcare-adjacent, secure workflow, audit logging, access control, and sensitive data language.
- Do not include unsupported Travel Health Advisor RAG/HuggingFace/cosine-search claims from the current master resume.
- Keep the generated resume exactly one page after approval.

## Approved Resume Emphasis

- Lead with SmartSolve full-stack/internal software and secure workflow work.
- Keep AAIS Data Engineering strong because it maps to cloud computing, complex data environments, Python, AWS, operational data, and troubleshooting.
- Reframe AAIS Software Engineering toward Python data modeling, React/Node feature work, RBAC/JWT, AWS Lambda, and PII-safe data movement.
- Reframe APKD toward healthcare workflow reliability, bug fixing, form security, audit logging, access-denied behavior, crash fixes, and legacy modernization.
- Use Travel Health Advisor as the top project because it is healthcare, full-stack JavaScript, Express/MongoDB, Mistral AI, and user-facing product work.
- Use HealthTrend as the second project because it reinforces healthcare data, streaming, Spark/PySpark, and operational analytics alignment.
- Added a professional summary to make the healthcare + AWS data engineering + full-stack fit visible immediately.
- Reduced SmartSolve to two high-signal bullets and used the recovered space to add more detail for AAIS Software Engineering, APKD, projects, and skills.
- Cleaned the skills section so `operational data` and `troubleshooting` are represented in context through bullets instead of listed as standalone technical skills.

## Approved Cover Letter Angle

Personal + technical direction: connect Fuze's patient-first digital health and remote-care mission with Aryan's pattern of building software for complex healthcare-adjacent, data-heavy, and internal operational workflows. Lead with digital health and remote care interest, but keep the strongest focus on the engineering and data side. Use APKD as the personal/professional healthcare connection, AAIS as the AWS/data troubleshooting proof point, and a combined healthcare + cloud/data + full-stack story.

Aryan's cover-letter inputs:

- Interest: digital health and remote care, with the engineering and data side as the strongest interest.
- Personal/professional connection: APKD healthcare workflow experience.
- Lead angle: combination of healthcare motivation, AWS/data troubleshooting, and full-stack product engineering.

## Cover Letter Verification

- Created `cover-letter.tex` from the approved Markdown cover-letter content.
- Compiled with `pdflatex -interaction=nonstopmode -halt-on-error cover-letter.tex`.
- Confirmed with `pdfinfo cover-letter.pdf`: `Pages: 1`.
- Extracted text with `pdftotext cover-letter.pdf -` and verified readable text extraction.
- Rendered the PDF to PNG for visual review; confirmed clean one-page layout.
- `cover-letter.pdf` is included as the submission-ready cover-letter artifact.

## Resume Verification

- Compiled with `pdflatex -interaction=nonstopmode -halt-on-error resume.tex`.
- Confirmed with `pdfinfo resume.pdf`: `Pages: 1`.
- Extracted text with `pdftotext resume.pdf -` and verified the resume is readable, keyword-aligned, and in usable ATS order.
- Rendered the PDF to PNG for visual review after the readability pass.
- Revised the resume from compressed 10pt/footnote-size bullets to an 11pt document with normal small bullets while preserving the one-page limit.
- Recompiled and re-rendered after the content restructure; confirmed the expanded-detail version still fits on one page.
- Performed a layout-only spacing pass after visual PDF review: compacted Education into two one-line entries and loosened spacing around experience role headers without changing resume bullet content.
- Generated `resume.pdf` is local and ignored by git under the repo's binary/generated artifact rules.
