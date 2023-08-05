import os
import logging
import logging.handlers
from jim.config import LOGGING_LEVEL


def init_logging(path):
    """Инициализация логгера"""
    # path = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, 'server.log')

    logger = logging.getLogger('server')
    formatter = logging.Formatter("%(asctime)-25s %(filename)-30s "
                                  "%(levelname)-10s %(message)s")

    fh = logging.handlers.TimedRotatingFileHandler(
        path, when='D', interval=1, backupCount=5, encoding='utf-8')
    fh.setLevel(LOGGING_LEVEL)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.setLevel(LOGGING_LEVEL)


class Log:
    """Класс для логирования вызова функций"""
    logger = logging.getLogger('server')

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            f = func(*args, **kwargs)
            self.logger.debug(f'Module: {func.__module__}, '
                              f'function: {func.__name__}, '
                              f'args: {args}, kwargs: {kwargs}')
            return f
        return wrapped


if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setLevel(LOGGING_LEVEL)
    # console.setFormatter(formatter)
    # logger.addHandler(console)
    # logger.info('Тестовый запуск логирования')
    # logger.debug('Тестовый запуск логирования')
    # logger.critical('Тестовый запуск логирования')
