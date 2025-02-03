"""
config module

Centralized configuration management for the JANUX Authentication Gateway.

Features:
- Loads and validates environment variables.
- Provides access to critical application configurations.

Submodules:
- config: Defines the `Config` class for managing configurations.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from .config import Config, _read_secret, _read_jwt_key, _get_env_variable

# Expose the Config class for external use.
__all__ = ["Config"]
