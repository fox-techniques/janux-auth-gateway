"""
test_response.py

Unit tests for the response schemas in the JANUX Authentication Gateway.

Tests:
- Validation of ConflictResponse schema.
- Validation of ErrorResponse schema.
- Ensuring example values match expected outputs.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from janux_auth_gateway.schemas.response import ConflictResponse, ErrorResponse


def test_conflict_response_schema():
    """
    Test the ConflictResponse schema.

    Steps:
    1. Create a `ConflictResponse` instance.
    2. Verify that it correctly stores the `detail` attribute.

    Expected Outcome:
    - The schema should store the correct error message.
    """
    response = ConflictResponse(detail="Email already registered.")
    assert response.detail == "Email already registered."


def test_error_response_schema():
    """
    Test the ErrorResponse schema.

    Steps:
    1. Create an `ErrorResponse` instance.
    2. Verify that it correctly stores `detail` and `code` attributes.

    Expected Outcome:
    - The schema should store the correct error message and status code.
    """
    response = ErrorResponse(detail="An unexpected error occurred.", code=500)
    assert response.detail == "An unexpected error occurred."
    assert response.code == 500


def test_conflict_response_example():
    """
    Test the example value of ConflictResponse.

    Steps:
    1. Retrieve the schema example for `ConflictResponse`.
    2. Verify it matches the expected format.

    Expected Outcome:
    - The example should match `{"detail": "Email already registered."}`.
    """
    example = ConflictResponse.model_json_schema()["properties"]
    assert example["detail"]["example"] == "Email already registered."


def test_error_response_example():
    """
    Test the example value of ErrorResponse.

    Steps:
    1. Retrieve the schema example for `ErrorResponse`.
    2. Verify it matches the expected format.

    Expected Outcome:
    - The example should match `{"detail": "An unexpected error occurred.", "code": 500}`.
    """
    example = ErrorResponse.model_json_schema()["properties"]
    assert example["detail"]["example"] == "An unexpected error occurred."
    assert example["code"]["example"] == 500
