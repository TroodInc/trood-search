from adapters.topline import views


def setup_routes(app):
    app.router.add_route('*', '/api/topline/pipeline/', views.ToplinePipelineView)
