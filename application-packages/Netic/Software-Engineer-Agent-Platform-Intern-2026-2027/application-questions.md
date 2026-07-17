# Netic Software Engineer Agent Platform Intern Application Questions

## Recent reading

Question: What is the most interesting paper, blog post, or documentation you have read in the past month?

Answer:

I recently spent time with a survey paper on LLM-as-a-Judge methods. It stuck with me because I have been thinking more about how hard it is to evaluate AI systems once the output is not just a simple right or wrong answer.

The useful part for me was the reminder that an LLM judge is still a system with failure modes. It can be sensitive to wording, ordering, rubric design, and hidden bias. That matters for agentic products because an eval loop can look scientific while quietly rewarding the wrong behavior. If an agent is testing another agent, the evaluation harness has to be treated like production infrastructure, not just a prompt.

That connects pretty directly to why Netic's Agent Platform role interests me. The job description talks about eval loops, harnesses, guardrails, rollback paths, and human-in-the-loop checkpoints. Those are the parts of AI engineering I want to get better at, because they decide whether an agentic system can be trusted outside a demo.
