"""
test_token.py

Unit tests for the token schema in the JANUX Authentication Gateway.

Tests:
- Validation of Token schema.
- Ensuring example values match expected outputs.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from janux_auth_gateway.schemas.token import Token


def test_token_schema():
    """
    Test the Token schema.

    Steps:
    1. Create a `Token` instance.
    2. Verify that it correctly stores `access_token` and `token_type`.

    Expected Outcome:
    - The schema should store the correct token data.
    """
    response = Token(access_token="sample.jwt.token", token_type="bearer")

    assert response.access_token == "sample.jwt.token"
    assert response.token_type == "bearer"


def test_token_example():
    """
    Test the example values of Token schema.

    Steps:
    1. Retrieve the schema example for `Token`.
    2. Verify it matches the expected format.

    Expected Outcome:
    - The example should match `{"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "token_type": "bearer"}`.
    """
    example = Token.model_json_schema()["properties"]

    assert (
        example["access_token"]["example"] == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    assert example["token_type"]["example"] == "bearer"
