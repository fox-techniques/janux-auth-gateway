"""
database module

Handles database connections and operations for the JANUX Authentication Gateway.

Submodules:
- mongoDB: Manages MongoDB initialization and user authentication.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from .mongoDB import init_db, authenticate_user, authenticate_admin

__all__ = ["init_db", "authenticate_user", "authenticate_admin"]
