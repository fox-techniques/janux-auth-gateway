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

from .config import Config, get_env_variable

__all__ = ["Config", "get_env_variable"]
