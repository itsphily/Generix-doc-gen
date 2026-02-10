# docgen-cli

An AI-powered documentation generator for source code files using OpenAI's GPT models.

## What It Does

**docgen** automatically generates comprehensive markdown documentation for your source code files. It uses AI to analyze your code and create clear, structured documentation including:
- Overview and purpose
- Function/class descriptions
- Parameters and return values
- Usage examples

It also tracks documentation status (current/stale/error) and can verify if your docs are still accurate after code changes.

## Features

- 🤖 **AI-Powered**: Uses OpenAI GPT-4o-mini to generate high-quality documentation
- 📝 **Markdown Output**: Clean, readable markdown files
- 📊 **Status Tracking**: Monitors if documentation is current, stale, or has errors
- 🔍 **Accuracy Checking**: Detects when code changes make docs outdated
- 💾 **Persistent Storage**: Stores metadata in `.docgen/docs.json` (project-local)
- 🎨 **Rich CLI**: Beautiful colored terminal output with formatted tables

## Start Here

1. **Make sure dependencies are installed.** In your terminal, run:
   ```bash
   uv sync
   ```

2. **Check the CLI help.** Run:
   ```bash
   uv run docgen --help
   ```
   You should see 4 commands: `generate`, `list`, `check`, `update`.

3. **Try listing docs** (there are none yet):
   ```bash
   uv run docgen list
   ```
   You should see: "No documentation entries found"

4. **Generate docs for a file** (this calls the LLM — make sure your `.env` has `OPENAI_API_KEY`):
   ```bash
   uv run docgen generate src/docgen/models.py
   ```
   This should create `docs/models.md` with AI-generated documentation.

5. **List again** to see the entry:
   ```bash
   uv run docgen list
   ```
   You should see a table with `models.py`, status `current`, and the timestamp.

6. **Run the tests** to confirm everything passes:
   ```bash
   uv run pytest -v
   ```
   You should see 17 tests passing.

---

## Setup

1. **Clone and install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure OpenAI API Key:**

   Copy the example env file and add your API key:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

   Get your API key from: https://platform.openai.com/api-keys

## Usage

### Generate documentation
```bash
uv run docgen generate path/to/file.py
uv run docgen generate src/utils.py --output docs/api
```

### List all documentation entries
```bash
uv run docgen list
uv run docgen list --status stale    # filter by status
```

### Check if documentation is current
```bash
uv run docgen check path/to/file.py
```
Compares source code hash and uses AI to verify accuracy if code changed.

### Update existing documentation
```bash
uv run docgen update path/to/file.py
```

## Output

- Documentation files are saved to `docs/` by default (configurable with `--output`)
- Each source file gets a corresponding `.md` file
- Metadata is stored in `.docgen/docs.json` (project-local)

## Testing

```bash
uv run pytest -v
```

## Tech Stack

- Python 3.13+
- Typer (CLI framework)
- OpenAI Python SDK
- Rich (terminal formatting)
- python-dotenv (environment management)
