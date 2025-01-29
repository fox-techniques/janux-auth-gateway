"""
test_admin_router.py

Unit tests for the admin-related API routes in the JANUX Authentication Gateway.

Tests:
- Admin listing users.
- Admin deleting users.
- Retrieving admin profile.
- Logging out admin users.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from janux_auth_gateway.routers.admin_router import admin_router
from janux_auth_gateway.models.user import User
from janux_auth_gateway.auth.jwt import get_current_admin
from fastapi import FastAPI

# Set up a FastAPI test client
app = FastAPI()
app.include_router(admin_router)
client = TestClient(app)


@pytest.mark.asyncio
@patch("janux_auth_gateway.models.user.User.find_all", new_callable=AsyncMock)
async def test_list_users_success(mock_find_all):
    """
    Test admin retrieving a list of users.

    Steps:
    1. Mock `User.find_all()` to return test users.
    2. Call `GET /users` as an admin.

    Expected Outcome:
    - API should return a list of users.
    """
    mock_find_all.return_value.to_list.return_value = [
        User(email="user1@example.com", full_name="User One"),
        User(email="user2@example.com", full_name="User Two"),
    ]

    response = client.get("/users", headers={"Authorization": "Bearer admin_token"})

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["email"] == "user1@example.com"


@pytest.mark.asyncio
@patch("janux_auth_gateway.models.user.User.get", new_callable=AsyncMock)
async def test_delete_user_success(mock_get_user):
    """
    Test admin successfully deleting a user.

    Steps:
    1. Mock `User.get()` to return a user.
    2. Call `DELETE /users/{user_id}` as an admin.

    Expected Outcome:
    - API should return a success message.
    """
    mock_get_user.return_value = User(email="delete@example.com", full_name="To Delete")

    response = client.delete(
        "/users/123", headers={"Authorization": "Bearer admin_token"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User ID 123 successfully deleted."


@pytest.mark.asyncio
@patch("janux_auth_gateway.models.user.User.get", new_callable=AsyncMock)
async def test_delete_user_not_found(mock_get_user):
    """
    Test admin attempting to delete a non-existent user.

    Steps:
    1. Mock `User.get()` to return `None`.
    2. Call `DELETE /users/{user_id}`.

    Expected Outcome:
    - API should return 404 Not Found.
    """
    mock_get_user.return_value = None

    response = client.delete(
        "/users/999", headers={"Authorization": "Bearer admin_token"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."


@pytest.mark.asyncio
@patch(
    "janux_auth_gateway.auth.jwt.get_current_admin",
    return_value={"username": "admin@example.com"},
)
async def test_get_admin_profile(mock_get_admin):
    """
    Test admin retrieving their own profile.

    Steps:
    1. Mock `get_current_admin()` to return an admin.
    2. Call `GET /profile`.

    Expected Outcome:
    - API should return the admin's profile.
    """
    response = client.get("/profile", headers={"Authorization": "Bearer admin_token"})

    assert response.status_code == 200
    assert response.json()["admin"]["username"] == "admin@example.com"


@pytest.mark.asyncio
@patch(
    "janux_auth_gateway.auth.jwt.get_current_admin",
    return_value={"username": "admin@example.com"},
)
async def test_admin_logout(mock_get_admin):
    """
    Test admin logout.

    Steps:
    1. Mock `get_current_admin()`.
    2. Call `POST /logout`.

    Expected Outcome:
    - API should return a logout confirmation message.
    """
    response = client.post("/logout", headers={"Authorization": "Bearer admin_token"})

    assert response.status_code == 200
    assert response.json()["message"] == "You have been logged out successfully."
