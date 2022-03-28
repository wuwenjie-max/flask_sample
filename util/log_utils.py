import sys
from functools import lru_cache

from loguru import logger as office_logger

from util.setting import logger_level

_format = (
    '<g>{time:YYYY-MM-DD HH:mm:ss}</g> '
    '| <level>{level: <8}</level> '
    '| <e>{thread.name: <10}</e> '
    '| <fg #CF55E8>{extra[utc]: <18}</fg #CF55E8>'
    '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> '
    '- <level>{message}</level>'
)

office_logger.remove(0)
office_logger.add(sys.stderr, format=_format, level=logger_level)


@lru_cache()
def job_logger(job_id):
    return office_logger.patch(lambda record: record["extra"].update(utc=job_id))


sys_logger = job_logger("scheduler program")
dete_logger = job_logger("detector program")