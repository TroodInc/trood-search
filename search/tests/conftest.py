import pytest

from search.server import init


@pytest.fixture
def app():
    app = init([])
    return app


@pytest.fixture
def client(loop, aiohttp_client, app):
    return loop.run_until_complete(aiohttp_client(app))
