from functools import wraps
from loguru import logger

from util.core import response_format


def exception(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            logger.error(str(e))
            return response_format(status=0, message=str(e))
        return res
    return inner



