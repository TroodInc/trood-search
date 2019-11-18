import os
import importlib

from search import views


def setup(app):
    app.router.add_get('/', views.search)
    app.router.add_get('/ping/', views.ping)
