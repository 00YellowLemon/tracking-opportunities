# Anthropic Skills Design Reference

**Source:** The Complete Guide to Building Skills for Claude (Anthropic)

*   **Skill Structure:** Skills are packaged as a simple folder in kebab-case format. Inside, there must be a `SKILL.md` file (exact spelling, case-sensitive).
*   **YAML Frontmatter:**
    *   Must use `---` delimiters.
    *   `name`: kebab-case, no spaces, no capitals. Do NOT prefix with "claude" or "anthropic".
    *   `description`: What it does and when to use it. Must include specific trigger phrases (e.g. "when the user asks to...", "use this for..."). Keep it under 1024 characters.
    *   No XML angle brackets in YAML.
*   **Best Practices for SKILL.md Instructions:**
    *   Be concise; use bullet points and numbered lists.
    *   Put critical instructions at the top with clear headers (`## Important`, `## Critical`).
    *   Avoid ambiguous language (use explicit conditions).
    *   Move detailed explanations, long documentation, or reference material to separate files inside a `references/` subdirectory.
    *   Link to reference files rather than putting all content inline. Keep `SKILL.md` under 5,000 words.
*   **Trigger Phrases:** Use specific "WHAT" and "WHEN" descriptions. Add negative triggers if a skill triggers too often ("Do NOT use for...").
*   **Examples:** Provide clear, structural examples of the expected input and output.
