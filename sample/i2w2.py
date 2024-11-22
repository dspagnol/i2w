import logging

from i2w import Converter
from i2w import LoggingDebugFilter


logging.basicConfig(level=logging.INFO)

converter = Converter('fr_CA')

print(converter.to_words(200123))

logging_filter = LoggingDebugFilter(debug_level=2)
for handler in logging.root.handlers:
    handler.addFilter(logging_filter)
logging.getLogger().setLevel(logging.DEBUG)

print(converter.to_words(123))
