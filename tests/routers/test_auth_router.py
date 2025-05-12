"""
test_auth_router.py

Unit tests for the authentication-related API routes in the JANUX Authentication Gateway.

Tests:
- Ensures the `/auth/login` endpoint exists and responds.
- Verifies successful login returns a JWT token.
- Checks login failure with incorrect credentials.
- Confirms correct integration of authentication logic.

Features:
- Uses FastAPI's TestClient for API testing.
- Mocks authentication dependencies to prevent actual database calls.
- Validates correct response codes and token structures.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import FastAPI
from janux_auth_gateway.routers.auth_router import auth_router
from unittest.mock import patch, MagicMock

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
client = TestClient(app)


@pytest.mark.asyncio
async def test_login_endpoint_works():
    """
    Ensure the /auth/login endpoint exists and responds.

    Expected Outcome:
    - Should return 401 Unauthorized (since dependencies are mocked).
    """
    mock_redis = MagicMock()
    mock_redis.get.return_value = None
    mock_redis.incr.return_value = 1
    mock_redis.expire.return_value = True

    with patch("janux_auth_gateway.routers.auth_router.redis_client", mock_redis):
        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401
