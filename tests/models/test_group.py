# -*- coding: utf-8 -*-


import unittest
import pytest

from stalker.models.auth import User, Group


class GroupTester(unittest.TestCase):
    """tests the stalker.models.auth.Group class
    """

    def setUp(self):
        """set up the test in method level
        """
        super(GroupTester, self).setUp()

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
        self.kwargs = {
            "name": "Test Group",
            "users": [
                self.test_user1,
                self.test_user2,
                self.test_user3
            ]
        }

        self.test_group = Group(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Group class
        """
        assert Group.__auto_name__ is False

    def test_users_argument_is_skipped(self):
        """testing if the users argument is skipped the users attribute will be
        an empty list
        """
        self.kwargs.pop('users')
        new_group = Group(**self.kwargs)
        assert new_group.users == []

    def test_users_argument_is_not_a_list_of_User_instances(self):
        """testing if a TypeError will be raised when the users argument is not
        a list of User instances
        """
        self.kwargs['users'] = [12, 'not a user']
        with pytest.raises(TypeError) as cm:
            Group(**self.kwargs)

        assert str(cm.value) == \
            'Group.users attribute must all be stalker.models.auth.User ' \
            'instances not int'

    def test_users_attribute_is_not_a_list_of_User_instances(self):
        """testing if a TypeError will be raised when the users attribute is
        not a list of User instances
        """
        with pytest.raises(TypeError) as cm:
            self.test_group.users = [12, 'not a user']

        assert str(cm.value) == \
            'Group.users attribute must all be stalker.models.auth.User ' \
            'instances not int'

    def test_users_argument_updates_the_groups_attribute_in_the_given_User_instances(self):
        """testing if the Users given with the users argument will have the
        current Group instance in their groups attribute
        """
        self.kwargs['name'] = 'New Group'
        new_group = Group(**self.kwargs)

        for user in self.kwargs['users']:
            assert new_group in user.groups

    def test_users_attribute_updates_the_groups_attribute_in_the_given_User_instances(self):
        """testing if the Users given with the users attribute will have the
        current Group instance in their groups attribute
        """
        test_users = self.kwargs.pop('users')
        new_group = Group(**self.kwargs)
        new_group.users = test_users
        for user in test_users:
            assert new_group in user.groups

    def test_permissions_argument_is_working_properly(self):
        """testing if permissions can be added to the Group on __init__()
        """
        # create a couple of permissions
        from stalker import Permission
        perm1 = Permission('Allow', 'Create', 'User')
        perm2 = Permission('Allow', 'Read', 'User')
        perm3 = Permission('Deny',  'Delete', 'User')

        new_group = Group(
            name='Test Group',
            users=[self.test_user1, self.test_user2],
            permissions=[perm1, perm2, perm3]
        )

        assert new_group.permissions == [perm1, perm2, perm3]
