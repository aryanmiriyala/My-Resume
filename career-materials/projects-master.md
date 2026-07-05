# Projects Master

This document stores detailed project material for tailoring resumes, cover letters, and interview answers.

## Standard Project Structure

- `Platform-Ready Description`: copyable project paragraph for LinkedIn, cover letters, portfolios, or an expanded projects section.
- `Features`: product behavior, user-facing capability, or research functionality.
- `Tech Stack`: one comma-separated line with a domain prefix, such as `AI / Tech stack: Python, OpenAI API, LLM inference.`
- `Positioning Angles`: ways to frame the project for different job families.
- `Reusable Bullet Options`: ATS-friendly bullets for resumes and tailored applications.

## Travel Health Advisor

Date: Apr. 2025  
Primary positioning: Full-stack AI application, RAG, personalized health recommendations

### Platform-Ready Description

Travel Health Advisor is a full-stack health application that provides personalized travel health advisories based on a user's health profile and destination. The project combines a React frontend, Node.js/Express backend, MongoDB persistence, and an AI-powered retrieval/generation pipeline.

### Features

- Personalized destination-specific health advisories.
- Health-risk and precaution recommendations based on user profile and travel destination.
- RAG-powered retrieval from a large health database.
- Conversational chatbot for follow-up questions.
- Downloadable dynamic travel checklist.

### Tech Stack

Full-stack AI / Tech stack: React, Node.js, Express.js, MongoDB, Mistral AI, HuggingFace models, TailwindCSS, cosine similarity search, RAG.

### Positioning Angles

- AI product engineering
- Full-stack web application
- RAG pipeline design
- Health-domain personalization
- Conversational AI
- MongoDB-backed retrieval

### Reusable Bullet Options

- Developed a full-stack travel health platform with React, TailwindCSS, and Express.js to generate personalized destination-specific advisories from user health profiles.
- Engineered a RAG pipeline with Mistral AI and HuggingFace models to vectorize and query MongoDB health data using cosine similarity search.
- Built a conversational AI assistant that used retrieved health context to generate personalized travel guidance and downloadable checklists.

## Travel Health Advisory Map - BGSU Hackathon 2025

Date: 2025  
Primary positioning: Hackathon health AI application, React/Vite frontend, interactive data visualization, Mistral AI chatbot  
Source: https://github.com/aryanmiriyala/BGSU-Hackathon-2025

### Platform-Ready Description

Built a BGSU Hackathon 2025 AI/ML + Health track project with team VibeCoders: an interactive travel health advisory map using React, Vite, and react-simple-maps. The application lets users click countries on a world map, highlights the selected location, displays the selected country name, and includes a floating Mistral AI chatbot for travel-health questions. The project also includes React Router login/signup pages, environment-based API key handling through Vite, and JavaScript/CSS/HTML frontend implementation.

### Features

- Interactive world map for country selection.
- Country highlighting and selected-country display.
- Floating Mistral AI chatbot for health-related travel questions.
- Login and signup navigation through React Router.
- Vite environment-variable handling for API configuration.

### Tech Stack

Health AI frontend / Tech stack: React 18, Vite, JavaScript, CSS, HTML, react-simple-maps, D3, TopoJSON, Axios, React Router, Mistral AI API, Node.js, npm.

### Positioning Angles

- Healthcare-adjacent software project
- Graduate software engineer project
- JavaScript/React feature development
- AI chatbot integration
- Interactive data visualization
- Hackathon teamwork

### Reusable Bullet Options

- Built a BGSU Hackathon 2025 health AI application with React, Vite, and react-simple-maps, enabling users to explore an interactive world map and select countries for travel-health context.
- Integrated a floating Mistral AI chatbot with Axios and Vite environment configuration to answer health-related travel questions from the frontend.
- Implemented React Router login/signup flows and JavaScript/CSS UI components for a hackathon project in the AI/ML and Health tracks.

## RocketGrades

Date: Mar. 2025  
Primary positioning: Full-stack LMS, AI feedback, secure backend, file storage

### Platform-Ready Description

RocketGrades is a full-stack learning management system application with an AI feedback agent. It combines Angular frontend work, Node.js backend services, Auth0 role-based access control, MongoDB Atlas persistence, AWS S3 file storage, and Mistral AI/LangChain for assignment feedback.

### Features

- LMS-style assignment workflows.
- AI-powered assignment feedback.
- Role-based access control through Auth0.
- Persistent application data in MongoDB Atlas.
- File storage in AWS S3.

### Tech Stack

Full-stack LMS / AI / Tech stack: Angular, Node.js, Mistral AI, LangChain, MongoDB, MongoDB Atlas, AWS S3, Auth0, TailwindCSS.

### Positioning Angles

- Full-stack software engineering
- AI-assisted education technology
- Secure application backend
- Role-based access control
- Cloud file storage

### Reusable Bullet Options

- Built a full-stack LMS application with an AI feedback agent using Mistral AI and LangChain to automate assignment review.
- Designed a secure Node.js backend with Auth0 RBAC, MongoDB Atlas, and AWS S3 for role-based access, persistence, and file storage.

## Additional Project Slots

Use this section to add future projects. Capture:

- Problem solved
- Users or audience
- Architecture
- Tech stack
- Features
- Deployment
- Measurable impact, if known
- Reusable bullet options
- Cover-letter talking points

## LinkedIn Highlighted Projects

These projects were provided from Aryan's LinkedIn project highlights and should be treated as additional source material for targeted resumes, cover letters, and interview prep.

### Diff-Grounded Pull Request Description Generation with Structured Evidence using Large Language Models

Primary positioning: LLM research, software repository mining, evidence-grounded generation, automated evaluation

#### Platform-Ready Description

Developed an ICSME-published LLM research project for generating evidence-grounded GitHub pull request descriptions from real repository artifacts. The pipeline collects commits, file diffs, linked issues, and repository metadata; builds structured PR context; improves weak commit messages; summarizes file-level changes; and generates reviewer-ready descriptions under grounding constraints. Also built an automated LLM evaluation workflow to compare generated descriptions against raw code-change evidence. The approach outperformed baseline descriptions from the AIDev and PRSummarizer datasets in correctness, coverage, and clarity.

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
