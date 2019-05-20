import logging
from config import Config
from aiohttp import web

from router import routes

config = Config()
logging.basicConfig(filename=config.LOG_FILE, filemode='w', level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger(__name__)


def main():
    app = web.Application()
    app.add_routes(routes)

    logger.info('Starting app...')
    web.run_app(app, port=config.PORT)


if __name__ == '__main__':
    main()
