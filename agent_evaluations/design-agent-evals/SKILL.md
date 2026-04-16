---
name: design-agent-evals
description: Helps users architect, categorize, and design agent evaluations for AI agent harnesses. Use this skill when asked to create an evaluation framework, define metrics for agent behavior, write new agent evals, track agent performance, or structure a testing strategy for autonomous agents. Do NOT use this skill for standard unit testing or generic software CI/CD pipelines.
---

# Design Agent Evaluations

## Critical Instructions

*   **Correctness Over Efficiency:** Always design evaluations to test correctness first. An agent must clear the correctness bar before optimizing for efficiency metrics (like latency, cost, and step ratio).
*   **Targeted Measurement:** Ensure each eval specifically measures an agent behavior the user actually cares about in production. Avoid creating evals just to artificially bump aggregate benchmark scores.
*   **Focus on Behavior:** Evals shape system behavior. When designing an eval, explicitly define the "vector" of behavior you are optimizing for (e.g., parallel tool usage, multi-hop retrieval, maintaining durable memory).

## Curation Strategy

When instructed to design or source agent evaluations, you should recommend the following methods:

1.  **Dogfooding & Tracing:** Convert real-world failures into evaluations. Every error observed in a trace should become a new eval to prevent regressions.
2.  **External Benchmarks:** Selectively adapt tasks from established datasets (e.g., Terminal Bench, BFCL).
3.  **Artisanal Evals:** Craft custom tests to observe highly specific, isolated behaviors (e.g., "does the agent use the grep tool correctly when searching a large file?").

## Evaluation Categories

Structure evaluation harnesses by categorizing tests based on *what* they test (the "middle view"), not *where* the data originated. Common categories to implement:

*   `file_operations`: Read, write, grep, pagination, parallel file access.
*   `retrieval`: Multi-hop synthesis, finding cross-file information.
*   `tool_use`: Tool selection, multi-step chaining, state tracking.
*   `memory`: Persisting durable information and recalling seeded context.
*   `conversation`: Asking clarifying questions, maintaining dialogue context.

## Defining Metrics

When designing the evaluation metrics, apply these principles:

1.  **Define the Ideal Trajectory:** Always map out a baseline sequence of steps that produces a correct outcome with *zero unnecessary actions*.
2.  **Calculate Ratios:** Measure observed behavior against the ideal trajectory:
    *   **Step ratio:** Observed agent steps / ideal agent steps.
    *   **Tool call ratio:** Observed tool calls / ideal tool calls.
    *   **Latency ratio:** Observed latency / ideal latency.
    *   **Solve rate:** Expected steps / observed latency.

## References

For deeper context on evaluation philosophy and metric design, refer to the documents in the `references/` directory:

*   `references/langchain-evals.md`: Core philosophy, metrics, and ideal trajectories for deep agents.
*   `references/anthropic-skills-guide.md`: Guidelines on skill formatting and best practices.
