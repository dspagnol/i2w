"""Type aliases and custom enum base class for i2w.

Defines generic type aliases for language and territory-based dictionaries,
and provides a custom Enum base class with auto-incrementing values.
"""

import enum

type TerritoryDict[T] = dict[str | None, T]
type LanguageDict[T] = dict[str | None, TerritoryDict[T]]


class Enum(enum.Enum):
    @staticmethod
    def _generate_next_value_(
        _name: str,
        _start: int,
        count: int,
        _last_values: object,
    ) -> int:
        return count + 1
