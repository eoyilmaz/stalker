# -*- coding: utf-8 -*-

import unittest
import pytest

from stalker.testing import UnitTestDBBase
from stalker import Department


class DepartmentTester(unittest.TestCase):
    """tests the Department class
    """

    def setUp(self):
        """lets setup the tests
        """
        super(DepartmentTester, self).setUp()

        from stalker import User
        self.test_admin = User(
            name='admin',
            login='admin',
            email='admin@admins.com',
            password='12345',
        )

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

        self.test_user5 = User(
            name="User5",
            login="user5",
            email="user5@test.com",
            password="123456",
        )

        self.users_list = [
            self.test_user1,
            self.test_user2,
            self.test_user3,
            self.test_user4
        ]

        import datetime
        import pytz
        self.date_created = self.date_updated = datetime.datetime.now(pytz.utc)

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

    def test___auto_name__class_attribute_is_set_to_false(self):
        """testing if the __auto_name__ class attribute is set to False for
        Department class
        """
        assert Department.__auto_name__ is False

    def test___hash___value_is_correctly_calculated(self):
        """testing if the __hash__ value is correctly calculated
        """
        assert self.test_department.__hash__() == \
            hash(self.test_department.id) + \
            2 * hash(self.test_department.name) + \
            3 * hash(self.test_department.entity_type)

    def test_users_argument_accepts_an_empty_list(self):
        """testing if users argument accepts an empty list
        """
        # this should work without raising any error
        self.kwargs["users"] = []
        new_dep = Department(**self.kwargs)
        assert isinstance(new_dep, Department)

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
        with pytest.raises(TypeError) as cm:
            Department(**self.kwargs)

        assert str(cm.value) == \
            'DepartmentUser.user should be a stalker.models.auth.User ' \
            'instance, not int'

    def test_users_attribute_accepts_only_a_list_of_user_objects(self):
        """testing if users attribute accepts only a list of user objects
        """
        test_value = [1, 2.3, [], {}]
        # this should raise a TypeError
        with pytest.raises(TypeError) as cm:
            self.test_department.users = test_value

        assert str(cm.value) == \
            'DepartmentUser.user should be a stalker.models.auth.User ' \
            'instance, not int'

    def test_users_attribute_elements_accepts_User_only_1(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a User object to the users list
        """
        # append
        with pytest.raises(TypeError) as cm:
            self.test_department.users.append(0)

        assert str(cm.value) == \
            'DepartmentUser.user should be a stalker.models.auth.User ' \
            'instance, not int'

    def test_users_attribute_elements_accepts_User_only_2(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a User object to the users list
        """
        # __setitem__
        with pytest.raises(TypeError) as cm:
            self.test_department.users[0] = 0

        assert str(cm.value) == \
            'DepartmentUser.user should be a stalker.models.auth.User ' \
            'instance, not int'

    def test_users_argument_is_not_iterable(self):
        """testing if a TypeError will be raised when the given users
        argument is not an instance of list
        """
        self.kwargs["users"] = "a user"
        with pytest.raises(TypeError) as cm:
            Department(**self.kwargs)

        assert str(cm.value) == \
            'DepartmentUser.user should be a stalker.models.auth.User ' \
            'instance, not str'

    def test_users_attribute_is_not_iterable(self):
        """testing if a TypeError will be raised when the users attribute
        is tried to be set to a non-iterable value
        """
        with pytest.raises(TypeError) as cm:
            self.test_department.users = "a user"

        assert str(cm.value) == \
            'DepartmentUser.user should be a stalker.models.auth.User ' \
            'instance, not str'

    def test_users_attribute_defaults_to_empty_list(self):
        """testing if the users attribute defaults to an empty list if the
         users argument is skipped
        """
        self.kwargs.pop("users")
        new_department = Department(**self.kwargs)
        assert new_department.users == []

    def test_users_attribute_set_to_None(self):
        """testing if a TypeError will be raised when the users attribute is
        set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_department.users = None

        assert str(cm.value) == "'NoneType' object is not iterable"

    def test_equality(self):
        """testing equality of two Department objects
        """
        from stalker import Entity
        dep1 = Department(**self.kwargs)
        dep2 = Department(**self.kwargs)

        entity_kwargs = self.kwargs.copy()
        entity_kwargs.pop("users")
        entity1 = Entity(**entity_kwargs)

        self.kwargs["name"] = "Animation"
        dep3 = Department(**self.kwargs)

        assert dep1 == dep2
        assert not dep1 == dep3
        assert not dep1 == entity1

    def test_inequality(self):
        """testing inequality of two Department objects
        """
        from stalker import Entity
        dep1 = Department(**self.kwargs)
        dep2 = Department(**self.kwargs)

        entity_kwargs = self.kwargs.copy()
        entity_kwargs.pop("users")
        entity1 = Entity(**entity_kwargs)

        self.kwargs["name"] = "Animation"
        dep3 = Department(**self.kwargs)

        assert not dep1 != dep2
        assert dep1 != dep3
        assert dep1 != entity1


class DepartmentDBTester(UnitTestDBBase):
    """tests that needs a Database
    """

    def setUp(self):
        """lets setup the tests
        """
        super(DepartmentDBTester, self).setUp()

        from stalker import User
        self.test_admin = User.query.filter_by(login="admin").first()

        # create a couple of test users
        self.test_user1 = User(
            name="User1",
            login="user1",
            email="user1@test.com",
            password="123456",
        )
        from stalker.db.session import DBSession
        DBSession.add(self.test_user1)

        self.test_user2 = User(
            name="User2",
            login="user2",
            email="user2@test.com",
            password="123456",
        )
        DBSession.add(self.test_user2)

        self.test_user3 = User(
            name="User3",
            login="user3",
            email="user3@test.com",
            password="123456",
        )
        DBSession.add(self.test_user3)

        self.test_user4 = User(
            name="User4",
            login="user4",
            email="user4@test.com",
            password="123456",
        )
        DBSession.add(self.test_user4)

        self.test_user5 = User(
            name="User5",
            login="user5",
            email="user5@test.com",
            password="123456",
        )
        DBSession.add(self.test_user5)

        self.users_list = [
            self.test_user1,
            self.test_user2,
            self.test_user3,
            self.test_user4
        ]

        import datetime
        import pytz
        self.date_created = self.date_updated = datetime.datetime.now(pytz.utc)

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
        DBSession.add(self.test_department)
        DBSession.commit()

    def test_user_role_attribute(self):
        """testing the automatic generation of the DepartmentUser class
        """
        # assign a user to a department and search for a DepartmentUser
        # representing that relation
        from stalker import DepartmentUser
        from stalker.db.session import DBSession
        DBSession.commit()
        with DBSession.no_autoflush:
            self.test_department.users.append(self.test_user5)

        dus = DepartmentUser.query\
            .filter(DepartmentUser.user == self.test_user5)\
            .filter(DepartmentUser.department == self.test_department)\
            .all()

        assert len(dus) > 0
        du = dus[0]
        assert isinstance(du, DepartmentUser)
        assert du.department == self.test_department
        assert du.user == self.test_user5
        assert du.role == None

    def test_tjp_id_is_working_properly(self):
        """testing if the tjp_is working properly
        """
        assert self.test_department.tjp_id == 'Department_36'

    def test_to_tjp_is_working_properly(self):
        """testing if the to_tjp property is working properly
        """
        expected_tjp = """
resource Department_36 "Department_36" {
    resource User_31 "User_31" {
    efficiency 1.0
}
    resource User_32 "User_32" {
    efficiency 1.0
}
    resource User_33 "User_33" {
    efficiency 1.0
}
    resource User_34 "User_34" {
    efficiency 1.0
}
}"""
        # print expected_tjp
        # print "-----------------"
        # print self.test_department.to_tjp
        # self.maxDiff = None
        assert self.test_department.to_tjp == expected_tjp
