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

## Agentic Engineering: System-Level Multi-Agent Collaboration

**Source:** [Agentic Engineering: How Swarms of AI Agents Are Redefining Software Engineering (LangChain Blog)](https://www.langchain.com/blog/agentic-engineering-redefining-software-engineering)

Agentic engineering is a multi-agent coordination model where AI agents act as digital team members. The goal is to move software through the full delivery pipeline faster and safer by mirroring real-world engineering teams, rather than just treating AI as a collection of isolated assistants to write code faster.

### Core Architectural Model: Leaders and Workers
This model utilizes a native control plane for multi-agent coordination, enabling cross-team workflow orchestration, shared memory, and traceability across the entire software lifecycle. The architecture is built around two complementary roles:

*   **Leader Agents (Project Leaders):**
    *   Act as a digital project leader providing coordination, governance, and visibility across a swarm of worker agents.
    *   Maintain a shared prompt and workflow library to standardize practices and lower onboarding friction.
    *   Provide a common tool gateway for secure access to capabilities.
    *   Manage long-term memory for continuous learning and global observability for system-wide auditing.
    *   Separate orchestration (when and how agents act) from execution.
*   **Worker Agents (Individual Contributors):**
    *   Function autonomously within defined boundaries, retrieving context from systems of record (code repos, trackers, logs).
    *   Interpret user intent, plan, and execute workflows using tools, coding agents, or subagents.
    *   Validate outcomes for correctness and report actions to the Leader Agent for accountability.
    *   Designed to be loosely coupled, enabling horizontal scaling and dynamic task delegation.

### Agentic Engineering vs. AI Coding Agents
While AI coding agents (like Codex or Claude) excel at translating intent into code within a single session, they operate at a fundamentally different abstraction level:

*   **Scope:** AI coding agents operate within a bounded, user-driven loop. Agentic engineering is an orchestration control plane that manages end-to-end delivery across developer and team boundaries.
*   **Relationship:** They are not competing. Codex-class coding models often run *inside* Worker Agents as reasoning and code-generation engines, while the agentic engineering framework handles state, memory, and cross-agent coordination.

### Pilot Study Insights (Systemic Impact)
*   **Debugging:** Coordinated execution across agents (e.g., cross-team triage) resulted in a 93% reduction in time-to-root-cause.
*   **Development:** Workflows saw a 65% execution time reduction. Crucially, the biggest gains came from compressing downstream tasks (like functional testing post-PR merge) through coordinated agents, not just from faster initial code generation.

## Async Subagents for Long-Running Tasks

**Source:** [Running Subagents in the Background (LangChain Blog)](https://www.langchain.com/blog/running-subagents-in-the-background)

When a supervisor delegates complex, time-consuming tasks to subagents, the traditional synchronous (inline) execution loop creates severe bottlenecks. Async subagents resolve this by decoupling the supervisor from the subagent's execution process.

*   **The Synchronous Bottleneck:** Inline subagents block the supervisor agent for the duration of the task. Because tool calls in an agent loop are synchronous, the supervisor cannot respond to user inputs, coordinate other tasks, or course-correct until the subagent finishes. This is a critical failure point for tasks that take hours.
*   **"Fire-and-Steer" Paradigm:** Async subagents operate in the background. The supervisor launches a task and immediately receives a task ID, freeing it to handle user interaction, dispatch parallel subagents, or cancel obsolete work. This shifts the delegation pattern from "fire-and-forget" to a dynamic "fire-and-steer" approach.
*   **Independent State and Process Separation:** True async subagents are not merely functions of the parent agent. They run as fully isolated agents with their own independent process, state, and memory thread.
*   **Standardized Remote Management:** To orchestrate independent background agents effectively, communication should occur over a framework-agnostic API specification (such as the Agent Protocol). This provides standard endpoints for creating threads, launching runs, polling status, sending updates, and managing long-term memory, ensuring the supervisor is decoupled from how or where the subagent is deployed.
