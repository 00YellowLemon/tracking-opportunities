---
name: harness-customization
description: What to do when designing a custom agent architecture or harness to support specific tasks. Use when a user asks to design an agent system, match a harness to a task, or structure agent capabilities.
---

# Harness Customization & Task Fit

## Overview
At its core, an agent is just: `agent = model + harness`
The harness is the scaffolding that connects the model to the real world. A model simply calls tools in a loop, but the harness's job is to provide the correct context at every step.

## Task-Harness Fit
The usefulness of an agent depends heavily on its harness. You must match the harness to the specific demands of the task. A harness designed for a customer support chatbot requires different scaffolding than a long-running asynchronous coding agent.

Consider these factors when designing a custom harness:
- **Context Management:** How much context is needed? Do you need long-running session management or context summarization to prevent window overflow?
- **Environment:** Does the agent operate in a static toolset or a dynamic environment (like a filesystem or code sandbox)?
- **Failures & Policies:** Are there transient failures that need retry logic? Are there strict PII or compliance policies that must be enforced systematically?

## Design Pattern: Deep Agents Integration
Since you are using the `deepagents` architecture, it comes pre-assembled with an opinionated middleware stack (handling memory, context management, and sandboxing).
- Use the built-in capabilities to get a production-ready agent fast.
- Identify where the task requires finer-grained customization (e.g., custom guardrails, distinct prompting) and inject custom middleware specifically for those unique business logic components, leaving the core `deepagents` loop intact.

## Delegation and Long-Running Tasks
If the harness must handle complex, long-running objectives:
- Utilize subagents to handle isolated sub-tasks with clean context windows.
- Implement a Todo List or similar state tracker to persist progress across a long run.
