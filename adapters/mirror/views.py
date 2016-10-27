from aiohttp import web

from adapters.mirror.reports import generators
from adapters.mirror.reports.serializers import DynamicReportSerializer, SummaryReportSerializer
from app.views import LoginRequiredView, BaseView


class PlaceReportView(BaseView):
    async def get(self):
        project_id = self.request.GET.get('project_id')
        place_id = self.request.GET.get('place_id')
        report = await generators.generate_base_place_report(
            project_id=project_id,
            place_id=place_id,
            pool=self.request['db'],
            cache=self.request['cache']
        )
        return web.json_response(report)


class DynamicReportView(BaseView):
    async def post(self):
        data = await self.request.json()
        serializer = DynamicReportSerializer(data, many=True)
        serializer.is_valid()
        await serializer.save(self.request['cache'])
        return web.json_response(status=200)


class SummaryReportView(BaseView):
    async def post(self):
        data = await self.request.json()
        serializer = SummaryReportSerializer(data, many=True)
        serializer.is_valid()
        await serializer.save(self.request['cache'])
        return web.json_response(status=200)

