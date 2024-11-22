import enum

from ._types import Enum
from ._types import LanguageDict


class ConverterImplTypeProperty(Enum):

    CONVERTER_IMPL_TYPE = enum.auto()


class ConverterImplTypeValue(Enum):

    SHORT_SCALE = enum.auto()
    LONG_SCALE = enum.auto()


class BoolProperty(Enum):

    CONJUNCTION_BEFORE_UNITS = enum.auto()
    CONJUNCTION_BEFORE_TENS = enum.auto()
    CONJUNCTION_BEFORE_1_UNIT_IF_LT_80 = enum.auto()
    CONJUNCTION_BEFORE_1_UNIT_IF_EQ_80 = enum.auto()
    CONJUNCTION_BEFORE_1_UNIT_IF_EQ_90 = enum.auto()
    CONJUNCTION_BEFORE_LAST_NON_0_PERIOD = enum.auto()
    TENS_7_AND_9_AS_FR = enum.auto()
    PLURAL_HUNDRED00 = enum.auto()
    OMIT_ONE_FROM_HUNDRED = enum.auto()
    OMIT_ONE_FROM_THOUSAND = enum.auto()
    LARGE_NUMBER_INVARIABLE = enum.auto()
    LARGE_NUMBER_THOUSAND_REPLACES_ARD_SUFFIX = enum.auto()
    LARGE_NUMBER_NO_LIAISON_USE_ALT_UNIT_PREFIX = enum.auto()


class StrProperty(Enum):

    WORD_SEPARATOR = enum.auto()
    WORD_SEPARATOR_11_99 = enum.auto()
    WORD_SEPARATOR_11_99_CONJUNCTION = enum.auto()
    MINUS = enum.auto()
    AND = enum.auto()
    HUNDRED = enum.auto()
    HUNDREDS = enum.auto()
    THOUSAND = enum.auto()
    LARGE_NUMBER_1 = enum.auto()
    LARGE_NUMBER_INFIX_BASE = enum.auto()
    LARGE_NUMBER_INFIX_SUFFIX = enum.auto()


class StrListProperty(Enum):

    TENS_NAMES = enum.auto()
    HUNDREDS_NAMES = enum.auto()
    LARGE_NUMBER_SUFFIXES = enum.auto()
    LARGE_NUMBER_SUFFIXES_PLURAL = enum.auto()
    LARGE_NUMBER_PREFIXES_N_LT_10 = enum.auto()
    LARGE_NUMBER_UNITS = enum.auto()
    LARGE_NUMBER_UNITS_ALT = enum.auto()
    LARGE_NUMBER_TENS = enum.auto()
    LARGE_NUMBER_HUNDREDS = enum.auto()


class StrListListProperty(Enum):

    LARGE_NUMBER_UNITS_LIASON = enum.auto()
    LARGE_NUMBER_TENS_LIASON = enum.auto()
    LARGE_NUMBER_TENS_I_A= enum.auto()
    LARGE_NUMBER_HUNDREDS_LIASON = enum.auto()


class Gender(Enum):

    MALE = enum.auto()
    FEMALE = enum.auto()


CONVERTER_IMPL_TYPE_PROPERTIES: LanguageDict[dict[ConverterImplTypeProperty, ConverterImplTypeValue]] = {
    None: {
        None: {
            ConverterImplTypeProperty.CONVERTER_IMPL_TYPE: ConverterImplTypeValue.SHORT_SCALE,
        },
    },
    'en': {
        'GB': {
            ConverterImplTypeProperty.CONVERTER_IMPL_TYPE: ConverterImplTypeValue.LONG_SCALE,
        },
    },
    'es': {
        None: {
            ConverterImplTypeProperty.CONVERTER_IMPL_TYPE: ConverterImplTypeValue.LONG_SCALE,
        },
    },
    'fr': {
        None: {
            ConverterImplTypeProperty.CONVERTER_IMPL_TYPE: ConverterImplTypeValue.LONG_SCALE,
        },
    },
    'pt': {
        None: {
            ConverterImplTypeProperty.CONVERTER_IMPL_TYPE: ConverterImplTypeValue.LONG_SCALE,
        },
        'BR': {
            ConverterImplTypeProperty.CONVERTER_IMPL_TYPE: ConverterImplTypeValue.SHORT_SCALE,
        },
    },
}


BOOL_PROPERTIES: LanguageDict[dict[BoolProperty, bool]] = {
    None: {
        None: {
            BoolProperty.LARGE_NUMBER_INVARIABLE: True,
        },
    },
    'en': {
        'GB': {
            BoolProperty.LARGE_NUMBER_THOUSAND_REPLACES_ARD_SUFFIX: True,
        },
    },
    'es': {
        None: {
            BoolProperty.CONJUNCTION_BEFORE_UNITS: True,
            BoolProperty.OMIT_ONE_FROM_HUNDRED: True,
            BoolProperty.OMIT_ONE_FROM_THOUSAND: True,
            BoolProperty.LARGE_NUMBER_INVARIABLE: False,
            BoolProperty.LARGE_NUMBER_THOUSAND_REPLACES_ARD_SUFFIX: True,
        },
    },
    'fr': {
        None: {
            BoolProperty.CONJUNCTION_BEFORE_1_UNIT_IF_LT_80: True,
            BoolProperty.TENS_7_AND_9_AS_FR: True,
            BoolProperty.PLURAL_HUNDRED00: True,
            BoolProperty.OMIT_ONE_FROM_HUNDRED: True,
            BoolProperty.OMIT_ONE_FROM_THOUSAND: True,
            BoolProperty.LARGE_NUMBER_INVARIABLE: False,
            BoolProperty.LARGE_NUMBER_NO_LIAISON_USE_ALT_UNIT_PREFIX: True,
        },
        'BE': {
            BoolProperty.TENS_7_AND_9_AS_FR: False,
            BoolProperty.CONJUNCTION_BEFORE_1_UNIT_IF_EQ_90: True,
        },
        'CH': {
            BoolProperty.TENS_7_AND_9_AS_FR: False,
            BoolProperty.CONJUNCTION_BEFORE_1_UNIT_IF_EQ_80: True,
            BoolProperty.CONJUNCTION_BEFORE_1_UNIT_IF_EQ_90: True,
        },
    },
    'pt': {
        None: {
            BoolProperty.CONJUNCTION_BEFORE_UNITS: True,
            BoolProperty.CONJUNCTION_BEFORE_TENS: True,
            BoolProperty.CONJUNCTION_BEFORE_LAST_NON_0_PERIOD: True, # https://www.dicio.com.br/como-escrever-numeros-por-extenso/
            BoolProperty.OMIT_ONE_FROM_HUNDRED: True,
            BoolProperty.OMIT_ONE_FROM_THOUSAND: True,
            BoolProperty.LARGE_NUMBER_INVARIABLE: False,
            BoolProperty.LARGE_NUMBER_THOUSAND_REPLACES_ARD_SUFFIX: True,
        },
    },
}


STR_PROPERTIES: LanguageDict[dict[StrProperty, str]] = {
    None: {
        None: {
            StrProperty.WORD_SEPARATOR: ' ',
            StrProperty.WORD_SEPARATOR_11_99: '-',
            StrProperty.WORD_SEPARATOR_11_99_CONJUNCTION: ' ',
            StrProperty.MINUS: 'minus',
            StrProperty.AND: 'and',
            StrProperty.HUNDRED: 'hundred',
            StrProperty.HUNDREDS: 'hundreds',
            StrProperty.THOUSAND: 'thousand',
            StrProperty.LARGE_NUMBER_1: 'one',
            StrProperty.LARGE_NUMBER_INFIX_BASE: 'lli',
            StrProperty.LARGE_NUMBER_INFIX_SUFFIX: 'lli',
        },
    },
    'es': {
        None: {
            StrProperty.WORD_SEPARATOR_11_99: ' ',
            StrProperty.MINUS: 'menos',
            StrProperty.AND: 'y',
            StrProperty.THOUSAND: 'mil',
            StrProperty.LARGE_NUMBER_1: 'un',
            StrProperty.LARGE_NUMBER_INFIX_SUFFIX: 'll',
        },
    },
    'fr': {
        None: {
            StrProperty.WORD_SEPARATOR: '-',
            StrProperty.WORD_SEPARATOR_11_99_CONJUNCTION: '-',
            StrProperty.MINUS: 'moins',
            StrProperty.AND: 'et',
            StrProperty.HUNDRED: 'cent',
            StrProperty.HUNDREDS: 'cents',
            StrProperty.THOUSAND: 'mille',
            StrProperty.LARGE_NUMBER_1: 'un',
        },
        'CA': {
            StrProperty.WORD_SEPARATOR: ' ',
            StrProperty.WORD_SEPARATOR_11_99_CONJUNCTION: ' ',
        },
    },
    'pt': {
        None: {
            StrProperty.WORD_SEPARATOR_11_99: ' ',
            StrProperty.MINUS: 'menos',
            StrProperty.AND: 'e',
            StrProperty.THOUSAND: 'mil',
            StrProperty.LARGE_NUMBER_1: 'um',
            StrProperty.LARGE_NUMBER_INFIX_BASE: 'li',
            StrProperty.LARGE_NUMBER_INFIX_SUFFIX: 'li',
        },
        'BR': {
            StrProperty.LARGE_NUMBER_INFIX_SUFFIX: 'lh',
        },
    },
}


STR_LIST_PROPERTIES: LanguageDict[dict[StrListProperty, list[str]]] = {
    None: {
        None: {
            StrListProperty.TENS_NAMES:                    ['', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'],
            StrListProperty.LARGE_NUMBER_SUFFIXES:         ['on', 'ard'],
            StrListProperty.LARGE_NUMBER_SUFFIXES_PLURAL:  ['ons', 'ards'],
            StrListProperty.LARGE_NUMBER_PREFIXES_N_LT_10: ['ni', 'mi', 'bi', 'tri', 'quadri', 'quinti', 'sexti', 'septi', 'octi', 'noni'],
            StrListProperty.LARGE_NUMBER_UNITS:            ['', 'un', 'duo', 'tre', 'quattuor', 'quin', 'se', 'septe', 'octo', 'nove'],
            StrListProperty.LARGE_NUMBER_UNITS_ALT:        ['', 'un', 'duo', 'tre', 'quattuor', 'quin', 'se', 'septe', 'octo', 'nove'],
            StrListProperty.LARGE_NUMBER_TENS:             ['', 'dec', 'vigint', 'trigint', 'quadragint', 'quinquagint', 'sexagint', 'septuagint', 'octogint', 'nonagint'],
            StrListProperty.LARGE_NUMBER_HUNDREDS:         ['', 'centi', 'ducenti', 'trecenti', 'quadringenti', 'quingenti', 'sescenti', 'septingenti', 'octingenti', 'nongenti'],
        },
    },
    'es': {
        None: {
            StrListProperty.TENS_NAMES:                    ['', 'diez', 'veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa'],
            StrListProperty.HUNDREDS_NAMES:                ['', 'ciento', 'doscientos', 'trescientos', 'cuatrocientos', 'quinientos', 'seiscientos', 'setecientos', 'ochocientos', 'novecientos'],
            StrListProperty.LARGE_NUMBER_SUFFIXES:         ['ón', ''],
            StrListProperty.LARGE_NUMBER_SUFFIXES_PLURAL:  ['ones', ''],
            StrListProperty.LARGE_NUMBER_PREFIXES_N_LT_10: ['ni', 'mi', 'bi', 'tri', 'quatri', 'quinti', 'sexti', 'septi', 'octi', 'noni'],
        },
    },
    'fr': {
        None: {
            StrListProperty.TENS_NAMES:                    ['', 'dix', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'soixante', 'quatre-vingt', 'quatre-vingt'],
            StrListProperty.LARGE_NUMBER_PREFIXES_N_LT_10: ['ni', 'mi', 'bi', 'tri', 'quatri', 'quinti', 'sexti', 'septi', 'octi', 'noni'],
            StrListProperty.LARGE_NUMBER_UNITS_ALT:        ['', 'un', 'duo', 'tré', 'quattuor', 'quin', 'sé', 'septé', 'octo', 'nové'],
            StrListProperty.LARGE_NUMBER_TENS:             ['', 'déc', 'vigint', 'trigint', 'quadragint', 'quinquagint', 'sexagint', 'septuagint', 'octogint', 'nonagint'],
        },
        'BE': {
            StrListProperty.TENS_NAMES:                    ['', 'dix', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'septante', 'quatre-vingt', 'nonante'],
        },
        'CH': {
            StrListProperty.TENS_NAMES:                    ['', 'dix', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'septante', 'huitante', 'nonante'],
        },
    },
    'pt': {
        None: {
            StrListProperty.TENS_NAMES:                    ['', 'dez', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa'],
            StrListProperty.HUNDREDS_NAMES:                ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos'],
            StrListProperty.LARGE_NUMBER_SUFFIXES:         ['ão', 'ar'],
            StrListProperty.LARGE_NUMBER_SUFFIXES_PLURAL:  ['ões', 'ares'],
            StrListProperty.LARGE_NUMBER_PREFIXES_N_LT_10: ['ni', 'mi', 'bi', 'tri', 'quatri', 'quinti', 'sexti', 'septi', 'octi', 'noni'],
        },
    },
}


STR_LIST_LIST_PROPERTIES: LanguageDict[dict[StrListListProperty, list[list[str]]]] = {
    None: {
        None: {
            StrListListProperty.LARGE_NUMBER_UNITS_LIASON:    [[], [], [], ['s'], [], [], ['s', 'x'], ['m', 'n'], [], ['m', 'n']],
            StrListListProperty.LARGE_NUMBER_TENS_LIASON:     [[], ['n'], ['m', 's'], ['n', 's'], ['n', 's'], ['n', 's'], ['n'], ['n'], ['m', 'x'], []],
            StrListListProperty.LARGE_NUMBER_TENS_I_A:        [['', ''], ['i', 'i'], ['i', 'i'], ['i', 'a'], ['i', 'a'], ['i', 'a'], ['i', 'a'], ['i', 'a'], ['i', 'a'], ['i', 'a']],
            StrListListProperty.LARGE_NUMBER_HUNDREDS_LIASON: [[], ['n', 'x'], ['n'], ['n', 's'], ['n', 's'], ['n', 's'], ['n'], ['n'], ['m', 'x'], []],
        }
    },
}


NUMBER_NAMES: LanguageDict[dict[int, str]] = {
    None: {
        None: {
            0: 'zero',
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six',
            7: 'seven',
            8: 'eight',
            9: 'nine',
            11: 'eleven',
            12: 'twelve',
            13: 'thirteen',
            14: 'fourteen',
            15: 'fifteen',
            16: 'sixteen',
            17: 'seventeen',
            18: 'eighteen',
            19: 'nineteen',
        },
    },
    'es': {
        None: {
            0: 'cero',
            1: 'uno',
            2: 'dos',
            3: 'tres',
            4: 'cuatro',
            5: 'cinco',
            6: 'seis',
            7: 'siete',
            8: 'ocho',
            9: 'nueve',
            11: 'once',
            12: 'doce',
            13: 'trece',
            14: 'catorce',
            15: 'quince',
            16: 'dieciséis',
            17: 'diecisiete',
            18: 'dieciocho',
            19: 'diecinueve',
            21: 'veintiuno',
            22: 'veintidós',
            23: 'veintitrés',
            24: 'veinticuatro',
            25: 'veinticinco',
            26: 'veintiséis',
            27: 'veintisiete',
            28: 'veintiocho',
            29: 'veintinueve',
            100: 'cien',
        },
    },
    'fr': {
        None: {
            0: 'zéro',
            1: 'un',
            2: 'deux',
            3: 'trois',
            4: 'quatre',
            5: 'cinq',
            6: 'six',
            7: 'sept',
            8: 'huit',
            9: 'neuf',
            11: 'onze',
            12: 'douze',
            13: 'treize',
            14: 'quatorze',
            15: 'quinze',
            16: 'seize',
            17: '',
            18: '',
            19: '',
            70: 'soixante-dix',
            71: '',
            72: '',
            73: '',
            74: '',
            75: '',
            76: '',
            80: 'quatre-vingts',
            90: 'quatre-vingt-dix',
        },
        'BE': {
            70: '',
            90: '',
        },
        'CH': {
            70: '',
            80: '',
            90: '',
        },
    },
    'pt': {
        None: {
            0: 'zero',
            1: 'um',
            2: 'dois',
            3: 'três',
            4: 'quatro',
            5: 'cinco',
            6: 'seis',
            7: 'sete',
            8: 'oito',
            9: 'nove',
            11: 'onze',
            12: 'doze',
            13: 'treze',
            14: 'catorze',
            15: 'quinze',
            16: 'dezasseis',
            17: 'dezassete',
            18: 'dezoito',
            19: 'dezanove',
            100: 'cem',
        },
        'BR': {
            14: 'quatorze',
            16: 'dezesseis',
            17: 'dezessete',
            19: 'dezenove',
        },
    },
}
