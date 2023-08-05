import os
import logging
from jim.config import LOGGING_LEVEL


def init_logging():
    """Инициализация логгера"""
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, '../logs/', 'client.log')
    logger = logging.getLogger('client')
    formatter = logging.Formatter("%(asctime)s\t%(filename)-30s "
                                  "%(levelname)-10s\t%(message)s ")

    fh = logging.FileHandler(path, encoding='utf-8')
    fh.setLevel(LOGGING_LEVEL)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.setLevel(LOGGING_LEVEL)


class Log:
    """Класс для логирования вызова функций"""
    logger = logging.getLogger('client')

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            f = func(*args, **kwargs)
            self.logger.debug(f'Module: {func.__module__}, '
                              f'function: {func.__name__}, '
                              f'args: {args}, kwargs: {kwargs}')
            return f
        return wrapped


if __name__ == '__main__':
    init_logging()
    # console = logging.StreamHandler()
    # console.setLevel(LOGGING_LEVEL)
    # console.setFormatter(formatter)
    # logger.addHandler(console)
    # logger.info('Тестовый запуск логирования')
    # logger.debug('Тестовый запуск логирования')
    # logger.critical('Тестовый запуск логирования')
