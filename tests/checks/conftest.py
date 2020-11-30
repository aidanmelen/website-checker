"""checks test fixtures."""
import datetime

import pytest
from pytest_mock import MockFixture


@pytest.fixture
def mock_requests_get_happy_path(mocker: MockFixture):
    """Fixture for mocking requests.get happy path."""
    mock = mocker.patch("requests.get")
    mock.return_value.ok = True
    mock.return_value.__enter__.return_value.elapsed = datetime.timedelta(milliseconds=100)
    return mock


@pytest.fixture
def mock_requests_get_sad_path(mocker: MockFixture):
    """Fixture for mocking requests.get sad path."""
    mock = mocker.patch("requests.get")
    mock.return_value.ok = False
    mock.return_value.__enter__.return_value.elapsed = datetime.timedelta(milliseconds=400)
    return mock
