"""cli test fixtures."""
import os

import pytest
from click.testing import CliRunner
from pytest_mock import MockFixture


@pytest.fixture
def mock_click() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.fixture
def mock_checks_network(mocker: MockFixture):
    """Fixture for mocking checks.network."""
    return mocker.patch("website_checker.checks.network")


@pytest.fixture
def mock_checks_health(mocker: MockFixture):
    """Fixture for mocking checks.health."""
    return mocker.patch("website_checker.checks.health")


@pytest.fixture
def mock_checks_latency(mocker: MockFixture):
    """Fixture for mocking checks.latency."""
    return mocker.patch("website_checker.checks.latency")


@pytest.fixture(autouse=True, scope="session")
def mock_envvars():
    """Mock environment variables."""
    os.environ["CHECK_NETWORK_URLS"] = "https://google.com https://wikipedia.org"
    os.environ["CHECK_HEALTH_URLS"] = "https://google.com"
    os.environ["CHECK_LATENCY_URLS"] = "https://google.com"
    yield
    del os.environ["CHECK_NETWORK_URLS"]
    del os.environ["CHECK_HEALTH_URLS"]
    del os.environ["CHECK_LATENCY_URLS"]
