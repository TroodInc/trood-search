import pytest
from typing import Optional
from urllib.parse import urlparse
from starlette.testclient import TestClient
from fastapi import HTTPException, Depends
from starlette.requests import Request

from .database import database
from .main import app
from .views import token_parameter
from .aio_trood_sdk.auth_http import TrooAuthHeader


class MockAuthHeader(TrooAuthHeader):
    async def __call__(self, request: Request) -> Optional[str]:
        white_urls = ["/search/"]
        parsed_url = urlparse(str(request.url))
        if parsed_url.path in white_urls:
            return True

        api_key: str = request.headers.get(self.model.name)
        if not api_key:
            if self.auto_error:
                raise HTTPException(
                    status_code=403, detail="Not authenticated"
                )
            else:
                return None

        return api_key


mock_auth = MockAuthHeader(name="Authorization")


@pytest.fixture
def headers():
    return {"Authorization": "Token mocktoken"}


async def override_token_parameter(token: str = Depends(mock_auth)):
    return token


@pytest.fixture
def client():
    app.dependency_overrides[token_parameter] = override_token_parameter
    with TestClient(app) as test_client:
        yield test_client
