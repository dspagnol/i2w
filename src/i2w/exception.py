"""Exception classes for i2w conversion operations.

Defines the exception hierarchy used throughout i2w for various error conditions
including localization, validation, and range errors.
"""

import sys


class I2WError(Exception):
    """Base exception class for all i2w-related errors."""

    def __init__(self, *args: object) -> None:
        """Initialize exception with message arguments."""
        super().__init__(*args)


# Backward compatibility alias
I2WException = I2WError


class LocalizationError(I2WError):
    """Raised when an invalid or unsupported locale is provided."""

    def __init__(self, locale: str) -> None:
        """Initialize exception with invalid locale.

        Args:
            locale: The invalid locale string that was provided.
        """
        super().__init__(f"invalid locale: '{locale}'")
        self._locale = locale


class InvalidInteger(I2WError):
    """Raised when a string cannot be parsed as a valid integer."""

    def __init__(self, s: str) -> None:
        """Initialize exception with invalid string.

        Args:
            s: The string that could not be parsed as an integer.
        """
        super().__init__(f"invalid integer: '{s}'")
        self._s = s


class IntegerOutOfRange(I2WError):
    """Raised when an integer exceeds the system's maximum string digit limit."""

    def __init__(self) -> None:
        """Initialize exception for exceeding maximum string digits."""
        max_digits: int = sys.get_int_max_str_digits()
        super().__init__(
            f"number is beyond the maximum supported digits: '{max_digits}'",
        )


class IntegerOutOfBoundsError(I2WError):
    """Raised when an integer is outside the supported range for a conversion."""

    def __init__(self, min_value: int, max_value: int, n: int) -> None:
        """Initialize exception for integer out of bounds.

        Args:
            min_value: The minimum allowed value.
            max_value: The maximum allowed value.
            n: The value that was out of bounds.
        """
        self._min = min_value
        self._max = max_value
        self._n = n
        super().__init__(
            f"number should be between '{self._min}' and '{self._max}': '{self._n}'",
        )


class MaxStrDigitsOutOfBoundsError(I2WError):
    """Raised when max_str_digits argument is outside the supported range."""

    def __init__(self, min_value: int, max_value: int, n: int) -> None:
        """Initialize exception for max_str_digits out of bounds.

        Args:
            min_value: The minimum allowed value.
            max_value: The maximum allowed value.
            n: The value that was out of bounds.
        """
        self._min = min_value
        self._max = max_value
        self._n = n
        msg = (
            f"maximum str digits should be between "
            f"'{self._min}' and '{self._max}': '{self._n}'"
        )
        super().__init__(msg)


class InternalError(I2WError):
    """Raised when an internal i2w error occurs (indicates a bug)."""
