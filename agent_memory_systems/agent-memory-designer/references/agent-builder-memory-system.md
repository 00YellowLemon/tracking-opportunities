# How we built Agent Builder's memory system

*Source:* https://blog.langchain.com/how-we-built-agent-builders-memory-system/

## Core Concepts
*   **Procedural Memory:** The set of rules that can be applied to working memory to determine the agent's behavior (e.g., core instructions).
*   **Semantic Memory:** Facts about the world.
*   **Episodic Memory:** Sequences of the agent's past behavior (e.g., conversation logs).

## Implementation Approach: "Virtual Filesystem"
*   LLMs are excellent at working with filesystems natively.
*   Use standard files like `AGENTS.md` to define core instructions (procedural memory).
*   Use `tools.json` for customized MCP servers (to limit context overflow).
*   Use specific "agent skills" and arbitrary user-uploaded files for semantic memory.
*   The filesystem abstraction is backed by a database (like Postgres) for efficiency, but exposed to the agent as a filesystem.
*   Agents can update these files "in the hot path" (as they are working).

## Learning and Compacting Over Time
*   Instead of starting with a massive `AGENTS.md`, allow it to build iteratively. As users correct the agent, the agent updates its own files to remember preferences and handle edge cases.
*   **Challenge:** Agents are generally good at adding specific things to their memory but struggle to compact and generalize learnings. Background memory processes (e.g., a daily cron job) to reflect and summarize memory can help with this.

## Best Practices
*   **Validation:** Always validate file schemas (like `tools.json` or custom markdown frontmatter) and return validation errors to the LLM to prevent formatting corruption.
*   **Human in the loop:** Require explicit human approval for memory updates to mitigate prompt injection.
*   **Explicit Management:** Expose commands like `/remember` to prompt the agent explicitly to reflect on conversations and update its memory.