---
name: agent-middleware
description: What to do when you need to add custom capabilities to a LangChain agent using the create_agent middleware primitive. Use when a user asks to implement custom agent logic, manage tools, or modify agent state across execution hooks.
---

# Agent Middleware

## Overview
A key requirement for a production AI agent is connecting the agent to the right context, data, and environments. When building an agent harness using the `deepagents` architecture, the best way to add fine-grained custom capabilities and business logic on top of the pre-assembled scaffolding is to use **Middleware**.

Middleware hooks into the core agent loop at specific points:
- Before and after model calls
- Before and after tool calls
- At agent startup and teardown

## Middleware Capabilities & Patterns

### 1. Deterministic Logic
Use middleware to enforce business logic, apply guardrails, or control the agent dynamically (such as swapping models, adjusting prompts, or summarizing message history). Anything that should strictly fire at a certain point in the loop and should NOT be placed in the prompt belongs here.

**Common Middleware:**
- `SummarizationMiddleware`, `ContextEditingMiddleware` (to prevent context overflow).
- `PIIMiddleware`, `HumanInTheLoopMiddleware` (to enforce policies or steer the agent).

### 2. Tool Lifecycle Management
Instead of registering tools directly on the agent, use middleware to handle the full lifecycle (setup, initialization, registration, teardown) and provide a clean set of tools to the agent.
- Keeps configuration close to the logic that governs the tool.
- Vital when tools have external dependencies.

**Common Middleware:**
- `ShellToolMiddleware`, `FilesystemMiddleware`, `CodeInterpreterMiddleware` (to take actions in an environment).

### 3. Custom State Tracking
Middleware can extend the agent's state with custom properties, such as tracking counters or flags that persist across agent runs.
- Facilitates sharing data between different middleware hooks.

### 4. Stream Handling
Use middleware to intercept and transform the agent's output stream.
- Good for filtering events, injecting metadata, or routing events to different consumers (e.g., token deltas to a UI, tool calls to an audit log).

## Prebuilt vs Custom
- Consider prebuilt middleware for common concerns like handling transient failures (`ToolRetryMiddleware`, `ModelRetryMiddleware`), context summarization, and memory mapping.
- Create custom middleware for bespoke organization logic. Custom middleware can be cleanly reused across all agents within a company.
