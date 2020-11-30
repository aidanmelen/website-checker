"""Test cases for the console module."""
from website_checker import cli


def test_main_command_succeeds(mock_click):
    """It exits with a status code of zero."""
    result = mock_click.invoke(cli.main)
    assert result.exit_code == 0


def test_main_command_prints_usage(mock_click):
    """It prints the usage message with group options and subcommands."""
    result = mock_click.invoke(cli.main)
    assert "Usage: check [OPTIONS] COMMAND [ARGS]" in result.output
    assert "--debug / --no-debug  Toggle debug mode." in result.output
    assert "network" in result.output
    assert "health" in result.output
    assert "latency" in result.output
