import os

from celery import Celery

from util.setting import conf


def task_files():
    file_paths = []
    bash_path = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk(bash_path):
        if len(set(root.split('/')).intersection({'.git', 'venv', '__pycache__'})) > 0:
            continue
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    py_files = [file[:-3] for file in file_paths if file[-3:] == '.py']
    py_files = [
        file.replace(bash_path + '/', '').replace('/', '.') for file in py_files
    ]
    py_files.remove('celery_server')
    return py_files


py_files = task_files()
celery_app = Celery('celery_server', broker=conf.get('BROKER_URL'), include=py_files)
celery_app.config_from_object(conf)


if __name__ == '__main__':
    # cmd celery -A celery_server worker -l INFO -c 4 -D -f ./celery.log --pidfile celery.pid
    celery_app.start()
    # task_files()
