from abc import ABC


class BaseEngine(ABC):
    """ Base full text index engine. """

    async def search(self, *args, **kwargs):
        """ Search data in index by given parameters. """
        raise NotImplementedError

    async def create(self, *args, **kwargs):
        """ Create a new record in the index. """
        raise NotImplementedError

    async def update(self, *args, **kwargs):
        """ Update the exists record in the index. """
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        """ Delete the exists record in the index. """
        raise NotImplementedError
