import os

from databases import Database

database = Database(os.environ.get("SPHINX_DB", "mysql://127.0.0.1:9306/"))
