"""
test_config.py

Unit tests for the configuration module in the JANUX Authentication Gateway.

Tests:
- Retrieving environment variables with and without defaults.
- Ensuring `Config` class loads expected values.
- Validating required environment variables.
- Handling missing or invalid configuration values.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import os
from janux_auth_gateway.config import get_env_variable, Config


def test_get_env_variable_existing(monkeypatch):
    """
    Test retrieving an existing environment variable.

    Steps:
    1. Set an environment variable.
    2. Retrieve it using `get_env_variable()`.

    Expected Outcome:
    - The function should return the correct value.
    """
    monkeypatch.setenv("TEST_VAR", "test_value")
    assert get_env_variable("TEST_VAR") == "test_value"


def test_get_env_variable_with_default():
    """
    Test retrieving a non-existent environment variable with a default value.

    Steps:
    1. Call `get_env_variable()` with a non-existent key but provide a default value.

    Expected Outcome:
    - The function should return the default value.
    """
    assert get_env_variable("NON_EXISTENT_VAR", "default_value") == "default_value"


def test_get_env_variable_missing():
    """
    Test retrieving a missing environment variable without a default.

    Steps:
    1. Attempt to retrieve a missing variable without a default.

    Expected Outcome:
    - The function should raise a `ValueError`.
    """
    with pytest.raises(ValueError) as exc_info:
        get_env_variable("UNDEFINED_VAR")

    assert "Missing environment variable" in str(exc_info.value)


def test_config_has_all_required_attributes():
    """
    Test that `Config` contains all expected attributes.

    Steps:
    1. Define the expected attribute names.
    2. Check that each attribute exists in `Config`.

    Expected Outcome:
    - `Config` should contain all required attributes.
    - No attributes should be missing.
    """
    expected_attributes = {
        "SECRET_KEY",
        "ALGORITHM",
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "MONGO_URI",
        "MONGO_DATABASE_NAME",
        "MONGO_SUPER_ADMIN_EMAIL",
        "MONGO_SUPER_ADMIN_PASSWORD",
        "USER_TOKEN_URL",
        "ADMIN_TOKEN_URL",
        "ENVIRONMENT",
        "CONTAINER",
        "ALLOWED_ORIGINS",
    }

    missing_attributes = [
        attr for attr in expected_attributes if not hasattr(Config, attr)
    ]

    assert not missing_attributes, f"Config is missing attributes: {missing_attributes}"
