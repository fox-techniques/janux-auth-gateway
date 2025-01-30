"""
test_admin_router.py

Minimal unit tests for the admin-related API routes in the JANUX Authentication Gateway.

Tests:
- Ensures the `/admins/users` endpoint exists.
- Ensures the `/admins/users/{user_id}` endpoint exists.
- Ensures the `/admins/profile` endpoint exists.
- Ensures the `/admins/logout` endpoint exists.

Features:
- Uses FastAPI's TestClient for API testing.
- Only checks API behavior (status codes), as detailed logic is tested separately.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi.testclient import TestClient
from fastapi import FastAPI
from janux_auth_gateway.routers.admin_router import admin_router

app = FastAPI()
app.include_router(admin_router, prefix="/admins")
client = TestClient(app)


def test_list_users_exists():
    """
    Test that `GET /admins/users` endpoint exists.

    Expected Outcome:
    - API should return either `200 OK` or `401 Unauthorized` (if auth is required).
    """
    response = client.get("/admins/users")
    assert response.status_code in [200, 401]


def test_delete_user_exists():
    """
    Test that `DELETE /admins/users/{user_id}` endpoint exists.

    Expected Outcome:
    - API should return either `200 OK`, `401 Unauthorized`, or `404 Not Found`.
    """
    response = client.delete("/admins/users/test-user-id")
    assert response.status_code in [200, 401, 404]


def test_get_admin_profile_exists():
    """
    Test that `GET /admins/profile` endpoint exists.

    Expected Outcome:
    - API should return either `200 OK` or `401 Unauthorized`.
    """
    response = client.get("/admins/profile")
    assert response.status_code in [200, 401]


def test_admin_logout_exists():
    """
    Test that `POST /admins/logout` endpoint exists.

    Expected Outcome:
    - API should return either `200 OK` or `401 Unauthorized`.
    """
    response = client.post("/admins/logout")
    assert response.status_code in [200, 401]
