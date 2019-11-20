import asyncio
import logging

from ..database import database

logger = logging.getLogger(__name__)


class Engine:
    def __init__(self, index):
        self.database = database
        self.indexes = index.split(",")

    async def search(self, select, match, limit):
        indexes = (
            self.search_index(i, select, match, limit) for i in self.indexes[:]
        )
        results = await asyncio.gather(*indexes)
        return results

    async def search_index(self, index, select, match, limit):
        query = f"select {select} from {index} where match('{match}') limit {limit}"
        return await self.database.fetch_all(query=query)

    async def create(self, query):
        query = self.make_touch_query("INSERT", query)
        return await database.execute(query=query)

    async def update(self, query):
        query = self.make_touch_query("REPLACE", query)
        return await database.execute(query=query)

    async def delete(self, query):
        query = f"DELETE FROM {self.indexes[0]} WHERE id={query['id']}"
        return await database.execute(query=query)

    def make_touch_query(self, name, query):
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
