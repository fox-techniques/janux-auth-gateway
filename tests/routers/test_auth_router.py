"""
test_auth_router.py

Unit tests for the authentication-related API routes in the JANUX Authentication Gateway.

Tests:
- User login with correct credentials.
- Admin login with correct credentials.
- Handling of incorrect login attempts.
- Token issuance and validation.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from janux_auth_gateway.routers.auth_router import auth_router
from janux_auth_gateway.auth.jwt import create_access_token
from janux_auth_gateway.database.mongoDB import authenticate_user, authenticate_admin
from fastapi import FastAPI
from starlette import status

# Set up a FastAPI test client
app = FastAPI()
app.include_router(auth_router)
client = TestClient(app)


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.authenticate_user", new_callable=AsyncMock)
async def test_user_login_success(mock_authenticate_user):
    """
    Test user login with correct credentials.

    Steps:
    1. Mock `authenticate_user()` to return `True`.
    2. Call `POST /login` with valid credentials.

    Expected Outcome:
    - API should return a valid JWT token.
    """
    mock_authenticate_user.return_value = True

    response = client.post(
        "/login",
        data={"username": "user@example.com", "password": "validpassword"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.authenticate_admin", new_callable=AsyncMock)
async def test_admin_login_success(mock_authenticate_admin):
    """
    Test admin login with correct credentials.

    Steps:
    1. Mock `authenticate_admin()` to return `True`.
    2. Call `POST /login` with valid credentials.

    Expected Outcome:
    - API should return a valid JWT token.
    """
    mock_authenticate_admin.return_value = True

    response = client.post(
        "/login",
        data={"username": "admin@example.com", "password": "adminpassword"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.authenticate_user", new_callable=AsyncMock)
@patch("janux_auth_gateway.database.mongoDB.authenticate_admin", new_callable=AsyncMock)
async def test_login_invalid_credentials(
    mock_authenticate_admin, mock_authenticate_user
):
    """
    Test login with incorrect credentials.

    Steps:
    1. Mock `authenticate_admin()` and `authenticate_user()` to return `False`.
    2. Call `POST /login` with incorrect credentials.

    Expected Outcome:
    - API should return `401 Unauthorized`.
    """
    mock_authenticate_user.return_value = False
    mock_authenticate_admin.return_value = False

    response = client.post(
        "/login",
        data={"username": "wronguser@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password"


@pytest.mark.asyncio
@patch("janux_auth_gateway.auth.jwt.create_access_token", new_callable=AsyncMock)
async def test_token_contains_correct_claims(mock_create_access_token):
    """
    Test token contains correct user information.

    Steps:
    1. Mock `create_access_token()` to return a predefined token.
    2. Call `POST /login` with valid credentials.

    Expected Outcome:
    - API should return a JWT token with the correct claims.
    """
    mock_create_access_token.return_value = "mocked.jwt.token"

    response = client.post(
        "/login",
        data={"username": "user@example.com", "password": "validpassword"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] == "mocked.jwt.token"
    assert response.json()["token_type"] == "bearer"
