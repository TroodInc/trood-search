import logging
from urllib.parse import urlparse

import aiomysql


logger = logging.getLogger(__name__)


def setup(app):
    app['db'] = DB(app, app['settings'].SPHINX_DSN)


class DB:
    def __init__(self, app, dsn):
        self.app = app
        self.host, self.port = urlparse(dsn).netloc.split(':')

    async def connect(self, app):
        app['pool'] = await aiomysql.create_pool(
            host=self.host, port=self.port
        )
        logger.info('Database pool was create')

    async def shutdown(self, app):
        app['pool'].close()
        await app['pool'].wait_closed()
        logger.info('Database pool was close')
