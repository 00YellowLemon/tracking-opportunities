# Context Engineering Strategies

*Source:* https://blog.langchain.com/context-engineering-for-agents/

Context engineering addresses the delicate art of filling the context window with just the right information.

## Four Main Strategies

1.  **Write Context (Saving out of context)**
    *   **Scratchpads:** Useful within sessions. An agent writes notes, tool output, or plans to an external file or state object to prevent context bloat.
    *   **Memories:** Useful across sessions. The agent synthesizes interactions into long-term memories.

2.  **Select Context (Pulling into context)**
    *   **Scratchpads/State:** Exposing only specific state fields or file contents dynamically to the LLM at each step.
    *   **Memories:** Using embeddings, knowledge graphs, or file selection to pull in relevant facts, few-shot examples, or procedural instructions.
    *   **Tools:** Using RAG on tool descriptions to select only relevant tools to pass to the agent.
    *   **Knowledge/RAG:** Mixing AST parsing, grep, and semantic search to reliably pull relevant code or documents.

3.  **Compress Context (Reducing tokens)**
    *   **Summarization:** Post-processing tool outputs, or summarizing large conversation histories, with an LLM before placing it into context.
    *   **Trimming:** Hard-coded pruning of context (e.g., dropping older messages).

4.  **Isolate Context (Splitting tasks/environments)**
    *   **Multi-agent:** Distributing tasks to subagents, each with their own isolated context windows, instructions, and tools.
    *   **Environments/Sandboxes:** Running tools in sandboxes where token-heavy outputs (images, audio, large JSON) are assigned to variables within the sandbox rather than returned to the LLM.
    *   **State:** Isolating specific data fields in a structured runtime state and only passing required fields to the LLM at each turn.