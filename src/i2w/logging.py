import logging


# Convinience logging filter class.
class LoggingDebugFilter(logging.Filter):

    def __init__(self, debug_level: int) -> None:
        self.__debug_level = debug_level

    def filter(self, record) -> bool:
        to_be_logged: bool = True
        if record.levelno == logging.DEBUG:
            if not hasattr(record, 'debug_level'):
                record.debug_level = 0
            to_be_logged = (record.debug_level <= self.__debug_level)
            record.msg = ('  ' * record.debug_level) + record.msg
        return to_be_logged
