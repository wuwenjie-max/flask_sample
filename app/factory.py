import os

import redis
import redis_lock
from flask import Blueprint, Flask
from flask_apscheduler import APScheduler

from app.router import router
from util.log_utils import sys_logger as logger
from util.core import JSONEncoder, db, read_yaml
from util.setting import base_path


def create_app(config_name='development'):
    app = Flask(__name__)

    os.chdir(base_path)
    logger.info('current work path: {}'.format(base_path))
    config_path = os.path.join(base_path, 'config/config.yaml')

    # 读取配置文件
    conf = read_yaml(config_name, config_path)
    app.config.update(conf)

    # 注册api
    register_api(app, router)
    logger.info(app.url_map)

    # 规范输出
    app.json_encoder = JSONEncoder

    # 数据库连接
    db.app = app
    db.init_app(app)

    # crontab job
    if app.config.get("SCHEDULER_OPEN"):
        scheduler_init(app)

    # log config
    if not os.path.exists(app.config['LOGGING_PATH']):
        os.mkdir(app.config['LOGGING_PATH'])

    # create tmp dir
    if not os.path.exists(app.config['TMP_DIR']):
        os.mkdir(app.config['TMP_DIR'])

    return app


class Config:
    SCHEDULER_API_ENABLED = True
    JOBS = []


def scheduler_init(app):
    """
    保证系统只启动一次定时任务
    所有的server 需在120s内一起启动
    :param app:
    :return:
    """
    scheduler = APScheduler()
    conf = Config()
    conf.JOBS = app.config.get('JOBS')
    app.config.from_object(conf)
    with redis.Redis(
        host=app.config.get('REDIS_HOST'),
        port=app.config.get('REDIS_PORT'),
        decode_responses=True,
        db=app.config.get('REDIS_DB'),
        username=app.config.get('REDIS_USER'),
        password=app.config.get('REDIS_PASS'),
    ) as conn:
        lock = redis_lock.Lock(conn, 'scheduler_init_key', expire=10)
        if lock.acquire(blocking=False):
            scheduler.init_app(app)
            scheduler.start()
            app.logger.info('Scheduler Started,---------------')


def register_api(app, routers):
    '''
    注册接口
    '''
    for router_api in routers:
        if isinstance(router_api, Blueprint):
            app.register_blueprint(router_api)
        else:
            raise ValueError('api router register error')
