from rich.console import Console
from rich.table import Table

from docgen.models import DocEntry, DocStatus

console = Console()

STATUS_COLORS = {
    DocStatus.CURRENT: "green",
    DocStatus.STALE: "yellow",
    DocStatus.ERROR: "red",
}


def success(message: str) -> None:
    """Display a success message."""
    console.print(f"[green]{message}[/green]")


def error(message: str) -> None:
    """Display an error message."""
    console.print(f"[red]{message}[/red]")


def warning(message: str) -> None:
    """Display a warning message."""
    console.print(f"[yellow]{message}[/yellow]")


def info(message: str) -> None:
    """Display an info message."""
    console.print(message)


def table(entries: list[DocEntry]) -> None:
    """Display documentation entries in a formatted table."""
    tbl = Table()
    tbl.add_column("#", style="dim", width=4)
    tbl.add_column("Source File")
    tbl.add_column("Doc File")
    tbl.add_column("Status")
    tbl.add_column("Generated")

    for idx, entry in enumerate(entries, start=1):
        status_color = STATUS_COLORS[entry.status]

        generated_str = entry.generated_at.strftime("%b %d %H:%M")

        tbl.add_row(
            str(idx),
            entry.source_file,
            entry.doc_file,
            f"[{status_color}]{entry.status.value}[/{status_color}]",
            generated_str,
        )

    console.print(tbl)

    # Summary
    total = len(entries)
    current_count = sum(1 for e in entries if e.status == DocStatus.CURRENT)
    stale_count = sum(1 for e in entries if e.status == DocStatus.STALE)
    info(f"\n  {total} docs ({current_count} current, {stale_count} stale)")
