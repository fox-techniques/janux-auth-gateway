"""
test_response.py

Unit tests for response schemas in the JANUX Authentication Gateway.

Tests:
- Ensures all response schemas have the correct attributes.
- Validates that example values match expected outputs.
- Ensures required fields are enforced.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from pydantic import ValidationError
from janux_auth_gateway.schemas.response_schema import (
    ConflictResponse,
    ErrorResponse,
    UnauthorizedResponse,
)


def test_conflict_response_structure():
    """
    Test that `ConflictResponse` schema has the correct attributes.

    Expected Outcome:
    - The `detail` field should exist and match the expected example.
    """
    response = ConflictResponse(detail="Email already registered.")
    assert response.detail == "Email already registered."


def test_conflict_response_missing_detail():
    """
    Test that `ConflictResponse` requires a `detail` field.

    Expected Outcome:
    - Should raise a `ValidationError` when `detail` is missing.
    """
    with pytest.raises(ValidationError):
        ConflictResponse()  # Missing required field


def test_conflict_response_example():
    """
    Test that `ConflictResponse` example matches the expected format.

    Expected Outcome:
    - The example should match the provided JSON schema.
    """
    expected_example = {"detail": "Email already registered."}
    assert (
        ConflictResponse.model_config["json_schema_extra"]["example"]
        == expected_example
    )


def test_error_response_structure():
    """
    Test that `ErrorResponse` schema has the correct attributes.

    Expected Outcome:
    - The `detail` field should match the expected value.
    - The `code` field should match the expected status code.
    """
    response = ErrorResponse(detail="An unexpected error occurred.", code=500)
    assert response.detail == "An unexpected error occurred."
    assert response.code == 500


def test_error_response_missing_fields():
    """
    Test that `ErrorResponse` requires both `detail` and `code` fields.

    Expected Outcome:
    - Should raise a `ValidationError` when fields are missing.
    """
    with pytest.raises(ValidationError):
        ErrorResponse(detail="An error occurred.")  # Missing `code`

    with pytest.raises(ValidationError):
        ErrorResponse(code=500)  # Missing `detail`


def test_error_response_example():
    """
    Test that `ErrorResponse` example matches the expected format.

    Expected Outcome:
    - The example should match the provided JSON schema.
    """
    expected_example = {"detail": "An unexpected error occurred.", "code": 500}
    assert (
        ErrorResponse.model_config["json_schema_extra"]["example"] == expected_example
    )


def test_unauthorized_response_structure():
    """
    Test that `UnauthorizedResponse` schema has the correct attributes.

    Expected Outcome:
    - The `detail` field should match the expected value.
    - The `code` field should match the expected status code.
    """
    response = UnauthorizedResponse(detail="Invalid credentials.", code=401)
    assert response.detail == "Invalid credentials."
    assert response.code == 401


def test_unauthorized_response_missing_fields():
    """
    Test that `UnauthorizedResponse` requires both `detail` and `code` fields.

    Expected Outcome:
    - Should raise a `ValidationError` when fields are missing.
    """
    with pytest.raises(ValidationError):
        UnauthorizedResponse(detail="Invalid credentials.")  # Missing `code`

    with pytest.raises(ValidationError):
        UnauthorizedResponse(code=401)  # Missing `detail`


def test_unauthorized_response_example():
    """
    Test that `UnauthorizedResponse` example matches the expected format.

    Expected Outcome:
    - The example should match the provided JSON schema.
    """
    expected_example = {"detail": "Invalid credentials.", "code": 401}
    assert (
        UnauthorizedResponse.model_config["json_schema_extra"]["example"]
        == expected_example
    )
