import logging
from config_base import ConfigBase


class Config(ConfigBase):
    PORT = 7000

    # Logging
    LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = None

    STORE_NONE_WPROSZAIM = True

    DB_URI = 'sqlite:///data.db'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
