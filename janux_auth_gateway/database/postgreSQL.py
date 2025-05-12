"""
postgres.py

PostgreSQL database connection and user/admin authentication logic for JANUX Authentication Gateway.

Features:
- Creates async SQLAlchemy engine and session maker.
- Initializes database schema for development/test environments.
- Inserts default admin and test user accounts if they do not exist.
- Implements authentication logic and credential validation.
- Provides helper functions to check for existing users/admins.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from janux_auth_gateway.database.postgreSQL_base import Base
from sqlalchemy.future import select
from janux_auth_gateway.config import Config
from janux_auth_gateway.auth.passwords import hash_password, verify_password
from hestia_logger import get_logger
from janux_auth_gateway.models.postgreSQL.user_model import User
from janux_auth_gateway.models.postgreSQL.admin_model import Admin
from typing import Optional

# Logger instance
logger = get_logger("auth_service_logger")

# ---------- 1. Database Engine & Session Setup ---------- #

engine = create_async_engine(
    Config.POSTGRES_URI,
    echo=Config.POSTGRES_ECHO,
    pool_size=Config.POSTGRES_POOL_SIZE,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


from urllib.parse import urlparse


# ---------- 2. Database Initialization ---------- #
async def init_db_postgres(test_admin=None, test_user=None):
    try:
        logger.info("Creating PostgreSQL tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Schema created.")

        admin_creds = test_admin or (
            Config.POSTGRES_ADMIN_USERNAME,
            Config.POSTGRES_ADMIN_PASSWORD,
            Config.POSTGRES_ADMIN_FULLNAME,
            Config.POSTGRES_ADMIN_ROLE,
        )

        user_creds = test_user or (
            Config.POSTGRES_USER_USERNAME,
            Config.POSTGRES_USER_PASSWORD,
            Config.POSTGRES_USER_FULLNAME,
            Config.POSTGRES_USER_ROLE,
        )

        async with AsyncSessionLocal() as session:
            await create_admin_account_postgres(session, *admin_creds)
            await create_user_account_postgres(session, *user_creds)

    except Exception as e:
        logger.error(f"Error initializing PostgreSQL database: {e}")
        raise SystemExit("Database initialization failed.")


# ---------- 3. Admin & User Account Creation ---------- #
async def create_admin_account_postgres(
    session, username: str, password: str, full_name: str, role: str
):
    result = await session.execute(select(Admin).where(Admin.username == username))
    existing = result.scalar_one_or_none()
    if not existing:
        admin = Admin(
            username=username,
            full_name=full_name,
            hashed_password=hash_password(password),
            role=role,
        )
        session.add(admin)
        await session.commit()
        logger.info("Admin account created.")
    else:
        logger.info("Admin account already exists.")


async def create_user_account_postgres(
    session, username: str, password: str, full_name: str, role: str
):
    result = await session.execute(select(User).where(User.username == username))
    existing = result.scalar_one_or_none()
    if not existing:
        user = User(
            username=username,
            full_name=full_name,
            hashed_password=hash_password(password),
            role=role,
        )
        session.add(user)
        await session.commit()
        logger.info("User account created.")
    else:
        logger.info("User account already exists.")


# ---------- 4. Authentication Logic ---------- #
async def authenticate_user_postgres(username: str, password: str) -> bool:
    logger.info(f"Authenticating user: {username}")
    async with AsyncSessionLocal() as session:
        user = await user_exists_postgres(session, username)
        if not user:
            logger.warning("User not found.")
            return False
        if not verify_password(password, user.hashed_password, user.email):
            logger.warning("Password verification failed.")
            return False
        return True


async def authenticate_admin_postgres(username: str, password: str) -> bool:
    logger.info(f"Authenticating admin: {username}")
    async with AsyncSessionLocal() as session:
        admin = await admin_exists_postgres(session, username)
        if not admin:
            logger.warning("Admin not found.")
            return False
        if not verify_password(password, admin.hashed_password, admin.email):
            logger.warning("Password verification failed.")
            return False
        return True


# ---------- 5. Existence Check Helpers ---------- #
async def user_exists_postgres(session, username: str) -> Optional[User]:
    result = await session.execute(select(User).where(User.email == username))
    return result.scalar_one_or_none()


async def admin_exists_postgres(session, username: str) -> Optional[Admin]:
    result = await session.execute(select(Admin).where(Admin.email == username))
    return result.scalar_one_or_none()
