"""
test_roles.py

Unit tests for role enumerations in the JANUX Authentication Gateway.

Tests:
- Ensures all role values are correctly assigned.
- Validates membership of roles in their respective enums.
- Checks role mappings (`VALID_ADMIN_ROLES`, `VALID_USER_ROLES`).

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from janux_auth_gateway.models.mongoDB.roles_model import (
    AdminRole,
    UserRole,
    VALID_ADMIN_ROLES,
    VALID_USER_ROLES,
)


def test_admin_role_values():
    """
    Test that `AdminRole` values are correctly assigned.

    Expected Outcome:
    - `AdminRole.ADMIN` should be "admin".
    - `AdminRole.SUPER_ADMIN` should be "super_admin".
    """
    assert AdminRole.ADMIN.value == "admin"
    assert AdminRole.SUPER_ADMIN.value == "super_admin"


def test_user_role_values():
    """
    Test that `UserRole` values are correctly assigned.

    Expected Outcome:
    - `UserRole.USER` should be "user".
    - `UserRole.CONTRIBUTOR` should be "contributor".
    - `UserRole.MAINTAINER` should be "maintainer".
    - `UserRole.TESTER` should be "tester".
    """
    assert UserRole.USER.value == "user"
    assert UserRole.CONTRIBUTOR.value == "contributor"
    assert UserRole.MAINTAINER.value == "maintainer"
    assert UserRole.TESTER.value == "tester"


def test_admin_role_membership():
    """
    Test that valid admin roles exist in `AdminRole`.

    Expected Outcome:
    - All values in `VALID_ADMIN_ROLES` should exist in `AdminRole`.
    """
    for role in VALID_ADMIN_ROLES:
        assert role in AdminRole.__members__.values()


def test_user_role_membership():
    """
    Test that valid user roles exist in `UserRole`.

    Expected Outcome:
    - All values in `VALID_USER_ROLES` should exist in `UserRole`.
    """
    for role in VALID_USER_ROLES:
        assert role in UserRole.__members__.values()


def test_valid_admin_roles_mapping():
    """
    Test that `VALID_ADMIN_ROLES` correctly maps `AdminRole`.

    Expected Outcome:
    - `VALID_ADMIN_ROLES` should match the set of `AdminRole` values.
    """
    expected_roles = {"admin", "super_admin"}
    assert VALID_ADMIN_ROLES == expected_roles


def test_valid_user_roles_mapping():
    """
    Test that `VALID_USER_ROLES` correctly maps `UserRole`.

    Expected Outcome:
    - `VALID_USER_ROLES` should match the set of `UserRole` values.
    """
    expected_roles = {"user", "contributor", "maintainer", "tester"}
    assert VALID_USER_ROLES == expected_roles


@pytest.mark.parametrize("role", ["admin", "super_admin"])
def test_valid_admin_roles(role):
    """
    Test that valid admin roles are in `VALID_ADMIN_ROLES`.

    Expected Outcome:
    - The role should be in `VALID_ADMIN_ROLES`.
    """
    assert role in VALID_ADMIN_ROLES


@pytest.mark.parametrize("role", ["user", "contributor", "maintainer", "tester"])
def test_valid_user_roles(role):
    """
    Test that valid user roles are in `VALID_USER_ROLES`.

    Expected Outcome:
    - The role should be in `VALID_USER_ROLES`.
    """
    assert role in VALID_USER_ROLES


@pytest.mark.parametrize("role", ["invalid_role", "root", "moderator"])
def test_invalid_roles(role):
    """
    Test that invalid roles are NOT in `VALID_ADMIN_ROLES` or `VALID_USER_ROLES`.

    Expected Outcome:
    - The role should NOT be in either `VALID_ADMIN_ROLES` or `VALID_USER_ROLES`.
    """
    assert role not in VALID_ADMIN_ROLES
    assert role not in VALID_USER_ROLES
