# GlobalFoundries - AI/ML Systems Engineer Tailoring Notes

## Resume Direction

Position Aryan as an early-career systems/performance engineer with strong computer science fundamentals, Python analysis code, C++/OpenMP runtime experimentation, reproducible benchmarking, ML/RL experimentation, and large-scale data pipeline experience. The job is not a generic applied AI role; it is a workload characterization, performance modeling, hardware/software tradeoff, and technical communication role.

The resume emphasizes:

- Self-Adaptive Parallelism: C++/OpenMP runtime instrumentation, per-epoch telemetry, adaptive scheduling, UCB optimization, benchmarking, speedup/efficiency/Karp-Flatt plots, and workload behavior analysis.
- MarioRL: ML/RL experimentation, PyTorch, Stable-Baselines3, TensorBoard, preprocessing, model comparison, checkpoints, and performance graphs.
- HealthTrend: Spark/PySpark/Kafka/Hadoop pipeline for distributed ingestion and processing.
- Diff-Grounded PR Generation: LLM evaluation, repository evidence, source-grounded generation, and metadata-driven context construction.
- AAIS: Python, PySpark, AWS Glue, SQL, Pandas, multiprocessing, large CSV processing, production data validation, and reproducible data workflows.
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
- MarioRL: PyTorch, Stable-Baselines3, PPO, DQN, Gym, TensorBoard, frame preprocessing, checkpoints, reward and training-speed graphs.
- HealthTrend: Spark, PySpark, Kafka, Hadoop HDFS, Docker Compose, CSV/JSON ingestion, stream and batch processing.
- Diff-Grounded PR Generation: Python, OpenAI API, GitHub API, commits, diffs, linked issues, metadata, LLM evaluation, source-grounded generation.
- BGSU GRA remains useful interview context for technical communication and leadership, but is intentionally omitted from the resume to keep the one-page layout readable.

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
- Distributed/data systems: HealthTrend and AAIS cover Spark, PySpark, Kafka/HDFS, SQL, and large-scale production processing.
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
