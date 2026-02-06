# Skill: Generating Documentation

## Description

Generate comprehensive markdown documentation for source code files using the OpenAI LLM API. Use this skill when the user asks to generate docs, document a file, create documentation, or write docs for source code.

## Workflow

1. **Read the source file** — Use `Path.read_text()` to get the source code contents
2. **Validate the input** — Check that the file exists, is a file (not directory), and is not empty
3. **Call the LLM** — Use the `llm.py` module (never call the OpenAI SDK directly in commands)
4. **Format the output** — The LLM returns markdown; save it as `<source_name>.md`
5. **Save to `docs/` directory** — Create the directory if it doesn't exist
6. **Update storage** — Add or update a `DocEntry` in storage with the correct `source_hash`
7. **Display feedback** — Use `display.success()` to confirm completion

## LLM Module Usage

Always use the functions in `src/docgen/llm.py` to interact with the LLM. Never import `OpenAI` directly in command files.

```python
# CORRECT: Use the llm module
from docgen.llm import generate_documentation

docs = generate_documentation(source_code, source_path.name)
```

```python
# WRONG: Do NOT import OpenAI directly in commands
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(...)
```

## Prompt Engineering Conventions

When adding new LLM functions to `llm.py`, follow this pattern:

```python
def new_llm_function(source_code: str, filename: str) -> str:
    """Clear docstring explaining what this function does.

    Args:
        source_code: The contents of the source file.
        filename: The name of the source file (for context).

    Returns:
        The generated content as a string.
    """
    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Clear, specific system prompt defining the role and task.",
            },
            {
                "role": "user",
                "content": f"Action verb for `{filename}`:\n\n```\n{source_code}\n```",
            },
        ],
    )

    return response.choices[0].message.content
```

Key principles:
- System prompt defines the **role** and **output requirements**
- User prompt provides the **source code** wrapped in a code block
- Include the **filename** for context
- Always return `response.choices[0].message.content`
- Use `gpt-4o-mini` as the default model

## Documentation Output Format

Generated markdown documentation should include:
- **Overview** — What the module/file does
- **Functions/Classes** — Each public function or class
- **Parameters** — With types and descriptions
- **Return values** — What each function returns
- **Usage examples** — How to use the documented code

## Error Handling

Always wrap LLM calls in try/except:

```python
try:
    docs = generate_documentation(source_code, source_path.name)
except Exception as e:
    display.error(f"LLM error: {e}")
    raise typer.Exit(EXIT_ERROR)
```

## Storage Conventions

After generating documentation, always update storage:

```python
import hashlib

# Compute hash of current source
source_hash = hashlib.sha256(source_code.encode()).hexdigest()

# Create entry
entry = DocEntry(
    source_file=str(source_path),
    doc_file=str(doc_path),
    source_hash=source_hash,
)
add_entry(entry)
```

## File Naming

- Documentation files are named after the source file: `models.py` → `docs/models.md`
- Use `source_path.stem + ".md"` to generate the doc filename
- Default output directory is `docs/`

## Checklist

Before completing documentation generation:
- [ ] Source file validated (exists, is file, not empty)
- [ ] LLM called via `llm.py` module (not directly)
- [ ] Error handling around LLM call
- [ ] Doc file written to correct location
- [ ] Storage entry created/updated with source_hash
- [ ] Success message displayed via `display.success()`
