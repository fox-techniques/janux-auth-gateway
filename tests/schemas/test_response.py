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

    Expected Outcome:
    - The schema should correctly store the detail message.
    """
    response = ConflictResponse(detail="Email already registered.")
    assert response.detail == "Email already registered."


def test_error_response_schema():
    """
    Test the ErrorResponse schema.

    Expected Outcome:
    - The schema should correctly store the detail message and status code.
    """
    response = ErrorResponse(detail="An unexpected error occurred.", code=500)
    assert response.detail == "An unexpected error occurred."
    assert response.code == 500


def test_conflict_response_example():
    """
    Test the example value of ConflictResponse.

    Expected Outcome:
    - The example should match `{"detail": "Email already registered."}`.
    """
    example = ConflictResponse.model_json_schema()["properties"]
    assert example["detail"]["example"] == "Email already registered."


def test_error_response_example():
    """
    Test the example value of ErrorResponse.

    Expected Outcome:
    - The example should match `{"detail": "An unexpected error occurred.", "code": 500}`.
    """
    example = ErrorResponse.model_json_schema()["properties"]
    assert example["detail"]["example"] == "An unexpected error occurred."
    assert example["code"]["example"] == 500
