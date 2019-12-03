import asyncio
import logging

from aiohttp import ClientSession

from ..database import database
from . import BaseEngine

logger = logging.getLogger(__name__)


class Engine(BaseEngine):
    """ Sphinx search engine interface. """

    def __init__(self, index, app):
        self.app = app
        self.database = database
        self.indexes = index.split(",")
        self.meta_query = "SHOW META"

    async def search(self, select, match, limit):
        """ Search data in index by given parameters. """
        indexes = (
            self._search_index(i, select, match, limit)
            for i in self.indexes[:]
        )
        results = await asyncio.gather(*indexes)
        return results

    async def create(self, query):
        """ Create a new record in the index. """
        query = self._generate_touch_query("INSERT", query)
        return await database.execute(query=query)

    async def update(self, query):
        """ Update the exists record in the index. """
        query = self._generate_touch_query("REPLACE", query)
        return await database.execute(query=query)

    async def delete(self, query):
        """ Delete the exists record in the index. """
        query = f"DELETE FROM {self.indexes[0]} WHERE id={query['id']}"
        return await database.execute(query=query)

    async def _search_index(self, index, select, match, limit):
        snippet = self.app.snippets.get(index, "")
        if snippet != "":
            snippet = snippet.format(match=match)

        query = f"select {select}{snippet} from {index} where match('{match}') limit {limit}"
        results = await self.database.fetch_all(query=query)
        meta = await self.database.fetch_all(query=self.meta_query)
        meta = dict(meta)
        attrs, matches = await self._split_on_attrs_and_matches(results)
        result = {"meta": meta, "attrs": attrs, "matches": matches}
        return result

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

    def _generate_touch_query(self, name, query):
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
        return f"{name} INTO {self.indexes[0]} ({columns}) VALUES ({values})"
