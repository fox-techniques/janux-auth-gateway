"""
test_token.py

Unit tests for the token schema in the JANUX Authentication Gateway.

Tests:
- Validation of `Token` schema.
- Ensuring example values match expected outputs.
- Required field validation.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from pydantic import ValidationError
from janux_auth_gateway.schemas.token_schema import Token


def test_token_schema():
    """
    Test the Token schema.

    Expected Outcome:
    - The schema should correctly store the access_token and token_type.
    """
    response = Token(access_token="mocked.jwt.token", token_type="bearer")

    assert response.access_token == "mocked.jwt.token"
    assert response.token_type == "bearer"


def test_token_missing_access_token():
    """
    Test that `Token` schema requires an `access_token`.

    Expected Outcome:
    - Should raise a `ValidationError` when `access_token` is missing.
    """
    with pytest.raises(ValidationError):
        Token(token_type="bearer")  # Missing `access_token`


def test_token_missing_token_type():
    """
    Test that `Token` schema requires a `token_type`.

    Expected Outcome:
    - Should raise a `ValidationError` when `token_type` is missing.
    """
    with pytest.raises(ValidationError):
        Token(access_token="mocked.jwt.token")  # Missing `token_type`


def test_token_example():
    """
    Test the example values of `Token` schema.

    Expected Outcome:
    - The example should match `{"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "token_type": "bearer"}`.
    """
    example = Token.model_json_schema()["properties"]

    assert (
        example["access_token"]["example"] == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    assert example["token_type"]["example"] == "bearer"
