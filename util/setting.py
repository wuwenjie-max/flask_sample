import os

from util.core import read_yaml

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(base_path, 'config/config.yaml')
conf = read_yaml('common', config_path)


# tmp files
tmp_dir = conf.get('TMP_DIR')

logger_level = conf.get('LOGGING_LEVEL')

#clickhouse config
BATCH_SIZE = 1000
CLICKHOUSE_DB = 'default'
CLICKHOUSE_HOST = '172.0.0.1'
CLICKHOUSE_PORT = 9000
CLICKHOUSE_USER = 'default'
CLICKHOUSE_PASS = '123456'

#minio config
MINIO_ENDPOINT = '172.0.0.1:8000'
MINIO_ACCESS_KEY = 'access_key'
MINIO_SECRET_KEY = 'secret_key'
MINIO_BUCKET_NAME = 'bucket'