# Long-Running Agents: Core Architecture

**Source:** [Expanding our long-running agents research preview (Cursor Blog)](https://cursor.com/blog/long-running-agents)

*   **Custom Harnesses:** Frontier models fail predictably on long tasks. A custom harness that provides the right scaffolding is required to patch unique deficiencies in memory and follow-through.
*   **Upfront Planning Requirement:** Agents must propose a strategy and secure human approval before execution. A minor incorrect assumption early on compounds into a completely wrong solution by the end of a long-horizon task.
*   **Multi-Agent Verification:** Relying on a single agent to remember the big picture over 24+ hours is a failure pattern. Separate agents must evaluate and verify work against the established plan to maintain focus and ensure the task is completed rather than partially implemented.
*   **Production-Readiness Scope:** Long-running agents should be designed for thoroughness—finding edge cases, fixing similar occurrences across the codebase, and creating high-coverage tests, unlike synchronous agents focused on local snippets.
