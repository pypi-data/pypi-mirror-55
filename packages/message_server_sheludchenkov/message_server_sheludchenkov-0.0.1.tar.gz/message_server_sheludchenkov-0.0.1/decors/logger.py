import logging
from loggers.server_log_config import init_logging


init_logging()
logger = logging.getLogger('server')


class Log:
    def __call__(self, func):
        def wrapped(*args, **kwargs):
            f = func(*args, **kwargs)
            logger.debug(f'Module: {func.__module__}, '
                         f'function: {func.__name__}, '
                         f'args: {args}, kwargs: {kwargs}')
            return f
        return wrapped
