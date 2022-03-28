import datetime

from loguru import logger

from app.models.models import User
from util.core import db


def my_job():
    curr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info('curr time: {}, my job success'.format(curr))


def db_query():
    with db.app.app_context():
        data = db.session.query(User).first()
        logger.info(data)
