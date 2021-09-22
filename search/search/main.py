from fastapi import FastAPI

from . import database, snippets
from .middlewares import SearchErrorMiddleware
from .views import router

app = FastAPI(
    title="TROOD search API",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs/",
    redoc_url=None,
    version="1.1.1",
)

app.error_middleware = SearchErrorMiddleware(
    app.exception_middleware, debug=app._debug
)


@app.on_event("startup")
async def startup():
    await database.startup(app)
    snippets.setup(app)


@app.on_event("shutdown")
async def shutdown():
    await database.shutdown(app)


app.include_router(router)
