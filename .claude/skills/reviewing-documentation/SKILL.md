# Skill: Reviewing Documentation and CLI Commands

## Description

Review CLI command files and generated documentation for quality, correctness, and adherence to project conventions. Use this skill when the user asks to review code, check quality, audit a command, or validate that best practices are followed.

## Workflow

1. **Read the target file(s)** — Read the command file or documentation to review
2. **Read reference files** — Check `display.py`, `constants.py`, `llm.py`, and a known-good command (e.g., `generate.py`) for conventions
3. **Check against quality checklist** — Go through each item systematically
4. **Report findings** — Use the output format below with severity levels

## Code Quality Checklist

### Type Annotations
Every command parameter must use the `Annotated` pattern:

```python
# CORRECT
from typing import Annotated

def command(
    source_file: Annotated[str, typer.Argument(help="description")],
    output_dir: Annotated[str, typer.Option("--output", "-o", help="description")] = "docs",
) -> None:
```

```python
# WRONG - missing type annotations
def command(source_file, output_dir="docs"):
```

### Docstrings
Every command function must have a docstring:

```python
# CORRECT
@app.command()
def generate(...) -> None:
    """Generate documentation for a source file."""
```

```python
# WRONG - no docstring
@app.command()
def generate(...) -> None:
    # no docstring here
```

### Display Module Usage
Always use `display.success()`, `display.error()`, `display.warning()`, `display.info()` — never use `print()`:

```python
# CORRECT
from docgen import display
display.success(f"Generated: {doc_path}")
display.error(f"File not found: {source_file}")
```

```python
# WRONG
print("Done!")
print("Error: " + message)
```

### Exit Codes
Use constants from `constants.py`, never hardcoded integers:

```python
# CORRECT
from docgen.constants import EXIT_ERROR, EXIT_INVALID_INPUT
raise typer.Exit(EXIT_INVALID_INPUT)
```

```python
# WRONG
raise typer.Exit(1)
raise typer.Exit(2)
```

### Input Validation
Every command must validate its inputs before processing:

```python
# CORRECT
source_path = Path(source_file)
if not source_path.exists():
    display.error(f"File not found: {source_file}")
    raise typer.Exit(EXIT_INVALID_INPUT)

if not source_path.is_file():
    display.error(f"Not a file: {source_file}")
    raise typer.Exit(EXIT_INVALID_INPUT)
```

```python
# WRONG - no validation, will crash on missing files
source_code = Path(source_file).read_text()
```

### LLM Module Usage
Commands must never import or use the OpenAI SDK directly. Always use `llm.py`:

```python
# CORRECT
from docgen.llm import generate_documentation
docs = generate_documentation(source_code, filename)
```

```python
# WRONG
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(...)
```

### Storage Module Usage
Commands must never manipulate the JSON storage file directly. Always use `storage.py`:

```python
# CORRECT
from docgen.storage import add_entry, find_entry, load_entries, save_entries
add_entry(entry)
```

```python
# WRONG
import json
data = json.loads(STORAGE_PATH.read_text())
data["entries"].append({...})
STORAGE_PATH.write_text(json.dumps(data))
```

### Error Handling
LLM calls and file operations must be wrapped in try/except:

```python
# CORRECT
try:
    docs = generate_documentation(source_code, source_path.name)
except Exception as e:
    display.error(f"LLM error: {e}")
    raise typer.Exit(EXIT_ERROR)
```

## Output Format

When reporting review findings, use this format:

### Issues Found

| Severity | Issue | Location | Suggested Fix |
|----------|-------|----------|---------------|
| Critical | Using `print()` instead of `display` module | Line 12 | Replace with `display.info(...)` |
| Critical | Wrong exit code on success | Line 45 | Use `EXIT_SUCCESS` or remove exit |
| Warning | Missing docstring | Line 8 | Add `"""Command description."""` |
| Warning | No input validation | Line 15 | Add file existence check |

### Summary

- **Critical issues**: X
- **Warnings**: Y
- **Status**: PASS / FAIL

### Suggested Fixes

Provide specific code changes for each critical issue.

## Conventions Checklist

- [ ] All parameters use `Annotated[type, typer.Argument/Option(...)]`
- [ ] Function has a docstring
- [ ] Return type is `-> None`
- [ ] Uses `display` module for all output (no `print()`)
- [ ] Uses `constants.py` exit codes (no hardcoded numbers)
- [ ] Validates all inputs before processing
- [ ] Uses `llm.py` for LLM calls (no direct OpenAI imports in commands)
- [ ] Uses `storage.py` for data persistence (no direct JSON manipulation)
- [ ] Error handling around LLM calls and file I/O
- [ ] Uses f-strings (no string concatenation with `+`)
- [ ] Imports at the top of the file (not inside functions)
