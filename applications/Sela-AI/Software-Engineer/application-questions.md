# Sela AI - Application Questions

## What's something you've learned in the last 6 months that changed how you work?

The biggest shift for me recently has been how I think about working with AI tools. I used to think mostly about the model and the prompt. Now I think much more about the evidence I give the model and how I verify what comes back.

I saw this clearly while working on my diff-grounded pull request description project. The goal was to generate PR descriptions from real development context: commits, file diffs, linked issues, and repository metadata. At first, it is tempting to think the model itself is the main thing. But the more I worked on it, the more I realized the real engineering problem was deciding what context mattered, how to structure it, and how to check whether the output was actually supported by the code changes.

That changed how I work day to day. I still use tools like Codex and Claude Code because they make me faster, but I trust them differently now. I do not just accept a polished answer because it sounds right. I look for what it is grounded in, whether it matches the code or requirements, and where I still need to use my own judgment. It made me more disciplined, but also more confident using AI as a real engineering tool instead of just a shortcut.

## What's something you built that you're proud of that no one asked you to build?

My self-adaptive scheduling project for OpenMP workloads is probably the best example. No one asked me to take it as far as I did. It started as an idea I was genuinely curious about: instead of assuming one fixed scheduling strategy is always best, could a runtime system observe how a workload behaves and adapt its scheduling decisions while the program is running?

I kept pushing on it because the problem felt like the kind of engineering I enjoy most. It had real systems work, performance tradeoffs, messy benchmarking, and a lot of moments where the answer was not obvious. I built a C++/OpenMP runtime experiment that collected per-epoch telemetry and used a UCB-based controller to explore scheduling policy, chunk size, and thread count. Then I benchmarked it against serial and fixed-policy baselines across Mandelbrot, heat diffusion, and reduction workloads, and generated plots for runtime, speedup, efficiency, and scheduler behavior.

What makes me proud is not just that I built the system, but that I stayed with it through the confusing parts. Performance work can be frustrating because small changes can produce noisy results, and you have to be careful not to fool yourself. That project taught me to be more patient, more evidence-driven, and more willing to keep refining an idea until I understood what the system was actually doing. It also reinforced that I like building software where there is a real feedback loop between theory, implementation, measurement, and iteration.
