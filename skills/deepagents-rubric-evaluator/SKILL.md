---
name: deepagents-rubric-evaluator
description: Implements self-evaluation and correction loops in deepagents using RubricMiddleware. Use when an agent task has verifiable success criteria (like passing tests, avoiding forbidden patterns) and needs to iteratively self-correct until the criteria are met or a limit is reached.
---

# DeepAgents Rubric Evaluator

This skill enables an agent to evaluate and iteratively correct its own work against a defined rubric using Langchain's `deepagents` `RubricMiddleware`.

## WHEN TO USE

Use this pattern when:
- The task has clear, verifiable definitions of "done" (e.g., test suite passes, required sections exist).
- The agent output quality degrades due to complex instructions or non-deterministic errors.
- You want the system, rather than the user, to handle the retry and correction loop automatically.

## CRITICAL INSTRUCTIONS

- **Define a Grader System Prompt:** Clearly specify the role of the grader sub-agent and what "good" looks like.
- **Provide Tool Verification:** Whenever possible, give the grader tools (like `run_test_suite` or `lint`) to gather hard evidence instead of relying solely on LLM reasoning.
- **Set `max_iterations`:** Always configure `max_iterations` to prevent infinite loops when the rubric cannot be satisfied.
- **Clear Rubrics:** Pass rubrics at invocation time as newline-delimited checklists.

## Implementation Steps

### 1. Define `RubricMiddleware`

Configure the middleware with the grader's model, system prompt, optional tools, and max iteration limit.

```python
from deepagents import RubricMiddleware

# The grader often uses a smaller/cheaper model than the main agent
rubric_middleware = RubricMiddleware(
    model="anthropic:claude-3-5-haiku-20241022",
    system_prompt="You are a code reviewer grading generated code against a rubric.",
    tools=[run_test_suite], # Provide tools to gather evidence
    max_iterations=5,       # CRITICAL: Cap iterations to avoid infinite loops
)
```

### 2. Pass Middleware to the Deep Agent

Attach the middleware when creating the deep agent. The agent has its own operating instructions (how to work), while the middleware handles grading (judging the work).

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-3-5-sonnet-20241022",
    system_prompt=(
        "You are a careful Python engineer. Write correct, readable code. "
        "Follow the user's instructions exactly."
    ),
    middleware=[rubric_middleware],
)
```

### 3. Invoke with Rubric Criteria

At invocation time, provide the human request and the checklist that the grader must mark as satisfied. If the rubric is omitted, the middleware does nothing.

```python
from langchain.messages import HumanMessage

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Write a Python function `find_duplicates(lst)` that returns a list of "
                    "all elements that appear more than once in the input list, in the order "
                    "they first appear."
                )
            )
        ],
        "rubric": (
            "- All tests pass in run_test_suite\n"
            "- The function is named `find_duplicates` and accepts a single list argument\n"
        ),
    },
    config={"configurable": {"thread_id": "code-generation-session"}},
)

print(result["messages"][-1].text)
```

## Best Practices & Pitfalls

- **Model Selection:** Use a faster, more cost-effective model for the grader (e.g., Claude Haiku) and a more capable model for the generating agent (e.g., Claude Sonnet).
- **Actionable Feedback:** The grader returns per-criterion feedback. Ensure your rubric criteria are specific enough so that the generated feedback tells the agent exactly what to fix.
- **Deterministic Evaluation:** When tools are provided, the grader evaluates based on execution results rather than abstract reasoning. This significantly increases reliability.
- **Empty Rubrics:** If no rubric string is provided at invoke time, the middleware is effectively bypassed. Use this dynamically based on the task type.
