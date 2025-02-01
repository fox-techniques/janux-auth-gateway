"""
test_config.py

Unit tests for the configuration module in the JANUX Authentication Gateway.

Tests:
- Retrieval of environment variables with defaults.
- Handling of missing required environment variables.
- Config validation without exposing secret values.

Features:
- Uses `pytest-mock` to override environment variables.
- Mocks private/public key file reads to avoid file system dependencies.
- Ensures secure validation without printing sensitive information.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import os
from unittest.mock import patch, mock_open
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
    Mock the entire Config class properties without exposing secrets.
    """
    mocker.patch.dict(
        os.environ,
        {
            "ENVIRONMENT": "test",
            "ALLOWED_ORIGINS": "http://localhost,http://127.0.0.1",
            "CONTAINER": "False",
            "AUTH_PRIVATE_KEY_PATH": "/fake/private.pem",
            "AUTH_PUBLIC_KEY_PATH": "/fake/public.pem",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
            "USER_TOKEN_URL": "http://localhost/token",
            "ADMIN_TOKEN_URL": "http://localhost/admin-token",
            "MONGO_URI": "mongodb://localhost:27017/test_db",
            "MONGO_DATABASE_NAME": "test_db",
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
        },
    )

    fake_private_key = "-----BEGIN PRIVATE KEY-----\nFAKEKEY\n-----END PRIVATE KEY-----"
    fake_public_key = "-----BEGIN PUBLIC KEY-----\nFAKEKEY\n-----END PUBLIC KEY-----"

    mocker.patch("builtins.open", mock_open(read_data=fake_private_key), create=True)
    with patch("builtins.open", mock_open(read_data=fake_public_key)):
        yield


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


def test_config_validation_failure_invalid_keys(mocker):
    """
    Test that Config.validate() raises an error if private/public keys are invalid.

    Expected Outcome:
    - Should raise a ValueError if private or public keys are invalid.
    """
    mocker.patch.object(Config, "PRIVATE_KEY", "INVALID_KEY")
    mocker.patch.object(Config, "PUBLIC_KEY", "INVALID_KEY")

    with pytest.raises(ValueError, match="Invalid configuration for PRIVATE_KEY"):
        Config.validate()


def test_config_validation_failure_invalid_mongo_uri(mocker):
    """
    Test that Config.validate() raises an error if MongoDB URI is invalid.

    Expected Outcome:
    - Should raise a ValueError if the MongoDB URI does not start with the expected prefix.
    """
    mocker.patch.object(Config, "MONGO_URI", "invalid_uri")

    with pytest.raises(ValueError, match="Invalid configuration for MONGO_URI"):
        Config.validate()


def test_config_missing_critical_vars(mocker):
    """
    Test that Config.validate() raises an error when a required variable is missing.

    Expected Outcome:
    - Should raise a ValueError when a critical variable like PRIVATE_KEY is missing.
    """
    mocker.patch.object(Config, "PRIVATE_KEY", "")

    with pytest.raises(ValueError, match="Invalid configuration for PRIVATE_KEY"):
        Config.validate()
