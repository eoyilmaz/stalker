# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause


import unittest

from stalker.models.auth import Permission

class PermissionTester(unittest.TestCase):
    """tests the stalker.models.auth.Permission class
    """
    
    def setUp(self):
        """setup the test
        """
        self.kwargs = {
            'access': 'Allow',
            'action': 'Add',
            'class_name': 'Project'
        }
        
        self.test_permission = Permission(**self.kwargs)
    
    #def tearDown(self):
    #    """clean the test
    #    """
    #    DBSession.remove()
    
    def test_access_argument_is_skipped(self):
        """testing if a TypeError will be raised when the access argument is
        skipped
        """
        self.kwargs.pop('access')
        self.assertRaises(TypeError, Permission, **self.kwargs)
    
    def test_access_argument_is_None(self):
        """testing if a TypeError will be raised when the access argument is
        None
        """
        self.kwargs['access'] = None
        self.assertRaises(TypeError, Permission, **self.kwargs)
    
    def test_access_argument_accepts_only_Allow_or_Deny_as_value(self):
        """testing if a ValueError will be raised when the value of access is
        something other than 'Allow' or 'Deny'
        """
        self.kwargs['access'] = 'Allowed'
        self.assertRaises(ValueError, Permission, **self.kwargs)
    
    def test_access_argument_is_setting_access_attribute_value(self):
        """testing if the access argument is setting the access attribute value
        correctly
        """
        self.assertEqual(self.kwargs['access'], self.test_permission.access)
    
    def test_access_attribute_is_read_only(self):
        """testing if access attribute is read only
        """
        self.assertRaises(AttributeError, setattr, self.test_permission,
                          'access', 'Deny')
    
    def test_action_argument_is_skipped_will_raise_a_TypeError(self):
        """testing if a TypeError will be raised when the action argument is
        skipped
        """
        self.kwargs.pop('action')
        self.assertRaises(TypeError, Permission, **self.kwargs)
    
    def test_action_argument_is_None(self):
        """testing if a TypeError will be raised when the action argument is
        set to None
        """
        self.kwargs['action'] = None
        self.assertRaises(TypeError, Permission, **self.kwargs)
   
    def test_action_argument_accepts_default_values_only(self):
        """testing if a ValueError will be raised when the action argument is
        not in the list of defaults.DEFAULT_ACTIONS
        """
        self.kwargs['action'] = 'Create'
        self.assertRaises(ValueError, Permission, **self.kwargs)
    
    def test_action_argument_is_setting_the_argument_attribute(self):
        """testing if the action argument is setting the argument attribute
        value
        """
        self.assertEqual(self.kwargs['action'], self.test_permission.action)
    
    def test_action_attribute_is_read_only(self):
        """testing if the action attribute is read only
        """
        self.assertRaises(AttributeError, setattr, self.test_permission,
                          'action', 'Add')
    
    def test_class_name_argument_skipped(self):
        """testing if a TypeError will be raised when the class_name argument
        is skipped
        """
        self.kwargs.pop('class_name')
        self.assertRaises(TypeError, Permission, **self.kwargs)
    
    def test_class_name_argument_is_None(self):
        """testing if a TypeError will be raised when the class_name argument
        is None
        """
        self.kwargs['class_name'] = None
        self.assertRaises(TypeError, Permission, **self.kwargs)
    
    def test_class_name_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the class_name argument
        is not a string instance
        """
        self.kwargs['class_name'] = 10
        self.assertRaises(TypeError, Permission, **self.kwargs)
    
    def test_class_name_argument_is_setting_the_class_name_attribute_value(self):
        """testing if the class_name argument value is correctly passed to the
        class_name attribute
        """
        self.assertEqual(self.kwargs['class_name'],
                         self.test_permission.class_name)
    
    def test_class_name_attribute_is_read_only(self):
        """testing if the class_name attribute is read only
        """
        self.assertRaises(AttributeError, setattr, self.test_permission,
                          'class_name', 'Asset')
