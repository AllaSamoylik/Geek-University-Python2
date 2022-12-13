import inspect
import logging
from functools import wraps


def log(logger):
    def log_deco(func):
        @wraps(func)
        def debug_log(*args, **kwargs):
            parent_f = inspect.stack()[1][3]
            logger.debug(f'Функция {func.__name__}() вызвана из функции {parent_f}() '
                         f'с аргументами {args}, {kwargs}')
            return func(*args, **kwargs)
        return debug_log
    return log_deco
