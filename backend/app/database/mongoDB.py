from pymongo import MongoClient

from app.auth.passwords import verify_password

from app.logging.custom_logger import get_logger

logger = get_logger("app_logger")

# MongoDB connection URI
MONGO_URI = "mongodb://localhost:27017"  # Docker exposes this on localhost

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["janux_db"]

# Collections
users_collection = db["users"]

# from app.config.secrets import read_secret


# def create_mongodb_uri():
#     username = read_secret("mongodb_username")
#     password = read_secret("mongodb_password")
#     host = read_secret("mongodb_host")
#     port = read_secret("mongodb_port")

#     return f"mongodb://{username}:{password}@{host}:{port}/"


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user by username and password.
    """
    logger.info("Authenticating user...")

    # Check if the username exists in the database
    user = username_exists(username)
    if not username_exists(username):
        return False

    # Check if the password matches the hashed password in the database
    if not verify_password(password, user["password"]):
        return False

    return True


def username_exists(username: str) -> bool:
    """
    Authenticate a user by username.
    """
    logger.info("Checking if username exists...")
    # Find the user in the database
    user = users_collection.find_one({"email": username})
    if not user:
        return False

    return user
