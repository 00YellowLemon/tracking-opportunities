# Harness Designer Agent: Memory Architecture & Context Engineering

## 1. Architecture Overview
The Harness Designer agent operates as an autonomous architect that conceptualizes and designs AI agent harnesses. Its final outputs are structured instructions fed to a coding agent (like Codex) to implement the harness (architecture, code, tools, prompts, models).

To support complex reasoning and learning over time, the agent uses the `deepagents` `CompositeBackend` to route filesystem operations:
- **Default (`/`) -> `StateBackend`:** Acts as an ephemeral scratchpad. Used for intermediate planning, drafting out thoughts, and storing temporary token-heavy outputs. Clears out after the conversation thread concludes.
- **`/memories/` -> `StoreBackend`:** Backed by Cloud Postgres via LangGraph's `BaseStore`. This provides durable, cross-thread storage for the agent's procedural instructions, semantic knowledge bases, and episodic logs, all managed as `.md` files.

## 2. Memory Taxonomy inside `/memories/`
The agent uses its file tools (`ls`, `read_file`, `write_file`, `edit_file`) to manage the following memory structures inside the persistent `/memories/` route.

### A. Procedural Memory (Agent Behavior & Rules)
Files that dictate *how* the Harness Designer agent does its job.
- **`/memories/AGENTS.md`**: The core set of rules for the agent. If the user tells the agent "Always prefer LangGraph over AutoGen for harnesses," the agent will edit this file to persist that instruction permanently.
- **`/memories/design_standards.md`**: Best practices the agent must follow when outputting instructions for the coding agent (e.g., standard folder structures, required boilerplate).

### B. Semantic Memory (Factual Knowledge & Outputs)
Files containing knowledge the agent gathers and the actual harness designs it produces.
- **`/memories/harnesses/<harness_name>/architecture.md`**: The semantic output. Contains the high-level architecture designed by the agent.
- **`/memories/harnesses/<harness_name>/prompts.md`**: The system prompts designed for the target harness.
- **`/memories/harnesses/<harness_name>/tools_spec.md`**: The specifications for the tools the coding agent needs to build.
- **`/memories/harnesses/<harness_name>/codex_instructions.md`**: The final, synthesized output document containing explicit instructions ready to be passed to the coding agent.
- **`/memories/patterns/<pattern_name>.md`**: Reusable architectural patterns the agent learns over time (e.g., `multi-agent-supervisor-pattern.md`, `rag-routing-pattern.md`).

### C. Episodic Memory (Past Actions)
Files that track history to inform future context.
- **`/memories/changelog.md`**: A summary of all harnesses designed and updates made over time.
- **`/memories/feedback_log.md`**: Historical feedback from the Human-in-the-Loop on past designs.

## 3. Context Management Strategies

- **Write Context:**
  - **Scratchpads:** The agent writes intermediate drafts to the root directory (e.g., `/draft_architecture.md`) using the `StateBackend`. This prevents bloating the active context window with messy, unfinished thoughts.
  - **Memories:** Once a draft is finalized, the agent writes it to `/memories/harnesses/<name>/` via the `StoreBackend`.
- **Select Context:**
  - Rather than loading all past harnesses into context, the agent uses `ls` and `grep` inside `/memories/patterns/` or `/memories/harnesses/` to pull specific examples or templates relevant to the current user request.
- **Compress Context:**
  - Instead of reading full, lengthy conversation logs, the agent maintains a summarized `/memories/feedback_log.md` to extract core learnings from user feedback.
- **Isolate Context:**
  - The generation of code (by the coding agent) is isolated from the design phase. The Harness Designer agent only deals with architectural markdown, preventing its context from being overwhelmed by raw code blocks.

## 4. Learning Loop & Inputs

**Inputs to the Agent:**
1. **User Prompt:** High-level description of the desired agent harness (e.g., "I need an agent that scans SEC filings and generates summaries. Make it fast.").
2. **Current State:** The current procedural memory (`/memories/AGENTS.md`) and design standards loaded automatically.

**The Learning Mechanism:**
The agent is capable of self-updating. If a user says, "Actually, for SEC filings, we should use a RAG tool instead of just passing the whole text," the agent will:
1. Update `/memories/harnesses/sec_agent/tools_spec.md` to include a RAG tool.
2. Formulate a new generalized rule in `/memories/patterns/rag-routing-pattern.md` so it remembers this approach for future document-heavy harnesses.

## 5. Validation & Safety (Human-in-the-Loop)

Because modifying procedural memory (`AGENTS.md`) alters the fundamental behavior of the agent, and generating `codex_instructions.md` triggers downstream coding execution, explicit Human-in-the-Loop (HITL) checkpoints are required.

**HITL Checkpoints:**
1. **Memory Update Approval:** Before the agent commits an edit to `/memories/AGENTS.md` or `/memories/design_standards.md` (via `edit_file`), the HITL middleware pauses execution. The user must review the proposed behavioral rule change.
2. **Final Design Approval:** Before the `/memories/harnesses/<name>/codex_instructions.md` file is marked "ready" or handed off to the coding agent, the human reviews the architecture. Feedback provided here is captured by the agent and appended to the `/memories/feedback_log.md` to inform future designs.

**File Validation:**
The agent should be equipped with validation middleware to ensure any structured memory files it outputs adhere to required schemas (e.g., ensuring `codex_instructions.md` always has `# Architecture`, `# Prompts`, and `# Tools` headers).
