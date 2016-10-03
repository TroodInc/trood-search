import aiopg
import yaml
import argparse
from aiohttp import web

from app.router import setup_routes


DSN = 'dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}'


async def db_middleware(app, handler):
    async def middleware(request):
        if app.get('topline_db'):
            request['topline_db'] = app['topline_db']
        elif app.get('topline_dsn'):
            app['topline_db'] = await aiopg.create_pool(app['topline_dsn'])
            request['topline_db'] = app['topline_db']
        return await handler(request)
    return middleware


def start_app(port):
    app = web.Application(middlewares=[db_middleware])
    try:
        with open("config/topline.yaml", 'r') as stream:
            topline_config = yaml.load(stream)
            app['topline_dsn'] = DSN.format(**topline_config)
    except FileNotFoundError:
        pass
    setup_routes(app)
    web.run_app(app, port=port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', help='Port, on which server will be serving')
    args = parser.parse_args()
    port = int(args.port) if args.port else 80
    start_app(port)
