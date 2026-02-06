from typing import Annotated

import typer

from docgen import display
from docgen.constants import EXIT_INVALID_INPUT
from docgen.models import DocStatus
from docgen.storage import get_entries

app = typer.Typer()


@app.command()
def list(
    status: Annotated[
        str | None, typer.Option("--status", "-s", help="filter by status (current/stale/error)")
    ] = None,
) -> None:
    """List all generated documentation entries."""
    # Parse status filter
    status_filter = None
    if status:
        try:
            status_filter = DocStatus(status.lower())
        except ValueError:
            display.error(f"Invalid status: {status}. Use current, stale, or error")
            raise typer.Exit(EXIT_INVALID_INPUT)

    # Get filtered entries
    entries = get_entries(status=status_filter)

    if not entries:
        display.warning("No documentation entries found")
        return

    display.table(entries)
