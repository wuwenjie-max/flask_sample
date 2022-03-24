from flask import Blueprint

from util.decorator_utils import exception
from util.core import response_format

test = Blueprint('test', __name__, url_prefix='/test')

@test.route('/', methods=['GET'])
@exception
def func():
    return response_format(data='test example')
