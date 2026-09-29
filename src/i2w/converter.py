class Converter:
    """Public API for converting integers to words in multiple languages.

    Converts integers to their word representation in a specified or system locale.
    Automatically selects the appropriate converter implementation based on
    the locale's rules (short scale or long scale).

    This class is the primary programmatic interface for integer-to-words conversion.
    It can also be used from the command line for convenience and testing.

    Attributes:
        __impl: Private implementation instance providing the actual conversion logic.
    """

    def __init__(self, locale_name: str | None = None) -> None:
        """Initialize converter with optional locale override.

        Args:
            locale_name: POSIX format locale code (e.g., 'en_US', 'fr_FR', 'pt_BR').

                        When a language-only code is provided (e.g., 'en', 'fr'),
                        the most common territory for that language is automatically
                        deduced. For example:
                        - 'en' becomes 'en_US'
                        - 'fr' becomes 'fr_FR'
                        - 'es' becomes 'es_ES'
                        - 'pt' becomes 'pt_PT'

                        If not provided, the system's environment locale is used.
                        Explicitly provided locale values are validated strictly.

                        Supported locales include:
                        - English: en, en_US, en_GB
                        - French: fr, fr_FR, fr_BE, fr_CH, fr_CA
                        - Spanish: es, es_ES
                        - Portuguese: pt, pt_PT, pt_BR

                        Defaults to system locale.
        """
        from ._constants import ConverterImplTypeValue
        from ._converter import ConverterImpl, ConverterRegistrar
        from ._localization import Localization
        from ._logging import logger

        localization: Localization = Localization(
            locale_name=locale_name,
            strict=(locale_name is not None),
        )
        impl_type: ConverterImplTypeValue = localization.get_impl_type()
        logger.debug("converter: %s", str(impl_type))
        self.__impl: ConverterImpl = ConverterRegistrar.get_class(type_id=impl_type)(
            localization=localization,
        )

    def to_words(self, i: int) -> str:
        """Convert an integer to its word representation.

        Args:
            i: The integer to convert.

        Returns:
            Word representation of the integer in the initialized locale.
        """
        return self.__impl.to_words(i=i)
