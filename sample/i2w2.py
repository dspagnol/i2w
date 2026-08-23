import logging

import i2w


logging.basicConfig(level=logging.INFO)

converter = i2w.Converter(locale_name="fr_CA")

print(converter.to_words(i=200123))

logging_filter = i2w.LoggingDebugFilter(debug_level=2)
for handler in logging.root.handlers:
    handler.addFilter(filter=logging_filter)
logging.getLogger().setLevel(level=logging.DEBUG)

print(converter.to_words(i=123))
