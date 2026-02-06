import json
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner():
    """CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_storage(tmp_path, monkeypatch):
    """Empty storage for testing."""
    storage_dir = tmp_path / ".docgen"
    storage_dir.mkdir()
    storage_file = storage_dir / "docs.json"
    storage_file.write_text(json.dumps({"version": 1, "entries": []}))

    from docgen import storage
    monkeypatch.setattr(storage, "STORAGE_DIR", storage_dir)
    monkeypatch.setattr(storage, "STORAGE_PATH", storage_file)

    return storage_file


@pytest.fixture
def sample_data(temp_storage):
    """Pre-populated storage with sample documentation entries."""
    data = {
        "version": 1,
        "entries": [
            {
                "source_file": "utils.py",
                "doc_file": "docs/utils.md",
                "status": "current",
                "generated_at": "2025-01-01T10:00:00",
                "source_hash": "abc123",
            },
            {
                "source_file": "main.py",
                "doc_file": "docs/main.md",
                "status": "stale",
                "generated_at": "2025-01-02T10:00:00",
                "source_hash": "def456",
            },
        ],
    }
    temp_storage.write_text(json.dumps(data, indent=2))
    return data


@pytest.fixture
def mock_llm():
    """Mock the LLM module to avoid real API calls in tests."""
    with patch("docgen.llm._get_client") as mock_client:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "# Mock Documentation\n\nGenerated docs."
        mock_client.return_value.chat.completions.create.return_value = mock_response
        yield mock_client
