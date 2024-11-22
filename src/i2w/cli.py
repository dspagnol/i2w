import argparse
import logging
import sys

from .converter import Converter
from .exception import InvalidInteger
from .exception import I2WException
from .logging import LoggingDebugFilter


def initialize_log(verbose_level: int) -> None:
    logging_level: int = logging.INFO
    if verbose_level:
        logging_level = logging.DEBUG
    LOGGING_FORMAT = '%(levelname)s: %(message)s'
    logging.basicConfig(format=LOGGING_FORMAT, level=logging_level)
    logging.addLevelName(logging.FATAL, 'fatal')
    logging.addLevelName(logging.ERROR, 'error')
    logging.addLevelName(logging.WARN,  'warn ')
    logging.addLevelName(logging.INFO,  'info ')
    logging.addLevelName(logging.DEBUG, 'debug')
    if verbose_level:
        logging_filter = LoggingDebugFilter(debug_level=verbose_level)
        for handler in logging.root.handlers:
            handler.addFilter(logging_filter)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser('i2w') # TODO put program name to in a variable
    parser.add_argument('--locale', '-l')
    parser.add_argument('--verbose', '-v', action='count', default=0, dest='verbose_level')
    parser.add_argument('numbers', type=int, nargs='*', default=[])
    args = parser.parse_args()
    return args


def main() -> None:

    sys.set_int_max_str_digits(maxdigits=0)

    args = parse_arguments()

    initialize_log(verbose_level=args.verbose_level)

    def process_number(converter: Converter, x: int | str) -> bool:
        success: bool = False
        try:
            is_int: bool = True
            i: int
            if isinstance(x, int):
                i = x
            else:
                try:
                    i = int(x)
                except ValueError:
                    logging.error(f"invalid integer: '{x}'")
                    is_int = False
            if is_int:
                print(converter.to_words(i=i))
                success = True
        except InvalidInteger as e:
            logging.error(str(e))
        return success

    success: bool = True

    try:
        converter = Converter(args.locale)
        for s in args.numbers:
            success &= process_number(converter, s)
        if len(args.numbers) == 0:
            if sys.stdin.readable():
                for line in sys.stdin:
                    for s in line.split():
                        success &= process_number(converter, s)
    except I2WException as e:
        logging.error(str(e))
        success = False
    except KeyboardInterrupt:
        pass

    if not success:
        exit(1)


if __name__ == '__main__':
    main()
