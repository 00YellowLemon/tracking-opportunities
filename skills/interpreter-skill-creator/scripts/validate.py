import os
import sys

def validate_skill(skill_dir):
    errors = []
    skill_md_path = os.path.join(skill_dir, "SKILL.md")

    if not os.path.exists(skill_md_path):
        errors.append("Missing SKILL.md in the skill directory.")
        return errors

    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for YAML frontmatter
    if not content.startswith("---"):
        errors.append("SKILL.md does not start with YAML frontmatter (---).")
    else:
        # Extract frontmatter
        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append("SKILL.md does not have properly closed YAML frontmatter.")
        else:
            frontmatter = parts[1]

            # Check for XML tags in frontmatter only
            if "<" in frontmatter and ">" in frontmatter:
                errors.append("YAML frontmatter contains XML tags which are forbidden.")

            if "name:" not in frontmatter:
                errors.append("Frontmatter missing required 'name' field.")
            else:
                name_line = [line for line in frontmatter.split('\n') if line.strip().startswith('name:')][0]
                name_value = name_line.split(':', 1)[1].strip().strip('"').strip("'")

                if " " in name_value:
                    errors.append(f"Name '{name_value}' contains spaces. Must be kebab-case.")
                if any(c.isupper() for c in name_value):
                    errors.append(f"Name '{name_value}' contains capital letters. Must be kebab-case.")
                if name_value.startswith("claude") or name_value.startswith("anthropic"):
                    errors.append(f"Name '{name_value}' starts with reserved prefixes 'claude' or 'anthropic'.")

            if "description:" not in frontmatter:
                errors.append("Frontmatter missing required 'description' field.")

            if "module:" not in frontmatter and "metadata:" not in frontmatter:
                # Based on the blog post, an interpreter skill should ideally reference a module
                # Let's just issue a warning or a soft error
                pass

    # Check for script file (e.g., index.ts)
    ts_files = [f for f in os.listdir(skill_dir) if f.endswith(".ts") or f.endswith(".js")]
    if not ts_files and not os.path.exists(os.path.join(skill_dir, "scripts")):
        errors.append("No TypeScript/JavaScript module found in the skill directory to act as the interpreter skill logic.")

    return errors

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate.py <path_to_skill_directory>")
        sys.exit(1)

    target_dir = sys.argv[1]

    if not os.path.isdir(target_dir):
        print(f"Error: {target_dir} is not a valid directory.")
        sys.exit(1)

    validation_errors = validate_skill(target_dir)

    if validation_errors:
        print("Validation failed with the following errors:")
        for error in validation_errors:
            print(f"- {error}")
        sys.exit(1)
    else:
        print("Validation passed! The interpreter skill structure looks good.")
        sys.exit(0)
