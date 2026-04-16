# Agent Evaluations and Designing Harnesses
**Source:** [How we build evals for Deep Agents (LangChain Blog)](https://blog.langchain.com/how-we-build-evals-for-deep-agents/)

*   **Evals Shape Behavior:** Every evaluation is a vector shifting overall system behavior. Targeted evals reflecting desired production behaviors are vastly superior to blindly pursuing aggregate benchmark scores.
*   **Targeted Measurement:** The best agent evals directly measure an agent behavior explicitly cared about in the product.
*   **Curation Strategy (Sources of Evals):**
    *   **Dogfooding & Tracing:** Everyday usage and tracing. Every failure is an opportunity for a new eval to prevent regression.
    *   **External Benchmarks:** Selective adaptation of tasks from datasets like Terminal Bench 2.0 or BFCL.
    *   **Artisanal Evals:** Custom, hand-crafted tests verifying isolated behaviors (e.g., verifying a specific tool works).
*   **Evaluation Categorization (The "Middle View"):** Group evals by what they test rather than the source. Categories include:
    *   **File operations:** Read, write, grep, ls, pagination, parallel invocation.
    *   **Retrieval:** Multi-hop document synthesis, finding cross-file information.
    *   **Tool use:** Tracking state, multi-step chaining, correct tool selection.
    *   **Memory:** Persisting durable info and recalling seeded context.
    *   **Conversation:** Clarifying vague requests, multi-turn dialogue.
*   **Correctness vs. Efficiency:**
    *   **Correctness First:** If an agent cannot reliably solve the primary task, efficiency does not matter. Measure via assertions, exact matches, or LLM-as-a-judge.
    *   **Efficiency Second:** Compare models that pass correctness. Measure latency, cost, and excessive tool usage or turns.
*   **Key Efficiency Metrics:**
    *   **Step ratio:** Observed agent steps / ideal agent steps.
    *   **Tool call ratio:** Observed tool calls / ideal tool calls.
    *   **Latency ratio:** Observed latency / ideal latency.
    *   **Solve rate:** Expected steps / observed latency.
*   **The "Ideal Trajectory":** A baseline sequence of steps producing a correct outcome with zero unnecessary actions. For example, doing tasks via optimal tool parallelization without unnecessary intermediate conversational turns.
