import os
import uuid
import json
import logging
import hashlib
import hmac
import base64

from aiohttp import ClientSession, web
from aiohttp.client_exceptions import ClientResponseError


logger = logging.getLogger(__name__)


def get_service_token(domain, secret):
    key = hashlib.sha1(b'trood.signer' + secret.encode('utf-8')).digest()
    signature = hmac.new(key, msg=domain.encode('utf-8'), digestmod=hashlib.sha1).digest()
    signature = base64.urlsafe_b64encode(signature).strip(b'=')
    return f'Service {domain}:{signature.decode("utf-8")}'


async def check_token(host, service_token, token):
    if not token:
        return None

    url = f'{host}/api/v1.0/verify-token'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': service_token
    }

    parts = token.split()
    token_type = "service" if parts[0] == "Service" else "user"

    user = None
    async with ClientSession(headers=headers) as session:
        response = await session.post(url, json={
            "type": token_type,
            "token": parts[1]
        })
        if response.status == 200:
            data = await response.json()
            user = data['data']

    return user


@web.middleware
async def trood_auth(request, handler):
    settings = request.app['settings']
    is_white_url = request.path in settings.EXCEPT_URLS.split(',')
    if is_white_url:
        return await handler(request)

    user_token = request.headers.get('Authorization')
    service_token = get_service_token(settings.AUTH_DOMAIN, settings.AUTH_SECRET)
    user = await check_token(settings.AUTH_URL, service_token, user_token)
    if user:
        request['user'] = user
        return await handler(request)

    return web.json_response({"error": "Authorization failed"}, status=403)
