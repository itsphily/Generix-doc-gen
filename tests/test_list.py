"""Tests for the list command."""

from docgen.commands import app


class TestList:
    """Test suite for list command."""

    def test_shows_all_entries(self, runner, sample_data):
        """Test that all entries are shown."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "utils.py" in result.output
        assert "main.py" in result.output

    def test_filters_by_current_status(self, runner, sample_data):
        """Test filtering by current status."""
        result = runner.invoke(app, ["list", "--status", "current"])

        assert result.exit_code == 0
        assert "utils.py" in result.output
        assert "main.py" not in result.output

    def test_filters_by_stale_status(self, runner, sample_data):
        """Test filtering by stale status."""
        result = runner.invoke(app, ["list", "--status", "stale"])

        assert result.exit_code == 0
        assert "main.py" in result.output
        assert "utils.py" not in result.output

    def test_short_flag(self, runner, sample_data):
        """Test using short -s flag."""
        result = runner.invoke(app, ["list", "-s", "current"])

        assert result.exit_code == 0
        assert "utils.py" in result.output

    def test_invalid_status_shows_error(self, runner, temp_storage):
        """Test that invalid status shows error."""
        result = runner.invoke(app, ["list", "--status", "invalid"])

        assert result.exit_code == 2
        assert "Invalid status" in result.output

    def test_empty_list_shows_warning(self, runner, temp_storage):
        """Test that empty list shows warning."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "No documentation entries found" in result.output

    def test_case_insensitive_status(self, runner, sample_data):
        """Test that status filter is case insensitive."""
        result = runner.invoke(app, ["list", "--status", "CURRENT"])

        assert result.exit_code == 0
        assert "utils.py" in result.output
