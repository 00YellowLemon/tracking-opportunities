# The Anatomy of an Agent Harness

**Source:** [https://blog.langchain.com/the-anatomy-of-an-agent-harness/](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)

*   **Agent = Model + Harness**: A harness is the system surrounding the model (system prompts, tools, storage, execution environments, orchestration).
*   **Filesystems as Durable Storage**: Filesystems allow agents to offload intermediate context, persist state across sessions, and work around context limits.
*   **Version Control**: Integrating Git with the filesystem provides agents with the ability to rollback errors and version track work.
*   **General Purpose Tooling**: Providing Bash execution scales problem-solving autonomously far better than hardcoding individual tools.
*   **Sandboxes**: Isolated execution environments allow agents to securely execute their own generated code and utilize tools like logs/browsers for self-verification.
*   **Combating Context Rot**: A full context window degrades performance. Harnesses must manage this via compaction, offloading heavy tool outputs to files, and dynamically loading skills.
*   **Ralph Loops**: A technique where intercepts prevent premature agent exiting and reinject prompts, forcing continuation on long-horizon tasks.
