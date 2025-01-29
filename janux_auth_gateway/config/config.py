"""
config.py

Central configuration module for the application. This module loads and validates
environment variables using python-dotenv and os.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """
    Retrieve environment variables with an optional default.

    Args:
        var_name (str): The name of the environment variable to retrieve.
        default (Optional[str]): The default value if the variable is not set.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not set and no default is provided.
    """
    value = os.getenv(var_name, default)
    if value is None:
        raise ValueError(
            f"Missing environment variable: '{var_name}'. "
            "Please set it in your environment or .env file."
        )
    return value


class Config:
    """
    Configuration class to centralize and validate environment variables.
    """

    # Application configuration
    ENVIRONMENT = get_env_variable("ENVIRONMENT", "local")

    # JWT configuration
    SECRET_KEY = get_env_variable("AUTH_SECRET_KEY")
    ALGORITHM = get_env_variable("AUTH_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        get_env_variable("ACCESS_TOKEN_EXPIRE_MINUTES", "20")
    )

    # Token URL
    USER_TOKEN_URL = get_env_variable("USER_TOKEN_URL")
    ADMIN_TOKEN_URL = get_env_variable("ADMIN_TOKEN_URL")

    # MongoDB connection URI
    MONGO_URI = get_env_variable("MONGO_URI")
    MONGO_DATABASE_NAME = get_env_variable("MONGO_DATABASE_NAME")
    MONGO_SUPER_ADMIN_EMAIL = get_env_variable("MONGO_SUPER_ADMIN_EMAIL")
    MONGO_SUPER_ADMIN_PASSWORD = get_env_variable("MONGO_SUPER_ADMIN_PASSWORD")

    @staticmethod
    def validate():
        """
        Validates the presence of critical environment variables.

        Raises:
            ValueError: If any required environment variable is missing or invalid.
        """
        validators = {
            "SECRET_KEY": lambda v: len(v) >= 32,
            "MONGO_URI": lambda v: v.startswith("mongodb://")
            or v.startswith("mongodb+srv://"),
        }

        for var, validator in validators.items():
            value = getattr(Config, var)
            if not validator(value):
                raise ValueError(f"Invalid configuration for {var}: {value}")


# Validate configuration at import time
Config.validate()
