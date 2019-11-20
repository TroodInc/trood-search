from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from .database import database
from .views import router


app = FastAPI(
    title="TROOD search API",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs/",
    redoc_url=None,
    version="1.1.1",
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router)
