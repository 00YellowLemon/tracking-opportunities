# Agent Harnesses: Design & Anatomy

**Source:** [The Anatomy of an Agent Harness (LangChain Blog)](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)

**Core Philosophy: Agent = Model + Harness**
*   If it's not the model, it's the harness. The model provides raw intelligence; the harness provides the system that makes it useful.
*   A harness includes: System Prompts, Tools/Skills/MCPs, Infrastructure (filesystem, sandbox), Orchestration (subagents, routing), and Hooks/Middleware (compaction, linting).
*   **Why a Harness?** Out of the box, models cannot maintain durable state, execute code, access real-time knowledge, or set up environments. A harness bridges this gap.

## Core Harness Components & Primitives

### 1. Filesystems (Durable Storage & Context)
*   **The foundational primitive.** Provides a workspace for reading data, code, and docs.
*   Allows agents to offload intermediate outputs and maintain state across sessions, avoiding context limits.
*   Acts as a natural collaboration surface for multi-agent or human-agent teams.
*   *Taste insight:* Version control (Git) integrated with the filesystem allows agents to track work, rollback errors, and branch experiments.

### 2. Bash + Code (General Purpose Tooling)
*   Instead of pre-designing every single tool, give the model a general-purpose execution tool (like Bash).
*   Allows the model to design and write its own tools on the fly.
*   *Taste insight:* Code execution is the default strategy for autonomous problem solving, far scaling better than fixed toolsets.

### 3. Sandboxes & Verification Tools
*   Agents need safe, isolated environments to act and observe.
*   Sandboxes unlock scale (on-demand spin-up/tear-down) and security.
*   Harnesses must provide good default tooling: pre-installed runtimes, CLIs, and browsers.
*   *Taste insight:* Tools like logs, screenshots, and test runners create **self-verification loops**, enabling agents to ground solutions in reality rather than just outputting text.

### 4. Memory & Search (Continual Learning)
*   Memory relies on the filesystem (e.g., reading/writing an `AGENTS.md` file) to inject durable knowledge across sessions.
*   Search and MCP (Model Context Protocol) tools allow agents to retrieve information beyond their training data cutoff.

## Combating Context Rot
As context fills, agent reasoning degrades. A robust harness actively manages context:
*   **Compaction:** Intelligently offloading and summarizing the existing context window so work can continue seamlessly.
*   **Tool Call Offloading:** Keeping only the head/tail tokens of massive tool outputs in context, and writing the full output to the filesystem.
*   **Skills (Progressive Disclosure):** Loading tools/MCP servers dynamically as needed, rather than cluttering context on startup.

## Long Horizon Execution Patterns
To make agents work autonomously over long periods:
*   **Ralph Loops:** A harness hook that intercepts a model's attempt to exit, reinjecting the prompt into a clean context window to force continuation against a goal.
*   **Planning & Self-Verification:** Harnesses enforce plan files and run pre-defined test suites, looping errors back to the model for correction.

## Key Takeaways for Harness Design (Building "Taste")
*   **Optimize for the Task:** Just because a model was post-trained on a specific harness doesn't mean that harness is best for your task. Swapping or tuning the harness can yield massive performance gains (e.g., jumping from Top 30 to Top 5 on benchmarks).
*   **Harnesses patch deficiencies AND amplify intelligence:** Even as models natively improve at planning or self-verification, a well-configured environment with durable state and tight verification loops will always make the underlying model more efficient.