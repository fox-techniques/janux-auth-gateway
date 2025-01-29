"""
test_roles.py

Unit tests for the role enumerations in the JANUX Authentication Gateway.

Tests:
- Ensure AdminRole and UserRole enums contain the expected values.
- Confirm that enums behave as string-based enumerations.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from janux_auth_gateway.models.roles import AdminRole, UserRole


def test_admin_role_values():
    """
    Test that `AdminRole` contains the correct values.

    Steps:
    1. Verify that `AdminRole.ADMIN` matches "admin".
    2. Verify that `AdminRole.SUPER_ADMIN` matches "super_admin".

    Expected Outcome:
    - Enum values should match the expected role names.
    """
    assert AdminRole.ADMIN == "admin"
    assert AdminRole.SUPER_ADMIN == "super_admin"


def test_user_role_values():
    """
    Test that `UserRole` contains the correct values.

    Steps:
    1. Verify each role in `UserRole` has the expected string value.

    Expected Outcome:
    - Enum values should match the expected role names.
    """
    assert UserRole.USER == "user"
    assert UserRole.CONTRIBUTOR == "contributor"
    assert UserRole.MAINTAINER == "maintainer"
    assert UserRole.TESTER == "tester"


def test_admin_role_enum_type():
    """
    Test that `AdminRole` behaves as a string-based Enum.

    Steps:
    1. Verify that `AdminRole.ADMIN` is an instance of `AdminRole`.
    2. Verify that `AdminRole.ADMIN` is an instance of `str`.

    Expected Outcome:
    - Enum members should be instances of both `Enum` and `str`.
    """
    assert isinstance(AdminRole.ADMIN, AdminRole)
    assert isinstance(AdminRole.ADMIN, str)


def test_user_role_enum_type():
    """
    Test that `UserRole` behaves as a string-based Enum.

    Steps:
    1. Verify that `UserRole.USER` is an instance of `UserRole`.
    2. Verify that `UserRole.USER` is an instance of `str`.

    Expected Outcome:
    - Enum members should be instances of both `Enum` and `str`.
    """
    assert isinstance(UserRole.USER, UserRole)
    assert isinstance(UserRole.USER, str)
