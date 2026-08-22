"""Logging filter for debug level filtering and formatting.

Provides a filter class that conditionally logs debug messages based on
verbosity levels and applies indentation based on debug depth.
"""

import logging
import typing


class LoggingDebugFilter(logging.Filter):
    """Filter DEBUG messages by verbosity level and add debug-level indentation."""

    def __init__(self, debug_level: int) -> None:
        """Initialize the debug filter with a verbosity level.

        Args:
            debug_level: The debug verbosity level (0-3).
        """
        self.__debug_level = debug_level

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter a log record based on debug level.

        Args:
            record: The log record to filter.

        Returns:
            True if the record should be logged, False otherwise.
        """
        to_be_logged: bool = True
        if record.levelno == logging.DEBUG:
            if not hasattr(record, "debug_level"):
                record.debug_level = 0  # type: ignore
            debug_level_value: int = typing.cast(int, getattr(record, "debug_level", 0))
            to_be_logged = debug_level_value <= self.__debug_level
            record.msg = ("  " * debug_level_value) + record.msg  # type: ignore
        return to_be_logged
