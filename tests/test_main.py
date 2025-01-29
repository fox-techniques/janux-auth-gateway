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
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI
from janux_auth_gateway.main import app, lifespan
from janux_auth_gateway.database.mongoDB import init_db


@pytest.fixture
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
    assert response.headers["access-control-allow-origin"] == "*"


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.init_db", new_callable=AsyncMock)
async def test_lifespan_startup(mock_init_db):
    """
    Test the FastAPI lifespan function during startup.

    Steps:
    1. Mock `init_db()` to simulate database connection.
    2. Call the lifespan function.

    Expected Outcome:
    - The startup should complete without exceptions.
    - The database initialization should be called.
    """
    async with lifespan(app):
        mock_init_db.assert_called_once()


@pytest.mark.asyncio
@patch(
    "janux_auth_gateway.database.mongoDB.init_db",
    side_effect=Exception("Database failure"),
)
async def test_lifespan_startup_failure(mock_init_db):
    """
    Test the FastAPI lifespan function when database initialization fails.

    Steps:
    1. Mock `init_db()` to raise an exception.
    2. Call the lifespan function.

    Expected Outcome:
    - The function should raise an exception.
    - An error message should be logged.
    """
    with pytest.raises(Exception, match="Database failure"):
        async with lifespan(app):
            pass
