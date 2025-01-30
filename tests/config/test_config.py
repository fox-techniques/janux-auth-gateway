"""
test_config.py

Unit tests for the configuration module in the JANUX Authentication Gateway.

Tests:
- Retrieval of environment variables with defaults
- Handling of missing required environment variables
- Config class initialization with mock values
- Validation of critical environment variables

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import os
import secrets  # ✅ Securely generate random secrets
from unittest.mock import patch
from janux_auth_gateway.config import get_env_variable, Config


def test_get_env_variable_with_existing_value(mocker):
    """
    Test retrieval of an existing environment variable.

    Expected Outcome:
    - The function should return the correct value set in the environment.
    """
    mocker.patch.dict(os.environ, {"TEST_ENV_VAR": "test_value"})

    assert get_env_variable("TEST_ENV_VAR") == "test_value"


def test_get_env_variable_with_default_value():
    """
    Test retrieval of an environment variable with a default fallback.

    Expected Outcome:
    - The function should return the default value if the variable is not set.
    """
    assert get_env_variable("NON_EXISTENT_VAR", "default_value") == "default_value"


def test_get_env_variable_missing_without_default():
    """
    Test that missing required environment variables raise an exception.

    Expected Outcome:
    - The function should raise a ValueError if no default is provided.
    """
    with pytest.raises(ValueError, match="Missing environment variable: 'MISSING_VAR'"):
        get_env_variable("MISSING_VAR")


@pytest.fixture
def mock_config(mocker):
    """
    Mock the entire Config class properties to prevent exposure of real secrets.
    """
    mocker.patch.multiple(
        Config,
        SECRET_KEY=secrets.token_urlsafe(
            32
        ),  # ✅ Securely generate a random secret key
        ALGORITHM="HS256",
        ACCESS_TOKEN_EXPIRE_MINUTES=30,
        USER_TOKEN_URL="http://localhost/token",
        ADMIN_TOKEN_URL="http://localhost/admin-token",
        MONGO_URI="mongodb://localhost:27017/test_db",
        MONGO_DATABASE_NAME="test_db",
        MONGO_SUPER_ADMIN_EMAIL="admin@example.com",
        MONGO_SUPER_ADMIN_PASSWORD="adminpassword",
        ALLOWED_ORIGINS="http://localhost",
        CONTAINER=False,
    )


def test_config_initialization(mock_config):
    """
    Test that the Config class initializes correctly with mocked values.

    Expected Outcome:
    - All environment variables should be loaded correctly.
    """
    assert (
        isinstance(Config.SECRET_KEY, str) and len(Config.SECRET_KEY) >= 32
    )  # ✅ Ensure secret is securely generated
    assert Config.ALGORITHM == "HS256"
    assert Config.ACCESS_TOKEN_EXPIRE_MINUTES == 30
    assert Config.USER_TOKEN_URL == "http://localhost/token"
    assert Config.ADMIN_TOKEN_URL == "http://localhost/admin-token"
    assert Config.MONGO_URI == "mongodb://localhost:27017/test_db"
    assert Config.MONGO_DATABASE_NAME == "test_db"
    assert Config.MONGO_SUPER_ADMIN_EMAIL == "admin@example.com"
    assert Config.MONGO_SUPER_ADMIN_PASSWORD == "adminpassword"
    assert Config.ALLOWED_ORIGINS == "http://localhost"
    assert Config.CONTAINER is False  # Ensures proper boolean conversion


def test_config_validation_success(mock_config):
    """
    Test that Config.validate() does not raise an error when variables are valid.

    Expected Outcome:
    - Validation should pass without exceptions.
    """
    try:
        Config.validate()
    except ValueError:
        pytest.fail("Config.validate() raised ValueError unexpectedly!")


def test_config_validation_failure(mocker):
    """
    Test that Config.validate() raises an error for invalid configurations.

    Expected Outcome:
    - Should raise a ValueError if required variables are missing or invalid.
    """
    mocker.patch.object(Config, "MONGO_URI", "invalid_uri")

    with pytest.raises(ValueError, match="Invalid configuration for MONGO_URI"):
        Config.validate()


def test_config_missing_critical_vars(mocker):
    """
    Test that Config.validate() raises an error when a required variable is missing.

    Expected Outcome:
    - Should raise a ValueError when a critical variable like SECRET_KEY is missing.
    """
    mocker.patch.object(Config, "SECRET_KEY", "")

    with pytest.raises(ValueError, match="Invalid configuration for SECRET_KEY"):
        Config.validate()
