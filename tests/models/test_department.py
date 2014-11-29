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
import datetime
from stalker import db, Department, Entity, User


class DepartmentTester(unittest.TestCase):
    """tests the Department class
    """

    def setUp(self):
        """lets setup the tests
        """
        db.setup()  # uses in memory sqlite db
        db.init()

        self.test_admin = User.query.filter_by(login="admin").first()

        # create a couple of test users
        self.test_user1 = User(
            name="User1",
            login="user1",
            email="user1@test.com",
            password="123456",
        )
        db.DBSession.add(self.test_user1)

        self.test_user2 = User(
            name="User2",
            login="user2",
            email="user2@test.com",
            password="123456",
        )
        db.DBSession.add(self.test_user2)

        self.test_user3 = User(
            name="User3",
            login="user3",
            email="user3@test.com",
            password="123456",
        )
        db.DBSession.add(self.test_user3)

        self.test_user4 = User(
            name="User4",
            login="user4",
            email="user4@test.com",
            password="123456",
        )
        db.DBSession.add(self.test_user4)

        self.test_user5 = User(
            name="User5",
            login="user5",
            email="user5@test.com",
            password="123456",
        )
        db.DBSession.add(self.test_user5)

        self.users_list = [
            self.test_user1,
            self.test_user2,
            self.test_user3,
            self.test_user4
        ]

        self.date_created = self.date_updated = datetime.datetime.now()

        self.kwargs = {
            "name": "Test Department",
            "description": "This is a department for testing purposes",
            "created_by": self.test_admin,
            "updated_by": self.test_admin,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "users": self.users_list
        }

        # create a default department object
        self.test_department = Department(**self.kwargs)
        db.DBSession.add(self.test_department)
        db.DBSession.commit()

    def test___auto_name__class_attribute_is_set_to_false(self):
        """testing if the __auto_name__ class attribute is set to False for
        Department class
        """
        self.assertFalse(Department.__auto_name__)

    def test_users_argument_accepts_an_empty_list(self):
        """testing if users argument accepts an empty list
        """
        # this should work without raising any error
        self.kwargs["users"] = []
        new_dep = Department(**self.kwargs)
        self.assertTrue(isinstance(new_dep, Department))

    def test_users_attribute_accepts_an_empty_list(self):
        """testing if users attribute accepts an empty list
        """
        # this should work without raising any error
        self.test_department.users = []

    def test_users_argument_accepts_only_a_list_of_user_objects(self):
        """testing if users argument accepts only a list of user objects
        """
        test_value = [1, 2.3, [], {}]
        self.kwargs["users"] = test_value
        # this should raise a TypeError
        self.assertRaises(
            TypeError,
            Department,
            **self.kwargs
        )

    def test_users_attribute_accepts_only_a_list_of_user_objects(self):
        """testing if users attribute accepts only a list of user objects
        """
        test_value = [1, 2.3, [], {}]
        # this should raise a TypeError
        self.assertRaises(
            TypeError,
            setattr,
            self.test_department,
            "users",
            test_value
        )

    def test_users_attribute_elements_accepts_User_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a User object to the users list
        """
        # append
        self.assertRaises(
            TypeError,
            self.test_department.users.append,
            0
        )

        # __setitem__
        self.assertRaises(
            TypeError,
            self.test_department.users.__setitem__,
            0,
            0
        )

    def test_users_argument_is_not_iterable(self):
        """testing if a TypeError will be raised when the given users
        argument is not an instance of list
        """
        test_values = [1, 1.2, "a user"]
        for test_value in test_values:
            self.kwargs["users"] = test_value
            self.assertRaises(TypeError, Department, **self.kwargs)

    def test_users_attribute_is_not_iterable(self):
        """testing if a TypeError will be raised when the users attribute
        is tried to be set to a non-iterable value
        """
        test_values = [1, 1.2, "a user"]
        for test_value in test_values:
            self.assertRaises(TypeError, setattr, self.test_department,
                              "users", test_value)

    def test_users_attribute_defaults_to_empty_list(self):
        """testing if the users attribute defaults to an empty list if the
         users argument is skipped
        """
        self.kwargs.pop("users")
        new_department = Department(**self.kwargs)
        self.assertEqual(new_department.users, [])

    def test_users_attribute_set_to_None(self):
        """testing if a TypeError will be raised when the users attribute is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_department, "users",
                          None)

    def test_user_role_attribute(self):
        """testing the automatic generation of the DepartmentUser class
        """
        # assign a user to a department and search for a DepartmentUser
        # representing that relation
        from stalker import DepartmentUser
        db.DBSession.commit()
        with db.DBSession.no_autoflush:
            self.test_department.users.append(self.test_user5)

        dus = DepartmentUser.query\
            .filter(DepartmentUser.user == self.test_user5)\
            .filter(DepartmentUser.department == self.test_department)\
            .all()

        self.assertTrue(len(dus) > 0)
        du = dus[0]
        self.assertTrue(isinstance(du, DepartmentUser))
        self.assertEqual(du.department, self.test_department)
        self.assertEqual(du.user, self.test_user5)
        self.assertEqual(du.role, None)

    def test_equality(self):
        """testing equality of two Department objects
        """
        dep1 = Department(**self.kwargs)
        dep2 = Department(**self.kwargs)

        entity_kwargs = self.kwargs.copy()
        entity_kwargs.pop("users")
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
        entity_kwargs.pop("users")
        entity1 = Entity(**entity_kwargs)

        self.kwargs["name"] = "Animation"
        dep3 = Department(**self.kwargs)

        self.assertFalse(dep1 != dep2)
        self.assertTrue(dep1 != dep3)
        self.assertTrue(dep1 != entity1)

    def test_tjp_id_is_working_properly(self):
        """testing if the tjp_is working properly
        """
        self.assertEqual(self.test_department.tjp_id, 'Department_35')

    def test_to_tjp_is_working_properly(self):
        """testing if the to_tjp property is working properly
        """
        expected_tjp = """
resource Department_35 "Department_35" {
    resource User_30 "User_30" {
    efficiency 1.0
}
    resource User_31 "User_31" {
    efficiency 1.0
}
    resource User_32 "User_32" {
    efficiency 1.0
}
    resource User_33 "User_33" {
    efficiency 1.0
}
}"""
        # print expected_tjp
        # print "-----------------"
        # print self.test_department.to_tjp
        # self.maxDiff = None
        self.assertEqual(self.test_department.to_tjp, expected_tjp)
