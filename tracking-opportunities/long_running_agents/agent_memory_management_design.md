# Agent Memory Management Design for Harness Generation

**Sources:**
- [Deep Agents Backends](https://docs.langchain.com/oss/python/deepagents/backends)
- [Deep Agents Memory](https://docs.langchain.com/oss/python/deepagents/memory)

This document outlines the memory management and architectural design for an autonomous agent tasked with generating AI agent harnesses.

## Architectural Memory Principles
- **Upfront Planning and Alignment:** Memory starts with a stable foundation. The agent must formulate a plan and secure human approval *before* any instructions are generated, preventing compounding errors early in the process.
- **Multi-Agent Verification:** Since a single agent cannot reliably hold all context during long runs, use evaluator agents. These evaluators serve as a persistent memory retrieval mechanism, constantly checking worker output against the agreed-upon plan to prevent drift.
- **Hierarchical Role Separation:** Maintain clean context by separating roles. "Planners" maintain the global context (big picture memory) and recursively break down tasks. "Workers" only hold local context (short-term memory) needed for their specific task.
- **Cycles and Fresh Starts:** Implement a "Judge" agent to evaluate progress at the end of cycles. This clears degraded short-term context and forces a fresh start, realigning the agent with the persistent plan.

## Storage Strategy (Composite Backend)
- **Routing by Path:** Utilize a composite routing mechanism to direct memory operations to different persistence backends based on file path prefixes.
- **Ephemeral State (Short-term):** Designate a default state backend for intermediate scratchpads and short-term reasoning. This context is wiped after the thread completes, preventing pollution of long-term storage.
- **Durable Store (Long-term):** Designate specific paths (e.g., `/skills/`) to a durable store backend. This persists essential operating knowledge across multiple runs and threads.

## Memory Scope and Supported Types
- **User-Scoped Isolation:** Because this is a single-user system, all durable memory namespaces are rigidly scoped to the specific user's identity, ensuring no cross-contamination if scaled later.
- **Episodic Memory:** Maintain searchable records of past execution threads. This allows the agent to recall the exact steps and outcomes of previously generated harnesses, serving as experience-based context.
- **Procedural Memory:** Store reusable skills and step-by-step instructions (e.g., how to format Codex prompts). The agent reads these into context only when the specific capability is required.
- **No Semantic Memory:** By design, the system avoids storing generalized semantic memory (like persistent user preferences or broad facts), keeping the context window strictly focused on the current episodic and procedural task.

## Inputs and Human-in-the-Loop (HITL)
- **System Inputs:** The primary inputs include the explicit user request for the harness, any provided procedural skills, and the target specifications for the coding agent.
- **Upfront Approval Gate:** Enforce a strict Human-in-the-Loop checkpoint where the user must review and approve the Planner's architectural strategy before any worker begins execution.
- **Output Review Gate:** Implement an interrupt-driven approval checkpoint before the final generated instructions are dispatched to the downstream coding agent, ensuring the output adheres to the initially approved plan.
