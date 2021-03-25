# -*- coding: utf-8 -*-

import unittest
import pytest
from sqlalchemy import Column, Integer

from stalker import ACLMixin
from stalker.db.declarative import Base


# create a new class and mix it with ACLMixin
class TestClassForACL(Base, ACLMixin):
    __tablename__ = 'TestClassForACLs'
    id = Column(Integer, primary_key=True)

    def __init__(self):
        self.name = None


class ACLMixinTester(unittest.TestCase):
    """tests the stalker.models.mixins.ACLMixin class
    """

    def setUp(self):
        """setup the test
        """
        # create permissions
        from stalker import Permission
        self.test_perm1 = Permission(
            access='Allow',
            action='Create',
            class_name='Something'
        )
        self.test_instance = TestClassForACL()
        self.test_instance.name = 'Test'
        self.test_instance.permissions.append(self.test_perm1)

    def test_permission_attribute_accept_Permission_instances_only(self):
        """testing if the permissions attribute accepts only Permission
        instances
        """
        with pytest.raises(TypeError) as cm:
            self.test_instance.permissions = [234]

        assert str(cm.value) == \
               'TestClassForACL.permissions should be all instances of ' \
               'stalker.models.auth.Permission not int'

    def test_permission_attribute_is_working_properly(self):
        """testing if the permissions attribute is working properly
        """
        assert self.test_instance.permissions == [self.test_perm1]

    def test_acl_property_returns_a_list(self):
        """testing if the __acl__ property returns a list
        """
        assert isinstance(self.test_instance.__acl__, list)

    def test_acl_property_returns_a_proper_ACL_list(self):
        """testing if the __acl__ property returns a proper ACL list according
        to the given permissions
        """
        assert self.test_instance.__acl__ == \
            [('Allow', 'TestClassForACL:Test', 'Create_Something')]
