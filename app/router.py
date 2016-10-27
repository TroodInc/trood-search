from adapters.topline import views as topline_views
from adapters.mirror import views as mirror_views
from app import views as dashboard_views


def setup_routes(app):
    app.router.add_route('*', '/dashboard/events/', dashboard_views.EventListView, name='dashboard:events')
    app.router.add_route('*', '/topline/pipeline/', topline_views.PipelineView, name='topline:pipeline')
    app.router.add_route('*', '/mirror/place/', mirror_views.PlaceReportView, name='mirror:place')
    app.router.add_route('*', '/mirror/summary/', mirror_views.SummaryReportView, name='mirror:summary')
    app.router.add_route('*', '/mirror/dynamic/', mirror_views.DynamicReportView, name='mirror:dynamic')
