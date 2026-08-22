class Converter:
    """Public API for converting integers to words in multiple languages.

    Converts integers to their word representation in the specified locale.
    Automatically selects the appropriate converter implementation based on
    the locale's rules (short scale or long scale).

    Attributes:
        __impl: Private implementation instance providing the actual conversion logic.
    """

    def __init__(self, locale_: str = "") -> None:
        """Initialize converter with optional locale.

        Args:
            locale_: POSIX locale (e.g., 'en_US', 'fr_FR'). Defaults to
                     system locale.
        """
        from ._constants import ConverterImplTypeValue
        from ._converter import ConverterImpl, ConverterRegistrar
        from ._localization import Localization
        from ._logging import logger

        localization: Localization = Localization(locale_=locale_)
        impl_type: ConverterImplTypeValue = localization.get_impl_type()
        logger.debug("converter: %s", str(impl_type))
        self.__impl: ConverterImpl = ConverterRegistrar.get_class(type_id=impl_type)(
            localization=localization
        )

    def to_words(self, i: int) -> str:
        """Convert an integer to its word representation.

        Args:
            i: The integer to convert.

        Returns:
            Word representation of the integer in the initialized locale.
        """
        return self.__impl.to_words(i=i)
