# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest
from stalker.models.auth import User, Group
from stalker.db.session import DBSession, ZopeTransactionExtension

class GroupTester(unittest.TestCase):
    """tests the stalker.models.auth.Group class
    """
    
    @classmethod
    def setUpClass(cls):
        """sets the test in class level
        """
        DBSession.remove()
        DBSession.configure(extension=None)
    
    @classmethod
    def tearDownClass(cls):
        """clear the test in class level
        """
        DBSession.remove()
        DBSession.configure(extension=ZopeTransactionExtension)
    
    def setUp(self):
        """set up the test in method level
        """
        
        # create a couple of Users
        self.test_user1 = User(
            name='User1',
            login='user1',
            password='1234',
            email='user1@test.com',
        )
        
        self.test_user2 = User(
            name='User2',
            login='user2',
            password='1234',
            email='user1@test.com',
        )
        
        self.test_user3 = User(
            name='User3',
            login='user3',
            password='1234',
            email='user3@test.com',
        )
        
        # create a test group
        
        self.kwargs= {
            "name": "Test Group",
            "users": [
                self.test_user1,
                self.test_user2,
                self.test_user3
            ]
        }
        
        self.test_group = Group(**self.kwargs)
    
    def test_users_argument_is_skipped(self):
        """testing if the users argument is skipped the users attribute will be
        an empty list
        """
        self.kwargs.pop('users')
        new_group = Group(**self.kwargs)
        self.assertEqual(new_group.users, [])
    
    def test_users_argument_is_not_a_list_of_User_instances(self):
        """testing if a TypeError will be raised when the users argument is not
        a list of User instances
        """
        self.kwargs['users'] = [12, 'not a user']
        self.assertRaises(TypeError, Group, **self.kwargs)
    
    def test_users_attribute_is_not_a_list_of_User_instances(self):
        """testing if a TypeError will be raised when the users attribute is
        not a list of User instances
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_group,
            'users',
            [12, 'not a user']
        )
    
    def test_users_argument_updates_the_groups_attribute_in_the_given_User_instances(self):
        """testing if the Users given with the users argument will have the
        current Group instance in their groups attribute
        """
        self.kwargs['name'] = 'New Group'
        new_group = Group(**self.kwargs)
        
        for user in self.kwargs['users']:
            self.assertIn(new_group, user.groups)
    
    def test_users_attribute_updates_the_groups_attribute_in_the_given_User_instances(self):
        """testing if the Users given with the users attribute will have the
        current Group instance in their groups attribute
        """
        test_users = self.kwargs.pop('users')
        new_group = Group(**self.kwargs)
        new_group.users = test_users
        for user in test_users:
            self.assertIn(new_group, user.groups)
