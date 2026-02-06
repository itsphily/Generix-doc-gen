"""Tests for the check command."""

from docgen.commands import app


class TestCheck:
    """Test suite for check command."""

    def test_file_not_found_shows_error(self, runner, temp_storage):
        """Test that missing file shows error."""
        result = runner.invoke(app, ["check", "nonexistent.py"])

        assert result.exit_code == 2
        assert "File not found" in result.output

    def test_no_docs_found_shows_error(self, runner, temp_storage, tmp_path):
        """Test that file with no docs shows error."""
        source = tmp_path / "example.py"
        source.write_text("def hello(): pass")

        result = runner.invoke(app, ["check", str(source)])

        assert result.exit_code == 2
        assert "No documentation found" in result.output
