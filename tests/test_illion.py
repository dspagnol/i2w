import unittest

from src.i2w._constants import Gender
from src.i2w._illion import IllionConverter
from src.i2w._localization import Localization


class IllionNLT10Test(unittest.TestCase):

    def test(self):
        gender = Gender.MALE
        for data in self.get_test_data():
            locale_, step, plural, words = data
            localization = Localization(locale_=locale_)
            n = 1
            for word in words:
                converter = IllionConverter(localization=localization)
                self.assertEqual(converter.to_words(n=n, step=step, plural=plural, gender=gender), word, f'{locale_}, n = {n}')
                n += 1

    def get_test_data(self) -> list[tuple[str, int, bool, list[str]]]:
        return [
            ('C', 0, False, [
                'million',
                'billion',
                'trillion',
                'quadrillion',
                'quintillion',
                'sextillion',
                'septillion',
                'octillion',
                'nonillion',
            ]),
            ('en_CA', 0, False, [
                'million',
                'billion',
                'trillion',
                'quadrillion',
                'quintillion',
                'sextillion',
                'septillion',
                'octillion',
                'nonillion',
            ]),
            ('en_GB', 0, False, [
                'million',
                'billion',
                'trillion',
                'quadrillion',
                'quintillion',
                'sextillion',
                'septillion',
                'octillion',
                'nonillion',
            ]),
            ('en_GB', 1, False, [
                'thousand million',
                'thousand billion',
                'thousand trillion',
                'thousand quadrillion',
                'thousand quintillion',
                'thousand sextillion',
                'thousand septillion',
                'thousand octillion',
                'thousand nonillion',
            ]),
            ('en_US', 0, False, [
                'million',
                'billion',
                'trillion',
                'quadrillion',
                'quintillion',
                'sextillion',
                'septillion',
                'octillion',
                'nonillion',
            ]),
            ('fr_CA', 0, False, [
                'million',
                'billion',
                'trillion',
                'quatrillion',
                'quintillion',
                'sextillion',
                'septillion',
                'octillion',
                'nonillion',
            ]),
            ('fr_FR', 0, False, [
                'million',
                'billion',
                'trillion',
                'quatrillion',
                'quintillion',
                'sextillion',
                'septillion',
                'octillion',
                'nonillion',
            ]),
            ('fr_FR', 1, False, [
                'milliard',
                'billiard',
                'trilliard',
                'quatrilliard',
                'quintilliard',
                'sextilliard',
                'septilliard',
                'octilliard',
                'nonilliard',
            ]),
            ('pt_BR', 0, False, [
                'milhão',
                'bilhão',
                'trilhão',
                'quatrilhão',
                'quintilhão',
                'sextilhão',
                'septilhão',
                'octilhão',
                'nonilhão',
            ]),
            ('pt_BR', 0, True, [
                'milhões',
                'bilhões',
                'trilhões',
                'quatrilhões',
                'quintilhões',
                'sextilhões',
                'septilhões',
                'octilhões',
                'nonilhões',
            ]),
            ('pt_PT', 0, False, [
                'milião',
                'bilião',
                'trilião',
                'quatrilião',
                'quintilião',
                'sextilião',
                'septilião',
                'octilião',
                'nonilião',
            ]),
            ('pt_PT', 1, False, [
                'mil milião',
                'mil bilião',
                'mil trilião',
                'mil quatrilião',
                'mil quintilião',
                'mil sextilião',
                'mil septilião',
                'mil octilião',
                'mil nonilião',
            ]),
            ('pt_PT', 0, True, [
                'miliões',
                'biliões',
                'triliões',
                'quatriliões',
                'quintiliões',
                'sextiliões',
                'septiliões',
                'octiliões',
                'noniliões',
            ]),
            ('pt_PT', 1, True, [
                'mil miliões',
                'mil biliões',
                'mil triliões',
                'mil quatriliões',
                'mil quintiliões',
                'mil sextiliões',
                'mil septiliões',
                'mil octiliões',
                'mil noniliões',
            ]),
        ]


class IllionNLT100Test(unittest.TestCase):

    def test(self):
        gender = Gender.MALE
        for data in self.get_test_data():
            locale_, step, plural, words = data
            localization = Localization(locale_=locale_)
            n = 10
            for word in words:
                converter = IllionConverter(localization=localization)
                self.assertEqual(converter.to_words(n=n, step=step, plural=plural, gender=gender), word, f'{locale_}, n = {n}')
                n += 1

    def get_test_data(self) -> list[tuple[str, int, bool, list[str]]]:
        return [
            ('C', 0, False, [
                'decillion',
                'undecillion',
                'duodecillion',
                'tredecillion',
                'quattuordecillion',
                'quindecillion',
                'sedecillion',
                'septendecillion',
                'octodecillion',
                'novendecillion',
                'vigintillion',
            ]),
            ('fr_FR', 0, False, [
                'décillion',
                'undécillion',
                'duodécillion',
                'trédécillion',
                'quattuordécillion',
                'quindécillion',
                'sédécillion',
                'septendécillion',
                'octodécillion',
                'novendécillion',
                'vigintillion',
            ]),
            ('fr_FR', 1, False, [
                'décilliard',
                'undécilliard',
                'duodécilliard',
                'trédécilliard',
                'quattuordécilliard',
                'quindécilliard',
                'sédécilliard',
                'septendécilliard',
                'octodécilliard',
                'novendécilliard',
                'vigintilliard',
            ]),
        ]


if __name__ == '__main__':
    unittest.main()
