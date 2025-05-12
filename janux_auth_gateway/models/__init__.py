"""
models module

Defines the database models for either MongoDB (Beanie) or PostgreSQL (SQLAlchemy) in the
JANUX Authentication Gateway, depending on the backend selected via configuration.

Submodules:
- mongo.admin_model / user_model / roles_model: Beanie ODM models for MongoDB
- postgres.admin_model / user_model / roles_model: SQLAlchemy models for PostgreSQL

Features:
- Backend-agnostic model import using `Config.AUTH_DB_BACKEND`
- Centralized role management through enums for maintainability

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from janux_auth_gateway.config import Config

if Config.AUTH_DB_BACKEND == "mongo":
    from janux_auth_gateway.models.mongoDB.admin_model import Admin
    from janux_auth_gateway.models.mongoDB.user_model import User
    from janux_auth_gateway.models.mongoDB.roles_model import AdminRole, UserRole

elif Config.AUTH_DB_BACKEND == "postgres":
    from janux_auth_gateway.models.postgreSQL.admin_model import Admin
    from janux_auth_gateway.models.postgreSQL.user_model import User
    from janux_auth_gateway.models.postgreSQL.roles_model import AdminRole, UserRole

__all__ = ["Admin", "User", "AdminRole", "UserRole"]
