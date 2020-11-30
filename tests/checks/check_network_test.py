"""Test suite for the check network."""
from unittest import mock

import pytest
from requests.exceptions import ConnectTimeout

from website_checker import checks

# from unittest.mock import call


def test_network_check_can_connect():
    """Check passes when connection is established."""
    # arrange
    mock_url = "https://google.com"
    mock_timeout = 5

    # act and assert
    with mock.patch("requests.head") as mock_requests_head:
        result = checks.network(mock_url, mock_timeout)

        # call_args example
        # args, kwargs = mock_requests_head.call_args
        # assert mock_url in args
        # assert {"timeout": mock_timeout} == kwargs

        mock_requests_head.assert_called_once_with(mock_url, timeout=mock_timeout)
        assert result


def test_network_check_cannot_connect():
    """Check fails when connection is not established."""
    mock_url = "https://google.com"
    mock_timeout = 5
    with mock.patch("requests.head") as mock_requests_head:
        mock_requests_head.side_effect = ConnectTimeout
        result = checks.network(mock_url, mock_timeout)

        # assert_has_calls example
        # mock_requests_head.assert_has_calls(
        #     [call(mock_url, timeout=mock_timeout)],
        #     any_order=False,
        # )

        mock_requests_head.assert_called_once_with(mock_url, timeout=mock_timeout)
        assert not result


@mock.patch("requests.head", side_effect=Exception)
def test_network_check_raises_exception_on_sad_path(mock_requests_head):
    """Check raises `Exception` with bad inputs."""
    mock_url = "spaghetti"
    mock_timeout = "meatballs"
    with pytest.raises(Exception):
        checks.network(mock_url, timeout=mock_timeout)
