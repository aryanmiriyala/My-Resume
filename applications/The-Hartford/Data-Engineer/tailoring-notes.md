# Tailoring Notes - The Hartford Data Engineer

Status: Resume and cover letter generated after Aryan approval on 2026-07-05.

## Target Angle

Primary angle: Data engineer with insurance-domain experience building production AWS/PySpark/SQL workflows, cloud data pipelines, data validation, controlled access, and standardized data assets for analytics and downstream modeling.

Secondary angle: Software engineer with full-stack and AI-adjacent background who can support ML/AI data readiness, reproducible GitHub-based handoffs, cross-functional communication, and business-facing data solutions.

## Highest-Value Keywords

- Data Engineer
- Actuarial Strategic Modeling
- data assets
- machine learning
- artificial intelligence
- continuous data delivery
- SDLC
- MLOps
- Agile
- scalable software modules
- analytics solution suite
- data pipelines
- data quality
- data lineage
- exploratory analysis
- nulls
- duplicates
- real-time modeling
- GitHub
- reproducible results
- Python
- SQL
- relational databases
- Hadoop
- Spark
- cloud data sources
- XML
- JSON
- ETL
- metadata management
- data validation
- Linux
- Git
- automation
- AWS S3
- AWS EMR
- technical and non-technical communication
- business solutions

## Truth-Grounded Match Points

- AAIS Data Engineering Intern: Built production PySpark and AWS Glue workflows over 20+ TB of golden-table insurance data from Oracle, Impala, PostgreSQL, and related enterprise sources; calculated recurring charges for 700+ member companies; profiled and mapped 160+ source tables into 25 MDM domains; built validation, reverse ETL, S3, IAM, and Semarchy MDM migration workflows.
- AAIS Software Engineering Intern: Generated 1,000+ production SQL tables across Oracle/PostgreSQL and 10+ insurance lines using Python/JSON; built Python/Pandas/multiprocessing/fuzzy-matching workflows for large CSV processing; implemented AWS Lambda/S3 PII-tokenized data movement and RBAC/JWT access-control modernization for about 110 users.
- HealthTrend project: Built a Dockerized healthcare data pipeline using Apache NiFi, Kafka, Hadoop HDFS, Spark, PySpark, JSON, and CSV ingestion, directly matching the role's Hadoop/Spark/cloud-style data-source requirements.
- SmartSolve: Shows modern software engineering, secure internal tools, Git-based engineering habits, AI-assisted workflows, and applied AI planning, but should be secondary for this role.
- Diff-Grounded PR Description research: Useful only if space is needed for AI/ML and reproducible GitHub artifacts; not as strong as HealthTrend for this data engineering role.

## Avoid / Be Careful

- Do not claim R experience unless Aryan confirms it.
- Do not claim direct Airflow, Autosys, or Cron ownership unless Aryan confirms it. Use AWS Glue Workflows and automation language instead.
- Do not claim AWS EMR experience unless Aryan confirms it. Use AWS Glue, S3, Lambda, and IAM truthfully while noting Spark/PySpark experience.
- Do not overstate MLOps ownership. Frame as building ML/AI-ready data assets and data pipelines for analytical consumption.
- Do not proceed to final application materials until Aryan confirms whether the role is viable given the posting's no sponsorship / no STEM OPT I-983 statement and hybrid-location expectation.

## Proposed Resume Emphasis

- Professional summary should lead with data engineering, insurance domain, Python/SQL/PySpark, AWS data pipelines, data quality, and ML/AI-ready data assets.
- Skills should prioritize Python, SQL, PySpark, Spark, AWS Glue, AWS S3, AWS Lambda, AWS IAM, ETL, data validation, data quality, metadata/MDM, Oracle, PostgreSQL, Impala, JDBC, Hadoop HDFS, Kafka, NiFi, JSON, CSV, Linux, Git, Docker, and Pandas.
- Experience should keep AAIS Data Engineering as the strongest section with quantified scope: 20+ TB, 700+ member companies, 160+ source tables, 25 MDM domains, and 160+ Pentaho jobs replaced.
- AAIS Software Engineering should support the data-standardization story with 1,000+ generated SQL tables, 10+ insurance lines, Oracle/PostgreSQL, Python/JSON, AWS Lambda/S3, PII tokenization, and RBAC/JWT.
- Projects should use HealthTrend first because it directly maps to Hadoop/Spark, JSON/CSV ingestion, distributed data pipelines, and analytics readiness.
- A second project should be selected based on space: Diff-Grounded PR Description research for AI/reproducibility/GitHub artifacts, or FalconGraph for RAG/search/data ingestion.

## Proposed Cover Letter Angle

Use a concise two-paragraph personal + technical cover letter.

Recommended story:

- Open with interest in The Hartford's intersection of insurance, actuarial modeling, and modern data engineering, especially the opportunity to build reliable data assets that support ML/AI and business decision-making.
- Use AAIS as the strongest credibility point: insurance-domain data engineering with PySpark, AWS Glue, S3, SQL, validation, MDM migration, and large-scale production data.
- Mention that Aryan has already worked close to the Hartford problem space: insurance data standardization, data quality, cross-source pipelines, and business-facing data workflows.
- Close with communication and handoff fit: GitHub artifacts, reproducible work, translating technical data problems into business-facing solutions, and collaborating with technical/non-technical stakeholders.

## Questions for Aryan Before Drafting Cover Letter

- Is this role viable for you given the posting says no sponsorship and no STEM OPT I-983 Training Plan endorsement?
- Are you comfortable with the 3-day hybrid expectation in Hartford, Columbus, Chicago, or Charlotte if they enforce it?
- Do you have any personal connection to The Hartford, actuarial modeling, insurance analytics, Connecticut, Columbus, Chicago, or Charlotte?
- Should the cover letter lean more toward insurance-domain data engineering, ML/AI-ready data assets, or business-impact/data-quality storytelling?

## Proposed Resume Changes Pending Approval

- Created `applications/The-Hartford/Data-Engineer/resume.tex` from the one-page application resume pattern.
- Tailored the summary, skills, AAIS bullets, APKD/SmartSolve bullets, and project section toward data engineering, insurance, AWS, Spark/PySpark, data quality, metadata, and ML/AI data assets.
- Generated `resume.pdf` as the submission artifact after verifying it is exactly one readable page.

## Proposed Cover Letter Changes Pending Approval

- Created `cover-letter.md`, `cover-letter.tex`, and `cover-letter.pdf`.
- Kept the cover letter to two full paragraphs with a personal + technical tone grounded in AAIS insurance data engineering and The Hartford's actuarial modeling / ML-AI data-asset needs.

## Verification

- LaTeX compiled: `resume.tex` and `cover-letter.tex` compiled successfully with `pdflatex -interaction=nonstopmode -halt-on-error`.
- PDF page count: `resume.pdf` is 1 page; `cover-letter.pdf` is 1 page.
- PDF text checked: Extracted text from both PDFs with `pdftotext` and verified readable extraction.
- Visual review: Rendered both PDFs to PNG with `pdftoppm` and checked layout; resume is dense but readable and cover letter is cleanly spaced.
- Cleanup: Removed LaTeX build artifacts and kept only source files plus final submission PDFs.
