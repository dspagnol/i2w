import logging


logger = logging.LoggerAdapter(logging.getLogger(__name__))
logger_d1 = logging.LoggerAdapter(logging.getLogger(__name__), {'debug_level': 1})
logger_d2 = logging.LoggerAdapter(logging.getLogger(__name__), {'debug_level': 2})
logger_d3 = logging.LoggerAdapter(logging.getLogger(__name__), {'debug_level': 3})
