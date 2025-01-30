"""
test_roles.py

Unit tests for the role enumerations in the JANUX Authentication Gateway.

Tests:
- Ensure AdminRole and UserRole enums contain the expected values.
- Confirm that enums behave as string-based enumerations.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from janux_auth_gateway.models.roles import AdminRole, UserRole


def test_admin_role_values():
    """
    Test that `AdminRole` contains the correct values.

    Expected Outcome:
    - `AdminRole.ADMIN` should be "admin".
    - `AdminRole.SUPER_ADMIN` should be "super_admin".
    """
    assert AdminRole.ADMIN == "admin"
    assert AdminRole.SUPER_ADMIN == "super_admin"


def test_user_role_values():
    """
    Test that `UserRole` contains the correct values.

    Expected Outcome:
    - `UserRole.USER` should be "user".
    - `UserRole.CONTRIBUTOR` should be "contributor".
    - `UserRole.MAINTAINER` should be "maintainer".
    - `UserRole.TESTER` should be "tester".
    """
    assert UserRole.USER == "user"
    assert UserRole.CONTRIBUTOR == "contributor"
    assert UserRole.MAINTAINER == "maintainer"
    assert UserRole.TESTER == "tester"


def test_admin_role_enum_type():
    """
    Test that `AdminRole` behaves as a string-based Enum.

    Expected Outcome:
    - `AdminRole.ADMIN` should be an instance of `AdminRole`.
    - `AdminRole.ADMIN` should be an instance of `str`.
    """
    assert isinstance(AdminRole.ADMIN, AdminRole)
    assert isinstance(AdminRole.ADMIN, str)


def test_user_role_enum_type():
    """
    Test that `UserRole` behaves as a string-based Enum.

    Expected Outcome:
    - `UserRole.USER` should be an instance of `UserRole`.
    - `UserRole.USER` should be an instance of `str`.
    """
    assert isinstance(UserRole.USER, UserRole)
    assert isinstance(UserRole.USER, str)


def test_admin_role_valid_values():
    """
    Test that `AdminRole` accepts only valid values.

    Expected Outcome:
    - Creating `AdminRole("admin")` should return `AdminRole.ADMIN`.
    - Creating `AdminRole("super_admin")` should return `AdminRole.SUPER_ADMIN`.
    - Any invalid value should raise a `ValueError`.
    """
    assert AdminRole("admin") == AdminRole.ADMIN
    assert AdminRole("super_admin") == AdminRole.SUPER_ADMIN

    with pytest.raises(ValueError, match="is not a valid AdminRole"):
        AdminRole("invalid")


def test_user_role_valid_values():
    """
    Test that `UserRole` accepts only valid values.

    Expected Outcome:
    - Creating `UserRole("user")` should return `UserRole.USER`.
    - Creating `UserRole("contributor")` should return `UserRole.CONTRIBUTOR`.
    - Creating `UserRole("maintainer")` should return `UserRole.MAINTAINER`.
    - Creating `UserRole("tester")` should return `UserRole.TESTER`.
    - Any invalid value should raise a `ValueError`.
    """
    assert UserRole("user") == UserRole.USER
    assert UserRole("contributor") == UserRole.CONTRIBUTOR
    assert UserRole("maintainer") == UserRole.MAINTAINER
    assert UserRole("tester") == UserRole.TESTER

    with pytest.raises(ValueError, match="is not a valid UserRole"):
        UserRole("invalid")
