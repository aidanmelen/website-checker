"""Helper functions."""
import datetime
import logging
import sys

from structlog import wrap_logger
from structlog.processors import JSONRenderer
from structlog.stdlib import add_logger_name
from structlog.stdlib import filter_by_level


def _add_timestamp(_, __, event_dict):
    """Add UTC ISO formatted timestamp to log event."""
    event_dict["timestamp"] = datetime.datetime.utcnow().isoformat()
    return event_dict


def get_logger(name, log_level):
    """Get JSON logger.

    Args:
        name: The logger name.
        log_level: The log level.

    Returns:
        A logger.
    """
    logging.basicConfig(
        level=log_level, stream=sys.stdout, format="%(message)s"
    )

    if log_level == "DEBUG":  # pragma: no cover
        processors = [
            filter_by_level,
            add_logger_name,
            _add_timestamp,
            JSONRenderer(indent=1, sort_keys=True),
        ]
    else:
        processors = [
            filter_by_level,
            add_logger_name,
            _add_timestamp,
            JSONRenderer(sort_keys=True),
        ]

    return wrap_logger(
        logging.getLogger(name),
        processors=processors,
    )
