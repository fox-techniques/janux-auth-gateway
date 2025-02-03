"""
janux_auth_gateway package

The JANUX Authentication Gateway provides a modular and extensible framework for user and admin authentication,
JWT management, and database operations using MongoDB and Beanie.

Modules:
- `app`: Contains the core application logic, including authentication, routing, models, and schemas.
- `routers`: Defines API routes for users, admins, authentication, and system utilities.
- `schemas`: Provides Pydantic models for request and response validation.
- `models`: Beanie-based MongoDB models for users and admins.
- `auth`: Manages password hashing and JWT handling.
- `logging`: Custom logging configuration and middleware.
- `errors`: Centralized error handling for consistent API responses.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from .config import Config, _read_secret, _read_jwt_key, _get_env_variable

# Only allow these functions to be imported within the package
__module_exports__ = ["Config", "_read_secret", "_read_jwt_key", "_get_env_variable"]


# Make sure internal functions can only be imported within package
def __getattr__(name):
    if name in __module_exports__:
        return globals()[name]  # Allow internal access within the package
    raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")


__version__ = "0.1.0"
