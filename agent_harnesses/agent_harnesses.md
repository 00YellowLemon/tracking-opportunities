# Agent Harnesses: Design & Anatomy

**Source:** [The Anatomy of an Agent Harness (LangChain Blog)](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)

**Core Philosophy: Agent = Model + Harness**
*   If it's not the model, it's the harness. The model provides raw intelligence; the harness provides the system that makes it useful.
*   A harness includes: System Prompts, Tools/Skills/MCPs, Infrastructure (filesystem, sandbox), Orchestration (subagents, routing), and Hooks/Middleware (compaction, linting).
*   **Why a Harness?** Out of the box, models cannot maintain durable state, execute code, access real-time knowledge, or set up environments. A harness bridges this gap.

## Core Harness Components & Primitives

### 1. Filesystems (Durable Storage & Context)
**Source:** [How agents can use filesystems for context engineering (LangChain Blog)](https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/)

*   **The foundational primitive.** Provides a workspace for reading data, code, and docs.
*   Allows agents to offload intermediate outputs and maintain state across sessions, avoiding context limits.
*   Acts as a natural collaboration surface for multi-agent or human-agent teams.
*   **Context Engineering & Scratch Pads:** Use the filesystem to write large tool results (e.g., raw web search content), keeping conversation history light and avoiding token limits. Agents can then intelligently search (`grep`) for needed keywords and read only the necessary context.
*   **Dynamic Information Retrieval:** For tasks requiring vast amounts of context, agents can write plans, store subagent outputs, or dynamically load specific skill instructions from the filesystem rather than loading them all in the system prompt.
*   **Niche Retrieval:** Instead of relying entirely on semantic search, agents can use filesystem traversal tools (`ls`, `glob`, `grep`) to precisely locate information in deeply nested structures (e.g., code files), taking advantage of pre-existing logical directory organizations.
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
*   *Further Reading:* See [Agent Memory Systems](agent_memory_systems.md) for more details on implementation and best practices.

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

## Developing Taste and Evaluating Subjective Quality

**Source:** [Harness design for long-running application development (Anthropic)](https://www.anthropic.com/engineering/harness-design-long-running-apps)

To build "taste" into agents and handle subjective tasks (like frontend design) or long-running software engineering, harness design must address self-evaluation limits and context management.

*   **Separate Generator and Evaluator Agents:** Models are notoriously lenient when grading their own work. Building a standalone, highly-skeptical "Evaluator" agent forces the "Generator" agent to improve iteratively against concrete feedback.
*   **Make Subjective Quality Gradable:** Define concrete criteria (e.g., *Design Quality*, *Originality*, *Craft*, *Functionality*). Penalize generic patterns ("AI slop") heavily to encourage aesthetic risk-taking.
*   **Three-Agent Architecture for Complex Builds:**
    *   **Planner:** Turns simple prompts into high-level, ambitious product specs.
    *   **Generator:** Builds the app in chunks, agreeing on a "sprint contract" (what "done" looks like) before coding.
    *   **Evaluator:** Navigates the live app (e.g., via Playwright) to test features and ensure visual/functional quality against the contract.
*   **Structured Handoffs vs. Compaction:** For massive tasks, passing structured state (files/artifacts) into a fresh context window ("context resets") is sometimes necessary.

### The "Don'ts" of Agent Harnesses
*   **Don't rely on self-evaluation for subjective tasks:** Agents will confidently praise their own mediocre work. Use a separate evaluator.
*   **Don't over-specify technical implementation upfront:** The planner should focus on product features and deliverables, not granular technical specs, to prevent early mistakes from cascading through the build.
*   **Don't use simple compaction if the model exhibits "context anxiety":** If an agent starts rushing to finish because it thinks it is nearing its context limit, give it a clean slate (context reset) with a structured handoff instead of just summarizing history.
*   **Don't assume harness components are permanently necessary:** Every harness piece patches a model deficiency. As new models release with better base capabilities, regularly strip away scaffolding to see what is still load-bearing.