import logging
import json

from fastapi import Depends
from fastapi.routing import APIRouter
from starlette import status
from starlette.responses import JSONResponse
from starlette.requests import Request

from .engines.sphinx import Engine

from .aio_trood_sdk.auth_http import trood_auth

logger = logging.getLogger(__name__)


router = APIRouter()


async def token_parameter(token: str = Depends(trood_auth)):
    return token


@router.get("/", tags=["health check"])
async def health_check():
    return {"status": "OK"}


@router.get("/search/", tags=["search"])
async def search(
    index: str = "",
    select: str = "*",
    match: str = "",
    limit: str = "0,10",
    token: str = Depends(token_parameter),
):
    """ Full-text search endpoint. """
    engine = Engine(index)
    results = await engine.search(select, match, limit)
    if len(results) == 1:
        results = results[0]

    return results


@router.post(
    "/index/",
    tags=["index"],
    responses={403: {"description": "Not authenticated"}},
)
async def index(request: Request, token: str = Depends(token_parameter)):
    """
    RT index actions endpoint.

    Event must be valid for custodian event schema
    Index naming rule
    rt_ + event.object + _index

    TODO: Implement batch/many/bulk operation
    TODO: Validation refactoring
    """

    async def is_valid():
        errors = []
        try:
            event = await request.json()
        except json.decoder.JSONDecodeError:
            event = {}

        if "action" not in event:
            errors.append({"action": "is required"})
        elif event["action"] not in ("create", "update", "delete"):
            errors.append({"action": "must be one of create, update, delete"})

        if "object" not in event:
            errors.append({"object": "is required"})

        if "current" not in event:
            errors.append({"current": "is required"})

        if "previous" not in event:
            errors.append({"previous": "is required"})

        return event, errors

    event, errors = await is_valid()
    if errors:
        return JSONResponse(errors, status_code=400)

    engine = Engine(f"rt_{event['object']}_index")
    result = None
    if event["action"] == "create":
        result = await engine.create(event["current"])
    elif event["action"] == "update":
        result = await engine.update(event["current"])
    elif event["action"] == "delete":
        result = await engine.delete(event["previous"])

    return result
