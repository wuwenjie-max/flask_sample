from flask import Flask, Blueprint
import os
import yaml

from app.router import router
from util.core import JSONEncoder

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
    return app



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

