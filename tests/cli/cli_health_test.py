"""Test cases for the console module."""
import logging

from website_checker import cli


def test_health_subcommand_prints_usage(mock_click):
    """It prints the usage message with subcommand options."""
    result = mock_click.invoke(cli.main, ["health", "--help"])
    assert "Usage: check health [OPTIONS]" in result.output
    assert "--url" in result.output
    assert "--timeout" in result.output


def test_health_subcommand_invokes_health_happy_path(
    mock_click, mock_checks_health, caplog
):
    """It invokes health check and logs out pass."""
    # arrange
    mock_url = "https://google.com"
    mock_checks_health.return_value = True

    # act
    with caplog.at_level(logging.INFO):
        mock_click.invoke(cli.main, ["health", "--url", mock_url])

    # assert
    mock_checks_health.assert_called_once_with(url=mock_url, timeout=5)
    assert "pass" in caplog.text


def test_health_subcommand_invokes_health_sad_path(
    mock_click, mock_checks_health, caplog
):
    """It invokes health check and logs out failure."""
    mock_checks_health.return_value = False
    with caplog.at_level(logging.INFO):
        mock_click.invoke(cli.main, ["health", "--url", "https://google.com"])
    assert mock_checks_health.called
    assert "fail" in caplog.text


def test_health_subcommand_raises_on_exception(
    mock_click, mock_checks_health, caplog
):
    """It invokes health check and logs out exception."""
    mock_checks_health.side_effect = Exception("unknown error")
    with caplog.at_level(logging.INFO):
        mock_click.invoke(cli.main, ["health", "--url", "https://google.com"])
    assert '"error": "Exception(\'unknown error\')"' in caplog.text
