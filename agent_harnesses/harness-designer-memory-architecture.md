# Harness Designer Agent: Memory Architecture & Implementation

This document outlines the memory architecture and design for the autonomous agent responsible for generating instructions to build AI agent harnesses. This agent acts as a "Planner," creating the specifications and instructions that a coding agent (like Codex) will execute.

## 1. Memory Storage Architecture (Composite Backend)

The agent will utilize the **Composite Backend** from `deepagents` to manage both ephemeral scratchpad space and durable, cross-session memory stored in a cloud Postgres instance. This prevents context rot while allowing the agent to continuously learn.

### Architecture Implementation
The `CompositeBackend` routes filesystem operations to different backends based on the path.

*   **Default Route (`/workspace/` or `/`)**: Maps to `StateBackend`. This is an ephemeral scratchpad stored in LangGraph state for the current thread.
*   **Persistent Route (`/memories/`)**: Maps to `StoreBackend` backed by Postgres. This is the long-term, durable storage that persists across sessions and threads.

**Conceptual Implementation:**
```python
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
# Assuming a Postgres BaseStore implementation is provided
from custom_postgres_store import PostgresStore

agent = create_deep_agent(
    model="your-chosen-model",
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(
                namespace=lambda rt: (rt.server_info.user.identity,)
            ),
        }
    ),
    store=PostgresStore()
)
```

## 2. Managing Long-Term Memory (`/memories/`)

The agent will rely heavily on the virtual filesystem (mapped to Postgres) to store knowledge as Markdown files. This avoids stuffing the context window and allows the agent to dynamically load rules via `read_file` or search via `grep`/`glob`.

### What will be stored in `/memories/`?

1.  **`/memories/AGENTS.md` (Procedural Memory)**
    *   **Purpose:** The core instruction manual that evolves over time.
    *   **Content:** Contains rules on how to format instructions for the coding agent, what "AI slop" to avoid, mandatory verification steps (e.g., "always require a Playwright test for frontend components"), and architectural best practices for harnesses.

2.  **`/memories/harness_blueprints.md` (Semantic Memory)**
    *   **Purpose:** A library of successful, reusable harness architectures.
    *   **Content:** High-level specifications of past successful builds (e.g., "The 3-Agent Evaluator Pattern", "S3 Virtual Filesystem Harness"). When asked to design a new harness, the agent can `grep` this file for starting templates.

3.  **`/memories/evaluator_feedback.md` (Episodic/Correction Memory)**
    *   **Purpose:** Tracking past mistakes to improve future instructions.
    *   **Content:** If the coding agent fails to implement a harness or the evaluator agent rejects the build, the failure reason is appended here (e.g., "Coding agent failed because tool descriptions lacked type hints. *Correction:* Explicitly instruct the coding agent to add Pydantic models for all tool inputs.").

## 3. Ephemeral Memory (`StateBackend`)

The default `StateBackend` acts as the agent's short-term memory (scratchpad) during an active design session.

*   **`/workspace/draft_specs.md`**: The agent uses this to write out the sprawling, detailed requirements before compacting them into the final instructions.
*   **`/workspace/sprint_contract.md`**: A temporary file where the Planner agent defines the exact deliverables (the "sprint contract") that the coding agent and evaluator agent will agree upon before coding begins.

## 4. Inputs Needed

To kick off the design process, the agent requires the following inputs (provided via user prompt or structured context):

1.  **The Objective:** What is the end goal of the harness being built? (e.g., "An agent that writes React components", "An agent that manages a Google Calendar").
2.  **Environmental Constraints:** Where will this harness run? (e.g., "Local CLI", "Cloud server with no shell access").
3.  **Required Capabilities:** Does the harness need durable memory, sandboxed code execution, or specialized MCP tools?
4.  **Performance Needs:** Are there concerns about context window limits or long-running execution times that necessitate compaction hooks or "Ralph Loops"?

## 5. Human-in-the-Loop (HITL)

Because designing an agent harness dictates the behavior, security, and architecture of the resulting system, Human-in-the-Loop is critical before handing off to the coding agent.

1.  **Sprint Contract Approval:** Before the final instructions are sent to the coding agent, the Planner agent writes the `/workspace/sprint_contract.md` and pauses. The human reviews this contract to ensure the scope and architectural choices (e.g., using `StoreBackend` vs `FilesystemBackend`) are correct.
2.  **Security Review:** The human must approve any instructions that dictate the coding agent should give the new harness unrestricted access (like `LocalShellBackend` or un-sandboxed `FilesystemBackend` with `virtual_mode=False`).
3.  **Procedural Updates:** Periodically, the human reviews `/memories/AGENTS.md` and `/memories/evaluator_feedback.md` to prune outdated rules or manually inject new design philosophies (taste insights).