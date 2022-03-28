import os
import time

from celery_server import celery_app
from util.setting import conf, tmp_dir


class ExportData:
    def __init__(self):
        self.tmp_files = []

    def __del__(self):
        for file in self.tmp_files:
            if os.path.exists(file):
                print(file)
                os.remove(file)

    def worker(self, table_name):
        tmp_file = os.path.join(tmp_dir, table_name + str(int(time.time())))
        with open(tmp_file, 'w') as file:
            for i in range(10000):
                file.write('{} \r\n'.format(i))
        self.tmp_files.append(tmp_file)

def export(table_name):
    use_celery = conf.get('USE_CELERY', False)
    if use_celery:
        job = worker.apply_async((table_name,))
        return {'job_id': job.id}
    else:
        return online(table_name)

def online(table_name):
    instance = ExportData()
    instance.worker(table_name)
    return 'tmp write success'

@celery_app.task
def worker(table_name):
    online(table_name)
