"""Logging utilities."""

import logging
from typing import Any


class Log:
    """Logger wrapper.

    Provides structured logging with keyword arguments support.

    Attributes:
        _logger: Underlying Python logger instance
    """

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    @staticmethod
    def create(service: str) -> "Log":
        """Create a logger for a service.

        Args:
            service: Service name for the logger

        Returns:
            Log instance for the service
        """
        logger = logging.getLogger(f"langcode.{service}")
        return Log(logger)

    def _log(self, level: str, message: str, **kwargs: Any):
        """Internal logging method.

        Args:
            level: Log level name (info, warning, error, debug)
            message: Log message
            **kwargs: Additional context to include in log
        """
        log_method = getattr(self._logger, level)
        if kwargs:
            log_method(f"{message} {kwargs}")
        else:
            log_method(message)

    def info(self, message: str, **kwargs: Any):
        """Log info message.

        Args:
            message: Log message
            **kwargs: Additional context
        """
        self._log("info", message, **kwargs)

    def warn(self, message: str, **kwargs: Any):
        """Log warning message.

        Args:
            message: Log message
            **kwargs: Additional context
        """
        self._log("warning", message, **kwargs)

    def error(self, message: str, **kwargs: Any):
        """Log error message.

        Args:
            message: Log message
            **kwargs: Additional context
        """
        self._log("error", message, **kwargs)

    def debug(self, message: str, **kwargs: Any):
        """Log debug message.

        Args:
            message: Log message
            **kwargs: Additional context
        """
        self._log("debug", message, **kwargs)
