import asyncio
import logging

from aiohttp import ClientSession

from ..database import database
from ..parsers import RQL2SQLParser, RQL2SphinxQLParser
from . import BaseEngine

logger = logging.getLogger(__name__)


class Engine(BaseEngine):
    """
    Sphinx search engine interface.

    Events must be valid for custodian event schema

    Index naming rule
    rt_ + event.object + _index
    """

    def __init__(self, app, events=None):
        self.events = events
        self.app = app
        self.database = database
        self.meta_query = "SHOW META"

    async def process_events(self):
        # TODO: Batch processing
        for event in self.events:
            index = f"rt_{event['object']}_index"
            if event["action"] == "create":
                await self.create(index, event["current"])
            elif event["action"] == "update":
                await self.update(index, event["current"])
            elif event["action"] == "remove":
                await self.delete(index, event["previous"])

    async def search(self, index, select, search_filter, match, limit):
        """ Search data in index by given parameters. """
        snippet = self.app.snippets.get(index, "")
        search_expression = ""
        if search_filter != "":
            parser = RQL2SQLParser(search_filter)
            search_filter = f", {parser.make_query()} as search_filter"
            search_expression = " AND search_filter 1"

        if match != "*":
            parser = RQL2SphinxQLParser(match)
            match = parser.make_query()

        if snippet != "":
            snippet = snippet.format(match=match)

        query = f"select {select}{snippet}{search_filter} from {index} where match('{match}'){search_expression} limit {limit}"
        logger.info(query)
        results = await self.database.fetch_all(query=query)
        meta = await self.database.fetch_all(query=self.meta_query)
        meta = dict(meta)
        attrs, matches = await self._split_on_attrs_and_matches(results)
        result = {"meta": meta, "attrs": attrs, "matches": matches}
        return result

    async def create(self, index, query):
        """ Create a new record in the index. """
        query = self._generate_touch_query(index, "INSERT", query)
        return await database.execute(query=query)

    async def update(self, index, query):
        """ Update the exists record in the index. """
        query = self._generate_touch_query(index, "REPLACE", query)
        return await database.execute(query=query)

    async def delete(self, index, query):
        """ Delete the exists record in the index. """
        query = f"DELETE FROM {index} WHERE id={query['id']}"
        return await database.execute(query=query)

    async def _split_on_attrs_and_matches(self, results):
        attrs = []
        matches = []
        for i, result in enumerate(results):
            if i == 0:
                attrs = result.keys()

            match = []
            for key in attrs[:]:
                match.append(result[key])

            matches.append(match)

        return attrs, matches

    def _generate_touch_query(self, index, name, query):
        """ Generate INSERT, REPLACE query. """
        assert name in {"INSERT", "REPLACE"}
        columns = []
        values = []
        for key, value in query.items():
            columns.append(str(key))
            if isinstance(value, str):
                value = f"'{value}'"

            values.append(str(value))

        columns = ",".join(columns)
        values = ",".join(values)
        return f"{name} INTO {index} ({columns}) VALUES ({values})"
