"""Test suite for the check latency."""
from website_checker import checks


def test_latency_check_passes_on_happy_path(mock_requests_get_happy_path):
    """Check passes when latency is less than the threshold."""
    # arrange
    mock_url = "https://google.com"
    mock_timeout = 5
    mock_threshold = 300

    # act
    result = checks.latency(mock_url, mock_timeout, mock_threshold)

    # assert
    mock_requests_get_happy_path.assert_called_once_with(
        mock_url, timeout=mock_timeout
    )
    assert result


def test_latency_check_fails_on_sad_path(mock_requests_get_sad_path):
    """Check fails when latency is greater than the threshold."""
    mock_url = "https://google.com"
    mock_timeout = 5
    mock_threshold = 300
    result = checks.latency(mock_url, mock_timeout, mock_threshold)
    mock_requests_get_sad_path.assert_called_once_with(
        mock_url, timeout=mock_timeout
    )
    assert not result
