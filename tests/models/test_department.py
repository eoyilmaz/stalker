# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
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

import unittest2
import datetime
from stalker import Department, Entity, User


class DepartmentTester(unittest2.TestCase):
    """tests the Department class
    """

    def setUp(self):
        """lets setup the tests
        """
        # create a couple of test users
        self.test_user1 = User(
            name="User1",
            login="user1",
            email="user1@test.com",
            password="123456",
        )

        self.test_user2 = User(
            name="User2",
            login="user2",
            email="user2@test.com",
            password="123456",
        )

        self.test_user3 = User(
            name="User3",
            login="user3",
            email="user3@test.com",
            password="123456",
        )

        self.test_user4 = User(
            name="User4",
            login="user4",
            email="user4@test.com",
            password="123456",
        )

        self.members_list = [
            self.test_user1,
            self.test_user2,
            self.test_user3,
            self.test_user4
        ]

        self.test_admin = User(
            name="admin",
            login="admin",
            email="admin@test.com",
            password="admin",
        )

        self.date_created = self.date_updated = datetime.datetime.now()

        self.kwargs = {
            "name": "Test Department",
            "description": "This is a department for testing purposes",
            "created_by": self.test_admin,
            "updated_by": self.test_admin,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "members": self.members_list,
            "lead": self.test_user1
        }

        # create a default department object
        self.test_department = Department(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_false(self):
        """testing if the __auto_name__ class attribute is set to False for
        Department class
        """
        self.assertFalse(Department.__auto_name__)

    def test_members_argument_accepts_an_empty_list(self):
        """testing if members argument accepts an empty list
        """
        # this should work without raising any error
        self.kwargs["members"] = []
        new_dep = Department(**self.kwargs)
        self.assertIsInstance(new_dep, Department)

    def test_members_attribute_accepts_an_empty_list(self):
        """testing if members attribute accepts an empty list
        """
        # this should work without raising any error
        self.test_department.members = []

    def test_members_argument_accepts_only_a_list_of_user_objects(self):
        """testing if members argument accepts only a list of user objects
        """
        test_value = [1, 2.3, [], {}]
        self.kwargs["members"] = test_value
        # this should raise a TypeError
        self.assertRaises(
            TypeError,
            Department,
            **self.kwargs
        )

    def test_members_attribute_accepts_only_a_list_of_user_objects(self):
        """testing if members attribute accepts only a list of user objects
        """
        test_value = [1, 2.3, [], {}]
        # this should raise a TypeError
        self.assertRaises(
            TypeError,
            setattr,
            self.test_department,
            "members",
            test_value
        )

    def test_members_attribute_elements_accepts_User_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a User object to the members list
        """
        # append
        self.assertRaises(
            TypeError,
            self.test_department.members.append,
            0
        )

        # __setitem__
        self.assertRaises(
            TypeError,
            self.test_department.members.__setitem__,
            0,
            0
        )

    def test_members_argument_is_not_iterable(self):
        """testing if a TypeError will be raised when the given members
        argument is not an instance of list
        """
        test_values = [1, 1.2, "a user"]
        for test_value in test_values:
            self.kwargs["members"] = test_value
            self.assertRaises(TypeError, Department, **self.kwargs)

    def test_members_attribute_is_not_iterable(self):
        """testing if a TypeError will be raised when the members attribute
        is tried to be set to a non-iterable value
        """
        test_values = [1, 1.2, "a user"]
        for test_value in test_values:
            self.assertRaises(TypeError, setattr, self.test_department,
                              "members", test_value)

    def test_members_attribute_defaults_to_empty_list(self):
        """testing if the members attribute defaults to an empty list if the
         members argument is skipped
        """
        self.kwargs.pop("members")
        new_department = Department(**self.kwargs)
        self.assertEqual(new_department.members, [])

    def test_members_attribute_set_to_None(self):
        """testing if a TypeError will be raised when the members attribute is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_department, "members",
                          None)

    def test_users_attribute_is_a_synonym_for_members(self):
        """testing if the users attribute is actually a synonym for the members
        attribute
        """
        self.assertEqual(self.test_department.members,
                         self.test_department.users)

    def test_lead_argument_accepts_only_user_objects(self):
        """testing if lead argument accepts only user objects
        """
        test_values = ["", 1, 2.3, [], {}]
        # all of the above values should raise an TypeError
        for test_value in test_values:
            self.kwargs["lead"] = test_value
            self.assertRaises(
                TypeError,
                Department,
                **self.kwargs
            )

    def test_lead_attribute_accepts_only_User_instances(self):
        """testing if a TypeError will be raised when the lead attribute
        is not User instance
        """
        test_values = ["", 1, 2.3, [], {}]
        # all of the above values should raise an TypeError
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_department,
                "lead",
                test_value
            )

    def test_member_remove_also_removes_department_from_user(self):
        """testing if removing an user from the members list also removes the
        department from the users department argument
        """
        # check if the user is in the department
        self.assertIn(self.test_department, self.test_user1.departments)

        # now remove the user from the department
        self.test_department.members.remove(self.test_user1)

        # now check if department is not in users departments anymore
        self.assertNotIn(self.test_department, self.test_user1.departments)

        # assign the user back
        self.test_user1.departments.append(self.test_department)

        # check if the user is in the department
        self.assertIn(self.test_user1, self.test_department.members)

    def test_equality(self):
        """testing equality of two Department objects
        """
        dep1 = Department(**self.kwargs)
        dep2 = Department(**self.kwargs)

        entity_kwargs = self.kwargs.copy()
        entity_kwargs.pop("members")
        entity_kwargs.pop("lead")
        entity1 = Entity(**entity_kwargs)

        self.kwargs["name"] = "Animation"
        dep3 = Department(**self.kwargs)

        self.assertTrue(dep1 == dep2)
        self.assertFalse(dep1 == dep3)
        self.assertFalse(dep1 == entity1)

    def test_inequality(self):
        """testing inequality of two Department objects
        """
        dep1 = Department(**self.kwargs)
        dep2 = Department(**self.kwargs)

        entity_kwargs = self.kwargs.copy()
        entity_kwargs.pop("members")
        entity_kwargs.pop("lead")
        entity1 = Entity(**entity_kwargs)

        self.kwargs["name"] = "Animation"
        dep3 = Department(**self.kwargs)

        self.assertFalse(dep1 != dep2)
        self.assertTrue(dep1 != dep3)
        self.assertTrue(dep1 != entity1)

    def test_tjp_id_is_working_properly(self):
        """testing if the tjp_is working properly
        """
        self.assertEqual(self.test_department.tjp_id, 'Department_None')

    def test_to_tjp_is_working_properly(self):
        """testing if the to_tjp property is working properly
        """
        self.test_department.id = 1324
        self.test_user1.id = 1325
        self.test_user2.id = 1326
        self.test_user3.id = 1327
        self.test_user4.id = 1328

        expected_tjp = """resource Department_1324 "Test Department" {
            resource User_1325 "User1"
            resource User_1326 "User2"
            resource User_1327 "User3"
            resource User_1328 "User4"
        }"""
        self.assertEqual(self.test_department.to_tjp, expected_tjp)
