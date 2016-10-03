import asyncio
from aiohttp import web

from adapters.topline.authentication import is_authenticated
from adapters.topline.reports import generators
from app.serializers import DateRangeSerializer


class ToplineView(web.View):
    @asyncio.coroutine
    def __iter__(self):
        if not self.request.get('topline_db'):
            return web.json_response({
                'error': 'topline database config is not provided'
            }, status=500)
        authenticated = yield from is_authenticated(self.request)
        if not authenticated:
            return web.json_response({
                'error': 'invalid credentials provided'
            }, status=401)
        response = yield from super(ToplineView, self).__iter__()
        return response


class PipelineView(ToplineView):
    async def get(self):
        serializer = DateRangeSerializer(data=self.request.GET)
        try:
            serializer.is_valid()
        except ValueError:
            self.request['db'].close()
            return web.json_response(status=400)

        date_from = serializer.validated_data.get('date_from')
        date_to = serializer.validated_data.get('date_to')
        report = await generators.get_pipeline_report(date_from, date_to, request=self.request)
        return web.json_response(report)
