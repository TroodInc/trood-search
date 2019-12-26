import json
import logging

from fastapi import Depends
from fastapi.routing import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from .aio_trood_sdk.auth_http import trood_auth
from .engines.sphinx import Engine

logger = logging.getLogger(__name__)


router = APIRouter()


async def token_parameter(token: str = Depends(trood_auth)):
    return token


@router.get("/", tags=["health check"])
async def health_check():
    return {"status": "OK"}


@router.get("/search/", tags=["search"])
async def search(
    request: Request,
    index: str = "",
    select: str = "*",
    match: str = "''",
    limit: str = "0,10",
    token: str = Depends(token_parameter),
):
    """ Full-text search endpoint. """
    engine = Engine(request.app)
    results = await engine.search(index, select, match, limit)
    return results


@router.post(
    "/index/",
    tags=["index"],
    responses={403: {"description": "Not authenticated"}},
)
async def index(request: Request, token: str = Depends(token_parameter)):
    """
    RT index actions endpoint.
    """
    try:
        events = await request.json()
    except json.decoder.JSONDecodeError:
        return JSONResponse(
            {"status": "Error", "data": "Invalid JSON"}, status_code=400
        )

    # TODO: Validation
    engine = Engine(request.app, events['events'])
    await engine.process_events()
    return {"status": "Ok"}


@router.get(
    "/snippets/",
    tags=["snippets"],
    responses={403: {"description": "Not authenticated"}},
)
async def snippet_list(
    request: Request, token: str = Depends(token_parameter)
):
    """ Registered snippets endpoint. """
    return request.app.snippets


@router.post(
    "/snippets/",
    tags=["snippets"],
    responses={403: {"description": "Not authenticated"}},
)
async def snippet_register(
    request: Request, token: str = Depends(token_parameter)
):
    """ Register/update snippet endpoint. """
    try:
        snippet = await request.json()
    except json.decoder.JSONDecodeError:
        return JSONResponse({"error": "Unvalid JSON."}, status_code=400)

    request.app.snippets.update(snippet)
    return request.app.snippets


@router.delete(
    "/snippets/{index_name}/",
    tags=["snippets"],
    responses={403: {"description": "Not authenticated"}},
)
async def snippet_delete(
    request: Request, index_name: str, token: str = Depends(token_parameter)
):
    """ Delete registered snippet endpoint. """
    request.app.snippets.pop(index_name, None)
    return JSONResponse(status_code=204)
