import datetime
import decimal
import os
import uuid

import yaml
from flask import jsonify
from flask.json import JSONEncoder as BaseJSONEncoder
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

from util.constants_utils import ResponseCode, ResponseMsg

scheduler = APScheduler()

db = SQLAlchemy()


class JSONEncoder(BaseJSONEncoder):
    def default(self, o):
        """
        如有其他的需求可直接在下面添加
        :param o:
        :return:
        """
        if isinstance(o, datetime.datetime):
            # 格式化时间
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            # 格式化日期
            return o.strftime('%Y-%m-%d')
        if isinstance(o, decimal.Decimal):
            # 格式化高精度数字
            return str(o)
        if isinstance(o, uuid.UUID):
            # 格式化uuid
            return str(o)
        if isinstance(o, bytes):
            # 格式化字节数据
            return o.decode("utf-8")
        return super(JSONEncoder, self).default(o)


def response_format(
    code=ResponseCode.SUCCESS.value, message=ResponseMsg.SUCCESS.value, data=[]
):
    return jsonify({'code': code, 'msg': message, 'data': data})


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
