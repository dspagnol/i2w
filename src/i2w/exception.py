import sys


# TODO Make me abstract.
class I2WException(Exception):

    def __init__(self, *args):
        super().__init__(*args)


class LocalizationError(I2WException):

    def __init__(self, locale: str):
        super().__init__(f"invalid locale: '{locale}'")
        self._locale = locale


class InvalidInteger(I2WException):

    def __init__(self, s: str):
        super().__init__(f"invalid integer: '{s}'")
        self._s = s


class IntegerOutOfRange(I2WException):

    def __init__(self) -> None:
        max_digits: int = sys.get_int_max_str_digits()
        super().__init__(f"number is beyond the maximum supported digits: '{max_digits}'")


class IntegerOutOfBoundsError(I2WException):

    def __init__(self, min: int, max: int, n: int):
        self._min = min
        self._max = max
        self._n = n
        super().__init__(f"number should be between '{self._min}' and '{self._max}': '{self._n}'")


class MaxStrDigitsOutOfBoundsError(I2WException):

    def __init__(self, min: int, max: int, n: int):
        self._min = min
        self._max = max
        self._n = n
        super().__init__(f"maximum str digits should be between '{self._min}' and '{self._max}': '{self._n}'")


class InternalError(I2WException):
    pass
