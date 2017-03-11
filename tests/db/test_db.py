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

import logging
from stalker import log
from stalker.testing import UnitTestBase

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


class DatabaseTester(UnitTestBase):
    """tests the database and connection to the database
    """

    # def setUp(self):
    #     """set the test up
    #     """
    #     super(DatabaseTester, self).setUp()

    # def test_creating_a_custom_in_memory_db(self):
    #     """testing if a custom in-memory sqlite database will be created
    #     """
    #     # try to persist a user and get it back
    #     # create a new user
    #     kwargs = {
    #         "name": "Erkan Ozgur Yilmaz",
    #         "login": "eoyilmaz",
    #         "email": "eoyilmaz@gmail.com",
    #         #"created_by": admin,
    #         "password": "password",
    #     }
    #
    #     from stalker import db, User
    #     new_user = User(**kwargs)
    #     db.DBSession.add(new_user)
    #     db.DBSession.commit()
    #
    #     # now check if the newUser is there
    #     new_user_db = User.query.filter_by(name=kwargs["name"]).first()
    #
    #     self.assertTrue(new_user_db is not None)

    def test_default_admin_creation(self):
        """testing if a default admin is created
        """
        # set default admin creation to True
        from stalker import db, defaults
        defaults.auto_create_admin = True

        # check if there is an admin
        from stalker import User
        admin_db = User.query.filter(User.name == defaults.admin_name).first()

        self.assertEqual(admin_db.name, defaults.admin_name)

    def test_default_admin_for_already_created_databases(self):
        """testing if no extra admin is going to be created for already setup
        databases
        """
        # set default admin creation to True
        from stalker import db, defaults
        defaults.auto_create_admin = True
        db.init()

        # try to call the init() for a second time and see if there are more
        # than one admin
        db.init()

        # and get how many admin is created, (it is impossible to create
        # second one because the tables.simpleEntity.c.nam.unique=True

        from stalker import User
        admins = User.query.filter_by(name=defaults.admin_name).all()

        self.assertTrue(len(admins) == 1)

    def test_no_default_admin_creation(self):
        """testing if there is no user if stalker.config.Conf.auto_create_admin
        is False
        """
        # turn down auto admin creation
        from stalker import db, defaults
        defaults.auto_create_admin = False

        # create a clean database
        self.tearDown()

        # init the db
        db.setup(self.config)
        db.init()

        # Restore auto admin creation
        defaults.auto_create_admin = True

        # check if there is a use with name admin
        from stalker import User
        self.assertTrue(
            User.query.filter_by(name=defaults.admin_name).first()
            is None
        )

        # check if there is a admins department
        from stalker import Department
        self.assertTrue(
            Department.query
            .filter_by(name=defaults.admin_department_name)
            .first() is None
        )

    def test_non_unique_names_on_different_entity_type(self):
        """testing if there can be non-unique names for different entity types
        """
        # try to create a user and an entity with same name
        # expect Nothing
        kwargs = {
            "name": "user1",
            #"created_by": admin
        }

        from stalker import db, Entity
        entity1 = Entity(**kwargs)
        db.DBSession.add(entity1)
        db.DBSession.commit()

        # lets create the second user
        kwargs.update({
            "name": "User1 Name",
            "login": "user1",
            "email": "user1@gmail.com",
            "password": "user1",
        })

        from stalker import User
        user1 = User(**kwargs)
        db.DBSession.add(user1)

        # expect nothing, this should work without any error
        db.DBSession.commit()

    def test_ticket_status_initialization(self):
        """testing if the ticket statuses are correctly created
        """
        from stalker import StatusList
        ticket_status_list = StatusList.query \
            .filter(StatusList.name == 'Ticket Statuses') \
            .first()

        self.assertTrue(isinstance(ticket_status_list, StatusList))

        expected_status_names = [
            'New',
            'Reopened',
            'Closed',
            'Accepted',
            'Assigned'
        ]

        self.assertEqual(len(ticket_status_list.statuses),
                         len(expected_status_names))
        for status in ticket_status_list.statuses:
            self.assertTrue(status.name in expected_status_names)

    def test_daily_status_initialization(self):
        """testing if the daily statuses are correctly created
        """
        from stalker import StatusList
        daily_status_list = StatusList.query \
            .filter(StatusList.name == 'Daily Statuses') \
            .first()

        self.assertTrue(isinstance(daily_status_list, StatusList))

        expected_status_names = [
            'Open',
            'Closed'
        ]

        self.assertEqual(len(daily_status_list.statuses),
                         len(expected_status_names))

        from stalker import User
        admin = User.query.filter(User.name == 'admin').first()
        for status in daily_status_list.statuses:
            self.assertTrue(status.name in expected_status_names)
            # check if the created_by and updated_by attributes
            # are set to admin
            self.assertEqual(status.created_by, admin)
            self.assertEqual(status.updated_by, admin)

    def test_register_creates_suitable_Permissions(self):
        """testing if stalker.db.register is able to create suitable
        Permissions
        """
        from stalker import db

        # create a new dummy class
        class TestClass(object):
            pass

        db.register(TestClass)

        # now check if the TestClass entry is created in Permission table

        from stalker import Permission
        permissions_db = Permission.query \
            .filter(Permission.class_name == 'TestClass') \
            .all()

        logger.debug("%s" % permissions_db)

        from stalker import defaults
        actions = defaults.actions

        for action in permissions_db:
            self.assertTrue(action.action in actions)

    def test_register_raise_TypeError_for_wrong_class_name_argument(self):
        """testing if a TypeError will be raised if the class_name argument is
        not an instance of type or str
        """
        from stalker import db
        with self.assertRaises(TypeError):
            db.register(23425)

    def test_permissions_created_for_all_the_classes(self):
        """testing if Permission instances are created for classes in the SOM
        """
        class_names = [
            'Asset', 'AuthenticationLog', 'Budget', 'BudgetEntry', 'Client',
            'Good', 'Group', 'Permission', 'User', 'Department',
            'SimpleEntity', 'Entity', 'EntityGroup', 'ImageFormat', 'Link',
            'Message', 'Note', 'Page', 'Project', 'PriceList', 'Repository',
            'Review', 'Role', 'Scene', 'Sequence', 'Shot', 'Status',
            'StatusList', 'Structure', 'Studio', 'Tag', 'TimeLog', 'Task',
            'FilenameTemplate', 'Ticket', 'TicketLog', 'Type', 'Vacation',
            'Version', 'Daily', 'Invoice', 'Payment',
        ]

        from stalker import defaults, Permission
        permission_db = Permission.query.all()

        self.assertEqual(
            len(permission_db),
            len(class_names) * len(defaults.actions) * 2
        )

        for permission in permission_db:
            self.assertTrue(permission.access in ['Allow', 'Deny'])
            self.assertTrue(permission.action in defaults.actions)
            self.assertTrue(permission.class_name in class_names)
            logger.debug('permission.access: %s' % permission.access)
            logger.debug('permission.action: %s' % permission.action)
            logger.debug('permission.class_name: %s' % permission.class_name)

    def test_permissions_not_created_over_and_over_again(self):
        """testing if the Permissions are created only once and trying to call
        __init_db__ will not raise any error
        """
        from stalker import db
        db.DBSession.remove()
        # DBSession.close()
        db.setup(self.config)
        db.init()

        # this should not give any error
        db.DBSession.remove()

        db.setup(self.config)
        db.init()

        # and we still have correct amount of Permissions
        from stalker import Permission
        permissions = Permission.query.all()
        self.assertEqual(len(permissions), 420)

    def test_ticket_statuses_are_not_created_over_and_over_again(self):
        """testing if the Ticket Statuses are created only once and trying to
        call __init_db__ will not raise any error
        """
        # create the environment variable and point it to a temp directory
        from stalker import db
        db.DBSession.remove()

        db.setup(self.config)
        db.init()

        # this should not give any error
        db.setup(self.config)
        db.init()

        # this should not give any error
        db.setup(self.config)
        db.init()

        # and we still have correct amount of Statuses
        from stalker import Status, StatusList
        statuses = Status.query.all()
        self.assertEqual(len(statuses), 17)

        status_list = \
            StatusList.query.filter_by(target_entity_type='Ticket').first()
        self.assertTrue(status_list is not None)
        self.assertEqual(status_list.name, 'Ticket Statuses')

    def test_task_status_initialization(self):
        """testing if the task statuses are correctly created
        """
        from stalker import StatusList
        task_status_list = StatusList.query \
            .filter(StatusList.name == 'Task Statuses') \
            .first()

        self.assertTrue(isinstance(task_status_list, StatusList))

        expected_status_names = [
            'Waiting For Dependency',
            'Ready To Start',
            'Work In Progress',
            'Pending Review',
            'Has Revision',
            'Dependency Has Revision',
            'On Hold',
            'Stopped',
            'Completed'
        ]

        expected_status_codes = [
            'WFD',
            'RTS',
            'WIP',
            'PREV',
            'HREV',
            'DREV',
            'OH',
            'STOP',
            'CMPL'
        ]

        self.assertEqual(
            len(task_status_list.statuses),
            len(expected_status_names)
        )

        db_status_names = map(lambda x: x.name, task_status_list.statuses)
        db_status_codes = map(lambda x: x.code, task_status_list.statuses)
        self.assertEqual(
            sorted(expected_status_names),
            sorted(db_status_names)
        )
        self.assertEqual(
            sorted(expected_status_codes),
            sorted(db_status_codes)
        )

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        from stalker import User
        admin = User.query.filter(User.name == 'admin').first()
        for status in task_status_list.statuses:
            self.assertEqual(status.created_by, admin)
            self.assertEqual(status.updated_by, admin)

    def test_asset_status_initialization(self):
        """testing if the asset statuses are correctly created
        """
        from stalker import StatusList
        asset_status_list = StatusList.query \
            .filter(StatusList.name == 'Asset Statuses') \
            .first()

        self.assertTrue(isinstance(asset_status_list, StatusList))

        expected_status_names = [
            'Waiting For Dependency',
            'Ready To Start',
            'Work In Progress',
            'Pending Review',
            'Has Revision',
            'Dependency Has Revision',
            'On Hold',
            'Stopped',
            'Completed'
        ]

        expected_status_codes = [
            'WFD',
            'RTS',
            'WIP',
            'PREV',
            'HREV',
            'DREV',
            'OH',
            'STOP',
            'CMPL'
        ]

        self.assertEqual(
            len(asset_status_list.statuses),
            len(expected_status_names)
        )

        db_status_names = map(lambda x: x.name, asset_status_list.statuses)
        db_status_codes = map(lambda x: x.code, asset_status_list.statuses)
        self.assertEqual(
            sorted(expected_status_names),
            sorted(db_status_names)
        )
        self.assertEqual(
            sorted(expected_status_codes),
            sorted(db_status_codes)
        )

    def test_shot_status_initialization(self):
        """testing if the shot statuses are correctly created
        """
        from stalker import StatusList
        shot_status_list = StatusList.query \
            .filter(StatusList.name == 'Shot Statuses') \
            .first()

        self.assertTrue(isinstance(shot_status_list, StatusList))

        expected_status_names = [
            'Waiting For Dependency',
            'Ready To Start',
            'Work In Progress',
            'Pending Review',
            'Has Revision',
            'Dependency Has Revision',
            'On Hold',
            'Stopped',
            'Completed'
        ]

        expected_status_codes = [
            'WFD',
            'RTS',
            'WIP',
            'PREV',
            'HREV',
            'DREV',
            'OH',
            'STOP',
            'CMPL'
        ]

        self.assertEqual(
            len(shot_status_list.statuses),
            len(expected_status_names)
        )

        db_status_names = map(lambda x: x.name, shot_status_list.statuses)
        db_status_codes = map(lambda x: x.code, shot_status_list.statuses)
        self.assertEqual(
            sorted(expected_status_names),
            sorted(db_status_names)
        )
        self.assertEqual(
            sorted(expected_status_codes),
            sorted(db_status_codes)
        )

    def test_sequence_status_initialization(self):
        """testing if the sequence statuses are correctly created
        """
        from stalker import StatusList
        sequence_status_list = StatusList.query \
            .filter(StatusList.name == 'Sequence Statuses') \
            .first()

        self.assertTrue(isinstance(sequence_status_list, StatusList))

        expected_status_names = [
            'Waiting For Dependency',
            'Ready To Start',
            'Work In Progress',
            'Pending Review',
            'Has Revision',
            'Dependency Has Revision',
            'On Hold',
            'Stopped',
            'Completed'
        ]

        expected_status_codes = [
            'WFD',
            'RTS',
            'WIP',
            'PREV',
            'HREV',
            'DREV',
            'OH',
            'STOP',
            'CMPL'
        ]

        self.assertEqual(
            len(sequence_status_list.statuses),
            len(expected_status_names)
        )

        db_status_names = map(lambda x: x.name, sequence_status_list.statuses)
        db_status_codes = map(lambda x: x.code, sequence_status_list.statuses)
        self.assertEqual(
            sorted(expected_status_names),
            sorted(db_status_names)
        )
        self.assertEqual(
            sorted(expected_status_codes),
            sorted(db_status_codes)
        )
        # check if the created_by and updated_by attributes are correctly set
        # to admin
        from stalker import User
        admin = User.query.filter(User.name == 'admin').first()
        for status in sequence_status_list.statuses:
            self.assertEqual(status.created_by, admin)
            self.assertEqual(status.updated_by, admin)

    def test_task_status_initialization_when_there_is_a_Task_status_list(self):
        """testing if the task statuses are correctly created when there is a
        StatusList for Task is already created
        """
        from stalker import StatusList
        task_status_list = StatusList.query \
            .filter(StatusList.target_entity_type == 'Task') \
            .first()

        self.assertTrue(isinstance(task_status_list, StatusList))

        expected_status_names = [
            'Waiting For Dependency',
            'Ready To Start',
            'Work In Progress',
            'Pending Review',
            'Has Revision',
            'Dependency Has Revision',
            'On Hold',
            'Stopped',
            'Completed'
        ]

        expected_status_codes = [
            'WFD',
            'RTS',
            'WIP',
            'PREV',
            'HREV',
            'DREV',
            'OH',
            'STOP',
            'CMPL'
        ]

        self.assertEqual(
            len(task_status_list.statuses),
            len(expected_status_names)
        )

        db_status_names = map(lambda x: x.name, task_status_list.statuses)
        db_status_codes = map(lambda x: x.code, task_status_list.statuses)
        self.assertEqual(
            sorted(expected_status_names),
            sorted(db_status_names)
        )
        self.assertEqual(
            sorted(expected_status_codes),
            sorted(db_status_codes)
        )

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        from stalker import User
        admin = User.query.filter(User.name == 'admin').first()
        for status in task_status_list.statuses:
            self.assertEqual(status.created_by, admin)
            self.assertEqual(status.updated_by, admin)

    def test_asset_status_initialization_when_there_is_an_Asset_status_list(self):
        """testing if the asset statuses are correctly created when there is a
        StatusList for Sequence is already created
        """
        from stalker import db, StatusList
        asset_status_list = StatusList.query \
            .filter(StatusList.name == 'Asset Statuses') \
            .first()

        self.assertTrue(isinstance(asset_status_list, StatusList))

        expected_status_names = [
            'Waiting For Dependency',
            'Ready To Start',
            'Work In Progress',
            'Pending Review',
            'Has Revision',
            'Dependency Has Revision',
            'On Hold',
            'Stopped',
            'Completed'
        ]

        expected_status_codes = [
            'WFD',
            'RTS',
            'WIP',
            'PREV',
            'HREV',
            'DREV',
            'OH',
            'STOP',
            'CMPL'
        ]

        self.assertEqual(
            len(asset_status_list.statuses),
            len(expected_status_names)
        )

        db_status_names = map(lambda x: x.name, asset_status_list.statuses)
        db_status_codes = map(lambda x: x.code, asset_status_list.statuses)
        self.assertEqual(
            sorted(expected_status_names),
            sorted(db_status_names)
        )
        self.assertEqual(
            sorted(expected_status_codes),
            sorted(db_status_codes)
        )

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        from stalker import User
        admin = User.query.filter(User.name == 'admin').first()
        for status in asset_status_list.statuses:
            self.assertEqual(status.created_by, admin)
            self.assertEqual(status.updated_by, admin)

    def test_shot_status_initialization_when_there_is_a_Shot_status_list(self):
        """testing if the shot statuses are correctly created when there is a
        StatusList for Shot is already created
        """
        from stalker import StatusList
        shot_status_list = StatusList.query \
            .filter(StatusList.name == 'Shot Statuses') \
            .first()

        self.assertTrue(isinstance(shot_status_list, StatusList))

        expected_status_names = [
            'Waiting For Dependency',
            'Ready To Start',
            'Work In Progress',
            'Pending Review',
            'Has Revision',
            'Dependency Has Revision',
            'On Hold',
            'Stopped',
            'Completed'
        ]

        expected_status_codes = [
            'WFD',
            'RTS',
            'WIP',
            'PREV',
            'HREV',
            'DREV',
            'OH',
            'STOP',
            'CMPL'
        ]

        self.assertEqual(
            len(shot_status_list.statuses),
            len(expected_status_names)
        )

        db_status_names = map(lambda x: x.name, shot_status_list.statuses)
        db_status_codes = map(lambda x: x.code, shot_status_list.statuses)
        self.assertEqual(
            sorted(expected_status_names),
            sorted(db_status_names)
        )
        self.assertEqual(
            sorted(expected_status_codes),
            sorted(db_status_codes)
        )

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        from stalker import User
        admin = User.query.filter(User.name == 'admin').first()
        for status in shot_status_list.statuses:
            self.assertEqual(status.created_by, admin)
            self.assertEqual(status.updated_by, admin)

    def test_sequence_status_initialization_when_there_is_a_Sequence_status_list(self):
        """testing if the sequence statuses are correctly created when there is
        a StatusList for Sequence is already created
        """
        from stalker import StatusList
        sequence_status_list = StatusList.query \
            .filter(StatusList.name == 'Sequence Statuses') \
            .first()

        self.assertTrue(isinstance(sequence_status_list, StatusList))

        expected_status_names = [
            'Waiting For Dependency',
            'Ready To Start',
            'Work In Progress',
            'Pending Review',
            'Has Revision',
            'Dependency Has Revision',
            'On Hold',
            'Stopped',
            'Completed'
        ]

        expected_status_codes = [
            'WFD',
            'RTS',
            'WIP',
            'PREV',
            'HREV',
            'DREV',
            'OH',
            'STOP',
            'CMPL'
        ]

        self.assertEqual(
            len(sequence_status_list.statuses),
            len(expected_status_names)
        )

        db_status_names = map(lambda x: x.name, sequence_status_list.statuses)
        db_status_codes = map(lambda x: x.code, sequence_status_list.statuses)
        self.assertEqual(
            sorted(expected_status_names),
            sorted(db_status_names)
        )
        self.assertEqual(
            sorted(expected_status_codes),
            sorted(db_status_codes)
        )

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        from stalker import User
        admin = User.query.filter(User.name == 'admin').first()
        for status in sequence_status_list.statuses:
            self.assertEqual(status.created_by, admin)
            self.assertEqual(status.updated_by, admin)

    def test_review_status_initialization(self):
        """testing if the review statuses are correctly created
        """
        from stalker import StatusList
        review_status_list = StatusList.query \
            .filter(StatusList.name == 'Review Statuses') \
            .first()

        self.assertTrue(isinstance(review_status_list, StatusList))

        expected_status_names = [
            'New',
            'Requested Revision',
            'Approved',
        ]

        expected_status_codes = [
            'NEW',
            'RREV',
            'APP'
        ]

        self.assertEqual(
            len(review_status_list.statuses),
            len(expected_status_names)
        )

        db_status_names = map(lambda x: x.name, review_status_list.statuses)
        db_status_codes = map(lambda x: x.code, review_status_list.statuses)
        self.assertEqual(
            sorted(expected_status_names),
            sorted(db_status_names)
        )
        self.assertEqual(
            sorted(expected_status_codes),
            sorted(db_status_codes)
        )

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        from stalker import User
        admin = User.query.filter(User.name == 'admin').first()
        for status in review_status_list.statuses:
            self.assertEqual(status.created_by, admin)
            self.assertEqual(status.updated_by, admin)

    def test___create_entity_statuses_no_entity_type_supplied(self):
        """testing db.__create_entity_statuses() will raise a ValueError when
        no entity_type is supplied
        """
        from stalker.db import create_entity_statuses
        kwargs = {
            'status_names': ['A', 'B'],
            'status_codes': ['A', 'B']
        }
        with self.assertRaises(ValueError) as cm:
            create_entity_statuses(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'Please supply entity_type'
        )

    def test___create_entity_statuses_no_status_names_supplied(self):
        """testing db.__create_entity_statuses() will raise a ValueError when
        no status_names is supplied
        """
        from stalker.db import create_entity_statuses
        kwargs = {
            'entity_type': 'Hede Hodo',
            'status_codes': ['A', 'B']
        }
        with self.assertRaises(ValueError) as cm:
            create_entity_statuses(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'Please supply status names'
        )

    def test___create_entity_statuses_no_status_codes_supplied(self):
        """testing db.__create_entity_statuses() will raise a ValueError when
        no status_codes is supplied
        """
        from stalker.db import create_entity_statuses
        kwargs = {
            'entity_type': 'Hede Hodo',
            'status_names': ['A', 'B']
        }
        with self.assertRaises(ValueError) as cm:
            create_entity_statuses(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'Please supply status codes'
        )

    def test_initialization_of_alembic_version_table(self):
        """testing if the db.init() will also create a table called
        alembic_version
        """
        from stalker import db
        sql_query = 'select version_num from "alembic_version"'
        version_num = \
            db.DBSession.connection().execute(sql_query).fetchone()[0]
        self.assertEqual('31b1e22b455e', version_num)

    def test_initialization_of_alembic_version_table_multiple_times(self):
        """testing if the db.create_alembic_table() will handle initializing
        the table multiple times
        """
        from stalker import db
        sql_query = 'select version_num from "alembic_version"'
        version_num = \
            db.DBSession.connection().execute(sql_query).fetchone()[0]
        self.assertEqual('31b1e22b455e', version_num)

        db.DBSession.remove()
        db.init()
        db.init()
        db.init()

        version_nums = \
            db.DBSession.connection().execute(sql_query).fetchall()

        # no additional version is created
        self.assertEqual(1, len(version_nums))

    def test_alembic_version_mismatch(self):
        """testing if the db.init() will raise a ValueError if the alembic
        version of the database is not equal to the alembic_version of the
        current Stalker release
        """
        from stalker import db
        db.init()

        # now change the alembic_version
        sql = "update alembic_version set version_num = 'some_random_number'"
        db.DBSession.connection().execute(sql)
        db.DBSession.commit()

        # check if it is updated correctly
        sql = "select version_num from alembic_version"
        result = db.DBSession.connection().execute(sql).fetchone()
        self.assertEqual(
            result[0], 'some_random_number'
        )

        # close the connection
        db.DBSession.connection().close()
        db.DBSession.remove()

        # re-setup
        with self.assertRaises(ValueError) as cm:
            db.setup(self.config)

        self.assertEqual(
            str(cm.exception),
            'Please update the database to version: %s' % db.alembic_version
        )

    def test_initialization_of_repo_environment_variables(self):
        """testing if the db.create_repo_env_vars() will create environment
        variables for each repository in the system
        """
        # create a couple of repositories
        from stalker import db, Repository
        repo1 = Repository(name='Repo1')
        repo2 = Repository(name='Repo2')
        repo3 = Repository(name='Repo3')

        all_repos = [repo1, repo2, repo3]
        db.DBSession.add_all(all_repos)
        db.DBSession.commit()

        # remove any auto created repo vars
        import os
        for repo in all_repos:
            try:
                os.environ.pop('REPO%s' % repo.id)
            except KeyError:
                pass

        # check if all removed
        for repo in all_repos:
            # check if environment vars are created
            self.assertFalse('REPO%s' % repo.id in os.environ)

        # remove db connection
        db.DBSession.remove()

        # reconnect
        db.setup(self.config)

        all_repos = Repository.query.all()

        for repo in all_repos:
            # check if environment vars are created
            self.assertTrue('REPO%s' % repo.id in os.environ)

    def test_db_init_with_studio_instance(self):
        """testing db.init() using existing Studio instance for config values
        """
        # check the defaults
        from stalker import defaults
        self.assertNotEqual(defaults.daily_working_hours, 8)
        self.assertNotEqual(defaults.weekly_working_days, 4)
        self.assertNotEqual(defaults.weekly_working_hours, 32)
        self.assertNotEqual(defaults.yearly_working_days, 180)

        import datetime
        self.assertNotEqual(defaults.timing_resolution,
                            datetime.timedelta(minutes=5))

        from stalker import Studio, WorkingHours

        # check no studio
        studios = Studio.query.all()
        self.assertEqual(studios, [])

        wh = WorkingHours(
            working_hours={
                'mon': [[10 * 60, 18 * 60]],
                'tue': [[10 * 60, 18 * 60]],
                'wed': [[10 * 60, 18 * 60]],
                'thu': [[10 * 60, 18 * 60]],
                'fri': [],
                'sat': [],
                'sun': [],
            }
        )
        wh.daily_working_hours = 8

        test_studio = Studio(
            name='Test Studio',
        )
        test_studio.working_hours = wh
        test_studio.timing_resolution = datetime.timedelta(minutes=5)

        from stalker import db
        db.DBSession.add(test_studio)
        db.DBSession.commit()

        # remove everything
        db.DBSession.connection().close()
        db.DBSession.remove()

        # re-init db
        db.setup(self.config)

        # and expect the defaults to be updated with studio defaults
        self.assertEqual(defaults.daily_working_hours, 8)
        self.assertEqual(defaults.weekly_working_days, 4)
        self.assertEqual(defaults.weekly_working_hours, 32)
        self.assertEqual(defaults.yearly_working_days, 209)
        self.assertEqual(defaults.timing_resolution,
                         datetime.timedelta(minutes=5))


class DatabaseModelsTester(UnitTestBase):
    """tests the database model with a PostgreSQL database

    NOTE TO DEVELOPERS:

    Most of the tests in this TestCase uses parts of the system which are
    tested but probably not tested while running the individual tests.

    Incomplete isolation is against to the logic behind unit testing, every
    test should only cover a unit of the code, and a complete isolation should
    be created. But this can not be done in persistence tests (AFAIK), it needs
    to be done in this way for now. Mocks can not be used because every created
    object goes to the database, so they need to be real objects.
    """

    def test_persistence_of_Asset(self):
        """testing the persistence of Asset
        """
        from stalker import User
        test_user = User(
            name='Test User',
            login='tu',
            email='test@user.com',
            password='secret'
        )

        from stalker import Type
        asset_type = Type(
            name='A new asset type A',
            code='anata',
            target_entity_type='Asset'
        )

        from stalker import Status
        status1 = Status.query.filter_by(code='NEW').first()
        status2 = Status.query.filter_by(code='WIP').first()
        status3 = Status.query.filter_by(code='CMPL').first()

        from stalker import Repository
        test_repository_type = Type(
            name='Test Repository Type A',
            code='trta',
            target_entity_type=Repository,
        )

        test_repository = Repository(
            name='Test Repository A',
            type=test_repository_type
        )

        from stalker import StatusList
        project_status_list = StatusList(
            name='Project Status List A',
            statuses=[status1, status2, status3],
            target_entity_type='Project',
        )

        commercial_type = Type(
            name='Commercial A',
            code='comm',
            target_entity_type='Project'
        )

        from stalker import Project
        test_project = Project(
            name='Test Project For Asset Creation',
            code='TPFAC',
            status_list=project_status_list,
            type=commercial_type,
            repository=test_repository,
        )

        from stalker import db
        db.DBSession.add(test_project)
        db.DBSession.commit()

        from stalker import StatusList
        task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()
        asset_status_list = StatusList.query\
            .filter_by(target_entity_type='Asset').first()

        kwargs = {
            'name': 'Test Asset',
            'code': 'test_asset',
            'description': 'This is a test Asset object',
            'type': asset_type,
            'project': test_project,
            'status_list': asset_status_list,
            'created_by': test_user,
            'responsible': [test_user]
        }

        from stalker import Asset
        test_asset = Asset(**kwargs)
        # logger.debug('test_asset.project : %s' % test_asset.project)

        db.DBSession.add(test_asset)
        db.DBSession.commit()

        # logger.debug('test_asset.project (after commit): %s' %
        #              test_asset.project)

        from stalker import Task
        test_task1 = Task(
            name='test task 1', status=0,
            status_list=task_status_list,
            parent=test_asset,
        )

        test_task2 = Task(
            name='test task 2', status=0,
            status_list=task_status_list,
            parent=test_asset,
        )

        test_task3 = Task(
            name='test task 3', status=0,
            status_list=task_status_list,
            parent=test_asset,
        )

        db.DBSession.add_all([test_task1, test_task2, test_task3])
        db.DBSession.commit()

        code = test_asset.code
        created_by = test_asset.created_by
        date_created = test_asset.date_created
        date_updated = test_asset.date_updated
        duration = test_asset.duration
        description = test_asset.description
        end = test_asset.end
        name = test_asset.name
        nice_name = test_asset.nice_name
        notes = test_asset.notes
        project = test_asset.project
        references = test_asset.references
        status = test_asset.status
        status_list = test_asset.status_list
        start = test_asset.start
        tags = test_asset.tags
        children = test_asset.children
        type_ = test_asset.type
        updated_by = test_asset.updated_by

        del test_asset

        test_asset_db = Asset.query.filter_by(name=kwargs['name']).one()

        assert (isinstance(test_asset_db, Asset))

        #self.assertEqual(test_asset, test_asset_DB)
        self.assertEqual(code, test_asset_db.code)
        self.assertTrue(test_asset_db.created_by is not None)
        self.assertEqual(created_by, test_asset_db.created_by)
        self.assertEqual(date_created, test_asset_db.date_created)
        self.assertEqual(date_updated, test_asset_db.date_updated)
        self.assertEqual(description, test_asset_db.description)
        self.assertEqual(duration, test_asset_db.duration)
        self.assertEqual(end, test_asset_db.end)
        self.assertEqual(name, test_asset_db.name)
        self.assertEqual(nice_name, test_asset_db.nice_name)
        self.assertEqual(notes, test_asset_db.notes)
        self.assertEqual(project, test_asset_db.project)
        self.assertEqual(references, test_asset_db.references)
        self.assertEqual(start, test_asset_db.start)
        self.assertEqual(status, test_asset_db.status)
        self.assertEqual(status_list, test_asset_db.status_list)
        self.assertEqual(tags, test_asset_db.tags)
        self.assertEqual(children, test_asset_db.children)
        self.assertEqual(type_, test_asset_db.type)
        self.assertEqual(updated_by, test_asset_db.updated_by)

        # now test the deletion of the asset class
        db.DBSession.delete(test_asset_db)
        db.DBSession.commit()

        # we should still have the user
        self.assertIsNotNone(
            User.query.filter(User.id == created_by.id).first()
        )

        # we should still have the project
        self.assertIsNotNone(
            Project.query.filter(Project.id == project.id).first()
        )

    def test_persistence_of_Budget_and_BudgetEntry(self):
        """testing the persistence of Budget and BudgetEntry classes
        """
        from stalker import User
        test_user = User(
            name='Test User',
            login='tu',
            email='test@user.com',
            password='secret'
        )

        from stalker import Status
        status1 = Status.query.filter_by(code='NEW').first()
        status2 = Status.query.filter_by(code='WIP').first()
        status3 = Status.query.filter_by(code='CMPL').first()

        from stalker import Type
        test_repository_type = Type(
            name='Test Repository Type A',
            code='trta',
            target_entity_type='Repository',
        )

        from stalker import Repository
        test_repository = Repository(
            name='Test Repository A',
            type=test_repository_type
        )

        from stalker import StatusList
        project_status_list = StatusList(
            name='Project Status List A',
            statuses=[status1, status2, status3],
            target_entity_type='Project',
        )

        budget_status_list = StatusList(
            name='Budget Statuses',
            statuses=[status1, status2, status3],
            target_entity_type='Budget'
        )

        commercial_type = Type(
            name='Commercial A',
            code='comm',
            target_entity_type='Project'
        )

        from stalker import Project
        test_project = Project(
            name='Test Project For Budget Creation',
            code='TPFBC',
            status_list=project_status_list,
            type=commercial_type,
            repository=test_repository,
        )

        from stalker import db
        db.DBSession.add(test_project)
        db.DBSession.commit()

        kwargs = {
            'name': 'Test Budget',
            'project': test_project,
            'created_by': test_user,
            'status_list': budget_status_list,
            'status': status1
        }

        from stalker import Budget
        test_budget = Budget(**kwargs)

        db.DBSession.add(test_budget)
        db.DBSession.commit()

        from stalker import Good
        good = Good(name='Some Good', cost=9, msrp=10, unit='$/hour')
        db.DBSession.add(good)
        db.DBSession.commit()

        # create some entries
        from stalker import BudgetEntry
        entry1 = BudgetEntry(budget=test_budget, good=good, amount=5.0)
        entry2 = BudgetEntry(budget=test_budget, good=good, amount=1.0)

        db.DBSession.add_all([entry1, entry2])
        db.DBSession.commit()

        created_by = test_budget.created_by
        date_created = test_budget.date_created
        date_updated = test_budget.date_updated
        name = test_budget.name
        nice_name = test_budget.nice_name
        project = test_budget.project
        tags = test_budget.tags
        updated_by = test_budget.updated_by
        notes = test_budget.notes
        entries = test_budget.entries
        status = test_budget.status

        del test_budget

        test_budget_db = Budget.query.filter_by(name=kwargs['name']).one()

        assert (isinstance(test_budget_db, Budget))

        self.assertTrue(test_budget_db.created_by is not None)
        self.assertEqual(created_by, test_budget_db.created_by)
        self.assertEqual(date_created, test_budget_db.date_created)
        self.assertEqual(date_updated, test_budget_db.date_updated)
        self.assertEqual(name, test_budget_db.name)
        self.assertEqual(nice_name, test_budget_db.nice_name)
        self.assertEqual(notes, test_budget_db.notes)
        self.assertEqual(project, test_budget_db.project)
        self.assertEqual(tags, test_budget_db.tags)
        self.assertEqual(updated_by, test_budget_db.updated_by)
        self.assertEqual(entries, test_budget_db.entries)
        self.assertEqual(status, status1)

        # and we should have our entries intact
        self.assertTrue(
            BudgetEntry.query.all() != []
        )

        # now test the deletion of the asset class
        db.DBSession.delete(test_budget_db)
        db.DBSession.commit()

        # we should still have the user
        self.assertTrue(
            User.query.filter(User.id == created_by.id).first() is not None
        )

        # we should still have the project
        self.assertTrue(
            Project.query.filter(Project.id == project.id).first() is not None
        )

        # and we should have our page deleted
        self.assertTrue(
            Budget.query.filter(Budget.name == kwargs['name']).first() is None
        )

        # and we should have our entries deleted
        self.assertTrue(
            BudgetEntry.query.all() == []
        )

        # we still should have the good
        good_db = Good.query.filter(Good.name == 'Some Good').first()
        self.assertTrue(good_db is not None)

    def test_persistence_of_Invoice(self):
        """testing the persistence of Invoice instances
        """
        from stalker import User
        test_user = User(
            name='Test User',
            login='tu',
            email='test@user.com',
            password='secret'
        )

        from stalker import Status
        status1 = Status.query.filter_by(code='NEW').first()
        status2 = Status.query.filter_by(code='WIP').first()
        status3 = Status.query.filter_by(code='CMPL').first()

        from stalker import Type
        test_repository_type = Type(
            name='Test Repository Type A',
            code='trta',
            target_entity_type='Repository',
        )

        from stalker import Repository
        test_repository = Repository(
            name='Test Repository A',
            type=test_repository_type
        )

        from stalker import StatusList
        project_status_list = StatusList(
            name='Project Status List A',
            statuses=[status1, status2, status3],
            target_entity_type='Project',
        )

        budget_status_list = StatusList(
            name='Budget Statuses',
            statuses=[status1, status2, status3],
            target_entity_type='Budget'
        )

        commercial_type = Type(
            name='Commercial A',
            code='comm',
            target_entity_type='Project'
        )

        from stalker import db, Client, Project
        test_client = Client(name='Test Client')
        db.DBSession.add(test_client)

        test_project = Project(
            name='Test Project For Budget Creation',
            code='TPFBC',
            status_list=project_status_list,
            type=commercial_type,
            repository=test_repository,
            clients=[test_client]
        )

        db.DBSession.add(test_project)
        db.DBSession.commit()

        from stalker import Budget
        test_budget = Budget(
            name='Test Budget',
            project=test_project,
            created_by=test_user,
            status_list=budget_status_list,
            status=status1
        )

        db.DBSession.add(test_budget)
        db.DBSession.commit()

        from stalker import Good
        good = Good(name='Some Good', cost=9, msrp=10, unit='$/hour')
        db.DBSession.add(good)
        db.DBSession.commit()

        # create some entries
        from stalker import BudgetEntry
        entry1 = BudgetEntry(budget=test_budget, good=good, amount=5.0)
        entry2 = BudgetEntry(budget=test_budget, good=good, amount=1.0)

        db.DBSession.add_all([entry1, entry2])
        db.DBSession.commit()

        # create an invoice
        from stalker import Invoice
        test_invoice = Invoice(
            created_by=test_user,
            budget=test_budget,
            client=test_client,
            amount=1232.4,
            unit='TRY'
        )
        db.DBSession.add(test_invoice)

        created_by = test_invoice.created_by
        date_created = test_invoice.date_created
        date_updated = test_invoice.date_updated
        name = test_invoice.name
        nice_name = test_invoice.nice_name
        tags = test_invoice.tags
        notes = test_invoice.notes
        updated_by = test_invoice.updated_by

        budget = test_budget
        client = test_client
        amount = 1232.4
        unit = 'TRY'

        del test_invoice

        test_invoice_db = Invoice.query\
            .filter(Invoice.name == name)\
            .first()

        assert(isinstance(test_invoice_db, Invoice))

        self.assertEqual(test_user, test_invoice_db.created_by)
        self.assertEqual(created_by, test_invoice_db.created_by)
        self.assertEqual(date_created, test_invoice_db.date_created)
        self.assertEqual(date_updated, test_invoice_db.date_updated)
        self.assertEqual(name, test_invoice_db.name)
        self.assertEqual(nice_name, test_invoice_db.nice_name)
        self.assertEqual(notes, test_invoice_db.notes)
        self.assertEqual(tags, test_invoice_db.tags)
        self.assertEqual(updated_by, test_invoice_db.updated_by)

        self.assertEqual(budget, test_invoice_db.budget)
        self.assertEqual(client, test_invoice_db.client)
        self.assertEqual(amount, test_invoice_db.amount)
        self.assertEqual(unit, test_invoice_db.unit)

        # now test the deletion of the invoice instance
        db.DBSession.delete(test_invoice_db)
        db.DBSession.commit()

        # we should still have the budget
        self.assertEqual(
            Budget.query.filter(Budget.id == budget.id).first(),
            budget
        )

        # we should still have the client
        self.assertEqual(
            Client.query.filter(Client.id == client.id).first(),
            client
        )

        # and we should have the invoice deleted
        self.assertIsNone(
            Invoice.query.filter(Invoice.name == test_invoice_db.name).first()
        )

    def test_persistence_of_Payment(self):
        """testing the persistence of Payment instances
        """
        from stalker import User
        test_user = User(
            name='Test User',
            login='tu',
            email='test@user.com',
            password='secret'
        )

        from stalker import Status
        status1 = Status.query.filter_by(code='NEW').first()
        status2 = Status.query.filter_by(code='WIP').first()
        status3 = Status.query.filter_by(code='CMPL').first()

        from stalker import Type
        test_repository_type = Type(
            name='Test Repository Type A',
            code='trta',
            target_entity_type='Repository',
        )

        from stalker import Repository
        test_repository = Repository(
            name='Test Repository A',
            type=test_repository_type
        )

        from stalker import StatusList
        project_status_list = StatusList(
            name='Project Status List A',
            statuses=[status1, status2, status3],
            target_entity_type='Project',
        )

        budget_status_list = StatusList(
            name='Budget Statuses',
            statuses=[status1, status2, status3],
            target_entity_type='Budget'
        )

        commercial_type = Type(
            name='Commercial A',
            code='comm',
            target_entity_type='Project'
        )

        from stalker import db, Client
        test_client = Client(name='Test Client')
        db.DBSession.add(test_client)

        from stalker import Project
        test_project = Project(
            name='Test Project For Budget Creation',
            code='TPFBC',
            status_list=project_status_list,
            type=commercial_type,
            repository=test_repository,
            clients=[test_client]
        )

        db.DBSession.add(test_project)
        db.DBSession.commit()

        from stalker import Budget
        test_budget = Budget(
            name='Test Budget',
            project=test_project,
            created_by=test_user,
            status_list=budget_status_list,
            status=status1
        )

        db.DBSession.add(test_budget)
        db.DBSession.commit()

        from stalker import Good
        good = Good(name='Some Good', cost=9, msrp=10, unit='$/hour')
        db.DBSession.add(good)
        db.DBSession.commit()

        # create some entries
        from stalker import BudgetEntry
        entry1 = BudgetEntry(budget=test_budget, good=good, amount=5.0)
        entry2 = BudgetEntry(budget=test_budget, good=good, amount=1.0)

        db.DBSession.add_all([entry1, entry2])
        db.DBSession.commit()

        # create an invoice
        from stalker import Invoice
        test_invoice = Invoice(
            created_by=test_user,
            budget=test_budget,
            client=test_client,
            amount=1232.4,
            unit='TRY'
        )
        db.DBSession.add(test_invoice)

        from stalker import Payment
        test_payment = Payment(
            created_by=test_user,
            invoice=test_invoice,
            amount=123.4,
            unit='TRY'
        )

        created_by = test_payment.created_by
        date_created = test_payment.date_created
        date_updated = test_payment.date_updated
        name = test_payment.name
        nice_name = test_payment.nice_name
        tags = test_payment.tags
        notes = test_payment.notes
        updated_by = test_payment.updated_by

        invoice = test_invoice
        amount = 123.4
        unit = 'TRY'

        del test_payment

        test_payment_db = Payment.query\
            .filter(Payment.name == name)\
            .first()

        assert(isinstance(test_payment_db, Payment))

        self.assertEqual(test_user, test_payment_db.created_by)
        self.assertEqual(created_by, test_payment_db.created_by)
        self.assertEqual(date_created, test_payment_db.date_created)
        self.assertEqual(date_updated, test_payment_db.date_updated)
        self.assertEqual(name, test_payment_db.name)
        self.assertEqual(nice_name, test_payment_db.nice_name)
        self.assertEqual(notes, test_payment_db.notes)
        self.assertEqual(tags, test_payment_db.tags)
        self.assertEqual(updated_by, test_payment_db.updated_by)

        self.assertEqual(invoice, test_payment_db.invoice)
        self.assertEqual(amount, test_payment_db.amount)
        self.assertEqual(unit, test_payment_db.unit)

        # now test the deletion of the invoice instance
        db.DBSession.delete(test_payment_db)
        db.DBSession.commit()

        # we should still have the budget
        self.assertEqual(
            Budget.query.filter(Budget.id == test_budget.id).first(),
            test_budget
        )

        # we should still have the Invoice
        self.assertEqual(
            Invoice.query.filter(Invoice.id == test_invoice.id).first(),
            test_invoice
        )

        # and we should have the payment deleted
        self.assertIsNone(
            Payment.query.filter(Payment.name == test_payment_db.name).first()
        )

    def test_persistence_of_Page(self):
        """testing the persistence of Page
        """
        from stalker import User
        test_user = User(
            name='Test User',
            login='tu',
            email='test@user.com',
            password='secret'
        )

        from stalker import Status
        status1 = Status.query.filter_by(code='NEW').first()
        status2 = Status.query.filter_by(code='WIP').first()
        status3 = Status.query.filter_by(code='CMPL').first()

        from stalker import Type
        test_repository_type = Type(
            name='Test Repository Type A',
            code='trta',
            target_entity_type='Repository',
        )

        from stalker import Repository
        test_repository = Repository(
            name='Test Repository A',
            type=test_repository_type
        )

        from stalker import StatusList
        project_status_list = StatusList(
            name='Project Status List A',
            statuses=[status1, status2, status3],
            target_entity_type='Project',
        )

        commercial_type = Type(
            name='Commercial A',
            code='comm',
            target_entity_type='Project'
        )

        from stalker import Project
        test_project = Project(
            name='Test Project For Asset Creation',
            code='TPFAC',
            status_list=project_status_list,
            type=commercial_type,
            repository=test_repository,
        )

        from stalker import db
        db.DBSession.add(test_project)
        db.DBSession.commit()

        kwargs = {
            'title': 'Test Wiki Page',
            'content': 'This is a test wiki page',
            'project': test_project,
            'created_by': test_user
        }

        from stalker import Page
        test_page = Page(**kwargs)

        db.DBSession.add(test_page)
        db.DBSession.commit()

        created_by = test_page.created_by
        date_created = test_page.date_created
        date_updated = test_page.date_updated
        name = test_page.name
        nice_name = test_page.nice_name
        project = test_page.project
        tags = test_page.tags
        updated_by = test_page.updated_by
        title = test_page.title
        content = test_page.content
        notes = test_page.notes

        del test_page

        test_page_db = Page.query.filter_by(title=kwargs['title']).one()

        assert (isinstance(test_page_db, Page))

        #self.assertEqual(test_asset, test_asset_DB)
        self.assertTrue(test_page_db.created_by is not None)
        self.assertEqual(created_by, test_page_db.created_by)
        self.assertEqual(date_created, test_page_db.date_created)
        self.assertEqual(date_updated, test_page_db.date_updated)
        self.assertEqual(content, test_page_db.content)
        self.assertEqual(name, test_page_db.name)
        self.assertEqual(nice_name, test_page_db.nice_name)
        self.assertEqual(notes, test_page_db.notes)
        self.assertEqual(project, test_page_db.project)
        self.assertEqual(tags, test_page_db.tags)
        self.assertEqual(title, test_page_db.title)
        self.assertEqual(updated_by, test_page_db.updated_by)

        # now test the deletion of the asset class
        db.DBSession.delete(test_page_db)
        db.DBSession.commit()

        # we should still have the user
        self.assertTrue(
            User.query.filter(User.id == created_by.id).first() is not None
        )

        # we should still have the project
        self.assertTrue(
            Project.query.filter(Project.id == project.id).first() is not None
        )

        # and we should have our page deleted
        self.assertTrue(
            Page.query.filter(Page.title == kwargs['title']).first() is None
        )

    def test_persistence_of_TimeLog(self):
        """testing the persistence of TimeLog
        """
        logger.setLevel(log.logging_level)

        description = 'this is a time log'
        import datetime
        import pytz
        start = datetime.datetime(2013, 1, 10, tzinfo=pytz.utc)
        end = datetime.datetime(2013, 1, 13, tzinfo=pytz.utc)

        from stalker import User
        user1 = User(
            name='User1',
            login='user1',
            email='user1@users.com',
            password='pass'
        )

        user2 = User(
            name='User2',
            login='user2',
            email='user2@users.com',
            password='pass'
        )

        from stalker import Status
        stat1 = Status(
            name='Work In Progress',
            code='WIP'
        )

        stat2 = Status(
            name='Completed',
            code='CMPL'
        )

        from stalker import Repository
        repo = Repository(
            name='Commercials Repository',
            linux_path='/mnt/shows',
            windows_path='S:/',
            osx_path='/mnt/shows'
        )

        from stalker import StatusList
        proj_status_list = StatusList(
            name='Project Statuses',
            statuses=[stat1, stat2],
            target_entity_type='Project'
        )

        task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()

        from stalker import Type
        projtype = Type(
            name='Commercial Project',
            code='comm',
            target_entity_type='Project'
        )

        from stalker import Project
        proj1 = Project(
            name='Test Project',
            code='tp',
            type=projtype,
            status_list=proj_status_list,
            repository=repo
        )

        from stalker import Task
        test_task = Task(
            name='Test Task',
            start=start,
            end=end,
            resources=[user1, user2],
            project=proj1,
            status_list=task_status_list,
            responsible=[user1]
        )

        from stalker import TimeLog
        test_time_log = TimeLog(
            task=test_task,
            resource=user1,
            start=datetime.datetime(2013, 1, 10, tzinfo=pytz.utc),
            end=datetime.datetime(2013, 1, 13, tzinfo=pytz.utc),
            description=description
        )

        from stalker import db
        db.DBSession.add(test_time_log)
        db.DBSession.commit()
        tlog_id = test_time_log.id

        del test_time_log

        # now retrieve it back
        test_time_log_db = TimeLog.query.filter_by(id=tlog_id).first()

        self.assertEqual(description, test_time_log_db.description)
        self.assertEqual(start, test_time_log_db.start)
        self.assertEqual(end, test_time_log_db.end)
        self.assertEqual(user1, test_time_log_db.resource)
        self.assertEqual(test_task, test_time_log_db.task)

    def test_persistence_of_TimeLog_raw_sql(self):
        """testing the persistence of TimeLog
        """
        import datetime
        import pytz
        start = datetime.datetime(2013, 1, 10, tzinfo=pytz.utc)
        end = datetime.datetime(2013, 1, 13, tzinfo=pytz.utc)

        from stalker import User
        user1 = User(
            name='User1',
            login='user1',
            email='user1@users.com',
            password='pass'
        )

        user2 = User(
            name='User2',
            login='user2',
            email='user2@users.com',
            password='pass'
        )

        from stalker import Status
        stat1 = Status(
            name='Work In Progress',
            code='WIP'
        )

        stat2 = Status(
            name='Completed',
            code='CMPL'
        )

        from stalker import Repository
        repo = Repository(
            name='Commercials Repository',
            linux_path='/mnt/shows',
            windows_path='S:/',
            osx_path='/mnt/shows'
        )

        from stalker import StatusList
        proj_status_list = StatusList(
            name='Project Statuses',
            statuses=[stat1, stat2],
            target_entity_type='Project'
        )

        task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()

        from stalker import Type
        projtype = Type(
            name='Commercial Project',
            code='comm',
            target_entity_type='Project'
        )

        from stalker import Project
        proj1 = Project(
            name='Test Project',
            code='tp',
            type=projtype,
            status_list=proj_status_list,
            repository=repo
        )

        from stalker import Task
        test_task = Task(
            name='Test Task',
            start=start,
            end=end,
            resources=[user1, user2],
            project=proj1,
            status_list=task_status_list,
            responsible=[user1]
        )

        from stalker import db
        db.DBSession.add(test_task)
        db.DBSession.commit()

        # now insert a new TimeLog in to the Timelogs table which has the same
        # value for start and end arguments, which should automatically raise
        # an IntegrityError by the database itself.

        # try insert start = start
        from stalker import TimeLog
        new_tl1 = TimeLog(
            task=test_task,
            resource=user1,
            start=start,
            end=end
        )
        db.DBSession.add(new_tl1)
        db.DBSession.commit()

        # create a new TimeLog
        new_tl2 = TimeLog(
            task=test_task,
            resource=user1,
            start=end,
            end=end + datetime.timedelta(hours=3)
        )
        db.DBSession.add(new_tl2)
        db.DBSession.commit()

        # update it to have overlapping timing values with new_tl1
        from sqlalchemy.exc import IntegrityError
        new_tl2.start = start + datetime.timedelta(hours=2)

        with self.assertRaises(IntegrityError) as cm:
            db.DBSession.commit()

    def test_persistence_of_Client(self):
        """testing the persistence of Client
        """
        logger.setLevel(log.logging_level)

        name = "TestClient"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        import datetime
        import pytz
        date_created = datetime.datetime.now(pytz.utc)
        date_updated = datetime.datetime.now(pytz.utc)

        from stalker import Client
        test_client = Client(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated
        )
        from stalker import db
        db.DBSession.add(test_client)
        db.DBSession.commit()

        # create three users

        # user1
        from stalker import User
        user1 = User(
            name="User1 Test Persistence Department",
            login='u1tpd',
            initials='u1tpd',
            description="this is for testing purposes",
            created_by=None,
            updated_by=None,
            login_name="user1_tp_client",
            first_name="user1_first_name",
            last_name="user1_last_name",
            email="user1@client.com",
            companies=[test_client],
            password="password",
        )

        # user2
        user2 = User(
            name="User2 Test Persistence Client",
            login='u2tpd',
            initials='u2tpd',
            description="this is for testing purposes",
            created_by=None,
            updated_by=None,
            login_name="user2_tp_client",
            first_name="user2_first_name",
            last_name="user2_last_name",
            email="user2@client.com",
            companies=[test_client],
            password="password",
        )

        # user3
        user3 = User(
            name="User3 Test Persistence Client",
            login='u3tpd',
            initials='u3tpd',
            description="this is for testing purposes",
            created_by=None,
            updated_by=None,
            login_name="user3_tp_client",
            first_name="user3_first_name",
            last_name="user3_last_name",
            email="user3@client.com",
            companies=[test_client],
            password="password",
        )

        db.DBSession.add_all([user1, user2, user3, test_client])
        db.DBSession.commit()

        self.assertTrue(test_client in db.DBSession)

        created_by = test_client.created_by
        date_created = test_client.date_created
        date_updated = test_client.date_updated
        description = test_client.description
        users = [u for u in test_client.users]
        name = test_client.name
        nice_name = test_client.nice_name
        notes = test_client.notes
        tags = test_client.tags
        updated_by = test_client.updated_by

        del test_client

        # lets check the data
        # first get the client from the db
        client_db = Client.query.filter_by(name=name).first()

        assert (isinstance(client_db, Client))

        self.assertEqual(created_by, client_db.created_by)
        self.assertEqual(date_created, client_db.date_created)
        self.assertEqual(date_updated, client_db.date_updated)
        self.assertEqual(description, client_db.description)
        self.assertEqual(users, client_db.users)
        self.assertEqual(name, client_db.name)
        self.assertEqual(nice_name, client_db.nice_name)
        self.assertEqual(notes, client_db.notes)
        self.assertEqual(tags, client_db.tags)
        self.assertEqual(updated_by, client_db.updated_by)

        # delete the client and expect the users are still there
        db.DBSession.delete(client_db)
        db.DBSession.commit()

        user1_db = User.query.filter_by(login='u1tpd').first()
        user2_db = User.query.filter_by(login='u2tpd').first()
        user3_db = User.query.filter_by(login='u3tpd').first()

        self.assertTrue(user1_db is not None)
        self.assertTrue(user2_db is not None)
        self.assertTrue(user3_db is not None)

    def test_persistence_of_Daily(self):
        """testing the persistence of a Daily instance
        """
        from stalker import Status
        status_new = Status.query.filter_by(code='NEW').first()
        status_wip = Status.query.filter_by(code='WIP').first()
        status_cmpl = Status.query.filter_by(code='CMPL').first()

        from stalker import StatusList
        test_project_status_list = StatusList(
            name='Project Statuses',
            target_entity_type='Project',
            statuses=[status_new, status_wip, status_cmpl]
        )

        from stalker import User
        test_user1 = User(
            name='User1',
            login='user1',
            email='user1@user1.com',
            password='12345'
        )

        from stalker import Repository, Project
        test_repo = Repository(name='Test Repository')
        test_project = Project(
            name='Test Project',
            code='TP',
            repository=test_repo,
            status_list=test_project_status_list
        )

        from stalker import Task
        test_task1 = Task(
            name='Test Task 1',
            project=test_project,
            responsible=[test_user1]
        )
        test_task2 = Task(
            name='Test Task 2',
            project=test_project,
            responsible=[test_user1]
        )
        test_task3 = Task(
            name='Test Task 3',
            project=test_project,
            responsible=[test_user1]
        )

        from stalker import db, Version
        test_version1 = Version(task=test_task1)
        db.DBSession.add(test_version1)
        db.DBSession.commit()

        test_version2 = Version(task=test_task1)
        db.DBSession.add(test_version2)
        db.DBSession.commit()

        test_version3 = Version(task=test_task1)
        db.DBSession.add(test_version3)
        db.DBSession.commit()

        test_version4 = Version(task=test_task2)
        db.DBSession.add(test_version4)
        db.DBSession.commit()

        from stalker import Link
        test_link1 = Link(original_filename='test_render1.jpg')
        test_link2 = Link(original_filename='test_render2.jpg')
        test_link3 = Link(original_filename='test_render3.jpg')
        test_link4 = Link(original_filename='test_render4.jpg')

        test_version1.outputs = [
            test_link1,
            test_link2,
            test_link3
        ]
        test_version4.outputs = [
            test_link4
        ]

        db.DBSession.add_all([
            test_task1, test_task2, test_task3,
            test_version1, test_version2, test_version3,
            test_version4,
            test_link1, test_link2, test_link3, test_link4
        ])
        db.DBSession.commit()

        # arguments
        name = 'Test Daily'
        links = [test_link1, test_link2, test_link3]

        from stalker import Daily
        daily = Daily(name=name, project=test_project)
        daily.links = links

        db.DBSession.add(daily)
        db.DBSession.commit()

        daily_id = daily.id

        del daily

        daily_db = Daily.query.get(daily_id)

        self.assertEqual(daily_db.name, name)
        self.assertEqual(daily_db.links, links)
        self.assertEqual(daily_db.project, test_project)

        link1_id = test_link1.id
        link2_id = test_link2.id
        link3_id = test_link3.id
        link4_id = test_link4.id

        # delete tests
        db.DBSession.delete(daily_db)
        db.DBSession.commit()

        # test if links are still there
        from stalker import Link
        test_link1_db = Link.query.get(link1_id)
        test_link2_db = Link.query.get(link2_id)
        test_link3_db = Link.query.get(link3_id)
        test_link4_db = Link.query.get(link4_id)

        self.assertTrue(test_link1_db is not None)
        self.assertTrue(isinstance(test_link1_db, Link))

        self.assertTrue(test_link2_db is not None)
        self.assertTrue(isinstance(test_link2_db, Link))

        self.assertTrue(test_link3_db is not None)
        self.assertTrue(isinstance(test_link3_db, Link))

        self.assertTrue(test_link4_db is not None)
        self.assertTrue(isinstance(test_link4_db, Link))

        from stalker import DailyLink
        self.assertEqual(
            DailyLink.query.all(),
            []
        )

        self.assertEqual(
            Link.query.count(),
            8  # including versions
        )

    def test_persistence_of_Department(self):
        """testing the persistence of Department
        """
        logger.setLevel(log.logging_level)

        name = "TestDepartment_test_persistence_Department"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        import datetime
        import pytz
        date_created = datetime.datetime.now(pytz.utc)
        date_updated = datetime.datetime.now(pytz.utc)

        from stalker import db, Department
        test_dep = Department(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated
        )
        db.DBSession.add(test_dep)
        db.DBSession.commit()

        # create three users, one for lead and two for users

        # user1
        from stalker import User
        user1 = User(
            name="User1 Test Persistence Department",
            login='u1tpd',
            initials='u1tpd',
            description="this is for testing purposes",
            created_by=None,
            updated_by=None,
            login_name="user1_tp_department",
            first_name="user1_first_name",
            last_name="user1_last_name",
            email="user1@department.com",
            departments=[test_dep],
            password="password",
        )

        # user2
        user2 = User(
            name="User2 Test Persistence Department",
            login='u2tpd',
            initials='u2tpd',
            description="this is for testing purposes",
            created_by=None,
            updated_by=None,
            login_name="user2_tp_department",
            first_name="user2_first_name",
            last_name="user2_last_name",
            email="user2@department.com",
            departments=[test_dep],
            password="password",
        )

        # user3
        # create three users, one for lead and two for users
        user3 = User(
            name="User3 Test Persistence Department",
            login='u3tpd',
            initials='u3tpd',
            description="this is for testing purposes",
            created_by=None,
            updated_by=None,
            login_name="user3_tp_department",
            first_name="user3_first_name",
            last_name="user3_last_name",
            email="user3@department.com",
            departments=[test_dep],
            password="password",
        )

        # add as the users
        test_dep.users = [user1, user2, user3]

        db.DBSession.add(test_dep)
        db.DBSession.commit()

        self.assertTrue(test_dep in db.DBSession)

        created_by = test_dep.created_by
        date_created = test_dep.date_created
        date_updated = test_dep.date_updated
        description = test_dep.description
        users = [u for u in test_dep.users]
        name = test_dep.name
        nice_name = test_dep.nice_name
        notes = test_dep.notes
        tags = test_dep.tags
        updated_by = test_dep.updated_by

        del test_dep

        # lets check the data
        # first get the department from the db
        test_dep_db = Department.query.filter_by(name=name).first()

        assert (isinstance(test_dep_db, Department))

        self.assertEqual(created_by, test_dep_db.created_by)
        self.assertEqual(date_created, test_dep_db.date_created)
        self.assertEqual(date_updated, test_dep_db.date_updated)
        self.assertEqual(description, test_dep_db.description)
        self.assertEqual(users, test_dep_db.users)
        self.assertEqual(name, test_dep_db.name)
        self.assertEqual(nice_name, test_dep_db.nice_name)
        self.assertEqual(notes, test_dep_db.notes)
        self.assertEqual(tags, test_dep_db.tags)
        self.assertEqual(updated_by, test_dep_db.updated_by)

    def test_persistence_of_Entity(self):
        """testing the persistence of Entity
        """
        # create an Entity with a couple of tags
        # the Tag1
        name = "Tag1_test_creating_an_Entity"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        import datetime
        import pytz
        date_created = date_updated = datetime.datetime.now(pytz.utc)

        from stalker import Tag
        tag1 = Tag(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated
        )

        # the Tag2
        name = "Tag2_test_creating_an_Entity"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        import datetime
        import pytz
        date_created = date_updated = datetime.datetime.now(pytz.utc)

        tag2 = Tag(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated
        )

        # the note
        from stalker import Note
        note1 = Note(content="content for note1")
        note2 = Note(content="content for note2")

        # the entity
        name = "TestEntity"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        date_created = date_updated = datetime.datetime.now(pytz.utc)

        from stalker import Entity
        test_entity = Entity(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated,
            tags=[tag1, tag2],
            notes=[note1, note2],
        )

        # assign the note1 also to another entity
        test_entity2 = Entity(
            name='Test Entity 2',
            notes=[note1]
        )

        # persist it to the database
        from stalker import db
        db.DBSession.add_all([test_entity, test_entity2])
        db.DBSession.commit()

        # store attributes
        created_by = test_entity.created_by
        date_created = test_entity.date_created
        date_updated = test_entity.date_updated
        description = test_entity.description
        name = test_entity.name
        nice_name = test_entity.nice_name
        notes = test_entity.notes
        tags = test_entity.tags
        updated_by = test_entity.updated_by

        # delete the previous test_entity
        del test_entity

        # now try to retrieve it
        from stalker import Entity
        test_entity_db = Entity.query.filter_by(name=name).first()

        assert (isinstance(test_entity_db, Entity))

        self.assertEqual(created_by, test_entity_db.created_by)
        self.assertEqual(date_created, test_entity_db.date_created)
        self.assertEqual(date_updated, test_entity_db.date_updated)
        self.assertEqual(description, test_entity_db.description)
        self.assertEqual(name, test_entity_db.name)
        self.assertEqual(nice_name, test_entity_db.nice_name)
        self.assertEqual(
            sorted(notes, key=lambda x: x.name),
            sorted([note1, note2], key=lambda x: x.name)
        )
        self.assertEqual(notes, test_entity_db.notes)
        self.assertEqual(tags, test_entity_db.tags)
        self.assertEqual(updated_by, test_entity_db.updated_by)

        # delete tests

        # Deleting an Entity should also delete the associated notes
        from stalker import db
        db.DBSession.delete(test_entity_db)
        db.DBSession.commit()

        from stalker import Entity, Note
        test_entity2_db = Entity.query.filter_by(name='Test Entity 2').first()
        self.assertTrue(isinstance(test_entity2_db, Entity))

        self.assertEqual(
            sorted([note1, note2], key=lambda x: x.name),
            sorted(Note.query.all(), key=lambda x: x.name)
        )
        self.assertEqual(
            sorted([note1], key=lambda x: x.name),
            sorted(test_entity2_db.notes, key=lambda x: x.name)
        )

    def test_persistence_of_EntityGroup(self):
        """testing the persistence of EntityGroup
        """
        # create a couple of task
        from stalker import Status
        status1 = Status(name="stat1", code="STS1")
        status2 = Status(name="stat2", code="STS2")
        status3 = Status(name="stat3", code="STS3")
        status4 = Status(name="stat4", code="STS4")
        status5 = Status(name="stat5", code="STS5")

        from stalker import User
        user1 = User(
            name="User1",
            login="user1",
            email="user1@user.com",
            password="1234",
        )

        user2 = User(
            name="User2",
            login="user2",
            email="user2@user.com",
            password="1234",
        )

        user3 = User(
            name="User3",
            login="user3",
            email="user3@user.com",
            password="1234",
        )

        from stalker import StatusList
        project_status_list = StatusList(
            name="Project Status List",
            statuses=[status1, status2, status3, status4, status5],
            target_entity_type='Project',
        )

        from stalker import Repository
        repo = Repository(
            name='Test Repo',
            linux_path='/mnt/M/JOBs',
            windows_path='M:/JOBs',
            osx_path='/Users/Shared/Servers/M',
        )

        from stalker import Project
        project1 = Project(
            name='Tests Project',
            code='tp',
            status_list=project_status_list,
            repository=repo,
        )

        from stalker import Type
        char_asset_type = Type(
            name='Character Asset',
            code='char',
            target_entity_type='Asset'
        )

        from stalker import Asset
        asset1 = Asset(
            name='Char1',
            code='char1',
            type=char_asset_type,
            project=project1,
            responsible=[user1]
        )

        from stalker import Task
        task1 = Task(
            name="Test Task",
            watchers=[user3],
            parent=asset1,
        )

        child_task1 = Task(
            name='Child Task 1',
            resources=[user1, user2],
            parent=task1,
        )

        child_task2 = Task(
            name='Child Task 2',
            resources=[user1, user2],
            parent=task1,
        )

        task2 = Task(
            name='Another Task',
            project=project1,
            resources=[user1],
            responsible=[user2]
        )

        from stalker import EntityGroup
        entity_group1 = EntityGroup(name='My Tasks')
        entity_group1.entities = [
            task1, child_task2, task2
        ]

        from stalker import db
        db.DBSession.add_all([
            task1, child_task1, child_task2, task2, user1, user2, entity_group1
        ])
        db.DBSession.commit()

        created_by = entity_group1.created_by
        date_created = entity_group1.date_created
        date_updated = entity_group1.date_updated
        name = entity_group1.name
        entities = entity_group1.entities
        tags = entity_group1.tags
        type_ = entity_group1.type
        updated_by = entity_group1.updated_by

        del entity_group1

        # now query it back
        entity_group1_db = EntityGroup.query.filter_by(name=name).first()

        assert (isinstance(entity_group1_db, EntityGroup))

        self.assertEqual(created_by, entity_group1_db.created_by)
        self.assertEqual(date_created, entity_group1_db.date_created)
        self.assertEqual(date_updated, entity_group1_db.date_updated)
        self.assertEqual(name, entity_group1_db.name)
        self.assertEqual(tags, entity_group1_db.tags)
        self.assertEqual(
            sorted(entities, key=lambda x: x.name),
            sorted(entity_group1_db.entities, key=lambda x: x.name)
        )
        self.assertEqual(
            entities,
            [task1, child_task2, task2]
        )
        self.assertEqual(type_, entity_group1_db.type)
        self.assertEqual(updated_by, entity_group1_db.updated_by)

        # delete tests
        # deleting entity group will not delete the contained entities
        db.DBSession.delete(entity_group1_db)
        db.DBSession.commit()

        self.assertEqual(
            sorted([task1, asset1, child_task1, child_task2, task2],
                   key=lambda x: x.name),
            sorted(Task.query.all(), key=lambda x: x.name)
        )

        # We still should have the users intact
        admin = User.query.filter_by(name='admin').first()
        self.assertEqual(
            sorted([user1, user2, user3, admin], key=lambda x: x.name),
            sorted(User.query.all(), key=lambda x: x.name)
        )

        self.assertEqual(
            sorted(
                [asset1, task1, child_task1, child_task2, task2],
                key=lambda x: x.name
            ),
            sorted(Task.query.all(), key=lambda x: x.name)
        )

    def test_persistence_of_FilenameTemplate(self):
        """testing the persistence of FilenameTemplate
        """
        from stalker import Type
        ref_type = Type.query.filter_by(name="Reference").first()

        # create a FilenameTemplate object for movie links
        kwargs = {
            "name": "Movie Links Template",
            "target_entity_type": 'Link',
            "type": ref_type,
            "description": "this is a template to be used for links to movie"
                           "files",
            "path": "REFS/{{link_type.name}}",
            "filename": "{{link.file_name}}",
            "output_path": "OUTPUT",
            "output_file_code": "{{link.file_name}}",
        }

        from stalker import db, FilenameTemplate
        new_type_template = FilenameTemplate(**kwargs)

        # persist it
        db.DBSession.add(new_type_template)
        db.DBSession.commit()

        created_by = new_type_template.created_by
        date_created = new_type_template.date_created
        date_updated = new_type_template.date_updated
        description = new_type_template.description
        filename = new_type_template.filename
        name = new_type_template.name
        nice_name = new_type_template.nice_name
        notes = new_type_template.notes
        path = new_type_template.path
        tags = new_type_template.tags
        target_entity_type = new_type_template.target_entity_type
        updated_by = new_type_template.updated_by
        type_ = new_type_template.type

        del new_type_template

        # get it back
        new_type_template_db = \
            FilenameTemplate.query.filter_by(name=kwargs["name"]).first()

        assert (isinstance(new_type_template_db, FilenameTemplate))

        self.assertEqual(created_by, new_type_template_db.created_by)
        self.assertEqual(date_created, new_type_template_db.date_created)
        self.assertEqual(date_updated, new_type_template_db.date_updated)
        self.assertEqual(description, new_type_template_db.description)
        self.assertEqual(filename, new_type_template_db.filename)
        self.assertEqual(name, new_type_template_db.name)
        self.assertEqual(nice_name, new_type_template_db.nice_name)
        self.assertEqual(notes, new_type_template_db.notes)
        self.assertEqual(path, new_type_template_db.path)
        self.assertEqual(tags, new_type_template_db.tags)
        self.assertEqual(target_entity_type,
                         new_type_template_db.target_entity_type)
        self.assertEqual(updated_by, new_type_template_db.updated_by)
        self.assertEqual(type_, new_type_template_db.type)

    def test_persistence_of_ImageFormat(self):
        """testing the persistence of ImageFormat
        """
        # create a new ImageFormat object and try to read it back
        kwargs = {
            "name": "HD",
            "description": "test image format",
            "width": 1920,
            "height": 1080,
            "pixel_aspect": 1.0,
            "print_resolution": 300.0
        }

        # create the ImageFormat object
        from stalker import db, ImageFormat
        im_format = ImageFormat(**kwargs)

        # persist it
        db.DBSession.add(im_format)
        db.DBSession.commit()

        # store attributes
        created_by = im_format.created_by
        date_created = im_format.date_created
        date_updated = im_format.date_updated
        description = im_format.description
        device_aspect = im_format.device_aspect
        height = im_format.height
        name = im_format.name
        nice_name = im_format.nice_name
        notes = im_format.notes
        pixel_aspect = im_format.pixel_aspect
        print_resolution = im_format.print_resolution
        tags = im_format.tags
        updated_by = im_format.updated_by
        width = im_format.width

        # delete the previous im_format
        del im_format

        # get it back
        im_format_db = ImageFormat.query.filter_by(name=kwargs["name"]).first()

        assert (isinstance(im_format_db, ImageFormat))

        # just test the repository part of the attributes
        self.assertEqual(created_by, im_format_db.created_by)
        self.assertEqual(date_created, im_format_db.date_created)
        self.assertEqual(date_updated, im_format_db.date_updated)
        self.assertEqual(description, im_format_db.description)
        self.assertEqual(device_aspect, im_format_db.device_aspect)
        self.assertEqual(height, im_format_db.height)
        self.assertEqual(name, im_format_db.name)
        self.assertEqual(nice_name, im_format_db.nice_name)
        self.assertEqual(notes, im_format_db.notes)
        self.assertEqual(pixel_aspect, im_format_db.pixel_aspect)
        self.assertEqual(print_resolution, im_format_db.print_resolution)
        self.assertEqual(tags, im_format_db.tags)
        self.assertEqual(updated_by, im_format_db.updated_by)
        self.assertEqual(width, im_format_db.width)

    def test_persistence_of_Link(self):
        """testing the persistence of Link
        """
        # user
        from stalker import db, User
        user1 = User(
            name='Test User 1',
            login='tu1',
            email='test@users.com',
            password='secret'
        )
        db.DBSession.add(user1)
        db.DBSession.commit()
        # create a link Type
        from stalker import Type
        sound_link_type = Type(
            name='Sound',
            code='sound',
            target_entity_type='Link'
        )

        # create a Link
        kwargs = {
            'name': 'My Sound',
            'full_path': 'M:/PROJECTS/my_movie_sound.wav',
            'type': sound_link_type,
            'created_by': user1
        }

        from stalker import Link
        link1 = Link(**kwargs)

        # persist it
        db.DBSession.add_all([sound_link_type, link1])
        db.DBSession.commit()

        # use it as a task reference
        from stalker import Repository, Status, StatusList, Project, Task
        repo1 = Repository(name='test repo')
        status1 = Status.query.filter_by(code='NEW').first()
        status2 = Status.query.filter_by(code='WIP').first()

        project_statuses = StatusList(
            target_entity_type='Project',
            statuses=[status1, status2]
        )
        project1 = Project(
            name='Test Project 1',
            code='TP1',
            status_list=project_statuses,
            repository=repo1
        )
        task_statuses = StatusList.query\
            .filter_by(target_entity_type='Task').first()

        task1 = Task(
            name='Test Task',
            project=project1,
            status_list=task_statuses,
            responsible=[user1]
        )
        task1.references.append(link1)

        db.DBSession.add(task1)
        db.DBSession.commit()

        # store attributes
        created_by = link1.created_by
        date_created = link1.date_created
        date_updated = link1.date_updated
        description = link1.description
        name = link1.name
        nice_name = link1.nice_name
        notes = link1.notes
        full_path = link1.full_path
        tags = link1.tags
        type_ = link1.type
        updated_by = link1.updated_by

        # delete the link
        del link1

        # retrieve it back
        link1_db = Link.query.filter_by(name=kwargs["name"]).first()

        assert (isinstance(link1_db, Link))

        self.assertEqual(created_by, link1_db.created_by)
        self.assertEqual(date_created, link1_db.date_created)
        self.assertEqual(date_updated, link1_db.date_updated)
        self.assertEqual(description, link1_db.description)
        self.assertEqual(name, link1_db.name)
        self.assertEqual(nice_name, link1_db.nice_name)
        self.assertEqual(notes, link1_db.notes)
        self.assertEqual(full_path, link1_db.full_path)
        self.assertEqual(tags, link1_db.tags)
        self.assertEqual(type_, link1_db.type)
        self.assertEqual(updated_by, link1_db.updated_by)
        self.assertEqual(task1.references[0], link1_db)

        # delete tests
        task1.references.remove(link1_db)

        # Deleting a Link should not delete anything else
        db.DBSession.delete(link1_db)
        db.DBSession.commit()

        # We still should have the user and the type intact
        self.assertTrue(User.query.get(user1.id) is not None)
        self.assertEqual(user1, User.query.get(user1.id))

        self.assertTrue(Type.query.get(type_.id) is not None)
        self.assertEqual(type_, Type.query.get(type_.id))

        # The task should stay
        self.assertTrue(Task.query.get(task1.id) is not None)
        self.assertEqual(task1, Task.query.get(task1.id))

    def test_persistence_of_Note(self):
        """testing the persistence of Note
        """

        # create a Note and attach it to an entity

        # create a Note object
        note_kwargs = {
            "name": "Note1",
            "description": "This Note is created for the purpose of testing \
            the Note object",
            "content": "Please be carefull about this asset, I will fix the \
            rig later on",
        }

        from stalker import db, Note, Entity
        test_note = Note(**note_kwargs)

        # create an entity
        entity_kwargs = {
            "name": "Entity with Note",
            "description": "This Entity is created for testing purposes",
            "notes": [test_note],
        }

        test_entity = Entity(**entity_kwargs)

        db.DBSession.add_all([test_entity, test_note])
        db.DBSession.commit()

        # store the attributes
        content = test_note.content
        created_by = test_note.created_by
        date_created = test_note.date_created
        date_updated = test_note.date_updated
        description = test_note.description
        name = test_note.name
        nice_name = test_note.nice_name
        updated_by = test_note.updated_by

        # delete the note
        del test_note

        # try to get the note directly
        test_note_db = \
            Note.query.filter(Note.name == note_kwargs["name"]).first()

        assert (isinstance(test_note_db, Note))

        self.assertEqual(content, test_note_db.content)
        self.assertEqual(created_by, test_note_db.created_by)
        self.assertEqual(date_created, test_note_db.date_created)
        self.assertEqual(date_updated, test_note_db.date_updated)
        self.assertEqual(description, test_note_db.description)
        self.assertEqual(name, test_note_db.name)
        self.assertEqual(nice_name, test_note_db.nice_name)
        self.assertEqual(updated_by, test_note_db.updated_by)

    def test_persistence_of_Good(self):
        """testing hte persistence of Good
        """
        from stalker import db, Good

        g1 = Good(
            name='Test Good 1'
        )

        db.DBSession.add(g1)
        db.DBSession.commit()

        name = g1.name

        del g1

        g1_db = Good.query.first()

        self.assertEqual(g1_db.name, name)

    def test_persistence_of_Group(self):
        """testing the persistence of Group
        """
        from stalker import db, Group, User

        group1 = Group(
            name='Test Group'
        )

        user1 = User(
            name='User1',
            login='user1',
            email='user1@test.com',
            password='12'
        )
        user2 = User(
            name='User2',
            login='user2',
            email='user2@test.com',
            password='34'
        )

        group1.users = [user1, user2]

        db.DBSession.add(group1)
        db.DBSession.commit()

        name = group1.name
        users = group1.users

        del group1
        group_db = Group.query.filter_by(name=name).first()

        self.assertEqual(name, group_db.name)
        self.assertEqual(users, group_db.users)

    def test_persistence_of_PriceList(self):
        """testing the persistence of PriceList
        """
        from stalker import db, Good, PriceList
        g1 = Good(name='Test Good 1')
        g2 = Good(name='Test Good 2')
        g3 = Good(name='Test Good 3')

        p = PriceList(
            name='Test Price List',
            goods=[g1, g2, g3]
        )

        db.DBSession.add_all([p, g1, g2, g3])
        db.DBSession.commit()

        del p

        p_db = PriceList.query.first()

        self.assertEqual(p_db.name, 'Test Price List')
        self.assertEqual(p_db.goods, [g1, g2, g3])

        db.DBSession.delete(p_db)
        db.DBSession.commit()

        # we should still have goods
        self.assertTrue(g1 is not None)
        self.assertTrue(g2 is not None)
        self.assertTrue(g3 is not None)

        g1_db = Good.query.filter_by(name='Test Good 1').first()
        self.assertTrue(g1_db is not None)
        self.assertEqual(g1_db.name, 'Test Good 1')

        g2_db = Good.query.filter_by(name='Test Good 2').first()
        self.assertTrue(g2_db is not None)
        self.assertEqual(g2_db.name, 'Test Good 2')

        g3_db = Good.query.filter_by(name='Test Good 3').first()
        self.assertTrue(g3_db is not None)
        self.assertEqual(g3_db.name, 'Test Good 3')

    def test_persistence_of_Project(self):
        """testing the persistence of Project
        """
        # create mock objects
        import datetime
        import pytz
        start = datetime.datetime(2016, 11, 17, tzinfo=pytz.utc) + \
            datetime.timedelta(10)
        end = start + datetime.timedelta(days=20)

        from stalker import db, User
        lead = User(
            name="lead",
            login="lead",
            email="lead@lead.com",
            password="password"
        )

        user1 = User(
            name="user1",
            login="user1",
            email="user1@user1.com",
            password="password"
        )

        user2 = User(
            name="user2",
            login="user2",
            email="user1@user2.com",
            password="password"
        )

        user3 = User(
            name="user3",
            login="user3",
            email="user3@user3.com",
            password="password"
        )

        from stalker import ImageFormat, Type, Project, Structure, Repository
        image_format = ImageFormat(
            name="HD",
            width=1920,
            height=1080
        )

        project_type = Type(
            name='Commercial Project',
            code='commproj',
            target_entity_type='Project'
        )

        structure_type = Type(
            name='Commercial Structure',
            code='commstr',
            target_entity_type='Project'
        )

        project_structure = Structure(
            name="Commercial Structure",
            custom_templates="{{project.code}}\n"
                             "{{project.code}}/ASSETS\n"
                             "{{project.code}}/SEQUENCES\n",
            type=structure_type,
        )

        repo = Repository(
            name="Commercials Repository",
            linux_path="/mnt/M/Projects",
            windows_path="M:/Projects",
            osx_path="/mnt/M/Projects"
        )

        from stalker import Status, StatusList
        status1 = Status.query.filter_by(code="OH").first()
        status2 = Status.query.filter_by(code="CMPL").first()

        project_status_list = StatusList(
            name="A Status List for testing Project",
            statuses=[status1, status2],
            target_entity_type='Project'
        )

        db.DBSession.add(project_status_list)
        db.DBSession.commit()

        # create data for mixins
        # Reference Mixin
        link_type = Type(
            name='Image',
            code='image',
            target_entity_type='Link'
        )

        from stalker import Link
        ref1 = Link(
            name="Ref1",
            full_path="/mnt/M/JOBs/TEST_PROJECT",
            filename="1.jpg",
            type=link_type
        )

        ref2 = Link(
            name="Ref2",
            full_path="/mnt/M/JOBs/TEST_PROJECT",
            filename="1.jpg",
            type=link_type
        )

        # TaskMixin
        task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()

        db.DBSession.add(task_status_list)
        db.DBSession.add_all([lead, ref1, ref2])
        db.DBSession.commit()

        from stalker import WorkingHours
        working_hours = WorkingHours(
            working_hours={
                'mon': [[570, 720], [780, 1170]],
                'tue': [[570, 720], [780, 1170]],
                'wed': [[570, 720], [780, 1170]],
                'thu': [[570, 720], [780, 1170]],
                'fri': [[570, 720], [780, 1170]],
                'sat': [[570, 720], [780, 1170]],
                'sun': [],
            }
        )

        # create a project object
        kwargs = {
            'name': 'Test Project',
            'code': 'TP',
            'description': 'This is a project object for testing purposes',
            'image_format': image_format,
            'fps': 25,
            'type': project_type,
            'structure': project_structure,
            'repositories': [repo],
            'is_stereoscopic': False,
            'display_width': 1.0,
            'start': start,
            'end': end,
            'status_list': project_status_list,
            'status': 0,
            'references': [ref1, ref2],
            'working_hours': working_hours
        }

        new_project = Project(**kwargs)

        # persist it in the database
        db.DBSession.add(new_project)
        db.DBSession.commit()

        from stalker import Task
        task1 = Task(
            name="task1",
            status_list=task_status_list,
            status=0,
            project=new_project,
            resources=[user1, user2],
            responsible=[user1]
        )

        task2 = Task(
            name="task2",
            status_list=task_status_list,
            status=0,
            project=new_project,
            resources=[user3],
            responsible=[user1]
        )
        dt = datetime.datetime
        td = datetime.timedelta
        new_project._computed_start = dt.now(pytz.utc)
        new_project._computed_end = dt.now(pytz.utc) + td(10)

        db.DBSession.add_all([task1, task2])
        db.DBSession.commit()

        # add tickets
        from stalker import Ticket
        ticket1 = Ticket(
            project=new_project
        )
        db.DBSession.add(ticket1)
        db.DBSession.commit()

        # create dailies
        from stalker import Daily
        d1 = Daily(name='Daily1', project=new_project)
        d2 = Daily(name='Daily2', project=new_project)
        d3 = Daily(name='Daily3', project=new_project)
        db.DBSession.add_all([d1, d2, d3])
        db.DBSession.commit()

        # store the attributes
        assets = new_project.assets
        code = new_project.code
        created_by = new_project.created_by
        date_created = new_project.date_created
        date_updated = new_project.date_updated
        description = new_project.description
        end = new_project.end
        duration = new_project.duration
        fps = new_project.fps
        image_format = new_project.image_format
        is_stereoscopic = new_project.is_stereoscopic
        name = new_project.name
        nice_name = new_project.nice_name
        notes = new_project.notes
        references = new_project.references
        repositories = [repo]
        sequences = new_project.sequences
        start = new_project.start
        status = new_project.status
        status_list = new_project.status_list
        structure = new_project.structure
        tags = new_project.tags
        tasks = new_project.tasks
        type_ = new_project.type
        updated_by = new_project.updated_by
        users = [user for user in new_project.users]
        computed_start = new_project.computed_start
        computed_end = new_project.computed_end

        # delete the project
        del new_project

        # now get it
        new_project_db = db.DBSession.query(Project). \
            filter_by(name=kwargs["name"]).first()

        assert isinstance(new_project_db, Project)

        self.assertEqual(assets, new_project_db.assets)
        self.assertEqual(code, new_project_db.code)
        self.assertEqual(computed_start, new_project_db.computed_start)
        self.assertEqual(computed_end, new_project_db.computed_end)
        self.assertEqual(created_by, new_project_db.created_by)
        self.assertEqual(date_created, new_project_db.date_created)
        self.assertEqual(date_updated, new_project_db.date_updated)
        self.assertEqual(description, new_project_db.description)
        self.assertEqual(end, new_project_db.end)
        self.assertEqual(duration, new_project_db.duration)
        self.assertEqual(fps, new_project_db.fps)
        self.assertEqual(image_format, new_project_db.image_format)
        self.assertEqual(is_stereoscopic, new_project_db.is_stereoscopic)
        self.assertEqual(name, new_project_db.name)
        self.assertEqual(nice_name, new_project_db.nice_name)
        self.assertEqual(notes, new_project_db.notes)
        self.assertEqual(references, new_project_db.references)
        self.assertEqual(repositories, new_project_db.repositories)
        self.assertEqual(sequences, new_project_db.sequences)
        self.assertEqual(start, new_project_db.start)
        self.assertEqual(status, new_project_db.status)
        self.assertEqual(status_list, new_project_db.status_list)
        self.assertEqual(structure, new_project_db.structure)
        self.assertEqual(tags, new_project_db.tags)
        self.assertEqual(tasks, new_project_db.tasks)
        self.assertEqual(type_, new_project_db.type)
        self.assertEqual(updated_by, new_project_db.updated_by)
        self.assertEqual(users, new_project_db.users)

        # delete tests
        # now delete the project and expect the following also to be deleted
        #
        # Tasks
        # Tickets
        db.DBSession.delete(new_project_db)
        db.DBSession.commit()

        # Tasks
        self.assertEqual([], Task.query.all())

        # Tickets
        self.assertEqual([], Ticket.query.all())

        # Dailies
        self.assertEqual([], Daily.query.all())

    def test_persistence_of_Repository(self):
        """testing the persistence of Repository
        """
        # create a new Repository object and try to read it back
        kwargs = {
            "name": "Movie-Repo",
            "description": "test repository",
            "linux_path": "/mnt/M",
            "osx_path": "/mnt/M",
            "windows_path": "M:/"
        }

        # create the repository object
        from stalker import db, Repository
        repo = Repository(**kwargs)

        # save it to database
        db.DBSession.add(repo)
        db.DBSession.commit()

        # store attributes
        created_by = repo.created_by
        date_created = repo.date_created
        date_updated = repo.date_updated
        description = repo.description
        linux_path = repo.linux_path
        name = repo.name
        nice_name = repo.nice_name
        notes = repo.notes
        osx_path = repo.osx_path
        path = repo.path
        tags = repo.tags
        updated_by = repo.updated_by
        windows_path = repo.windows_path

        # delete the repo
        del repo

        # get it back
        repo_db = Repository.query\
            .filter_by(name=kwargs["name"]) \
            .first()

        assert (isinstance(repo_db, Repository))

        self.assertEqual(created_by, repo_db.created_by)
        self.assertEqual(date_created, repo_db.date_created)
        self.assertEqual(date_updated, repo_db.date_updated)
        self.assertEqual(description, repo_db.description)
        self.assertEqual(linux_path, repo_db.linux_path)
        self.assertEqual(name, repo_db.name)
        self.assertEqual(nice_name, repo_db.nice_name)
        self.assertEqual(notes, repo_db.notes)
        self.assertEqual(osx_path, repo_db.osx_path)
        self.assertEqual(path, repo_db.path)
        self.assertEqual(tags, repo_db.tags)
        self.assertEqual(updated_by, repo_db.updated_by)
        self.assertEqual(windows_path, repo_db.windows_path)

    def test_persistence_of_Scene(self):
        """testing the persistence of Scene
        """
        from stalker import db, Status, StatusList
        status1 = Status.query.filter_by(code="OH").first()
        status2 = Status.query.filter_by(code="WIP").first()
        status3 = Status.query.filter_by(code="CMPL").first()

        project_status_list = StatusList(
            name="Project Statuses",
            statuses=[status1, status2, status3],
            target_entity_type='Project'
        )

        shot_status_list = StatusList.query\
            .filter_by(target_entity_type='Shot').first()

        from stalker import Repository, User, Type, Project
        repo1 = Repository(
            name="Commercial Repository"
        )

        user1 = User(
            name="User1",
            login="user1",
            email="user1@user.com",
            password="1234",
        )

        commercial_project_type = Type(
            name='Commercial Project',
            code='commproj',
            target_entity_type='Project'
        )

        test_project1 = Project(
            name='Test Project',
            code='TP',
            status_list=project_status_list,
            type=commercial_project_type,
            repository=repo1,
        )

        kwargs = {
            'name': 'Test Scene',
            'code': 'TSce',
            'description': 'this is a test scene',
            'project': test_project1,
        }

        from stalker import Shot, Scene
        test_scene = Scene(**kwargs)

        # now add the shots
        shot1 = Shot(
            code='SH001',
            project=test_project1,
            scenes=[test_scene],
            status_list=shot_status_list,
            responsible=[user1]
        )
        shot2 = Shot(
            code='SH002',
            project=test_project1,
            scenes=[test_scene],
            status_list=shot_status_list,
            responsible=[user1]
        )
        shot3 = Shot(
            code='SH003',
            project=test_project1,
            scenes=[test_scene],
            status_list=shot_status_list,
            responsible=[user1]
        )
        db.DBSession.add_all([shot1, shot2, shot3])
        db.DBSession.add(test_scene)
        db.DBSession.commit()

        # store the attributes
        code = test_scene.code
        created_by = test_scene.created_by
        date_created = test_scene.date_created
        date_updated = test_scene.date_updated
        description = test_scene.description
        name = test_scene.name
        nice_name = test_scene.nice_name
        notes = test_scene.notes
        project = test_scene.project
        shots = test_scene.shots
        tags = test_scene.tags
        updated_by = test_scene.updated_by

        # delete the test_sequence
        del test_scene

        test_scene_db = Scene.query.filter_by(name=kwargs['name']).first()

        self.assertEqual(code, test_scene_db.code)
        self.assertEqual(created_by, test_scene_db.created_by)
        self.assertEqual(date_created, test_scene_db.date_created)
        self.assertEqual(date_updated, test_scene_db.date_updated)
        self.assertEqual(description, test_scene_db.description)
        self.assertEqual(name, test_scene_db.name)
        self.assertEqual(nice_name, test_scene_db.nice_name)
        self.assertEqual(notes, test_scene_db.notes)
        self.assertEqual(project, test_scene_db.project)
        self.assertEqual(shots, test_scene_db.shots)
        self.assertEqual(tags, test_scene_db.tags)
        self.assertEqual(updated_by, test_scene_db.updated_by)

    def test_persistence_of_Sequence(self):
        """testing the persistence of Sequence
        """
        from stalker import Status, StatusList, Project, Repository, Type, User
        status1 = Status.query.filter_by(code="OH").first()
        status2 = Status.query.filter_by(code="WIP").first()
        status3 = Status.query.filter_by(code="CMPL").first()

        project_status_list = StatusList(
            name="Project Statuses",
            statuses=[status1, status2, status3],
            target_entity_type='Project'
        )

        sequence_status_list = StatusList.query\
            .filter_by(target_entity_type='Sequence').first()

        shot_status_list = StatusList.query\
            .filter_by(target_entity_type='Shot').first()

        repo1 = Repository(
            name="Commercial Repository"
        )

        commercial_project_type = Type(
            name='Commercial Project',
            code='commproj',
            target_entity_type='Project'
        )

        lead = User(
            name="lead",
            login="lead",
            email="lead@lead.com",
            password="password"
        )

        test_project1 = Project(
            name='Test Project',
            code='TP',
            status_list=project_status_list,
            type=commercial_project_type,
            repository=repo1,
        )

        kwargs = {
            'name': 'Test Sequence',
            'code': 'TS',
            'description': 'this is a test sequence',
            'project': test_project1,
            'status_list': sequence_status_list,
            'schedule_model': 'effort',
            'schedule_timing': 50,
            'schedule_unit': 'd',
            'responsible': [lead],
        }

        from stalker import Sequence
        test_sequence = Sequence(**kwargs)

        # now add the shots
        from stalker import Shot
        shot1 = Shot(
            code='SH001',
            project=test_project1,
            sequences=[test_sequence],
            status_list=shot_status_list,
            responsible=[lead]
        )
        shot2 = Shot(
            code='SH002',
            project=test_project1,
            sequences=[test_sequence],
            status_list=shot_status_list,
            responsible=[lead]
        )
        shot3 = Shot(
            code='SH003',
            project=test_project1,
            sequence=test_sequence,
            status_list=shot_status_list,
            responsible=[lead]
        )

        from stalker import db
        db.DBSession.add_all([shot1, shot2, shot3])
        db.DBSession.add(test_sequence)
        db.DBSession.commit()

        # store the attributes
        code = test_sequence.code
        created_by = test_sequence.created_by
        date_created = test_sequence.date_created
        date_updated = test_sequence.date_updated
        description = test_sequence.description
        end = test_sequence.end
        name = test_sequence.name
        nice_name = test_sequence.nice_name
        notes = test_sequence.notes
        project = test_sequence.project
        references = test_sequence.references
        shots = test_sequence.shots
        start = test_sequence.start
        status = test_sequence.status
        status_list = test_sequence.status_list
        tags = test_sequence.tags
        children = test_sequence.children
        tasks = test_sequence.tasks
        updated_by = test_sequence.updated_by
        schedule_model = test_sequence.schedule_model
        schedule_timing = test_sequence.schedule_timing
        schedule_unit = test_sequence.schedule_unit

        # delete the test_sequence
        del test_sequence

        test_sequence_db = Sequence.query \
            .filter_by(name=kwargs['name']).first()

        self.assertEqual(code, test_sequence_db.code)
        self.assertEqual(created_by, test_sequence_db.created_by)
        self.assertEqual(date_created, test_sequence_db.date_created)
        self.assertEqual(date_updated, test_sequence_db.date_updated)
        self.assertEqual(description, test_sequence_db.description)
        self.assertEqual(end, test_sequence_db.end)
        self.assertEqual(name, test_sequence_db.name)
        self.assertEqual(nice_name, test_sequence_db.nice_name)
        self.assertEqual(notes, test_sequence_db.notes)
        self.assertEqual(project, test_sequence_db.project)
        self.assertEqual(references, test_sequence_db.references)
        self.assertEqual(shots, test_sequence_db.shots)
        self.assertEqual(start, test_sequence_db.start)
        self.assertEqual(status, test_sequence_db.status)
        self.assertEqual(status_list, test_sequence_db.status_list)
        self.assertEqual(tags, test_sequence_db.tags)
        self.assertEqual(children, test_sequence_db.children)
        self.assertEqual(tasks, test_sequence_db.tasks)
        self.assertEqual(updated_by, test_sequence_db.updated_by)
        self.assertEqual(schedule_model, test_sequence_db.schedule_model)
        self.assertEqual(schedule_timing,
                         test_sequence_db.schedule_timing)
        self.assertEqual(schedule_unit,
                         test_sequence_db.schedule_unit)

    def test_persistence_of_Shot(self):
        """testing the persistence of Shot
        """
        from stalker import Status, StatusList, Project, Type, Repository, User
        status1 = Status.query.filter_by(code="OH").first()
        status2 = Status.query.filter_by(code="WIP").first()
        status3 = Status.query.filter_by(code="CMPL").first()

        project_status_list = StatusList(
            name="Project Statuses",
            statuses=[status1, status2, status3],
            target_entity_type='Project'
        )

        sequence_status_list = StatusList.query\
            .filter_by(target_entity_type='Sequence').first()

        shot_status_list = StatusList.query\
            .filter_by(target_entity_type='Shot').first()

        commercial_project_type = Type(
            name='Commercial Project',
            code='commproj',
            target_entity_type=Project,
        )

        repo1 = Repository(
            name="Commercial Repository"
        )

        lead = User(
            name="lead",
            login="lead",
            email="lead@lead.com",
            password="password"
        )

        test_project1 = Project(
            name='Test project',
            code='tp',
            status_list=project_status_list,
            type=commercial_project_type,
            repository=repo1,
        )

        kwargs = {
            'name': "Test Sequence 1",
            'code': 'tseq1',
            'description': 'this is a test sequence',
            'project': test_project1,
            'status_list': sequence_status_list,
            'responsible': [lead]
        }

        from stalker import Sequence, Scene, Shot
        test_seq1 = Sequence(**kwargs)

        kwargs['name'] = 'Test Sequence 2'
        kwargs['code'] = 'tseq2'
        test_seq2 = Sequence(**kwargs)

        test_sce1 = Scene(
            name='Test Scene 1',
            code='tsce1',
            project=test_project1
        )

        test_sce2 = Scene(
            name='Test Scene 2',
            code='tsce2',
            project=test_project1
        )

        # now add the shots
        shot_kwargs = {
            'code': 'SH001',
            'project': test_project1,
            'sequences': [test_seq1, test_seq2],
            'scenes': [test_sce1, test_sce2],
            'status': 0,
            'status_list': shot_status_list,
            'responsible': [lead]
        }

        test_shot = Shot(**shot_kwargs)

        from stalker import db
        db.DBSession.add(test_shot)
        db.DBSession.add(test_seq1)
        db.DBSession.commit()

        # store the attributes
        code = test_shot.code
        children = test_shot.children
        cut_duration = test_shot.cut_duration
        cut_in = test_shot.cut_in
        cut_out = test_shot.cut_out
        date_created = test_shot.date_created
        date_updated = test_shot.date_updated
        description = test_shot.description
        name = test_shot.name
        nice_name = test_shot.nice_name
        notes = test_shot.notes
        references = test_shot.references
        sequences = test_shot.sequences
        scenes = test_shot.scenes
        status = test_shot.status
        status_list = test_shot.status_list
        tags = test_shot.tags
        tasks = test_shot.tasks
        updated_by = test_shot.updated_by
        fps = test_shot.fps

        # delete the shot
        del test_shot

        test_shot_db = Shot.query.filter_by(code=shot_kwargs["code"]).first()

        self.assertEqual(code, test_shot_db.code)
        self.assertEqual(children, test_shot_db.children)
        self.assertEqual(cut_duration, test_shot_db.cut_duration)
        self.assertEqual(cut_in, test_shot_db.cut_in)
        self.assertEqual(cut_out, test_shot_db.cut_out)
        self.assertEqual(date_created, test_shot_db.date_created)
        self.assertEqual(date_updated, test_shot_db.date_updated)
        self.assertEqual(description, test_shot_db.description)
        self.assertEqual(name, test_shot_db.name)
        self.assertEqual(nice_name, test_shot_db.nice_name)
        self.assertEqual(notes, test_shot_db.notes)
        self.assertEqual(references, test_shot_db.references)
        self.assertEqual(scenes, test_shot_db.scenes)
        self.assertEqual(sequences, test_shot_db.sequences)
        self.assertEqual(status, test_shot_db.status)
        self.assertEqual(status_list, test_shot_db.status_list)
        self.assertEqual(tags, test_shot_db.tags)
        self.assertEqual(tasks, test_shot_db.tasks)
        self.assertEqual(updated_by, test_shot_db.updated_by)
        self.assertEqual(fps, test_shot_db.fps)

    def test_persistence_of_SimpleEntity(self):
        """testing the persistence of SimpleEntity
        """
        import json
        from stalker import db, SimpleEntity, Link
        thumbnail = Link()

        kwargs = {
            "name": "Simple Entity 1",
            "description": "this is for testing purposes",
            'thumbnail': thumbnail,
            'html_style': 'width: 100px; color: purple',
            'html_class': 'purple',
            'generic_text': json.dumps(
                {
                    'some_string': 'hello world'
                },
                sort_keys=True
            ),
        }

        test_simple_entity = SimpleEntity(**kwargs)

        # persist it to the database
        db.DBSession.add(test_simple_entity)
        db.DBSession.commit()

        created_by = test_simple_entity.created_by
        date_created = test_simple_entity.date_created
        date_updated = test_simple_entity.date_updated
        description = test_simple_entity.description
        name = test_simple_entity.name
        nice_name = test_simple_entity.nice_name
        updated_by = test_simple_entity.updated_by
        html_style = test_simple_entity.html_style
        html_class = test_simple_entity.html_class
        generic_text = test_simple_entity.generic_text
        __stalker_version__ = test_simple_entity.__stalker_version__

        del test_simple_entity

        # now try to retrieve it
        test_simple_entity_db = SimpleEntity.query\
            .filter(SimpleEntity.name == kwargs["name"]).first()

        assert (isinstance(test_simple_entity_db, SimpleEntity))

        #self.assertEqual(test_simple_entity, test_simple_entity_DB)
        self.assertEqual(created_by, test_simple_entity_db.created_by)
        self.assertEqual(date_created, test_simple_entity_db.date_created)
        self.assertEqual(date_updated, test_simple_entity_db.date_updated)
        self.assertEqual(description, test_simple_entity_db.description)
        self.assertEqual(name, test_simple_entity_db.name)
        self.assertEqual(nice_name, test_simple_entity_db.nice_name)
        self.assertEqual(updated_by, test_simple_entity_db.updated_by)
        self.assertEqual(html_style, test_simple_entity_db.html_style)
        self.assertEqual(html_class, test_simple_entity_db.html_class)
        self.assertEqual(__stalker_version__,
                         test_simple_entity_db.__stalker_version__)
        self.assertTrue(thumbnail is not None)
        self.assertEqual(thumbnail, test_simple_entity_db.thumbnail)
        self.assertTrue(generic_text is not None)
        self.assertEqual(generic_text, test_simple_entity_db.generic_text)

    def test_persistence_of_Status(self):
        """testing the persistence of Status
        """
        # the status
        kwargs = {
            "name": "TestStatus_test_creating_Status",
            "description": "this is for testing purposes",
            "code": "TSTST"
        }

        from stalker import db, Status
        test_status = Status(**kwargs)

        # persist it to the database
        db.DBSession.add(test_status)
        db.DBSession.commit()

        # store the attributes
        code = test_status.code
        created_by = test_status.created_by
        date_created = test_status.date_created
        date_updated = test_status.date_updated
        description = test_status.description
        name = test_status.name
        nice_name = test_status.nice_name
        notes = test_status.notes
        tags = test_status.tags
        updated_by = test_status.updated_by

        # delete the test_status
        del test_status

        # now try to retrieve it
        test_status_db = Status.query\
            .filter(Status.name == kwargs["name"]).first()

        assert (isinstance(test_status_db, Status))

        # just test the status part of the object
        self.assertEqual(code, test_status_db.code)
        self.assertEqual(created_by, test_status_db.created_by)
        self.assertEqual(date_created, test_status_db.date_created)
        self.assertEqual(date_updated, test_status_db.date_updated)
        self.assertEqual(description, test_status_db.description)
        self.assertEqual(name, test_status_db.name)
        self.assertEqual(nice_name, test_status_db.nice_name)
        self.assertEqual(notes, test_status_db.notes)
        self.assertEqual(tags, test_status_db.tags)
        self.assertEqual(updated_by, test_status_db.updated_by)

    def test_persistence_of_StatusList(self):
        """testing the persistence of StatusList
        """
        # create a couple of statuses
        from stalker import db, Status, StatusList
        statuses = [
            Status(name="Waiting To Start", code="WTS"),
            Status(name="On Hold A", code="OHA"),
            Status(name="Work In Progress A", code="WIPA"),
            Status(name="Complete A", code="CMPLA"),
        ]

        kwargs = dict(
            name="Hede Hodo Status List",
            statuses=statuses,
            target_entity_type="Hede Hodo"
        )

        sequence_status_list = StatusList(**kwargs)

        db.DBSession.add(sequence_status_list)
        db.DBSession.commit()

        # store the attributes
        created_by = sequence_status_list.created_by
        date_created = sequence_status_list.date_created
        date_updated = sequence_status_list.date_updated
        description = sequence_status_list.description
        name = sequence_status_list.name
        nice_name = sequence_status_list.nice_name
        notes = sequence_status_list.notes
        statuses = sequence_status_list.statuses
        tags = sequence_status_list.tags
        target_entity_type = sequence_status_list.target_entity_type
        updated_by = sequence_status_list.updated_by

        # delete the sequence_status_list
        del sequence_status_list

        # now get it back
        sequence_status_list_db = StatusList.query \
            .filter_by(name=kwargs["name"]) \
            .first()

        assert (isinstance(sequence_status_list_db, StatusList))

        self.assertEqual(created_by, sequence_status_list_db.created_by)
        self.assertEqual(date_created, sequence_status_list_db.date_created)
        self.assertEqual(date_updated, sequence_status_list_db.date_updated)
        self.assertEqual(description, sequence_status_list_db.description)
        self.assertEqual(name, sequence_status_list_db.name)
        self.assertEqual(nice_name, sequence_status_list_db.nice_name)
        self.assertEqual(notes, sequence_status_list_db.notes)
        self.assertEqual(statuses, sequence_status_list_db.statuses)
        self.assertEqual(tags, sequence_status_list_db.tags)
        self.assertEqual(target_entity_type,
                         sequence_status_list_db.target_entity_type)
        self.assertEqual(updated_by, sequence_status_list_db.updated_by)

        # try to create another StatusList for the same target_entity_type
        # and do not expect an IntegrityError unless it is committed.

        kwargs["name"] = "new Sequence Status List"
        new_sequence_list = StatusList(**kwargs)

        db.DBSession.add(new_sequence_list)
        self.assertTrue(new_sequence_list in db.DBSession)

        from sqlalchemy.exc import IntegrityError
        with self.assertRaises(IntegrityError) as cm:
            db.DBSession.commit()

        # roll it back
        db.DBSession.rollback()

    def test_persistence_of_Structure(self):
        """testing the persistence of Structure
        """
        from stalker import db, Type, Task
        # create pipeline steps for character
        modeling_task_type = Type(
            name='Modeling',
            code='model',
            description='This is the step where all the modeling job is done',
            target_entity_type='Task'
        )

        animation_task_type = Type(
            name='Animation',
            description='This is the step where all the animation job is '
                        'done it is not limited with characters, other '
                        'things can also be animated',
            code='Anim',
            target_entity_type='Task'
        )

        # create a new asset Type
        char_asset_type = Type(
            name='Character',
            code='char',
            description="This is the asset type which covers animated "
                        "characters",
            target_entity_type='Asset',
        )

        # get the Version Type for FilenameTemplates
        v_type = Type.query \
            .filter_by(target_entity_type="FilenameTemplate") \
            .filter_by(name="Version") \
            .first()

        # create a new type template for character assets
        from stalker import FilenameTemplate
        asset_template = FilenameTemplate(
            name="Character Asset Template",
            description="This is the template for character assets",
            path="Assets/{{asset_type.name}}/{{pipeline_step.code}}",
            filename="{{asset.name}}_{{take.name}}_{{asset_type.name}}_\
            v{{version.version_number}}",
            target_entity_type="Asset",
            type=v_type
        )

        # create a new link type
        image_link_type = Type(
            name='Image',
            code='image',
            description="It is used for links showing an image",
            target_entity_type='Link'
        )

        # get reference Type of FilenameTemplates
        r_type = Type.query \
            .filter_by(target_entity_type="FilenameTemplate") \
            .filter_by(name="Reference") \
            .first()

        # create a new template for references
        image_reference_template = FilenameTemplate(
            name="Image Reference Template",
            description="this is the template for image references, it "
                        "shows where to place the image files",
            path="REFS/{{reference.type.name}}",
            filename="{{reference.file_name}}",
            target_entity_type='Link',
            type=r_type
        )

        commercial_structure_type = Type(
            name='Commercial',
            code='commercial',
            target_entity_type='Structure'
        )

        # create a new structure
        kwargs = {
            'name': 'Commercial Structure',
            'description': 'The structure for commercials',
            'custom_template': """
                Assets
                Sequences
                Sequences/{% for sequence in project.sequences %}
                {{sequence.code}}""",
            'templates': [asset_template, image_reference_template],
            'type': commercial_structure_type
        }

        from stalker import Structure
        new_structure = Structure(**kwargs)

        db.DBSession.add_all([
            new_structure, modeling_task_type, animation_task_type,
            char_asset_type, image_link_type
        ])
        db.DBSession.commit()

        # store the attributes
        templates = new_structure.templates
        created_by = new_structure.created_by
        date_created = new_structure.date_created
        date_updated = new_structure.date_updated
        description = new_structure.description
        name = new_structure.name
        nice_name = new_structure.nice_name
        notes = new_structure.notes
        custom_template = new_structure.custom_template
        tags = new_structure.tags
        updated_by = new_structure.updated_by

        # delete the new_structure
        del new_structure

        new_structure_db = Structure.query\
            .filter_by(name=kwargs["name"]).first()

        assert (isinstance(new_structure_db, Structure))

        self.assertEqual(templates, new_structure_db.templates)
        self.assertEqual(created_by, new_structure_db.created_by)
        self.assertEqual(date_created, new_structure_db.date_created)
        self.assertEqual(date_updated, new_structure_db.date_updated)
        self.assertEqual(description, new_structure_db.description)
        self.assertEqual(name, new_structure_db.name)
        self.assertEqual(nice_name, new_structure_db.nice_name)
        self.assertEqual(notes, new_structure_db.notes)
        self.assertEqual(custom_template, new_structure_db.custom_template)
        self.assertEqual(tags, new_structure_db.tags)
        self.assertEqual(updated_by, new_structure_db.updated_by)

    def test_persistence_of_Studio(self):
        """testing the persistence of Studio
        """
        from stalker import db, Studio
        test_studio = Studio(name='Test Studio')
        db.DBSession.add(test_studio)
        db.DBSession.commit()

        # customize attributes
        from stalker import WorkingHours
        test_studio.daily_working_hours = 11
        test_studio.working_hours = WorkingHours(
            working_hours={
                'mon': [],
                'sat': [[100, 1300]]
            }
        )
        import datetime
        test_studio.timing_resolution = datetime.timedelta(hours=1, minutes=30)

        name = test_studio.name
        daily_working_hours = test_studio.daily_working_hours
        timing_resolution = test_studio._timing_resolution
        working_hours = test_studio.working_hours
        # now = test_studio.now

        del test_studio

        # get it back
        test_studio_db = Studio.query.first()

        self.assertEqual(name, test_studio_db.name)
        self.assertEqual(daily_working_hours,
                         test_studio_db.daily_working_hours)
        self.assertEqual(timing_resolution, test_studio_db.timing_resolution)
        self.assertEqual(working_hours, test_studio_db.working_hours)

    def test_persistence_of_Tag(self):
        """testing the persistence of Tag
        """
        name = "Tag_test_creating_a_Tag"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        import datetime
        import pytz
        date_created = date_updated = datetime.datetime.now(pytz.utc)

        from stalker import db, Tag
        tag = Tag(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated)

        # persist it to the database
        db.DBSession.add(tag)
        db.DBSession.commit()

        # store the attributes
        description = tag.description
        created_by = tag.created_by
        updated_by = tag.updated_by
        date_created = tag.date_created
        date_updated = tag.date_updated

        # delete the aTag
        del tag

        # now try to retrieve it
        tag_db = db.DBSession.query(Tag).filter_by(name=name).first()

        assert (isinstance(tag_db, Tag))

        self.assertEqual(name, tag_db.name)
        self.assertEqual(description, tag_db.description)
        self.assertEqual(created_by, tag_db.created_by)
        self.assertEqual(updated_by, tag_db.updated_by)
        self.assertEqual(date_created, tag_db.date_created)
        self.assertEqual(date_updated, tag_db.date_updated)

    def test_persistence_of_Task(self):
        """testing the persistence of Task
        """
        # create a task
        from stalker import db, Status, User
        status1 = Status(name="stat1", code="STS1")
        status2 = Status(name="stat2", code="STS2")
        status3 = Status(name="stat3", code="STS3")
        status4 = Status(name="stat4", code="STS4")
        status5 = Status(name="stat5", code="STS5")

        user1 = User(
            name="User1",
            login="user1",
            email="user1@user.com",
            password="1234",
        )

        user2 = User(
            name="User2",
            login="user2",
            email="user2@user.com",
            password="1234",
        )

        user3 = User(
            name="User3",
            login="user3",
            email="user3@user.com",
            password="1234",
        )

        from stalker import StatusList, Repository, Project
        project_status_list = StatusList(
            name="Project Status List",
            statuses=[status1, status2, status3, status4, status5],
            target_entity_type='Project',
        )

        repo = Repository(
            name='Test Repo',
            linux_path='/mnt/M/JOBs',
            windows_path='M:/JOBs',
            osx_path='/Users/Shared/Servers/M',
        )

        project1 = Project(
            name='Tests Project',
            code='tp',
            status_list=project_status_list,
            repository=repo,
        )

        from stalker import Type, Asset, Task, TimeLog
        char_asset_type = Type(
            name='Character Asset',
            code='char',
            target_entity_type='Asset'
        )

        asset1 = Asset(
            name='Char1',
            code='char1',
            type=char_asset_type,
            project=project1,
            responsible=[user1]
        )

        task1 = Task(
            name="Test Task",
            watchers=[user3],
            parent=asset1
        )

        child_task1 = Task(
            name='Child Task 1',
            resources=[user1, user2],
            parent=task1,
        )

        child_task2 = Task(
            name='Child Task 2',
            resources=[user1, user2],
            parent=task1,
        )

        task2 = Task(
            name='Another Task',
            project=project1,
            resources=[user1],
            responsible=[user2]
        )

        # time logs
        import datetime
        import pytz
        time_log1 = TimeLog(
            task=child_task1,
            resource=user1,
            start=datetime.datetime.now(pytz.utc),
            end=datetime.datetime.now(pytz.utc) + datetime.timedelta(1)
        )
        task1.computed_start = datetime.datetime.now(pytz.utc)
        task1.computed_end = \
            datetime.datetime.now(pytz.utc) + datetime.timedelta(10)

        time_log2 = TimeLog(
            task=child_task2,
            resource=user1,
            start=datetime.datetime.now(pytz.utc) + datetime.timedelta(1),
            end=datetime.datetime.now(pytz.utc) + datetime.timedelta(2)
        )

        # time log for another task
        time_log3 = TimeLog(
            task=task2,
            resource=user1,
            start=datetime.datetime.now(pytz.utc) + datetime.timedelta(2),
            end=datetime.datetime.now(pytz.utc) + datetime.timedelta(3)
        )

        # Versions
        from stalker import Version
        version1 = Version(
            task=task1
        )
        db.DBSession.add(version1)
        db.DBSession.commit()

        version2 = Version(
            task=task1
        )
        db.DBSession.add(version2)
        db.DBSession.commit()

        version3 = Version(
            task=task2
        )
        db.DBSession.add(version3)
        db.DBSession.commit()

        version4 = Version(
            task=task2
        )
        db.DBSession.add(version4)
        db.DBSession.commit()

        version3.inputs = [version2]
        version2.inputs = [version1]
        version2.inputs = [version4]
        db.DBSession.add(version1)
        db.DBSession.commit()

        # references
        from stalker import Link
        ref1 = Link(
            full_path='some_path',
            original_filename='original_filename'
        )

        ref2 = Link(
            full_path='some_path',
            original_filename='original_filename'
        )

        task1.references.append(ref1)
        task1.references.append(ref2)

        db.DBSession.add_all([
            task1, child_task1, child_task2, task2, time_log1,
            time_log2, time_log3, user1, user2, version1, version2, version3,
            version4, ref1, ref2
        ])
        db.DBSession.commit()

        computed_start = task1.computed_start
        computed_end = task1.computed_end
        created_by = task1.created_by
        date_created = task1.date_created
        date_updated = task1.date_updated
        duration = task1.duration
        end = task1.end
        is_milestone = task1.is_milestone
        name = task1.name
        parent = task1.parent
        priority = task1.priority
        resources = task1.resources
        schedule_model = task1.schedule_model
        schedule_timing = task1.schedule_timing
        schedule_unit = task1.schedule_unit
        start = task1.start
        status = task1.status
        status_list = task1.status_list
        tasks = task1.tasks
        tags = task1.tags
        time_logs = task1.time_logs
        type_ = task1.type
        updated_by = task1.updated_by
        versions = [version1, version2]
        watchers = task1.watchers

        del task1

        # now query it back
        task1_db = Task.query.filter_by(name=name).first()

        assert (isinstance(task1_db, Task))

        self.assertEqual(time_logs, task1_db.time_logs)
        self.assertEqual(created_by, task1_db.created_by)
        self.assertEqual(computed_start, task1_db.computed_start)
        self.assertEqual(computed_end, task1_db.computed_end)
        self.assertEqual(date_created, task1_db.date_created)
        self.assertEqual(date_updated, task1_db.date_updated)
        self.assertEqual(duration, task1_db.duration)
        self.assertEqual(end, task1_db.end)
        self.assertEqual(is_milestone, task1_db.is_milestone)
        self.assertEqual(name, task1_db.name)
        self.assertEqual(parent, task1_db.parent)
        self.assertEqual(priority, task1_db.priority)
        self.assertEqual(resources, [])  # it is a parent task, no child
        self.assertEqual(resources, task1_db.resources)
        self.assertEqual(start, task1_db.start)
        self.assertEqual(status, task1_db.status)
        self.assertEqual(status_list, task1_db.status_list)
        self.assertEqual(tags, task1_db.tags)
        self.assertEqual(
            sorted(tasks, key=lambda x: x.name),
            sorted(task1_db.tasks, key=lambda x: x.name)
        )
        self.assertEqual(tasks, [child_task1, child_task2])
        self.assertEqual(type_, task1_db.type)
        self.assertEqual(updated_by, task1_db.updated_by)
        self.assertEqual(versions, task1_db.versions)
        self.assertEqual(watchers, task1_db.watchers)
        self.assertEqual(schedule_model, task1_db.schedule_model)
        self.assertEqual(schedule_timing, task1_db.schedule_timing)
        self.assertEqual(schedule_unit, task1_db.schedule_unit)
        self.assertEqual(version2.inputs, [version4])
        self.assertEqual(version3.inputs, [version2])
        self.assertEqual(version4.inputs, [])

        # delete tests

        # deleting a Task should also delete:
        #
        # Child Tasks
        # TimeLogs
        # Versions
        # And orphan-references
        #
        # task1_db.references = []
        # with db.DBSession.no_autoflush:
        #     for v in task1_db.versions:
        #         v.inputs = []
        #         for tv in Version.query.filter(Version.inputs.contains(v)):
        #             tv.inputs.remove(v)

        db.DBSession.delete(task1_db)
        db.DBSession.commit()

        # we still should have the versions that are in the inputs (version3
        # and version4) of the original versions (version1, version2)
        self.assertIsNotNone(Version.query.get(version3.id))
        self.assertIsNotNone(Version.query.get(version4.id))

        # Expect to have all child tasks also to be deleted
        self.assertEqual(
            sorted([asset1, task2], key=lambda x: x.name),
            sorted(Task.query.all(), key=lambda x: x.name)
        )

        # Expect to have time logs related to this task are deleted
        self.assertEqual(
            [time_log3],
            TimeLog.query.all()
        )

        # We still should have the users intact
        admin = User.query.filter_by(name='admin').first()
        self.assertEqual(
            sorted([user1, user2, user3, admin], key=lambda x: x.name),
            sorted(User.query.all(), key=lambda x: x.name)
        )

        # When updating the test to include deletion, the test task became a
        # parent task, so all the resources are removed, thus the resource
        # attribute should be tested separately.
        resources = task2.resources
        id_ = task2.id
        del task2

        another_task_db = Task.query.get(id_)
        self.assertEqual(resources, [user1])
        self.assertEqual(resources, another_task_db.resources)

        self.assertEqual(version3.inputs, [])
        self.assertEqual(version4.inputs, [])

    def test_persistence_of_Review(self):
        """testing the persistence of Review
        """
        # create a task
        from stalker import Status, StatusList
        status_new = Status.query.filter_by(code="NEW").first()
        status_rrev = Status.query.filter_by(code="RREV").first()
        status_app = Status.query.filter_by(code="APP").first()

        task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()
        asset_status_list = StatusList.query\
            .filter_by(target_entity_type='Asset').first()

        project_status_list = StatusList(
            name="Project Status List",
            statuses=[status_new, status_app, status_rrev],
            target_entity_type='Project',
        )

        import tempfile
        temp_repo_dir = tempfile.mkdtemp()
        from stalker import Repository
        repo = Repository(
            name='Test Repo',
            linux_path=temp_repo_dir,
            windows_path=temp_repo_dir,
            osx_path=temp_repo_dir,
        )

        from stalker import User
        user1 = User(
            name="User1",
            login="user1",
            email="user1@user.com",
            password="1234",
        )

        user2 = User(
            name="User2",
            login="user2",
            email="user2@user.com",
            password="1234",
        )

        user3 = User(
            name="User3",
            login="user3",
            email="user3@user.com",
            password="1234",
        )

        from stalker import Project
        project1 = Project(
            name='Tests Project',
            code='tp',
            status_list=project_status_list,
            repository=repo,
        )

        from stalker import Type
        char_asset_type = Type(
            name='Character Asset',
            code='char',
            target_entity_type='Asset'
        )

        from stalker import Asset
        asset1 = Asset(
            name='Char1',
            code='char1',
            status_list=asset_status_list,
            type=char_asset_type,
            project=project1,
            responsible=[user1]
        )

        from stalker import Task
        task1 = Task(
            name="Test Task",
            watchers=[user3],
            parent=asset1,
            status_list=task_status_list,
            schedule_timing=5,
            schedule_unit='h',
        )

        child_task1 = Task(
            name='Child Task 1',
            resources=[user1, user2],
            parent=task1,
            status_list=task_status_list
        )

        child_task2 = Task(
            name='Child Task 2',
            resources=[user1, user2],
            parent=task1,
            status_list=task_status_list
        )

        task2 = Task(
            name='Another Task',
            project=project1,
            status_list=task_status_list,
            resources=[user1],
            responsible=[user1]
        )

        # time logs
        import datetime
        import pytz
        from stalker import TimeLog
        time_log1 = TimeLog(
            task=child_task1,
            resource=user1,
            start=datetime.datetime.now(pytz.utc),
            end=datetime.datetime.now(pytz.utc) + datetime.timedelta(1)
        )
        task1.computed_start = datetime.datetime.now(pytz.utc)
        task1.computed_end = \
            datetime.datetime.now(pytz.utc) + datetime.timedelta(10)

        time_log2 = TimeLog(
            task=child_task2,
            resource=user1,
            start=datetime.datetime.now(pytz.utc) + datetime.timedelta(1),
            end=datetime.datetime.now(pytz.utc) + datetime.timedelta(2)
        )

        # time log for another task
        time_log3 = TimeLog(
            task=task2,
            resource=user1,
            start=datetime.datetime.now(pytz.utc) + datetime.timedelta(2),
            end=datetime.datetime.now(pytz.utc) + datetime.timedelta(3)
        )

        from stalker import Review
        rev1 = Review(
            task=task2,
            reviewer=user1,
            schedule_timing=1,
            schedule_unit='h'
        )

        from stalker import db
        db.DBSession.add_all([
            task1, child_task1, child_task2, task2, time_log1,
            time_log2, time_log3, user1, user2, rev1
        ])
        db.DBSession.commit()

        created_by = rev1.created_by
        date_created = rev1.date_created
        date_updated = rev1.date_updated
        name = rev1.name
        schedule_timing = rev1.schedule_timing
        schedule_unit = rev1.schedule_unit
        task = rev1.task
        updated_by = rev1.updated_by

        del rev1

        # now query it back
        rev1_db = Review.query.filter_by(name=name).first()

        assert (isinstance(rev1_db, Review))

        self.assertEqual(created_by, rev1_db.created_by)
        self.assertEqual(date_created, rev1_db.date_created)
        self.assertEqual(date_updated, rev1_db.date_updated)
        self.assertEqual(name, rev1_db.name)
        self.assertEqual(task, rev1_db.task)
        self.assertEqual(updated_by, rev1_db.updated_by)
        self.assertEqual(schedule_timing, rev1_db.schedule_timing)
        self.assertEqual(schedule_unit, rev1_db.schedule_unit)

        # delete tests

        # deleting a Review should be fairly simple:
        db.DBSession.delete(rev1_db)
        db.DBSession.commit()

        # Expect to have no task is deleted
        self.assertEqual(
            sorted(
                [asset1, task1, task2, child_task1, child_task2],
                key=lambda x: x.name
            ),
            sorted(Task.query.all(), key=lambda x: x.name)
        )

    def test_persistence_of_Ticket(self):
        """testing the persistence of Ticket
        """
        from stalker import Repository
        repo = Repository(
            name='Test Repository'
        )

        from stalker import Status, StatusList
        proj_status_list = StatusList(
            name='Project Statuses',
            statuses=[
                Status(name='Work In Progress', code='WIP'),
                Status(name='On Hold', code='OH'),
            ],
            target_entity_type='Project'
        )

        from stalker import Structure
        proj_structure = Structure(
            name='Commercials Structure'
        )

        from stalker import Project
        proj1 = Project(
            name='Test Project 1',
            code='TP1',
            repository=repo,
            structure=proj_structure,
            status_list=proj_status_list
        )

        from stalker import SimpleEntity, Entity
        simple_entity = SimpleEntity(
            name='Test Simple Entity'
        )

        entity = Entity(
            name='Test Entity'
        )

        from stalker import User
        user1 = User(
            name='user 1',
            login='user1',
            email='user1@users.com',
            password='pass'
        )
        user2 = User(
            name='user 2',
            login='user2',
            email='user2@users.com',
            password='pass'
        )

        from stalker import Note
        note1 = Note(content='This is the content of the note 1')
        note2 = Note(content='This is the content of the note 2')

        from stalker import db, Ticket
        related_ticket1 = Ticket(project=proj1)
        db.DBSession.add(related_ticket1)
        db.DBSession.commit()

        related_ticket2 = Ticket(project=proj1)
        db.DBSession.add(related_ticket2)
        db.DBSession.commit()

        # create Tickets
        test_ticket = Ticket(
            project=proj1,
            links=[simple_entity, entity],
            notes=[note1, note2],
            reported_by=user1,
            related_tickets=[related_ticket1,
                             related_ticket2]
        )

        test_ticket.reassign(user1, user2)
        test_ticket.priority = 'MAJOR'

        db.DBSession.add(test_ticket)
        db.DBSession.commit()

        comments = test_ticket.comments
        created_by = test_ticket.created_by
        date_created = test_ticket.date_created
        date_updated = test_ticket.date_updated
        description = test_ticket.description
        logs = test_ticket.logs
        links = test_ticket.links
        name = test_ticket.name
        notes = test_ticket.notes
        number = test_ticket.number
        owner = test_ticket.owner
        priority = test_ticket.priority
        project = test_ticket.project
        related_tickets = test_ticket.related_tickets
        reported_by = test_ticket.reported_by
        resolution = test_ticket.resolution
        status = test_ticket.status
        type_ = test_ticket.type
        updated_by = test_ticket.updated_by

        del test_ticket

        # now query it back
        from stalker import Ticket
        test_ticket_db = Ticket.query.filter_by(name=name).first()

        self.assertEqual(comments, test_ticket_db.comments)
        self.assertEqual(created_by, test_ticket_db.created_by)
        self.assertEqual(date_created, test_ticket_db.date_created)
        self.assertEqual(date_updated, test_ticket_db.date_updated)
        self.assertEqual(description, test_ticket_db.description)
        self.assertNotEqual([], logs)
        self.assertEqual(logs, test_ticket_db.logs)
        self.assertEqual(links, test_ticket_db.links)
        self.assertEqual(name, test_ticket_db.name)
        self.assertEqual(notes, test_ticket_db.notes)
        self.assertEqual(number, test_ticket_db.number)
        self.assertEqual(owner, test_ticket_db.owner)
        self.assertEqual(priority, test_ticket_db.priority)
        self.assertEqual(project, test_ticket_db.project)
        self.assertEqual(related_tickets, test_ticket_db.related_tickets)
        self.assertEqual(reported_by, test_ticket_db.reported_by)
        self.assertEqual(resolution, test_ticket_db.resolution)
        self.assertEqual(status, test_ticket_db.status)
        self.assertEqual(type_, test_ticket_db.type)
        self.assertEqual(updated_by, test_ticket_db.updated_by)

        # delete tests
        # Deleting a Ticket should also delete all the logs related to the
        # ticket
        self.assertEqual(
            sorted(test_ticket_db.logs, key=lambda x: x.name),
            sorted(logs, key=lambda x: x.name)
        )

        db.DBSession.delete(test_ticket_db)
        db.DBSession.commit()

        from stalker import TicketLog
        self.assertEqual([], TicketLog.query.all())

    def test_persistence_of_User(self):
        """testing the persistence of User
        """
        # create a new user save and retrieve it back

        # create a Department for the user
        dep_kwargs = {
            "name": "Test Department",
            "description": "This department has been created for testing \
            purposes",
        }

        from stalker import Department
        new_department = Department(**dep_kwargs)

        # create the user
        user_kwargs = {
            "name": "Test",
            "login": "testuser",
            "email": "testuser@test.com",
            "password": "12345",
            "description": "This user has been created for testing purposes",
            "departments": [new_department],
            'efficiency': 2.5
        }

        from stalker import db, User
        user1 = User(**user_kwargs)

        db.DBSession.add_all([user1, new_department])
        db.DBSession.commit()

        import datetime
        import pytz
        from stalker import Vacation
        vacation1 = Vacation(
            user=user1,
            start=datetime.datetime.now(pytz.utc),
            end=datetime.datetime.now(pytz.utc) + datetime.timedelta(1)
        )

        vacation2 = Vacation(
            user=user1,
            start=datetime.datetime.now(pytz.utc) + datetime.timedelta(2),
            end=datetime.datetime.now(pytz.utc) + datetime.timedelta(3)
        )

        user1.vacations.append(vacation1)
        user1.vacations.append(vacation2)
        db.DBSession.add(user1)
        db.DBSession.commit()

        # create a test project
        from stalker import Repository, Status, StatusList
        repo1 = Repository(name='Test Repo')
        status1 = Status.query.filter_by(code='NEW').first()
        status2 = Status.query.filter_by(code='WIP').first()
        project_statuses = StatusList(
            name='Project Statuses',
            target_entity_type='Project',
            statuses=[status1, status2]
        )
        from stalker import Project, Task, TimeLog
        project1 = Project(
            name='Test Project',
            code='TP',
            repository=repo1,
            status_list=project_statuses
        )
        task_statuses = StatusList.query\
            .filter_by(target_entity_type='Task').first()
        task1 = Task(
            name='Test Task 1',
            project=project1,
            status_list=task_statuses,
            resources=[user1],
            responsible=[user1]
        )
        dt = datetime.datetime
        td = datetime.timedelta
        time_log1 = TimeLog(
            task=task1,
            resource=user1,
            start=dt.now(pytz.utc),
            end=dt.now(pytz.utc) + td(1)
        )
        db.DBSession.add(time_log1)
        db.DBSession.add(task1)
        db.DBSession.commit()

        # store attributes
        created_by = user1.created_by
        date_created = user1.date_created
        date_updated = user1.date_updated
        departments = [dep for dep in user1.departments]
        description = user1.description
        efficiency = user1.efficiency
        email = user1.email
        authentication_logs = user1.authentication_logs
        login = user1.login
        name = user1.name
        nice_name = user1.nice_name
        notes = user1.notes
        password = user1.password
        groups = user1.groups
        projects = [project for project in user1.projects]
        tags = user1.tags
        tasks = user1.tasks
        watching = user1.watching
        updated_by = user1.updated_by
        vacations = [vacation1, vacation2]

        # delete new_user
        del user1

        user1_db = User.query\
            .filter(User.name == user_kwargs["name"]) \
            .first()

        assert (isinstance(user1_db, User))

        # the user itself
        #self.assertEqual(new_user, new_user_DB)
        self.assertEqual(created_by, user1_db.created_by)
        self.assertEqual(date_created, user1_db.date_created)
        self.assertEqual(date_updated, user1_db.date_updated)
        self.assertEqual(departments, user1_db.departments)
        self.assertEqual(description, user1_db.description)
        self.assertEqual(efficiency, user1_db.efficiency)
        self.assertEqual(email, user1_db.email)
        self.assertEqual(authentication_logs, user1_db.authentication_logs)
        self.assertEqual(login, user1_db.login)
        self.assertEqual(name, user1_db.name)
        self.assertEqual(nice_name, user1_db.nice_name)
        self.assertEqual(notes, user1_db.notes)
        self.assertEqual(password, user1_db.password)
        self.assertEqual(groups, user1_db.groups)
        self.assertEqual(projects, user1_db.projects)
        self.assertEqual(tags, user1_db.tags)
        self.assertEqual(tasks, user1_db.tasks)
        self.assertEqual(
            sorted(vacations, key=lambda x: x.name),
            sorted(user1_db.vacations, key=lambda x: x.name)
        )
        self.assertEqual(watching, user1_db.watching)
        self.assertEqual(updated_by, user1_db.updated_by)

        # as the member of a department
        department_db = Department.query\
            .filter(Department.name == dep_kwargs["name"]) \
            .first()

        self.assertEqual(user1_db, department_db.users[0])

        # delete tests
        self.assertEqual(
            sorted([vacation1, vacation2], key=lambda x: x.name),
            sorted(Vacation.query.all(), key=lambda x: x.name)
        )

        # deleting a user should also delete its vacations
        db.DBSession.delete(user1_db)
        db.DBSession.commit()

        self.assertEqual([], Vacation.query.all())

        # deleting a user should also delete the time logs
        self.assertEqual([], TimeLog.query.all())

    def test_persistence_of_AuthenticationLog(self):
        """testing the persistence of AuthenticationLog
        """
        import datetime
        import pytz
        from stalker import User, AuthenticationLog
        from stalker import db
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='sosecret'
        )
        db.DBSession.add(user1)
        db.DBSession.commit()

        from stalker.models.auth import LOGIN, LOGOUT
        al1 = AuthenticationLog(
            user=user1,
            action=LOGIN,
            date=datetime.datetime.now(pytz.utc)
        )

        al2 = AuthenticationLog(
            user=user1,
            action=LOGOUT,
            date=datetime.datetime.now(pytz.utc) + datetime.timedelta(minutes=10)
        )

        db.DBSession.add_all([al1, al2])
        db.DBSession.commit()

        al1_id = al1.id
        action = al1.action
        date = al1.date

        del al1

        al1_from_db = AuthenticationLog.query.get(al1_id)

        self.assertEqual(al1_from_db.user, user1)
        self.assertEqual(al1_from_db.date, date)
        self.assertEqual(al1_from_db.action, action)

        # check if users data is also updated
        self.assertEqual(
            sorted(user1.authentication_logs),
            sorted([al1_from_db, al2])
        )

        # delete tests
        db.DBSession.delete(al1_from_db)
        db.DBSession.commit()

        # check the user still exists
        user1_from_db = User.query.get(user1.id)
        self.assertIsNotNone(user1_from_db)

        # check if the other log is still there
        al2_from_db = AuthenticationLog.query.get(al2.id)
        self.assertIsNotNone(al2_from_db)

        # delete the other AuhenticationLog
        db.DBSession.delete(al2_from_db)
        db.DBSession.commit()

        # check if the user is still there
        user1_from_db = User.query.get(user1.id)
        self.assertIsNotNone(user1_from_db)

    def test_persistence_of_Vacation(self):
        """testing the persistence of Vacation instances
        """
        # create a User
        from stalker import db, User, Type, Vacation
        new_user = User(
            name='Test User',
            login='testuser',
            email='test@user.com',
            password='secret'
        )

        # personal vacation type
        personal_vacation = Type(
            name='Personal',
            code='PERS',
            target_entity_type='Vacation'
        )

        import datetime
        import pytz
        start = datetime.datetime(2013, 6, 7, 15, 0, tzinfo=pytz.utc)
        end = datetime.datetime(2013, 6, 21, 0, 0, tzinfo=pytz.utc)

        vacation = Vacation(
            user=new_user,
            type=personal_vacation,
            start=start,
            end=end
        )

        db.DBSession.add(vacation)
        db.DBSession.commit()

        name = vacation.name

        del vacation

        # get it back
        vacation_db = Vacation.query.filter_by(name=name).first()

        assert isinstance(vacation_db, Vacation)
        self.assertEqual(new_user, vacation_db.user)
        self.assertEqual(start, vacation_db.start)
        self.assertEqual(end, vacation_db.end)
        self.assertEqual(personal_vacation, vacation_db.type)

    def test_persistence_of_Version(self):
        """testing the persistence of Version instances
        """
        # create a project
        from stalker import db, Project, Status, StatusList, Repository
        test_project = Project(
            name='Test Project',
            code='tp',
            status_list=StatusList(
                name='Project Status List',
                target_entity_type=Project,
                statuses=[
                    Status.query.filter_by(code="WIP").first(),
                    Status.query.filter_by(code='CMPL').first()
                ]
            ),
            repository=Repository(
                name='Film Projects',
                windows_path='M:/',
                linux_path='/mnt/M/',
                osx_path='/Users/Volumes/M/',
            )
        )

        # create a task
        from stalker import Task, User
        test_task = Task(
            name='Modeling',
            project=test_project,
            status_list=StatusList.query
            .filter_by(target_entity_type='Task').first(),
            responsible=[
                User(name='user1', login='user1', email='u@u', password='12')
            ]
        )

        # create a new version
        from stalker import Version, Link
        test_version = Version(
            name='version for task modeling',
            task=test_task,
            take='MAIN',
            full_path='M:/Shows/Proj1/Seq1/Shots/SH001/Lighting'
            '/Proj1_Seq1_Sh001_MAIN_Lighting_v001.ma',
            outputs=[
                Link(
                    name='Renders',
                    full_path='M:/Shows/Proj1/Seq1/Shots/SH001/Lighting/'
                    'Output/test1.###.jpg'
                ),
            ]
        )

        # now save it to the database
        db.DBSession.add(test_version)
        db.DBSession.commit()

        # create a new version
        test_version_2 = Version(
            name='version for task modeling',
            task=test_task,
            take='MAIN',
            full_path='M:/Shows/Proj1/Seq1/Shots/SH001/Lighting'
            '/Proj1_Seq1_Sh001_MAIN_Lighting_v001.ma',
            inputs=[test_version]
        )
        self.assertEqual(test_version_2.inputs, [test_version])
        db.DBSession.add(test_version_2)
        db.DBSession.commit()

        created_by = test_version.created_by
        date_created = test_version.date_created
        date_updated = test_version.date_updated
        name = test_version.name
        nice_name = test_version.nice_name
        notes = test_version.notes
        outputs = test_version.outputs
        is_published = test_version.is_published
        full_path = test_version.full_path
        tags = test_version.tags
        take_name = test_version.take_name
        #        tickets = test_version.tickets
        type_ = test_version.type
        updated_by = test_version.updated_by
        version_number = test_version.version_number
        task = test_version.task

        del test_version

        # get it back from the db
        test_version_db = Version.query.filter_by(name=name).first()

        assert (isinstance(test_version_db, Version))

        self.assertEqual(created_by, test_version_db.created_by)
        self.assertEqual(date_created, test_version_db.date_created)
        self.assertEqual(date_updated, test_version_db.date_updated)
        self.assertEqual(name, test_version_db.name)
        self.assertEqual(nice_name, test_version_db.nice_name)
        self.assertEqual(notes, test_version_db.notes)
        self.assertEqual(outputs, test_version_db.outputs)
        self.assertEqual(is_published, test_version_db.is_published)
        self.assertEqual(full_path, test_version_db.full_path)
        self.assertEqual(tags, test_version_db.tags)
        self.assertEqual(take_name, test_version_db.take_name)
        self.assertEqual(type_, test_version_db.type)
        self.assertEqual(updated_by, test_version_db.updated_by)
        self.assertEqual(version_number, test_version_db.version_number)
        self.assertEqual(task, test_version_db.task)

        # try to delete version and expect the task, user and other versions
        # to be intact
        db.DBSession.delete(test_version_db)
        db.DBSession.commit()

        self.assertEqual(test_version_2.inputs, [])

        # create a new version append it to version_2.inputs and then delete
        # version_2
        test_version_3 = Version(
            name='version for task modeling',
            task=test_task,
            take='MAIN',
            full_path='M:/Shows/Proj1/Seq1/Shots/SH001/Lighting'
            '/Proj1_Seq1_Sh001_MAIN_Lighting_v003.ma'
        )
        test_version_2.inputs.append(test_version_3)
        self.assertEqual(test_version_2.inputs, [test_version_3])
        db.DBSession.add(test_version_3)
        db.DBSession.commit()

        # now delete test_version_2
        db.DBSession.delete(test_version_2)
        db.DBSession.commit()

        # and check if test_version_3 is still present in the database
        test_version_3_db = Version.query\
            .filter(Version.name == test_version_3.name)\
            .filter(Version.task == test_version_3.task)\
            .filter(Version.version_number == test_version_3.version_number)\
            .first()

        self.assertIsNotNone(test_version_3_db)
        self.assertEqual(test_version_3_db.task, test_version_3.task)
        self.assertEqual(
            test_version_3_db.version_number,
            test_version_3.version_number
        )

        # create a new version append it to version_3.children and then delete
        # version_3
        test_version_4 = Version(
            name='version for task modeling',
            task=test_task,
            take='MAIN',
            full_path='M:/Shows/Proj1/Seq1/Shots/SH001/Lighting'
            '/Proj1_Seq1_Sh001_MAIN_Lighting_v003.ma'
        )
        test_version_3.children.append(test_version_4)
        self.assertEqual(test_version_3.children, [test_version_4])
        db.DBSession.add(test_version_4)
        db.DBSession.commit()

        # and check if test_version_4 is still present in the database
        test_version_4_db = Version.query\
            .filter(Version.name == test_version_4.name)\
            .filter(Version.task == test_version_4.task)\
            .filter(Version.version_number == test_version_4.version_number)\
            .first()

        self.assertIsNotNone(test_version_4_db)
        self.assertEqual(test_version_4_db.task, test_version_4.task)
        self.assertEqual(
            test_version_4_db.version_number,
            test_version_4.version_number
        )
        self.assertEqual(
            test_version_4_db.parent,
            test_version_3
        )

        # now delete test_version_3
        db.DBSession.delete(test_version_3)
        db.DBSession.commit()

        # and check if test_version_4 is still present in the database
        test_version_4_db = Version.query\
            .filter(Version.name == test_version_4.name)\
            .filter(Version.task == test_version_4.task)\
            .filter(Version.version_number == test_version_4.version_number)\
            .first()

        self.assertIsNotNone(test_version_4_db)
        self.assertEqual(test_version_4_db.task, test_version_4.task)
        self.assertEqual(
            test_version_4_db.version_number,
            test_version_4.version_number
        )
        self.assertIsNone(test_version_4_db.parent)
