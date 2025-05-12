"""
database module

Handles database connections and operations for the JANUX Authentication Gateway.

Submodules:
- mongoDB: Manages MongoDB initialization and user authentication.
- postgreSQL: Manages PostgreSQL initialization and user authentication.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from janux_auth_gateway.config import Config

# Dynamically import database logic based on backend setting
if Config.AUTH_DB_BACKEND == "mongo":
    from .mongoDB import (
        init_db,
        authenticate_user,
        authenticate_admin,
    )

    __all__ = ["init_db", "authenticate_user", "authenticate_admin"]

elif Config.AUTH_DB_BACKEND == "postgres":
    from .postgreSQL import (
        init_db_postgres,
        authenticate_user_postgres,
        authenticate_admin_postgres,
    )

    __all__ = [
        "init_db_postgres",
        "authenticate_user_postgres",
        "authenticate_admin_postgres",
    ]

else:
    raise ValueError("Invalid AUTH_DB_BACKEND. Must be 'mongo' or 'postgres'.")
