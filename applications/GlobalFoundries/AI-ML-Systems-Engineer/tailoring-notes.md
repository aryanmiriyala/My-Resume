# GlobalFoundries - AI/ML Systems Engineer Tailoring Notes

## Resume Direction

Position Aryan as an early-career systems/performance engineer with strong computer science fundamentals, Python analysis code, C++/OpenMP runtime experimentation, reproducible benchmarking, ML/RL experimentation, and large-scale data pipeline experience. The job is not a generic applied AI role; it is a workload characterization, performance modeling, hardware/software tradeoff, and technical communication role.

## Job Keyword Map

Required skills:

- Computer Science degree, 0-2 years of relevant systems/ML/performance engineering experience, English written/verbal fluency, strong GPA, Python analysis code, reproducible modeling, technical communication.

Repeated terms:

- AI/ML workloads, workload characterization, performance modeling, throughput, latency, efficiency, architecture discussions, runtime, scheduling, memory layout, KPIs, written reports, presentations.

Responsibilities:

- Study AI/ML workload behavior, build quantitative models, evaluate throughput/latency/efficiency, reason about bottlenecks, communicate findings, and contribute to architecture/design tradeoff discussions.

Domain language:

- Semiconductor systems, hardware/software tradeoffs, inference/training workloads, compute and memory behavior, model validation, pre-silicon estimates, compiler/runtime collaboration.

Must-have tools:

- Python, C++/OpenMP, benchmarking, reproducible analysis, performance telemetry, PyTorch/TensorBoard, SQL/data pipelines where relevant.

Nice-to-have tools:

- Spark/PySpark, AWS Glue, LLM evaluation, Docker/Linux, reinforcement learning experimentation.

Unsupported terms to avoid:

- MLIR, IREE, TVM, RISC-V, silicon validation, SoC architecture ownership, roofline analysis, operational intensity profiling, ISA extensions, memory subsystem sizing, AI compiler toolchains, CUDA/GPU programming unless Aryan later verifies direct experience.

The resume emphasizes:

- Self-Adaptive Parallelism: C++/OpenMP runtime instrumentation, per-epoch telemetry, adaptive scheduling, UCB optimization, benchmarking, speedup/efficiency/Karp-Flatt plots, and workload behavior analysis.
- MarioRL: ML/RL experimentation, PyTorch, Stable-Baselines3, TensorBoard, preprocessing, model comparison, checkpoints, and performance graphs.
- Diff-Grounded PR Generation: LLM evaluation, repository evidence, source-grounded generation, and metadata-driven context construction.
- AAIS: Python, PySpark, AWS Glue, SQL, Pandas, multiprocessing, large CSV processing, production data validation, and reproducible data workflows.
- Alliance for Paired Kidney Donation: Lucee/ColdFusion work on an AWS-hosted healthcare operations platform, including anti-CSRF coverage, audit logging, date/time picker migrations, logistics defaults, and reliability fixes.
- Technical communication remains reflected through the systems project outputs, resume project descriptions, and cover letter; the BGSU GRA role was removed from the tailored resume to improve readability.
- SmartSolve: AI-enabled internal software, QMS relationship modeling, reproducible Docker development environments, and secure workflow design.

## Company Research Notes

- GF describes itself as a manufacturer of essential semiconductors enabling AI at scale from cloud to physical world.
- GF emphasizes differentiated, power-efficient and high-performance solutions, global manufacturing across the U.S., Europe, and Asia, and innovation through partnerships.
- Source used for company context: https://gf.com/about-gf/

## Cover Letter Angle

Use a technical, honest, personal angle: Aryan is drawn to the role because it combines ML workloads, systems behavior, performance reasoning, and reproducible analysis. Lead with the self-adaptive OpenMP scheduling project as the closest proof point. Be transparent that Aryan does not have direct silicon-design experience, while emphasizing strong CS fundamentals, 4.00 GPA, systems experimentation, Python analysis, and communication.

## Strongest Matching Experience / Projects

- Self-Adaptive Parallelism: C++, OpenMP, Python, runtime instrumentation, UCB controller, scheduling policy, chunk size, thread count, Mandelbrot, heat diffusion, reduction workloads, serial/fixed-policy baselines, runtime/speedup/efficiency/Karp-Flatt plots.
- AAIS Data Engineering: Python, PySpark, AWS Glue, SQL, 20+ TB of production insurance data, 700+ member companies, validation, reproducible workflows.
- AAIS Software Engineering: Python/JSON automation, 1,000+ SQL tables, Oracle/PostgreSQL, Python/Pandas data-cleaning workflows, multiprocessing, fuzzy matching, hashing.
- Alliance for Paired Kidney Donation: Lucee/ColdFusion, AWS-hosted healthcare platform, anti-CSRF protection, audit logging, date/time picker modernization, logistics defaults, reliability fixes.
- MarioRL: PyTorch, Stable-Baselines3, PPO, DQN, Gym, TensorBoard, frame preprocessing, checkpoints, reward and training-speed graphs.
- Diff-Grounded PR Generation: Python, OpenAI API, GitHub API, commits, diffs, linked issues, metadata, LLM evaluation, source-grounded generation.
- HealthTrend remains supporting source material for Spark/Kafka/Hadoop context, but was omitted from the tailored resume because internship experience takes precedence over project breadth.
- BGSU GRA remains useful interview context for technical communication and leadership, but is intentionally omitted from the resume to keep the one-page layout readable.

## Bullet Audit

Every experience and project bullet was checked against: action verb + what changed + technology/method + scope/domain + impact/result.

Experience bullets checked:

- SmartSolve bullets lead with supported/built/created, name QMS, Next.js, TypeScript, PostgreSQL, Drizzle ORM, SSO, auth middleware, Docker, WSL2/Colima, and explain traceability, secure workflows, and reproducible development.
- AAIS Data Engineering bullets lead with automated/built, name Python, PySpark, AWS Glue, SQL, S3, IAM, MDM, and include verified scale of 20+ TB and 700+ member companies.
- AAIS Software Engineering bullets lead with engineered/built/automated, name Python/JSON, SQL, Oracle/PostgreSQL, Pandas, AWS Lambda, hashlib/boto3, S3, and include verified 1,000+ table and 10+ insurance-line scope.
- APKD bullet leads with built and stabilized, names Lucee/ColdFusion and AWS-hosted healthcare operations, and explains security, auditability, date/time modernization, logistics defaults, and reliability fixes.

Project bullets checked:

- Self-Adaptive Parallelism bullet names C++, OpenMP, Python, Docker, Linux, per-epoch telemetry, UCB control, scheduling policy, chunk size, thread count, and performance plots across three workloads.
- MarioRL bullet names Python, PyTorch, Stable-Baselines3, Gym, TensorBoard, PPO, DQN, preprocessing, checkpoints, generated clips, and performance graphs.
- Diff-Grounded PR Generation bullet names Python, OpenAI API, GitHub API, LLM evaluation, commits, diffs, linked issues, metadata, structured PR descriptions, and source-grounded output evaluation.

Weak bullets rewritten:

- Consolidated the self-adaptive runtime and performance-output project bullets into one stronger project entry to make room for APKD while preserving performance-modeling evidence.
- Removed HealthTrend from the submitted resume because internship experience takes precedence over project breadth; kept it as supporting source material in these notes.

## Important Keyword Targets

AI/ML Systems Engineer, workload analysis, workload characterization, performance modeling, systems optimization, Python analysis code, reproducible models, throughput, latency, efficiency, KPIs, technical communication, written reports, presentations, architecture discussions, runtime, scheduling, kernel optimization, memory layout, inference and training stack, machine learning workloads, C++, OpenMP, PyTorch, TensorBoard, Spark, PySpark, distributed processing, LLM evaluation.

## Gaps / Intentionally Omitted Unsupported Keywords

- Direct semiconductor hardware architecture experience is not claimed.
- Direct silicon validation, SoC architecture, IP architecture, ISA extensions, memory subsystem sizing, on-chip/off-chip bandwidth allocation, roofline analysis, operational intensity profiling, and bottleneck decomposition are not claimed as completed work.
- MLIR, IREE, TVM, RISC-V, Vector/Matrix extensions, and AI compiler toolchain hands-on experience are intentionally omitted from skills because they are not verified.
- CNN/transformer/recurrent architecture implementation is not overstated; related ML experience is framed through RL experimentation, LLM inference/RAG, and performance analysis rather than unsupported model-family expertise.
- 100% in-office Dallas feasibility must be confirmed before submitting.

## Alignment Pass

ATS-style score: 83/100

Strong matches:

- Systems/performance: Self-Adaptive Parallelism provides the strongest match for runtime instrumentation, scheduling, workload benchmarking, performance plots, and systems optimization.
- Python analysis/reproducibility: AAIS data workflows, Python/Pandas pipelines, PySpark/Glue processing, and project benchmark outputs support clean analysis code and reproducible workflows.
- ML experimentation: MarioRL supports PyTorch, RL agent comparison, TensorBoard logging, preprocessing, checkpoints, and performance graphs.
- LLM evaluation: Diff-Grounded PR Generation supports source-grounded generation, repository evidence, metadata-driven context, and automated evaluation.
- Distributed/data systems: AAIS covers PySpark, Glue, SQL, AWS workflows, validation, and large-scale production processing; HealthTrend remains supporting source material outside the submitted resume.
- Internship continuity: SmartSolve, AAIS Data Engineering, AAIS Software Engineering, and APKD are all represented in Experience, with project content compressed before cutting internship roles.
- Technical communication: the systems project, benchmark outputs, and cover letter support written analysis, reproducible plots, and explaining technical results.
- New graduate fit: B.S. and M.S. in Computer Science, 4.00 GPA, internships, leadership, and project experience align with the NCG program.

Gaps / intentionally omitted unsupported keywords:

- The role has significant hardware architecture, semiconductor, roofline analysis, AI compiler, and RISC-V keywords that are not directly supported.
- The resume avoids unsupported MLIR/IREE/TVM/RISC-V claims.
- Dallas 100% in-office requirement is a major practical constraint.

Recommended improvements:

- If truthful, add any coursework or project exposure to computer architecture, compilers, operating systems, parallel computing, numerical methods, performance modeling, or hardware/software co-design.
- If Aryan has any direct class exposure to roofline analysis, MLIR, TVM, RISC-V, SIMD/vectorization, GPU programming, CUDA, or computer architecture simulators, add it before submitting.
- Be ready to explain the self-adaptive scheduling project deeply: telemetry design, controller behavior, benchmark methodology, what each workload stressed, and how the plots informed conclusions.

## Verification

- Resume compiled to exactly one page.
- Cover letter compiled to one page.
- PDF text extraction reviewed for ATS-readable content.
- Visual PDF render reviewed for spacing, readability, and bottom-of-page density.
- Application validator run.
