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

#### Platform-Ready Description

Built an AI-powered campus search prototype for BGSU that combines lightweight RAG with live web search across stored and crawled university webpages, PDFs, and campus resources. The system ingests and stores crawled content, chunks documents into retrievable passages, retrieves relevant context for user questions, and calls LLM inference to generate grounded answers with source-aware summaries. Also worked on graph-search functionality, using page/resource relationships to power an interactive graph interface that helps users trace how answers connect back to original campus sources.

#### Handshake Description

Built an AI-powered BGSU campus search prototype combining lightweight RAG, live web search, crawled webpages, PDFs, document chunking, retrieval, and LLM inference. Added graph-search functionality so users can trace source-grounded answers back to original campus resources.

#### Tech Stack

RAG / Search / Tech stack: Python, Flask, OpenAI API, LLM inference, lightweight RAG, embeddings, vector retrieval, semantic search, live web search, web crawling, PDF parsing, document chunking, React, Next.js, Three.js, Tailwind CSS, C++, graph algorithms, pandas.

#### Positioning Angles

- RAG search systems
- Source-grounded answer generation
- Web crawling and document ingestion
- Graph-based interfaces
- Campus knowledge search

#### Reusable Bullet Options

- Built a BGSU campus search prototype combining lightweight RAG, live web search, crawled webpages, PDFs, and LLM inference to generate source-grounded answers.
- Implemented document ingestion, chunking, vector retrieval, semantic search, and source-aware summarization across stored and crawled university resources.
- Developed graph-search functionality and an interactive graph interface using page/resource relationships to trace generated answers back to original sources.

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

### RocketGrader: Intelligent Assignment Feedback Platform

Primary positioning: full-stack AI education platform, secure LMS, file parsing, AI grading

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
