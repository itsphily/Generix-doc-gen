import hashlib
from pathlib import Path
from typing import Annotated

import typer

from docgen import display
from docgen.constants import EXIT_ERROR, EXIT_INVALID_INPUT
from docgen.llm import check_accuracy
from docgen.models import DocStatus
from docgen.storage import find_entry, load_entries, save_entries

app = typer.Typer()


@app.command()
def check(
    source_file: Annotated[str, typer.Argument(help="source file to check docs against")],
) -> None:
    """Check if documentation is still accurate for a source file."""
    # Validate source file exists
    source_path = Path(source_file)
    if not source_path.exists():
        display.error(f"File not found: {source_file}")
        raise typer.Exit(EXIT_INVALID_INPUT)

    # Find existing documentation entry
    existing = find_entry(str(source_path))
    if not existing:
        display.error(f"No documentation found for: {source_file}")
        raise typer.Exit(EXIT_INVALID_INPUT)

    # Check if doc file still exists
    doc_path = Path(existing.doc_file)
    if not doc_path.exists():
        display.error(f"Doc file missing: {existing.doc_file}")
        raise typer.Exit(EXIT_ERROR)

    # Read current source and existing docs
    source_code = source_path.read_text()
    existing_docs = doc_path.read_text()

    # Quick hash check
    current_hash = hashlib.sha256(source_code.encode()).hexdigest()
    if current_hash == existing.source_hash:
        display.success(f"Docs are up to date for {source_file}")
        return

    # Source changed -- call LLM to check accuracy
    display.info(f"Source changed, checking accuracy for {source_path.name}...")

    try:
        report = check_accuracy(source_code, existing_docs)
    except Exception as e:
        display.error(f"LLM error: {e}")
        raise typer.Exit(EXIT_ERROR)

    # Mark as stale in storage
    entries = load_entries()
    for entry in entries:
        if entry.source_file == str(source_path):
            entry.status = DocStatus.STALE
    save_entries(entries)

    display.warning(f"Docs may be stale for {source_file}")
    display.info(report)
