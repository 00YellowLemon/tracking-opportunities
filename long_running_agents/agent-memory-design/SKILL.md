---
name: agent-memory-design
description: Designs memory systems and architectural harnesses for long-running autonomous agents. Use when a user asks to "design an agent memory system", "architect a long-running agent", "build an agent harness", or "scale multi-agent coordination".
---

# Agent Memory Design Skill

This skill provides architectural guidance for designing memory systems and custom harnesses for long-running autonomous agents. Long-running agents handle ambitious, long-horizon tasks over hours or days, requiring specific architectures to mitigate model deficiencies in memory and follow-through.

## Architectural Principles for Memory and Harnesses

When designing an agent memory system, you must incorporate the following conceptual patterns:

### 1. Upfront Planning and Alignment
Memory starts with a stable foundation.
* **Action:** Force the agent to generate and secure human approval for a comprehensive plan *before* execution.
* **Why:** Tight prompt-response loops fail on long tasks. A minor incorrect assumption early on compounds into a completely wrong solution by the end. The approved plan serves as the primary "long-term memory" anchor.

### 2. Multi-Agent Verification (Cross-Checking)
A single agent cannot reliably hold the entire context over a 24+ hour runtime.
* **Action:** Implement a system of multiple agents where separate evaluator agents check the worker agent's output against the established plan.
* **Why:** Models lose track of the big picture, forget context, or stop at partial completion. Evaluator agents act as a persistent memory retrieval and correction mechanism, preventing drift.

### 3. Role Separation (Hierarchical Memory)
Avoid flat hierarchies where all agents share the same global state and use locks to coordinate, as this creates bottlenecks and risk-averse behavior.
* **Action:** Separate agents into "Planners" and "Workers".
    * **Planners:** Continuously explore the codebase, maintain the global context (big picture memory), and recursively break down work into tasks.
    * **Workers:** Maintain only local context (short-term memory) needed to complete a specific assigned task. They do not coordinate with other workers.

### 4. Cycles and Fresh Starts
Memory drift and tunnel vision are inevitable over long periods.
* **Action:** Implement work cycles with a "Judge" agent. At the end of a cycle, the judge evaluates progress and determines if the work should continue.
* **Why:** Starting the next iteration fresh clears degraded short-term context and forces the agent to re-orient based on the persistent plan and current codebase state.

### 5. Custom Scaffolding over Raw Intelligence
Do not rely on the raw model's context window alone to handle memory.
* **Action:** Tailor the harness to the specific frontier model being used. Use different models for different roles (e.g., use a model with strong long-context reasoning for Planners, and a strong coding model for Workers).
* **Why:** Every model has unique deficiencies. The harness must explicitly patch these gaps to ensure production-ready output (including tests and edge cases). Keep coordination mechanisms simple—worker agents can often resolve source control conflicts themselves without complex "integrator" agents.

## Implementation Guide

When asked to design a memory system, structure your output to address:
1. **The Planning State:** How the initial plan is stored, represented, and updated.
2. **The Verification Loop:** How evaluator agents access both the plan and the current state to verify work.
3. **The Role Definition:** Which agents hold global context vs. local context.
4. **The Context Reset:** The mechanism for ending a cycle, judging progress, and providing a fresh context window for the next iteration.
