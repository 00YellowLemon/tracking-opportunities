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

## Scaling Long-Running Agents

**Source:** [Scaling long-running autonomous coding (Cursor Blog)](https://cursor.com/blog/scaling-agents)

When scaling to hundreds of concurrent agents for massive projects, dynamic coordination often fails. Examples of these massive projects include building a web browser from scratch (1M+ lines of code) or executing large-scale framework migrations (e.g., Solid to React).

Key architectural lessons for scaling agents include:

*   **Avoid Flat Hierarchies and Locks:** Giving all agents equal status and using file-locking or optimistic concurrency for self-coordination creates severe bottlenecks. Agents become risk-averse, preferring small changes over solving hard problems.
*   **Separate Roles (Planners vs. Workers):**
    *   **Planners:** Continuously explore the codebase, break down work, and create tasks. Planning can be recursive (planners spawning sub-planners for specific areas).
    *   **Workers:** Focus entirely on completing assigned tasks. They do not coordinate with other workers or worry about the big picture.
*   **Implement Cycles and Fresh Starts:** At the end of a work cycle, a judge agent should determine whether to continue. Starting the next iteration fresh helps combat drift and tunnel vision.
*   **Match Models to Roles:** Different foundation models excel at different tasks. For instance, some models are better at high-level planning and maintaining focus over extended periods, while others may be better suited for raw, localized coding.
*   **Keep the System Simple:** Avoid over-engineering organizational designs. For example, adding dedicated "integrator" agents for conflict resolution can create bottlenecks, as worker agents are often capable of resolving version control conflicts themselves. Prompts matter more than complex harnesses.
