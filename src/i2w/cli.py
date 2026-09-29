import argparse
import logging
import sys

from .converter import Converter
from .exception import I2WError, InvalidInteger, MaxStrDigitsOutOfBoundsError
from .logging import LoggingDebugFilter


def configure_max_str_digits(max_str_digits: int | None) -> None:
    """Configure Python's maximum number of string digits for int parsing.

    Args:
        max_str_digits: Maximum digits accepted by int() conversion.
            If None, use Python's safe default for this interpreter.
            If 0, disable the limit (unsafe for untrusted input).
    """
    default_limit: int = sys.int_info.default_max_str_digits
    min_non_zero_limit: int = sys.int_info.str_digits_check_threshold

    if max_str_digits is None:
        max_str_digits = default_limit
    elif max_str_digits != 0 and max_str_digits < min_non_zero_limit:
        raise MaxStrDigitsOutOfBoundsError(
            min_value=min_non_zero_limit,
            max_value=sys.maxsize,
            n=max_str_digits,
        )

    try:
        sys.set_int_max_str_digits(maxdigits=max_str_digits)
    except ValueError as exc:
        raise MaxStrDigitsOutOfBoundsError(
            min_value=min_non_zero_limit,
            max_value=sys.maxsize,
            n=max_str_digits,
        ) from exc


def initialize_log(verbose_level: int) -> None:
    """Initialize logging with appropriate verbosity level.

    Args:
        verbose_level: The verbosity level (0=ERROR, 1=DEBUG, 2+=more debug).
    """
    logging_level: int = logging.INFO
    if verbose_level:
        logging_level = logging.DEBUG
    logging_format = "%(levelname)s: %(message)s"
    logging.basicConfig(format=logging_format, level=logging_level)
    logging.addLevelName(logging.FATAL, "fatal")
    logging.addLevelName(logging.ERROR, "error")
    logging.addLevelName(logging.WARN, "warn ")
    logging.addLevelName(logging.INFO, "info ")
    logging.addLevelName(logging.DEBUG, "debug")
    if verbose_level:
        logging_filter = LoggingDebugFilter(debug_level=verbose_level)
        for handler in logging.root.handlers:
            handler.addFilter(logging_filter)


def parse_arguments() -> argparse.Namespace:
    """Parse and return command-line arguments.

    Returns:
        Parsed command-line arguments namespace.
    """
    parser = argparse.ArgumentParser("i2w")  # TODO put program name to in a variable
    parser.add_argument(
        "--locale",
        "-l",
        default=None,
        help="POSIX locale (e.g., 'en_US', 'fr_FR'). Defaults to system locale.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        dest="verbose_level",
    )
    parser.add_argument(
        "--max-str-digits",
        type=int,
        default=None,
        help=(
            "Maximum string digits accepted when parsing integers. "
            "Use 0 to disable the limit (unsafe). Defaults to Python's safe default."
        ),
    )
    parser.add_argument("numbers", type=str, nargs="*", default=[])
    args = parser.parse_args()
    return args


def main() -> None:
    """Main entry point for the i2w command-line application."""
    args = parse_arguments()

    initialize_log(verbose_level=args.verbose_level)

    def process_number(converter: Converter, x: str) -> bool:
        success: bool = False
        try:
            i = int(x)
            print(converter.to_words(i=i))
            success = True
        except InvalidInteger as e:
            logging.error(str(e))
        except ValueError:
            logging.error("invalid integer: '%s'", x)
        return success

    success: bool = True

    try:
        configure_max_str_digits(max_str_digits=args.max_str_digits)
        converter = Converter(locale_name=args.locale)
        for s in args.numbers:
            success &= process_number(converter, s)
        if len(args.numbers) == 0 and sys.stdin.readable():
            for line in sys.stdin:
                for s in line.split():
                    success &= process_number(converter, s)
    except I2WError as e:
        logging.error(str(e))
        success = False
    except KeyboardInterrupt:
        pass

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
