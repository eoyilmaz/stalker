# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest
import datetime
from stalker import Department, Entity, User

class DepartmentTester(unittest.TestCase):
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


    def test_members_argument_accepts_an_empty_list(self):
        """testing if members argument accepts an empty list
        """
        # this should work without raising any error
        self.kwargs["members"] = []
        aNewDepartment = Department(**self.kwargs)

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
        self.assertEqual(self.test_user1.department, self.test_department)

        # now remove the user from the department
        self.test_department.members.remove(self.test_user1)

        # now check if users department became None
        self.assertEqual(self.test_user1.department, None)

        # assign the user back
        self.test_user1.department = self.test_department

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

        #
        #def test_plural_name(self):
        #"""testing the plural name of Deparment class
        #"""

        #self.assertTrue(Department.plural_name, "Departments")
