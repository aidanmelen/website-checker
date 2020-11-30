"""URL checks."""
import datetime

import requests


def network(url, timeout):
    """Check the website network connectivity.

    Args:
        url: The URL to check.
        timeout: The request timeout.

    Returns:
        True on pass and False on failure.
    """
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


def health(url, timeout):
    """Check the website health.

    Args:
        url: The URL to check.
        timeout: The request timeout.

    Returns:
        True on pass and False on failure.
    """
    return requests.get(url, timeout=timeout).ok


def latency(url, timeout, threshold):
    """Check the website latency.

    Args:
        url: The URL to check.
        timeout: The request timeout.
        threshold: The latency threshold.

    Returns:
        True on pass and False on failure.
    """
    with requests.get(url, timeout=timeout) as response:
        return response.elapsed < datetime.timedelta(milliseconds=threshold)
