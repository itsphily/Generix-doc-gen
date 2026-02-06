import json
from datetime import datetime
from pathlib import Path

from docgen.models import DocEntry, DocStatus

STORAGE_DIR = Path.home() / ".docgen"
STORAGE_PATH = STORAGE_DIR / "docs.json"


def _ensure_storage_exists() -> None:
    """Create storage directory and file if they don't exist."""
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    if not STORAGE_PATH.exists():
        STORAGE_PATH.write_text(json.dumps({"version": 1, "entries": []}))


def _entry_to_dict(entry: DocEntry) -> dict:
    """Convert a DocEntry to a JSON-serializable dictionary."""
    return {
        "source_file": entry.source_file,
        "doc_file": entry.doc_file,
        "status": entry.status.value,
        "generated_at": entry.generated_at.isoformat(),
        "source_hash": entry.source_hash,
    }


def _dict_to_entry(data: dict) -> DocEntry:
    """Convert a dictionary to a DocEntry object."""
    return DocEntry(
        source_file=data["source_file"],
        doc_file=data["doc_file"],
        status=DocStatus(data["status"]),
        generated_at=datetime.fromisoformat(data["generated_at"]),
        source_hash=data["source_hash"],
    )


def load_entries() -> list[DocEntry]:
    """Load all documentation entries from storage."""
    _ensure_storage_exists()
    data = json.loads(STORAGE_PATH.read_text())
    return [_dict_to_entry(e) for e in data["entries"]]


def save_entries(entries: list[DocEntry]) -> None:
    """Save all documentation entries to storage."""
    _ensure_storage_exists()
    data = {"version": 1, "entries": [_entry_to_dict(e) for e in entries]}
    STORAGE_PATH.write_text(json.dumps(data, indent=2))


def add_entry(entry: DocEntry) -> None:
    """Add an entry and save to storage."""
    entries = load_entries()
    entries.append(entry)
    save_entries(entries)


def get_entries(status: DocStatus | None = None) -> list[DocEntry]:
    """Get entries with optional filtering by status."""
    entries = load_entries()

    if status is not None:
        entries = [e for e in entries if e.status == status]

    return entries


def find_entry(source_file: str) -> DocEntry | None:
    """Find an entry by source file path. Returns None if not found."""
    entries = load_entries()
    for entry in entries:
        if entry.source_file == source_file:
            return entry
    return None


def delete_entry(source_file: str) -> None:
    """Delete an entry by source file path."""
    entries = load_entries()
    entries = [e for e in entries if e.source_file != source_file]
    save_entries(entries)
