---
name: deepagents-interpreter
description: Adds a Code Interpreter to Deep Agents allowing agents to execute code for multi-step logic. Use when a user asks to add an interpreter, execute code in the agent loop, set up CodeInterpreterMiddleware, handle recursive orchestration, or when an agent needs to process large datasets programmatically without returning intermediate steps to the model.
---

# Deep Agents Interpreter Skill

This skill provides instructions on how to equip Deep Agents with an embedded runtime (interpreter) so agents can execute code inside their loop.

## Overview

An interpreter is a small embedded runtime (QuickJS) that allows agents to write and execute code while working. It sits between serial tool calls and full sandboxes.

- **What it solves:** Instead of using one-at-a-time tool calls or provisioning a full sandbox, agents can write a script to coordinate delegation, compose tool calls, transform structured data, and keep intermediate state out of the model context.
- **How it works:** The interpreter acts as middleware. It adds an `eval` tool to the agent, creating a QuickJS context that evaluates code and returns the final expression to the model.

## Key Concepts

- **Interpreter State:** A third context surface (alongside message history and filesystem). It holds live working values that don't need to be model input yet.
- **Programmatic Tool Calling (PTC):** Allowlisted tools appear under the `tools` namespace inside the interpreter. The interpreter can call these tools (e.g., `await tools.task({...})`).
- **Recursive Orchestration:** Interpreter code can delegate slices of work to subagents via the `tools.task` tool, synthesize the results, and return only the synthesized output.

## CRITICAL: Security & Tool Exposure

Tools are **not** automatically exposed to interpreter code. You must choose which tools can cross the host-runtime bridge by providing a `ptc` allowlist. The interpreter is intentionally limited: no filesystem, no network, no shell, no package installation, and no wall-time access by default, unless explicitly bridged.

## Installation

### Python
```bash
uv add "deepagents[quickjs]"
```

### TypeScript
```bash
pnpm install deepagents @langchain/quickjs
```

## Setup Instructions

Here is how to set up the CodeInterpreterMiddleware with Programmatic Tool Calling.

### Python

```python
from deepagents import create_deep_agent
from langchain_quickjs import CodeInterpreterMiddleware

agent = create_deep_agent(
    model="openai:gpt-5.5",
    middleware=[CodeInterpreterMiddleware(ptc=["task"])],
)
```

### TypeScript

```typescript
import { createDeepAgent } from "deepagents";
import { createCodeInterpreterMiddleware } from "@langchain/quickjs";

const agent = createDeepAgent({
  model: "openai:gpt-5.5",
  middleware: [createCodeInterpreterMiddleware({ ptc: ["task"] })],
});
```

## References

For full details, including example scripts of an agent parsing documents or making network requests, refer to the blog post located at `references/give-your-agents-an-interpreter.md`.
