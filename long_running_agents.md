# Long-Running Agents: Design & Process

**Source:** [Expanding our long-running agents research preview (Cursor Blog)](https://cursor.com/blog/long-running-agents)

Long-running agents are designed to handle ambitious, long-horizon tasks (running for hours or days) autonomously, producing substantial and production-ready pull requests.

## Core Process & Design Principles

*   **Custom Harnesses over Raw Intelligence:** Frontier models fail predictably on long tasks. A custom harness that provides the right scaffolding is required to leverage the model's strengths and see difficult work through to completion.
*   **Plan Before Execution:** Agents must propose a plan and secure (human) approval *before* starting. Upfront alignment is crucial because a minor incorrect assumption early on compounds into a completely wrong solution by the end.
*   **Multi-Agent Verification for Follow-Through:** Models often lose track of the big picture or stop at partial completion. The process must use multiple different agents checking each other's work against the established plan to maintain focus and ensure completion.
*   **Thoroughness by Default:** Unlike synchronous agents that might provide a quick local fix, long-running agents should be designed to go further: finding edge cases, fixing similar occurrences across the codebase, and creating high-coverage tests.

## Do's and Don'ts of Designing Long-Running Agents

### Do's
*   **Do require upfront planning:** Force the agent to align on a strategy before it writes any code.
*   **Do implement cross-agent checking:** Use separate agents to evaluate and verify work to prevent the main agent from drifting or giving up.
*   **Do build custom scaffolding:** Tailor the harness to the specific frontier model to patch its unique deficiencies in memory and follow-through.
*   **Do design for production-readiness:** Set the expectation for the agent to output comprehensive PRs (including tests, edge case handling, and related fixes), not just snippets.

### Don'ts
*   **Don't use tight prompt-response loops for large tasks:** Jumping straight into execution without an approved plan leads to compounding errors on long-horizon work.
*   **Don't rely on a single agent to remember the big picture:** A lone agent is likely to lose context or stop prematurely over a 24+ hour runtime.
*   **Don't expect raw models to finish large tasks alone:** They need external mechanisms (plans, evaluators) to prevent them from stopping at partial completion.
