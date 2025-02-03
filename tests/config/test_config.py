"""
test_config.py

Unit tests for the configuration module in the JANUX Authentication Gateway.

Tests:
- Retrieval of environment variables with defaults.
- Handling of missing required environment variables.
- Secure handling of secrets using file-based and environment-based approaches.
- Validation of critical configuration settings.
- Proper loading of JWT private and public keys.
- Ensuring Redis and MongoDB configurations are correctly loaded.

Features:
- Uses `pytest-mock` to override environment variables.
- Mocks file reading operations to avoid filesystem dependencies.
- Ensures security best practices for managing secrets and keys.
- Validates behavior when secrets are missing or invalid.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import os
from unittest.mock import patch, mock_open
from janux_auth_gateway.config import Config

# In your test file
from janux_auth_gateway.config import _read_secret, _read_jwt_key, _get_env_variable


def test_get_env_variable_with_existing_value(mocker):
    """
    Test retrieval of an existing environment variable.

    Expected Outcome:
    - The function should return the correct value set in the environment.
    """
    mocker.patch.dict(os.environ, {"TEST_ENV_VAR": "test_value"})

    assert _get_env_variable("TEST_ENV_VAR") == "test_value"


def test_get_env_variable_with_default_value():
    """
    Test retrieval of an environment variable with a default fallback.

    Expected Outcome:
    - The function should return the default value if the variable is not set.
    """
    assert _get_env_variable("NON_EXISTENT_VAR", "default_value") == "default_value"


def test_get_env_variable_missing_without_default():
    """
    Test that missing required environment variables raise an exception.

    Expected Outcome:
    - The function should raise a ValueError if no default is provided.
    """
    with pytest.raises(ValueError, match="Missing environment variable: 'MISSING_VAR'"):
        _get_env_variable("MISSING_VAR")


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
            "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
            "TOKEN_ISSUER": "JANUX-server",
            "TOKEN_AUDIENCE": "JANUX-application",
            "USER_TOKEN_URL": "/auth/login",
            "ADMIN_TOKEN_URL": "/auth/login",
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
        },
    )

    # Mock secrets
    mocker.patch(
        "janux_auth_gateway.config._read_secret",
        side_effect=lambda key: f"mocked_{key}",
    )

    # Mock JWT key reading
    fake_private_key = "-----BEGIN PRIVATE KEY-----\nFAKEKEY\n-----END PRIVATE KEY-----"
    fake_public_key = "-----BEGIN PUBLIC KEY-----\nFAKEKEY\n-----END PUBLIC KEY-----"

    mocker.patch(
        "janux_auth_gateway.config._read_jwt_key",
        side_effect=lambda key_type: (
            fake_private_key if key_type == "private" else fake_public_key
        ),
    )

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
    mocker.patch.object(Config, "JWT_PRIVATE_KEY", "INVALID_KEY")
    mocker.patch.object(Config, "JWT_PUBLIC_KEY", "INVALID_KEY")

    with pytest.raises(
        ValueError, match="Invalid or missing `jwt_private_key` for signing JWTs."
    ):
        Config.validate()


def test_config_validation_failure_invalid_mongo_uri(mocker):
    """
    Test that Config.validate() raises an error if MongoDB URI is invalid.

    Expected Outcome:
    - Should raise a ValueError if the MongoDB URI is missing.
    """
    mocker.patch.object(Config, "MONGO_URI", "")

    with pytest.raises(
        ValueError, match="Missing `mongo_uri` for database connection."
    ):
        Config.validate()


def test_config_missing_critical_secrets(mocker):
    """
    Test that Config.validate() raises an error when a required secret is missing.

    Expected Outcome:
    - Should raise a ValueError when a critical secret is missing.
    """
    mocker.patch.object(Config, "JANUX_ENCRYPTION_KEY", "")

    with pytest.raises(
        ValueError, match="Missing `janux_encryption_key` for encryption."
    ):
        Config.validate()


def test_read_secret_from_file(mocker):
    """
    Test that secrets are correctly read from files.

    Expected Outcome:
    - The function should return the secret value from a file.
    """
    secret_value = "mocked_secret_value"
    mock_open_file = mock_open(read_data=secret_value)

    with patch("builtins.open", mock_open_file):
        with patch("os.path.exists", return_value=True):
            assert _read_secret("test_secret") == secret_value


def test_read_secret_from_env(mocker):
    """
    Test that secrets are read from environment variables if files are unavailable.

    Expected Outcome:
    - The function should return the secret value from environment variables.
    """
    mocker.patch.dict(os.environ, {"test_secret": "mocked_secret_from_env"})

    with patch("os.path.exists", return_value=False):
        assert _read_secret("test_secret") == "mocked_secret_from_env"


def test_read_jwt_key_from_file(mocker):
    """
    Test that JWT keys are correctly read from files.

    Expected Outcome:
    - The function should return the key content from a file.
    """
    jwt_key_value = "mocked_jwt_key"
    mock_open_file = mock_open(read_data=jwt_key_value)

    with patch("builtins.open", mock_open_file):
        with patch("os.path.exists", return_value=True):
            assert _read_jwt_key("private") == jwt_key_value


def test_read_jwt_key_missing(mocker):
    """
    Test that a ValueError is raised when no JWT key is found.

    Expected Outcome:
    - The function should raise a ValueError if no key file is found.
    """
    with patch("os.path.exists", return_value=False):
        with pytest.raises(ValueError, match="No private key file found"):
            _read_jwt_key("private")
