# Exercise 1: Creating a SKILL.md File

**Duration:** 10-12 minutes
**Goal:** Create the `reviewing-documentation` skill that teaches Claude Code how to review `docgen` CLI commands for code quality and convention adherence.

---

## Context

Skills are markdown instruction files that give Claude Code domain-specific knowledge. When a skill is loaded, Claude reads the SKILL.md file and follows its instructions precisely. In this exercise, you will create a skill that turns Claude into an expert code reviewer for the `docgen` project.

You will use two reference points throughout this exercise:
- **`generate.py`** — the "gold standard" command that follows all conventions correctly
- **`update.py`** — the "bad example" that violates many conventions (this is what the reviewer should catch)

Open both files now and keep them visible. Understanding the difference between them is the key to writing a good skill.

---

## Step 1: Copy the Template

Open the template file at `exercises/exercise-1-template-SKILL.md` and copy it to the skill location:

```
.claude/skills/reviewing-documentation/SKILL.md
```

Create the directory structure if it does not exist.

> **Hint:** You can do this from the terminal:
> ```bash
> mkdir -p .claude/skills/reviewing-documentation
> cp exercises/exercise-1-template-SKILL.md .claude/skills/reviewing-documentation/SKILL.md
> ```

---

## Step 2: Write the Description Section

Open your new `SKILL.md` file and fill in the **Description** section. This tells Claude WHAT the skill does and WHEN it should activate.

Your description should cover:
- **What it does:** Reviews CLI command files and generated documentation for code quality, convention adherence, and best practices
- **When it triggers:** When the user asks to review code, check quality, audit a command, validate best practices, or inspect documentation

> **Hint:** Think about the different ways a user might phrase a review request. Include trigger phrases like "review", "check", "audit", "validate", "inspect quality", and "look for issues". The more trigger phrases you include, the more reliably Claude will load this skill when needed.

Example structure:
```markdown
## Description

This skill reviews `docgen` CLI command files for code quality and convention adherence.
It activates when the user asks to [list trigger scenarios here].

The reviewer checks against a comprehensive checklist covering type annotations,
module usage, error handling, and project conventions.
```

---

## Step 3: Complete the Workflow

Fill in the **Workflow** section with these 4 steps. Each step should describe what Claude does and why.

### Step 1 — Read Target Files
Read the file(s) the user wants reviewed. Understand the command's purpose, its arguments, and its logic flow.

### Step 2 — Read Reference Files
Read the project's core modules to understand the established patterns:
- `display.py` — how output should be formatted (success, error, warning, info messages)
- `constants.py` — what exit codes and constants are available
- `llm.py` — how LLM calls should be made
- `generate.py` — the gold-standard command that follows all conventions

### Step 3 — Check Against Checklist
Compare the target file against every item in the Code Quality Checklist (which you will write in the next step). Flag each violation with a severity level.

### Step 4 — Report Findings
Format the results as specified in the Output Format section.

> **Hint:** Be explicit about which files to read. Claude performs better when you give it exact file paths rather than vague instructions like "read the relevant files."

---

## Step 4: Fill in the Code Quality Checklist

This is the most important section of the skill. For each category, provide a CORRECT example and a WRONG example. Claude uses these concrete examples to identify violations.

### Category 1: Type Annotations

All CLI parameters must use `Annotated` with `typer.Argument` or `typer.Option` and include a `help` string.

**CORRECT:**
```python
def generate(
    path: Annotated[str, typer.Argument(help="Path to the source file to document")],
    output: Annotated[str, typer.Option(help="Output directory for documentation")] = "docs",
):
```

**WRONG:**
```python
def generate(path: str, output: str = "docs"):
```

> **Hint:** Look at how `generate.py` declares its parameters versus how `update.py` does it. The difference is the `Annotated` wrapper with help text.

---

### Category 2: Display Module

All user-facing output must go through the `display` module, never through raw `print()`.

**CORRECT:**
```python
display.success("Documentation generated successfully")
display.error("File not found")
display.warning("No changes detected")
display.info("Processing file...")
```

**WRONG:**
```python
print("Documentation generated successfully")
print("Error: File not found")
```

> **Hint:** The `display` module provides consistent formatting with colors, icons, and proper styling. Using `print()` breaks the visual consistency of the CLI.

---

### Category 3: Exit Codes

All exit codes must use named constants from `constants.py`, never magic numbers.

**CORRECT:**
```python
from docgen.constants import EXIT_SUCCESS, EXIT_INVALID_INPUT, EXIT_GENERATION_ERROR

raise typer.Exit(EXIT_INVALID_INPUT)
```

**WRONG:**
```python
raise typer.Exit(1)
raise typer.Exit(code=2)
```

> **Hint:** Named exit codes make the code self-documenting. When you see `EXIT_INVALID_INPUT`, you know exactly what happened. When you see `1`, you have to guess.

---

### Category 4: Input Validation

All file path arguments must be validated before use. Check that the path exists and is the expected type (file vs directory).

**CORRECT:**
```python
path = Path(path_str)
if not path.exists():
    display.error(f"Path does not exist: {path}")
    raise typer.Exit(EXIT_INVALID_INPUT)
if not path.is_file():
    display.error(f"Path is not a file: {path}")
    raise typer.Exit(EXIT_INVALID_INPUT)
```

**WRONG:**
```python
# Directly reading the file without checking if it exists
content = Path(path_str).read_text()
```

> **Hint:** Without validation, the user gets a raw Python traceback instead of a friendly error message. Check `generate.py` to see how it validates inputs before proceeding.

---

### Category 5: LLM Module

All LLM interactions must go through the `llm` module, never by importing OpenAI or another provider directly.

**CORRECT:**
```python
from docgen.llm import generate_documentation

result = generate_documentation(source_code, context)
```

**WRONG:**
```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

> **Hint:** The `llm` module abstracts the provider. If the team switches from OpenAI to Anthropic, only `llm.py` needs to change. Commands that import OpenAI directly will break.

---

### Category 6: Storage Module

All documentation metadata must be managed through the `storage` module, never by manipulating JSON files directly.

**CORRECT:**
```python
from docgen.storage import add_entry, get_entries

add_entry(doc_metadata)
entries = get_entries()
```

**WRONG:**
```python
import json

with open("docs/index.json", "r") as f:
    data = json.load(f)
data.append(new_entry)
with open("docs/index.json", "w") as f:
    json.dump(data, f)
```

> **Hint:** Direct JSON manipulation bypasses validation, default values, and any future schema migrations that the `storage` module handles.

---

## Step 5: Define the Output Format

Fill in the **Output Format** section. The reviewer's output should be structured and actionable.

### Issues Table

The output should include a markdown table with these columns:

| Severity | Description | Location | Suggested Fix |
|----------|-------------|----------|---------------|
| Critical | Using `print()` instead of `display` module | `update.py`, line 23 | Replace `print(msg)` with `display.info(msg)` |
| Warning  | Missing docstring on command function | `update.py`, line 10 | Add a docstring describing the command's purpose |

- **Critical** — violations that break conventions or cause runtime issues
- **Warning** — style issues or missing best practices that should be fixed

### Summary

After the table, include a summary:
```
## Summary
- Critical issues: X
- Warnings: Y
- Total: Z

### Critical Fixes Required
[For each critical issue, show the specific code change needed]
```

> **Hint:** Structured output makes it easy for the main agent (or a human) to act on the findings. The suggested fix column is especially important — it tells the developer exactly what to do.

---

## Step 6: Complete the Conventions Checklist

Add a **Conventions Checklist** section with 10 or more items. These are yes/no checks the reviewer runs through for every file.

Write each item as a clear, checkable statement:

1. All CLI parameters use `Annotated` types with `typer.Argument()` or `typer.Option()` and include `help` text
2. All user-facing output uses the `display` module (`display.success()`, `display.error()`, `display.warning()`, `display.info()`)
3. No raw `print()` calls exist anywhere in the command
4. All exit codes use named constants from `constants.py` (e.g., `EXIT_SUCCESS`, `EXIT_INVALID_INPUT`)
5. No magic numbers are used for exit codes
6. All file path inputs are validated (existence check, type check) before use
7. Error messages are user-friendly and suggest next steps
8. The command function has a docstring explaining its purpose
9. LLM interactions use the `llm` module, not direct provider imports
10. Storage operations use the `storage` module, not direct JSON manipulation
11. Imports are organized: standard library, third-party, local modules
12. The command follows the same structure as `generate.py` (validate, process, display, exit)

> **Hint:** Think about what makes `generate.py` good and `update.py` bad. Every difference between those two files is a potential checklist item.

---

## Step 7: Verify Your Skill

Open Claude Code and run the `/skills` command. You should see `reviewing-documentation` listed as an available skill.

If it does not appear:
- Check that the file is at exactly `.claude/skills/reviewing-documentation/SKILL.md`
- Make sure the file is valid markdown
- Close and reopen Claude Code to reload skills

---

## Success Criteria

You have completed this exercise when:
- [ ] The SKILL.md file exists at `.claude/skills/reviewing-documentation/SKILL.md`
- [ ] The Description section explains what the skill does and when it triggers
- [ ] The Workflow section has 4 clear steps
- [ ] The Code Quality Checklist has 6 categories, each with CORRECT and WRONG examples
- [ ] The Output Format defines the issues table structure and summary format
- [ ] The Conventions Checklist has 10+ checkable items
- [ ] The skill appears when you run `/skills` in Claude Code
