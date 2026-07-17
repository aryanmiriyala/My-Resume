# Builder Note

Aryan Miriyala

## One thing I built

[Fix-It-Flow](https://github.com/aryanmiriyala/rockethacks-2026) is a voice-first repair assistant I built for RocketHacks 2026. A user can show an appliance through a camera, describe the problem aloud, and receive repair guidance before defaulting to replacement. The product combines Gemini Vision, Llama-style reasoning through Featherless.AI, ElevenLabs speech, and DynamoDB-backed session state in a Next.js application.

## What I owned

I owned the application flow that turned several AI services into one usable product. That included typed Next.js API routes, inspection turns, conversation and frame context, structured findings, safety warnings, repair-step generation, spoken instructions, and persisted sessions. The difficult part was not making one model call. It was keeping enough state for the next call to make sense, constraining outputs into shapes the interface could use, and giving a person a clear path when the system was uncertain.

## A recent technical rabbit hole

I recently went deep on whether an OpenMP program could adjust its own runtime strategy instead of using one fixed schedule. I built a C++ runtime that recorded per-epoch telemetry and used a UCB controller to explore scheduling policy, chunk size, and thread count across Mandelbrot, heat-diffusion, and reduction workloads. I compared it with serial and fixed-policy baselines and generated plots for runtime, speedup, efficiency, and scheduler decisions.

The interesting lesson was that finding a fast configuration is not the same as proving an adaptive policy is better. Exploration has a cost, workload phases can mislead the controller, and a promising result can disappear when the run budget changes. That pushed me to look at convergence behavior and repeated trials instead of selecting the nicest speedup number.

## How I would sanity-check an AI result

I would use several independent layers.

1. Define the claim and invariants before evaluating it. For an experiment recommendation, I would record the inputs, expected output schema, traffic assumptions, and conditions that would make the result invalid.
2. Replay the result and run deterministic checks. I would test state isolation, reproducibility, missing data, impossible values, and sensitivity to small changes in the prompt or inputs.
3. Compare factual claims with approved primary sources. For web-grounded checks, I would retrieve sources such as official platform documentation, manufacturer material, or government guidance, preserve the URLs and snapshots, and require citations that a reviewer can reopen.
4. Use an independent judge ensemble. Separate models or prompts would review product logic, statistical reasoning, and safety. I would calibrate them on known good and bad examples, hide the generating model's identity, and treat disagreement as a signal for review. This is a practical mixture-of-experts check, not a vote that turns uncertainty into truth.
5. Keep a human decision boundary. High-impact, low-confidence, novel, or conflicting results would not ship automatically. I would surface the evidence, judge rationales, counterexamples, and uncertainty so a person can make the final call.
