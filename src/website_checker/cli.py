"""Command-line interface."""
import click

from . import checks
from . import helpers


def _run_check(name, **kwargs):
    """Run a website check by name and log output.

    Args:
        name: The name of the website check to run.
        kwargs: keyword arguments to pass to the website check.

    Returns:
        None
    """
    event = {"check": name, "input": kwargs, "output": "fail"}

    try:
        result = getattr(checks, name)(**kwargs)
        event["output"] = "pass" if result else "fail"
        logger.info(event)
    except Exception as error:
        event["error"] = error
        logger.error(event)

    return None


@click.group(name="check")
@click.option("--debug/--no-debug", help="Toggle debug mode.")
@click.version_option()
def main(debug):
    """A simple python application for running checks against websites."""
    global logger
    log_level = "DEBUG" if debug else "INFO"
    logger = helpers.get_logger("website-checker", log_level)


# fmt: off
@main.command()
@click.option("urls", "--url", "-u", multiple=True, default=[None], show_default=True, help="The url to check.")  # noqa: B950
@click.option("--timeout", "-t", default=5, show_default=True, help="The HTTP request timeout in seconds.")       # noqa: B950
def network(urls, timeout):
    """Check website network connectivity."""
    for url in urls:
        _run_check("network", url=url, timeout=timeout)


# fmt: off
@main.command()
@click.option("urls", "--url", "-u", multiple=True, default=[None], show_default=True, help="The url to check.")  # noqa: B950
@click.option("--timeout", "-t", default=5, show_default=True, help="The HTTP request timeout in seconds.")       # noqa: B950
def health(urls, timeout):
    """Check website health."""
    for url in urls:
        _run_check("health", url=url, timeout=timeout)


# fmt: off
@main.command()
@click.option("urls", "--url", "-u", multiple=True, default=[None], show_default=True, help="The url to check.")   # noqa: B950
@click.option("--timeout", "-t", default=5, show_default=True, help="The HTTP request timeout in seconds.")        # noqa: B950
@click.option("--threshold", "-T", default=500, show_default=True, help="The latency threshold in milliseconds.")  # noqa: B950
def latency(urls, timeout, threshold):
    """Check website latency."""
    for url in urls:
        _run_check("latency", url=url, timeout=timeout, threshold=threshold)


def cli():
    """A wrapper function to pass auto_envvar_prefix to main entrypoint.

    The auto_envvar_prefix parameter needs to be passed to the script that is invoked.
    https://click.palletsprojects.com/en/7.x/options/#values-from-environment-variables
    """
    main(auto_envvar_prefix="CHECK")  # pragma: no cover


if __name__ == "__main__":
    cli()  # pragma: no cover
