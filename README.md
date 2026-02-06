# docgen-cli

An AI-powered documentation generator for source code files.

## Usage

```bash
uv run docgen generate <source-file>   # Generate docs for a file
uv run docgen list                     # List all generated docs
uv run docgen check <source-file>      # Check if docs are up to date
uv run docgen update <source-file>     # Update existing docs
```

## Setup

```bash
uv sync
export OPENAI_API_KEY="your-api-key"
```

## Testing

```bash
uv run pytest -v
```
