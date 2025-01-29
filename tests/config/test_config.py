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


def test_config_loads_correct_values(monkeypatch):
    """
    Test that `Config` loads correct environment variables.

    Steps:
    1. Set required environment variables using `monkeypatch`.
    2. Check that `Config` correctly retrieves them.

    Expected Outcome:
    - `Config` properties should match the set values.
    """
    monkeypatch.setenv("AUTH_SECRET_KEY", "supersecurekeythatisatleast32chars")
    monkeypatch.setenv("AUTH_ALGORITHM", "HS512")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    monkeypatch.setenv("MONGO_URI", "mongodb://localhost:27017")
    monkeypatch.setenv("MONGO_DATABASE_NAME", "janux_test")
    monkeypatch.setenv("MONGO_SUPER_ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setenv("MONGO_SUPER_ADMIN_PASSWORD", "securepassword")

    assert Config.SECRET_KEY == "supersecurekeythatisatleast32chars"
    assert Config.ALGORITHM == "HS512"
    assert Config.ACCESS_TOKEN_EXPIRE_MINUTES == 60
    assert Config.MONGO_URI == "mongodb://localhost:27017"
    assert Config.MONGO_DATABASE_NAME == "janux_test"
    assert Config.MONGO_SUPER_ADMIN_EMAIL == "admin@example.com"
    assert Config.MONGO_SUPER_ADMIN_PASSWORD == "securepassword"


def test_config_validation_success(monkeypatch):
    """
    Test that `Config.validate()` passes with correct values.

    Steps:
    1. Set valid environment variables.
    2. Call `Config.validate()`.

    Expected Outcome:
    - The validation should pass without raising an error.
    """
    monkeypatch.setenv("AUTH_SECRET_KEY", "supersecurekeythatisatleast32chars")
    monkeypatch.setenv("MONGO_URI", "mongodb://localhost:27017")

    # Should not raise an error
    Config.validate()


def test_config_validation_failure(monkeypatch):
    """
    Test that `Config.validate()` fails when required variables are missing or incorrect.

    Steps:
    1. Set invalid values for required environment variables.
    2. Call `Config.validate()`.

    Expected Outcome:
    - The function should raise a `ValueError` for invalid configurations.
    """
    monkeypatch.setenv("AUTH_SECRET_KEY", "short_key")  # Less than 32 chars
    monkeypatch.setenv("MONGO_URI", "invalid_mongo_uri")  # Not a valid URI

    with pytest.raises(ValueError) as exc_info:
        Config.validate()

    assert "Invalid configuration for SECRET_KEY" in str(
        exc_info.value
    ) or "Invalid configuration for MONGO_URI" in str(exc_info.value)
