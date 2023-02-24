# -*- coding: utf-8 -*-
"""ACLMixin related tests."""

import pytest

from sqlalchemy import Column, Integer

from stalker import ACLMixin, Permission
from stalker.db.declarative import Base


class TestClassForACL(Base, ACLMixin):
    """A class for testing ACLMixing."""

    __tablename__ = "TestClassForACLs"
    id = Column(Integer, primary_key=True)

    def __init__(self):
        super(TestClassForACL, self).__init__()
        self.name = None


@pytest.fixture(scope="function")
def acl_mixin_test_setup():
    """stalker.models.mixins.ACLMixin class.

    Returns:
        dict: Test data.
    """
    data = dict()
    # create permissions
    data["test_perm1"] = Permission(
        access="Allow", action="Create", class_name="Something"
    )
    data["test_instance"] = TestClassForACL()
    data["test_instance"].name = "Test"
    data["test_instance"].permissions.append(data["test_perm1"])
    return data


def test_permission_attribute_accept_permission_instances_only(acl_mixin_test_setup):
    """permissions attribute accepts only Permission instances."""
    data = acl_mixin_test_setup
    with pytest.raises(TypeError) as cm:
        data["test_instance"].permissions = [234]

    assert (
        str(cm.value) == "TestClassForACL.permissions should be all instances of "
        "stalker.models.auth.Permission not int"
    )


def test_permission_attribute_is_working_properly(acl_mixin_test_setup):
    """permissions attribute is working properly."""
    data = acl_mixin_test_setup
    assert data["test_instance"].permissions == [data["test_perm1"]]


def test_acl_property_returns_a_list(acl_mixin_test_setup):
    """__acl__ property returns a list."""
    data = acl_mixin_test_setup
    assert isinstance(data["test_instance"].__acl__, list)


def test_acl_property_returns_a_proper_ACL_list(acl_mixin_test_setup):
    """__acl__ property is a list of ACLs according to the given permissions."""
    data = acl_mixin_test_setup
    assert data["test_instance"].__acl__ == [
        ("Allow", "TestClassForACL:Test", "Create_Something")
    ]
