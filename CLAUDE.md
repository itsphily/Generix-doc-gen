# CLAUDE.md

An AI-powered documentation generator for source code files.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.13+ |
| CLI Framework | Typer |
| Data Validation | dataclasses |
| Output Formatting | Rich |
| Storage | JSON file |
| LLM | OpenAI Python SDK |
| Packaging | pyproject.toml + hatchling |
| Dependency Management | uv |

## Development

```bash
uv run docgen <command>
uv run pytest          # run tests
```

## Architecture

```
src/docgen/
    main.py           # Entry point, imports app from commands
    commands/
        __init__.py   # Creates main app, registers all command sub-apps
        generate.py   # generate command (calls LLM)
        list.py       # list command
        check.py      # check command (calls LLM)
        update.py     # update command
    models.py         # DocEntry dataclass, DocStatus enum (current/stale/error)
    storage.py        # JSON persistence (load_entries, save_entries, add_entry, get_entries, find_entry, delete_entry)
    display.py        # Output formatting (success/error/warning/info/table)
    llm.py            # OpenAI SDK wrapper (generate_documentation, check_accuracy, generate_summary)
    constants.py      # EXIT_SUCCESS=0, EXIT_ERROR=1, EXIT_INVALID_INPUT=2
```

**Flow**: `main.py` -> `commands/__init__.py` -> command file -> llm/storage/display

## Data Models

**DocStatus** (str, Enum): `CURRENT = "current"`, `STALE = "stale"`, `ERROR = "error"`

**DocEntry** (dataclass):
| Field | Type | Default |
|-------|------|---------|
| `source_file` | `str` | required |
| `doc_file` | `str` | required |
| `status` | `DocStatus` | `DocStatus.CURRENT` |
| `generated_at` | `datetime` | `datetime.now()` |
| `source_hash` | `str` | `""` |

## Storage

Data is persisted in `.docgen/docs.json` (project-local):

```json
{
  "version": 1,
  "entries": [
    {
      "source_file": "utils.py",
      "doc_file": "docs/utils.md",
      "status": "current",
      "generated_at": "2025-12-26T10:30:00",
      "source_hash": "a1b2c3..."
    }
  ]
}
```

## Rules

**Input validation:**
- Source file: must exist and be a file
- Source file: must not be empty
- Status filter: must be "current", "stale", or "error" (case-insensitive)

**Environment:**
- `OPENAI_API_KEY` must be set for generate, check, and update commands
