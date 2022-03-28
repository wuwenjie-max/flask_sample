'''
签名验证
'''

import datetime
import hashlib
import time
from functools import wraps

from flask import request

from loguru import logger
from util.setting import ACCESS_KEY, SECRET_KEY
from util.core import response_format
from util.constants_utils import ResponseCode, ResponseMsg


def get_secret_key(api_key):
    '''ak sk 可以改为数据库存储'''
    if api_key == ACCESS_KEY:
        return SECRET_KEY


def check_time(request_time, gap=60 * 5):
    current_time = int(time.time())
    request_time = int(
        datetime.datetime.strptime(request_time, '%Y-%m-%d %H:%M:%S').timestamp()
    )
    if current_time >= request_time and current_time - request_time <= gap:
        return True
    else:
        return False


def generate_sign(request_param: dict, secret_key: str, current_time: str):
    def dict_to_string(param):
        out = ''
        if param:
            for key in sorted(param.keys()):
                if key in ['api_key', 'sign', 'now']:
                    continue
                value = param[key]
                if type(value) == dict:
                    out = '{}{}={}&'.format(out, str(key), dict_to_string(value))
                else:
                    out = '{}{}={}&'.format(out, str(key), str(value))
        return out

    sign_str = dict_to_string(request_param) + 'time={}'.format(current_time)
    print(sign_str)
    sha256 = hashlib.sha256(secret_key.encode('utf-8'))
    sha256.update(sign_str.encode('utf-8'))
    return sha256.hexdigest()


def check_all(api_key: str, signature: str, current_time: str, request_param: dict):
    if not api_key or not signature or not current_time:
        raise ValueError('request must have api_key,sign,now')
    if not check_time(current_time):
        raise ValueError('request time shall not exceed 5 minutes')
    secret_key = get_secret_key(api_key)
    if not secret_key:
        raise ValueError('api_key not found')
    auth_sign = generate_sign(request_param, secret_key, current_time)
    if not auth_sign == signature:
        raise ValueError('sign unqualified')


def api_auth(func):
    @wraps(func)
    def inner(*args, **kwargs):
        api_key = request.args.get('api_key')
        signature = request.args.get('sign')
        current_time = request.args.get('now')
        try:
            request_param = request.args.to_dict()
            if request.method != 'GET':
                body = request.form.to_dict() or request.json or request.get_data()
                if body:
                    if type(body) == dict:
                        request_param.update(body)
                    else:
                        request_param.update({'body': body.decode('utf-8')})
            request_param.update(kwargs)
            check_all(api_key, signature, current_time, request_param)
        except Exception as e:
            logger.error('auth failed: {}'.format(str(e)))
            return response_format(code=ResponseCode.ALTH.value, message=ResponseMsg.ALTH.value)
        res = func(*args, **kwargs)
        return res

    return inner
