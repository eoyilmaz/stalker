# -*- coding: utf-8 -*-

import logging

import pytest

from stalker import log
from stalker.testing import UnitTestDBBase

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


class DatabaseTester(UnitTestDBBase):
    """tests the database and connection to the database
    """

    def test_dbsession_save_method_is_correctly_created(self):
        """testing if the DBSession is correctly created from
        ExtendedScopedSession class
        """
        from stalker.db.session import DBSession, ExtendedScopedSession
        assert isinstance(DBSession, ExtendedScopedSession)

    def test_dbsession_save_method_is_working_properly_for_single_entity(
            self):
        """testing if the DBSession.save() method is working properly for
        single entity
        """
        from stalker import User
        from stalker.db.session import DBSession

        test_user = User(
            name='Test User',
            login='tuser',
            email='tuser@gmail.com',
            password='12345'
        )
        DBSession.save(test_user)

        del test_user
        test_user_db = User.query.filter(User.name == 'Test User').first()
        assert test_user_db is not None

    def test_dbsession_save_method_is_working_properly_for_multiple_entity(self):
        """testing if the DBSession.save() method is working properly for
        single entity
        """
        from stalker import User
        from stalker.db.session import DBSession

        test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@gmail.com',
            password='12345'
        )
        test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@gmail.com',
            password='12345'
        )

        DBSession.save([test_user1, test_user2])

        del test_user1
        del test_user2
        test_user1_db = User.query.filter(User.name == 'Test User 1').first()
        test_user2_db = User.query.filter(User.name == 'Test User 2').first()
        assert test_user1_db is not None
        assert test_user2_db is not None

    def test_dbsession_save_method_is_working_properly_for_no_entry(self):
        """testing if the DBSession.save() method is working properly with no
        parameter given
        """
        from stalker import User
        from stalker.db.session import DBSession

        test_user = User(
            name='Test User',
            login='tuser',
            email='tuser@gmail.com',
            password='12345'
        )
        DBSession.add(test_user)
        DBSession.save()

        del test_user
        test_user_db = User.query.filter(User.name == 'Test User').first()
        assert test_user_db is not None

    def test_default_admin_creation(self):
        """testing if a default admin is created
        """
        # set default admin creation to True
        from stalker import defaults
        defaults.auto_create_admin = True

        # check if there is an admin
        from stalker import User
        admin_db = User.query.filter(User.name == defaults.admin_name).first()

        assert admin_db.name == defaults.admin_name

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

        assert len(admins) == 1

    def test_no_default_admin_creation(self):
        """testing if there is no user if stalker.config.Conf.auto_create_admin
        is False
        """
        self.tearDown()

        # turn down auto admin creation
        from stalker import db, defaults
        defaults.auto_create_admin = False

        # Setup
        # update the config
        from stalker.testing import create_random_db
        self.database_url, self.database_name = create_random_db()

        self.config['sqlalchemy.url'] = self.database_url
        from sqlalchemy.pool import NullPool
        self.config['sqlalchemy.poolclass'] = NullPool

        import os
        from stalker.config import Config
        try:
            os.environ.pop(Config.env_key)
        except KeyError:
            # already removed
            pass

        # regenerate the defaults
        import stalker
        import datetime
        stalker.defaults.timing_resolution = datetime.timedelta(hours=1)

        # init the db
        db.setup(self.config)
        db.init()

        # check if there is a use with name admin
        from stalker import User
        assert User.query.filter_by(name=defaults.admin_name).first() is None

        # check if there is a admins department
        from stalker import Department
        assert Department.query\
            .filter_by(name=defaults.admin_department_name)\
            .first() is None

    def test_non_unique_names_on_different_entity_type(self):
        """testing if there can be non-unique names for different entity types
        """
        # try to create a user and an entity with same name
        # expect Nothing
        kwargs = {
            "name": "user1",
            #"created_by": admin
        }

        from stalker import Entity
        from stalker.db.session import DBSession
        entity1 = Entity(**kwargs)
        DBSession.add(entity1)
        DBSession.commit()

        # lets create the second user
        kwargs.update({
            "name": "User1 Name",
            "login": "user1",
            "email": "user1@gmail.com",
            "password": "user1",
        })

        from stalker import User
        user1 = User(**kwargs)
        DBSession.add(user1)

        # expect nothing, this should work without any error
        DBSession.commit()

    def test_ticket_status_initialization(self):
        """testing if the ticket statuses are correctly created
        """
        from stalker import StatusList
        ticket_status_list = StatusList.query \
            .filter(StatusList.name == 'Ticket Statuses') \
            .first()

        assert isinstance(ticket_status_list, StatusList)

        expected_status_names = [
            'New',
            'Reopened',
            'Closed',
            'Accepted',
            'Assigned'
        ]

        assert len(ticket_status_list.statuses) == len(expected_status_names)
        for status in ticket_status_list.statuses:
            assert status.name in expected_status_names

    def test_daily_status_initialization(self):
        """testing if the daily statuses are correctly created
        """
        from stalker import StatusList
        daily_status_list = StatusList.query \
            .filter(StatusList.name == 'Daily Statuses') \
            .first()

        assert isinstance(daily_status_list, StatusList)

        expected_status_names = [
            'Open',
            'Closed'
        ]

        assert len(daily_status_list.statuses) == len(expected_status_names)

        admin = self.admin
        for status in daily_status_list.statuses:
            assert status.name in expected_status_names
            # check if the created_by and updated_by attributes
            # are set to admin
            assert status.created_by == admin
            assert status.updated_by == admin

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
            assert action.action in actions

    def test_register_raise_TypeError_for_wrong_class_name_argument(self):
        """testing if a TypeError will be raised if the class_name argument is
        not an instance of type or str
        """
        from stalker import db
        with pytest.raises(TypeError):
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

        assert \
            len(permission_db) == len(class_names) * len(defaults.actions) * 2

        for permission in permission_db:
            assert permission.access in ['Allow', 'Deny']
            assert permission.action in defaults.actions
            assert permission.class_name in class_names
            logger.debug('permission.access: %s' % permission.access)
            logger.debug('permission.action: %s' % permission.action)
            logger.debug('permission.class_name: %s' % permission.class_name)

    def test_permissions_not_created_over_and_over_again(self):
        """testing if the Permissions are created only once and trying to call
        __init_db__ will not raise any error
        """
        from stalker import db
        from stalker.db.session import DBSession
        DBSession.remove()
        # DBSession.close()
        db.setup(self.config)
        db.init()

        # this should not give any error
        DBSession.remove()

        db.setup(self.config)
        db.init()

        # and we still have correct amount of Permissions
        from stalker import Permission
        permissions = Permission.query.all()
        assert len(permissions) == 420

    def test_ticket_statuses_are_not_created_over_and_over_again(self):
        """testing if the Ticket Statuses are created only once and trying to
        call __init_db__ will not raise any error
        """
        # create the environment variable and point it to a temp directory
        from stalker import db
        from stalker.db.session import DBSession
        DBSession.remove()

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
        assert len(statuses) == 17

        status_list = \
            StatusList.query.filter_by(target_entity_type='Ticket').first()
        assert status_list is not None
        assert status_list.name == 'Ticket Statuses'

    def test_project_status_list_initialization(self):
        """testing if the project statuses are correctly created
        """
        from stalker import StatusList
        project_status_list = StatusList.query \
            .filter(StatusList.name == 'Project Statuses') \
            .filter(StatusList.target_entity_type == 'Project') \
            .first()

        assert isinstance(project_status_list, StatusList)

        expected_status_names = [
            'Ready To Start',
            'Work In Progress',
            'Completed'
        ]

        expected_status_codes = [
            'RTS',
            'WIP',
            'CMPL'
        ]

        assert len(project_status_list.statuses) == len(expected_status_names)

        db_status_names = map(lambda x: x.name, project_status_list.statuses)
        db_status_codes = map(lambda x: x.code, project_status_list.statuses)

        assert sorted(expected_status_names) == sorted(db_status_names)
        assert sorted(expected_status_codes) == sorted(db_status_codes)

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        admin = self.admin
        for status in project_status_list.statuses:
            assert status.created_by == admin
            assert status.updated_by == admin

    def test_task_status_initialization(self):
        """testing if the task statuses are correctly created
        """
        from stalker import StatusList
        task_status_list = StatusList.query \
            .filter(StatusList.name == 'Task Statuses') \
            .filter(StatusList.target_entity_type == 'Task') \
            .first()

        assert isinstance(task_status_list, StatusList)

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

        assert len(task_status_list.statuses) == len(expected_status_names)

        db_status_names = map(lambda x: x.name, task_status_list.statuses)
        db_status_codes = map(lambda x: x.code, task_status_list.statuses)
        assert sorted(expected_status_names) == sorted(db_status_names)

        assert sorted(expected_status_codes) == sorted(db_status_codes)

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        admin = self.admin
        for status in task_status_list.statuses:
            assert status.created_by == admin
            assert status.updated_by == admin

    def test_asset_status_initialization(self):
        """testing if the asset statuses are correctly created
        """
        from stalker import StatusList
        asset_status_list = StatusList.query \
            .filter(StatusList.name == 'Asset Statuses') \
            .filter(StatusList.target_entity_type == 'Asset') \
            .first()

        assert isinstance(asset_status_list, StatusList)

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

        assert len(asset_status_list.statuses) == len(expected_status_names)

        db_status_names = map(lambda x: x.name, asset_status_list.statuses)
        db_status_codes = map(lambda x: x.code, asset_status_list.statuses)
        assert sorted(expected_status_names) == sorted(db_status_names)
        assert sorted(expected_status_codes) == sorted(db_status_codes)

    def test_shot_status_initialization(self):
        """testing if the shot statuses are correctly created
        """
        from stalker import StatusList
        shot_status_list = StatusList.query \
            .filter(StatusList.name == 'Shot Statuses') \
            .filter(StatusList.target_entity_type == 'Shot') \
            .first()

        assert isinstance(shot_status_list, StatusList)

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

        assert len(shot_status_list.statuses) == len(expected_status_names)

        db_status_names = map(lambda x: x.name, shot_status_list.statuses)
        db_status_codes = map(lambda x: x.code, shot_status_list.statuses)
        assert sorted(expected_status_names) == sorted(db_status_names)
        assert sorted(expected_status_codes) == sorted(db_status_codes)

    def test_sequence_status_initialization(self):
        """testing if the sequence statuses are correctly created
        """
        from stalker import StatusList
        sequence_status_list = StatusList.query \
            .filter(StatusList.name == 'Sequence Statuses') \
            .filter(StatusList.target_entity_type == 'Sequence') \
            .first()

        assert isinstance(sequence_status_list, StatusList)

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

        assert len(sequence_status_list.statuses) == len(expected_status_names)

        db_status_names = map(lambda x: x.name, sequence_status_list.statuses)
        db_status_codes = map(lambda x: x.code, sequence_status_list.statuses)
        assert sorted(expected_status_names) == sorted(db_status_names)
        assert sorted(expected_status_codes) == sorted(db_status_codes)

        # check if the created_by and updated_by attributes are correctly set
        # to admin
        admin = self.admin
        for status in sequence_status_list.statuses:
            assert status.created_by == admin
            assert status.updated_by == admin

    def test_asset_status_initialization_when_there_is_an_Asset_status_list(self):
        """testing if the asset statuses are correctly created when there is a
        StatusList for Sequence is already created
        """
        from stalker import StatusList
        asset_status_list = StatusList.query \
            .filter(StatusList.name == 'Asset Statuses') \
            .first()

        assert isinstance(asset_status_list, StatusList)

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

        assert len(asset_status_list.statuses) == len(expected_status_names)

        db_status_names = map(lambda x: x.name, asset_status_list.statuses)
        db_status_codes = map(lambda x: x.code, asset_status_list.statuses)
        assert sorted(expected_status_names) == sorted(db_status_names)
        assert sorted(expected_status_codes) == sorted(db_status_codes)

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        admin = self.admin
        for status in asset_status_list.statuses:
            assert status.created_by == admin
            assert status.updated_by == admin

    def test_shot_status_initialization_when_there_is_a_Shot_status_list(self):
        """testing if the shot statuses are correctly created when there is a
        StatusList for Shot is already created
        """
        from stalker import StatusList
        shot_status_list = StatusList.query \
            .filter(StatusList.name == 'Shot Statuses') \
            .first()

        assert isinstance(shot_status_list, StatusList)

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

        assert len(shot_status_list.statuses) == len(expected_status_names)

        db_status_names = map(lambda x: x.name, shot_status_list.statuses)
        db_status_codes = map(lambda x: x.code, shot_status_list.statuses)
        assert sorted(expected_status_names) == sorted(db_status_names)
        assert sorted(expected_status_codes) == sorted(db_status_codes)

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        admin = self.admin
        for status in shot_status_list.statuses:
            assert status.created_by == admin
            assert status.updated_by == admin

    def test_sequence_status_initialization_when_there_is_a_Sequence_status_list(self):
        """testing if the sequence statuses are correctly created when there is
        a StatusList for Sequence is already created
        """
        from stalker import StatusList
        sequence_status_list = StatusList.query \
            .filter(StatusList.name == 'Sequence Statuses') \
            .first()

        assert isinstance(sequence_status_list, StatusList)

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

        assert len(sequence_status_list.statuses) == len(expected_status_names)

        db_status_names = map(lambda x: x.name, sequence_status_list.statuses)
        db_status_codes = map(lambda x: x.code, sequence_status_list.statuses)
        assert sorted(expected_status_names) == sorted(db_status_names)
        assert sorted(expected_status_codes) == sorted(db_status_codes)

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        admin = self.admin
        for status in sequence_status_list.statuses:
            assert status.created_by == admin
            assert status.updated_by == admin

    def test_review_status_initialization(self):
        """testing if the review statuses are correctly created
        """
        from stalker import StatusList
        review_status_list = StatusList.query \
            .filter(StatusList.name == 'Review Statuses') \
            .first()

        assert isinstance(review_status_list, StatusList)

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

        assert len(review_status_list.statuses) == len(expected_status_names)

        db_status_names = map(lambda x: x.name, review_status_list.statuses)
        db_status_codes = map(lambda x: x.code, review_status_list.statuses)
        assert sorted(expected_status_names) == sorted(db_status_names)
        assert sorted(expected_status_codes) == sorted(db_status_codes)

        # check if the created_by and updated_by attributes are correctly set
        # to the admin
        admin = self.admin
        for status in review_status_list.statuses:
            assert status.created_by == admin
            assert status.updated_by == admin

    def test___create_entity_statuses_no_entity_type_supplied(self):
        """testing db.__create_entity_statuses() will raise a ValueError when
        no entity_type is supplied
        """
        from stalker.db import create_entity_statuses
        kwargs = {
            'status_names': ['A', 'B'],
            'status_codes': ['A', 'B']
        }
        with pytest.raises(ValueError) as cm:
            create_entity_statuses(**kwargs)

        assert str(cm.value) == 'Please supply entity_type'

    def test___create_entity_statuses_no_status_names_supplied(self):
        """testing db.__create_entity_statuses() will raise a ValueError when
        no status_names is supplied
        """
        from stalker.db import create_entity_statuses
        kwargs = {
            'entity_type': 'Hede Hodo',
            'status_codes': ['A', 'B']
        }
        with pytest.raises(ValueError) as cm:
            create_entity_statuses(**kwargs)

        assert str(cm.value) == 'Please supply status names'

    def test___create_entity_statuses_no_status_codes_supplied(self):
        """testing db.__create_entity_statuses() will raise a ValueError when
        no status_codes is supplied
        """
        from stalker.db import create_entity_statuses
        kwargs = {
            'entity_type': 'Hede Hodo',
            'status_names': ['A', 'B']
        }
        with pytest.raises(ValueError) as cm:
            create_entity_statuses(**kwargs)

        assert str(cm.value) == 'Please supply status codes'

    def test_initialization_of_alembic_version_table(self):
        """testing if the db.init() will also create a table called
        alembic_version
        """
        from stalker.db.session import DBSession
        sql_query = 'select version_num from "alembic_version"'
        version_num = DBSession.connection().execute(sql_query).fetchone()[0]
        assert 'bf67e6a234b4' == version_num

    def test_initialization_of_alembic_version_table_multiple_times(self):
        """testing if the db.create_alembic_table() will handle initializing
        the table multiple times
        """
        from stalker import db
        from stalker.db.session import DBSession
        sql_query = 'select version_num from "alembic_version"'
        version_num = \
            DBSession.connection().execute(sql_query).fetchone()[0]
        assert 'bf67e6a234b4' == version_num

        DBSession.remove()
        db.init()
        db.init()
        db.init()

        version_nums = DBSession.connection().execute(sql_query).fetchall()

        # no additional version is created
        assert len(version_nums) == 1

    def test_alembic_version_mismatch(self):
        """testing if the db.init() will raise a ValueError if the alembic
        version of the database is not equal to the alembic_version of the
        current Stalker release
        """
        from stalker import db
        from stalker.db.session import DBSession
        db.init()

        # now change the alembic_version
        sql = "update alembic_version set version_num='some_random_number'"
        DBSession.connection().execute(sql)
        DBSession.commit()

        # check if it is updated correctly
        sql = "select version_num from alembic_version"
        result = DBSession.connection().execute(sql).fetchone()
        assert result[0] == 'some_random_number'

        # close the connection
        DBSession.connection().close()
        DBSession.remove()

        # re-setup
        with pytest.raises(ValueError) as cm:
            db.setup(self.config)

        assert str(cm.value) == 'Please update the database to version: %s' % db.alembic_version

        # also it is not possible to continue with the current DBSession
        from sqlalchemy.exc import PendingRollbackError
        from stalker import User
        with pytest.raises(PendingRollbackError) as cm:
            DBSession.query(User.id).all()

        assert "Can't reconnect until invalid transaction is rolled back. " \
               "(Background on this error at: http://sqlalche.me/e/14/8s2b)" in str(cm.value)

        # rollback and reconnect to the database
        DBSession.rollback()

        # expect it happen again
        with pytest.raises(ValueError) as cm:
            db.setup(self.config)

        assert str(cm.value) == 'Please update the database to version: ' \
                                '%s' % db.alembic_version

        # rollback and insert the correct alembic version number
        DBSession.rollback()
        from stalker.db import alembic_version
        sql = "update alembic_version set version_num='%s'" % alembic_version
        DBSession.connection().execute(sql)
        DBSession.commit()

        # and now expect everything to work correctly
        db.setup(self.config)
        all_users = DBSession.query(User).all()
        assert all_users is not None

    def test_initialization_of_repo_environment_variables(self):
        """testing if the db.create_repo_env_vars() will create environment
        variables for each repository in the system
        """
        # create a couple of repositories
        from stalker import db, Repository
        repo1 = Repository(name='Repo1', code='R1')
        repo2 = Repository(name='Repo2', code='R2')
        repo3 = Repository(name='Repo3', code='R3')

        all_repos = [repo1, repo2, repo3]
        from stalker.db.session import DBSession
        DBSession.add_all(all_repos)
        DBSession.commit()

        # remove any auto created repo vars
        import os
        for repo in all_repos:
            try:
                os.environ.pop('REPO%s' % repo.code)
            except KeyError:
                pass

        # check if all removed
        for repo in all_repos:
            # check if environment vars are created
            assert ('REPO%s' % repo.code) not in os.environ

        # remove db connection
        DBSession.remove()

        # reconnect
        db.setup(self.config)

        all_repos = Repository.query.all()

        for repo in all_repos:
            # check if environment vars are created
            assert ('REPO%s' % repo.code) in os.environ

    def test_db_init_with_studio_instance(self):
        """testing db.init() using existing Studio instance for config values
        """
        # check the defaults
        from stalker import defaults
        assert defaults.daily_working_hours != 8
        assert defaults.weekly_working_days != 4
        assert defaults.weekly_working_hours != 32
        assert defaults.yearly_working_days != 180

        import datetime
        assert defaults.timing_resolution != datetime.timedelta(minutes=5)

        from stalker import Studio, WorkingHours

        # check no studio
        studios = Studio.query.all()
        assert studios == []

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
        from stalker.db.session import DBSession
        DBSession.add(test_studio)
        DBSession.commit()

        # remove everything
        DBSession.connection().close()
        DBSession.remove()

        # re-init db
        db.setup(self.config)

        # and expect the defaults to be updated with studio defaults
        assert defaults.daily_working_hours == 8
        assert defaults.weekly_working_days == 4
        assert defaults.weekly_working_hours == 32
        assert defaults.yearly_working_days == 209
        assert defaults.timing_resolution == datetime.timedelta(minutes=5)

    def test_get_alembic_version_is_working_properly_when_there_is_no_alembic_version_table(self):
        """testing if get_alembic_version() is working properly when there is
        no alembic_version table
        """
        # drop the table
        from stalker import db
        from stalker.db.session import DBSession
        DBSession.connection().execute(
            'DROP TABLE IF EXISTS alembic_version'
        )
        # now get the alembic_version
        # this should not raise an OperationalError
        alembic_version = db.get_alembic_version()
        assert alembic_version is None

    def test_create_ticket_statuses_called_multiple_times(self):
        """testing if no IntegrityError will be raised when
        create_ticket_statuses() called multiple times
        """
        from stalker import db
        db.create_ticket_statuses()
        db.create_ticket_statuses()
        db.create_ticket_statuses()

    def test_create_entity_statuses_called_multiple_times(self):
        """testing if no IntegrityError will be raised when
        create_entity_statuses() called multiple times
        """
        from stalker import defaults

        # create statuses for Tickets
        ticket_names = defaults.ticket_status_names
        ticket_codes = defaults.ticket_status_codes

        from stalker import db
        db.create_entity_statuses(
            'Ticket', ticket_names, ticket_codes, self.admin
        )
        db.create_entity_statuses(
            'Ticket', ticket_names, ticket_codes, self.admin
        )

    def test_register_called_multiple_times(self):
        """testing if calling db.register() multiple times will not raise any
        errors
        """
        from stalker import db, User
        db.register(User)
        db.register(User)
        db.register(User)
        db.register(User)

    def test_setup_without_settings(self):
        """testing if db.setup() function will use the default settings if no
        setting is supplied
        """
        from stalker import db
        db.setup()
        # db.init()
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        engine = conn.engine
        assert str(engine.url) == 'sqlite://'

    def test_setup_with_settings(self):
        """testing if db.setup() function will use the given settings if no
        setting is supplied
        """
        # self.tearDown()

        # the default setup is already using the
        from stalker import db
        from sqlalchemy.exc import ArgumentError

        with pytest.raises(ArgumentError) as cm:
            db.setup({'sqlalchemy.url': 'random url'})

        assert str(cm.value) == "Could not parse rfc1738 URL from string " \
                                "'random url'"


class DatabaseModelsTester(UnitTestDBBase):
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

        from stalker import Repository
        test_repository_type = Type(
            name='Test Repository Type A',
            code='trta',
            target_entity_type='Repository',
        )

        test_repository = Repository(
            name='Test Repository A',
            code='TRA',
            type=test_repository_type
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
            type=commercial_type,
            repository=test_repository,
        )

        from stalker.db.session import DBSession
        DBSession.add(test_project)
        DBSession.commit()

        kwargs = {
            'name': 'Test Asset',
            'code': 'test_asset',
            'description': 'This is a test Asset object',
            'type': asset_type,
            'project': test_project,
            'created_by': test_user,
            'responsible': [test_user]
        }

        from stalker import Asset
        test_asset = Asset(**kwargs)
        # logger.debug('test_asset.project : %s' % test_asset.project)

        DBSession.add(test_asset)
        DBSession.commit()

        # logger.debug('test_asset.project (after commit): %s' %
        #              test_asset.project)

        from stalker import Task
        test_task1 = Task(
            name='test task 1', status=0,
            parent=test_asset,
        )

        test_task2 = Task(
            name='test task 2', status=0,
            parent=test_asset,
        )

        test_task3 = Task(
            name='test task 3', status=0,
            parent=test_asset,
        )

        DBSession.add_all([test_task1, test_task2, test_task3])
        DBSession.commit()

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

        #assert test_asset, test_asset_DB)
        assert code == test_asset_db.code
        assert test_asset_db.created_by is not None
        assert created_by == test_asset_db.created_by
        assert date_created == test_asset_db.date_created
        assert date_updated == test_asset_db.date_updated
        assert description == test_asset_db.description
        assert duration == test_asset_db.duration
        assert end == test_asset_db.end
        assert name == test_asset_db.name
        assert nice_name == test_asset_db.nice_name
        assert notes == test_asset_db.notes
        assert project == test_asset_db.project
        assert references == test_asset_db.references
        assert start == test_asset_db.start
        assert status == test_asset_db.status
        assert status_list == test_asset_db.status_list
        assert tags == test_asset_db.tags
        assert children == test_asset_db.children
        assert type_ == test_asset_db.type
        assert updated_by == test_asset_db.updated_by

        # now test the deletion of the asset class
        DBSession.delete(test_asset_db)
        DBSession.commit()

        # we should still have the user
        assert User.query.filter(User.id == created_by.id).first() is not None

        # we should still have the project
        assert Project.query.filter(
            Project.id == project.id).first() is not None

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
            code='TRA',
            type=test_repository_type
        )

        from stalker import StatusList
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
            type=commercial_type,
            repository=test_repository,
        )

        from stalker.db.session import DBSession
        DBSession.add(test_project)
        DBSession.commit()

        kwargs = {
            'name': 'Test Budget',
            'project': test_project,
            'created_by': test_user,
            'status_list': budget_status_list,
            'status': status1
        }

        from stalker import Budget
        test_budget = Budget(**kwargs)

        DBSession.add(test_budget)
        DBSession.commit()

        from stalker import Good
        good = Good(name='Some Good', cost=9, msrp=10, unit='$/hour')
        DBSession.add(good)
        DBSession.commit()

        # create some entries
        from stalker import BudgetEntry
        entry1 = BudgetEntry(budget=test_budget, good=good, amount=5.0)
        entry2 = BudgetEntry(budget=test_budget, good=good, amount=1.0)

        DBSession.add_all([entry1, entry2])
        DBSession.commit()

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

        assert test_budget_db.created_by is not None
        assert created_by == test_budget_db.created_by
        assert date_created == test_budget_db.date_created
        assert date_updated == test_budget_db.date_updated
        assert name == test_budget_db.name
        assert nice_name == test_budget_db.nice_name
        assert notes == test_budget_db.notes
        assert project == test_budget_db.project
        assert tags == test_budget_db.tags
        assert updated_by == test_budget_db.updated_by
        assert entries == test_budget_db.entries
        assert status == status1

        # and we should have our entries intact
        assert BudgetEntry.query.all() != []

        # now test the deletion of the asset class
        DBSession.delete(test_budget_db)
        DBSession.commit()

        # we should still have the user
        assert User.query.filter(User.id == created_by.id).first() is not None

        # we should still have the project
        assert Project.query.filter(
            Project.id == project.id).first() is not None

        # and we should have our page deleted
        assert Budget.query.filter(
            Budget.name == kwargs['name']).first() is None

        # and we should have our entries deleted
        assert BudgetEntry.query.all() == []

        # we still should have the good
        good_db = Good.query.filter(Good.name == 'Some Good').first()
        assert good_db is not None

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
            code='TRA',
            type=test_repository_type
        )

        from stalker import StatusList
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

        from stalker import Client, Project
        from stalker.db.session import DBSession
        test_client = Client(name='Test Client')
        DBSession.add(test_client)

        test_project = Project(
            name='Test Project For Budget Creation',
            code='TPFBC',
            type=commercial_type,
            repository=test_repository,
            clients=[test_client]
        )

        DBSession.add(test_project)
        DBSession.commit()

        from stalker import Budget
        test_budget = Budget(
            name='Test Budget',
            project=test_project,
            created_by=test_user,
            status_list=budget_status_list,
            status=status1
        )

        DBSession.add(test_budget)
        DBSession.commit()

        from stalker import Good
        good = Good(name='Some Good', cost=9, msrp=10, unit='$/hour')
        DBSession.add(good)
        DBSession.commit()

        # create some entries
        from stalker import BudgetEntry
        entry1 = BudgetEntry(budget=test_budget, good=good, amount=5.0)
        entry2 = BudgetEntry(budget=test_budget, good=good, amount=1.0)

        DBSession.add_all([entry1, entry2])
        DBSession.commit()

        # create an invoice
        from stalker import Invoice
        test_invoice = Invoice(
            created_by=test_user,
            budget=test_budget,
            client=test_client,
            amount=1232.4,
            unit='TRY'
        )
        DBSession.add(test_invoice)

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

        assert test_user == test_invoice_db.created_by
        assert created_by == test_invoice_db.created_by
        assert date_created == test_invoice_db.date_created
        assert date_updated == test_invoice_db.date_updated
        assert name == test_invoice_db.name
        assert nice_name == test_invoice_db.nice_name
        assert notes == test_invoice_db.notes
        assert tags == test_invoice_db.tags
        assert updated_by == test_invoice_db.updated_by

        assert budget == test_invoice_db.budget
        assert client == test_invoice_db.client
        assert amount == test_invoice_db.amount
        assert unit == test_invoice_db.unit

        # now test the deletion of the invoice instance
        DBSession.delete(test_invoice_db)
        DBSession.commit()

        # we should still have the budget
        assert Budget.query.filter(Budget.id == budget.id).first() == budget

        # we should still have the client
        assert Client.query.filter(Client.id == client.id).first() == client

        # and we should have the invoice deleted
        assert Invoice.query.filter(
            Invoice.name == test_invoice_db.name).first() is None

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
            code='TRA',
            type=test_repository_type
        )

        from stalker import StatusList
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

        from stalker import Client
        from stalker.db.session import DBSession
        test_client = Client(name='Test Client')
        DBSession.add(test_client)

        from stalker import Project
        test_project = Project(
            name='Test Project For Budget Creation',
            code='TPFBC',
            type=commercial_type,
            repository=test_repository,
            clients=[test_client]
        )

        DBSession.add(test_project)
        DBSession.commit()

        from stalker import Budget
        test_budget = Budget(
            name='Test Budget',
            project=test_project,
            created_by=test_user,
            status_list=budget_status_list,
            status=status1
        )

        DBSession.add(test_budget)
        DBSession.commit()

        from stalker import Good
        good = Good(name='Some Good', cost=9, msrp=10, unit='$/hour')
        DBSession.add(good)
        DBSession.commit()

        # create some entries
        from stalker import BudgetEntry
        entry1 = BudgetEntry(budget=test_budget, good=good, amount=5.0)
        entry2 = BudgetEntry(budget=test_budget, good=good, amount=1.0)

        DBSession.add_all([entry1, entry2])
        DBSession.commit()

        # create an invoice
        from stalker import Invoice
        test_invoice = Invoice(
            created_by=test_user,
            budget=test_budget,
            client=test_client,
            amount=1232.4,
            unit='TRY'
        )
        DBSession.add(test_invoice)

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

        assert test_user == test_payment_db.created_by
        assert created_by == test_payment_db.created_by
        assert date_created == test_payment_db.date_created
        assert date_updated == test_payment_db.date_updated
        assert name == test_payment_db.name
        assert nice_name == test_payment_db.nice_name
        assert notes == test_payment_db.notes
        assert tags == test_payment_db.tags
        assert updated_by == test_payment_db.updated_by

        assert invoice == test_payment_db.invoice
        assert amount == test_payment_db.amount
        assert unit == test_payment_db.unit

        # now test the deletion of the invoice instance
        DBSession.delete(test_payment_db)
        DBSession.commit()

        # we should still have the budget
        assert Budget.query.filter(
            Budget.id == test_budget.id).first() == test_budget

        # we should still have the Invoice
        assert Invoice.query.filter(
            Invoice.id == test_invoice.id).first() == test_invoice

        # and we should have the payment deleted
        assert Payment.query.filter(
            Payment.name == test_payment_db.name).first() is None

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
            code='TRA',
            type=test_repository_type
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
            type=commercial_type,
            repository=test_repository,
        )

        from stalker.db.session import DBSession
        DBSession.add(test_project)
        DBSession.commit()

        kwargs = {
            'title': 'Test Wiki Page',
            'content': 'This is a test wiki page',
            'project': test_project,
            'created_by': test_user
        }

        from stalker import Page
        test_page = Page(**kwargs)

        DBSession.add(test_page)
        DBSession.commit()

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

        #assert test_asset, test_asset_DB)
        assert test_page_db.created_by is not None
        assert created_by == test_page_db.created_by
        assert date_created == test_page_db.date_created
        assert date_updated == test_page_db.date_updated
        assert content == test_page_db.content
        assert name == test_page_db.name
        assert nice_name == test_page_db.nice_name
        assert notes == test_page_db.notes
        assert project == test_page_db.project
        assert tags == test_page_db.tags
        assert title == test_page_db.title
        assert updated_by == test_page_db.updated_by

        # now test the deletion of the asset class
        DBSession.delete(test_page_db)
        DBSession.commit()

        # we should still have the user
        assert User.query.filter(User.id == created_by.id).first() is not None

        # we should still have the project
        assert Project.query.filter(
            Project.id == project.id).first() is not None

        # and we should have our page deleted
        assert Page.query.filter(Page.title == kwargs['title']).first() is None

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
            code='CR',
            linux_path='/mnt/shows',
            windows_path='S:/',
            osx_path='/mnt/shows'
        )

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
            repository=repo
        )

        from stalker import Task
        test_task = Task(
            name='Test Task',
            start=start,
            end=end,
            resources=[user1, user2],
            project=proj1,
            responsible=[user1]
        )
        from stalker.db.session import DBSession

        from stalker import TimeLog
        test_time_log = TimeLog(
            task=test_task,
            resource=user1,
            start=datetime.datetime(2013, 1, 10, tzinfo=pytz.utc),
            end=datetime.datetime(2013, 1, 13, tzinfo=pytz.utc),
            description=description
        )

        DBSession.add(test_time_log)
        DBSession.commit()
        tlog_id = test_time_log.id

        del test_time_log

        # now retrieve it back
        test_time_log_db = TimeLog.query.filter_by(id=tlog_id).first()

        assert description == test_time_log_db.description
        assert start == test_time_log_db.start
        assert end == test_time_log_db.end
        assert user1 == test_time_log_db.resource
        assert test_task == test_time_log_db.task

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
            code='CR',
            linux_path='/mnt/shows',
            windows_path='S:/',
            osx_path='/mnt/shows'
        )

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
            repository=repo
        )

        from stalker import Task
        test_task = Task(
            name='Test Task',
            start=start,
            end=end,
            resources=[user1, user2],
            project=proj1,
            responsible=[user1]
        )

        from stalker.db.session import DBSession
        DBSession.add(test_task)
        DBSession.commit()

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
        DBSession.add(new_tl1)
        DBSession.commit()

        # create a new TimeLog
        new_tl2 = TimeLog(
            task=test_task,
            resource=user1,
            start=end,
            end=end + datetime.timedelta(hours=3)
        )
        DBSession.add(new_tl2)
        DBSession.commit()

        # update it to have overlapping timing values with new_tl1
        from sqlalchemy.exc import IntegrityError
        new_tl2.start = start + datetime.timedelta(hours=2)

        with pytest.raises(IntegrityError) as cm:
            DBSession.commit()

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
        from stalker.db.session import DBSession
        DBSession.add(test_client)
        DBSession.commit()

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

        from stalker.models.budget import Good
        good1 = Good(name='Test Good 1')
        good2 = Good(name='Test Good 2')
        good3 = Good(name='Test Good 3')
        good4 = Good(name='Test Good 4')
        good5 = Good(name='Test Good 5')
        test_client.goods = [good1, good2, good3, good5]

        DBSession.add(good4)
        DBSession.add_all([user1, user2, user3, test_client])
        DBSession.commit()

        assert test_client in DBSession

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
        goods = [good1, good2, good3]  # not included good5 on purpose

        # remove the good5 from list to see if it will still be exist in the db
        test_client.goods.remove(good5)
        DBSession.commit()

        del test_client

        # lets check the data
        # first get the client from the db
        client_db = Client.query.filter_by(name=name).first()

        assert isinstance(client_db, Client)

        assert created_by == client_db.created_by
        assert date_created == client_db.date_created
        assert date_updated == client_db.date_updated
        assert description == client_db.description
        assert users == client_db.users
        assert name == client_db.name
        assert nice_name == client_db.nice_name
        assert notes == client_db.notes
        assert tags == client_db.tags
        assert updated_by == client_db.updated_by
        assert goods == client_db.goods

        # delete the client and expect the users are still there
        DBSession.delete(client_db)
        DBSession.commit()

        user1_db = User.query.filter_by(login='u1tpd').first()
        user2_db = User.query.filter_by(login='u2tpd').first()
        user3_db = User.query.filter_by(login='u3tpd').first()

        assert user1_db is not None
        assert user2_db is not None
        assert user3_db is not None

        # goods should be deleted with client
        good1 = Good.query.filter_by(name='Test Good 1').first()
        good2 = Good.query.filter_by(name='Test Good 2').first()
        good3 = Good.query.filter_by(name='Test Good 3').first()
        good4 = Good.query.filter_by(name='Test Good 4').first()
        good5 = Good.query.filter_by(name='Test Good 5').first()

        assert good1 is None
        assert good2 is None
        assert good3 is None
        assert good4 is not None
        assert good5 is not None

    def test_persistence_of_Daily(self):
        """testing the persistence of a Daily instance
        """
        from stalker import User
        test_user1 = User(
            name='User1',
            login='user1',
            email='user1@user1.com',
            password='12345'
        )

        from stalker import Repository, Project
        test_repo = Repository(name='Test Repository', code='TR')
        test_project = Project(
            name='Test Project',
            code='TP',
            repository=test_repo,
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
        from stalker.db.session import DBSession
        DBSession.add_all([test_task1, test_task2, test_task3])
        DBSession.commit()

        from stalker import Version
        test_version1 = Version(task=test_task1)
        DBSession.add(test_version1)
        DBSession.commit()

        test_version2 = Version(task=test_task1)
        DBSession.add(test_version2)
        DBSession.commit()

        test_version3 = Version(task=test_task1)
        DBSession.add(test_version3)
        DBSession.commit()

        test_version4 = Version(task=test_task2)
        DBSession.add(test_version4)
        DBSession.commit()

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

        DBSession.add_all([
            test_task1, test_task2, test_task3,
            test_version1, test_version2, test_version3,
            test_version4,
            test_link1, test_link2, test_link3, test_link4
        ])
        DBSession.commit()

        # arguments
        name = 'Test Daily'
        links = [test_link1, test_link2, test_link3]

        from stalker import Daily
        daily = Daily(name=name, project=test_project)
        daily.links = links

        DBSession.add(daily)
        DBSession.commit()

        daily_id = daily.id

        del daily

        daily_db = Daily.query.get(daily_id)

        assert daily_db.name == name
        assert daily_db.links == links
        assert daily_db.project == test_project

        link1_id = test_link1.id
        link2_id = test_link2.id
        link3_id = test_link3.id
        link4_id = test_link4.id

        # delete tests
        DBSession.delete(daily_db)
        DBSession.commit()

        # test if links are still there
        from stalker import Link
        test_link1_db = Link.query.get(link1_id)
        test_link2_db = Link.query.get(link2_id)
        test_link3_db = Link.query.get(link3_id)
        test_link4_db = Link.query.get(link4_id)

        assert test_link1_db is not None
        assert isinstance(test_link1_db, Link)

        assert test_link2_db is not None
        assert isinstance(test_link2_db, Link)

        assert test_link3_db is not None
        assert isinstance(test_link3_db, Link)

        assert test_link4_db is not None
        assert isinstance(test_link4_db, Link)

        from stalker import DailyLink
        assert DailyLink.query.all() == []

        assert Link.query.count() == 8  # including versions

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

        from stalker import Department
        test_dep = Department(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated
        )
        from stalker.db.session import DBSession
        DBSession.add(test_dep)
        DBSession.commit()

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

        DBSession.add(test_dep)
        DBSession.commit()

        assert test_dep in DBSession

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

        assert isinstance(test_dep_db, Department)

        assert created_by == test_dep_db.created_by
        assert date_created == test_dep_db.date_created
        assert date_updated == test_dep_db.date_updated
        assert description == test_dep_db.description
        assert users == test_dep_db.users
        assert name == test_dep_db.name
        assert nice_name == test_dep_db.nice_name
        assert notes == test_dep_db.notes
        assert tags == test_dep_db.tags
        assert updated_by == test_dep_db.updated_by

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
        from stalker.db.session import DBSession
        DBSession.add_all([test_entity, test_entity2])
        DBSession.commit()

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

        assert created_by == test_entity_db.created_by
        assert date_created == test_entity_db.date_created
        assert date_updated == test_entity_db.date_updated
        assert description == test_entity_db.description
        assert name == test_entity_db.name
        assert nice_name == test_entity_db.nice_name
        assert \
            sorted(notes, key=lambda x: x.name) == \
            sorted([note1, note2], key=lambda x: x.name)

        assert notes == test_entity_db.notes
        assert tags == test_entity_db.tags
        assert updated_by == test_entity_db.updated_by

        # delete tests

        # Deleting an Entity should also delete the associated notes
        DBSession.delete(test_entity_db)
        DBSession.commit()

        from stalker import Entity, Note
        test_entity2_db = Entity.query.filter_by(name='Test Entity 2').first()
        assert isinstance(test_entity2_db, Entity)

        assert \
            sorted([note1, note2], key=lambda x: x.name) == \
            sorted(Note.query.all(), key=lambda x: x.name)
        assert \
            sorted([note1], key=lambda x: x.name) == \
            sorted(test_entity2_db.notes, key=lambda x: x.name)

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

        from stalker import Repository
        repo = Repository(
            name='Test Repo',
            code='TR',
            linux_path='/mnt/M/JOBs',
            windows_path='M:/JOBs',
            osx_path='/Users/Shared/Servers/M',
        )

        from stalker import Project
        project1 = Project(
            name='Tests Project',
            code='tp',
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

        from stalker.db.session import DBSession
        DBSession.add_all([
            task1, child_task1, child_task2, task2, user1, user2, entity_group1
        ])
        DBSession.commit()

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

        assert created_by == entity_group1_db.created_by
        assert date_created == entity_group1_db.date_created
        assert date_updated == entity_group1_db.date_updated
        assert name == entity_group1_db.name
        assert tags == entity_group1_db.tags
        assert \
            sorted(entities, key=lambda x: x.name) == \
            sorted(entity_group1_db.entities, key=lambda x: x.name)
        assert entities ==[task1, child_task2, task2]
        assert type_ == entity_group1_db.type
        assert updated_by == entity_group1_db.updated_by

        # delete tests
        # deleting entity group will not delete the contained entities
        DBSession.delete(entity_group1_db)
        DBSession.commit()

        assert sorted([task1, asset1, child_task1, child_task2, task2],
                      key=lambda x: x.name) == \
            sorted(Task.query.all(), key=lambda x: x.name)

        # We still should have the users intact
        admin = User.query.filter_by(name='admin').first()
        assert \
            sorted([user1, user2, user3, admin], key=lambda x: x.name) == \
            sorted(User.query.all(), key=lambda x: x.name)

        assert \
            sorted(
                [asset1, task1, child_task1, child_task2, task2],
                key=lambda x: x.name
            ) == \
            sorted(Task.query.all(), key=lambda x: x.name)

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

        from stalker import FilenameTemplate
        new_type_template = FilenameTemplate(**kwargs)

        # persist it
        from stalker.db.session import DBSession
        DBSession.add(new_type_template)
        DBSession.commit()

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

        assert new_type_template_db.created_by == created_by
        assert new_type_template_db.date_created == date_created
        assert new_type_template_db.date_updated == date_updated
        assert new_type_template_db.description == description
        assert new_type_template_db.filename == filename
        assert new_type_template_db.name == name
        assert new_type_template_db.nice_name == nice_name
        assert new_type_template_db.notes == notes
        assert new_type_template_db.path == path
        assert new_type_template_db.tags == tags
        assert new_type_template_db.target_entity_type == target_entity_type
        assert new_type_template_db.updated_by == updated_by
        assert new_type_template_db.type == type_

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
        from stalker import ImageFormat
        im_format = ImageFormat(**kwargs)

        # persist it
        from stalker.db.session import DBSession
        DBSession.add(im_format)
        DBSession.commit()

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
        assert im_format_db.created_by == created_by
        assert im_format_db.date_created == date_created
        assert im_format_db.date_updated == date_updated
        assert im_format_db.description == description
        assert im_format_db.device_aspect == device_aspect
        assert im_format_db.height == height
        assert im_format_db.name == name
        assert im_format_db.nice_name == nice_name
        assert im_format_db.notes == notes
        assert im_format_db.pixel_aspect == pixel_aspect
        assert im_format_db.print_resolution == print_resolution
        assert im_format_db.tags == tags
        assert im_format_db.updated_by == updated_by
        assert im_format_db.width == width

    def test_persistence_of_Link(self):
        """testing the persistence of Link
        """
        # user
        from stalker import User
        user1 = User(
            name='Test User 1',
            login='tu1',
            email='test@users.com',
            password='secret'
        )
        from stalker.db.session import DBSession
        DBSession.add(user1)
        DBSession.commit()
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
        DBSession.add_all([sound_link_type, link1])
        DBSession.commit()

        # use it as a task reference
        from stalker import Repository, Project, Task
        repo1 = Repository(name='test repo', code='TR')

        project1 = Project(
            name='Test Project 1',
            code='TP1',
            repository=repo1
        )

        task1 = Task(
            name='Test Task',
            project=project1,
            responsible=[user1]
        )
        task1.references.append(link1)

        DBSession.add(task1)
        DBSession.commit()

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

        assert link1_db.created_by == created_by
        assert link1_db.date_created == date_created
        assert link1_db.date_updated == date_updated
        assert link1_db.description == description
        assert link1_db.name == name
        assert link1_db.nice_name == nice_name
        assert link1_db.notes == notes
        assert link1_db.full_path == full_path
        assert link1_db.tags == tags
        assert link1_db.type == type_
        assert link1_db.updated_by == updated_by
        assert link1_db == task1.references[0]

        # delete tests
        task1.references.remove(link1_db)

        # Deleting a Link should not delete anything else
        DBSession.delete(link1_db)
        DBSession.commit()

        # We still should have the user and the type intact
        assert User.query.get(user1.id) is not None
        assert user1 == User.query.get(user1.id)

        assert Type.query.get(type_.id) is not None
        assert Type.query.get(type_.id) == type_

        # The task should stay
        assert Task.query.get(task1.id) is not None
        assert Task.query.get(task1.id) == task1

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

        from stalker import Note, Entity
        test_note = Note(**note_kwargs)

        # create an entity
        entity_kwargs = {
            "name": "Entity with Note",
            "description": "This Entity is created for testing purposes",
            "notes": [test_note],
        }

        test_entity = Entity(**entity_kwargs)

        from stalker.db.session import DBSession
        DBSession.add_all([test_entity, test_note])
        DBSession.commit()

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

        assert test_note_db.content == content
        assert test_note_db.created_by == created_by
        assert test_note_db.date_created == date_created
        assert test_note_db.date_updated == date_updated
        assert test_note_db.description == description
        assert test_note_db.name == name
        assert test_note_db.nice_name == nice_name
        assert test_note_db.updated_by == updated_by

    def test_persistence_of_Good(self):
        """testing hte persistence of Good
        """
        from stalker import Good
        g1 = Good(
            name='Test Good 1',
            cost=10,
            msrp=100,
            unit='TRY'
        )

        from stalker.db.session import DBSession
        DBSession.add(g1)
        DBSession.commit()

        name = g1.name
        cost = g1.cost
        msrp = g1.msrp
        unit = g1.unit

        del g1

        g1_db = Good.query.first()

        assert g1_db.name == name
        assert g1_db.cost == cost
        assert g1_db.msrp == msrp
        assert g1_db.unit == unit

        # attach a client
        from stalker.models.client import Client
        client = Client(name='Test Client')
        DBSession.add(client)

        g1_db.client = client
        DBSession.commit()
        del g1_db

        g1_db2 = Good.query.first()
        assert g1_db2.client == client

        # Delete the good
        DBSession.delete(g1_db2)
        DBSession.commit()

        # except the client still exist
        client_db = Client.query.filter(Client.name == 'Test Client').first()

        assert client_db is not None

    def test_persistence_of_Group(self):
        """testing the persistence of Group
        """
        from stalker import Group, User

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

        from stalker.db.session import DBSession
        DBSession.add(group1)
        DBSession.commit()

        name = group1.name
        users = group1.users

        del group1
        group_db = Group.query.filter_by(name=name).first()

        assert group_db.name == name
        assert group_db.users == users

    def test_persistence_of_PriceList(self):
        """testing the persistence of PriceList
        """
        from stalker import Good, PriceList
        g1 = Good(name='Test Good 1')
        g2 = Good(name='Test Good 2')
        g3 = Good(name='Test Good 3')

        p = PriceList(
            name='Test Price List',
            goods=[g1, g2, g3]
        )

        from stalker.db.session import DBSession
        DBSession.add_all([p, g1, g2, g3])
        DBSession.commit()

        del p

        p_db = PriceList.query.first()

        assert p_db.name == 'Test Price List'
        assert p_db.goods == [g1, g2, g3]

        DBSession.delete(p_db)
        DBSession.commit()

        # we should still have goods
        assert g1 is not None
        assert g2 is not None
        assert g3 is not None

        g1_db = Good.query.filter_by(name='Test Good 1').first()
        assert g1_db is not None
        assert g1_db.name == 'Test Good 1'

        g2_db = Good.query.filter_by(name='Test Good 2').first()
        assert g2_db is not None
        assert g2_db.name == 'Test Good 2'

        g3_db = Good.query.filter_by(name='Test Good 3').first()
        assert g3_db is not None
        assert g3_db.name == 'Test Good 3'

    def test_persistence_of_Project(self):
        """testing the persistence of Project
        """
        # create mock objects
        import datetime
        import pytz
        start = datetime.datetime(2016, 11, 17, tzinfo=pytz.utc) + \
            datetime.timedelta(10)
        end = start + datetime.timedelta(days=20)

        from stalker import User
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
            code='CR',
            linux_path="/mnt/M/Projects",
            windows_path="M:/Projects",
            osx_path="/mnt/M/Projects"
        )

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

        from stalker.db.session import DBSession
        DBSession.save([lead, ref1, ref2])

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
            'status': 0,
            'references': [ref1, ref2],
            'working_hours': working_hours
        }

        new_project = Project(**kwargs)

        # persist it in the database
        DBSession.add(new_project)
        DBSession.commit()

        from stalker import Task
        task1 = Task(
            name="task1",
            status=0,
            project=new_project,
            resources=[user1, user2],
            responsible=[user1]
        )

        task2 = Task(
            name="task2",
            status=0,
            project=new_project,
            resources=[user3],
            responsible=[user1]
        )
        dt = datetime.datetime
        td = datetime.timedelta
        new_project._computed_start = dt.now(pytz.utc)
        new_project._computed_end = dt.now(pytz.utc) + td(10)

        DBSession.add_all([task1, task2])
        DBSession.commit()

        # add tickets
        from stalker import Ticket
        ticket1 = Ticket(
            project=new_project
        )
        DBSession.add(ticket1)
        DBSession.commit()

        # create dailies
        from stalker import Daily
        d1 = Daily(name='Daily1', project=new_project)
        d2 = Daily(name='Daily2', project=new_project)
        d3 = Daily(name='Daily3', project=new_project)
        DBSession.add_all([d1, d2, d3])
        DBSession.commit()

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
        new_project_db = DBSession.query(Project). \
            filter_by(name=kwargs["name"]).first()

        assert isinstance(new_project_db, Project)

        assert new_project_db.assets == assets
        assert new_project_db.code == code
        assert new_project_db.computed_start == computed_start
        assert new_project_db.computed_end == computed_end
        assert new_project_db.created_by == created_by
        assert new_project_db.date_created == date_created
        assert new_project_db.date_updated == date_updated
        assert new_project_db.description == description
        assert new_project_db.end == end
        assert new_project_db.duration == duration
        assert new_project_db.fps == fps
        assert new_project_db.image_format == image_format
        assert new_project_db.is_stereoscopic == is_stereoscopic
        assert new_project_db.name == name
        assert new_project_db.nice_name == nice_name
        assert new_project_db.notes == notes
        assert new_project_db.references == references
        assert new_project_db.repositories == repositories
        assert new_project_db.sequences == sequences
        assert new_project_db.start == start
        assert new_project_db.status == status
        assert new_project_db.status_list == status_list
        assert new_project_db.structure == structure
        assert new_project_db.tags == tags
        assert new_project_db.tasks == tasks
        assert new_project_db.type == type_
        assert new_project_db.updated_by == updated_by
        assert new_project_db.users == users

        # delete tests
        # now delete the project and expect the following also to be deleted
        #
        # Tasks
        # Tickets
        DBSession.delete(new_project_db)
        DBSession.commit()

        # Tasks
        assert Task.query.all() == []

        # Tickets
        assert Ticket.query.all() == []

        # Dailies
        assert Daily.query.all() == []

    def test_persistence_of_Repository(self):
        """testing the persistence of Repository
        """
        # create a new Repository object and try to read it back
        kwargs = {
            "name": "Movie-Repo",
            "code": "MR",
            "description": "test repository",
            "linux_path": "/mnt/M",
            "osx_path": "/mnt/M",
            "windows_path": "M:/"
        }

        # create the repository object
        from stalker import Repository
        repo = Repository(**kwargs)

        # save it to database
        from stalker.db.session import DBSession
        DBSession.add(repo)
        DBSession.commit()

        # store attributes
        created_by = repo.created_by
        code = repo.code
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

        assert repo_db.created_by == created_by
        assert repo_db.code == code
        assert repo_db.date_created == date_created
        assert repo_db.date_updated == date_updated
        assert repo_db.description == description
        assert repo_db.linux_path == linux_path
        assert repo_db.name == name
        assert repo_db.nice_name == nice_name
        assert repo_db.notes == notes
        assert repo_db.osx_path == osx_path
        assert repo_db.path == path
        assert repo_db.tags == tags
        assert repo_db.updated_by == updated_by
        assert repo_db.windows_path == windows_path

    def test_persistence_of_Scene(self):
        """testing the persistence of Scene
        """
        from stalker import Repository, User, Type, Project
        repo1 = Repository(
            name="Commercial Repository",
            code='CR',
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
            type=commercial_project_type,
            repository=repo1,
        )
        from stalker.db.session import DBSession
        DBSession.add(test_project1)
        DBSession.commit()

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
            responsible=[user1]
        )
        shot2 = Shot(
            code='SH002',
            project=test_project1,
            scenes=[test_scene],
            responsible=[user1]
        )
        shot3 = Shot(
            code='SH003',
            project=test_project1,
            scenes=[test_scene],
            responsible=[user1]
        )
        DBSession.add_all([shot1, shot2, shot3])
        DBSession.add(test_scene)
        DBSession.commit()

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

        assert test_scene_db.code == code
        assert test_scene_db.created_by == created_by
        assert test_scene_db.date_created == date_created
        assert test_scene_db.date_updated == date_updated
        assert test_scene_db.description == description
        assert test_scene_db.name == name
        assert test_scene_db.nice_name == nice_name
        assert test_scene_db.notes == notes
        assert test_scene_db.project == project
        assert test_scene_db.shots == shots
        assert test_scene_db.tags == tags
        assert test_scene_db.updated_by == updated_by

    def test_persistence_of_Sequence(self):
        """testing the persistence of Sequence
        """
        from stalker import Project, Repository, Type, User
        repo1 = Repository(
            name="Commercial Repository",
            code='CR'
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
            type=commercial_project_type,
            repository=repo1,
        )
        from stalker.db.session import DBSession
        DBSession.add(test_project1)
        DBSession.commit()

        kwargs = {
            'name': 'Test Sequence',
            'code': 'TS',
            'description': 'this is a test sequence',
            'project': test_project1,
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
            responsible=[lead]
        )
        shot2 = Shot(
            code='SH002',
            project=test_project1,
            sequences=[test_sequence],
            responsible=[lead]
        )
        shot3 = Shot(
            code='SH003',
            project=test_project1,
            sequence=test_sequence,
            responsible=[lead]
        )

        DBSession.add_all([shot1, shot2, shot3])
        DBSession.add(test_sequence)
        DBSession.commit()

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

        assert test_sequence_db.code == code
        assert test_sequence_db.created_by == created_by
        assert test_sequence_db.date_created == date_created
        assert test_sequence_db.date_updated == date_updated
        assert test_sequence_db.description == description
        assert test_sequence_db.end == end
        assert test_sequence_db.name == name
        assert test_sequence_db.nice_name == nice_name
        assert test_sequence_db.notes == notes
        assert test_sequence_db.project == project
        assert test_sequence_db.references == references
        assert test_sequence_db.shots == shots
        assert test_sequence_db.start == start
        assert test_sequence_db.status == status
        assert test_sequence_db.status_list == status_list
        assert test_sequence_db.tags == tags
        assert test_sequence_db.children == children
        assert test_sequence_db.tasks == tasks
        assert test_sequence_db.updated_by == updated_by
        assert test_sequence_db.schedule_model == schedule_model
        assert test_sequence_db.schedule_timing == schedule_timing
        assert test_sequence_db.schedule_unit == schedule_unit

    def test_persistence_of_Shot(self):
        """testing the persistence of Shot
        """
        from stalker import Project, Type, Repository, User

        commercial_project_type = Type(
            name='Commercial Project',
            code='commproj',
            target_entity_type='Project',
        )

        repo1 = Repository(
            name="Commercial Repository",
            code='CR'
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
            type=commercial_project_type,
            repository=repo1,
        )
        from stalker.db.session import DBSession
        DBSession.add(test_project1)
        DBSession.commit()

        kwargs = {
            'name': "Test Sequence 1",
            'code': 'tseq1',
            'description': 'this is a test sequence',
            'project': test_project1,
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
            'responsible': [lead]
        }

        test_shot = Shot(**shot_kwargs)

        DBSession.save([test_shot, test_seq1])

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

        assert test_shot_db.code == code
        assert test_shot_db.children == children
        assert test_shot_db.cut_duration == cut_duration
        assert test_shot_db.cut_in == cut_in
        assert test_shot_db.cut_out == cut_out
        assert test_shot_db.date_created == date_created
        assert test_shot_db.date_updated == date_updated
        assert test_shot_db.description == description
        assert test_shot_db.name == name
        assert test_shot_db.nice_name == nice_name
        assert test_shot_db.notes == notes
        assert test_shot_db.references == references
        assert test_shot_db.scenes == scenes
        assert test_shot_db.sequences == sequences
        assert test_shot_db.status == status
        assert test_shot_db.status_list == status_list
        assert test_shot_db.tags == tags
        assert test_shot_db.tasks == tasks
        assert test_shot_db.updated_by == updated_by
        assert test_shot_db.fps == fps

    def test_persistence_of_SimpleEntity(self):
        """testing the persistence of SimpleEntity
        """
        import json
        from stalker import SimpleEntity, Link
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
        from stalker.db.session import DBSession
        DBSession.add(test_simple_entity)
        DBSession.commit()

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

        assert test_simple_entity_db.created_by == created_by
        assert test_simple_entity_db.date_created == date_created
        assert test_simple_entity_db.date_updated == date_updated
        assert test_simple_entity_db.description == description
        assert test_simple_entity_db.name == name
        assert test_simple_entity_db.nice_name == nice_name
        assert test_simple_entity_db.updated_by == updated_by
        assert test_simple_entity_db.html_style == html_style
        assert test_simple_entity_db.html_class == html_class
        assert test_simple_entity_db.__stalker_version__ == __stalker_version__
        assert thumbnail is not None
        assert test_simple_entity_db.thumbnail == thumbnail
        assert generic_text is not None
        assert test_simple_entity_db.generic_text == generic_text

    def test_persistence_of_Status(self):
        """testing the persistence of Status
        """
        # the status
        kwargs = {
            "name": "TestStatus_test_creating_Status",
            "description": "this is for testing purposes",
            "code": "TSTST"
        }

        from stalker import Status
        test_status = Status(**kwargs)

        # persist it to the database
        from stalker.db.session import DBSession
        DBSession.add(test_status)
        DBSession.commit()

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
        assert test_status_db.code == code
        assert test_status_db.created_by == created_by
        assert test_status_db.date_created == date_created
        assert test_status_db.date_updated == date_updated
        assert test_status_db.description == description
        assert test_status_db.name == name
        assert test_status_db.nice_name == nice_name
        assert test_status_db.notes == notes
        assert test_status_db.tags == tags
        assert test_status_db.updated_by == updated_by

    def test_persistence_of_StatusList(self):
        """testing the persistence of StatusList
        """
        # create a couple of statuses
        from stalker import Status, StatusList
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

        from stalker.db.session import DBSession
        DBSession.add(sequence_status_list)
        DBSession.commit()

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

        assert sequence_status_list_db.created_by == created_by
        assert sequence_status_list_db.date_created == date_created
        assert sequence_status_list_db.date_updated == date_updated
        assert sequence_status_list_db.description == description
        assert sequence_status_list_db.name == name
        assert sequence_status_list_db.nice_name == nice_name
        assert sequence_status_list_db.notes == notes
        assert sequence_status_list_db.statuses == statuses
        assert sequence_status_list_db.tags == tags
        assert sequence_status_list_db.target_entity_type == target_entity_type
        assert sequence_status_list_db.updated_by == updated_by

        # try to create another StatusList for the same target_entity_type
        # and do not expect an IntegrityError unless it is committed.

        kwargs["name"] = "new Sequence Status List"
        new_sequence_list = StatusList(**kwargs)

        DBSession.add(new_sequence_list)
        assert new_sequence_list in DBSession

        from sqlalchemy.exc import IntegrityError
        with pytest.raises(IntegrityError) as cm:
            DBSession.commit()

        assert '(psycopg2.errors.UniqueViolation) duplicate key value ' \
               'violates unique constraint ' \
               '"StatusLists_target_entity_type_key"' in str(cm.value)

        # roll it back
        DBSession.rollback()

    def test_persistence_of_Structure(self):
        """testing the persistence of Structure
        """
        from stalker import Type
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

        from stalker.db.session import DBSession
        DBSession.add_all([
            new_structure, modeling_task_type, animation_task_type,
            char_asset_type, image_link_type
        ])
        DBSession.commit()

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

        assert new_structure_db.templates == templates
        assert new_structure_db.created_by == created_by
        assert new_structure_db.date_created == date_created
        assert new_structure_db.date_updated == date_updated
        assert new_structure_db.description == description
        assert new_structure_db.name == name
        assert new_structure_db.nice_name == nice_name
        assert new_structure_db.notes == notes
        assert new_structure_db.custom_template == custom_template
        assert new_structure_db.tags == tags
        assert new_structure_db.updated_by == updated_by

    def test_persistence_of_Studio(self):
        """testing the persistence of Studio
        """
        from stalker import Studio
        from stalker.db.session import DBSession
        test_studio = Studio(name='Test Studio')
        DBSession.add(test_studio)
        DBSession.commit()

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

        assert test_studio_db.name == name
        assert test_studio_db.daily_working_hours == daily_working_hours
        assert test_studio_db.timing_resolution == timing_resolution
        assert test_studio_db.working_hours == working_hours

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

        from stalker import Tag
        tag = Tag(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated)

        # persist it to the database
        from stalker.db.session import DBSession
        DBSession.add(tag)
        DBSession.commit()

        # store the attributes
        description = tag.description
        created_by = tag.created_by
        updated_by = tag.updated_by
        date_created = tag.date_created
        date_updated = tag.date_updated

        # delete the aTag
        del tag

        # now try to retrieve it
        tag_db = DBSession.query(Tag).filter_by(name=name).first()

        assert (isinstance(tag_db, Tag))

        assert tag_db.name == name
        assert tag_db.description == description
        assert tag_db.created_by == created_by
        assert tag_db.updated_by == updated_by
        assert tag_db.date_created == date_created
        assert tag_db.date_updated == date_updated

    def test_persistence_of_Task(self):
        """testing the persistence of Task
        """
        # create a task
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

        from stalker import Repository, Project
        repo = Repository(
            name='Test Repo',
            code='TR',
            linux_path='/mnt/M/JOBs',
            windows_path='M:/JOBs',
            osx_path='/Users/Shared/Servers/M',
        )

        project1 = Project(
            name='Tests Project',
            code='tp',
            repository=repo,
        )
        from stalker.db.session import DBSession
        DBSession.add(project1)
        DBSession.commit()

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
        DBSession.add_all([asset1, task1, child_task1, child_task2, task2])
        DBSession.commit()

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
        DBSession.add(version1)
        DBSession.commit()

        version2 = Version(
            task=task1
        )
        DBSession.add(version2)
        DBSession.commit()

        version3 = Version(
            task=task2
        )
        DBSession.add(version3)
        DBSession.commit()

        version4 = Version(
            task=task2
        )
        DBSession.add(version4)
        DBSession.commit()

        version3.inputs = [version2]
        version2.inputs = [version1]
        version2.inputs = [version4]
        DBSession.add(version1)
        DBSession.commit()

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

        DBSession.add_all([
            task1, child_task1, child_task2, task2, time_log1,
            time_log2, time_log3, user1, user2, version1, version2, version3,
            version4, ref1, ref2
        ])
        DBSession.commit()

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

        assert task1_db.time_logs == time_logs
        assert task1_db.created_by == created_by
        assert task1_db.computed_start == computed_start
        assert task1_db.computed_end == computed_end
        assert task1_db.date_created == date_created
        assert task1_db.date_updated == date_updated
        assert task1_db.duration == duration
        assert task1_db.end == end
        assert task1_db.is_milestone == is_milestone
        assert task1_db.name == name
        assert task1_db.parent == parent
        assert task1_db.priority == priority
        assert resources == []  # it is a parent task, no child
        assert task1_db.resources == resources
        assert task1_db.start == start
        assert task1_db.status == status
        assert task1_db.status_list == status_list
        assert task1_db.tags == tags
        assert \
            sorted(tasks, key=lambda x: x.name) == \
            sorted(task1_db.tasks, key=lambda x: x.name)
        assert [child_task1, child_task2] == tasks
        assert task1_db.type == type_
        assert task1_db.updated_by == updated_by
        assert task1_db.versions == versions
        assert task1_db.watchers == watchers
        assert task1_db.schedule_model == schedule_model
        assert task1_db.schedule_timing == schedule_timing
        assert task1_db.schedule_unit == schedule_unit
        assert version2.inputs == [version4]
        assert version3.inputs == [version2]
        assert version4.inputs == []

        # delete tests

        # deleting a Task should also delete:
        #
        # Child Tasks
        # TimeLogs
        # Versions
        # And orphan-references
        #
        # task1_db.references = []
        # with DBSession.no_autoflush:
        #     for v in task1_db.versions:
        #         v.inputs = []
        #         for tv in Version.query.filter(Version.inputs.contains(v)):
        #             tv.inputs.remove(v)

        DBSession.delete(task1_db)
        DBSession.commit()

        # we still should have the versions that are in the inputs (version3
        # and version4) of the original versions (version1, version2)
        assert Version.query.get(version3.id) is not None
        assert Version.query.get(version4.id) is not None

        # Expect to have all child tasks also to be deleted
        assert \
            sorted([asset1, task2], key=lambda x: x.name) == \
            sorted(Task.query.all(), key=lambda x: x.name)

        # Expect to have time logs related to this task are deleted
        assert TimeLog.query.all() == [time_log3]

        # We still should have the users intact
        admin = User.query.filter_by(name='admin').first()
        assert \
            sorted([user1, user2, user3, admin], key=lambda x: x.name) == \
            sorted(User.query.all(), key=lambda x: x.name)

        # When updating the test to include deletion, the test task became a
        # parent task, so all the resources are removed, thus the resource
        # attribute should be tested separately.
        resources = task2.resources
        id_ = task2.id
        del task2

        another_task_db = Task.query.get(id_)
        assert resources == [user1]
        assert another_task_db.resources == resources

        assert version3.inputs == []
        assert version4.inputs == []

    def test_persistence_of_Review(self):
        """testing the persistence of Review
        """
        # create a task
        from stalker import Repository
        repo = Repository(
            name='Test Repo',
            code='TR',
            linux_path='/some/random/path',
            windows_path='/some/random/path',
            osx_path='/some/random/path',
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
            schedule_timing=5,
            schedule_unit='h',
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

        from stalker.db.session import DBSession
        DBSession.add_all([
            task1, child_task1, child_task2, task2, time_log1,
            time_log2, time_log3, user1, user2, rev1
        ])
        DBSession.commit()

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

        assert rev1_db.created_by == created_by
        assert rev1_db.date_created == date_created
        assert rev1_db.date_updated == date_updated
        assert rev1_db.name == name
        assert rev1_db.task == task
        assert rev1_db.updated_by == updated_by
        assert rev1_db.schedule_timing == schedule_timing
        assert rev1_db.schedule_unit == schedule_unit

        # delete tests

        # deleting a Review should be fairly simple:
        DBSession.delete(rev1_db)
        DBSession.commit()

        # Expect to have no task is deleted
        assert \
            sorted(
                [asset1, task1, task2, child_task1, child_task2],
                key=lambda x: x.name
            ) == \
            sorted(Task.query.all(), key=lambda x: x.name)

    def test_persistence_of_Ticket(self):
        """testing the persistence of Ticket
        """
        from stalker import Repository
        repo = Repository(
            name='Test Repository',
            code='TR'
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

        from stalker import Ticket
        from stalker.db.session import DBSession
        related_ticket1 = Ticket(project=proj1)
        DBSession.add(related_ticket1)
        DBSession.commit()

        related_ticket2 = Ticket(project=proj1)
        DBSession.add(related_ticket2)
        DBSession.commit()

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

        DBSession.add(test_ticket)
        DBSession.commit()

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

        assert comments == test_ticket_db.comments
        assert created_by == test_ticket_db.created_by
        assert date_created == test_ticket_db.date_created
        assert date_updated == test_ticket_db.date_updated
        assert description == test_ticket_db.description
        assert logs != []
        assert logs == test_ticket_db.logs
        assert links == test_ticket_db.links
        assert name == test_ticket_db.name
        assert notes == test_ticket_db.notes
        assert number == test_ticket_db.number
        assert owner == test_ticket_db.owner
        assert priority == test_ticket_db.priority
        assert project == test_ticket_db.project
        assert related_tickets == test_ticket_db.related_tickets
        assert reported_by == test_ticket_db.reported_by
        assert resolution == test_ticket_db.resolution
        assert status == test_ticket_db.status
        assert type_ == test_ticket_db.type
        assert updated_by == test_ticket_db.updated_by

        # delete tests
        # Deleting a Ticket should also delete all the logs related to the
        # ticket
        assert \
            sorted(test_ticket_db.logs, key=lambda x: x.name) == \
            sorted(logs, key=lambda x: x.name)

        DBSession.delete(test_ticket_db)
        DBSession.commit()

        from stalker import TicketLog
        assert TicketLog.query.all() == []

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

        from stalker import User
        from stalker.db.session import DBSession

        user1 = User(**user_kwargs)

        DBSession.add_all([user1, new_department])
        DBSession.commit()

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
        DBSession.add(user1)
        DBSession.commit()

        # create a test project
        from stalker import Repository
        repo1 = Repository(name='Test Repo', code='TR')
        from stalker import Project, Task, TimeLog
        project1 = Project(
            name='Test Project',
            code='TP',
            repository=repo1,
        )
        task1 = Task(
            name='Test Task 1',
            project=project1,
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
        DBSession.add(time_log1)
        DBSession.add(task1)
        DBSession.commit()

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
        #assert new_user, new_user_DB)
        assert user1_db.created_by == created_by
        assert user1_db.date_created == date_created
        assert user1_db.date_updated == date_updated
        assert user1_db.departments == departments
        assert user1_db.description == description
        assert user1_db.efficiency == efficiency
        assert user1_db.email == email
        assert user1_db.authentication_logs == authentication_logs
        assert user1_db.login == login
        assert user1_db.name == name
        assert user1_db.nice_name == nice_name
        assert user1_db.notes == notes
        assert user1_db.password == password
        assert user1_db.groups == groups
        assert user1_db.projects == projects
        assert user1_db.tags == tags
        assert user1_db.tasks == tasks
        assert \
            sorted(vacations, key=lambda x: x.name) == \
            sorted(user1_db.vacations, key=lambda x: x.name)
        assert user1_db.watching == watching
        assert user1_db.updated_by == updated_by

        # as the member of a department
        department_db = Department.query\
            .filter(Department.name == dep_kwargs["name"]) \
            .first()

        assert user1_db == department_db.users[0]

        # delete tests
        assert \
            sorted([vacation1, vacation2], key=lambda x: x.name) == \
            sorted(Vacation.query.all(), key=lambda x: x.name)

        # deleting a user should also delete its vacations
        DBSession.delete(user1_db)
        DBSession.commit()

        assert Vacation.query.all() == []

        # deleting a user should also delete the time logs
        assert TimeLog.query.all() == []

    def test_persistence_of_AuthenticationLog(self):
        """testing the persistence of AuthenticationLog
        """
        import datetime
        import pytz
        from stalker import User, AuthenticationLog
        from stalker.db.session import DBSession
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='sosecret'
        )
        DBSession.add(user1)
        DBSession.commit()

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

        DBSession.add_all([al1, al2])
        DBSession.commit()

        al1_id = al1.id
        action = al1.action
        date = al1.date

        del al1

        al1_from_db = AuthenticationLog.query.get(al1_id)

        assert al1_from_db.user == user1
        assert al1_from_db.date == date
        assert al1_from_db.action == action

        # check if users data is also updated
        assert \
            sorted(user1.authentication_logs) == sorted([al1_from_db, al2])

        # delete tests
        DBSession.delete(al1_from_db)
        DBSession.commit()

        # check the user still exists
        user1_from_db = User.query.get(user1.id)
        assert user1_from_db is not None

        # check if the other log is still there
        al2_from_db = AuthenticationLog.query.get(al2.id)
        assert al2_from_db is not None

        # delete the other AuhenticationLog
        DBSession.delete(al2_from_db)
        DBSession.commit()

        # check if the user is still there
        user1_from_db = User.query.get(user1.id)
        assert user1_from_db is not None

    def test_persistence_of_Vacation(self):
        """testing the persistence of Vacation instances
        """
        # create a User
        from stalker import User, Type, Vacation
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

        from stalker.db.session import DBSession
        DBSession.add(vacation)
        DBSession.commit()

        name = vacation.name

        del vacation

        # get it back
        vacation_db = Vacation.query.filter_by(name=name).first()

        assert isinstance(vacation_db, Vacation)
        assert vacation_db.user == new_user
        assert vacation_db.start == start
        assert vacation_db.end == end
        assert vacation_db.type == personal_vacation

    def test_persistence_of_Version(self):
        """testing the persistence of Version instances
        """
        # create a project
        from stalker import Project, Repository
        test_project = Project(
            name='Test Project',
            code='tp',
            repository=Repository(
                name='Film Projects',
                code='FP',
                windows_path='M:/',
                linux_path='/mnt/M/',
                osx_path='/Users/Volumes/M/',
            )
        )
        from stalker.db.session import DBSession
        DBSession.add(test_project)

        # create a task
        from stalker import Task, User
        test_task = Task(
            name='Modeling',
            project=test_project,
            responsible=[
                User(name='user1', login='user1', email='u@u', password='12')
            ]
        )
        DBSession.add(test_task)
        DBSession.commit()

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
        from stalker.db.session import DBSession
        DBSession.add(test_version)
        DBSession.commit()

        # create a new version
        test_version_2 = Version(
            name='version for task modeling',
            task=test_task,
            take='MAIN',
            full_path='M:/Shows/Proj1/Seq1/Shots/SH001/Lighting'
            '/Proj1_Seq1_Sh001_MAIN_Lighting_v001.ma',
            inputs=[test_version]
        )
        assert test_version_2.inputs == [test_version]
        DBSession.add(test_version_2)
        DBSession.commit()

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

        assert test_version_db.created_by == created_by
        assert test_version_db.date_created == date_created
        assert test_version_db.date_updated == date_updated
        assert test_version_db.name == name
        assert test_version_db.nice_name == nice_name
        assert test_version_db.notes == notes
        assert test_version_db.outputs == outputs
        assert test_version_db.is_published == is_published
        assert test_version_db.full_path == full_path
        assert test_version_db.tags == tags
        assert test_version_db.take_name == take_name
        assert test_version_db.type == type_
        assert test_version_db.updated_by == updated_by
        assert test_version_db.version_number == version_number
        assert test_version_db.task == task

        # try to delete version and expect the task, user and other versions
        # to be intact
        DBSession.delete(test_version_db)
        DBSession.commit()

        assert test_version_2.inputs == []

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
        assert test_version_2.inputs == [test_version_3]
        DBSession.add(test_version_3)
        DBSession.commit()

        # now delete test_version_2
        DBSession.delete(test_version_2)
        DBSession.commit()

        # and check if test_version_3 is still present in the database
        test_version_3_db = Version.query\
            .filter(Version.name == test_version_3.name)\
            .filter(Version.task == test_version_3.task)\
            .filter(Version.version_number == test_version_3.version_number)\
            .first()

        assert test_version_3_db is not None
        assert test_version_3_db.task == test_version_3.task
        assert \
            test_version_3_db.version_number == test_version_3.version_number

        # create a new version append it to version_3.children and then delete
        # version_3
        test_version_4 = Version(
            name='version for task modeling',
            task=test_task,
            take='MAIN'
        )
        test_version_3.children.append(test_version_4)
        DBSession.save(test_version_4)
        assert test_version_3.children == [test_version_4]
        assert test_version_4.parent == test_version_3

        # and check if test_version_4 is still present in the database
        test_version_4_db = Version.query\
            .filter(Version.name == test_version_4.name)\
            .filter(Version.task == test_version_4.task)\
            .filter(Version.version_number == test_version_4.version_number)\
            .first()

        assert test_version_4_db is not None
        assert test_version_4_db.task == test_version_4.task
        assert test_version_4_db.version_number == \
               test_version_4.version_number
        assert test_version_4_db.parent == test_version_3

        # now delete test_version_3
        DBSession.delete(test_version_3)
        DBSession.commit()

        # and check if test_version_4 is still present in the database
        test_version_4_db = Version.query\
            .filter(Version.name == test_version_4.name)\
            .filter(Version.task == test_version_4.task)\
            .filter(Version.version_number == test_version_4.version_number)\
            .first()

        assert test_version_4_db is not None
        assert test_version_4_db.task == test_version_4.task
        assert test_version_4_db.version_number == \
               test_version_4.version_number
        assert test_version_4_db.parent is None

        # create a new version and assign it as a child of version_5
        test_version_5 = Version(
            task=test_task,
            take='MAIN'
        )
        DBSession.save(test_version_5)
        test_version_4.children = [test_version_5]
        DBSession.commit()

        # now delete test_version_5
        test_version_5_id = test_version_5.id
        DBSession.delete(test_version_5)
        DBSession.commit()

        # query it from db
        assert Version.query.get(test_version_5_id) is None
        assert test_version_4.children == []

    def test_persistence_of_WorkingHours(self):
        """testing the persistence of WorkingHours instances
        """
        from stalker import WorkingHours
        wh = WorkingHours(
            name='Default Working Hours',
            working_hours={
                'mon': [[9, 12], [13, 18]],
                'tue': [[9, 12], [13, 18]],
                'wed': [[9, 12], [13, 18]],
                'thu': [[9, 12], [13, 18]],
                'fri': [[9, 12], [13, 18]],
                'sat': [],
                'sun': [],
            },
            daily_working_hours=8
        )

        from stalker.db.session import DBSession
        DBSession.add(wh)
        DBSession.commit()

        name = wh.name
        hours = wh.working_hours
        daily_working_hours = 8

        del wh

        wh_db = WorkingHours.query.filter_by(name=name).first()

        assert wh_db.name == name
        assert wh_db.working_hours == hours
        assert wh_db.daily_working_hours == daily_working_hours


def test_timezones_with_sqlite3(setup_sqlite3):
    """testing if timezones will be correctly handled in SQLite3
    """
    from stalker import db
    db.setup()
    db.init()

    from stalker.db.session import DBSession
    from stalker import SimpleEntity

    # check if we're really using SQLite3
    assert str(DBSession.connection().engine.url) == 'sqlite://'

    # create a simple entity
    test_se_1 = SimpleEntity(name='Test Entry 1')

    # check if it has UTC as timezone
    import pytz
    assert test_se_1.date_created.tzinfo == pytz.utc

    # commit to database
    DBSession.save(test_se_1)

    # now delete the local copy and retrieve it back
    del test_se_1

    test_se_1_db = SimpleEntity.query.filter_by(name='Test Entry 1').first()

    # now check if the test_se_1_db has the local time zone in its
    # date_created field
    import tzlocal
    local_tz = tzlocal.get_localzone()
    import datetime
    now = datetime.datetime.now(local_tz)
    assert test_se_1_db.date_created.tzinfo == now.tzinfo
