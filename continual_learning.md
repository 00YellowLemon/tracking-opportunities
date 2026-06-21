# Continual Learning for AI Agents

**Source:** [Continual learning for AI agents (LangChain Blog)](https://blog.langchain.com/continual-learning-for-ai-agents/)

Continual learning in AI systems happens at three distinct layers: the **model** (weights), the **harness** (code/scaffolding), and the **context** (memory/instructions). The following focuses on implementing continual learning specifically within the harness and context layers.

## Continual Learning at the Harness Layer
*   **Definition:** The harness encompasses the code that drives the agent, as well as permanent tools and base system prompts.
*   **Implementation loop (Meta-Harness approach):**
    1.  Run the agent over a batch of tasks.
    2.  Evaluate the task outcomes.
    3.  Store all execution logs (traces) into a filesystem.
    4.  Deploy a separate "coding agent" to analyze these traces and suggest concrete changes to the underlying harness code.
*   **Scope:** Usually optimized at the global agent level, though theoretically possible to maintain customized code harnesses per user.

## Continual Learning at the Context Layer
*   **Definition:** Context sits outside the harness and configures it dynamically. This includes memory, specific instructions, or skills (e.g., maintaining a `SOUL.md` file or user-specific preferences).
*   **Scope:** Can be updated at the agent level (global memory), or segmented at the tenant level (user, team, or organization).
*   **Implementation methods:**
    1.  **Offline jobs ("Dreaming"):** Asynchronous batch processes that run over recent execution traces to extract patterns, insights, and update the context files.
    2.  **In the hot path:** The agent explicitly updates its persistent memory in real-time as it works on a core task. This can be triggered autonomously via core instructions or explicitly prompted by the user.

## Traces as the Core Engine
*   **Foundation:** High-quality traces (the full execution path of an agent's actions) are the core dependency for enabling continual learning.
*   *Taste insight:* A well-designed agent harness must treat trace collection as a primary feature. Without traces, neither the harness nor the context can reflectively learn from past failures or successes.
