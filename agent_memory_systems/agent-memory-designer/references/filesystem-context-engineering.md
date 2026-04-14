# How agents can use filesystems for context engineering

*Source:* https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/

## Why Filesystems Help Context Engineering
Context engineering is the art of filling the context window with the right information. Filesystems solve several context problems:

1.  **Too many tokens (Retrieved Context >> Necessary Context):**
    *   Instead of dumping massive tool results (like search or API responses) into the conversation history, write them to the filesystem.
    *   The agent can use tools like `grep` or `read_file` to selectively read only the necessary pieces into its active context, avoiding token limit bloat.

2.  **Needs large amounts of context (Necessary Context > Supported Context Window):**
    *   Filesystems serve as an external storage location for multi-step tasks.
    *   Agents can write long-horizon plans to files and fetch them when needed.
    *   Subagents can write their findings to files rather than communicating entirely through the main agent's context window.

3.  **Finding Niche Information:**
    *   Models are specifically trained to traverse filesystems.
    *   Directories naturally structure information.
    *   Tools like `ls`, `glob`, and `grep` complement semantic search to isolate specific files, lines, and characters efficiently, particularly for code or API docs where semantic search often fails.

4.  **Learning over time:**
    *   Agents can update their own instruction files or skills directly based on explicit or implicit user feedback.
    *   This provides an automated way to continuously improve the agent without manual system prompt updates.