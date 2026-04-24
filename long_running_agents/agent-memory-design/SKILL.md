---
name: agent-memory-design
description: Architect and design memory systems and harnesses for long-running autonomous agents. Use when users ask to design an agent memory system, architect a long-running agent, build an agent harness, scale multi-agent coordination, or implement agentic engineering workflows.
---

# Agent Memory Design Skill

## CRITICAL: Initial Workflow Requirement
* **Iterative User Interview:** Before generating any architecture, you MUST conduct an iterative user interview phase to gather comprehensive requirements. Ensure you fully understand the user's goals before proposing a design.

## Core Architectural Principles
When designing a memory system or harness for a long-running agent, you must incorporate these fundamental patterns:

* **Custom Harnesses:** Tailor scaffolding to patch the specific frontier model's memory and follow-through deficiencies. Do not rely on raw model context windows alone.
* **Upfront Planning:** Force the agent to generate a plan and secure human approval *before* any execution begins. This plan acts as the primary long-term memory anchor.
* **Multi-Agent Verification:** Avoid relying on a single agent to maintain context over 24+ hours. Use separate evaluator agents to continuously check worker outputs against the approved plan.
* **Cycles and Fresh Starts:** Use a "Judge" agent at the end of work cycles to determine continuation. Start the next cycle fresh to clear degraded short-term memory and prevent drift.

## Architecture: Agentic Engineering & Role Separation
Scale systems horizontally using distinct roles. Avoid flat hierarchies, file-locking, or optimistic concurrency for self-coordination.

* **Leader Agents (Planners / Project Leaders):**
  * Provide coordination, governance, and visibility across a swarm of worker agents.
  * Continuously explore the codebase and recursively break down work.
  * Manage long-term memory, maintain a shared prompt/workflow library, and handle cross-team orchestration.
  * Separate orchestration (when/how agents act) from execution.
* **Worker Agents (Individual Contributors):**
  * Focus entirely on assigned tasks within defined boundaries.
  * Retrieve short-term context from systems of record.
  * Execute workflows using tools or coding agents as reasoning engines.
  * Do not coordinate directly with other workers; report actions to the Leader Agent.

## Architecture: Async Subagents
For tasks taking hours, inline synchronous execution creates severe bottlenecks.

* **Decoupled Execution ("Fire-and-Steer"):** Launch subagents in the background. The supervisor receives a task ID immediately, freeing it to handle user interaction or dispatch other agents.
* **Independent State:** Async subagents must run as fully isolated processes with their own independent state and memory threads.
* **Standardized Remote Management:** Use a framework-agnostic API (e.g., Agent Protocol) for standardized communication (creating threads, polling status, managing memory).

## Implementation Guide
Structure your final output with exactly these sections:
1. **Architecture Overview:** Describe the Leader/Worker roles, custom scaffolding, and async subagent implementation.
2. **Memory Design:** Detail how the initial plan is stored, how Planners maintain global context, and how Workers use local context.
3. **Evaluation Loop:** Explain how evaluator agents access the plan and current state to verify work, including the cycle reset mechanism.
4. **Subagent Hierarchy:** Define the breakdown of tasks and standardized remote management endpoints.
