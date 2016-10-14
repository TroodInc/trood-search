from aiohttp import web

from adapters.topline.authentication import ToplineAuthentication
from adapters.topline.reports import generators
from app.exceptions import ValidationError
from app.serializers import DateRangeSerializer
from app.views import LoginRequiredView


class PipelineView(LoginRequiredView):
    authentication_class = ToplineAuthentication

    async def get(self):
        serializer = DateRangeSerializer(data=self.request.GET)
        try:
            serializer.is_valid()
        except ValidationError as e:
            return web.json_response(e.message, status=400)

        date_from = serializer.validated_data.get('date_from')
        date_to = serializer.validated_data.get('date_to')
        report = await generators.get_pipeline_report(date_from, date_to, request=self.request)
        return web.json_response(report)
