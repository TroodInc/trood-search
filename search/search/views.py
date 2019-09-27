import asyncio
import json
import logging

from aiohttp import web
from search.engines import sphinx


logger = logging.getLogger(__name__)


async def ping(request):
    """ ping - pong view. """
    return web.json_response('pong')


async def search(request):
    """ search view. """
    results = await sphinx.search(request)
    return web.json_response(results)
