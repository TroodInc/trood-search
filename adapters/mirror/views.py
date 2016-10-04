from aiohttp import web

from adapters.mirror.reports import generators
from app.views import LoginRequiredView


class SummaryReportView(web.View):
    async def get(self):
        project_id = self.request.GET.get('project_id')
        report = await generators.get_summary_report(project_id, self.request)
        return web.json_response(report)


class PlaceReportView(web.View):
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
