import asyncio
from aiohttp import web

from app.events.manager import get_events
from app.exceptions import ValidationError
from app.serializers import DateRangeSerializer


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


class EventListView(web.View):
    async def get(self):
        serializer = DateRangeSerializer(data=self.request.GET)
        try:
            serializer.is_valid()
        except ValidationError as e:
            return web.json_response(e.message, status=400)
        date_from = serializer.validated_data.get('date_from')
        date_to = serializer.validated_data.get('date_to')
        events = await get_events(date_from, date_to, self.request['cache'])
        return web.json_response(events)

