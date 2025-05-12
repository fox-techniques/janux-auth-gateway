"""
user_model.py (PostgreSQL)

Defines the User model for PostgreSQL using SQLAlchemy ORM.

Features:
- Stores user details such as email, full name, hashed password, and role.
- Enforces unique email addresses and indexed lookups.
- Uses shared `UserRole` enum from roles.py.
- Automatically sets a creation timestamp using server-side defaults.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from sqlalchemy import Column, String, DateTime, func
from .roles_model import UserRole
from uuid import uuid4

from janux_auth_gateway.database.postgreSQL_base import Base


def generate_uuid() -> str:
    """
    Generate a UUID string for primary keys.

    Returns:
        str: A UUID string.
    """
    return str(uuid4())


class User(Base):
    """
    SQLAlchemy model for the User table in PostgreSQL.

    Attributes:
        id (str): Primary key UUID.
        username (str): Unique username of the user.
        full_name (str): Full name of the user.
        hashed_password (str): Hashed password.
        role (str): Role of the user (e.g., user, contributor).
        created_at (datetime): Timestamp of user creation.
    """

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.USER.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        """
        Return a readable string representation of the User instance.

        Returns:
            str: Human-readable user object string.
        """
        return f"<User(username='{self.username}', role='{self.role}', created_at='{self.created_at}')>"
