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

__version__ = "0.1.0"
