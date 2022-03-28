from functools import wraps

from util.constants_utils import ResponseCode
from util.core import response_format
from util.log_utils import sys_logger


def exception(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            sys_logger.exception(e)
            return response_format(code=ResponseCode.ERROR.value, message=str(e))
        return res

    return inner
