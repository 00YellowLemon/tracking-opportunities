# Agent Evaluations: Shaping Behavior

**Source:** [How we build evals for Deep Agents (LangChain Blog)](https://blog.langchain.com/how-we-build-evals-for-deep-agents/)

## Core Philosophy: Evals Shape Behavior
* Every eval acts as a vector that shifts the behavior of your overall agentic system.
* More evals do not automatically mean better agents. It is better to build targeted evals that reflect desired behaviors in production rather than blindly relying on aggregate benchmark scores.
* Each eval should be self-documenting (e.g., via docstrings) explaining the specific agent capability it measures.
* *Taste insight:* The best agent evals directly measure a specific behavior you actually care about in your product. Adding tests that just score well on benchmarks can create a false illusion of improvement.

## Curating Data for Evals
* **Sources of Evals:**
  1. **Dogfooding & Traces:** Using your agents daily and analyzing traces. Every error or failure mode becomes an opportunity to write an eval to ensure the mistake doesn't happen again.
  2. **External Benchmarks:** Pulling selected tasks from datasets (like BFCL or Terminal Bench) and adapting them to your agent.
  3. **Artisanal Evals:** Writing custom, hand-crafted tests to observe isolated behaviors (e.g., testing if a specific file reading tool works).
* *Taste insight:* Build a culture of shared responsibility where every interaction is traced. When an agent fails, trace the run, understand the failure mode, fix it, and add it as an eval.

## Categorizing Evals
* Group evals by *what they test*, not where the data came from, to get a clear "middle view" of your agent's performance.
* Key behavioral categories include:
  * **File operations:** Tool usage for read, write, edit, grep, etc.
  * **Retrieval:** Multi-hop document synthesis and finding cross-file info.
  * **Tool use:** Chaining multi-step calls, tracking state, and parallel invocation.
  * **Memory:** Persisting durable info and recalling seeded context.
  * **Conversation:** Asking clarifying questions for vague requests.

## Defining Metrics: Correctness vs. Efficiency
* **Correctness First:** If an agent cannot reliably solve the tasks you care about, nothing else matters. First, ensure models pass the correctness bar (measured via custom assertions, exact matches, or LLM-as-a-judge).
* **Efficiency Second:** Once models are correct, evaluate them on efficiency (latency, extra turns, unnecessary tool calls, cost).
* **Key Metrics Used:**
  * **Correctness:** Did it complete the task correctly? (1 or 0).
  * **Step ratio:** Observed agent steps / ideal agent steps.
  * **Tool call ratio:** Observed tool calls / ideal tool calls.
  * **Latency ratio:** Observed latency / ideal latency.
  * **Solve rate:** Number of expected steps / observed latency.
* *Taste insight:* To properly evaluate efficiency, establish an **"ideal trajectory"** for tasks. This is a baseline sequence of steps that produces the correct outcome with the fewest necessary tool calls, utilizing parallelization, and avoiding unnecessary intermediate turns.
