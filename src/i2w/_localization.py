import locale

from ._constants import BOOL_PROPERTIES
from ._constants import BoolProperty
from ._constants import CONVERTER_IMPL_TYPE_PROPERTIES
from ._constants import ConverterImplTypeProperty
from ._constants import ConverterImplTypeValue
from ._constants import NUMBER_NAMES
from ._constants import STR_LIST_LIST_PROPERTIES
from ._constants import STR_LIST_PROPERTIES
from ._constants import STR_PROPERTIES
from ._constants import StrListListProperty
from ._constants import StrListProperty
from ._constants import StrProperty
from ._logging import logger
from ._logging import logger_d1
from ._types import LanguageDict
from ._types import TerritoryDict
from .exception import LocalizationError


class Localization:
    """
    Localization is a layer on top of multi-language objects for translations and rules.
    """

    def __init__(self, locale_: str = '') -> None:
        """
        Create a localization object.

        Keyword arguments:
        locale_ -- no standard, but usually in POSIX format ([language[_territory][.codeset][@modifier]]) (default '')
        """
        self.__language: str | None = None # ISO 639
        self.__territory: str | None = None # ISO 3166-1 alpha-2
        if locale_ is None:
            locale_ = ''
        try:
            locale.setlocale(locale.LC_ALL, locale_)
        except locale.Error as e:
            if locale_:
                raise LocalizationError(locale_) from e
        language_and_territory: str | None = None
        (language_and_territory, _) = locale.getlocale(locale.LC_MESSAGES)
        logger.debug('detected locale: %s', language_and_territory)
        language: str | None = None
        territory: str | None = None
        if language_and_territory is not None:
            [language, territory] = language_and_territory.split('_')
        self.__language_and_territory = language_and_territory
        self.__language = language
        self.__territory = territory
        logger_d1.debug('using language:  %s', self.__language)
        logger_d1.debug('using territory: %s', self.__territory)

        self.__conjunction_before_units = self.__get_bool_property(
                key=BoolProperty.CONJUNCTION_BEFORE_UNITS)
        self.__conjunction_before_tens = self.__get_bool_property(
                key=BoolProperty.CONJUNCTION_BEFORE_TENS)
        self.__conjunction_before_1_unit_if_lt_80 = self.__get_bool_property(
                key=BoolProperty.CONJUNCTION_BEFORE_1_UNIT_IF_LT_80)
        self.__conjunction_before_1_unit_if_eq_80 = self.__get_bool_property(
                key=BoolProperty.CONJUNCTION_BEFORE_1_UNIT_IF_EQ_80)
        self.__conjunction_before_1_unit_if_eq_90 = self.__get_bool_property(
                key=BoolProperty.CONJUNCTION_BEFORE_1_UNIT_IF_EQ_90)
        self.__conjunction_before_last_non_0_period = self.__get_bool_property(
                key=BoolProperty.CONJUNCTION_BEFORE_LAST_NON_0_PERIOD)
        self.__tens_7_and_9_as_fr = self.__get_bool_property(
                key=BoolProperty.TENS_7_AND_9_AS_FR)
        self.__plural_hundred0 = self.__get_bool_property(
                key=BoolProperty.PLURAL_HUNDRED00)
        self.__omit_one_from_hundred = self.__get_bool_property(
                key=BoolProperty.OMIT_ONE_FROM_HUNDRED)
        self.__omit_one_from_thousand = self.__get_bool_property(
                key=BoolProperty.OMIT_ONE_FROM_THOUSAND)
        self.__large_number_invariable = self.__get_bool_property(
                key=BoolProperty.LARGE_NUMBER_INVARIABLE)
        self.__large_number_thousand_replaces_ard_suffix = self.__get_bool_property(
                key=BoolProperty.LARGE_NUMBER_THOUSAND_REPLACES_ARD_SUFFIX)
        self.__large_number_no_liaison_use_alt_unit_prefix = self.__get_bool_property(
                key=BoolProperty.LARGE_NUMBER_NO_LIAISON_USE_ALT_UNIT_PREFIX)
        self.__word_separator = self.__get_str_property(
                key=StrProperty.WORD_SEPARATOR)
        self.__word_separator_11_99 = self.__get_str_property(
                key=StrProperty.WORD_SEPARATOR_11_99)
        self.__word_separator_11_99_conjunction = self.__get_str_property(
                key=StrProperty.WORD_SEPARATOR_11_99_CONJUNCTION)
        self.__minus = self.__get_str_property(
                key=StrProperty.MINUS)
        self.__and = self.__get_str_property(
                key=StrProperty.AND)
        self.__hundred = self.__get_str_property(
                key=StrProperty.HUNDRED)
        self.__hundreds = self.__get_str_property(
                key=StrProperty.HUNDREDS)
        self.__thousand = self.__get_str_property(
                key=StrProperty.THOUSAND)
        self.__large_number_1 = self.__get_str_property(
                key=StrProperty.LARGE_NUMBER_1)
        self.__large_number_infix_base = self.__get_str_property(
                key=StrProperty.LARGE_NUMBER_INFIX_BASE)
        self.__large_number_infix_suffix = self.__get_str_property(
                key=StrProperty.LARGE_NUMBER_INFIX_SUFFIX)
        self.__tens_names = self.__get_str_list_property(
                key=StrListProperty.TENS_NAMES)
        self.__hundreds_names = self.__get_str_list_property(
                key=StrListProperty.HUNDREDS_NAMES)
        self.__large_number_suffixes = self.__get_str_list_property(
                key=StrListProperty.LARGE_NUMBER_SUFFIXES)
        self.__large_number_suffixes_plural = self.__get_str_list_property(
                key=StrListProperty.LARGE_NUMBER_SUFFIXES_PLURAL)
        self.__large_number_prefixes_n_lt_10 = self.__get_str_list_property(
                key=StrListProperty.LARGE_NUMBER_PREFIXES_N_LT_10)
        self.__large_number_units = self.__get_str_list_property(
                key=StrListProperty.LARGE_NUMBER_UNITS)
        self.__large_number_units_alt = self.__get_str_list_property(
                key=StrListProperty.LARGE_NUMBER_UNITS_ALT)
        self.__large_number_tens = self.__get_str_list_property(
                key=StrListProperty.LARGE_NUMBER_TENS)
        self.__large_number_hundreds = self.__get_str_list_property(
                key=StrListProperty.LARGE_NUMBER_HUNDREDS)
        self.__large_number_units_liaison = self.__get_str_list_list_property(
                key=StrListListProperty.LARGE_NUMBER_UNITS_LIASON)
        self.__large_number_tens_liaison = self.__get_str_list_list_property(
                key=StrListListProperty.LARGE_NUMBER_TENS_LIASON)
        self.__large_number_tens_i_a = self.__get_str_list_list_property(
                key=StrListListProperty.LARGE_NUMBER_TENS_I_A)
        self.__large_number_hundreds_liasion = self.__get_str_list_list_property(
                key=StrListListProperty.LARGE_NUMBER_HUNDREDS_LIASON)
        self.__cache: dict[int, str] = {}

    def get_impl_type(self) -> ConverterImplTypeValue:
        return self.__get_dict_entry(
                dictionary=CONVERTER_IMPL_TYPE_PROPERTIES,
                key=ConverterImplTypeProperty.CONVERTER_IMPL_TYPE,
                default_value=ConverterImplTypeValue.SHORT_SCALE,
                )

    def get_name_from_cache(self, i: int) -> str:
        words: str = ''
        if i in self.__cache:
            words = self.__cache[i]
        else:
            words = self.__get_dict_entry(
                dictionary=NUMBER_NAMES,
                key=i,
                default_value='',
                )
        return words

    def put_name_in_cache(self, i: int, words: str) -> None:
        self.__cache[i] = words

    @property
    def conjunction_before_units(self) -> bool:
        return self.__conjunction_before_units

    @property
    def conjunction_before_tens(self) -> bool:
        return self.__conjunction_before_tens

    @property
    def conjunction_before_1_unit_if_lt_80(self) -> bool:
        return self.__conjunction_before_1_unit_if_lt_80

    @property
    def conjunction_before_1_unit_if_eq_80(self) -> bool:
        return self.__conjunction_before_1_unit_if_eq_80

    @property
    def conjunction_before_1_unit_if_eq_90(self) -> bool:
        return self.__conjunction_before_1_unit_if_eq_90

    @property
    def conjunction_before_last_non_0_period(self) -> bool:
        return self.__conjunction_before_last_non_0_period

    @property
    def tens_7_and_9_as_fr(self) -> bool:
        return self.__tens_7_and_9_as_fr

    @property
    def plural_hundred0(self) -> bool:
        return self.__plural_hundred0

    @property
    def omit_one_from_hundred(self) -> bool:
        return self.__omit_one_from_hundred

    @property
    def omit_one_from_thousand(self) -> bool:
        return self.__omit_one_from_thousand

    @property
    def large_number_invariable(self) -> bool:
        return self.__large_number_invariable

    @property
    def large_number_thousand_replaces_ard_suffix(self) -> bool:
        return self.__large_number_thousand_replaces_ard_suffix

    @property
    def large_number_no_liaison_use_alt_unit_prefix(self) -> bool:
        return self.__large_number_no_liaison_use_alt_unit_prefix

    @property
    def word_separator(self) -> str:
        return self.__word_separator

    @property
    def word_separator_11_99(self) -> str:
        return self.__word_separator_11_99

    @property
    def word_separator_11_99_conjunction(self) -> str:
        return self.__word_separator_11_99_conjunction

    @property
    def minus(self) -> str:
        return self.__minus

    @property
    def and_(self) -> str:
        return self.__and

    @property
    def hundred(self) -> str:
        return self.__hundred

    @property
    def hundreds(self) -> str:
        return self.__hundreds

    @property
    def thousand(self) -> str:
        return self.__thousand 

    @property
    def large_number_1(self) -> str:
        return self.__large_number_1

    @property
    def large_number_infix_base(self) -> str:
        return self.__large_number_infix_base

    @property
    def large_number_infix_suffix(self) -> str:
        return self.__large_number_infix_suffix

    def tens_name(self, index: int) -> str:
        return self.__get_entry_from_str_list(str_list=self.__tens_names, index=index)

    def hundreds_name(self, index: int) -> str:
        return self.__get_entry_from_str_list(str_list=self.__hundreds_names, index=index)

    def large_number_suffixes(self, index: int) -> str:
        return self.__get_entry_from_str_list(str_list=self.__large_number_suffixes, index=index)

    def large_number_suffixes_plural(self, index: int) -> str:
        return self.__get_entry_from_str_list(str_list=self.__large_number_suffixes_plural, index=index)

    def large_number_prefixes_n_lt_10(self, index: int) -> str:
        return self.__get_entry_from_str_list(str_list=self.__large_number_prefixes_n_lt_10, index=index)

    def large_number_units(self, index: int) -> str:
        return self.__get_entry_from_str_list(str_list=self.__large_number_units, index=index)

    def large_number_units_alt(self, index: int) -> str:
        return self.__get_entry_from_str_list(str_list=self.__large_number_units_alt, index=index)

    def large_number_tens(self, index: int) -> str:
        return self.__get_entry_from_str_list(str_list=self.__large_number_tens, index=index)

    def large_number_hundreds(self, index: int) -> str:
        return self.__get_entry_from_str_list(str_list=self.__large_number_hundreds, index=index)

    def large_number_units_liaison(self, index: int) -> list[str]:
        return self.__get_entry_from_str_list_list(str_list_list=self.__large_number_units_liaison, index=index)

    def large_number_tens_liaison(self, index: int) -> list[str]:
        return self.__get_entry_from_str_list_list(str_list_list=self.__large_number_tens_liaison, index=index)

    def large_number_tens_i_a(self, index: int) -> list[str]:
        return self.__get_entry_from_str_list_list(str_list_list=self.__large_number_tens_i_a, index=index)

    def large_number_hundreds_liasion(self, index: int) -> list[str]:
        return self.__get_entry_from_str_list_list(str_list_list=self.__large_number_hundreds_liasion, index=index)

    def __get_bool_property(self, key: BoolProperty) -> bool:
        return self.__get_dict_entry(dictionary=BOOL_PROPERTIES, key=key, default_value=False)

    def __get_str_property(self, key: StrProperty) -> str:
        return self.__get_dict_entry(dictionary=STR_PROPERTIES, key=key, default_value='')

    def __get_str_list_property(self, key: StrListProperty) -> list[str]:
        return self.__get_dict_entry(dictionary=STR_LIST_PROPERTIES, key=key, default_value=[''])

    def __get_str_list_list_property(self, key: StrListListProperty) -> list[list[str]]:
        return self.__get_dict_entry(dictionary=STR_LIST_LIST_PROPERTIES, key=key, default_value=[['']])

    def __get_entry_from_str_list(self, str_list: list[str], index: int) -> str:
        if index > len(str_list) - 1:
            index = 0
        return str_list[index]

    def __get_entry_from_str_list_list(self, str_list_list: list[list[str]], index: int) -> list[str]:
        if index > len(str_list_list) - 1:
            index = 0
        return str_list_list[index]

    def __get_dict_entry[K, V](self, dictionary: LanguageDict[dict[K, V]], key: K, default_value: V) -> V:
        dict_preferred: dict[K, V]
        dict_fallback_1: dict[K, V]
        dict_fallback_2: dict[K, V]
        (dict_preferred, dict_fallback_1, dict_fallback_2) = self.__get_language_dicts(dictionary)
        value: V = default_value
        if key in dict_preferred:
            value = dict_preferred[key]
        elif key in dict_fallback_1:
            value = dict_fallback_1[key]
        elif key in dict_fallback_2:
            value = dict_fallback_2[key]
        return value

    def __get_language_dicts[K, V](self, dictionary: LanguageDict[dict[K, V]]) -> tuple[dict[K, V], dict[K, V], dict[K, V]]:
        language: str | None = self.__language
        if language not in dictionary:
            language = None
        dict_language: TerritoryDict[dict[K, V]] = dictionary[language]
        territory: str | None = self.__territory
        if territory not in dict_language:
            dict_language[territory] = {}
        dict_territory: dict[K, V] = dict_language[territory]
        return (dict_territory, dict_language[None] if None in dict_language else dictionary[None][None], dictionary[None][None])
