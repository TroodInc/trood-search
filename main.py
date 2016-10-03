import aiopg
import yaml
import argparse
from aiohttp import web

from app.router import setup_routes


DSN = 'dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}'


async def db_middleware(app, handler):
    async def middleware(request):
        project_name = request.match_info.route.name.split(':')[0]
        if project_name == 'topline':
            if not app.get('topline_db'):
                app['topline_db'] = await aiopg.create_pool(app['topline_dsn'])
            request['db'] = app['topline_db']
        return await handler(request)
    return middleware


def start_app(port):
    app = web.Application(middlewares=[db_middleware])
    with open("config/topline.yaml", 'r') as stream:
        topline_config = yaml.load(stream)
        app['topline_dsn'] = DSN.format(**topline_config)
    setup_routes(app)
    web.run_app(app, port=port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', help='Port, on which server will be serving')
    args = parser.parse_args()
    port = int(args.port) if args.port else 80
    start_app(port)
