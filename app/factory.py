from flask import Flask, Blueprint
from flask_apscheduler import APScheduler
import os
import yaml
import redis
import redis_lock

from app.router import router
from util.core import JSONEncoder, db

def create_app(config_name='development'):
    app = Flask(__name__)
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config/config.yaml')

    # 读取配置文件
    conf = read_yaml(config_name, config_path)
    app.config.update(conf)

    # 注册api
    register_api(app, router)

    # 规范输出
    app.json_encoder = JSONEncoder

    # 数据库连接
    db.app = app
    db.init_app(app)

    # crontab job
    if app.config.get("SCHEDULER_OPEN"):
        scheduler_init(app)

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
    with redis.Redis(host=app.config.get('REDIS_HOST'), port=app.config.get('REDIS_PORT'), decode_responses=True, db=app.config.get('REDIS_DB'), username=app.config.get('REDIS_USER'), password=app.config.get('REDIS_PASS')) as conn:
        lock = redis_lock.Lock(conn, 'scheduler_init_key', expire=10)
        if lock.acquire(blocking=False):
            scheduler.init_app(app)
            scheduler.start()
            app.logger.info('Scheduler Started,---------------')


def read_yaml(config_name, config_path):
    '''
    :param config_name: 配置名
    :param config_path: 配置文件路径
    :return:
    '''
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            conf = yaml.safe_load(file.read())
            if config_name.upper() in conf.keys():
                return conf[config_name.upper()]
            else:
                raise KeyError("config_name not found, please check it")
    else:
        raise KeyError('config path not found, {}'.format(config_path))


def register_api(app, routers):
    for router_api in routers:
        if isinstance(router_api, Blueprint):
            app.register_blueprint(router_api)
        else:
            raise ValueError('api router register error')

