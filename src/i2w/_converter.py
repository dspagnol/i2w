import abc
import collections.abc
import logging
import typing

from ._constants import ConverterImplTypeValue
from ._constants import Gender
from ._illion import IllionConverter
from ._localization import Localization
from ._logging import logger
from ._logging import logger_d1
from ._logging import logger_d2
from ._logging import logger_d3
from .exception import InternalError


class ConverterImpl(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, localization: Localization): ...

    @abc.abstractmethod
    def to_words(self, i: int) -> str: ...


class ConverterRegistrar:

    @staticmethod
    def register(type_id: ConverterImplTypeValue, type: typing.Type[ConverterImpl]) -> None:
        ConverterRegistrar.__registered_types[type_id] = type

    @staticmethod
    def get_class(type_id: ConverterImplTypeValue) -> typing.Type[ConverterImpl]:
        return ConverterRegistrar.__registered_types[type_id]

    __registered_types: dict[ConverterImplTypeValue, typing.Type[ConverterImpl]] = {}


class ScaleConverterImpl(ConverterImpl):

    def __init__(self, localization: Localization, name: str, slope: int, intercept: int):
        self.__localization = localization
        self.__name = name
        self.__slope = slope
        self.__intercept = intercept

    def to_words(self, i: int) -> str:

        logger.debug('processing %d', i)

        word_list: list[str] = []
        is_negative: bool = False

        if i < 0:
            i = abs(i)
            is_negative = True

        if i == 0:
            word_list = [self.__localization.get_name_from_cache(i=0)]

        else:
            reversed_word_list: list[str] = []
            step: int = 0
            n: int = self.__get_first_n()
            max_step: int = self.__get_n_steps() - 1
            conjunction_appended: bool = False

            spc: ScaledPeriodConverter = ScaledPeriodConverter(self.__localization, exponent_calculator=self.__calculate_exponent)

            # Input "i" is converted to str for performances purposes.
            # If "i" is too large, the "a = i % 1000" and "i //= 1000" operations are
            # slow due to memory copies. As an example: 300k-digit integer is
            # 80 times slower than string implementation. In the implementation below,
            # require large sequence of bytes never copied over and over.
            i_str: str = str(i)

            i2: int = len(i_str)
            while i2 > 0:

                # equivalent to "a = i % 1000"
                i1: int = i2 - 3
                if i1 < 0:
                    i1 = 0
                a: int = int(i_str[i1:i2]) # extract the next 3 characters (backward) and make int.

                # equivalent to "i //= 1000"
                i2 -= 3

                if a:
                    reversed_word_list.append(spc.to_words(a=a, n=n, step=step))
                    if not conjunction_appended and i1 and spc.is_conjunction_prepended_candidate(a=a):
                        reversed_word_list.append(self.__localization.and_)
                        conjunction_appended = True

                if step == max_step:
                    n += 1
                    step = 0
                else:
                    step += 1

            word_list.extend(reversed(reversed_word_list))

        words: str = self.__localization.word_separator.join(word_list)
        if is_negative:
            words = f'{self.__localization.minus} {words}'

        return words

    def get_name(self) -> str:
        return self.__name

    def __get_n_steps(self) -> int:
        return self.__slope

    def __get_first_n(self) -> int:
        # 3*(a*n+b) = 0  ==>  n = -b/a
        return - self.__intercept // self.__slope

    def __calculate_exponent(self, n: int, step: int) -> int:
        return 3 * (self.__slope * n + self.__intercept + step)


class ShortScaleConverterImpl(ScaleConverterImpl):

    def __init__(self, localization: Localization):
        # short scale: 10 ** ((1 * n + 1) * 3)
        super().__init__(localization=localization, name='short', slope=1, intercept=1)


class LongScaleConverterImpl(ScaleConverterImpl):

    def __init__(self, localization: Localization):
        # long scale:  10 ** ((2 * n + 0) * 3)
        super().__init__(localization=localization, name='long', slope=2, intercept=0)


ConverterRegistrar.register(type_id=ConverterImplTypeValue.SHORT_SCALE, type=ShortScaleConverterImpl)
ConverterRegistrar.register(type_id=ConverterImplTypeValue.LONG_SCALE, type=LongScaleConverterImpl)


class ScaledPeriodConverter:

    def __init__(
            self,
            localization: Localization,
            exponent_calculator: collections.abc.Callable[[int, int], int],
            ) -> None:
        self.__localization = localization
        self.__calculate_exponent = exponent_calculator
        self.__period: PeriodConverter = PeriodConverter(localization=self.__localization)
        self.__illion: IllionConverter = IllionConverter(localization=self.__localization)

    def is_conjunction_prepended_candidate(self, a: int) -> bool:
        is_candidate: bool = False
        if self.__localization.conjunction_before_last_non_0_period:
            tens_units: int = a % 100
            hundreds: int = a // 100
            is_candidate = (hundreds == 0) ^ (tens_units == 0)
            logger_d2.debug('conjunction prepended candidate: %d00+0%d => %s', hundreds, tens_units, is_candidate)
        return is_candidate

    def to_words(self, a: int, n: int, step: int) -> str:
    
        reversed_words: list[str] = []
        has_thousand: bool = False
        is_large_number: bool = n > 0
        if n > 0:
            logger_d1.debug('illion: n=%d, step=%d', n, step)
            has_thousand = self.__has_thousand(step)
            is_plural = not self.__localization.large_number_invariable and (a > 1 or has_thousand)
            reversed_words.append(self.__illion.to_words(n=n, step=step, plural=is_plural, gender=Gender.MALE))
        elif self.__is_thousand(n=n, step=step):
            logger_d1.debug('thousand: n=%d, step=%d', n, step)
            has_thousand = True
            reversed_words.append(self.__localization.thousand)

        if not (has_thousand and a == 1 and self.__localization.omit_one_from_thousand):
            if logger.isEnabledFor(logging.DEBUG):
                if n <= 0 and not has_thousand:
                    logger_d1.debug('hundreds: a=%d', a)
                logger_d2.debug('period: a=%d', a)
            reversed_words.append(self.__period.to_words(a, large_number=is_large_number))

        words: str = self.__localization.word_separator.join(reversed(reversed_words))
        logger_d2.debug('words: %s', words)
        return words

    def __has_thousand(self, step: int) -> bool:
        return step > 0 and self.__localization.large_number_thousand_replaces_ard_suffix

    def __is_thousand(self, n: int, step: int) -> bool:
        return self.__calculate_exponent(n, step) == 3


class PeriodConverter:

    def __init__(self, localization: Localization) -> None:
        self.__localization = localization

    def to_words(self, a: int, large_number: bool) -> str:
        if not 1 <= a <= 999:
            raise InternalError(f'small positive number not in range: {a}')
        words: str = ''
        if a == 1 and large_number:
            words = self.__localization.large_number_1
        else:
            words = self.__localization.get_name_from_cache(i=a)
            if not words:
                lower_than_100 = a % 100
                if lower_than_100:
                    words = self.__lower_than_100_to_words(a=lower_than_100)
                hundreds = a // 100
                if hundreds:
                    plural_hundred: bool = hundreds != 1 and lower_than_100 == 0 and self.__localization.plural_hundred0
                    n_hundreds_words = self.__hundreds_to_words(hundreds=hundreds, plural=plural_hundred)
                    if words:
                        if self.__localization.conjunction_before_tens:
                            words = f'{self.__localization.and_}{self.__localization.word_separator}{words}'
                        words = f'{n_hundreds_words}{self.__localization.word_separator}{words}'
                    else:
                        words = n_hundreds_words
                self.__localization.put_name_in_cache(i=a, words=words)
            else:
                logger_d3.debug('got lower than 1000 from cache')
        return words

    def __lower_than_100_to_words(self, a: int) -> str:
        words: str = ''
        if not 1 <= a <= 99:
            raise InternalError(f'small positive number not in range: {a}')
        words = self.__localization.get_name_from_cache(i=a)
        if not words:
            units = a % 10
            tens = a // 10 % 10
            logger_d3.debug('hundreds decomposed: %d0+0%d', tens, units)
            if units:
                u: int = units
                if tens in [7, 9] and self.__localization.tens_7_and_9_as_fr:
                    u += 10
                words = self.__localization.get_name_from_cache(i=u)
            if tens:
                tens_name = self.__localization.tens_name(index=tens)
                if words:
                    has_conjunction: bool = False
                    if (
                            self.__localization.conjunction_before_units or
                            units == 1 and (
                                tens < 8 and self.__localization.conjunction_before_1_unit_if_lt_80 or
                                tens == 8 and self.__localization.conjunction_before_1_unit_if_eq_80 or
                                tens == 9 and self.__localization.conjunction_before_1_unit_if_eq_90
                                )
                            ):
                        has_conjunction = True
                    word_separator: str
                    if has_conjunction:
                        word_separator = self.__localization.word_separator_11_99_conjunction
                    else:
                        word_separator = self.__localization.word_separator_11_99
                    word_list: list[str] = [tens_name]
                    if has_conjunction:
                        word_list.append(self.__localization.and_)
                    word_list.append(words)
                    words = word_separator.join(word_list)
                else:
                    words = tens_name
            self.__localization.put_name_in_cache(i=a, words=words)
        else:
            logger_d3.debug('got lower than 100 from cache')
        return words

    def __hundreds_to_words(self, hundreds: int, plural: bool) -> str:
        hundreds_words = self.__localization.hundreds_name(hundreds)
        if not hundreds_words:
            hundreds_words = self.__localization.hundreds if plural else self.__localization.hundred
            if hundreds != 1 or not self.__localization.omit_one_from_hundred:
                hundreds_words = f'{self.__localization.get_name_from_cache(i=hundreds)}{self.__localization.word_separator}{hundreds_words}'
        return hundreds_words
