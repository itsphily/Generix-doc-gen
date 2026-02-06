"""Tests for the update command (bad practices demo)."""

from unittest.mock import MagicMock, patch

from docgen.commands import app


@patch("openai.OpenAI")
class TestUpdate:
    """Test suite for update command.

    Note: We patch OpenAI directly because update.py imports it inline
    (one of its bad practices) instead of using llm.py.
    """

    def test_update_exits_with_wrong_code(self, mock_openai, runner, temp_storage, tmp_path):
        """Test that update uses wrong exit code (demonstrates the bug)."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "# Mock docs"
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        source = tmp_path / "example.py"
        source.write_text("def hello(): pass")

        result = runner.invoke(app, ["update", str(source)])

        # BUG: exits with 1 instead of 0 on success
        assert result.exit_code == 1

    def test_update_uses_print_instead_of_display(self, mock_openai, runner, temp_storage, tmp_path):
        """Test that update uses print() instead of display module."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "# Mock docs"
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        source = tmp_path / "example.py"
        source.write_text("def hello(): pass")

        result = runner.invoke(app, ["update", str(source)])

        # BAD: output comes from print(), not display module
        assert "Updating docs for" in result.output
        assert "Done!" in result.output
