# Agent Memory Implementation Instructions

**Source:** [LangChain Deep Agents Memory Docs](https://docs.langchain.com/oss/python/deepagents/memory)

These instructions outline the memory architecture for the Harness Designer Agent. The agent operates autonomously to conceptualize and output instructions for a coding agent to build AI agent harnesses.

## Memory Backend Architecture

The memory system relies on LangGraph's `deepagents` `CompositeBackend` to route virtual filesystem operations to different storage mechanisms based on required persistence.

*   **Ephemeral State (`StateBackend`)**
    *   Acts as the default route (e.g., the root `/` or `/workspace/`), serving as a short-term scratchpad.
    *   Used for drafting sprawling thoughts, intermediate planning, and temporary token-heavy outputs.
    *   Keeps the active context window clean by automatically evicting data once the active thread or session concludes.
*   **Durable Storage (`StoreBackend`)**
    *   Mapped exclusively to the `/memories/` directory and backed by a persistent Postgres database.
    *   Provides cross-thread, long-term storage for procedural instructions and agent behavioral rules as Markdown files.
    *   Implemented strictly with a user-scoped namespace (`user_id`) since this is a single-user application, ensuring complete isolation of persistent files.
    *   Allows the agent to dynamically load context using file tools (`ls`, `grep`, `read_file`) rather than stuffing the prompt context window.

## Memory Taxonomy

*   **Procedural Memory**
    *   Housed within `/memories/` (e.g., `AGENTS.md` and behavioral guidelines).
    *   Contains the evolving "how-to" manual that dictates the agent's behavior, formatting rules, and architectural standards for the harnesses it designs.
    *   The agent updates these procedural rules based on feedback to learn and optimize its instructional output over time.
*   **Episodic Memory**
    *   Captures sequences of past actions, conversational context, and historical failures.
    *   Managed entirely by the built-in LangGraph checkpointer instead of explicit file logs in the filesystem.
    *   Allows the agent to use thread search mechanisms to recall past debugging sessions, re-orient its strategy, and avoid repeating previous mistakes.
*   *(Note: Semantic Memory, which stores generic factual knowledge bases, is intentionally omitted from this architecture to focus strictly on process and action history.)*

## Architectural Strategies & Verification

*   **Upfront Planning as a Memory Anchor**
    *   Forces the agent to draft a concrete plan (or "sprint contract") in the ephemeral workspace before generating the final coding agent instructions.
    *   This upfront alignment acts as a persistent anchor for the task, preventing the compounding of minor errors over long work horizons.
*   **Multi-Agent Cross-Checking**
    *   Because models struggle to hold long context reliably, the architecture relies on evaluator agents to continually check the primary agent's output against the established plan.
    *   This acts as an external memory retrieval and correction loop, effectively combating context drift.
*   **Context Reset Cycles**
    *   Employs judge-evaluated work cycles. Once a stage is completed or evaluated, the agent starts fresh with a renewed context window.
    *   Clearing degraded short-term memory ensures the agent remains focused on the persistent plan and current constraints without being overwhelmed by past tokens.

## Human-in-the-Loop (HITL) Integration

*   **Memory Safeguards:** Modifying core procedural rules in `/memories/AGENTS.md` fundamentally alters agent behavior. Such write operations are explicitly gated behind an interrupt, requiring human approval to prevent corruption.
*   **Final Approval Checkpoint:** The final output instructions are paused for human review before hand-off to the coding agent. Any corrections provided by the user are absorbed and used to adjust procedural memory for future tasks.