from aiohttp import web

from adapters.mirror.authentication import MirrorAuthentication
from adapters.mirror.reports.manager import get_projects_for_manager, get_summary_reports, get_dynamic_reports
from adapters.mirror.reports.serializers import DynamicReportSerializer, SummaryReportSerializer
from app.views import LoginRequiredView


class DynamicReportView(LoginRequiredView):
    authentication_class = MirrorAuthentication

    async def get(self):
        project_id_list = await get_projects_for_manager(self.request['user_id'], self.request['db'])
        reports = await get_dynamic_reports(project_id_list, self.request)
        return web.json_response(reports, status=200)

    async def post(self):
        data = await self.request.json()
        serializer = DynamicReportSerializer(data, many=True)
        serializer.is_valid()
        await serializer.save(self.request['cache'])
        return web.json_response(status=200)


class SummaryReportView(LoginRequiredView):
    authentication_class = MirrorAuthentication

    async def get(self):
        project_id_list = await get_projects_for_manager(self.request['user_id'], self.request['db'])
        reports = await get_summary_reports(project_id_list, self.request)
        return web.json_response(reports, status=200)

    async def post(self):
        data = await self.request.json()
        serializer = SummaryReportSerializer(data, many=True)
        serializer.is_valid()
        await serializer.save(self.request['cache'])
        return web.json_response(status=200)

