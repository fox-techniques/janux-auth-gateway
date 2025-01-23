from passlib.context import CryptContext

# Configure the password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from app.logging.custom_logger import get_logger

logger = get_logger("app_logger")


def hash_password(password: str) -> str:
    """
    Hash the given password using bcrypt.
    """
    logger.info("Encrypt password...")

    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    logger.info("Verify password agains hashed password...")

    return bcrypt_context.verify(plain_password, hashed_password)
