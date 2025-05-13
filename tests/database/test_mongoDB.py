import pytest
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from unittest.mock import AsyncMock, MagicMock

from janux_auth_gateway.database.mongoDB import (
    create_admin_account,
    create_user_account,
    authenticate_user,
    authenticate_admin,
    username_exists,
    admin_username_exists,
)
from janux_auth_gateway.models.mongoDB.user_model import User
from janux_auth_gateway.models.mongoDB.admin_model import Admin


@pytest.fixture()
@pytest.mark.asyncio(scope="function")
async def mock_db(mocker):
    """
    Provides an isolated MongoDB test database.
    Mocks Redis to avoid rate-limiting in password verification.
    """
    # Patch redis in password module
    mock_redis = MagicMock()
    mock_redis.get.return_value = None
    mock_redis.incr.return_value = None
    mock_redis.expire.return_value = None
    mock_redis.delete.return_value = None

    mocker.patch("janux_auth_gateway.auth.passwords.redis_instance", mock_redis)

    # Setup test DB
    db_name = f"test_db_{uuid.uuid4().hex}"
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    test_db = client[db_name]

    mocker.patch(
        "janux_auth_gateway.database.mongoDB.AsyncIOMotorClient", return_value=client
    )

    await init_beanie(database=test_db, document_models=[User, Admin])
    await test_db["Admin"].create_index([("email", 1)], unique=True)
    await test_db["User"].create_index([("email", 1)], unique=True)

    test_admin = (
        "test.super.admin@example.com",
        "TestSuperAdminPassw0rd123!",
        "Test SuperAdminovski",
        "super_admin",
    )
    test_user = (
        "test.user@example.com",
        "TestUserPassw0rd123!",
        "Test TestUserovski",
        "user",
    )

    # Yield test data
    yield test_db, test_admin, test_user

    # Cleanup
    await client.drop_database(db_name)


@pytest.mark.asyncio(scope="function")
async def test_create_admin_account(mock_db):
    _, test_admin, _ = mock_db
    email, password, full_name, role = test_admin

    assert await Admin.find_one(Admin.email == email) is None
    await create_admin_account(email, password, full_name=full_name, role=role)
    created = await Admin.find_one(Admin.email == email)

    assert created is not None
    assert created.email == email
    assert created.full_name == full_name
    assert created.role == role


@pytest.mark.asyncio(scope="function")
async def test_create_user_account(mock_db):
    _, _, test_user = mock_db
    email, password, full_name, role = test_user

    assert await User.find_one(User.email == email) is None
    await create_user_account(email, password, full_name=full_name, role=role)
    created = await User.find_one(User.email == email)

    assert created is not None
    assert created.email == email
    assert created.full_name == full_name
    assert created.role == role


# @pytest.mark.asyncio(scope="function")
# async def test_authenticate_user_success(mock_db):
#     _, _, test_user = mock_db
#     email, password, full_name, role = test_user

#     await create_user_account(email, password, full_name=full_name, role=role)
#     assert await authenticate_user(email, password) is True


@pytest.mark.asyncio(scope="function")
async def test_authenticate_user_fail(mock_db):
    _, _, test_user = mock_db
    email, _, _, _ = test_user
    assert await authenticate_user(email, "WrongPassword!") is False


# @pytest.mark.asyncio(scope="function")
# async def test_authenticate_admin_success(mock_db):
#     _, test_admin, _ = mock_db
#     email, password, full_name, role = test_admin

#     await create_admin_account(email, password, full_name=full_name, role=role)
#     assert await authenticate_admin(email, password) is True


@pytest.mark.asyncio(scope="function")
async def test_authenticate_admin_fail(mock_db):
    _, test_admin, _ = mock_db
    email, _, _, _ = test_admin
    assert await authenticate_admin(email, "WrongPassword!") is False


@pytest.mark.asyncio(scope="function")
async def test_username_exists_found(mock_db):
    _, _, test_user = mock_db
    email, password, full_name, role = test_user

    await create_user_account(email, password, full_name=full_name, role=role)
    user = await username_exists(email)
    assert user is not None
    assert user.email == email


@pytest.mark.asyncio(scope="function")
async def test_username_exists_not_found(mock_db):
    user = await username_exists("nobody@example.com")
    assert user is None


@pytest.mark.asyncio(scope="function")
async def test_admin_username_exists_found(mock_db):
    _, test_admin, _ = mock_db
    email, password, full_name, role = test_admin

    await create_admin_account(email, password, full_name=full_name, role=role)
    admin = await admin_username_exists(email)
    assert admin is not None
    assert admin.email == email


@pytest.mark.asyncio(scope="function")
async def test_admin_username_exists_not_found(mock_db):
    admin = await admin_username_exists("nonexistent_admin@example.com")
    assert admin is None
