from flask import Blueprint

from util.core import response_format
from util.decorator_utils import exception
from app.worker.export_worker import export

test = Blueprint('test', __name__, url_prefix='/test')


@test.route('/', methods=['GET'])
@exception
def func():
    return response_format(data='test example')

@test.route('/export', methods=['GET'])
@exception
def export_data():
    response = export('export_job')
    return response_format(data=response)