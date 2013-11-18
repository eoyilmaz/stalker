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

import os
import shutil
import datetime
import unittest2
import tempfile
from sqlalchemy.exc import IntegrityError

from stalker.db.session import DBSession
from stalker import (db, defaults, Asset, Department, SimpleEntity, Entity,
                     ImageFormat, Link, Note, Project, Repository, Sequence,
                     Shot, Status, StatusList, Structure, Tag, Task, Type,
                     FilenameTemplate, User, Version, Permission, Group,
                     TimeLog, Ticket, Scene, WorkingHours, Studio, Vacation,
                     TicketLog)
import logging
from stalker import log

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


class DatabaseTester(unittest2.TestCase):
    """tests the database and connection to the database
    """

    @classmethod
    def setUpClass(cls):
        """set up the test for class
        """
        DBSession.remove()
        DBSession.configure(extension=None)

    @classmethod
    def tearDownClass(cls):
        """clean up the test
        """
        DBSession.configure(extension=None)

    def setUp(self):
        """setup the tests
        """
        # just set the default admin creation to true
        # some tests are relying on that
        defaults.auto_create_admin = True
        defaults.admin_name = "admin"
        defaults.admin_password = "admin"

        self.test_database_uri = "sqlite:///:memory:"

        self._createdDB = False

    def tearDown(self):
        """tearDown the tests
        """
        DBSession.remove()

    def test_creating_a_custom_in_memory_db(self):
        """testing if a custom in-memory sqlite database will be created
        """
        # create a database in memory
        db.setup({
            "sqlalchemy.url": "sqlite:///:memory:",
            "sqlalchemy.echo": False,
        })

        # try to persist a user and get it back
        # create a new user
        kwargs = {
            "name": "Erkan Ozgur Yilmaz",
            "login": "eoyilmaz",
            "email": "eoyilmaz@gmail.com",
            #"created_by": admin,
            "password": "password",
        }

        new_user = User(**kwargs)
        DBSession.add(new_user)
        DBSession.commit()

        # now check if the newUser is there
        new_user_db = User.query.filter_by(name=kwargs["name"]).first()

        self.assertTrue(new_user_db is not None)

    def test_default_admin_creation(self):
        """testing if a default admin is created
        """
        # set default admin creation to True
        defaults.auto_create_admin = True

        db.setup()
        db.init()

        # check if there is an admin
        admin_db = User.query.filter(User.name == defaults.admin_name).first()

        self.assertEqual(admin_db.name, defaults.admin_name)

    def test_default_admin_for_already_created_databases(self):
        """testing if no extra admin is going to be created for already setup
        databases
        """
        # set default admin creation to True
        defaults.auto_create_admin = True

        db.setup({
            "sqlalchemy.url": self.test_database_uri
        })
        db.init()

        # try to call the db.setup for a second time and see if there are more
        # than one admin

        db.setup({
            "sqlalchemy.url": self.test_database_uri
        })
        db.init()

        self._createdDB = True

        # and get how many admin is created, (it is imipossible to create
        # second one because the tables.simpleEntity.c.nam.unique=True

        admins = User.query.filter_by(name=defaults.admin_name).all()

        self.assertTrue(len(admins) == 1)

    def test_no_default_admin_creation(self):
        """testing if there is no user if stalker.config.Conf.auto_create_admin
        is False
        """
        # turn down auto admin creation
        defaults.auto_create_admin = False

        # setup the db
        db.setup()
        db.init()

        # check if there is a use with name admin
        self.assertTrue(
            User.query.filter_by(name=defaults.admin_name).first()
            is None
        )

        # check if there is a admins department
        self.assertTrue(
            Department.query
            .filter_by(name=defaults.admin_department_name)
            .first() is None
        )

    def test_non_unique_names_on_different_entity_type(self):
        """testing if there can be non-unique names for different entity types
        """
        db.setup()

        # try to create a user and an entity with same name
        # expect Nothing
        kwargs = {
            "name": "user1",
            #"created_by": admin
        }

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

        user1 = User(**kwargs)
        DBSession.add(user1)

        # expect nothing, this should work without any error
        DBSession.commit()

    def test_ticket_status_initialization(self):
        """testing if the ticket statuses are correctly created
        """
        db.setup()
        db.init()

        #ticket_statuses = Status.query.all()
        ticket_status_list = StatusList.query \
            .filter(StatusList.name == 'Ticket Statuses') \
            .first()

        self.assertTrue(isinstance(ticket_status_list, StatusList))

        expected_status_names = ['New', 'Reopened', 'Closed', 'Accepted',
                                 'Assigned']
        self.assertEqual(len(ticket_status_list.statuses),
                         len(expected_status_names))
        for status in ticket_status_list.statuses:
            self.assertTrue(status.name in expected_status_names)

    def test_register_creates_suitable_Permissions(self):
        """testing if stalker.db.register is able to create suitable
        Permissions
        """
        db.setup()

        # create a new dummy class
        class TestClass(object):
            pass

        db.register(TestClass)

        # now check if the TestClass entry is created in Permission table

        permissions_db = Permission.query \
            .filter(Permission.class_name == 'TestClass') \
            .all()

        logger.debug("%s" % permissions_db)

        actions = defaults.actions

        for action in permissions_db:
            self.assertTrue(action.action in actions)

    def test_register_raise_TypeError_for_wrong_class_name_argument(self):
        """testing if a TypeError will be raised if the class_name argument is
        not an instance of type or str or unicode
        """
        db.setup()
        self.assertRaises(TypeError, db.register, 23425)

    def test_permissions_created_for_all_the_classes(self):
        """testing if Permission instances are created for classes in the SOM
        """
        DBSession.remove()
        DBSession.configure(extension=None)
        db.setup()
        db.init()

        class_names = [
            'Asset', 'Group', 'Permission', 'User', 'Department',
            'SimpleEntity', 'Entity', 'ImageFormat', 'Link', 'Message', 'Note',
            'Project', 'Repository', 'Scene', 'Sequence', 'Shot', 'Status',
            'StatusList', 'Structure', 'Studio', 'Tag', 'TimeLog', 'Task',
            'FilenameTemplate', 'Ticket', 'TicketLog', 'Type', 'Vacation',
            'Version',
        ]

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
        # create the environment variable and point it to a temp directory
        temp_db_path = tempfile.mkdtemp()
        temp_db_filename = 'stalker.db'
        temp_db_full_path = os.path.join(temp_db_path, temp_db_filename)

        temp_db_url = 'sqlite:///' + temp_db_full_path

        DBSession.remove()
        db.setup(settings={'sqlalchemy.url': temp_db_url})
        db.init()

        # this should not give any error
        DBSession.remove()
        db.setup(settings={'sqlalchemy.url': temp_db_url})
        db.init()

        # and we still have correct amount of Permissions
        permissions = Permission.query.all()
        self.assertEqual(len(permissions), 290)

        # clean the test
        shutil.rmtree(temp_db_path)

    def test_ticket_statuses_are_not_created_over_and_over_again(self):
        """testing if the Ticket Statuses are created only once and trying to
        call __init_db__ will not raise any error
        """
        # create the environment variable and point it to a temp directory
        temp_db_path = tempfile.mkdtemp()
        temp_db_filename = 'stalker.db'
        temp_db_full_path = os.path.join(temp_db_path, temp_db_filename)

        temp_db_url = 'sqlite:///' + temp_db_full_path

        DBSession.remove()
        db.setup(settings={'sqlalchemy.url': temp_db_url})
        db.init()

        # this should not give any error
        # DBSession.remove()
        db.setup(settings={'sqlalchemy.url': temp_db_url})
        db.init()

        # this should not give any error
        # DBSession.remove()
        db.setup(settings={'sqlalchemy.url': temp_db_url})
        db.init()

        # and we still have correct amount of Permissions
        statuses = Status.query.all()
        self.assertEqual(len(statuses), 5)

        status_list = StatusList.query.all()
        self.assertEqual(len(status_list), 1)
        self.assertEqual(status_list[0].name, 'Ticket Statuses')
        # self.fail(temp_db_url)

        # clean the test
        shutil.rmtree(temp_db_path)


class DatabaseModelsTester(unittest2.TestCase):
    """tests the database model

    NOTE TO OTHER DEVELOPERS:

    Most of the tests in this TestCase uses parts of the system which are
    tested but probably not tested while running the individual tests.

    Incomplete isolation is against to the logic behind unit testing, every
    test should only cover a unit of the code, and a complete isolation should
    be created. But this can not be done in persistence tests (AFAIK), it needs
    to be done in this way for now. Mocks can not be used because every created
    object goes to the database, so they need to be real objects.
    """

    @classmethod
    def setUpClass(cls):
        """setup the test
        """
        # use a normal session instead of a managed one
        DBSession.remove()
        DBSession.configure(extension=None)

    @classmethod
    def tearDownClass(cls):
        """clean up the test
        """
        # delete the default test database file
        #os.remove(cls.test_db_file)
        DBSession.configure(extension=None)

    def setUp(self):
        """setup the test
        """
        # create a test database, possibly an in memory database
        self.test_db_file = ":memory:"
        self.test_db_uri = "sqlite:///" + self.test_db_file

        db.setup()
        db.init()

    def tearDown(self):
        """tearing down the test
        """
        DBSession.remove()

    def test_persistence_of_Asset(self):
        """testing the persistence of Asset
        """
        test_user = User(
            name='Test User',
            login='tu',
            email='test@user.com',
            password='secret'
        )

        asset_type = Type(
            name='A new asset type A',
            code='anata',
            target_entity_type=Asset
        )

        status1 = Status(name='On Hold A', code='OHA')
        status2 = Status(name='Completed A', code='CMPLTA')
        status3 = Status(name='Work In Progress A', code='WIPA')

        test_repository_type = Type(
            name='Test Repository Type A',
            code='trta',
            target_entity_type=Repository,
        )

        test_repository = Repository(
            name='Test Repository A',
            type=test_repository_type
        )

        project_status_list = StatusList(
            name='Project Status List A',
            statuses=[status1, status2, status3],
            target_entity_type='Project',
        )

        commercial_type = Type(
            name='Commercial A',
            code='comm',
            target_entity_type=Project
        )

        test_project = Project(
            name='Test Project For Asset Creation',
            code='TPFAC',
            status_list=project_status_list,
            type=commercial_type,
            repository=test_repository,
        )

        DBSession.add(test_project)
        DBSession.commit()

        task_status_list = StatusList(
            name='Task Status List',
            statuses=[status1, status2, status3],
            target_entity_type=Task,
        )

        asset_status_list = StatusList(
            name='Asset Status List',
            statuses=[status1, status2, status3],
            target_entity_type=Asset
        )

        kwargs = {
            'name': 'Test Asset',
            'code': 'test_asset',
            'description': 'This is a test Asset object',
            'type': asset_type,
            'project': test_project,
            'status_list': asset_status_list,
            'created_by': test_user
        }

        test_asset = Asset(**kwargs)
        # logger.debug('test_asset.project : %s' % test_asset.project)

        DBSession.add(test_asset)
        DBSession.commit()

        # logger.debug('test_asset.project (after commit): %s' %
        #              test_asset.project)

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

        #self.assertEqual(test_asset, test_asset_DB)
        self.assertEqual(code, test_asset_db.code)
        self.assertIsNotNone(test_asset_db.created_by)
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
        DBSession.delete(test_asset_db)
        DBSession.commit()

        # we should still have the user
        self.assertIsNotNone(
            User.query.filter(User.id == created_by.id).first()
        )

        # we should still have the project
        self.assertIsNotNone(
            Project.query.filter(Project.id == project.id).first()
        )

    def test_persistence_of_TimeLog(self):
        """testing the persistence of TimeLog
        """
        logger.setLevel(log.logging_level)

        description = 'this is a time log'
        start = datetime.datetime(2013, 1, 10)
        end = datetime.datetime(2013, 1, 13)

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

        stat1 = Status(
            name='Work In Progress',
            code='WIP'
        )

        stat2 = Status(
            name='Completed',
            code='CMPL'
        )

        repo = Repository(
            name='Commercials Repository',
            linux_path='/mnt/shows',
            windows_path='S:/',
            osx_path='/mnt/shows'
        )

        proj_status_list = StatusList(
            name='Project Statuses',
            statuses=[stat1, stat2],
            target_entity_type='Project'
        )

        task_status_list = StatusList(
            name='Task Statuses',
            statuses=[stat1, stat2],
            target_entity_type='Task'
        )

        projtype = Type(
            name='Commercial Project',
            code='comm',
            target_entity_type='Project'
        )

        proj1 = Project(
            name='Test Project',
            code='tp',
            type=projtype,
            status_list=proj_status_list,
            repository=repo
        )

        test_task = Task(
            name='Test Task',
            start=start,
            end=end,
            resources=[user1, user2],
            project=proj1,
            status_list=task_status_list
        )

        test_time_log = TimeLog(
            task=test_task,
            resource=user1,
            start=datetime.datetime(2013, 1, 10),
            end=datetime.datetime(2013, 1, 13),
            description=description
        )

        DBSession.add(test_time_log)
        DBSession.commit()

        tlog_id = test_time_log.id

        del test_time_log

        # now retrieve it back
        test_time_log_db = TimeLog.query.filter_by(id=tlog_id).first()

        self.assertEqual(description, test_time_log_db.description)
        self.assertEqual(start, test_time_log_db.start)
        self.assertEqual(end, test_time_log_db.end)
        self.assertEqual(user1, test_time_log_db.resource)
        self.assertEqual(test_task, test_time_log_db.task)

    def test_persistence_of_Department(self):
        """testing the persistence of Department
        """
        logger.setLevel(log.logging_level)

        name = "TestDepartment_test_persistence_Department"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        date_created = datetime.datetime.now()
        date_updated = datetime.datetime.now()

        test_dep = Department(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated
        )
        DBSession.add(test_dep)
        DBSession.commit()

        # create three users, one for lead and two for members

        # user1
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
            department=test_dep,
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
            department=test_dep,
            password="password",
        )

        # user3
        # create three users, one for lead and two for members
        user3 = User(
            name="User3 Test Persistence Department",
            login='u2tpd',
            initials='u2tpd',
            description="this is for testing purposes",
            created_by=None,
            updated_by=None,
            login_name="user3_tp_department",
            first_name="user3_first_name",
            last_name="user3_last_name",
            email="user3@department.com",
            department=test_dep,
            password="password",
        )

        # add as the members and the lead
        test_dep.lead = user1
        test_dep.members = [user1, user2, user3]

        DBSession.add(test_dep)
        DBSession.commit()

        self.assertTrue(test_dep in DBSession)

        created_by = test_dep.created_by
        date_created = test_dep.date_created
        date_updated = test_dep.date_updated
        description = test_dep.description
        lead = test_dep.lead
        members = test_dep.members
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
        self.assertEqual(lead, test_dep_db.lead)
        self.assertEqual(members, test_dep_db.members)
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
        date_created = date_updated = datetime.datetime.now()

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
        date_created = date_updated = datetime.datetime.now()

        tag2 = Tag(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated
        )

        # the note
        note1 = Note(content="content for note1")
        note2 = Note(content="content for note2")

        # the entity
        name = "TestEntity"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        date_created = date_updated = datetime.datetime.now()

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

        # persist it to the database
        DBSession.add(test_entity)
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
        test_entity_db = Entity.query.filter_by(name=name).first()

        assert (isinstance(test_entity_db, Entity))

        #self.assertEqual(test_entity, test_entity_DB)
        self.assertEqual(created_by, test_entity_db.created_by)
        self.assertEqual(date_created, test_entity_db.date_created)
        self.assertEqual(date_updated, test_entity_db.date_updated)
        self.assertEqual(description, test_entity_db.description)
        self.assertEqual(name, test_entity_db.name)
        self.assertEqual(nice_name, test_entity_db.nice_name)
        self.assertItemsEqual(notes, [note1, note2])
        self.assertEqual(notes, test_entity_db.notes)
        self.assertEqual(tags, test_entity_db.tags)
        self.assertEqual(updated_by, test_entity_db.updated_by)

        # delete tests

        # Deleting an Entity should also delete the associated notes
        DBSession.delete(test_entity_db)
        DBSession.commit()

        self.assertItemsEqual([], Note.query.all())

    def test_persistence_of_FilenameTemplate(self):
        """testing the persistence of FilenameTemplate
        """
        vers_type = Type.query.filter_by(name="Version").first()
        ref_type = Type.query.filter_by(name="Reference").first()

        # create a FilenameTemplate object for movie links
        kwargs = {
            "name": "Movie Links Template",
            "target_entity_type": Link,
            "type": ref_type,
            "description": "this is a template to be used for links to movie"
                           "files",
            "path": "REFS/{{link_type.name}}",
            "filename": "{{link.file_name}}",
            "output_path": "OUTPUT",
            "output_file_code": "{{link.file_name}}",
        }

        new_type_template = FilenameTemplate(**kwargs)
        #new_type_template2 = FilenameTemplate(**kwargs)

        # persist it
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
            #"created_by": admin,
            #"updated_by": admin,
            "width": 1920,
            "height": 1080,
            "pixel_aspect": 1.0,
            "print_resolution": 300.0
        }

        # create the ImageFormat object
        im_format = ImageFormat(**kwargs)

        # persist it
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
        #self.assertEqual(im_format, im_format_DB)
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
        user1 = User(
            name='Test User 1',
            login='tu1',
            email='test@users.com',
            password='secret'
        )
        DBSession.add(user1)
        DBSession.commit()

        # create a link Type
        sound_link_type = Type(
            name='Sound',
            code='sound',
            target_entity_type=Link
        )

        # create a Link
        kwargs = {
            'name': 'My Sound',
            'full_path': 'M:/PROJECTS/my_movie_sound.wav',
            'type': sound_link_type,
            'created_by': user1
        }

        link1 = Link(**kwargs)

        # persist it
        DBSession.add_all([sound_link_type, link1])
        DBSession.commit()

        # use it as a task reference
        repo1 = Repository(name='test repo')
        status1 = Status(name='New', code='NEW')
        status2 = Status(name='Work In Progress', code='WIP')
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
        task_statuses = StatusList(
            target_entity_type='Task',
            statuses=[status1, status2]
        )
        task1 = Task(
            name='Test Task',
            project=project1,
            status_list=task_statuses
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

        #self.assertEqual(new_link, new_link_DB)
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
        # Deleting a Link should not delete anything else
        DBSession.delete(link1_db)
        DBSession.commit()

        # We still should have the user and the type intact
        self.assertIsNotNone(User.query.get(user1.id))
        self.assertEqual(user1, User.query.get(user1.id))

        self.assertIsNotNone(Type.query.get(type_.id))
        self.assertEqual(type_, Type.query.get(type_.id))

        # The task should stay
        self.assertIsNotNone(Task.query.get(task1.id))
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

        test_note = Note(**note_kwargs)

        # create an entity
        entity_kwargs = {
            "name": "Entity with Note",
            "description": "This Entity is created for testing purposes",
            "notes": [test_note],
        }

        test_entity = Entity(**entity_kwargs)

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

        self.assertEqual(content, test_note_db.content)
        self.assertEqual(created_by, test_note_db.created_by)
        self.assertEqual(date_created, test_note_db.date_created)
        self.assertEqual(date_updated, test_note_db.date_updated)
        self.assertEqual(description, test_note_db.description)
        self.assertEqual(name, test_note_db.name)
        self.assertEqual(nice_name, test_note_db.nice_name)
        self.assertEqual(updated_by, test_note_db.updated_by)

    def test_persistence_of_Group(self):
        """testing the persistence of Group
        """

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

        DBSession.add(group1)
        DBSession.commit()

        name = group1.name
        users = group1.users

        del group1
        group_db = Group.query.filter_by(name=name).first()

        self.assertEqual(name, group_db.name)
        self.assertEqual(users, group_db.users)

    def test_persistence_of_Project(self):
        """testing the persistence of Project
        """
        # create mock objects
        start = datetime.date.today() + datetime.timedelta(10)
        end = start + datetime.timedelta(days=20)

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

        image_format = ImageFormat(
            name="HD",
            width=1920,
            height=1080
        )

        project_type = Type(
            name='Commercial Project',
            code='commproj',
            target_entity_type=Project
        )

        structure_type = Type(
            name='Commercial Structure',
            code='commstr',
            target_entity_type=Project
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

        status1 = Status(
            name="On Hold",
            code="OH"
        )

        status2 = Status(
            name="Complete",
            code="CMPLT"
        )

        project_status_list = StatusList(
            name="A Status List for testing Project",
            statuses=[status1, status2],
            target_entity_type=Project
        )

        DBSession.add(project_status_list)
        DBSession.commit()

        # create data for mixins
        # Reference Mixin
        link_type = Type(
            name='Image',
            code='image',
            target_entity_type='Link'
        )

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
        task_status_list = StatusList(
            name="Task Statuses",
            statuses=[status1, status2],
            target_entity_type=Task
        )

        DBSession.add(task_status_list)
        DBSession.add_all([ref1, ref2])
        DBSession.commit()

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
            'lead': lead,
            'image_format': image_format,
            'fps': 25,
            'type': project_type,
            'structure': project_structure,
            'repository': repo,
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
        DBSession.add(new_project)
        DBSession.commit()

        task1 = Task(
            name="task1",
            status_list=task_status_list,
            status=0,
            project=new_project,
            resources=[user1, user2]
        )

        task2 = Task(
            name="task2",
            status_list=task_status_list,
            status=0,
            project=new_project,
            resources=[user3]
        )

        dt = datetime.datetime
        td = datetime.timedelta
        new_project._computed_start = dt.now()
        new_project._computed_end = dt.now() + td(10)

        DBSession.add_all([task1, task2])
        DBSession.commit()

        # add tickets
        ticket1 = Ticket(
            project=new_project
        )
        DBSession.add(ticket1)
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
        lead = new_project.lead
        name = new_project.name
        nice_name = new_project.nice_name
        notes = new_project.notes
        references = new_project.references
        repository = new_project.repository
        sequences = new_project.sequences
        start = new_project.start
        status = new_project.status
        status_list = new_project.status_list
        structure = new_project.structure
        tags = new_project.tags
        tasks = new_project.tasks
        type_ = new_project.type
        updated_by = new_project.updated_by
        users = new_project.users
        computed_start = new_project.computed_start
        computed_end = new_project.computed_end
        timing_resolution = new_project.timing_resolution

        # delete the project
        del new_project

        # now get it
        new_project_db = DBSession.query(Project). \
            filter_by(name=kwargs["name"]).first()

        assert (isinstance(new_project_db, Project))

        #self.assertEqual(new_project, new_project_DB)
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
        self.assertEqual(lead, new_project_db.lead)
        self.assertEqual(name, new_project_db.name)
        self.assertEqual(nice_name, new_project_db.nice_name)
        self.assertEqual(notes, new_project_db.notes)
        self.assertEqual(references, new_project_db.references)
        self.assertEqual(repository, new_project_db.repository)
        self.assertEqual(sequences, new_project_db.sequences)
        self.assertEqual(start, new_project_db.start)
        self.assertEqual(status, new_project_db.status)
        self.assertEqual(status_list, new_project_db.status_list)
        self.assertEqual(structure, new_project_db.structure)
        self.assertEqual(tags, new_project_db.tags)
        self.assertEqual(tasks, new_project_db.tasks)
        self.assertEqual(timing_resolution, new_project_db.timing_resolution)
        self.assertEqual(type_, new_project_db.type)
        self.assertEqual(updated_by, new_project_db.updated_by)
        self.assertEqual(users, new_project_db.users)

        # delete tests
        # now delete the project and expect the following also to be deleted
        #
        # Tasks
        # Tickets
        DBSession.delete(new_project_db)
        DBSession.commit()

        # Tasks
        self.assertEqual([], Task.query.all())

        # Tickets
        self.assertEqual([], Ticket.query.all())

    def test_persistence_of_Repository(self):
        """testing the persistence of Repository
        """
        # create a new Repository object and try to read it back
        kwargs = {
            "name": "Movie-Repo",
            "description": "test repository",
            #"created_by": admin,
            #"updated_by": admin,
            "linux_path": "/mnt/M",
            "osx_path": "/mnt/M",
            "windows_path": "M:/"
        }

        # create the repository object
        repo = Repository(**kwargs)

        # save it to database
        DBSession.add(repo)
        DBSession.commit()

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
        repo_db = DBSession.query(Repository) \
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
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Work In Progress", code="WIP")
        status3 = Status(name="Finished", code="FIN")

        project_status_list = StatusList(
            name="Project Statuses",
            statuses=[status1, status2, status3],
            target_entity_type=Project
        )

        shot_status_list = StatusList(
            name="Shot Statuses",
            statuses=[status1, status2, status3],
            target_entity_type=Shot
        )

        repo1 = Repository(
            name="Commercial Repository"
        )

        commercial_project_type = Type(
            name='Commercial Project',
            code='commproj',
            target_entity_type=Project
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

        test_scene = Scene(**kwargs)

        # now add the shots
        shot1 = Shot(
            code='SH001',
            project=test_project1,
            scenes=[test_scene],
            status_list=shot_status_list
        )
        shot2 = Shot(
            code='SH002',
            project=test_project1,
            scenes=[test_scene],
            status_list=shot_status_list
        )
        shot3 = Shot(
            code='SH003',
            project=test_project1,
            scenes=[test_scene],
            status_list=shot_status_list
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

        #self.assertEqual(test_sequence, test_sequence_DB)
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

        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Work In Progress", code="WIP")
        status3 = Status(name="Finished", code="FIN")

        project_status_list = StatusList(
            name="Project Statuses",
            statuses=[status1, status2, status3],
            target_entity_type=Project
        )

        sequence_status_list = StatusList(
            name="Sequence Statuses",
            statuses=[status1, status2, status3],
            target_entity_type=Sequence
        )

        shot_status_list = StatusList(
            name="Shot Statuses",
            statuses=[status1, status2, status3],
            target_entity_type=Shot
        )

        repo1 = Repository(
            name="Commercial Repository"
        )

        commercial_project_type = Type(
            name='Commercial Project',
            code='commproj',
            target_entity_type=Project
        )

        test_project1 = Project(
            name='Test Project',
            code='TP',
            status_list=project_status_list,
            type=commercial_project_type,
            repository=repo1,
        )

        lead = User(
            name="lead",
            login="lead",
            email="lead@lead.com",
            password="password"
        )

        kwargs = {
            'name': 'Test Sequence',
            'code': 'TS',
            'description': 'this is a test sequence',
            'project': test_project1,
            'lead': lead,
            'status_list': sequence_status_list,
            'schedule_model': 'effort',
            'schedule_timing': 50,
            'schedule_unit': 'd'
        }

        test_sequence = Sequence(**kwargs)

        # now add the shots
        shot1 = Shot(
            code='SH001',
            project=test_project1,
            sequences=[test_sequence],
            status_list=shot_status_list
        )
        shot2 = Shot(
            code='SH002',
            project=test_project1,
            sequences=[test_sequence],
            status_list=shot_status_list
        )
        shot3 = Shot(
            code='SH003',
            project=test_project1,
            sequence=test_sequence,
            status_list=shot_status_list
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

        #self.assertEqual(test_sequence, test_sequence_DB)
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

        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Work In Progress", code="WIP")
        status3 = Status(name="Finished", code="FIN")

        project_status_list = StatusList(
            name="Project Statuses",
            statuses=[status1, status2, status3],
            target_entity_type=Project
        )

        sequence_status_list = StatusList(
            name="Sequence Statuses",
            statuses=[status1, status2, status3],
            target_entity_type=Sequence
        )

        shot_status_list = StatusList(
            name="Shot Statuses",
            statuses=[status1, status2, status3],
            target_entity_type=Shot
        )

        commercial_project_type = Type(
            name='Commercial Project',
            code='commproj',
            target_entity_type=Project,
        )

        repo1 = Repository(
            name="Commercial Repository"
        )

        test_project1 = Project(
            name='Test project',
            code='tp',
            status_list=project_status_list,
            type=commercial_project_type,
            repository=repo1,
        )

        lead = User(
            name="lead",
            login="lead",
            email="lead@lead.com",
            password="password"
        )

        kwargs = {
            'name': "Test Sequence 1",
            'code': 'tseq1',
            'description': 'this is a test sequence',
            'project': test_project1,
            'lead': lead,
            'status_list': sequence_status_list,
        }

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
            'status_list': shot_status_list
        }

        test_shot = Shot(**shot_kwargs)

        DBSession.add(test_shot)
        DBSession.add(test_seq1)
        DBSession.commit()

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

        # delete the shot
        del test_shot

        test_shot_db = Shot.query.filter_by(code=shot_kwargs["code"]).first()

        #self.assertEqual(test_shot, test_shot_DB)
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

    def test_persistence_of_SimpleEntity(self):
        """testing the persistence of SimpleEntity
        """
        thumbnail = Link()

        kwargs = {
            "name": "Simple Entity 1",
            "description": "this is for testing purposes",
            'thumbnail': thumbnail,
            'html_style': 'width: 100px; color: purple',
            'html_class': 'purple'
        }

        test_simple_entity = SimpleEntity(**kwargs)

        # persist it to the database
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
        __stalker_version__ = test_simple_entity.__stalker_version__

        del test_simple_entity

        # now try to retrieve it
        test_simple_entity_db = DBSession.query(SimpleEntity) \
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
        self.assertIsNotNone(thumbnail)
        self.assertEqual(thumbnail, test_simple_entity_db.thumbnail)

        ## delete tests
        #self.assertIsNotNone(Link.query.all())
        #
        ## Deleting a SimpleEntity should also delete its thumbnail
        #DBSession.delete(test_simple_entity_DB)
        #DBSession.commit()
        #
        #self.assertIsNone(Link.query.all())

    def test_persistence_of_Status(self):
        """testing the persistence of Status
        """

        # the status

        kwargs = {
            "name": "TestStatus_test_creating_Status",
            "description": "this is for testing purposes",
            "code": "TSTST"
        }

        test_status = Status(**kwargs)

        # persist it to the database
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
        test_status_db = DBSession.query(Status) \
            .filter(Status.name == kwargs["name"]).first()

        assert (isinstance(test_status_db, Status))

        # just test the status part of the object
        #self.assertEqual(test_status, test_status_DB)
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
        statuses = [
            Status(name="Waiting To Start", code="WTS"),
            Status(name="On Hold", code="OH"),
            Status(name="In Progress", code="WIP"),
            Status(name="Complete", code="CMPLT"),
        ]

        kwargs = dict(
            name="Sequence Status List",
            statuses=statuses,
            target_entity_type="Sequence"
        )

        sequence_status_list = StatusList(**kwargs)

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

        #self.assertEqual(sequence_status_list, sequence_status_list_DB)
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
        # and do not expect an IntegrityError

        kwargs["name"] = "new Sequence Status List"
        new_sequence_list = StatusList(**kwargs)

        DBSession.add(new_sequence_list)
        self.assertTrue(new_sequence_list in DBSession)
        self.assertRaises(IntegrityError, DBSession.commit)

    def test_persistence_of_Structure(self):
        """testing the persistence of Structure
        """
        # create pipeline steps for character
        modeling_tType = Type(
            name='Modeling',
            code='model',
            description='This is the step where all the modeling job is done',
            #created_by=admin,
            target_entity_type=Task
        )

        animation_tType = Type(
            name='Animation',
            description='This is the step where all the animation job is ' + \
                        'done it is not limited with characters, other ' + \
                        'things can also be animated',
            code='Anim',
            target_entity_type=Task
        )

        # create a new asset Type
        char_asset_type = Type(
            name='Character',
            code='char',
            description="This is the asset type which covers animated " + \
                        "characters",
            #created_by=admin,
            target_entity_type=Asset,
        )

        # get the Version Type for FilenameTemplates
        v_type = Type.query \
            .filter_by(target_entity_type="FilenameTemplate") \
            .filter_by(name="Version") \
            .first()

        # create a new type template for character assets
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
            target_entity_type=Link
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
            #created_by=admin,
            path="REFS/{{reference.type.name}}",
            filename="{{reference.file_name}}",
            target_entity_type='Link',
            type=r_type
        )

        commercial_structure_type = Type(
            name='Commercial',
            code='commercial',
            target_entity_type=Structure
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

        new_structure = Structure(**kwargs)

        DBSession.add(new_structure)
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

        new_structure_db = DBSession.query(Structure). \
            filter_by(name=kwargs["name"]).first()

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
        test_studio = Studio(name='Test Studio')
        DBSession.add(test_studio)
        DBSession.commit()

        # customize attributes
        test_studio.daily_working_hours = 11
        test_studio.working_hours = WorkingHours(
            working_hours={
                'mon': [],
                'sat': [[100, 1300]]
            }
        )
        test_studio.timing_resolution = datetime.timedelta(hours=1, minutes=30)

        name = test_studio.name
        daily_working_hours = test_studio.daily_working_hours
        timing_resolution = test_studio._timing_resolution
        working_hours = test_studio.working_hours
        # now = test_studio.now

        del test_studio

        # get it back
        test_studio_db = Studio.query.first()

        # self.assertEqual(now, test_studio_DB.now)
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
        date_created = date_updated = datetime.datetime.now()

        tag = Tag(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated)

        # persist it to the database
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
        status1 = Status(name="stat1", code="STS1")
        status2 = Status(name="stat2", code="STS2")
        status3 = Status(name="stat3", code="STS3")
        status4 = Status(name="stat4", code="STS4")
        status5 = Status(name="stat5", code="STS5")

        task_status_list = StatusList(
            name="Task Status List",
            statuses=[status1, status2, status3, status4, status5],
            target_entity_type=Task,
        )

        project_status_list = StatusList(
            name="Project Status List",
            statuses=[status1, status2, status3, status4, status5],
            target_entity_type=Project,
        )

        asset_status_list = StatusList(
            name="Asset Status List",
            statuses=[status1, status2, status3, status4, status5],
            target_entity_type=Asset,
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

        char_asset_type = Type(
            name='Character Asset',
            code='char',
            target_entity_type=Asset
        )

        asset1 = Asset(
            name='Char1',
            code='char1',
            status_list=asset_status_list,
            type=char_asset_type,
            project=project1,
        )

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

        task1 = Task(
            name="Test Task",
            watchers=[user3],
            parent=asset1,
            status_list=task_status_list,
            effort='5h',
            length='15h',
            bid='52h'
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
            resources=[user1]
        )

        # time logs
        time_log1 = TimeLog(
            task=child_task1,
            resource=user1,
            start=datetime.datetime.now(),
            end=datetime.datetime.now() + datetime.timedelta(1)
        )
        task1.computed_start = datetime.datetime.now()
        task1.computed_end = datetime.datetime.now() \
            + datetime.timedelta(10)

        time_log2 = TimeLog(
            task=child_task2,
            resource=user1,
            start=datetime.datetime.now() + datetime.timedelta(1),
            end=datetime.datetime.now() + datetime.timedelta(2)
        )

        # time log for another task
        time_log3 = TimeLog(
            task=task2,
            resource=user1,
            start=datetime.datetime.now() + datetime.timedelta(2),
            end=datetime.datetime.now() + datetime.timedelta(3)
        )

        # Versions
        version1 = Version(
            task=task1
        )

        version2 = Version(
            task=task1
        )

        version3 = Version(
            task=task2
        )

        # referenes
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
            ref1, ref2
        ])
        DBSession.commit()

        computed_start = task1.computed_start
        computed_end = task1.computed_end
        created_by = task1.created_by
        date_created = task1.date_created
        date_updated = task1.date_updated
        duration = task1.duration
        end = task1.end
        is_complete = task1.is_complete
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
        versions = task1.versions
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
        self.assertEqual(is_complete, task1_db.is_complete)
        self.assertEqual(is_milestone, task1_db.is_milestone)
        self.assertEqual(name, task1_db.name)
        self.assertEqual(parent, task1_db.parent)
        self.assertEqual(priority, task1_db.priority)
        self.assertItemsEqual(resources, [])  # it is a parent task, no child
        self.assertItemsEqual(resources, task1_db.resources)
        self.assertEqual(start, task1_db.start)
        self.assertEqual(status, task1_db.status)
        self.assertEqual(status_list, task1_db.status_list)
        self.assertEqual(tags, task1_db.tags)
        self.assertItemsEqual(tasks, task1_db.tasks)
        self.assertEqual(tasks, [child_task1, child_task2])
        self.assertEqual(type_, task1_db.type)
        self.assertEqual(updated_by, task1_db.updated_by)
        self.assertEqual(versions, task1_db.versions)
        self.assertEqual(watchers, task1_db.watchers)
        self.assertEqual(schedule_model, task1_db.schedule_model)
        self.assertEqual(schedule_timing, task1_db.schedule_timing)
        self.assertEqual(schedule_unit, task1_db.schedule_unit)

        # delete tests

        # deleting a Task should also delete:
        #
        # Child Tasks
        # TimeLogs
        # Versions
        DBSession.delete(task1_db)
        DBSession.commit()

        # Expect to have all child tasks also to be deleted
        self.assertItemsEqual(
            [asset1, task2],
            Task.query.all()
        )

        # Expect to have time logs related to this task are deleted
        self.assertItemsEqual(
            [time_log3],
            TimeLog.query.all()
        )

        # We still should have the users intact
        admin = User.query.filter_by(name='admin').first()
        self.assertItemsEqual(
            [user1, user2, user3, admin],
            User.query.all()
        )

        # When updating the test to include deletion, the test task became a
        # parent task, so all the resources are removed, thus the resource
        # attribute should be tested separately.
        resources = task2.resources
        id_ = task2.id
        del task2

        another_task_db = Task.query.get(id_)
        self.assertItemsEqual(resources, [user1])
        self.assertItemsEqual(resources, another_task_db.resources)

    def test_persistence_of_Ticket(self):
        """testing the persistence of Ticket
        """
        repo = Repository(
            name='Test Repository'
        )

        proj_status_list = StatusList(
            name='Project Statuses',
            statuses=[
                Status(name='Work In Progress', code='WIP'),
                Status(name='On Hold', code='OH'),
            ],
            target_entity_type='Project'
        )

        proj_structure = Structure(
            name='Commercials Structure'
        )

        proj1 = Project(
            name='Test Project 1',
            code='TP1',
            repository=repo,
            structure=proj_structure,
            status_list=proj_status_list
        )

        simple_entity = SimpleEntity(
            name='Test Simple Entity'
        )

        entity = Entity(
            name='Test Entity'
        )

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

        note1 = Note(content='This is the content of the note 1')
        note2 = Note(content='This is the content of the note 2')

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
        self.assertItemsEqual(test_ticket_db.logs, logs)

        DBSession.delete(test_ticket_db)
        DBSession.commit()

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

        new_department = Department(**dep_kwargs)

        # create the user
        user_kwargs = {
            "name": "Test",
            "login": "testuser",
            "email": "testuser@test.com",
            "password": "12345",
            "description": "This user has been created for testing purposes",
            "departments": [new_department],
        }

        user1 = User(**user_kwargs)

        DBSession.add_all([user1, new_department])
        DBSession.commit()

        vacation1 = Vacation(
            user=user1,
            start=datetime.datetime.now(),
            end=datetime.datetime.now() + datetime.timedelta(1)
        )

        vacation2 = Vacation(
            user=user1,
            start=datetime.datetime.now() + datetime.timedelta(2),
            end=datetime.datetime.now() + datetime.timedelta(3)
        )

        user1.vacations.append(vacation1)
        user1.vacations.append(vacation2)
        DBSession.add(user1)
        DBSession.commit()

        # create a test project
        repo1 = Repository(name='Test Repo')
        status1 = Status(name='New', code='NEW')
        status2 = Status(name='Work In Progress', code='WIP')
        project_statuses = StatusList(
            name='Project Statuses',
            target_entity_type='Project',
            statuses=[status1, status2]
        )
        project1 = Project(
            name='Test Project',
            code='TP',
            repository=repo1,
            status_list=project_statuses
        )
        task_statuses = StatusList(
            name='Task Statuses',
            target_entity_type='Task',
            statuses=[status1, status2]
        )
        task1 = Task(
            name='Test Task 1',
            project=project1,
            status_list=task_statuses,
            resources=[user1],
        )
        dt = datetime.datetime
        td = datetime.timedelta
        time_log1 = TimeLog(
            task=task1,
            resource=user1,
            start=dt.now(),
            end=dt.now() + td(1)
        )
        DBSession.add(time_log1)
        DBSession.add(task1)
        DBSession.commit()

        # store attributes
        created_by = user1.created_by
        date_created = user1.date_created
        date_updated = user1.date_updated
        departments = user1.departments
        description = user1.description
        email = user1.email
        last_login = user1.last_login
        login = user1.login
        name = user1.name
        nice_name = user1.nice_name
        notes = user1.notes
        password = user1.password
        groups = user1.groups
        projects = user1.projects
        projects_lead = user1.projects_lead
        tags = user1.tags
        tasks = user1.tasks
        watching = user1.watching
        updated_by = user1.updated_by
        vacations = [vacation1, vacation2]

        # delete new_user
        del user1

        user1_db = DBSession.query(User) \
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
        self.assertEqual(email, user1_db.email)
        self.assertEqual(last_login, user1_db.last_login)
        self.assertEqual(login, user1_db.login)
        self.assertEqual(name, user1_db.name)
        self.assertEqual(nice_name, user1_db.nice_name)
        self.assertEqual(notes, user1_db.notes)
        self.assertEqual(password, user1_db.password)
        self.assertEqual(groups, user1_db.groups)
        self.assertEqual(projects, user1_db.projects)
        self.assertEqual(projects_lead, user1_db.projects_lead)
        self.assertEqual(tags, user1_db.tags)
        self.assertEqual(tasks, user1_db.tasks)
        self.assertItemsEqual(vacations, user1_db.vacations)
        self.assertEqual(watching, user1_db.watching)
        self.assertEqual(updated_by, user1_db.updated_by)

        # as the member of a department
        department_db = DBSession.query(Department) \
            .filter(Department.name == dep_kwargs["name"]) \
            .first()

        self.assertEqual(user1_db, department_db.members[0])

        # delete tests
        self.assertItemsEqual(
            [vacation1, vacation2],
            Vacation.query.all()
        )

        # deleting a user should also delete its vacations
        DBSession.delete(user1_db)
        DBSession.commit()

        self.assertItemsEqual([], Vacation.query.all())

        # deleting a user should also delete the time logs
        self.assertItemsEqual([], TimeLog.query.all())

    def test_persistence_of_Vacation(self):
        """testing the persistence of Vacation instances
        """
        # create a User
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

        start = datetime.datetime(2013, 6, 7, 15, 0)
        end = datetime.datetime(2013, 6, 21, 0, 0)

        vacation = Vacation(
            user=new_user,
            type=personal_vacation,
            start=start,
            end=end
        )

        DBSession.add(vacation)
        DBSession.commit()

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
        test_project = Project(
            name='Test Project',
            code='tp',
            status_list=StatusList(
                name='Project Status List',
                target_entity_type=Project,
                statuses=[
                    Status(
                        name='Work In Progress',
                        code="WIP"
                    ),
                    Status(
                        name='Completed',
                        code='Cmplt'
                    )
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
        test_task = Task(
            name='Modeling',
            project=test_project,
            status_list=StatusList(
                name='Task Status List',
                target_entity_type=Task,
                statuses=[
                    Status(
                        name='Waiting to be Approved',
                        code='WAPP',
                    ),
                    Status(
                        name='Started',
                        code='Strt',
                    ),
                ]
            )
        )

        # create a new version
        test_version = Version(
            name='version for task modeling',
            task=test_task,
            version=10,
            take='MAIN',
            full_path='M:/Shows/Proj1/Seq1/Shots/SH001/Ligting'
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
        DBSession.add(test_version)
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
