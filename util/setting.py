import os

from util.core import read_yaml

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(base_path, 'config/config.yaml')

conf = read_yaml('common', config_path)
tmp_dir = conf.get('TMP_DIR')
logger_level = conf.get('LOGGING_LEVEL')
