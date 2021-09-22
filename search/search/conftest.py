from typing import Optional
from urllib.parse import urlparse

import pytest
from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.testclient import TestClient

from .aio_trood_sdk.auth_http import TrooAuthHeader
from .main import app
from .views import token_parameter


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


@pytest.fixture
def big_text():
    text = """
        This article covers the system architecture of the Trood Core platform and intended to provide a general understanding of how Trood-based software is being developed and supported.
        The material is designed for system engineers with an advanced technology background, though using the links provided and other TCP materials any interested researcher can make his way to a full understanding of the key concepts.
        The architecture of Trood Core is designed to fully comply with Trood Key Concepts. We won’t repeat the information here and just dive into technical details.
    """
    yield text
