import enum


type TerritoryDict[T] = dict[str | None, T]
type LanguageDict[T] = dict[str | None, TerritoryDict[T]]


class Enum(enum.Enum):

    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> int:
        return count + 1
