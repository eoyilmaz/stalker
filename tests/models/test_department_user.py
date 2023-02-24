# -*- coding: utf-8 -*-
"""Tests for the DepartmentUser class."""

import pytest

from stalker import Department, DepartmentUser, User


def test_role_argument_is_not_a_role_instance():
    """TypeError will be raised when the role argument is not a Role instance."""
    with pytest.raises(TypeError) as cm:
        DepartmentUser(
            department=Department(name="Test Department"),
            user=User(
                name="Test User", login="tuser", email="u@u.com", password="secret"
            ),
            role="not a role instance",
        )

    assert str(cm.value) == (
        "DepartmentUser.role should be a stalker.models.auth.Role instance, not str"
    )
