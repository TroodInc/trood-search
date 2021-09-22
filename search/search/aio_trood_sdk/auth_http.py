import base64
import hashlib
import hmac
import json
import logging
import os
import uuid
from typing import Optional
from urllib.parse import urlparse

from aiohttp import ClientSession, web
from aiohttp.client_exceptions import ClientResponseError
from fastapi import HTTPException
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security import APIKeyHeader
from starlette.requests import Request


def get_service_token(domain, secret):
    key = hashlib.sha1(b"trood.signer" + secret.encode("utf-8")).digest()
    signature = hmac.new(
        key, msg=domain.encode("utf-8"), digestmod=hashlib.sha1
    ).digest()
    signature = base64.urlsafe_b64encode(signature).strip(b"=")
    return f'Service {domain}:{signature.decode("utf-8")}'


async def check_token(token):
    if not token:
        return None

    url = f"{os.environ.get('AUTH_URL', 'http://auth:8000')}/api/v1.0/verify-token"
    headers = {
        "Content-Type": "application/json",
        "Authorization": get_service_token(
            os.environ.get("AUTH_DOMAIN", "SEARCH"),
            os.environ.get("AUTH_SECRET", "AUTH_SECRET",),
        ),
    }

    parts = token.split()
    token_type = "service" if parts[0] == "Service" else "user"

    user = None
    async with ClientSession(headers=headers) as session:
        response = await session.post(
            url, json={"type": token_type, "token": parts[1]}
        )
        if response.status == 200:
            data = await response.json()
            user = data["data"]

    return user


class TrooAuthHeader(APIKeyHeader):
    async def __call__(self, request: Request) -> Optional[str]:
        white_urls = os.environ.get("WHITE_URLS", "").split(",")
        parsed_url = urlparse(str(request.url))
        if parsed_url.path in white_urls:
            return True

        token: str = request.headers.get(self.model.name)
        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=403, detail="Not authenticated"
                )
            else:
                return None
        else:
            user = await check_token(token)

        return user


trood_auth = TrooAuthHeader(name="Authorization")
