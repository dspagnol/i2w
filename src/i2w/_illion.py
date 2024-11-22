from ._constants import Gender
from ._localization import Localization
from .exception import InternalError


# From https://en.wikipedia.org/wiki/Names_of_large_numbers
#  ----------------------------------------------------------
# | < 10   | >= 10                                           |
# |-------- -------------------------------------------------|
# | units  | units       | tens            | hundreds        |
# |-------- ------------- ----------------- -----------------|
# | mi     | un          | n  deci         | nx centi        |
# | bi     | duo         | ms viginti      | n  ducenti      |
# | tri    | tre      s  | ns triginta     | ns trecenti     |
# | quadri | quattuor    | ns quadraginta  | ns quadringenti |
# | quinti | quin        | ns quinquaginta | ns quingenti    |
# | sexti  | se       sx | n  sexaginta    | n  sescenti     |
# | septi  | septe    mn | n  septuaginta  | n  septingenti  |
# | octi   | octo        | mx octoginta    | mx octingenti   |
# | noni   | nove     mn |    nonaginta    |    nongenti     |
#  ----------------------------------------------------------


class IllionConverter:

    def __init__(self, localization: Localization) -> None:
        self.__localization = localization

    def to_words(self, n: int, step: int, plural: bool, gender: Gender) -> str:
        if n < 0:
            raise InternalError(f'negative n not supported: {n}')
        reversed_base_word_parts: list[str] = []
        while n:
            reversed_base_word_parts.append(self.__get_base_word(n=n%1000))
            n //= 1000
        infix_base: str = self.__localization.large_number_infix_base
        prefix: str = infix_base.join(reversed(reversed_base_word_parts))
        use_thousand: bool = self.__use_thousand(step=step)
        infix_suffix: str = self.__localization.large_number_infix_suffix
        suffix: str = self.__get_suffix(step=(0 if use_thousand else step), plural=plural)
        words: str = infix_suffix.join([prefix, suffix])
        if use_thousand:
            thousand: str = self.__localization.thousand
            word_separator: str = self.__localization.word_separator
            words = word_separator.join([thousand, words])
        return words

    def __use_thousand(self, step: int) -> bool:
        return step > 0 and self.__localization.large_number_thousand_replaces_ard_suffix

    def __get_base_word(self, n: int) -> str:
        base_word_parts: list[str] = []
        if n < 10:
            base_word_parts.append(self.__get_prefix_n_lt_10(index=n))
        else:
            units: int = n % 10
            t: int = n // 10 % 10
            h: int = n // 100
            liaison: str | None = None
            if units:
                liaison = self.__get_liaison(units, t, h)
            use_alternative_prefix: bool = not liaison and self.__localization.large_number_no_liaison_use_alt_unit_prefix
            if use_alternative_prefix:
                base_word_parts.append(self.__localization.large_number_units_alt(index=units))
            else:
                base_word_parts.append(self.__localization.large_number_units(index=units))
            if liaison:
                base_word_parts.append(liaison)
            base_word_parts.append(
                    self.__localization.large_number_tens(index=t) +
                    self.__localization.large_number_tens_i_a(index=t)[0 if h == 0 else 1]
                    )
            base_word_parts.append(self.__localization.large_number_hundreds(index=h))
        return ''.join(base_word_parts)

    def __get_prefix_n_lt_10(self, index: int) -> str:
        return self.__localization.large_number_prefixes_n_lt_10(index=index)

    def __get_liaison(self, units: int, tens: int, hundreds: int) -> str | None:
        result: str | None = None
        liaisons: list = []
        if tens:
            liaisons = self.__localization.large_number_tens_liaison(index=tens)
        elif hundreds:
            liaisons = self.__localization.large_number_hundreds_liasion(index=hundreds)
        for liaison in self.__localization.large_number_units_liaison(index=units):
            if units == 3 and 'x' in liaisons:
                result = 's' # exception to the rule for unit 3: s and x match
            if liaison in liaisons:
                result = liaison
            if result:
                break
        return result

    def __get_suffix(self, step: int, plural: bool) -> str:
        if plural:
            return self.__localization.large_number_suffixes_plural(index=step)
        else:
            return self.__localization.large_number_suffixes(index=step)
