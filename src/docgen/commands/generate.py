import hashlib
from pathlib import Path
from typing import Annotated

import typer

from docgen import display
from docgen.constants import EXIT_ERROR, EXIT_INVALID_INPUT
from docgen.llm import generate_documentation
from docgen.models import DocEntry, DocStatus
from docgen.storage import add_entry, find_entry, load_entries, save_entries

app = typer.Typer()


@app.command()
def generate(
    source_file: Annotated[str, typer.Argument(help="path to source file to document")],
    output_dir: Annotated[
        str, typer.Option("--output", "-o", help="output directory for docs")
    ] = "docs",
) -> None:
    """Generate documentation for a source file."""
    # Validate source file exists
    source_path = Path(source_file)
    if not source_path.exists():
        display.error(f"File not found: {source_file}")
        raise typer.Exit(EXIT_INVALID_INPUT)

    if not source_path.is_file():
        display.error(f"Not a file: {source_file}")
        raise typer.Exit(EXIT_INVALID_INPUT)

    # Read source code
    source_code = source_path.read_text()

    if not source_code.strip():
        display.error(f"File is empty: {source_file}")
        raise typer.Exit(EXIT_INVALID_INPUT)

    # Generate documentation via LLM
    display.info(f"Generating docs for {source_path.name}...")

    try:
        docs = generate_documentation(source_code, source_path.name)
    except Exception as e:
        display.error(f"LLM error: {e}")
        raise typer.Exit(EXIT_ERROR)

    # Write documentation file
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    doc_filename = source_path.stem + ".md"
    doc_path = output_path / doc_filename
    doc_path.write_text(docs)

    # Compute source hash
    source_hash = hashlib.sha256(source_code.encode()).hexdigest()

    # Update or add storage entry
    existing = find_entry(str(source_path))
    if existing:
        entries = load_entries()
        for entry in entries:
            if entry.source_file == str(source_path):
                entry.doc_file = str(doc_path)
                entry.status = DocStatus.CURRENT
                entry.source_hash = source_hash
        save_entries(entries)
    else:
        entry = DocEntry(
            source_file=str(source_path),
            doc_file=str(doc_path),
            source_hash=source_hash,
        )
        add_entry(entry)

    display.success(f"Generated: {doc_path}")
