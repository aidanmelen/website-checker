"""Test suite for the check health."""
from website_checker import checks


def test_health_check_with_200_response_code(mock_requests_get_happy_path):
    """Check passes when HTTP response is OK."""
    # arrange
    mock_url = "https://google.com"
    mock_timeout = 5

    # act
    result = checks.health(mock_url, mock_timeout)

    # assert
    mock_requests_get_happy_path.assert_called_once_with(mock_url, timeout=mock_timeout)
    assert result


def test_health_check_with_bad_response_code(mock_requests_get_sad_path):
    """Check passes when HTTP response is not OK."""
    mock_url = "https://google.com"
    mock_timeout = 5
    result = checks.health(mock_url, mock_timeout)
    mock_requests_get_sad_path.assert_called_once_with(mock_url, timeout=mock_timeout)
    assert not result
