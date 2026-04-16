# Harness Design for Long-Running Applications

**Source:** [https://www.anthropic.com/engineering/harness-design-long-running-apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)

*   **Subjective Task Evaluation**: Agents are notoriously lenient when grading their own work. Introducing a skeptical, external Evaluator agent forces the Generator agent to iterate and improve.
*   **Concrete Grading Criteria**: To evaluate subjective output (like UX design), define concrete guidelines (e.g. Design Quality, Originality, Craft) to turn subjective judgments into gradable parameters.
*   **Three-Agent Architecture**:
    *   **Planner**: Expands high-level prompts into concrete, deliverable-focused product specs (avoiding overly detailed technical specifications early on).
    *   **Generator**: Builds features in chunks based on agreed-upon "sprint contracts" (defining what 'done' means).
    *   **Evaluator**: Navigates the live application (e.g. via Playwright) to test features and ensure quality matches the contract, looping feedback back to the Generator.
*   **Context Resets vs Compaction**: For tasks where the agent experiences "context anxiety" (rushing to finish as the window fills up), perform a structured handoff of state to a fresh context window rather than simply summarizing history.
