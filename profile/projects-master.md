# Projects Master

This document stores detailed project material for tailoring resumes, cover letters, and interview answers.

## Standard Project Structure

- `Platform-Ready Description`: copyable project paragraph for LinkedIn, cover letters, portfolios, or an expanded projects section.
- `Handshake Description`: copyable project description for Handshake project entries. Must be 500 characters or fewer.
- `Features`: product behavior, user-facing capability, or research functionality.
- `Tech Stack`: one comma-separated line with a domain prefix, such as `AI / Tech stack: Python, OpenAI API, LLM inference.`
- `Positioning Angles`: ways to frame the project for different job families.
- `Reusable Bullet Options`: ATS-friendly bullets for resumes and tailored applications.

## Travel Health Advisor - BGSU Hackathon 2025

Date: 2025  
Primary positioning: Hackathon health AI application, full-stack React/Express prototype, interactive health data visualization, Mistral AI chatbot  
Source: https://github.com/aryanmiriyala/BGSU-Hackathon-2025
Recognition: BGSU Hackathon 2025 AI & ML Track Winner

### Platform-Ready Description

Built a BGSU Hackathon 2025 AI/ML + Health track project with team VibeCoders: a full-stack travel health advisory prototype using React, Vite, Express, MongoDB/Mongoose, and Mistral AI. The application lets users click countries on an interactive `react-simple-maps` world map, retrieves country-specific disease records from an Express API backed by MongoDB aggregation, organizes disease risk and vaccination information, and generates a downloadable vaccination checklist PDF. It also includes a health-profile form, local user/health-profile persistence, dark-mode UI controls, route-based login/signup screens, and a floating Mistral AI chatbot that uses the user's health profile as context for travel-health questions.

### Handshake Description

Built a BGSU Hackathon 2025 health AI prototype with React, Vite, Express, MongoDB/Mongoose, and Mistral AI. Users select countries on an interactive map, view disease and vaccine guidance, save health-profile context, ask a Mistral chatbot travel-health questions, and generate vaccination checklist PDFs.

### Features

- Interactive world map for country selection using `react-simple-maps` and world-atlas geography data.
- Express API with MongoDB/Mongoose disease records and aggregation by country, disease, population affected, healthcare access, vaccine availability, recovery rate, and occurrence count.
- Health-profile form capturing chronic conditions, surgeries, medications, symptoms, severity, accommodations, assistive devices, and allergies.
- Disease advisory UI that groups vaccine-required and non-vaccine disease data, calculates risk levels, and displays travel recommendations.
- Downloadable vaccination checklist PDF generated with `@react-pdf/renderer`.
- Floating Mistral AI chatbot that builds prompt context from the user's saved health profile.
- React Router login/signup screens, localStorage-based user flow, dark mode, toast notifications, animated controls, and responsive CSS module styling.
- Vite environment-variable handling for Mistral API configuration.

### Tech Stack

Full-stack health AI / Tech stack: React 18, Vite, JavaScript, CSS modules, HTML, Express.js, Node.js, MongoDB, Mongoose, REST APIs, react-simple-maps, world-atlas, D3, TopoJSON, Axios, React Router, Mistral AI API, React Markdown, @react-pdf/renderer, React Toastify, Framer Motion, Lucide React, React Icons, dotenv, CORS, localStorage, npm.

### Positioning Angles

- Healthcare-adjacent software project
- Graduate software engineer project
- Full-stack JavaScript/React feature development
- Express/MongoDB health data API
- AI chatbot integration with user health context
- Interactive geospatial data visualization
- Health-profile and vaccination-checklist workflow
- PDF generation
- Hackathon teamwork

### Reusable Bullet Options

- Built a full-stack BGSU Hackathon 2025 health AI prototype with React, Vite, Express, MongoDB/Mongoose, and Mistral AI for travel-health guidance.
- Implemented an interactive country-selection map with `react-simple-maps`, retrieving disease records from an Express/MongoDB API and surfacing risk, vaccine availability, healthcare access, and recovery-rate data.
- Built a health-profile form and context-aware Mistral AI chatbot that used saved user health details to answer travel-health questions.
- Generated downloadable vaccination checklist PDFs with `@react-pdf/renderer` based on country-specific vaccine-required disease data.

## Fix-It-Flow - RocketHacks 2026

Date: 2026
Primary positioning: Hackathon sustainability AI application, voice-first repair assistant, multimodal inspection workflow, Next.js PWA
Source: https://github.com/aryanmiriyala/rockethacks-2026

### Platform-Ready Description

Built a RocketHacks 2026 submission called Fix-It-Flow: a voice-first, AI-powered sustainability assistant that helps users diagnose household appliance issues, attempt repair, and avoid unnecessary e-waste. The Next.js 14 PWA supports an inspection flow where users describe a problem by voice while showing the item through the camera; Gemini Vision analyzes live frames, Featherless.AI/Llama reasoning combines visual context with the conversation, and the app recommends outcomes in sustainability order: repair, replace only the broken part, repurpose, donate, or recycle. The repair flow generates concise step-by-step instructions, reads them aloud with ElevenLabs text-to-speech, supports hands-free commands such as next, repeat, help, and end session, and persists repair/inspection sessions in AWS DynamoDB.

### Handshake Description

Built Fix-It-Flow for RocketHacks 2026: a Next.js 14 PWA that uses camera input, Web Speech API, Gemini Vision, Featherless.AI/Llama, ElevenLabs TTS, and AWS DynamoDB to diagnose appliance issues, guide hands-free repair steps, and prioritize repair/reuse/recycling decisions.

### Features

- Voice-first inspection mode using browser camera input and Web Speech API transcription.
- Gemini Vision live-frame analysis for appliance/device identification, visible issue summaries, requested camera views, confidence, and safety warnings.
- Featherless.AI reasoning with Llama/Qwen-style models to combine visual evidence, user transcript, prior conversation, and sustainability priorities into structured findings.
- Sustainability recommendation policy prioritizing repair, part replacement, reuse/repurpose, donation, and recycling before buying new.
- Repair mode with AI-generated step-by-step guidance capped to concise flows for hands-free use.
- ElevenLabs text-to-speech streaming for spoken repair instructions and in-repair answers.
- Voice commands for next/done, repeat, help, and end session.
- Contextual Q&A during repair sessions so users can ask questions and then resume the current step.
- Next.js App Router API routes for inspection sessions, inspection turns, device identification, repair-step generation, speech synthesis, chat, uploads, and session CRUD.
- AWS DynamoDB persistence for session state, conversation history, frames, findings, repair steps, and status.
- Modular TypeScript architecture with `features/camera`, `features/voice`, `features/repair`, `server/clients`, `server/services`, and shared typed interfaces.
- PWA support, Tailwind CSS styling, and environment-driven configuration for Gemini, Featherless.AI, ElevenLabs, and AWS.

### Tech Stack

Voice-first sustainability AI / Tech stack: Next.js 14, React 18, TypeScript, Tailwind CSS, Next.js App Router, PWA, Web Speech API, browser camera APIs, Google Gemini Vision, Featherless.AI, Llama 3.1 / Qwen2.5-VL model calls, ElevenLabs text-to-speech, AWS DynamoDB, AWS SDK for JavaScript, AWS S3 / Rekognition client code, REST-style API routes, JSON parsing, session persistence, prompt engineering, multimodal reasoning, npm.

### Positioning Angles

- Voice-first AI product engineering
- Multimodal AI workflow with camera, speech, LLM reasoning, and TTS
- Sustainability/e-waste reduction application
- Full-stack Next.js PWA development
- Hands-free repair guidance
- AWS-backed session persistence
- Hackathon product architecture

### Reusable Bullet Options

- Built Fix-It-Flow for RocketHacks 2026, a Next.js 14/TypeScript PWA that uses camera input, voice commands, Gemini Vision, Featherless.AI/Llama reasoning, ElevenLabs TTS, and DynamoDB to guide appliance repair and recycling decisions.
- Implemented a voice-first inspection workflow that combined live-frame analysis, spoken user context, conversation history, structured findings, confidence scores, requested camera views, and safety warnings to diagnose household item issues.
- Designed hands-free repair guidance with AI-generated steps, ElevenLabs audio playback, contextual Q&A, and voice commands for next, repeat, help, and end session.
- Built typed Next.js API routes and AWS-backed session persistence for inspection turns, repair sessions, device identification, text-to-speech, chat, uploads, findings, frames, and repair steps.

## Additional Project Slots

Use this section to add future projects. Capture:

- Problem solved
- Users or audience
- Architecture
- Tech stack
- Features
- Deployment
- Measurable impact, if known
- Handshake description under 500 characters
- Reusable bullet options
- Cover-letter talking points

## LinkedIn Highlighted Projects

These projects were provided from Aryan's LinkedIn project highlights and should be treated as additional source material for targeted resumes, cover letters, and interview prep.

### Diff-Grounded Pull Request Description Generation with Structured Evidence using Large Language Models

Primary positioning: LLM research, software repository mining, evidence-grounded generation, automated evaluation

#### Platform-Ready Description

Developed an ICSME-published LLM research project for generating evidence-grounded GitHub pull request descriptions from real repository artifacts. The pipeline collects commits, file diffs, linked issues, and repository metadata; builds structured PR context; improves weak commit messages; summarizes file-level changes; and generates reviewer-ready descriptions under grounding constraints. Also built an automated LLM evaluation workflow to compare generated descriptions against raw code-change evidence. The approach outperformed baseline descriptions from the AIDev and PRSummarizer datasets in correctness, coverage, and clarity.

#### Handshake Description

Developed an ICSME-published LLM research pipeline that generates evidence-grounded GitHub PR descriptions from commits, diffs, linked issues, and repository metadata. Built structured context construction, grounded generation, and automated evaluation against raw code-change evidence.

#### Tech Stack

AI / Tech stack: Python, OpenAI API, LLM inference, prompt engineering, GitHub API, retrieval-augmented context construction, knowledge graphs, software repository mining, NLP, automated LLM evaluation, pandas, scikit-learn.

#### Positioning Angles

- LLM systems research
- Grounded generation
- Software engineering automation
- Evaluation pipelines
- Repository mining

#### Reusable Bullet Options

- Built an ICSME-published LLM research pipeline that generated evidence-grounded GitHub pull request descriptions from commits, diffs, linked issues, and repository metadata.
- Developed structured PR-context construction, weak-commit-message improvement, file-level summarization, and grounding-constrained generation workflows using Python, OpenAI API, and GitHub API.
- Built an automated LLM evaluation workflow comparing generated PR descriptions against raw code-change evidence, outperforming AIDev and PRSummarizer baselines in correctness, coverage, and clarity.

### DreamScape: AI-Powered Sleep Learning Companion

Primary positioning: AI mobile app, React Native, local-first architecture, generative study tools
Source: https://github.com/aryanmiriyala/MakeUC-DreamScape

#### Platform-Ready Description

Built a cross-platform mobile app for sleep-based microlearning. Users can create flashcards, import documents, generate short learning cues, and replay cues during simulated sleep sessions. The app uses Gemini to summarize PDF/TXT documents into concise study cues and generate multiple-choice morning quizzes. It includes a sleep-mode audio system using ElevenLabs text-to-speech and ambient sound generation, cached audio playback, selectable voice personas, background ambience, cue scheduling, session tracking, and local persistence for topics, flashcards, cues, sleep sessions, quiz results, and user settings.

#### Handshake Description

Built a React Native/Expo mobile app for sleep-based microlearning with Gemini document summarization, generated quizzes, ElevenLabs text-to-speech cues, audio caching, cue scheduling, session tracking, and local-first persistence for topics, flashcards, cues, sessions, quiz results, and settings.

#### Tech Stack

AI mobile / Tech stack: React Native, Expo SDK 54, Expo Router, TypeScript, Gemini API, ElevenLabs API, AI document summarization, AI quiz generation, text-to-speech, ambient audio generation, Expo AV, Expo FileSystem, Expo Document Picker, Zustand, AsyncStorage, Zod, React Navigation, local-first app architecture.

#### Positioning Angles

- Cross-platform mobile engineering
- AI-powered study tools
- Local-first mobile persistence
- Audio generation and playback
- Type-safe mobile state management

#### Reusable Bullet Options

- Built a cross-platform React Native/Expo mobile app for sleep-based microlearning with AI-generated study cues, quizzes, text-to-speech audio, and local-first session tracking.
- Integrated Gemini and ElevenLabs APIs to summarize documents, generate quizzes, synthesize learning cues, cache audio, and schedule simulated sleep-mode playback.
- Designed typed Zustand/AsyncStorage stores for topics, flashcards, cues, sleep sessions, quiz results, and user settings in a local-first mobile architecture.

### FalconGraph Search: AI-Powered Campus Knowledge Search

Primary positioning: RAG, campus search, graph interface, source-grounded answers
Source: https://github.com/aryanmiriyala/BGSUHackathon
Date: November 2025

#### Platform-Ready Description

Built an AI-powered campus answer engine for BGSU that turns disconnected university webpages, PDFs, and DOCX resources into a searchable link graph and source-grounded RAG experience. A multithreaded C++/OpenMP crawler uses a config-driven pipeline and thread-safe queues to collect resources; Python cleaning stages extract text and checkpoint normalized graph nodes and edges; Sentence Transformers/OpenAI embeddings and FAISS rank relevant chunks; and a FastAPI endpoint generates cited answers. A Next.js interface renders markdown responses, cited sources, and nearby graph context so users can trace answers to original campus resources.

#### Handshake Description

Built a BGSU campus answer engine with a multithreaded C++/OpenMP crawler, Python document cleaning, FAISS retrieval, FastAPI RAG, and a Next.js interface that returns cited answers with source graph context.

#### Tech Stack

RAG / Search / Tech stack: C++, OpenMP, Python, FastAPI, FAISS, Sentence Transformers, all-MiniLM-L6-v2, OpenAI API, text-embedding-3-small, RAG, embeddings, semantic retrieval, web crawling, HTML/PDF/DOCX parsing, document chunking, directed graphs, checkpointed data processing, Next.js, React, TypeScript, Tailwind CSS, DaisyUI.

#### Positioning Angles

- RAG search systems
- Source-grounded answer generation
- Web crawling and document ingestion
- Graph-based interfaces
- Campus knowledge search

#### Reusable Bullet Options

- Built a BGSU campus answer engine that integrated a multithreaded C++/OpenMP crawler, Python document processing, FAISS retrieval, FastAPI RAG, and a Next.js interface into one config-driven pipeline.
- Implemented checkpointed HTML/PDF/DOCX cleaning, graph-node and edge reconstruction, document chunking, Sentence Transformer/OpenAI embeddings, and semantic ranking across university resources.
- Generated source-grounded answers with inline citations and graph context, enabling users to trace each response back to the original campus webpages and documents.

### HealthTrend: Healthcare Big Data Streaming Pipeline

Primary positioning: distributed data systems, healthcare IoT, streaming and batch ingestion

#### Platform-Ready Description

Built a Dockerized proof-of-concept for a healthcare data platform that ingests structured patient records and semi-structured IoT health events. Apache NiFi routes CSV patient data into Hadoop HDFS and streams JSON IoT events into Kafka. Apache Spark reads from both HDFS and Kafka for downstream processing and validation. The project simulates a healthcare analytics architecture for patient records, heart rate, oxygen level, and temperature data inside an isolated Docker Compose environment.

#### Handshake Description

Built a Dockerized healthcare data pipeline using Apache NiFi, Kafka, Hadoop HDFS, Spark, PySpark, and Docker Compose. Routed CSV patient records into HDFS and JSON IoT health events into Kafka, then processed both sources for validation and downstream analytics.

#### Tech Stack

Data engineering / Tech stack: Apache NiFi, Apache Kafka, Apache Zookeeper, Apache Hadoop HDFS, Apache Spark, PySpark, Docker Compose, Python, JSON, CSV, healthcare IoT data, stream ingestion, batch storage, distributed processing, containerized data pipelines.

#### Positioning Angles

- Healthcare data engineering
- Streaming pipelines
- Distributed systems
- Dockerized proof-of-concept architecture
- Kafka/HDFS/Spark/NiFi

#### Reusable Bullet Options

- Built a Dockerized healthcare data pipeline using Apache NiFi, Kafka, Hadoop HDFS, and Spark to ingest structured patient records and stream IoT health events.
- Routed CSV patient data into HDFS and JSON health events into Kafka, then processed both sources with Spark/PySpark for validation and downstream analytics.

### MarioRL: Super Mario Reinforcement Learning Agent Comparison

Primary positioning: reinforcement learning, model comparison, PyTorch, experiment tracking
Source: https://github.com/aryanmiriyala/ReinforcementLearning-SuperMario

#### Platform-Ready Description

Built a reinforcement learning project comparing Proximal Policy Optimization and Deep Q-Networks on the Super Mario Bros environment. The project trains agents on level 1-1 using gym-super-mario-bros, applies environment preprocessing including frame skipping, resizing, grayscale conversion, and frame stacking, and tracks model performance through saved checkpoints and TensorBoard logs. It includes training/testing scripts, custom agent/network code, generated clips, experiment artifacts, and performance graphs comparing reward, episode length, and training speed.

#### Handshake Description

Built a reinforcement learning project comparing PPO and DQN agents on Super Mario Bros using Python, PyTorch, Stable-Baselines3, Gym, and TensorBoard. Implemented frame preprocessing, checkpoints, generated clips, and performance graphs for reward, episode length, and training speed.

#### Tech Stack

Reinforcement learning / Tech stack: Python, reinforcement learning, PPO, DQN, Stable-Baselines3, PyTorch, Gym, gym-super-mario-bros, NES-Py, TensorBoard, environment wrappers, frame preprocessing, model checkpointing, training logs, Jupyter Notebook.

#### Positioning Angles

- Reinforcement learning
- Deep learning experimentation
- Agent benchmarking
- Model evaluation and visualization

#### Reusable Bullet Options

- Built a reinforcement learning project comparing PPO and DQN agents on Super Mario Bros using PyTorch, Stable-Baselines3, Gym, and TensorBoard.
- Implemented environment preprocessing with frame skipping, resizing, grayscale conversion, and frame stacking, then evaluated agents through checkpoints, logs, clips, and performance graphs.

### RAG-Based Analysis of App Update Frequency and User Reviews

Primary positioning: RAG research, NLP, review mining, software maintenance analytics
Source: https://github.com/aryanmiriyala/RAG-Model-App-Review-Analysis

#### Platform-Ready Description

Built a research project using Retrieval-Augmented Generation to study how mobile app update frequency relates to user feedback in Google Play reviews. The pipeline preprocesses app review datasets, extracts structured review content, generates semantic embeddings with Sentence Transformers, stores review context in ChromaDB, and retrieves relevant evidence for comparative analysis across apps with different version histories. The system uses vector search and review-mining techniques to compare sentiment, recurring user concerns, and maintenance-related feedback patterns.

#### Handshake Description

Built a RAG research pipeline using Python, Sentence Transformers, ChromaDB, embeddings, vector search, and review mining to study how mobile app update frequency relates to Google Play review feedback, sentiment, recurring user concerns, and maintenance patterns.

#### Tech Stack

RAG / NLP / Tech stack: Python, RAG, Sentence Transformers, ChromaDB, embeddings, vector search, semantic retrieval, NLP, review mining, sentiment analysis, scikit-learn, JSON processing, data preprocessing, information retrieval, research evaluation, LaTeX.

#### Positioning Angles

- RAG evaluation
- NLP and information retrieval
- App review mining
- Software maintenance analytics

#### Reusable Bullet Options

- Built a RAG research pipeline using Sentence Transformers and ChromaDB to analyze how mobile app update frequency relates to Google Play review feedback.
- Applied semantic retrieval, vector search, sentiment analysis, and review mining to compare maintenance patterns, recurring user concerns, and app version histories.

### RocketGrades: Intelligent Assignment Feedback Platform

Primary positioning: full-stack AI education platform, secure LMS, file parsing, AI grading
Source: https://github.com/aryanmiriyala/rockethacks25
Date: March 2025
Recognition: RocketHacks 2025 winner in two MLH tracks

#### Platform-Ready Description

Built a full-stack education platform that helps teachers manage classes, assignments, student submissions, and feedback workflows with AI-assisted grading. The Angular frontend includes role-based teacher/student dashboards, Auth0 login/signup flows, file upload/viewing, assignment management, and chat interactions. The TypeScript/Express backend exposes REST APIs for users, classes, assignments, submissions, files, and chat, with MongoDB/Mongoose models for persistence. Uploaded submissions are stored in AWS S3, parsed from PDF, DOCX, HTML, and text formats, then graded with a LangChain + Mistral AI pipeline returning structured scores, feedback, strengths, improvements, and rubric breakdowns.

#### Handshake Description

Built a full-stack AI assignment feedback platform with Angular, TypeScript, Express, MongoDB, Auth0, AWS S3, LangChain, and Mistral AI. Supported role-based dashboards, REST APIs, file uploads, PDF/DOCX/HTML parsing, and AI-generated scores, feedback, strengths, improvements, and rubric breakdowns.

#### Tech Stack

Full-stack AI education / Tech stack: Angular 19, TypeScript, Auth0, Node.js, Express, MongoDB, Mongoose, REST APIs, JWT, bcrypt, AWS S3, AWS Amplify, Multer, LangChain, Mistral AI, PDF parsing, Mammoth, JSDOM, Tailwind CSS, DaisyUI.

#### Positioning Angles

- Full-stack education platform
- AI grading workflow
- Secure role-based dashboards
- File processing and cloud storage
- REST API design

#### Reusable Bullet Options

- Built a full-stack AI assignment feedback platform with Angular, TypeScript, Express, MongoDB, Auth0, AWS S3, LangChain, and Mistral AI.
- Designed REST APIs and MongoDB/Mongoose models for users, classes, assignments, submissions, files, and chat while supporting role-based teacher/student dashboards.
- Implemented submission upload, parsing, and AI grading across PDF, DOCX, HTML, and text files, returning structured scores, feedback, strengths, improvements, and rubric breakdowns.

### Self-Adaptive Parallelism via OpenMP Runtime Coordination

Primary positioning: systems research, parallel computing, adaptive scheduling, performance benchmarking

#### Platform-Ready Description

Built a parallel-computing research system that studies how OpenMP workloads can adapt runtime behavior rather than rely on a single fixed scheduling strategy. The system instruments parallel kernels, records per-epoch telemetry, and uses a UCB-based controller to explore combinations of scheduling policy, chunk size, and thread count. Evaluated the adaptive runtime against serial and fixed-policy baselines across Mandelbrot rendering, heat diffusion, and reduction workloads, then generated benchmark summaries and paper-ready plots for runtime, speedup, efficiency, Karp-Flatt behavior, and scheduler decisions.

#### Handshake Description

Built a C++/OpenMP parallel-computing research system that records per-epoch telemetry and uses a UCB controller to tune scheduling policy, chunk size, and thread count. Benchmarked Mandelbrot, heat diffusion, and reduction workloads and generated runtime, speedup, efficiency, and scheduler-behavior plots.

#### Tech Stack

Systems / Parallel computing / Tech stack: C++, OpenMP, Python, PyQt, Docker, Make, Linux, TCP servers, runtime instrumentation, UCB bandit optimization, adaptive scheduling, CSV telemetry pipelines, performance benchmarking, data visualization.

#### Positioning Angles

- Parallel computing
- Systems research
- Adaptive runtime control
- Performance benchmarking
- C++/OpenMP

#### Reusable Bullet Options

- Built a C++/OpenMP adaptive runtime research system that used per-epoch telemetry and a UCB controller to tune scheduling policy, chunk size, and thread count.
- Benchmarked adaptive scheduling against serial and fixed-policy baselines across Mandelbrot, heat diffusion, and reduction workloads.
- Generated paper-ready performance summaries and plots for runtime, speedup, efficiency, Karp-Flatt behavior, and scheduler decisions.

## GitHub And Local Repository Audit Projects

The following entries were added or expanded after a July 2026 audit of Aryan's public GitHub account and locally available GitHub clones. Capabilities listed as implemented were verified in source code, manifests, configuration, or commit history. Roadmap items are labeled separately and must not be used as completed-work claims.

### AI Project Management Tool: Explainable Execution-Planning Prototype

Date: May 2026

Primary positioning: B2B product prototype, technical project planning, explainable assignment recommendations, typed Next.js application architecture

Source: Local GitHub clone of `aryanmiriyala/AI-Project-Management-Tool` (private or unavailable through the public API at audit time)

Implementation status: Interactive front-end prototype with typed mock data; external AI, database, authentication, and GitHub ingestion are planned but not implemented

#### Platform-Ready Description

Built an interactive Next.js/TypeScript prototype for turning ambiguous software initiatives into reviewable execution plans. The application includes a planning workspace for project briefs and project types, generated task templates, typed project/task/collaborator models, project dashboards, risk and status views, skill requirements, and explainable owner recommendations containing confidence and rationale. Also documented a modular-monolith architecture for future requirement parsing, repository intelligence, task decomposition, workload-aware matching, audit logs, and human approval, while keeping those roadmap capabilities separate from the implemented prototype.

#### Handshake Description

Built a Next.js/TypeScript execution-planning prototype with project intake, generated task templates, typed project/task/collaborator models, risk dashboards, skill requirements, and explainable ownership recommendations containing confidence and rationale.

#### Implemented Features

- Next.js App Router landing page and multi-route planning workspace.
- Project intake fields for project name, type, and brief.
- Template-driven generation of reviewable plan tasks for platform, feature, and integration work.
- Typed domain models for projects, tasks, collaborators, statuses, skills, risks, and assignment recommendations.
- Workspace dashboard showing active projects, collaborators, timelines, statuses, and at-risk work.
- Project detail views with goals, risks, task boards, required skills, recommended owners, confidence levels, and recommendation rationale.
- npm workspace structure separating the web application from future shared packages.
- Product and architecture documentation covering users, success signals, boundaries, security requirements, and scaling phases.

#### Planned Architecture — Do Not Present as Implemented

- OpenAI Responses API with structured outputs for requirement parsing and project decomposition.
- PostgreSQL, Drizzle ORM, and pgvector for relational workflow data and retrieval.
- GitHub App/webhooks for repository and contributor intelligence.
- Inngest background workflows, organization tenancy, RBAC, audit logs, Sentry/OpenTelemetry, Vitest, and Playwright.

#### Tech Stack

Implemented product prototype / Tech stack: Next.js 15, React 19, TypeScript 5.8, App Router, CSS, npm workspaces, typed domain models, mock-data services, responsive application UI, product architecture documentation.

#### Positioning Angles

- Product-minded software engineering
- Explainable AI/human-in-the-loop interface design
- Technical project planning and task decomposition
- Typed frontend architecture
- Risk and workload visualization
- Translating an ambiguous product concept into an implementable MVP boundary

#### Reusable Bullet Options

- Built a Next.js 15/TypeScript execution-planning prototype that transformed project briefs into reviewable task plans and displayed skills, risks, statuses, and explainable owner recommendations.
- Designed typed models and multi-route dashboards for projects, tasks, collaborators, assignment confidence, recommendation rationale, timelines, and delivery risks.
- Scoped a modular-monolith roadmap for repository-aware planning and human-approved AI recommendations while keeping unimplemented AI and data services clearly separated from the working prototype.

### Personal Engineering Portfolio: Star-Chart Case-Study Platform

Date: 2026

Primary positioning: frontend engineering, design systems, interactive data storytelling, accessible motion, technical case studies

Source: Local GitHub clone of `aryanmiriyala/my-personal-website` (private or unavailable through the public API at audit time)

#### Platform-Ready Description

Built a responsive engineering portfolio with Next.js 15, React 19, TypeScript, and Tailwind CSS 4 around a custom star-chart visual system. The site combines a canvas starfield, animated project constellation, semantic experience/research/project content, statically generated case-study routes, and scroll-driven architecture walkthroughs. GSAP and Lenis coordinate motion while `prefers-reduced-motion`, focus states, semantic landmarks, fluid typography, sitemap/robots metadata, and responsive navigation preserve accessibility and search visibility. Project, publication, experience, volunteering, and skills content is maintained through typed data modules rather than duplicated page markup.

#### Handshake Description

Built a responsive Next.js/TypeScript engineering portfolio with a custom star-chart design system, canvas visuals, GSAP/Lenis motion, statically generated project case studies, scroll-driven architecture walkthroughs, typed content modules, SEO metadata, and reduced-motion accessibility.

#### Features

- Canvas-based cosmic background and animated constellation for featured projects.
- Statically generated `/work/<slug>` case studies with problem, architecture, engineering decisions, and outcomes.
- Scroll-driven architecture visualization using GSAP ScrollTrigger.
- Typed content modules for projects, publications, experience, volunteering, skills, and contact information.
- Custom typography and design tokens using Bricolage Grotesque, Hanken Grotesk, and IBM Plex Mono.
- Responsive navigation, fluid typography, focus states, semantic landmarks, and reduced-motion behavior.
- Contact form integration, Vercel Analytics, sitemap, robots metadata, favicon assets, and Google site-verification file.
- Exactly pinned dependency versions and lockfile for reproducible installs.

#### Tech Stack

Portfolio / Tech stack: Next.js 15, React 19, TypeScript 5.9, Tailwind CSS 4, App Router, static generation, Canvas API, GSAP 3, ScrollTrigger, Lenis, custom CSS design tokens, Vercel Analytics, responsive design, accessibility, SEO metadata, npm.

#### Positioning Angles

- Frontend and full-stack product engineering
- Design-system implementation
- Accessible motion and interaction design
- Technical storytelling and case-study architecture
- Responsive and SEO-aware web development
- Reproducible dependency management

#### Reusable Bullet Options

- Built a responsive Next.js 15/TypeScript engineering portfolio with a custom star-chart design system, canvas visuals, GSAP/Lenis motion, and statically generated technical case studies.
- Implemented scroll-driven architecture walkthroughs and typed content modules for projects, publications, experience, volunteering, and skills, keeping technical narratives structured and reusable.
- Added responsive navigation, semantic landmarks, focus states, reduced-motion behavior, sitemap/robots metadata, analytics, and pinned dependencies to improve accessibility, discoverability, and reproducibility.

### FindYourFlame: Campus Matchmaking Interface Prototype

Date: November--December 2025

Primary positioning: Next.js product prototype, Supabase authentication, campus-community UX, responsive frontend

Source: Local GitHub clone of `aryanmiriyala/bgsu-matchmaking` (private or unavailable through the public API at audit time)

Implementation status: Marketing experience and `.edu` Supabase authentication are implemented; matchmaking, chat, AI icebreakers, moderation, and database schemas remain roadmap concepts

#### Platform-Ready Description

Built a responsive campus-matchmaking interface prototype with Next.js 16, React 19, TypeScript, Tailwind CSS, DaisyUI, and Supabase authentication. The implemented product includes a branded landing experience, animated intro and typewriter hero, campus-focused feature and FAQ sections, sign-up/sign-in mode switching, `.edu` email validation, password validation, Supabase email confirmation and password authentication, persisted browser sessions, loading/error/success feedback, and responsive navigation. The repository also documents future matching modes and AI-assisted icebreakers, but those capabilities are not yet implemented.

#### Handshake Description

Built a responsive Next.js/TypeScript campus-matchmaking prototype with Tailwind/DaisyUI, animated onboarding, `.edu` email validation, and Supabase sign-up/sign-in flows with confirmation, persisted sessions, and user feedback states.

#### Implemented Features

- Responsive marketing page for campus-only social matching.
- Animated letter intro and timed typewriter hero components.
- Campus-focused product sections, experience concepts, onboarding steps, FAQ, and waitlist interface.
- Sign-up and sign-in modes with controlled React form state.
- Client-side `.edu` email and minimum-password validation.
- Supabase email/password authentication, confirmation redirect, session persistence, and automatic token refresh.
- Loading, success, and error states plus post-login navigation.

#### Roadmap — Do Not Present as Implemented

- Matchmaking algorithms, interest vectors, availability matching, realtime chat, blind-spark reveals, prompt roulette, AI-generated icebreakers, and automated moderation.

#### Tech Stack

Campus product prototype / Tech stack: Next.js 16, React 19, TypeScript, App Router, Tailwind CSS 3.4, DaisyUI 5, Supabase JavaScript client, Supabase Auth, React state management, responsive UI, CSS animation, npm.

#### Positioning Angles

- Consumer product prototyping
- Authentication and onboarding UX
- Responsive Next.js frontend development
- Campus/community software concepts
- Honest MVP and roadmap scoping

#### Reusable Bullet Options

- Built a responsive Next.js 16/TypeScript campus-matchmaking prototype with Tailwind CSS, DaisyUI, animated onboarding, and campus-focused product flows.
- Implemented `.edu` email validation and Supabase sign-up/sign-in flows with email confirmation, password validation, persistent sessions, automatic token refresh, and user feedback states.
- Separated implemented authentication and interface functionality from planned matchmaking, chat, moderation, and AI features to maintain an honest MVP boundary.

### PDFsplitter: Installable PDF Command-Line Utility

Date: March 2026

Primary positioning: developer tooling, Node.js CLI, file processing, defensive input validation

Source: https://github.com/aryanmiriyala/PDFsplitter

#### Platform-Ready Description

Built an installable Node.js command-line utility that divides a PDF into two output files at a user-selected page. The `pdfsplit` executable validates argument presence, positive integer input, source-file existence, PDF extension, and split-page bounds; loads and copies pages with `pdf-lib`; preserves the input directory and base filename; names both outputs by their page ranges; and returns clear success or failure messages with nonzero exit codes for invalid usage.

#### Handshake Description

Built an installable Node.js CLI with `pdf-lib` that validates input files and split bounds, divides a PDF at a requested page, preserves the source path and filename, and creates two clearly named page-range outputs with actionable error handling.

#### Features

- Globally installable `pdfsplit` binary declared through `package.json`.
- PDF loading, page copying, document creation, and serialization using `pdf-lib`.
- Validation for missing arguments, non-integer or negative pages, absent files, non-PDF extensions, and out-of-range split points.
- Automatic output naming such as `report-1-3.pdf` and `report-4-10.pdf`.
- Error handling with human-readable CLI messages and nonzero process exit codes.

#### Tech Stack

Developer tooling / Tech stack: JavaScript, Node.js, CommonJS, pdf-lib, filesystem APIs, path APIs, CLI argument parsing, binary file processing, npm package binaries.

#### Positioning Angles

- Node.js developer tooling
- Command-line interface design
- File and document processing
- Defensive input validation
- Small end-to-end utility ownership

#### Reusable Bullet Options

- Built an installable Node.js CLI with `pdf-lib` that split source PDFs into two page-range files at a user-selected boundary.
- Implemented defensive validation for missing arguments, invalid page numbers, missing files, non-PDF inputs, and out-of-range splits, returning actionable errors and process exit codes.
- Automated path-preserving output generation with page-range filenames to make split documents immediately identifiable.

### Yoda: BGSU Campus Navigator

Date: March 2023

Primary positioning: Flutter mobile development, Google Maps integration, campus navigation, hackathon delivery

Source: https://github.com/aryanmiriyala/CS23_YODA

Recognition: Second Prize, BGSU Hackathon 2023

Evidence source: Typed portfolio project data; repository was not available through the public GitHub API during the July 2026 audit

#### Platform-Ready Description

Built a Flutter/Dart campus-navigation application for BGSU students with origin and destination selection, building information cards, campus images and metadata, Google Maps markers, and a straight-line route preview between selected locations. Delivered the application during the BGSU Hackathon and earned second prize.

#### Handshake Description

Built a Flutter/Dart BGSU campus navigator with origin/destination selection, building cards and metadata, Google Maps markers, and route previews; delivered it during the 2023 BGSU Hackathon and earned second prize.

#### Tech Stack

Mobile / Navigation / Tech stack: Flutter, Dart, google_maps_flutter, Google Maps SDK, map markers, route visualization, mobile UI, campus building data.

#### Positioning Angles

- Cross-platform mobile development
- Maps and location-based interfaces
- Hackathon delivery
- Student/community software
- Early end-to-end application development

#### Reusable Bullet Options

- Built a Flutter/Dart BGSU campus navigator with building metadata, Google Maps markers, origin/destination controls, and route previews, earning second prize at the 2023 BGSU Hackathon.
- Integrated `google_maps_flutter` with campus location data to help students select buildings and preview navigation between campus destinations.

### Career Ops: Application and Job-Discovery Automation System

Date: 2025--2026

Primary positioning: workflow automation, Python CLI tooling, ATS integrations, document generation and validation, structured career data

Source: https://github.com/aryanmiriyala/career-ops

#### Platform-Ready Description

Built a repository-centered career operations system that separates job discovery from application-package generation. A dependency-light Python CLI generates targeted ATS search queries, fetches structured postings from configured Greenhouse, Lever, Ashby, and SmartRecruiters endpoints, supplements them with public job-board APIs, discovers and validates ATS board identifiers, scores and filters early-career roles, maintains a minimal CSV inbox, and writes dated Markdown reports. A second workflow stores verified career source material, creates role-specific LaTeX resumes and cover letters, tracks applications, and validates required artifacts, one-page PDF output, text extraction, alignment notes, and build-artifact cleanup.

#### Handshake Description

Built a Python career-operations system with structured Greenhouse/Lever/Ashby/SmartRecruiters ingestion, role filtering, CSV/Markdown reporting, targeted LaTeX application packages, PDF text/page validation, and repository-based application tracking.

#### Features

- Explicit separation between broad job discovery and selected-role application generation.
- Config-driven role buckets, source catalogs, ATS adapters, location/experience filters, and company watchlists.
- Structured direct ATS ingestion for Greenhouse, Lever, Ashby, and SmartRecruiters.
- Public-job-board supplements from Arbeitnow and RemoteOK.
- ATS URL/token discovery and verification from collected search-result links.
- Strict CSV inbox containing company, position, posted date, pull date, and URL, with noisy scoring details moved to dated reports.
- Freshness tracking based on first discovery when providers omit reliable posting timestamps.
- Role-fit scoring, strict shortlist and broader review-candidate outputs, and manual application approval.
- Source-of-truth profile documents for experience, projects, skills, bullet banks, and writing guidance.
- Targeted LaTeX resume/cover-letter generation with job keyword maps, truthful alignment notes, and application tracking.
- Package validator checking required files, cover-letter artifacts, recorded alignment results, one-page resume PDFs, extractable text, and leftover LaTeX build artifacts.

#### Tech Stack

Workflow automation / Tech stack: Python 3, standard-library HTTP/JSON/CSV processing, CLI argument parsing, Greenhouse API, Lever API, Ashby API, SmartRecruiters API, Arbeitnow API, RemoteOK API, JSON configuration, CSV, Markdown, LaTeX, pdflatex, pdfinfo, pdftotext, Git, repository-based workflows.

#### Positioning Angles

- End-to-end workflow automation
- API and ATS integration
- Config-driven data ingestion and filtering
- Developer productivity tooling
- Document-generation pipelines
- Validation and human-in-the-loop decision systems
- Product judgment around data quality and source-of-truth design

#### Reusable Bullet Options

- Built a Python career-operations system that ingested structured postings from Greenhouse, Lever, Ashby, and SmartRecruiters, filtered early-career roles, and generated CSV and dated Markdown review outputs.
- Designed separate job-discovery and application-generation pipelines with explicit handoff rules, structured profile data, targeted LaTeX documents, tracker updates, and human approval boundaries.
- Implemented application-package validation for required artifacts, one-page PDF output, text extraction, alignment evidence, and generated-build cleanup, improving consistency across role-specific submissions.

### Automated GitHub Profile README

Date: 2026

Primary positioning: GitHub Actions automation, API integration, generated documentation, resilient repository metadata workflows

Source: https://github.com/aryanmiriyala/aryanmiriyala

#### Platform-Ready Description

Built a scheduled GitHub Actions workflow and Node.js generator that refreshes featured-project metadata in a profile README. The script reads a JSON project configuration, queries the GitHub REST API for repository language, star count, links, and activity timestamps, gracefully falls back to configured names and URLs when repositories are unavailable, generates Markdown cards, replaces only a marker-delimited README section, and commits changes only when the generated output differs.

#### Handshake Description

Built a scheduled GitHub Actions and Node.js workflow that queries repository metadata, generates featured-project Markdown, safely replaces marker-delimited README content, falls back for unavailable repositories, and commits only when output changes.

#### Features

- Weekly cron schedule plus manual workflow dispatch.
- GitHub REST API client with authenticated headers, explicit errors, and optional 404 fallback behavior.
- JSON-driven featured-project configuration.
- Generated language, star-count, repository-link, and last-updated metadata.
- Marker-based README replacement that fails safely when expected boundaries are absent.
- Automated commit, rebase, and push only when staged content changed.
- Node.js 20 GitHub Actions runtime with repository-scoped contents permission.

#### Tech Stack

Developer automation / Tech stack: JavaScript, Node.js, ES modules, GitHub REST API, GitHub Actions, YAML, JSON, Markdown generation, filesystem APIs, scheduled workflows, Git automation.

#### Positioning Angles

- GitHub Actions and CI automation
- API-driven documentation generation
- Resilient fallback and error handling
- Repository maintenance tooling
- Small automation ownership

#### Reusable Bullet Options

- Built a scheduled GitHub Actions and Node.js workflow that queried repository metadata and regenerated featured-project Markdown for a developer profile.
- Implemented marker-delimited README replacement, unavailable-repository fallbacks, and change-aware commits to prevent destructive or unnecessary automated updates.
- Integrated GitHub REST API data for repository language, stars, links, and activity timestamps through a JSON-configured generation pipeline.

## Repository Audit: Not Yet Resume-Ready

Keep these repositories in the inventory so future work can be recognized, but do not use them as authored project evidence until substantive implementation or contribution history exists.

- `Damn-Vulnerable-RESTaurant-API-Game`: a clone/template of an upstream FastAPI/PostgreSQL security-training application. The audited code and authorship metadata belong to the upstream project; no Aryan-authored modification was verified. It may support a learning narrative only if Aryan documents vulnerabilities completed, fixes implemented, or a separate write-up.
- `SolarSystemSim`: contains only a one-line README describing an intended solar-system simulation; no implementation was present in the local clone.
- `FalconGames`: public repository with a collaborative browser-game description but no committed source code.
- `beach-game`: public repository with a Three.js learning description but no committed source code.
- `clinker`: fork of the upstream gene-cluster comparison project. Do not claim the upstream implementation; add only if Aryan's own commits or contributions are identified.
- `FindYourFlame` roadmap features: matching algorithms, realtime chat, AI icebreakers, moderation, and production data models are planned, not implemented.
- `AI Project Management Tool` roadmap features: external AI generation, repository ingestion, PostgreSQL/Drizzle persistence, authentication, background jobs, and production observability are planned, not implemented.
