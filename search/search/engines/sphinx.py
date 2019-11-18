import asyncio
import uuid
import json
import logging

from aiohttp import ClientSession, web
from aiohttp.client_exceptions import ClientResponseError


logger = logging.getLogger(__name__)


async def search(request):
    """  """
    settings = request.app['settings']
    search_data = get_search_data(request.query, settings)
    collect_data = await get_collect_data(search_data, settings)
    return collect_data


def get_search_data(query, settings):
    indexes = query.getall('index', [])
    if not indexes:
        indexes = settings.SEARCH_INDEXES.split(',')

    match = query.get('match', None)
    if match is None:
        match = ''
    
    select = query.get('select', None)
    if select is None:
        select = '*'
    
    limit = query.get('limit', None)
    if limit is None:
        limit = '0,10'
    
    data = {
        'indexes': indexes,
        'match': match,
        'select': select,
        'limit': limit
    }
    return data


async def get_collect_data(search_data, settings):
    host = settings.SPHINX_URL
    results = await asyncio.gather(
        *[sphinx(i, host, search_data) for i in search_data['indexes'][:]]
    )
    return results


async def sphinx(index, host, data):
    data['index'] = index
    return await sphinxsearch(host, data)


async def sphinxsearch(host, query):
    # url = f'{host}search/'
    # data = '&'.join(f'{k}={v}' for k,v in query.items())
    url = f'{host}sql/'
    data = f'query={make_sql(query)}'
    async with ClientSession() as session:
        response = await session.post(url, data=data)
        if response.status == 200:
            results = await response.json()
        else:
            response = await response.text()
            logger.warn(response)
            results = {'searchengine': 'error'}

    return results


def make_sql(query):
    sql = f'select {query["select"]} from {query["index"]} where match(\'{query["match"]}\') limit {query["limit"]}'
    return sql
