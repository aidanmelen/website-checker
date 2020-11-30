"""Test cases for the console module."""
import logging

from website_checker import cli


def test_network_check_prints_usage(mock_click):
    """It prints the usage message with check options."""
    result = mock_click.invoke(cli.main, ["network", "--help"])
    assert "Usage: check network [OPTIONS]" in result.output
    assert "--url" in result.output
    assert "--timeout" in result.output


def test_network_check_invokes_network_happy_path(
    mock_click, mock_checks_network, caplog
):
    """It invokes network check and logs out pass."""
    # arrange
    mock_checks_network.return_value = True

    # act
    with caplog.at_level(logging.INFO):
        mock_click.invoke(cli.main, ["network", "--url", "https://google.com"])

    # assert
    assert mock_checks_network.called
    assert "pass" in caplog.text


def test_network_check_invokes_network_sad_path(
    mock_click, mock_checks_network, caplog
):
    """It invokes network check and logs out failure."""
    mock_checks_network.return_value = False
    with caplog.at_level(logging.INFO):
        mock_click.invoke(cli.main, ["network", "--url", "https://google.com"])
    assert mock_checks_network.called
    assert "fail" in caplog.text


def test_network_check_fails_on_exception(
    mock_click, mock_checks_network, caplog
):
    """It invokes network check and logs out exception."""
    mock_checks_network.side_effect = Exception("unknown error")
    with caplog.at_level(logging.INFO):
        mock_click.invoke(cli.main, ["network", "--url", "https://google.com"])
    assert '"error": "Exception(\'unknown error\')"' in caplog.text
    assert "fail" in caplog.text
