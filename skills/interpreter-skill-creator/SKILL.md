---
name: interpreter-skill-creator
description: Use this skill when you need to create a new "interpreter skill" for an AI agent. It guides you on how to properly structure an interpreter skill, write its `SKILL.md` instructions, and implement the companion module that runs in an interpreter. Trigger phrases include "create an interpreter skill", "build a new interpreter skill", or "make an interpreter skill".
---

# Interpreter Skill Creator

You are tasked with creating a new "interpreter skill", which is an extension of standard agent skills. An interpreter skill consists of both instructions (the `SKILL.md` file) and an executable code module (e.g., `index.ts`) that the agent can import and run within its interpreter runtime.

## CRITICAL: Required Folder Structure

When building an interpreter skill, the target folder MUST contain:
- `SKILL.md`: The main instructions with specific YAML frontmatter.
- A code module (usually a TypeScript file like `index.ts` or in a `scripts/` folder) containing the deterministic routines the agent can call.

## CRITICAL: Writing SKILL.md

The `SKILL.md` file defines when the skill is relevant and how to use it.
- **YAML Frontmatter**: The file MUST start with YAML frontmatter bounded by `---`.
- **Required Fields**:
  - `name`: Must be kebab-case, with no spaces and no capitals. Do NOT use "claude" or "anthropic" prefixes.
  - `description`: Must explain WHAT the skill does and WHEN to use it, including trigger phrases.
  - `metadata.module` (optional but recommended): Specify the path to the module file (e.g., `module: ./index.ts`).
- **No XML Tags**: Ensure there are no XML angle brackets anywhere in the YAML frontmatter due to security restrictions.
- **Body Content**:
  - Keep instructions concise using bullet points and numbered lists.
  - Clearly instruct the agent on how to import and use the companion module (e.g., show an import snippet like `const { myFunc } = await import("@/skills/my-skill");`).
  - Use `## CRITICAL` headers for important validations.

## CRITICAL: Writing the Code Module

The deterministic part of the workflow should live in the code module, not in prompt instructions.
- Export functions that handle the heavy lifting (e.g., validations, multi-step subagent scheduling, table manipulations).
- Design the API surface so the agent can pass context dynamically, while the module executes the structured procedure.
- The module is what gives the agent the determinism of a workflow while maintaining model discretion over when to apply it.

## Verification Step

After you create the new interpreter skill structure, YOU MUST run the validation script included in this meta-skill's directory to ensure structural correctness:

```bash
python3 skills/interpreter-skill-creator/scripts/validate.py path_to_new_skill_directory
```

Fix any errors reported by the validation script.

## References

For additional context on interpreter skills, please read:
- `./references/interpreter-skills-guide.md` (A comprehensive guide on interpreter skills based on the LangChain blog post)
