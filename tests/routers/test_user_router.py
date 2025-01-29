"""
test_user_router.py

Unit tests for the user-related API routes in the JANUX Authentication Gateway.

Tests:
- User registration with valid data.
- Handling of duplicate email during registration.
- Retrieving user profile.
- Logging out user.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI
from janux_auth_gateway.routers.user_router import user_router
from janux_auth_gateway.models.user import User
from janux_auth_gateway.auth.jwt import get_current_user

# Set up a FastAPI test client
app = FastAPI()
app.include_router(user_router)
client = TestClient(app)


@pytest.mark.asyncio
@patch("janux_auth_gateway.models.user.User.find_one", new_callable=AsyncMock)
@patch("janux_auth_gateway.models.user.User.insert", new_callable=AsyncMock)
async def test_register_user_success(mock_insert, mock_find_one):
    """
    Test user registration with valid data.

    Steps:
    1. Mock `User.find_one()` to return `None` (user does not exist).
    2. Mock `User.insert()` to simulate database insertion.
    3. Call `POST /register` with valid data.

    Expected Outcome:
    - API should return a `201 Created` status and the registered user's data.
    """
    mock_find_one.return_value = None

    response = client.post(
        "/register",
        json={
            "email": "newuser@example.com",
            "password": "securepassword",
            "full_name": "New User",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "newuser@example.com"
    assert response.json()["full_name"] == "New User"


@pytest.mark.asyncio
@patch("janux_auth_gateway.models.user.User.find_one", new_callable=AsyncMock)
async def test_register_duplicate_email(mock_find_one):
    """
    Test handling of duplicate email during registration.

    Steps:
    1. Mock `User.find_one()` to return an existing user.
    2. Call `POST /register` with an existing email.

    Expected Outcome:
    - API should return `409 Conflict` with an appropriate error message.
    """
    mock_find_one.return_value = User(
        email="existing@example.com", full_name="Existing User"
    )

    response = client.post(
        "/register",
        json={
            "email": "existing@example.com",
            "password": "password123",
            "full_name": "Existing User",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered."


@pytest.mark.asyncio
@patch(
    "janux_auth_gateway.auth.jwt.get_current_user",
    return_value={"username": "user@example.com"},
)
async def test_get_user_profile(mock_get_user):
    """
    Test retrieving user profile.

    Steps:
    1. Mock `get_current_user()` to return a logged-in user.
    2. Call `GET /profile`.

    Expected Outcome:
    - API should return the user's profile data.
    """
    response = client.get("/profile", headers={"Authorization": "Bearer user_token"})

    assert response.status_code == 200
    assert response.json()["user"]["username"] == "user@example.com"


@pytest.mark.asyncio
@patch(
    "janux_auth_gateway.auth.jwt.get_current_user",
    return_value={"username": "user@example.com"},
)
async def test_user_logout(mock_get_user):
    """
    Test user logout.

    Steps:
    1. Mock `get_current_user()`.
    2. Call `POST /logout`.

    Expected Outcome:
    - API should return a logout confirmation message.
    """
    response = client.post("/logout", headers={"Authorization": "Bearer user_token"})

    assert response.status_code == 200
    assert response.json()["message"] == "You have been logged out successfully."
