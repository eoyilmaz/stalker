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

from stalker.testing import UnitTestBase
from stalker import User

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UserTest(UnitTestBase):
    """Tests the user class
    """

    def setUp(self):
        """setup the test
        """
        super(UserTest, self).setUp()

        # need to have some test object for
        # a department
        from stalker import db, Department
        self.test_department1 = Department(
            name="Test Department 1"
        )
        self.test_department2 = Department(
            name="Test Department 2"
        )
        self.test_department3 = Department(
            name="Test Department 3"
        )

        db.DBSession.add_all([
            self.test_department1,
            self.test_department2,
            self.test_department3
        ])

        # a couple of groups
        from stalker import Group
        self.test_group1 = Group(
            name="Test Group 1"
        )
        self.test_group2 = Group(
            name="Test Group 2"
        )
        self.test_group3 = Group(
            name="Test Group 3"
        )

        db.DBSession.add_all([
            self.test_group1,
            self.test_group2,
            self.test_group3
        ])
        db.DBSession.commit()

        # a couple of statuses
        from stalker import Status, StatusList
        self.status_cmpl = Status.query.filter(Status.code == 'CMPL').first()
        self.status_wip = Status.query.filter(Status.code == "WIP").first()
        self.status_rts = Status.query.filter(Status.code == "RTS").first()
        self.status_prev = Status.query.filter(Status.code == "PREV").first()

        # a project status list
        self.project_status_list = StatusList(
            name="Project Status List",
            statuses=[
                self.status_cmpl,
                self.status_wip,
                self.status_rts,
                self.status_prev
            ],
            target_entity_type='Project',
        )

        # a repository type
        from stalker import Type, Repository, Project
        self.test_repository_type = Type(
            name="Test",
            code='test',
            target_entity_type=Repository,
        )

        # a repository
        self.test_repository = Repository(
            name="Test Repository",
            type=self.test_repository_type
        )

        # a project type
        self.commercial_project_type = Type(
            name="Commercial Project",
            code='comm',
            target_entity_type=Project,
        )

        # a couple of projects
        self.test_project1 = Project(
            name="Test Project 1",
            code='tp1',
            status_list=self.project_status_list,
            type=self.commercial_project_type,
            repository=self.test_repository,
        )

        self.test_project2 = Project(
            name="Test Project 2",
            code='tp2',
            status_list=self.project_status_list,
            type=self.commercial_project_type,
            repository=self.test_repository,
        )

        self.test_project3 = Project(
            name="Test Project 3",
            code='tp3',
            status_list=self.project_status_list,
            type=self.commercial_project_type,
            repository=self.test_repository,
        )

        db.DBSession.add_all([
            self.test_project1,
            self.test_project2,
            self.test_project3
        ])

        # a task status list
        self.task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()

        self.test_lead = User(
            name='lead',
            login='lead',
            email='lead@lead.com',
            password='12345'
        )

        # a couple of tasks
        from stalker import Task
        self.test_task1 = Task(
            name="Test Task 1",
            status_list=self.task_status_list,
            project=self.test_project1,
            responsible=[self.test_lead]
        )

        self.test_task2 = Task(
            name="Test Task 2",
            status_list=self.task_status_list,
            project=self.test_project1,
            responsible=[self.test_lead]
        )

        self.test_task3 = Task(
            name="Test Task 3",
            status_list=self.task_status_list,
            project=self.test_project2,
            responsible=[self.test_lead]
        )

        self.test_task4 = Task(
            name="Test Task 4",
            status_list=self.task_status_list,
            project=self.test_project3,
            responsible=[self.test_lead]
        )

        db.DBSession.add_all([
            self.test_task1,
            self.test_task2,
            self.test_task3,
            self.test_task4
        ])

        # for task1
        from stalker import Version
        self.test_version1 = Version(
            task=self.test_task1,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version1)

        self.test_version2 = Version(
            task=self.test_task1,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version2)

        self.test_version3 = Version(
            task=self.test_task1,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version3)

        # for task2
        self.test_version4 = Version(
            task=self.test_task2,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version4)

        self.test_version5 = Version(
            task=self.test_task2,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version5)

        self.test_version6 = Version(
            task=self.test_task2,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version6)

        # for task3
        self.test_version7 = Version(
            task=self.test_task3,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version7)

        self.test_version8 = Version(
            task=self.test_task3,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version8)

        self.test_version9 = Version(
            task=self.test_task3,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version9)

        # for task4
        self.test_version10 = Version(
            task=self.test_task4,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version10)

        self.test_version11 = Version(
            task=self.test_task4,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version11)

        self.test_version12 = Version(
            task=self.test_task4,
            full_path='some/path'
        )
        db.DBSession.add(self.test_version12)

        # *********************************************************************
        # Tickets
        # *********************************************************************

        # no need to create status list for tickets cause we have a database
        # set up an running so it will be automatically linked

        # tickets for version1
        from stalker import Ticket
        self.test_ticket1 = Ticket(
            project=self.test_project1,
            links=[self.test_version1],
        )
        db.DBSession.add(self.test_ticket1)
        # set it to closed
        self.test_ticket1.resolve()

        # create a new ticket and leave it open
        self.test_ticket2 = Ticket(
            project=self.test_project1,
            links=[self.test_version1],
        )
        db.DBSession.add(self.test_ticket2)

        # create a new ticket and close and then reopen it
        self.test_ticket3 = Ticket(
            project=self.test_project1,
            links=[self.test_version1],
        )
        db.DBSession.add(self.test_ticket3)
        self.test_ticket3.resolve()
        self.test_ticket3.reopen()

        # *********************************************************************
        # tickets for version2
        # create a new ticket and leave it open
        self.test_ticket4 = Ticket(
            project=self.test_project1,
            links=[self.test_version2],
        )
        db.DBSession.add(self.test_ticket4)

        # create a new Ticket and close it
        self.test_ticket5 = Ticket(
            project=self.test_project1,
            links=[self.test_version2],
        )
        db.DBSession.add(self.test_ticket5)
        self.test_ticket5.resolve()

        # create a new Ticket and close it
        self.test_ticket6 = Ticket(
            project=self.test_project1,
            links=[self.test_version3],
        )
        db.DBSession.add(self.test_ticket6)
        self.test_ticket6.resolve()

        # *********************************************************************
        # tickets for version3
        # create a new ticket and close it
        self.test_ticket7 = Ticket(
            project=self.test_project1,
            links=[self.test_version3],
        )
        db.DBSession.add(self.test_ticket7)
        self.test_ticket7.resolve()

        # create a new ticket and close it
        self.test_ticket8 = Ticket(
            project=self.test_project1,
            links=[self.test_version3],
        )
        db.DBSession.add(self.test_ticket8)
        self.test_ticket8.resolve()

        # *********************************************************************
        # tickets for version4
        # create a new ticket and close it
        self.test_ticket9 = Ticket(
            project=self.test_project1,
            links=[self.test_version4],
        )
        db.DBSession.add(self.test_ticket9)

        self.test_ticket9.resolve()

        # no tickets for any other version
        # *********************************************************************

        # a status list for sequence
        self.sequence_status_list = StatusList.query\
            .filter_by(target_entity_type='Sequence').first()

        # a couple of sequences
        from stalker import Sequence
        self.test_sequence1 = Sequence(
            name="Test Seq 1",
            code='ts1',
            project=self.test_project1,
            status_list=self.sequence_status_list
        )

        self.test_sequence2 = Sequence(
            name="Test Seq 2",
            code='ts2',
            project=self.test_project1,
            status_list=self.sequence_status_list
        )

        self.test_sequence3 = Sequence(
            name="Test Seq 3",
            code='ts3',
            project=self.test_project1,
            status_list=self.sequence_status_list
        )

        self.test_sequence4 = Sequence(
            name="Test Seq 4",
            code='ts4',
            project=self.test_project1,
            status_list=self.sequence_status_list
        )

        db.DBSession.add_all([
            self.test_sequence1,
            self.test_sequence2,
            self.test_sequence3,
            self.test_sequence4
        ])

        from stalker import defaults
        self.test_admin = \
            User.query.filter(User.name == defaults.admin_name).first()
        self.assertTrue(self.test_admin is not None)

        # create test company
        from stalker import Client
        self.test_company = Client(name='Test Company')

        # create the default values for parameters
        self.kwargs = {
            'name': 'Erkan Ozgur Yilmaz',
            'login': 'eoyilmaz',
            'description': 'this is a test user',
            'password': 'hidden',
            'email': 'eoyilmaz@fake.com',
            'departments': [self.test_department1],
            'groups': [self.test_group1,
                       self.test_group2],
            'created_by': self.test_admin,
            'updated_by': self.test_admin,
            'efficiency': 1.0,
            'companies': [self.test_company]
        }

        # create a proper user object
        self.test_user = User(**self.kwargs)
        db.DBSession.add(self.test_user)
        db.DBSession.commit()

        # just change the kwargs for other tests
        self.kwargs['name'] = 'some other name'
        self.kwargs['email'] = 'some@other.email'

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        User class
        """
        self.assertFalse(User.__auto_name__)

    def test_email_argument_accepting_only_string(self):
        """testing if email argument accepting only string values
        """
        # try to create a new user with wrong attribute
        self.kwargs["email"] = 1.3
        with self.assertRaises(TypeError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'User.email should be an instance of str not float'
        )

    def test_email_attribute_accepting_only_string_1(self):
        """testing if email attribute accepting only string values
        """
        # try to assign something else than a string
        test_value = 1

        with self.assertRaises(TypeError) as cm:
            self.test_user.email = test_value

        self.assertEqual(
            str(cm.exception),
            'User.email should be an instance of str not int'
        )

    def test_email_attribute_accepting_only_string_2(self):
        """testing if email attribute accepting only string values
        """
        # try to assign something else than a string
        test_value = ["an email"]

        with self.assertRaises(TypeError) as cm:
            self.test_user.email = test_value

        self.assertEqual(
            str(cm.exception),
            'User.email should be an instance of str not list'
        )

    def test_email_argument_format_1(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        # any of this values should raise a ValueError
        self.kwargs["email"] = "an email in no format"
        with self.assertRaises(ValueError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'check the formatting of User.email, there is no @ sign'
        )

    def test_email_argument_format_2(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        # any of this values should raise a ValueError
        self.kwargs["email"] = "an_email_with_no_part2"
        with self.assertRaises(ValueError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'check the formatting of User.email, there is no @ sign'
        )

    def test_email_argument_format_3(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        # any of this values should raise a ValueError
        self.kwargs["email"] = "@an_email_with_only_part2"
        with self.assertRaises(ValueError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'check the formatting of User.email, the name part is missing'
        )

    def test_email_argument_format_4(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        # any of this values should raise a ValueError
        self.kwargs["email"] = "@"
        with self.assertRaises(ValueError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'check the formatting of User.email, the name part is missing'
        )

    def test_email_attribute_format_1(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        # any of these email values should raise a ValueError
        with self.assertRaises(ValueError) as cm:
            self.test_user.email = "an email in no format"

        self.assertEqual(
            str(cm.exception),
            'check the formatting of User.email, there is no @ sign'
        )

    def test_email_attribute_format_2(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        # any of these email values should raise a ValueError
        with self.assertRaises(ValueError) as cm:
            self.test_user.email = "an_email_with_no_part2"

        self.assertEqual(
            str(cm.exception),
            'check the formatting of User.email, there is no @ sign'
        )

    def test_email_attribute_format_3(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        # any of these email values should raise a ValueError
        with self.assertRaises(ValueError) as cm:
            self.test_user.email = "@an_email_with_only_part2"

        self.assertEqual(
            str(cm.exception),
            'check the formatting of User.email, the name part is missing'
        )

    def test_email_attribute_format_4(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        # any of these email values should raise a ValueError
        with self.assertRaises(ValueError) as cm:
            self.test_user.email = "@"

        self.assertEqual(
            str(cm.exception),
            'check the formatting of User.email, the name part is missing'
        )

    def test_email_attribute_format_5(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        # any of these email values should raise a ValueError
        with self.assertRaises(ValueError) as cm:
            self.test_user.email = "eoyilmaz@"

        self.assertEqual(
            str(cm.exception),
            'check the formatting User.email, the domain part is missing'
        )

    def test_email_attribute_format_6(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        # any of these email values should raise a ValueError
        with self.assertRaises(ValueError) as cm:
            self.test_user.email = "eoyilmaz@some.compony@com"

        self.assertEqual(
            str(cm.exception),
            'check the formatting of User.email, there are more than one @ '
            'sign'
        )

    def test_email_argument_should_be_a_unique_value(self):
        """testing if the email argument should be a unique value
        """
        from stalker import db, User
        # this test should include a database
        test_email = "test@email.com"
        self.kwargs['login'] = 'test_user1'
        self.kwargs['email'] = test_email
        user1 = User(**self.kwargs)
        db.DBSession.add(user1)
        db.DBSession.commit()

        self.kwargs['login'] = 'test_user2'
        user2 = User(**self.kwargs)
        db.DBSession.add(user2)

        from sqlalchemy.exc import IntegrityError
        with self.assertRaises(IntegrityError) as cm:
            db.DBSession.commit()

        self.assertTrue(
            str(cm.exception).startswith(
                '(psycopg2.IntegrityError) duplicate key value violates '
                'unique constraint "Users_email_key"'
            )
        )

    def test_email_attribute_is_working_properly(self):
        """testing if email attribute works properly
        """
        test_email = "eoyilmaz@somemail.com"
        self.test_user.email = test_email
        self.assertEqual(self.test_user.email, test_email)

    def test_login_argument_conversion_to_strings(self):
        """testing if a ValueError will be raised when the given objects
        conversion to string results an empty string
        """
        self.kwargs["login"] = "----++==#@#$"
        with self.assertRaises(ValueError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'User.login can not be an empty string'
        )

    def test_login_argument_for_empty_string(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to login argument
        """
        self.kwargs["login"] = ""
        with self.assertRaises(ValueError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'User.login can not be an empty string'
        )

    def test_login_attribute_for_empty_string(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to login attribute
        """
        with self.assertRaises(ValueError) as cm:
            self.test_user.login = ''

        self.assertEqual(
            str(cm.exception),
            'User.login can not be an empty string'
        )

    def test_login_argument_is_skipped(self):
        """testing if a TypeError will be raised when the login argument is
        skipped
        """
        self.kwargs.pop("login")
        with self.assertRaises(TypeError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'User.login can not be None'
        )

    def test_login_argument_is_None(self):
        """testing if a TypeError will be raised when trying to assign None
        to login argument
        """
        self.kwargs["login"] = None
        with self.assertRaises(TypeError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'User.login can not be None'
        )

    def test_login_attribute_is_None(self):
        """testing if a TypeError will be raised when trying to assign None
        to login attribute
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.login = None

        self.assertEqual(
            str(cm.exception),
            'User.login can not be None'
        )

    def test_login_argument_formatted_correctly(self):
        """testing if login argument formatted correctly
        """
        #                 input       expected
        test_values = [
            ("e. ozgur", "eozgur"),
            ("erkan", "erkan"),
            ("Ozgur", "ozgur"),
            ("Erkan ozgur", "erkanozgur"),
            ("eRKAN", "erkan"),
            ("eRkaN", "erkan"),
            (" eRkAn", "erkan"),
            (" eRkan ozGur", "erkanozgur"),
            ("213 e.ozgur", "eozgur"),
        ]

        for valuePair in test_values:
            # set the input and expect the expected output
            self.kwargs["login"] = valuePair[0]
            test_user = User(**self.kwargs)
            self.assertEqual(
                test_user.login,
                valuePair[1]
            )

    def test_login_attribute_formatted_correctly(self):
        """testing if login attribute formatted correctly
        """
        #                 input       expected
        test_values = [
            ("e. ozgur", "eozgur"),
            ("erkan", "erkan"),
            ("Ozgur", "ozgur"),
            ("Erkan ozgur", "erkanozgur"),
            ("eRKAN", "erkan"),
            ("eRkaN", "erkan"),
            (" eRkAn", "erkan"),
            (" eRkan ozGur", "erkanozgur"),
        ]

        for valuePair in test_values:
            # set the input and expect the expected output
            self.test_user.login = valuePair[0]

            self.assertEqual(
                self.test_user.login,
                valuePair[1]
            )

    def test_login_argument_should_be_a_unique_value(self):
        """testing if the login argument should be a unique value
        """
        from stalker import db, User
        # this test should include a database
        test_login = 'test_user1'
        self.kwargs['login'] = test_login
        self.kwargs['email'] = "test1@email.com"
        user1 = User(**self.kwargs)
        db.DBSession.add(user1)
        db.DBSession.commit()

        self.kwargs['email'] = "test2@email.com"

        user2 = User(**self.kwargs)
        db.DBSession.add(user2)

        from sqlalchemy.exc import IntegrityError
        with self.assertRaises(IntegrityError) as cm:
            db.DBSession.commit()

        self.assertTrue(
            str(cm.exception).startswith(
                '(psycopg2.IntegrityError) duplicate key value violates '
                'unique constraint "Users_login_key"'
            )
        )

    def test_login_argument_is_working_properly(self):
        """testing if the login argument is working properly
        """
        self.assertEqual(self.test_user.login, self.kwargs['login'])

    def test_login_attribute_is_working_properly(self):
        """testing if the login attribute is working properly
        """
        test_value = 'newlogin'
        self.test_user.login = test_value
        self.assertEqual(self.test_user.login, test_value)

    def test_last_login_attribute_None(self):
        """testing if nothing happens when the last login attribute is set to
        None
        """
        # nothing should happen
        self.test_user.last_login = None

    def test_departments_argument_is_skipped(self):
        """testing if a User can be created without a Department instance
        """
        try:
            self.kwargs.pop('departments')
        except KeyError:
            pass

        new_user = User(**self.kwargs)
        self.assertEqual(new_user.departments, [])

    def test_departments_argument_is_None(self):
        """testing if a User can be created with the departments argument value
        is to None
        """
        self.kwargs['departments'] = None
        new_user = User(**self.kwargs)
        self.assertEqual(new_user.departments, [])

    def test_departments_attribute_is_set_None(self):
        """testing if a TypeError will be raised when the User's departments
        attribute set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.departments = None

        self.assertEqual(
            str(cm.exception),
            "'NoneType' object is not iterable"
        )

    def test_departments_argument_is_an_empty_list(self):
        """testing if a User can be created with the departments argument is an
        empty list
        """
        self.kwargs['departments'] = []
        User(**self.kwargs)

    def test_departments_attribute_is_an_empty_list(self):
        """testing if the departments attribute can be set to an empty list
        """
        self.test_user.departments = []
        self.assertEqual(self.test_user.departments, [])

    def test_departments_argument_only_accepts_list_of_department_objects(self):
        """testing if a TypeError will be raised when trying to assign
        anything other than a Department object to departments argument
        """
        # try to assign something other than a department object
        test_values = [
            "A department",
            1,
            1.0,
            ["a department"],
            {"a": "department"}
        ]

        self.kwargs["departments"] = test_values
        with self.assertRaises(TypeError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'DepartmentUser.department should be a '
            'stalker.models.department.Department instance, not str'
        )

    def test_departments_attribute_only_accepts_department_objects(self):
        """testing if a TypeError will be raised when trying to assign
        anything other than a Department object to departments attribute
        """
        # try to assign something other than a department
        test_value = "a department"
        with self.assertRaises(TypeError) as cm:
            self.test_user.departments = test_value

        self.assertEqual(
            str(cm.exception),
            'DepartmentUser.department should be a '
            'stalker.models.department.Department instance, not str'
        )

    def test_departments_attribute_works_properly(self):
        """testing if departments attribute works properly
        """
        # try to set and get the same value back
        self.test_user.departments = [self.test_department2]
        self.assertEqual(
            sorted(self.test_user.departments, key=lambda x: x.name),
            sorted([self.test_department2], key=lambda x: x.name)
        )

    def test_departments_attribute_supports_appending(self):
        """testing if departments attribute supports appending
        """
        self.test_user.departments = []
        self.test_user.departments.append(self.test_department1)
        self.test_user.departments.append(self.test_department2)
        self.assertEqual(
            sorted(self.test_user.departments, key=lambda x: x.name),
            sorted([self.test_department1, self.test_department2],
                   key=lambda x: x.name)
        )

    def test_password_argument_being_None(self):
        """testing if a TypeError will be raised when trying to assign None
        to the password argument
        """
        import copy
        kwargs = copy.copy(self.kwargs)
        kwargs["password"] = None
        with self.assertRaises(TypeError) as cm:
            User(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'User.password cannot be None'
        )

    def test_password_argument_is_an_empty_string(self):
        """testing if a ValueError will be raised the password argument is an
        empty string
        """
        import copy
        kwargs = copy.copy(self.kwargs)
        kwargs["password"] = ''

        with self.assertRaises(ValueError) as cm:
            User(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'User.password can not be an empty string'
        )

    def test_password_attribute_being_None(self):
        """testing if a TypeError will be raised when tyring to assign None to
        the password attribute
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.password = None

        self.assertEqual(
            str(cm.exception),
            'User.password cannot be None'
        )

    def test_password_attribute_works_properly(self):
        """testing if password attribute works properly
        """
        test_password = "a new test password"
        self.test_user.password = test_password
        self.assertNotEquals(self.test_user.password, test_password)

    def test_password_argument_being_scrambled(self):
        """testing if password is scrambled when trying to store it
        """
        test_password = "a new test password"
        self.kwargs["password"] = test_password
        new_user = User(**self.kwargs)
        self.assertNotEquals(new_user.password, test_password)

    def test_password_attribute_being_scrambled(self):
        """testing if password is scrambled when trying to store it
        """
        test_password = "a new test password"
        self.test_user.password = test_password

        # test if they are not the same any more
        self.assertNotEquals(self.test_user.password, test_password)

    def test_check_password_works_properly(self):
        """testing if check_password method works properly
        """
        test_password = "a new test password"
        self.test_user.password = test_password

        # check if it is scrambled
        self.assertNotEquals(self.test_user.password, test_password)

        # check if check_password returns True
        self.assertTrue(self.test_user.check_password(test_password))

        # check if check_password returns False
        self.assertFalse(self.test_user.check_password("wrong pass"))

    def test_groups_argument_for_None(self):
        """testing if the groups attribute will be an empty list
        when the groups argument is None
        """
        self.kwargs["groups"] = None
        new_user = User(**self.kwargs)
        self.assertEqual(new_user.groups, [])

    def test_groups_attribute_for_None(self):
        """testing if a TypeError will be raised when groups attribute is set
        to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.groups = None

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: None is not list-like'
        )

    def test_groups_argument_accepts_only_Group_instances(self):
        """testing if a TypeError will be raised when trying to assign anything
        other then a Group instances to the group argument
        """
        self.kwargs["groups"] = "a_group"
        with self.assertRaises(TypeError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: str is not list-like'
        )

    def test_groups_attribute_accepts_only_Group_instances(self):
        """testing if a TypeError will be raised when trying to assign anything
        other then a Group instances to the group attribute
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.groups = "a_group"

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: str is not list-like'
        )

    def test_groups_attribute_works_properly(self):
        """testing if groups attribute works properly
        """
        test_pg = [self.test_group3]
        self.test_user.groups = test_pg
        self.assertEqual(self.test_user.groups, test_pg)

    def test_groups_attribute_elements_accepts_Group_only_1(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a Group instances to the groups list
        """
        # append
        with self.assertRaises(TypeError) as cm:
            self.test_user.groups.append(0)

        self.assertEqual(
            str(cm.exception),
            'Any group in User.groups should be an instance of '
            'stalker.models.auth.Group not int'
        )

    def test_groups_attribute_elements_accepts_Group_only_2(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a Group instances to the groups list
        """
        # __setitem__
        with self.assertRaises(TypeError) as cm:
            self.test_user.groups[0] = 0

        self.assertEqual(
            str(cm.exception),
            'Any group in User.groups should be an instance of '
            'stalker.models.auth.Group not int'
        )

    def test_projects_attribute_is_None(self):
        """testing if a TypeError will be raised when the projects attribute is
        set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.projects = None

        self.assertEqual(
            str(cm.exception),
            "'NoneType' object is not iterable"
        )

    def test_projects_attribute_is_set_to_a_value_which_is_not_a_list(self):
        """testing if the projects attribute is accepting lists only
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.projects = 'not a list'

        self.assertEqual(
            str(cm.exception),
            'ProjectUser.project should be a stalker.models.project.Project '
            'instance, not str'
        )

    def test_projects_attribute_is_set_to_list_of_other_objects_than_Project_instances(self):
        """testing if a TypeError will be raised when the projects attribute is
        set to a value which is a list of other values than Projects instances
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.projects = \
                ['not', 'a', 'list', 'of', 'projects', 32]

        self.assertEqual(
            str(cm.exception),
            'ProjectUser.project should be a stalker.models.project.Project '
            'instance, not str'
        )

    def test_projects_attribute_is_working_properly(self):
        """testing if the projects attribute is working properly
        """
        self.test_user.rate = 102.0
        test_list = [self.test_project1, self.test_project2]
        self.test_user.projects = test_list
        self.assertEqual(
            sorted(test_list, key=lambda x: x.name),
            sorted(self.test_user.projects, key=lambda x: x.name)
        )
        self.test_user.projects.append(self.test_project3)
        self.assertTrue(self.test_project3 in self.test_user.projects)
        # also check the back ref
        self.assertTrue(self.test_user in self.test_project1.users)
        self.assertTrue(self.test_user in self.test_project2.users)
        self.assertTrue(self.test_user in self.test_project3.users)

    def test_tasks_attribute_None(self):
        """testing if a TypeError will be raised when the tasks attribute is
        set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.tasks = None

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: None is not list-like'
        )

    def test_tasks_attribute_accepts_only_list_of_task_objects(self):
        """testing if a TypeError will be raised when trying to assign
        anything other than a list of task objects to the tasks argument
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.tasks = "aTask1"

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: str is not list-like'
        )

    def test_tasks_attribute_accepts_an_empty_list(self):
        """testing if nothing happens when trying to assign an empty list to
        tasks attribute
        """
        # this should work without any error
        self.test_user.tasks = []

    def test_tasks_attribute_works_properly(self):
        """testing if tasks attribute is working properly
        """
        tasks = [self.test_task1,
                 self.test_task2,
                 self.test_task3,
                 self.test_task4]

        self.test_user.tasks = tasks

        self.assertEqual(self.test_user.tasks, tasks)

    def test_tasks_attribute_elements_accepts_Tasks_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than a Task object to the tasks list
        """
        # append
        with self.assertRaises(TypeError) as cm:
            self.test_user.tasks.append(0)

        self.assertEqual(
            str(cm.exception),
            'Any element in User.tasks should be an instance of '
            'stalker.models.task.Task not int'
        )

    def test_equality_operator(self):
        """testing equality of two users
        """
        self.kwargs.update({
            "name": "Generic User",
            "description": "this is a different user",
            "login": "guser",
            "email": "generic.user@generic.com",
            "password": "verysecret",
        })

        new_user = User(**self.kwargs)

        self.assertFalse(self.test_user == new_user)

    def test_inequality_operator(self):
        """testing inequality of two users
        """
        self.kwargs.update({
            "name": "Generic User",
            "description": "this is a different user",
            "login": "guser",
            "email": "generic.user@generic.com",
            "password": "verysecret",
        })

        new_user = User(**self.kwargs)

        self.assertTrue(self.test_user != new_user)

    def test___repr__(self):
        """testing the representation
        """
        self.assertEqual(
            self.test_user.__repr__(),
            "<%s ('%s') (User)>" % (
                self.test_user.name,
                self.test_user.login)
        )

    def test_tickets_attribute_is_an_empty_list_by_default(self):
        """testing if the User.tickets is an empty list by default
        """
        self.assertEqual(self.test_user.tickets, [])

    def test_open_tickets_attribute_is_an_empty_list_by_default(self):
        """testing if the User.open_tickets is an empty list by default
        """
        self.assertEqual(self.test_user.open_tickets, [])

    def test_tickets_attribute_is_read_only(self):
        """testing if the User.tickets attribute is a read only attribute
        """
        with self.assertRaises(AttributeError) as cm:
            self.test_user.tickets = []

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

    def test_open_tickets_attribute_is_read_only(self):
        """testing if the User.open_tickets attribute is a read only attribute
        """
        with self.assertRaises(AttributeError) as cm:
            self.test_user.open_tickets = []

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

    def test_tickets_attribute_returns_all_tickets_owned_by_this_user(self):
        """testing if User.tickets returns all the tickets owned by this user
        """
        self.assertEqual(len(self.test_user.tasks), 0)

        # there should be no tickets assigned to this user
        self.assertTrue(self.test_user.tickets == [])

        # be careful not all of these are open tickets
        self.test_ticket1.reassign(self.test_user, self.test_user)
        self.test_ticket2.reassign(self.test_user, self.test_user)
        self.test_ticket3.reassign(self.test_user, self.test_user)
        self.test_ticket4.reassign(self.test_user, self.test_user)
        self.test_ticket5.reassign(self.test_user, self.test_user)
        self.test_ticket6.reassign(self.test_user, self.test_user)
        self.test_ticket7.reassign(self.test_user, self.test_user)
        self.test_ticket8.reassign(self.test_user, self.test_user)

        # now we should have some tickets
        self.assertTrue(len(self.test_user.tickets) > 0)

        # now check for exact items
        self.assertEqual(
            sorted(self.test_user.tickets, key=lambda x: x.name),
            sorted([self.test_ticket2, self.test_ticket3, self.test_ticket4],
                   key=lambda x: x.name)
        )

    def test_open_tickets_attribute_returns_all_open_tickets_owned_by_this_user(self):
        """testing if User.open_tickets returns all the open tickets owned by
        this user
        """
        self.assertEqual(len(self.test_user.tasks), 0)

        # there should be no tickets assigned to this user
        self.assertTrue(self.test_user.open_tickets == [])

        # assign the user to some tickets
        self.test_ticket1.reopen(self.test_user)
        self.test_ticket2.reopen(self.test_user)
        self.test_ticket3.reopen(self.test_user)
        self.test_ticket4.reopen(self.test_user)
        self.test_ticket5.reopen(self.test_user)
        self.test_ticket6.reopen(self.test_user)
        self.test_ticket7.reopen(self.test_user)
        self.test_ticket8.reopen(self.test_user)

        # be careful not all of these are open tickets
        self.test_ticket1.reassign(self.test_user, self.test_user)
        self.test_ticket2.reassign(self.test_user, self.test_user)
        self.test_ticket3.reassign(self.test_user, self.test_user)
        self.test_ticket4.reassign(self.test_user, self.test_user)
        self.test_ticket5.reassign(self.test_user, self.test_user)
        self.test_ticket6.reassign(self.test_user, self.test_user)
        self.test_ticket7.reassign(self.test_user, self.test_user)
        self.test_ticket8.reassign(self.test_user, self.test_user)

        # now we should have some open tickets
        self.assertTrue(len(self.test_user.open_tickets) > 0)

        # now check for exact items
        self.assertEqual(
            sorted(self.test_user.open_tickets, key=lambda x: x.name),
            sorted([
                self.test_ticket1,
                self.test_ticket2,
                self.test_ticket3,
                self.test_ticket4,
                self.test_ticket5,
                self.test_ticket6,
                self.test_ticket7,
                self.test_ticket8,
            ], key=lambda x: x.name)
        )

        # close a couple of them
        from stalker.models.ticket import FIXED, CANTFIX, INVALID

        self.test_ticket1.resolve(self.test_user, FIXED)
        self.test_ticket2.resolve(self.test_user, INVALID)
        self.test_ticket3.resolve(self.test_user, CANTFIX)

        # new check again
        self.assertEqual(
            sorted(self.test_user.open_tickets, key=lambda x: x.name),
            sorted([
                self.test_ticket4,
                self.test_ticket5,
                self.test_ticket6,
                self.test_ticket7,
                self.test_ticket8
            ], key=lambda x: x.name)
        )

    def test_tjp_id_is_working_properly(self):
        """testing if the tjp_id is working properly
        """
        self.assertEqual(self.test_user.tjp_id, 'User_%s' % self.test_user.id)

    def test_to_tjp_is_working_properly(self):
        """testing if the to_tjp property is working properly
        """
        expected_tjp = \
            'resource User_%s "User_%s" {\n    efficiency 1.0\n}' % \
            (self.test_user.id, self.test_user.id)

        self.assertEqual(expected_tjp, self.test_user.to_tjp)

    def test_to_tjp_is_working_properly_for_a_user_with_vacations(self):
        """testing if the to_tjp property is working properly for a user with
        vacations
        """
        import datetime
        import pytz
        from stalker import Vacation, Type

        personal_vacation = Type(
            name='Personal',
            code='PERS',
            target_entity_type='Vacation'
        )

        Vacation(
            user=self.test_user,
            type=personal_vacation,
            start=datetime.datetime(2013, 6, 7, 0, 0, tzinfo=pytz.utc),
            end=datetime.datetime(2013, 6, 21, 0, 0, tzinfo=pytz.utc)
        )

        Vacation(
            user=self.test_user,
            type=personal_vacation,
            start=datetime.datetime(2013, 7, 1, 0, 0, tzinfo=pytz.utc),
            end=datetime.datetime(2013, 7, 15, 0, 0, tzinfo=pytz.utc)
        )

        expected_tjp = """resource User_%s "User_%s" {
    efficiency 1.0
    vacation 2013-06-07-03:00:00 - 2013-06-21-03:00:00
    vacation 2013-07-01-03:00:00 - 2013-07-15-03:00:00
}""" % (self.test_user.id, self.test_user.id)

        # print expected_tjp
        # print '---------------'
        # print self.test_user.to_tjp

        self.assertEqual(
            expected_tjp,
            self.test_user.to_tjp
        )

    def test_vacations_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the vacations attribute
        is set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.vacations = None

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: None is not list-like'
        )

    def test_vacations_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the vacations attribute
        is set to a value other than a list
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.vacations = 'not a list of Vacation instances'

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: str is not list-like'
        )

    def test_vacations_attribute_is_not_a_list_of_Vacation_instances(self):
        """testing if a TypeError will be raised when the vacations attribute
        is set to a list of other objects than Vacation instances
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.vacations = ['list of', 'other', 'instances', 1]

        self.assertEqual(
            str(cm.exception),
            'All of the elements in User.vacations should be a '
            'stalker.models.studio.Vacation instance, not str'
        )

    def test_vacations_attribute_is_working_properly(self):
        """testing if the vacations attribute is working properly
        """
        import datetime
        import pytz
        from stalker import Type, Vacation
        some_other_user = User(
            name='Some Other User',
            login='sou',
            email='some@other.user.com',
            password='my password'
        )

        personal_vac_type = Type(
            name='Personal Vacation',
            code='PERS',
            target_entity_type='Vacation'
        )

        vac1 = Vacation(
            user=some_other_user,
            type=personal_vac_type,
            start=datetime.datetime(2013, 6, 7, tzinfo=pytz.utc),
            end=datetime.datetime(2013, 6, 10, tzinfo=pytz.utc)
        )

        self.assertFalse(
            vac1 in self.test_user.vacations
        )

        self.test_user.vacations.append(vac1)

        self.assertTrue(
            vac1 in self.test_user.vacations
        )

    def test_efficiency_argument_skipped(self):
        """testing if the efficiency attribute value will be 1.0 if the
        efficiency argument is skipped
        """
        self.kwargs.pop('efficiency')
        new_user = User(**self.kwargs)
        self.assertEqual(1.0, new_user.efficiency)

    def test_efficiency_argument_is_None(self):
        """testing if the efficiency attribute value will be 1.0 if the
        efficiency argument is None
        """
        self.kwargs['efficiency'] = None
        new_user = User(**self.kwargs)
        self.assertEqual(1.0, new_user.efficiency)

    def test_efficiency_attribute_is_set_to_None(self):
        """testing if the efficiency attribute value will be 1.0 if it is set
        to None
        """
        self.test_user.efficiency = 4.0
        self.test_user.efficiency = None
        self.assertEqual(1.0, self.test_user.efficiency)

    def test_efficiency_argument_is_not_a_float_or_integer(self):
        """testing if a TypeError will be raised when the efficiency argument
        is not a float or integer
        """
        self.kwargs['efficiency'] = 'not a float or integer'
        with self.assertRaises(TypeError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            'User.efficiency should be a float number greater or equal to '
            '0.0, not str',
            str(cm.exception)
        )

    def test_efficiency_attribute_is_not_a_float_or_integer(self):
        """testing if a TypeError will be raised when the efficiency attribute
        is set to a value other than a float or integer
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.efficiency = 'not a float or integer'

        self.assertEqual(
            'User.efficiency should be a float number greater or equal to '
            '0.0, not str',
            str(cm.exception)
        )

    def test_efficiency_argument_is_a_negative_float_or_integer(self):
        """testing if a ValueError will be raised when the efficiency argument
        is a negative float or integer
        """
        self.kwargs['efficiency'] = -1
        with self.assertRaises(ValueError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            'User.efficiency should be a float number greater or equal to '
            '0.0, not -1',
            str(cm.exception)
        )

    def test_efficiency_attribute_is_a_negative_float_or_integer(self):
        """testing if a ValueError will be raised when the efficiency attribute
        is set to a negative float or integer
        """
        with self.assertRaises(ValueError) as cm:
            self.test_user.efficiency = -2.0

        self.assertEqual(
            'User.efficiency should be a float number greater or equal to '
            '0.0, not -2.0',
            str(cm.exception)
        )

    def test_efficiency_argument_is_working_properly(self):
        """testing if the efficiency argument value is correctly passed to the
        efficiency attribute
        """
        # integer value
        self.kwargs['efficiency'] = 2
        new_user = User(**self.kwargs)
        self.assertEqual(
            2.0,
            new_user.efficiency
        )

        # float value
        self.kwargs['efficiency'] = 2.3
        new_user = User(**self.kwargs)
        self.assertEqual(
            2.3,
            new_user.efficiency
        )

    def test_efficiency_attribute_is_working_properly(self):
        """testing if the efficiency attribute value can correctly be changed
        """
        # integer
        self.assertNotEqual(
            2,
            self.test_user.efficiency
        )

        self.test_user.efficiency = 2
        self.assertEqual(
            2.0,
            self.test_user.efficiency
        )

        # float
        self.assertNotEqual(
            2.3,
            self.test_user.efficiency
        )

        self.test_user.efficiency = 2.3
        self.assertEqual(
            2.3,
            self.test_user.efficiency
        )

    def test_companies_argument_is_skipped(self):
        """testing if the companies attribute will be set to an empty list when
        the company argument is skipped
        """
        self.kwargs.pop('companies')
        new_user = User(**self.kwargs)
        self.assertEquals(new_user.companies, [])

    def test_companies_argument_is_None(self):
        """testing if the companies argument is set to None the companies
        attribute will be an empty list
        """
        self.kwargs['companies'] = None
        new_user = User(**self.kwargs)
        self.assertTrue(new_user.companies == [])

    def test_companies_attribute_is_set_to_None(self):
        """testing if a the companies attribute will be an empty list if it is
        set to None
        """
        self.assertTrue(self.test_user.companies is not None)
        with self.assertRaises(TypeError) as cm:
            self.test_user.companies = None
        self.assertEqual(
            str(cm.exception),
            "'NoneType' object is not iterable"
        )

    def test_companies_argument_is_not_a_list(self):
        """testing if a TypeError will be raised if the companies argument is
        not a list
        """
        self.kwargs['companies'] = 'not a list of clients'
        with self.assertRaises(TypeError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'ClientUser.client should be instance of '
            'stalker.models.client.Client, not str'
        )

    def test_companies_argument_is_not_a_list_of_client_instances(self):
        """testing if a TypeError will be raised when the companies argument is
        not a list of Client instances
        """
        test_value = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        self.kwargs["companies"] = test_value
        with self.assertRaises(TypeError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'ClientUser.client should be instance of '
            'stalker.models.client.Client, not int'
        )

    def test_companies_attribute_is_set_to_a_value_other_than_a_list_of_client_instances(self):
        """testing if a TypeError will be raised when the companies attribute
        is set to a value other than a list of Client instances
        """
        test_value = [1, 1.2, "a user", ["a", "user"], {"a": "user"}]
        with self.assertRaises(TypeError) as cm:
            self.test_user.companies = test_value

        self.assertEqual(
            str(cm.exception),
            'ClientUser.client should be instance of '
            'stalker.models.client.Client, not int'
        )

    def test_companies_attribute_is_working_properly(self):
        """from issue #27
        """
        from stalker import db, Client, User
        new_companies = []
        c1 = Client(name='Company X')
        c2 = Client(name='Company Y')
        c3 = Client(name='Company Z')
        db.DBSession.add_all([c1, c2, c3])
        db.DBSession.commit()

        c1 = Client.query.filter_by(name='Company X').first()
        c2 = Client.query.filter_by(name='Company Y').first()
        c3 = Client.query.filter_by(name='Company Z').first()

        user = User(name='test_user', password='1234', email='a@a.com',
                    login='test_user', clients=[c3])
        db.DBSession.commit()

        new_companies.append(c1)
        new_companies.append(c2)
        user.companies = new_companies
        db.DBSession.commit()

        self.assertTrue(c1 in user.companies)
        self.assertTrue(c2 in user.companies)
        self.assertTrue(c3 not in user.companies)

    def test_companies_attribute_is_working_properly_2(self):
        """from issue #27
        """
        from stalker import db, Client, User
        c1 = Client(name='Company X')
        c2 = Client(name='Company Y')
        c3 = Client(name='Company Z')

        user = User(
            name='Fredrik',
            login='fredrik',
            email='f@f.f',
            password='pass',
            companies=[c1, c2, c3]
        )

        db.DBSession.add(user)

        self.assertTrue(c1 in db.DBSession)
        self.assertTrue(c2 in db.DBSession)
        self.assertTrue(c3 in db.DBSession)

        db.DBSession.commit()

        c1 = Client(name='New Company X')
        c2 = Client(name='New Company Y')
        c3 = Client(name='New Company Z')

        db.DBSession.add_all([c1, c2, c3])
        db.DBSession.commit()

        user = User.query.filter_by(name='Fredrik').first()
        user.companies = [c1, c2, c3]

        db.DBSession.commit()

    def test_watching_attribute_is_a_list_of_other_values_than_Task(self):
        """testing if a TypeError will be raised when the watching attribute is
        set to a list of other values than a Task
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.watching = ['not', 1, 'list of tasks']

        self.assertEqual(
            str(cm.exception),
            'Any element in User.watching should be an instance of '
            'stalker.models.task.Task not str'
        )

    def test_watching_attribute_is_working_properly(self):
        """testing if the watching attribute is working properly
        """
        test_value = [self.test_task1, self.test_task2]
        self.assertEqual(self.test_user.watching, [])
        self.test_user.watching = test_value
        self.assertEqual(
            sorted(test_value, key=lambda x: x.name),
            sorted(self.test_user.watching, key=lambda x: x.name)
        )

    def test_rate_argument_is_skipped(self):
        """testing if the rate attribute will be 0 when the rate argument is
        skipped
        """
        if 'rate' in self.kwargs:
            self.kwargs.pop('rate')

        new_user = User(**self.kwargs)
        self.assertEqual(new_user.rate, 0)

    def test_rate_argument_is_none(self):
        """testing if the rate attribute will be 0 when the rate argument is
        None
        """
        self.kwargs['rate'] = None
        new_user = User(**self.kwargs)
        self.assertEqual(new_user.rate, 0)

    def test_rate_attribute_is_set_to_none(self):
        """testing if the rate will be set to 0 if it is set to None
        """
        self.assertNotEqual(self.test_user.rate, None)

        self.test_user.rate = None
        self.assertEqual(self.test_user.rate, 0)

    def test_rate_argument_is_not_a_float_or_integer_value(self):
        """testing if a TypeError will be raised when the rate argument is not
        an integer or float value
        """
        self.kwargs['rate'] = 'some string'
        with self.assertRaises(TypeError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'User.rate should be a float number greater or equal to 0.0, not '
            'str'
        )

    def test_rate_attribute_is_not_a_float_or_integer_value(self):
        """testing if a TypeError will be raised when the rate attribute is set
        to a value other than an integer or float
        """
        with self.assertRaises(TypeError) as cm:
            self.test_user.rate = 'some string'

        self.assertEqual(
            str(cm.exception),
            'User.rate should be a float number greater or equal to 0.0, not '
            'str'
        )

    def test_rate_argument_is_a_negative_number(self):
        """testing if a ValueError will be raised when the rate argument is a
        negative value
        """
        self.kwargs['rate'] = -1
        with self.assertRaises(ValueError) as cm:
            User(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'User.rate should be a float number greater or equal to 0.0, not '
            '-1'
        )

    def test_rate_attribute_is_set_to_a_negative_number(self):
        """testing if a ValueError will be raised when the rate attribute is
        set to a negative number
        """
        with self.assertRaises(ValueError) as cm:
            self.test_user.rate = -1

        self.assertEqual(
            str(cm.exception),
            'User.rate should be a float number greater or equal to 0.0, not '
            '-1'
        )

    def test_rate_argument_is_working_properly(self):
        """testing if the rate argument is working properly
        """
        test_value = 102.3
        self.kwargs['rate'] = test_value
        new_user = User(**self.kwargs)
        self.assertEqual(new_user.rate, test_value)

    def test_rate_attribute_is_working_properly(self):
        """testing if rate attribute is working properly
        """
        test_value = 212.5
        self.assertNotEqual(self.test_user.rate, test_value)
        self.test_user.rate = test_value
        self.assertEqual(self.test_user.rate, test_value)
