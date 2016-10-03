import asyncio
from aiohttp import web


class LoginRequiredView(web.View):
    authentication_class = None

    @asyncio.coroutine
    def __iter__(self):
        authenticated = yield from self.authentication_class(self.request).authenticate()
        if not authenticated:
            return web.json_response({
                'error': 'invalid credentials provided'
            }, status=401)
        response = yield from super(LoginRequiredView, self).__iter__()
        return response

