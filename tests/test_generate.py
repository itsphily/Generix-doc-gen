"""Tests for the generate command."""

import json

from docgen.commands import app


class TestGenerate:
    """Test suite for generate command."""

    def test_generates_docs_for_valid_file(self, runner, temp_storage, mock_llm, tmp_path):
        """Test generating docs for a valid source file."""
        source = tmp_path / "example.py"
        source.write_text("def hello(): pass")

        result = runner.invoke(app, ["generate", str(source)])

        assert result.exit_code == 0
        assert "Generated:" in result.output

    def test_creates_doc_file(self, runner, temp_storage, mock_llm, tmp_path):
        """Test that a markdown doc file is created."""
        source = tmp_path / "example.py"
        source.write_text("def hello(): pass")
        output_dir = tmp_path / "docs"

        runner.invoke(app, ["generate", str(source), "--output", str(output_dir)])

        doc_file = output_dir / "example.md"
        assert doc_file.exists()
        assert doc_file.read_text() == "# Mock Documentation\n\nGenerated docs."

    def test_file_not_found_shows_error(self, runner, temp_storage):
        """Test that missing file shows error."""
        result = runner.invoke(app, ["generate", "nonexistent.py"])

        assert result.exit_code == 2
        assert "File not found" in result.output

    def test_empty_file_shows_error(self, runner, temp_storage, tmp_path):
        """Test that empty file shows error."""
        source = tmp_path / "empty.py"
        source.write_text("")

        result = runner.invoke(app, ["generate", str(source)])

        assert result.exit_code == 2
        assert "File is empty" in result.output

    def test_saves_entry_to_storage(self, runner, temp_storage, mock_llm, tmp_path):
        """Test that generation saves an entry to storage."""
        source = tmp_path / "example.py"
        source.write_text("def hello(): pass")

        runner.invoke(app, ["generate", str(source)])

        data = json.loads(temp_storage.read_text())
        assert len(data["entries"]) == 1
        assert data["entries"][0]["source_file"] == str(source)
        assert data["entries"][0]["status"] == "current"

    def test_custom_output_dir(self, runner, temp_storage, mock_llm, tmp_path):
        """Test generating docs to a custom output directory."""
        source = tmp_path / "example.py"
        source.write_text("def hello(): pass")
        custom_dir = tmp_path / "custom_docs"

        result = runner.invoke(app, ["generate", str(source), "-o", str(custom_dir)])

        assert result.exit_code == 0
        assert (custom_dir / "example.md").exists()
