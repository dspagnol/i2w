class Converter:

    def __init__(self, locale_: str = '') -> None:

        from ._converter import ConverterImpl
        from ._constants import ConverterImplTypeValue
        from ._converter import ConverterRegistrar
        from ._localization import Localization
        from ._logging import logger

        localization: Localization = Localization(locale_=locale_)
        impl_type: ConverterImplTypeValue = localization.get_impl_type()
        logger.debug('converter: %s', str(impl_type))
        self.__impl: ConverterImpl = ConverterRegistrar.get_class(type_id=impl_type)(localization=localization)

    def to_words(self, i: int) -> str:
        return self.__impl.to_words(i=i)
