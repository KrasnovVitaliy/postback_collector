import logging
from config_base import ConfigBase


class Config(ConfigBase):
    PUBLIC_HOST = "51.158.176.243"
    PORT = 7000

    # Logging
    LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = None

    DB_URI = 'sqlite:////root/postback_collector.db'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
