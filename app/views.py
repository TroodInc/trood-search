import asyncio
import collections
from aiohttp import web

from app.events.manager import get_events
from app.exceptions import ValidationError, APIException
from app.serializers import DateRangeSerializer


class BaseView(web.View):
    @asyncio.coroutine
    def __iter__(self):
        try:
            response = yield from super(BaseView, self).__iter__()
        except APIException as e:
            if isinstance(e.message, str):
                message = {'error': e.message}
            elif isinstance(e.message, collections.Mapping) or isinstance(e.message, collections.Sequence):
                message = e.message
            else:
                message = "Can't serialize {} to dict or list".format(type(e.message).__name__)
                raise TypeError(message)
            return web.json_response(message, status=e.status_code)
        return response


class LoginRequiredView(BaseView):
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

