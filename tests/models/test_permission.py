# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>


from stalker.models.auth import Permission
from stalker.testing import UnitTestBase


class PermissionTester(UnitTestBase):
    """tests the stalker.models.auth.Permission class
    """

    def setUp(self):
        """setup the test
        """
        super(PermissionTester, self).setUp()
        self.kwargs = {
            'access': 'Allow',
            'action': 'Create',
            'class_name': 'Project'
        }

        self.test_permission = Permission(**self.kwargs)

    def test_access_argument_is_skipped(self):
        """testing if a TypeError will be raised when the access argument is
        skipped
        """
        self.kwargs.pop('access')
        with self.assertRaises(TypeError) as cm:
            Permission(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            '__init__() takes exactly 4 arguments (3 given)'
        )

    def test_access_argument_is_None(self):
        """testing if a TypeError will be raised when the access argument is
        None
        """
        self.kwargs['access'] = None
        with self.assertRaises(TypeError) as cm:
            Permission(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Permission.access should be an instance of str not NoneType'
        )

    def test_access_argument_accepts_only_Allow_or_Deny_as_value(self):
        """testing if a ValueError will be raised when the value of access is
        something other than 'Allow' or 'Deny'
        """
        self.kwargs['access'] = 'Allowed'
        with self.assertRaises(ValueError) as cm:
            Permission(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Permission.access should be "Allow" or "Deny" not Allowed'
        )

    def test_access_argument_is_setting_access_attribute_value(self):
        """testing if the access argument is setting the access attribute value
        correctly
        """
        self.assertEqual(self.kwargs['access'], self.test_permission.access)

    def test_access_attribute_is_read_only(self):
        """testing if access attribute is read only
        """
        with self.assertRaises(AttributeError) as cm:
            self.test_permission.access = 'Deny'

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

    def test_action_argument_is_skipped_will_raise_a_TypeError(self):
        """testing if a TypeError will be raised when the action argument is
        skipped
        """
        self.kwargs.pop('action')
        with self.assertRaises(TypeError) as cm:
            Permission(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            '__init__() takes exactly 4 arguments (3 given)'
        )

    def test_action_argument_is_None(self):
        """testing if a TypeError will be raised when the action argument is
        set to None
        """
        self.kwargs['action'] = None
        with self.assertRaises(TypeError) as cm:
            Permission(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Permission.action should be an instance of str not NoneType'
        )

    def test_action_argument_accepts_default_values_only(self):
        """testing if a ValueError will be raised when the action argument is
        not in the list of defaults.DEFAULT_ACTIONS
        """
        self.kwargs['action'] = 'Add'
        with self.assertRaises(ValueError) as cm:
            Permission(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            "Permission.action should be one of the values of ['Create', "
            "'Read', 'Update', 'Delete', 'List'] not 'Add'"
        )

    def test_action_argument_is_setting_the_argument_attribute(self):
        """testing if the action argument is setting the argument attribute
        value
        """
        self.assertEqual(self.kwargs['action'], self.test_permission.action)

    def test_action_attribute_is_read_only(self):
        """testing if the action attribute is read only
        """
        with self.assertRaises(AttributeError) as cm:
            self.test_permission.action = 'Add'

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

    def test_class_name_argument_skipped(self):
        """testing if a TypeError will be raised when the class_name argument
        is skipped
        """
        self.kwargs.pop('class_name')
        with self.assertRaises(TypeError) as cm:
            Permission(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            '__init__() takes exactly 4 arguments (3 given)'
        )

    def test_class_name_argument_is_None(self):
        """testing if a TypeError will be raised when the class_name argument
        is None
        """
        self.kwargs['class_name'] = None
        with self.assertRaises(TypeError) as cm:
            Permission(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Permission.class_name should be an instance of str not NoneType'
        )

    def test_class_name_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the class_name argument
        is not a string instance
        """
        self.kwargs['class_name'] = 10
        with self.assertRaises(TypeError) as cm:
            Permission(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Permission.class_name should be an instance of str not int'
        )

    def test_class_name_argument_is_setting_the_class_name_attribute_value(self):
        """testing if the class_name argument value is correctly passed to the
        class_name attribute
        """
        self.assertEqual(self.kwargs['class_name'],
                         self.test_permission.class_name)

    def test_class_name_attribute_is_read_only(self):
        """testing if the class_name attribute is read only
        """
        with self.assertRaises(AttributeError) as cm:
            self.test_permission.class_name = 'Asset'

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )
