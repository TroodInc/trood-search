import os

from databases import Database

database = Database(os.environ.get("SPHINX_DB", "mysql://127.0.0.1:9306/"))


async def startup(app):
    app.database = database
    await app.database.connect()


async def shutdown(app):
    await app.database.disconnect()
