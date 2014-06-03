# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import unittest

from sqlalchemy import Column, Integer

from stalker import db
from stalker.db.session import DBSession
from stalker.models.mixins import ACLMixin
from stalker.db.declarative import Base
from stalker.models.auth import Permission


# create a new class and mix it with ACLMixin
class TestClassForACL(Base, ACLMixin):
    __tablename__ = 'TestClassForACLs'
    id = Column(Integer, primary_key=True)

    def __init__(self):
        self.name = None


class ACLMixinTester(unittest.TestCase):
    """tests the stalker.models.mixins.ACLMixin class
    """

    @classmethod
    def setUpClass(cls):
        """setup the test in class level
        """
        DBSession.remove()
        DBSession.configure()

    @classmethod
    def tearDownClass(cls):
        """cleanup the test in class level
        """
        DBSession.remove()
        DBSession.configure()

    def setUp(self):
        """setup the test
        """
        db.setup()

        # create permissions
        self.test_perm1 = Permission(
            access='Allow',
            action='Create',
            class_name='Something'
        )
        self.test_instance = TestClassForACL()
        self.test_instance.name = 'Test'
        self.test_instance.permissions.append(self.test_perm1)

    def tearDown(self):
        """clean the test
        """
        DBSession.remove()

    def test_permission_attribute_accept_Permission_instances_only(self):
        """testing if the permissions attribute accepts only Permission
        instances
        """
        self.assertRaises(TypeError, setattr, self.test_instance, [234])

    def test_permission_attribute_is_working_properly(self):
        """testing if the permissions attribute is working properly
        """
        self.assertEqual(self.test_instance.permissions, [self.test_perm1])

    def test_acl_property_returns_a_list(self):
        """testing if the __acl__ property returns a list
        """
        self.assertTrue(isinstance(self.test_instance.__acl__, list))

    def test_acl_property_returns_a_proper_ACL_list(self):
        """testing if the __acl__ property returns a proper ACL list according
        to the given permissions
        """
        self.assertEqual(
            self.test_instance.__acl__,
            [('Allow', 'TestClassForACL:Test', 'Create_Something')]
        )
