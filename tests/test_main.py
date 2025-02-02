"""
test_main.py

Unit tests for the main entry point of the JANUX Authentication Gateway.

Tests:
- FastAPI app initialization.
- Middleware configuration.
- Route registration.
- Database initialization in lifespan function.
- Exception handling during startup.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from fastapi.testclient import TestClient
from janux_auth_gateway.main import app
from janux_auth_gateway.config import Config


@pytest.fixture()
def client():
    """
    Fixture to set up a test client for FastAPI.

    Returns:
        TestClient: A test client instance.
    """
    return TestClient(app)


def test_app_initialization(client):
    """
    Test that the FastAPI app initializes correctly.

    Steps:
    1. Verify that the app title is correctly set.
    2. Check that all routers are registered.

    Expected Outcome:
    - The app title should match "JANUX Authentication Gateway".
    - All major routes should be included.
    """
    assert app.title == "JANUX Authentication Gateway"

    routes = {route.path for route in app.routes}
    assert "/" in routes
    assert "/health" in routes
    assert "/auth/login" in routes
    assert "/admins/users" in routes
    assert "/users/register" in routes


def test_cors_middleware(client):
    """
    Test that CORS middleware is configured correctly.

    Steps:
    1. Send a preflight `OPTIONS` request.
    2. Verify that CORS headers are present.

    Expected Outcome:
    - The response should include CORS headers.
    """
    response = client.options("/", headers={"Origin": "http://example.com"})
    assert "access-control-allow-origin" in response.headers

    expected_origin = (
        Config.ALLOWED_ORIGINS[0]
        if Config.ALLOWED_ORIGINS and Config.ALLOWED_ORIGINS[0] != ""
        else "*"
    )

    assert response.headers["access-control-allow-origin"] == expected_origin
