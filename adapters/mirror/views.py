import aiohttp
from aiohttp import web

from adapters.mirror.authentication import MirrorAuthentication
from adapters.mirror.reports.manager import get_projects_for_manager, get_summary_reports, get_dynamic_reports
from adapters.mirror.reports.serializers import DynamicReportSerializer, SummaryReportSerializer
from app.views import LoginRequiredView


class MirrorProxyView(LoginRequiredView):
    authentication_class = MirrorAuthentication
    method_uri = None

    async def get(self):
        host = self.request['app']['mirror_host']
        headers = {'Authorization': self.request.headers.get('Authorization')}
        async with aiohttp.ClientSession() as client:
            async with client.get(url=host + self.method_uri, headers=headers) as response:
                data = await response.json()
        return web.json_response(data)


class DynamicReportView(MirrorProxyView):
    authentication_class = MirrorAuthentication
    method_uri = '/r/CLIENT_MANAGER/reports/chanels/data/dynamic/'

    async def post(self):
        data = await self.request.json()
        serializer = DynamicReportSerializer(data, many=True)
        serializer.is_valid()
        await serializer.save(self.request['cache'])
        return web.json_response(status=200)


class SummaryReportView(MirrorProxyView):
    method_uri = '/r/CLIENT_MANAGER/reports/chanels/data/summary/'

    async def post(self):
        data = await self.request.json()
        serializer = SummaryReportSerializer(data, many=True)
        serializer.is_valid()
        await serializer.save(self.request['cache'])
        return web.json_response(status=200)


class MirrorEventsView(MirrorProxyView):
    method_uri = '/r/CLIENT_MANAGER/reports/events/data/'


class MirrorRegularitiesView(MirrorProxyView):
    method_uri = '/r/CLIENT_MANAGER/reports/regularities/data/'

