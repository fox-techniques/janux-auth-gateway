"""
test_base_router.py

Unit tests for the base API routes in the JANUX Authentication Gateway.

Tests:
- Root endpoint returns a welcome message.
- Health check endpoint returns service status.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from janux_auth_gateway.routers.base_router import base_router

# Set up a FastAPI test client
app = FastAPI()
app.include_router(base_router)
client = TestClient(app)


def test_root_endpoint():
    """
    Test root endpoint (`/`).

    Steps:
    1. Call `GET /`.

    Expected Outcome:
    - The response should return a welcome message.
    """
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the JANUX Authentication Gateway!"
    }


def test_health_check_endpoint():
    """
    Test health check endpoint (`/health`).

    Steps:
    1. Call `GET /health`.

    Expected Outcome:
    - The response should return `{"status": "healthy"}`.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
