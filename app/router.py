from adapters.topline import views as topline_views


def setup_routes(app):
    app.router.add_route('*', '/topline/pipeline/', topline_views.PipelineView, name='topline:pipeline')
