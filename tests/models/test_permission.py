# -*- coding: utf-8 -*-


import sys
import unittest
import pytest
from stalker.models.auth import Permission


class PermissionTester(unittest.TestCase):
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
        with pytest.raises(TypeError) as cm:
            Permission(**self.kwargs)

        if sys.version_info[0] >= 3:
            assert str(cm.value) == \
                "__init__() missing 1 required positional argument: 'access'"
        else:
            if sys.version_info[1] == 7:
                # Python 2.7
                assert str(cm.value) == \
                    '__init__() takes exactly 4 arguments (3 given)'
            else:
                # Python 2.6
                assert str(cm.value) == \
                    '__init__() takes exactly 4 non-keyword arguments (1 ' \
                    'given)'

    def test_access_argument_is_None(self):
        """testing if a TypeError will be raised when the access argument is
        None
        """
        self.kwargs['access'] = None
        with pytest.raises(TypeError) as cm:
            Permission(**self.kwargs)

        assert str(cm.value) == \
            'Permission.access should be an instance of str not NoneType'

    def test_access_argument_accepts_only_Allow_or_Deny_as_value(self):
        """testing if a ValueError will be raised when the value of access is
        something other than 'Allow' or 'Deny'
        """
        self.kwargs['access'] = 'Allowed'
        with pytest.raises(ValueError) as cm:
            Permission(**self.kwargs)

        assert str(cm.value) == \
            'Permission.access should be "Allow" or "Deny" not Allowed'

    def test_access_argument_is_setting_access_attribute_value(self):
        """testing if the access argument is setting the access attribute value
        correctly
        """
        assert self.kwargs['access'] == self.test_permission.access

    def test_access_attribute_is_read_only(self):
        """testing if access attribute is read only
        """
        with pytest.raises(AttributeError) as cm:
            self.test_permission.access = 'Deny'

        assert str(cm.value) == "can't set attribute"

    def test_action_argument_is_skipped_will_raise_a_TypeError(self):
        """testing if a TypeError will be raised when the action argument is
        skipped
        """
        self.kwargs.pop('action')
        with pytest.raises(TypeError) as cm:
            Permission(**self.kwargs)

        if sys.version_info[0] >= 3:
            assert str(cm.value) == \
                "__init__() missing 1 required positional argument: 'action'"
        else:
            if sys.version_info[1] == 7:
                # Python 2.7
                assert str(cm.value) == \
                    '__init__() takes exactly 4 arguments (3 given)'
            else:
                # Python 2.6
                assert str(cm.value) == \
                    '__init__() takes exactly 4 non-keyword arguments ' \
                    '(2 given)'

    def test_action_argument_is_None(self):
        """testing if a TypeError will be raised when the action argument is
        set to None
        """
        self.kwargs['action'] = None
        with pytest.raises(TypeError) as cm:
            Permission(**self.kwargs)

        assert str(cm.value) == \
            'Permission.action should be an instance of str not NoneType'

    def test_action_argument_accepts_default_values_only(self):
        """testing if a ValueError will be raised when the action argument is
        not in the list of defaults.DEFAULT_ACTIONS
        """
        self.kwargs['action'] = 'Add'
        with pytest.raises(ValueError) as cm:
            Permission(**self.kwargs)

        assert str(cm.value) == \
            "Permission.action should be one of the values of ['Create', " \
            "'Read', 'Update', 'Delete', 'List'] not 'Add'"

    def test_action_argument_is_setting_the_argument_attribute(self):
        """testing if the action argument is setting the argument attribute
        value
        """
        assert self.kwargs['action'] == self.test_permission.action

    def test_action_attribute_is_read_only(self):
        """testing if the action attribute is read only
        """
        with pytest.raises(AttributeError) as cm:
            self.test_permission.action = 'Add'

        assert str(cm.value) == "can't set attribute"

    def test_class_name_argument_skipped(self):
        """testing if a TypeError will be raised when the class_name argument
        is skipped
        """
        self.kwargs.pop('class_name')
        with pytest.raises(TypeError) as cm:
            Permission(**self.kwargs)

        if sys.version_info[0] >= 3:
            assert str(cm.value) == \
                "__init__() missing 1 required positional argument: " \
                "'class_name'"
        else:
            if sys.version_info[1] == 7:
                # Pythone 2.7
                assert str(cm.value) == \
                    '__init__() takes exactly 4 arguments (3 given)'
            else:
                # Pythone 2.6
                assert str(cm.value) == \
                    '__init__() takes exactly 4 non-keyword arguments (3 ' \
                    'given)'

    def test_class_name_argument_is_None(self):
        """testing if a TypeError will be raised when the class_name argument
        is None
        """
        self.kwargs['class_name'] = None
        with pytest.raises(TypeError) as cm:
            Permission(**self.kwargs)

        assert str(cm.value) == \
            'Permission.class_name should be an instance of str not NoneType'

    def test_class_name_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the class_name argument
        is not a string instance
        """
        self.kwargs['class_name'] = 10
        with pytest.raises(TypeError) as cm:
            Permission(**self.kwargs)

        assert str(cm.value) == \
            'Permission.class_name should be an instance of str not int'

    def test_class_name_argument_is_setting_the_class_name_attribute_value(self):
        """testing if the class_name argument value is correctly passed to the
        class_name attribute
        """
        assert self.test_permission.class_name == self.kwargs['class_name']

    def test_class_name_attribute_is_read_only(self):
        """testing if the class_name attribute is read only
        """
        with pytest.raises(AttributeError) as cm:
            self.test_permission.class_name = 'Asset'

        assert str(cm.value) == "can't set attribute"
