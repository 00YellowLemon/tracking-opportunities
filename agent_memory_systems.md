# Agent Memory Systems

**Source:** [How we built Agent Builder’s memory system](https://blog.langchain.com/how-we-built-agent-builders-memory-system/)

## Core Concepts of Agent Memory
*   **Procedural Memory:** Rules dictating agent behavior (e.g., core instructions).
*   **Semantic Memory:** Factual knowledge about the world or specific domains.
*   **Episodic Memory:** Sequences of the agent’s past actions and behaviors.

## File-Based Implementation
*   **Memory as a Filesystem:** Use a "virtual filesystem" (backed by a database like Postgres) to store memory, taking advantage of LLMs' proficiency with filesystems.
*   **Procedural Implementation:** Use standard files like `AGENTS.md` for core instructions and `tools.json` (customized MCP servers) for tool access.
*   **Semantic Implementation:** Use agent skill files and other knowledge documents that the agent can read and write "in the hot path".
*   **Iterative Memory Building:** Allow agents to update their own memory (e.g., `AGENTS.md`) based on natural language corrections, avoiding manual upfront documentation.

## Practical Learnings & Best Practices
*   **Prompting is Key:** The hardest challenge is prompting agents to correctly manage memory (knowing when to remember, format rules, file destinations).
*   **Validate File Schemas:** Always validate custom file shapes (like JSON or specific Markdown frontmatter) to catch agent formatting errors.
*   **Memory Compaction Issues:** Agents excel at adding specific details but struggle to abstract and compact learnings (e.g., generalizing a rule from specific instances).
*   **Explicit Management:** End users may still need to explicitly prompt the agent to reflect, summarize, or compact memory.
*   **Human-in-the-Loop:** Require explicit human approval for memory updates to mitigate risks like prompt injection.

## Future Focus Areas
*   **Background Processes:** Run background jobs (e.g., daily cron) to reflect on conversations and compact/generalize memories.
*   **Episodic Memory Addition:** Expose past conversation logs as files for the agent to reference.
*   **Semantic Search:** Enable semantic searching over memory files for specific retrieval needs.
*   **Levels of Memory:** Introduce scoped memory (e.g., user-level, org-level) via dedicated directories.
