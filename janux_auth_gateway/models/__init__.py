"""
models module

Defines the database models for MongoDB using Beanie ODM in the JANUX Authentication Gateway.

Submodules:
- admin: Defines the `Admin` model for admin-related database operations.
- user: Defines the `User` model for user-related database operations.
- roles: Provides enumerations for roles (users and admins).

Features:
- Beanie-based MongoDB models with Pydantic validation.
- Centralized role management through enums for maintainability.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from .admin_model import Admin
from .user_model import User
from .roles_model import AdminRole, UserRole

__all__ = ["Admin", "User", "AdminRole", "UserRole"]
