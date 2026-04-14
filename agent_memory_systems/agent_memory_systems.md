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

## Learning Over Time (Context Evolution)
**Source:** [How agents can use filesystems for context engineering (LangChain Blog)](https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/)
*   **Automated Skill Updates:** An agent's skills and instructions can be treated as context stored in the filesystem. When users provide explicit or implicit feedback, the agent can write that information to its files to "remember" it for future iterations.
*   **Personalization:** This approach is excellent for quickly learning and storing custom user preferences (e.g., names, preferred output formats) without requiring external manual prompt updates.

## Context Engineering Strategies
**Source:** [Context Engineering for Agents (LangChain Blog)](https://blog.langchain.com/context-engineering-for-agents/)

Context engineering is the art of filling the LLM's context window with the right information at each step, preventing issues like context poisoning (hallucinations entering context), distraction (context overwhelming training), and confusion.

*   **Write Context (Saving out-of-context):** Persisting information outside the active context window to aid the task.
    *   **Scratchpads:** Useful for within-session tasks. Agents take notes or save plans (e.g., via file writing tools or runtime state objects) to persist information without taking up context tokens.
    *   **Memories:** Useful across sessions. Agents synthesize and reflect on past interactions to create long-term memories (e.g., self-generated procedural or episodic memories).
*   **Select Context (Pulling into context):** Strategically retrieving only relevant information.
    *   **Scratchpads/State:** Exposing specific parts of an agent's runtime state or reading specific files as needed.
    *   **Memories:** Fetching specific few-shot examples, instructions, or facts (often using embeddings/knowledge graphs) rather than loading all stored knowledge.
    *   **Tools:** Using Retrieval Augmented Generation (RAG) on tool descriptions to fetch only the most relevant tools for a task, reducing model confusion.
    *   **Knowledge/RAG:** Using a mix of techniques (AST parsing, grep, semantic search, re-ranking) to reliably pull relevant code or documents into context.
*   **Compress Context (Reducing tokens):** Retaining only essential information for the task.
    *   **Summarization:** Using LLMs to distill information. This can be applied to the full trajectory of a long conversation, at agent-agent handoffs, or to condense the outputs of token-heavy tool calls.
    *   **Trimming:** Filtering or pruning context using hard-coded heuristics (e.g., dropping older messages) or trained pruners.
*   **Isolate Context (Splitting tasks/environments):** Distributing context to maintain focus and limit window size.
    *   **Multi-agent Architectures:** Splitting work into sub-agents with separate concerns. Each agent has its own specific context window, instructions, and tools tailored to a sub-task.
    *   **Sandboxes/Environments:** Running code in isolated environments (like sandboxes) where large outputs (like images or heavy JSON) are stored as variables in the sandbox state rather than passed back into the LLM context.
    *   **State Schemas:** Using structured runtime state objects to isolate context in specific fields, exposing only the necessary fields to the LLM at each turn.

## Future Focus Areas
*   **Background Processes:** Run background jobs (e.g., daily cron) to reflect on conversations and compact/generalize memories.
*   **Episodic Memory Addition:** Expose past conversation logs as files for the agent to reference.
*   **Semantic Search:** Enable semantic searching over memory files for specific retrieval needs.
*   **Levels of Memory:** Introduce scoped memory (e.g., user-level, org-level) via dedicated directories.
