"""
roles.py

Defines role enumerations for users and admins.

Features:
- Centralized role management for better maintainability and type safety.
- Provides enums for admin roles (`AdminRole`) and user roles (`UserRole`).

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from enum import Enum


class AdminRole(str, Enum):
    """
    Enum for admin roles.

    Attributes:
        ADMIN: Regular admin role.
        SUPER_ADMIN: Super admin role with elevated privileges.
    """

    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class UserRole(str, Enum):
    """
    Enum for user roles.

    Attributes:
        USER: Regular user role.
        CONTRIBUTOR: Contributor role for project contributions.
        MAINTAINER: Maintainer role for managing resources.
        TESTER: Tester role for testing functionalities.
    """

    USER = "user"
    CONTRIBUTOR = "contributor"
    MAINTAINER = "maintainer"
    TESTER = "tester"
