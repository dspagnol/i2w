"""Exception classes for i2w conversion operations.

Defines the exception hierarchy used throughout i2w for various error conditions
including localization, validation, and range errors.
"""

import sys


class I2WException(Exception):
    """Base exception class for all i2w-related errors."""

    def __init__(self, *args):
        """Initialize exception with message arguments."""
        super().__init__(*args)


class LocalizationError(I2WException):
    """Raised when an invalid or unsupported locale is provided."""

    def __init__(self, locale: str):
        """Initialize exception with invalid locale.

        Args:
            locale: The invalid locale string that was provided.
        """
        super().__init__(f"invalid locale: '{locale}'")
        self._locale = locale


class InvalidInteger(I2WException):
    """Raised when a string cannot be parsed as a valid integer."""

    def __init__(self, s: str):
        """Initialize exception with invalid string.

        Args:
            s: The string that could not be parsed as an integer.
        """
        super().__init__(f"invalid integer: '{s}'")
        self._s = s


class IntegerOutOfRange(I2WException):
    """Raised when an integer exceeds the system's maximum string digit limit."""

    def __init__(self) -> None:
        """Initialize exception for exceeding maximum string digits."""
        max_digits: int = sys.get_int_max_str_digits()
        super().__init__(
            f"number is beyond the maximum supported digits: '{max_digits}'"
        )


class IntegerOutOfBoundsError(I2WException):
    """Raised when an integer is outside the supported range for a conversion."""

    def __init__(self, min: int, max: int, n: int):
        """Initialize exception for integer out of bounds.

        Args:
            min: The minimum allowed value.
            max: The maximum allowed value.
            n: The value that was out of bounds.
        """
        self._min = min
        self._max = max
        self._n = n
        super().__init__(
            f"number should be between '{self._min}' and '{self._max}': '{self._n}'"
        )


class MaxStrDigitsOutOfBoundsError(I2WException):
    """Raised when max_str_digits argument is outside the supported range."""

    def __init__(self, min: int, max: int, n: int):
        """Initialize exception for max_str_digits out of bounds.

        Args:
            min: The minimum allowed value.
            max: The maximum allowed value.
            n: The value that was out of bounds.
        """
        self._min = min
        self._max = max
        self._n = n
        msg = (
            f"maximum str digits should be between "
            f"'{self._min}' and '{self._max}': '{self._n}'"
        )
        super().__init__(msg)


class InternalError(I2WException):
    """Raised when an internal i2w error occurs (indicates a bug)."""

    pass
