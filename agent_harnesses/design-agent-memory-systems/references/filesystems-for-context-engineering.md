# How Agents Can Use Filesystems for Context Engineering

**Source:** [https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/](https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/)

*   **Filesystem over Message History**: Instead of accumulating heavy context (e.g. web search results) in conversation history, agents can write outputs to the filesystem and `grep` only what is necessary, drastically cutting token cost and retaining signal.
*   **Dynamic Information Retrieval**: Agents can load massive instruction sets (skills) dynamically from disk instead of crowding the initial system prompt.
*   **Search Strategies**: LLMs are natively trained on filesystem structures. Using tools like `ls`, `glob`, and `grep` can sometimes outperform semantic search when traversing logically nested directories (like codebases).
*   **Learning Over Time**: When receiving corrections from users, agents can automatically append these insights to procedural memory files (e.g., modifying `AGENTS.md`) rather than human operators having to manually rewrite prompts.
