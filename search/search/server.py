import asyncio
import logging
import logging.handlers
import sys
import os

import uvloop

from aiohttp import web

from search import routes, settings
from search.aio_trood_sdk.auth_http import trood_auth

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def init(args):
    """ Init application. """
    app_settings = settings.setup()
    if app_settings.SENTRY_ENABLED:
        import sentry_sdk
        from sentry_sdk.integrations.aiohttp import AioHttpIntegration

        sentry_sdk.init(
            dsn=app_settings.SENTRY_DSN, integrations=[AioHttpIntegration()]
        )

    app = web.Application(middlewares=[trood_auth])
    app['settings'] = app_settings
    routes.setup(app)
    return app


def main(argv):
    logging.basicConfig(
        format='%(levelname)s | %(asctime)s | %(name)s:%(lineno)s | %(message)s',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()]
    )
    loop = asyncio.get_event_loop()

    app = init(argv)
    
    try:
        web.run_app(app, host=app['settings'].HOST, port=app['settings'].PORT)

    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if __name__ == '__main__':
    main(sys.argv[1:])
