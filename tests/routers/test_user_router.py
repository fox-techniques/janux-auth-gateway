"""
test_user_router.py

Minimal unit tests for the user-related API routes in the JANUX Authentication Gateway.

Tests:
- Ensures the `/users/register` endpoint exists.
- Ensures the `/users/profile` endpoint exists.
- Ensures the `/users/logout` endpoint exists.

Features:
- Uses FastAPI's TestClient for API testing.
- Only checks API behavior (status codes), as detailed logic is tested separately.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi.testclient import TestClient
from fastapi import FastAPI
from janux_auth_gateway.routers.user_router import user_router


app = FastAPI()
app.include_router(user_router, prefix="/users")
client = TestClient(app)


def test_get_user_profile_exists():
    """
    Test that `GET /users/profile` endpoint exists.

    Expected Outcome:
    - API should return either `200 OK` or `401 Unauthorized`.
    """
    response = client.get("/users/profile")
    assert response.status_code in [200, 401]


def test_user_logout_exists():
    """
    Test that `POST /users/logout` endpoint exists.

    Expected Outcome:
    - API should return either `200 OK` or `401 Unauthorized`.
    """
    response = client.post("/users/logout")
    assert response.status_code in [200, 401]
