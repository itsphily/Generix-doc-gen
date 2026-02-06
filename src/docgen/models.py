from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DocStatus(str, Enum):
    CURRENT = "current"
    STALE = "stale"
    ERROR = "error"


@dataclass
class DocEntry:
    source_file: str
    doc_file: str
    status: DocStatus = DocStatus.CURRENT
    generated_at: datetime = field(default_factory=datetime.now)
    source_hash: str = ""
