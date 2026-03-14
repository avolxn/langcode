"""Logging utilities."""

import logging
from typing import Any


class Log:
    """Logger wrapper."""

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    @staticmethod
    def create(service: str) -> "Log":
        """Create a logger for a service."""
        logger = logging.getLogger(f"langcode.{service}")
        return Log(logger)

    def info(self, message: str, **kwargs: Any):
        """Log info message."""
        if kwargs:
            self._logger.info(f"{message} {kwargs}")
        else:
            self._logger.info(message)

    def warn(self, message: str, **kwargs: Any):
        """Log warning message."""
        if kwargs:
            self._logger.warning(f"{message} {kwargs}")
        else:
            self._logger.warning(message)

    def error(self, message: str, **kwargs: Any):
        """Log error message."""
        if kwargs:
            self._logger.error(f"{message} {kwargs}")
        else:
            self._logger.error(message)

    def debug(self, message: str, **kwargs: Any):
        """Log debug message."""
        if kwargs:
            self._logger.debug(f"{message} {kwargs}")
        else:
            self._logger.debug(message)
