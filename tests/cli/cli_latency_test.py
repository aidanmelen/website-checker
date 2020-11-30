"""Test cases for the console module."""
import logging

from website_checker import cli


def test_latency_subcommand_prints_usage(mock_click):
    """It prints the usage message with subcommand options."""
    result = mock_click.invoke(cli.main, ["latency", "--help"])
    assert "Usage: check latency [OPTIONS]" in result.output
    assert "--url" in result.output
    assert "--timeout" in result.output
    assert "--threshold" in result.output


def test_latency_subcommand_invokes_latency_happy_path(
    mock_click, mock_checks_latency, caplog
):
    """It invokes latency check and logs out pass."""
    # arrange
    mock_checks_latency.return_value = True

    # act
    with caplog.at_level(logging.INFO):
        mock_click.invoke(cli.main, ["latency", "--url", "https://google.com"])

    # assert
    assert mock_checks_latency.called
    assert "pass" in caplog.text


def test_latency_subcommand_invokes_latency_sad_path(
    mock_click, mock_checks_latency, caplog
):
    """It invokes latency check and logs out failure."""
    mock_checks_latency.return_value = False
    with caplog.at_level(logging.INFO):
        mock_click.invoke(cli.main, ["latency", "--url", "https://google.com"])
    assert mock_checks_latency.called
    assert "fail" in caplog.text


def test_latency_subcommand_raises_on_exception(
    mock_click, mock_checks_latency, caplog
):
    """It invokes latency check and logs out exception."""
    mock_checks_latency.side_effect = Exception("unknown error")
    with caplog.at_level(logging.INFO):
        mock_click.invoke(cli.main, ["latency", "--url", "https://google.com"])
    assert '"error": "Exception(\'unknown error\')"' in caplog.text
    assert "fail" in caplog.text
