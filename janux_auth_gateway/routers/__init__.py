"""
routers module

Defines API routes for the JANUX Authentication Gateway.

Submodules:
- base_router: Provides basic routes like root and health check endpoints.
- auth_router: Manages authentication-related operations (e.g., login).
- admin_router: Handles admin-only operations such as user management.
- user_router: Manages user-specific operations like registration and profile retrieval.

Features:
- Modular route definitions for better maintainability.
- Uses FastAPI's dependency injection for role-based access control.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from .base_router import base_router
from .auth_router import auth_router
from .admin_router import admin_router
from .user_router import user_router

__all__ = ["base_router", "auth_router", "admin_router", "user_router"]
