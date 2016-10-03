import aiopg
import yaml
import argparse
from aiohttp import web

from app.router import setup_routes


DSN = 'dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}'


async def db_middleware(app, handler):
    async def middleware(request):
        if not app.get('db'):
            app['db'] = await aiopg.create_pool(app['dsn'])
        request['db'] = app['db']
        return await handler(request)
    return middleware


def start_app(port):
    with open("config/app.yaml", 'r') as stream:
        app_config = yaml.load(stream)
    app = web.Application(middlewares=[db_middleware])
    setup_routes(app)
    app['dsn'] = DSN.format(**app_config)
    web.run_app(app, port=port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', help='Port, on which server will be serving')
    args = parser.parse_args()
    port = int(args.port) if args.port else 80
    start_app(port)
