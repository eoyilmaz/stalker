# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import os
import shutil
import datetime
import unittest
import tempfile
import logging
from sqlalchemy.exc import IntegrityError

from stalker.conf import defaults
from stalker import db
from stalker.db.session import DBSession, ZopeTransactionExtension
from stalker import (Asset, Department, SimpleEntity, Entity, ImageFormat,
                     Link, Note, Project, Repository, Sequence, Shot,
                     Status, StatusList, Structure, Tag, Task, Type,
                     FilenameTemplate, User, Version, Permission, Group)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DatabaseTester(unittest.TestCase):
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
        DBSession.configure(extension=ZopeTransactionExtension())
    
    def setUp(self):
        """setup the tests
        """
        # just set the default admin creation to true
        # some tests are relying on that
        defaults.AUTO_CREATE_ADMIN = True
        defaults.ADMIN_NAME = "admin"
        defaults.ADMIN_PASSWORD = "admin"
        
        self.TEST_DATABASE_URI = "sqlite:///:memory:"
        
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
        #admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        kwargs = {
            "name": "eoyilmaz",
            "first_name": "Erkan Ozgur",
            "last_name": "Yilmaz",
            "login_name": "eoyilmaz",
            "email": "eoyilmaz@gmail.com",
            #"created_by": admin,
            "password": "password",
        }

        newUser = User(**kwargs)
        DBSession.add(newUser)
        DBSession.commit()
        
        # now check if the newUser is there
        newUser_DB = DBSession.query(User)\
            .filter_by(name=kwargs["name"])\
            .filter_by(first_name=kwargs["first_name"])\
            .filter_by(last_name=kwargs["last_name"])\
            .first()
        
        self.assertTrue(newUser_DB is not None)

    def test_creating_a_custom_sqlite_db(self):
        """testing if a custom sqlite database will be created in the given
        location
        """
        self.TEST_DATABASE_FILE = tempfile.mktemp() + ".db"
        self.TEST_DATABASE_DIALECT = "sqlite:///"
        self.TEST_DATABASE_URI = self.TEST_DATABASE_DIALECT +\
                                 self.TEST_DATABASE_FILE
        
        # check if there is no file with the same name
        self.assertFalse(os.path.exists(self.TEST_DATABASE_FILE))

        # setup the database
        db.setup({
            "sqlalchemy.url": self.TEST_DATABASE_URI,
            "sqlalchemy.echo": False,
        })

        # check if the file is created
        self.assertTrue(os.path.exists(self.TEST_DATABASE_FILE))

        # create a new user
        #admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)

        kwargs = {
            "name": "eoyilmaz",
            "first_name": "Erkan Ozgur",
            "last_name": "Yilmaz",
            "login_name": "eoyilmaz",
            "email": "eoyilmaz@gmail.com",
            #"created_by": admin,
            "password": "password",
        }
        
        newUser = User(**kwargs)
        DBSession.add(newUser)
        DBSession.commit()
        
        # now reconnect and check if the newUser is there
        DBSession.remove()
        db.setup({
            "sqlalchemy.url": self.TEST_DATABASE_URI,
            "sqlalchemy.echo": False
        })
        
        newUser_DB = DBSession.query(User)\
            .filter_by(name=kwargs["name"])\
            .filter_by(first_name=kwargs["first_name"])\
            .filter_by(last_name=kwargs["last_name"])\
            .first()
        
        self.assertTrue(newUser_DB is not None)
        
        # delete the temp file
        os.remove(self.TEST_DATABASE_FILE)
        DBSession.remove()
    
    def test_default_admin_creation(self):
        """testing if a default admin is created
        """
        # set default admin creation to True
        defaults.AUTO_CREATE_ADMIN = True
        
        db.setup()
        
        # check if there is an admin
        #admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        admin_DB = DBSession.query(User)\
            .filter(User.name==defaults.ADMIN_NAME)\
            .first()
        
        self.assertEqual(admin_DB.name, defaults.ADMIN_NAME)

    def test_default_admin_for_already_created_databases(self):
        """testing if no extra admin is going to be created for already setup
        databases
        """
        # set default admin creation to True
        defaults.AUTO_CREATE_ADMIN = True
        
        db.setup({
            "sqlalchemy.url": self.TEST_DATABASE_URI
        })
        
        # try to call the db.setup for a second time and see if there are more
        # than one admin
        
        db.setup({
            "sqlalchemy.url": self.TEST_DATABASE_URI
        })
        
        self._createdDB = True
        
        # and get how many admin is created, (it is imipossible to create
        # second one because the tables.simpleEntity.c.nam.unique=True
        
        admins = DBSession.query(User)\
            .filter_by(name=defaults.ADMIN_NAME)\
            .all()
        
        self.assertTrue(len(admins) == 1)
    
#    def test_auth_authenticate_LogginError_raised(self):
#        """testing if stalker.errors.LoginError will be raised when
#        authentication information is wrong
#        """
#        
#        db.setup()
#        
#        test_datas = [
#            ("", ""),
#            ("a user name", ""),
#            ("", "just a pass"),
#            ("no correct user", "wrong pass")
#        ]
#
#        for user_name, password in test_datas:
#            self.assertRaises(
#                LoginError,
#                auth.authenticate,
#                user_name,
#                password
#            )

    def test_no_default_admin_creation(self):
        """testing if there is no user if default.AUTO_CREATE_ADMIN is False
        """
        # turn down auto admin creation
        defaults.AUTO_CREATE_ADMIN = False
        
        # setup the db
        db.setup()
        
        # check if there is a use with name admin
        self.assertTrue(
            DBSession.query(User).filter_by(name=defaults.ADMIN_NAME).first()
            is None
        )

        # check if there is a admins department
        self.assertTrue(
            DBSession.query(Department)
            .filter_by(name=defaults.ADMIN_DEPARTMENT_NAME)
            .first() is None
        )

    def test_non_unique_names_on_different_entity_type(self):
        """testing if there can be non-unique names for different entity types
        """
        db.setup()
        #admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)

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
            "first_name": "user1name",
            "login_name": "user1",
            "email": "user1@gmail.com",
            "password": "user1",
        })

        user1 = User(**kwargs)
        DBSession.add(user1)
        
        # expect nothing, this should work without any error
        DBSession.commit()
    
#    def test_entity_types_table_is_created_properly(self):
#        """testing if the entity_types table is created properly
#        """
#        
#        db.setup()
#        
#        # check if db.metadata.tables has a table with name entity_types
#        self.assertTrue("entity_types", db.metadata.tables)
    
    def test_ticket_status_initialization(self):
        """testing if the ticket statuses are created correctly
        """
        db.setup()
        
        #ticket_statuses = DBSession.query(Status).all()
        ticket_status_list = DBSession.query(StatusList)\
            .filter(StatusList.name=='Ticket Statuses')\
            .first()
        
        self.assertIsInstance(ticket_status_list, StatusList)
        
        expected_status_names = ['New', 'Reopened', 'Closed']
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
        
        permissions_DB = DBSession.query(Permission)\
            .filter(Permission.class_name=='TestClass')\
            .all()
        
        logger.debug("%s" % permissions_DB)
        
        actions = defaults.DEFAULT_ACTIONS
        
        for action in permissions_DB:
            self.assertIn(action.action, actions)
    
    def test_register_raise_TypeError_for_wrong_class_name_argument(self):
        """testing if a TypeError will be raised if the class_name argument is
        not an instance of type or str or unicode
        """
        db.setup()
        self.assertRaises(TypeError, db.register, 23425)
    
    def test_setup_calls_the_callback_function(self):
        """testing if setup will call the given callback function
        """
        
        def test_func():
            raise RuntimeError
        
        self.assertRaises(RuntimeError, db.setup, **{"callback": test_func})
    
    def test_permissions_created_for_all_the_classes(self):
        """testing if Permission instances are created for classes in the SOM
        """
        
        DBSession.remove()
        DBSession.configure(extension=None)
        db.setup()
        
        class_names = [
            'Asset', 'Action', 'Group', 'Permission', 'User', 'Department',
            'Entity', 'SimpleEntity', 'TaskableEntity', 'ImageFormat', 'Link',
            'Message', 'Note', 'Project', 'Repository', 'Sequence', 'Shot',
            'Status', 'StatusList', 'Structure', 'Tag', 'Booking', 'Task',
            'FilenameTemplate', 'Ticket', 'TicketLog', 'Type', 'Version',
        ]
        
        permission_DB = DBSession.query(Permission).all()
        
        self.assertEqual(
            len(permission_DB),
            len(class_names) * len(defaults.DEFAULT_ACTIONS) * 2
        )
        
        from pyramid.security import Allow, Deny
        
        for permission in permission_DB:
            self.assertIn(permission.access, [Allow, Deny])
            self.assertIn(permission.action,  defaults.DEFAULT_ACTIONS)
            self.assertIn(permission.class_name, class_names)
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
        
        # this should not give any error
        DBSession.remove()
        db.setup(settings={'sqlalchemy.url': temp_db_url})
        
        # and we still have correct amount of Permissions
        permissions = DBSession.query(Permission).all()
        self.assertEqual(len(permissions), 224)
        
        # clean the test
        shutil.rmtree(temp_db_path)
    
class DatabaseModelsTester(unittest.TestCase):
    """tests the database model
    
    NOTE TO OTHER DEVELOPERS:
    
    Most of the tests in this TestCase uses parts of the system which are
    tested but probably not tested while running the individual tests.
    
    Incomplete isolation is against to the logic behind unittesting, every test
    should only cover a unit of the code, and a complete isolation should be
    created. But this can not be done in persistence tests (AFAIK), it needs to
    be done in this way for now. Mocks can not be used because every created
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
        #os.remove(cls.TEST_DATABASE_FILE)
        DBSession.configure(extension=ZopeTransactionExtension())

    def setUp(self):
        """setup the test
        """
        # create a test database, possibly an in memory datase
        self.TEST_DATABASE_FILE = ":memory:"
        self.TEST_DATABASE_URI = "sqlite:///" + self.TEST_DATABASE_FILE
        
        # setup using this db
        #db.setup({"sqlalchemy.url": self.TEST_DATABASE_URI})
        db.setup()
    
    def tearDown(self):
        """tearing down the test
        """
        DBSession.remove()
    
    def test_persistence_Asset(self):
        """testing the persistence of Asset
        """
        
        asset_type = Type(
            name="A new asset type A",
            target_entity_type=Asset
        )
        
        status1 = Status(name="On Hold A", code="OHA")
        status2 = Status(name="Completed A", code="CMPLTA")
        status3 = Status(name="Work In Progress A", code="WIPA")
        
        test_repository_type = Type(
            name="Test Repository Type A",
            target_entity_type=Repository,
        )
        
        test_repository = Repository(
            name="Test Repository A",
            type=test_repository_type
        )
        
        project_statusList = StatusList(
            name="Project Status List A",
            statuses=[status1, status2, status3],
            target_entity_type="Project",
            )
        
        commercial_type = Type(name="Commercial A", target_entity_type=Project)
        
        test_project = Project(
            name="Test Project For Asset Creation",
            status_list=project_statusList,
            type=commercial_type,
            repository=test_repository,
            )
        
        DBSession.add(test_project)
        DBSession.commit()
        
        task_status_list = StatusList(
            name="Task Status List",
            statuses=[status1, status2, status3],
            target_entity_type=Task,
        )
        
        asset_statusList = StatusList(
            name="Asset Status List",
            statuses=[status1, status2, status3],
            target_entity_type=Asset
        )
        
        kwargs = {
            "name": "Test Asset",
            "description": "This is a test Asset object",
            "type": asset_type,
            "project": test_project,
            "status_list": asset_statusList,
        }
        
        test_asset = Asset(**kwargs)
        
        DBSession.add(test_asset)
        DBSession.commit()
        
        mock_task1 = Task(
            name="test task 1", status=0,
            status_list=task_status_list,
            task_of=test_asset,
        )
        
        mock_task2 = Task(
            name="test task 2", status=0,
            status_list=task_status_list,
            task_of=test_asset,
        )
        
        mock_task3 = Task(
            name="test task 3", status=0,
            status_list=task_status_list,
            task_of=test_asset,
        )
        
        DBSession.add_all([mock_task1, mock_task2, mock_task3])
        DBSession.commit()
        
        code = test_asset.code
        created_by = test_asset.created_by
        date_created = test_asset.date_created
        date_updated = test_asset.date_updated
        description = test_asset.description
        name = test_asset.name
        nice_name = test_asset.nice_name
        notes = test_asset.notes
        project = test_asset.project
        references = test_asset.references
        status = test_asset.status
        status_list = test_asset.status_list
        tags = test_asset.tags
        tasks = test_asset.tasks
        type = test_asset.type
        updated_by = test_asset.updated_by

        del test_asset

        test_asset_DB = DBSession.query(Asset).\
        filter_by(name=kwargs["name"]).one()

        assert(isinstance(test_asset_DB, Asset))

        #self.assertEqual(test_asset, test_asset_DB)
        self.assertEqual(code, test_asset_DB.code)
        self.assertEqual(created_by, test_asset_DB.created_by)
        self.assertEqual(date_created, test_asset_DB.date_created)
        self.assertEqual(date_updated, test_asset_DB.date_updated)
        self.assertEqual(description, test_asset_DB.description)
        self.assertEqual(name, test_asset_DB.name)
        self.assertEqual(nice_name, test_asset_DB.nice_name)
        self.assertEqual(notes, test_asset_DB.notes)
        self.assertEqual(project, test_asset_DB.project)
        self.assertEqual(references, test_asset_DB.references)
        self.assertEqual(status, test_asset_DB.status)
        self.assertEqual(status_list, test_asset_DB.status_list)
        self.assertEqual(tags, test_asset_DB.tags)
        self.assertEqual(tasks, test_asset_DB.tasks)
        self.assertEqual(type, test_asset_DB.type)
        self.assertEqual(updated_by, test_asset_DB.updated_by)
    
    def test_persistence_Booking(self):
        """testing the persistence of Booking
        """
        self.fail("test is not implemented yet")
    
#    def test_persistence_Review(self):
#        """testing the persistence of Review
#        """
#        
#        # create a new review and connect it to a SimpleEntity
#        new_entity = Entity(name="Review Test Simple Entity")
#        
#        new_review = Review(
#            name="Review",
#            to=new_entity,
#            body="testing the review",
#        )
#        
#        # store it to the database
#        DBSession.add(new_review)
#        DBSession.commit()
#        
#        body = new_review.body
#        code = new_review.code
#        created_by = new_review.created_by
#        date_created = new_review.date_created
#        date_updated = new_review.date_updated
#        description = new_review.description
#        name = new_review.name
#        nice_name = new_review.nice_name
#        notes = new_review.notes
#        reviews = new_review.reviews
#        tags = new_review.tags
#        to = new_review.to
#        type_ = new_review.type
#        updated_by = new_review.updated_by
#        
#        del new_review
#        
#        new_review_DB = DBSession.query(Review).filter_by(name=name).first()
#        
#        assert(isinstance(new_review_DB, Review))
#        
#        self.assertEqual(body, new_review_DB.body)
#        self.assertEqual(code, new_review_DB.code)
#        self.assertEqual(created_by, new_review_DB.created_by)
#        self.assertEqual(date_created, new_review_DB.date_created)
#        self.assertEqual(date_updated, new_review_DB.date_updated)
#        self.assertEqual(description, new_review_DB.description)
#        self.assertEqual(name, new_review_DB.name)
#        self.assertEqual(nice_name, new_review_DB.nice_name)
#        self.assertEqual(notes, new_review_DB.notes)
#        self.assertEqual(reviews, new_review_DB.reviews)
#        self.assertEqual(tags, new_review_DB.tags)
#        self.assertEqual(to, new_review_DB.to)
#        self.assertEqual(type_, new_review_DB.type)
#        self.assertEqual(updated_by, new_review_DB.updated_by)
    
    def test_persistence_Department(self):
        """testing the persistence of Department
        """
        logger.setLevel(logging.DEBUG)
        
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
            name="user1_test_persistence_department",
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
            name="user2_test_persistence_department",
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
            name="user3_test_persistence_department",
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
        
        self.assertIn(test_dep, DBSession)
        
        code = test_dep.code
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
        test_dep_db = DBSession.query(Department).\
        filter_by(name=name).first()
        
        assert(isinstance(test_dep_db, Department))
        
        #self.assertEqual(test_dep, test_dep_db)
        self.assertEqual(code, test_dep_db.code)
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
    
    def test_persistence_Entity(self):
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
        note1 = Note(name="test note")
        
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
            notes=[note1],
            )
        
        # persist it to the database
        DBSession.add(test_entity)
        DBSession.commit()
        
        # store attributes
        code = test_entity.code
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
        test_entity_DB = DBSession.query(Entity).\
        filter_by(name=name).first()
        
        assert(isinstance(test_entity_DB, Entity))
        
        #self.assertEqual(test_entity, test_entity_DB)
        self.assertEqual(code, test_entity_DB.code)
        self.assertEqual(created_by, test_entity_DB.created_by)
        self.assertEqual(date_created, test_entity_DB.date_created)
        self.assertEqual(date_updated, test_entity_DB.date_updated)
        self.assertEqual(description, test_entity_DB.description)
        self.assertEqual(name, test_entity_DB.name)
        self.assertEqual(nice_name, test_entity_DB.nice_name)
        self.assertEqual(notes, test_entity_DB.notes)
        self.assertEqual(tags, test_entity_DB.tags)
        self.assertEqual(updated_by, test_entity_DB.updated_by)
    
    def test_persistence_FilenameTemplate(self):
        """testing the persistence of FilenameTemplate
        """
        ## get the admin
        #admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create a FilenameTemplate object for movie links
        kwargs = {
            "name": "Movie Links Template",
            "target_entity_type": Link,
            "description": "this is a template to be used for links to movie"
                           "files",
            #"created_by": admin,
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
        
        code = new_type_template.code
        created_by = new_type_template.created_by
        date_created = new_type_template.date_created
        date_updated = new_type_template.date_updated
        description = new_type_template.description
        filename = new_type_template.filename
        name = new_type_template.name
        nice_name = new_type_template.nice_name
        notes = new_type_template.notes
        output_path = new_type_template.output_path
        path = new_type_template.path
        tags = new_type_template.tags
        target_entity_type = new_type_template.target_entity_type
        updated_by = new_type_template.updated_by
        
        del new_type_template
        
        # get it back
        new_type_template_DB = DBSession.query(FilenameTemplate).\
        filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(new_type_template_DB, FilenameTemplate))
        
        #self.assertEqual(new_type_template, new_type_template_DB)
        self.assertEqual(code, new_type_template_DB.code)
        self.assertEqual(created_by, new_type_template_DB.created_by)
        self.assertEqual(date_created, new_type_template_DB.date_created)
        self.assertEqual(date_updated, new_type_template_DB.date_updated)
        self.assertEqual(description, new_type_template_DB.description)
        self.assertEqual(filename, new_type_template_DB.filename)
        self.assertEqual(name, new_type_template_DB.name)
        self.assertEqual(nice_name, new_type_template_DB.nice_name)
        self.assertEqual(notes, new_type_template_DB.notes)
        self.assertEqual(output_path,
                         new_type_template_DB.output_path)
        self.assertEqual(path, new_type_template_DB.path)
        self.assertEqual(tags, new_type_template_DB.tags)
        self.assertEqual(target_entity_type,
                         new_type_template_DB.target_entity_type)
        self.assertEqual(updated_by, new_type_template_DB.updated_by)
    
    def test_persistence_ImageFormat(self):
        """testing the persistence of ImageFormat
        """
        
        ## get the admin
        #admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
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
        code = im_format.code
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
        im_format_DB = DBSession.query(ImageFormat).\
        filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(im_format_DB, ImageFormat))
        
        # just test the repository part of the attributes
        #self.assertEqual(im_format, im_format_DB)
        self.assertEqual(code, im_format_DB.code)
        self.assertEqual(created_by, im_format_DB.created_by)
        self.assertEqual(date_created, im_format_DB.date_created)
        self.assertEqual(date_updated, im_format_DB.date_updated)
        self.assertEqual(description, im_format_DB.description)
        self.assertEqual(device_aspect, im_format_DB.device_aspect)
        self.assertEqual(height, im_format_DB.height)
        self.assertEqual(name, im_format_DB.name)
        self.assertEqual(nice_name, im_format_DB.nice_name)
        self.assertEqual(notes, im_format_DB.notes)
        self.assertEqual(pixel_aspect, im_format_DB.pixel_aspect)
        self.assertEqual(print_resolution, im_format_DB.print_resolution)
        self.assertEqual(tags, im_format_DB.tags)
        self.assertEqual(updated_by, im_format_DB.updated_by)
        self.assertEqual(width, im_format_DB.width)
    
    def test_persistence_Link(self):
        """testing the persistence of Link
        """
        
        #admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create a link Type
        sound_link_type = Type(
            name="Sound",
            #created_by=admin,
            target_entity_type=Link
        )
        
        # create a Link
        kwargs = {
            "name": "My Sound",
            #"created_by": admin,
            "path": "M:/PROJECTS/my_movie_sound.wav",
            "type": sound_link_type
        }
        
        new_link = Link(**kwargs)
        
        # persist it
        DBSession.add_all([sound_link_type, new_link])
        DBSession.commit()
        
        # store attributes
        code = new_link.code
        created_by = new_link.created_by
        date_created = new_link.date_created
        date_updated = new_link.date_updated
        description = new_link.description
        name = new_link.name
        nice_name = new_link.nice_name
        notes = new_link.notes
        path = new_link.path
        tags = new_link.tags
        type = new_link.type
        updated_by = new_link.updated_by
        
        # delete the link
        del new_link
        
        # retrieve it back
        new_link_DB = DBSession.query(Link).\
        filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(new_link_DB, Link))
        
        #self.assertEqual(new_link, new_link_DB)
        self.assertEqual(code, new_link_DB.code)
        self.assertEqual(created_by, new_link_DB.created_by)
        self.assertEqual(date_created, new_link_DB.date_created)
        self.assertEqual(date_updated, new_link_DB.date_updated)
        self.assertEqual(description, new_link_DB.description)
        self.assertEqual(name, new_link_DB.name)
        self.assertEqual(nice_name, new_link_DB.nice_name)
        self.assertEqual(notes, new_link_DB.notes)
        self.assertEqual(path, new_link_DB.path)
        self.assertEqual(tags, new_link_DB.tags)
        self.assertEqual(type, new_link_DB.type)
        self.assertEqual(updated_by, new_link_DB.updated_by)
    
    def test_persistence_Note(self):
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
        code = test_note.code
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
        test_note_DB = DBSession.query(Note).\
        filter(Note.name == note_kwargs["name"]).first()
        
        assert(isinstance(test_note_DB, Note))
        
        # try to get the note from the entity
        test_entity_DB = DBSession.query(Entity).\
        filter(Entity.name == entity_kwargs["name"]).first()

        self.assertEqual(code, test_note_DB.code)
        self.assertEqual(content, test_note_DB.content)
        self.assertEqual(created_by, test_note_DB.created_by)
        self.assertEqual(date_created, test_note_DB.date_created)
        self.assertEqual(date_updated, test_note_DB.date_updated)
        self.assertEqual(description, test_note_DB.description)
        self.assertEqual(name, test_note_DB.name)
        self.assertEqual(nice_name, test_note_DB.nice_name)
        self.assertEqual(updated_by, test_note_DB.updated_by)
    
    def test_persistence_Group(self):
        """testing the persistence of Group
        """
        
        group1 = Group(
            name='Test Group'
        )
        
        user1 = User(
            login_name='user1',
            first_name='user1',
            email='user1@test.com',
            password='12'
        )
        user2 = User(
            login_name='user2',
            first_name='user2',
            email='user2@test.com',
            password='34'
        )
        
        group1.users = [user1, user2]
        
        DBSession.add(group1)
        DBSession.commit()
        
        name = group1.name
        users = group1.users
        
        del group1
        group_DB = Group.query().filter_by(name=name).first()
        
        self.assertEqual(name, group_DB.name)
        self.assertEqual(users, group_DB.users)
    
    def test_persistence_Project(self):
        """testing the persistence of Project
        """
        # create mock objects
        start_date = datetime.date.today() + datetime.timedelta(10)
        due_date = start_date + datetime.timedelta(days=20)
        
        lead = User(
            login_name="lead",
            first_name="lead",
            last_name="lead",
            email="lead@lead.com",
            password="password"
        )
        
        user1 = User(
            login_name="user1",
            first_name="user1",
            last_name="user1",
            email="user1@user1.com",
            password="password"
        )
        
        user2 = User(
            login_name="user2",
            first_name="user2",
            last_name="user2",
            email="user1@user2.com",
            password="password"
        )
        
        user3 = User(
            login_name="user3",
            first_name="user3",
            last_name="user3",
            email="user3@user3.com",
            password="password"
        )
        
        image_format = ImageFormat(
            name="HD",
            width=1920,
            height=1080
        )
        
        project_type = Type(
            name="Commercial Project",
            target_entity_type=Project
        )
        
        structure_type = Type(
            name="Commercial Structure",
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
            name="Image",
            target_entity_type="Link"
        )
        
        ref1 = Link(
            name="Ref1",
            path="/mnt/M/JOBs/TEST_PROJECT",
            filename="1.jpg",
            type=link_type
        )
        
        ref2 = Link(
            name="Ref2",
            path="/mnt/M/JOBs/TEST_PROJECT",
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
        
        # create a project object
        kwargs = {
            "name": "Test Project",
            "description": "This is a project object for testing purposes",
            "lead": lead,
            "image_format": image_format,
            "fps": 25,
            "type": project_type,
            "structure": project_structure,
            "repository": repo,
            "is_stereoscopic": False,
            "display_width": 1.0,
            "start_date": start_date,
            "due_date": due_date,
            "status_list": project_status_list,
            "status": 0,
            "references": [ref1, ref2],
            }
        
        new_project = Project(**kwargs)
        
        # persist it in the database
        DBSession.add(new_project)
        DBSession.commit()
        
        task1 = Task(
            name="task1",
            status_list=task_status_list,
            status=0,
            task_of=new_project,
            )

        task2 = Task(
            name="task2",
            status_list=task_status_list,
            status=0,
            task_of=new_project,
            )
        
        DBSession.add_all([task1, task2])
        DBSession.commit()
        
        # store the attributes
        assets = new_project.assets
        code = new_project.code
        created_by = new_project.created_by
        date_created = new_project.date_created
        date_updated = new_project.date_updated
        description = new_project.description
        #display_width = new_project.display_width
        due_date = new_project.due_date
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
        start_date = new_project.start_date
        status = new_project.status
        status_list = new_project.status_list
        structure = new_project.structure
        tags = new_project.tags
        tasks = new_project.tasks
        type = new_project.type
        updated_by = new_project.updated_by
        users = new_project.users
        
        # delete the project
        del new_project
        
        # now get it
        new_project_DB = DBSession.query(Project).\
        filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(new_project_DB, Project))
        
        #self.assertEqual(new_project, new_project_DB)
        self.assertEqual(assets, new_project_DB.assets)
        self.assertEqual(code, new_project_DB.code)
        self.assertEqual(created_by, new_project_DB.created_by)
        self.assertEqual(date_created, new_project_DB.date_created)
        self.assertEqual(date_updated, new_project_DB.date_updated)
        self.assertEqual(description, new_project_DB.description)
        #self.assertEqual(display_width, new_project_DB.display_width)
        self.assertEqual(due_date, new_project_DB.due_date)
        self.assertEqual(duration, new_project_DB.duration)
        self.assertEqual(fps, new_project_DB.fps)
        self.assertEqual(image_format, new_project_DB.image_format)
        self.assertEqual(is_stereoscopic, new_project_DB.is_stereoscopic)
        self.assertEqual(lead, new_project_DB.lead)
        self.assertEqual(name, new_project_DB.name)
        self.assertEqual(nice_name, new_project_DB.nice_name)
        self.assertEqual(notes, new_project_DB.notes)
        self.assertEqual(references, new_project_DB.references)
        self.assertEqual(repository, new_project_DB.repository)
        self.assertEqual(sequences, new_project_DB.sequences)
        self.assertEqual(start_date, new_project_DB.start_date)
        self.assertEqual(status, new_project_DB.status)
        self.assertEqual(status_list, new_project_DB.status_list)
        self.assertEqual(structure, new_project_DB.structure)
        self.assertEqual(tags, new_project_DB.tags)
        self.assertEqual(tasks, new_project_DB.tasks)
        self.assertEqual(type, new_project_DB.type)
        self.assertEqual(updated_by, updated_by)
        self.assertEqual(users, new_project_DB.users)
    
    def test_persistence_Repository(self):
        """testing the persistence of Repository
        """
        ## get the admin
        #admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
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
        repo_db = DBSession.query(Repository)\
            .filter_by(name=kwargs["name"])\
            .first()
        
        assert(isinstance(repo_db, Repository))
        
        #self.assertEqual(repo.code, repo_db.code)
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
    
    def test_persistence_Sequence(self):
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
            name="Commercial Project",
            target_entity_type=Project
        )

        project1 = Project(
            name="Test project",
            status_list=project_status_list,
            type=commercial_project_type,
            repository=repo1,
            )

        lead = User(
            login_name="lead",
            email="lead@lead.com",
            first_name="lead",
            last_name="lead",
            password="password"
        )

        kwargs = {
            "name": "Test sequence",
            "description": "this is a test sequence",
            "project": project1,
            "lead": lead,
            "status_list": sequence_status_list,
            }

        test_sequence = Sequence(**kwargs)

        # now add the shots
        shot1 = Shot(code="SH001", sequence=test_sequence, status=0,
                     status_list=shot_status_list)
        shot2 = Shot(code="SH002", sequence=test_sequence, status=0,
                     status_list=shot_status_list)
        shot3 = Shot(code="SH003", sequence=test_sequence, status=0,
                     status_list=shot_status_list)
        
        DBSession.add(test_sequence)
        DBSession.commit()
        
        # store the attributes
        code = test_sequence.code
        created_by = test_sequence.created_by
        date_created = test_sequence.date_created
        date_updated = test_sequence.date_updated
        description = test_sequence.description
        due_date = test_sequence.due_date
        duration = test_sequence.duration
        lead = test_sequence.lead
        name = test_sequence.name
        nice_name = test_sequence.nice_name
        notes = test_sequence.notes
        project = test_sequence.project
        references = test_sequence.references
        shots = test_sequence.shots
        start_date = test_sequence.start_date
        status = test_sequence.status
        status_list = test_sequence.status_list
        tags = test_sequence.tags
        tasks = test_sequence.tasks
        updated_by = test_sequence.updated_by
        
        # delete the test_sequence
        del test_sequence
        
        test_sequence_DB = DBSession.query(Sequence)\
            .filter_by(name=kwargs["name"]).one()
        
        #self.assertEqual(test_sequence, test_sequence_DB)
        self.assertEqual(code, test_sequence_DB.code)
        self.assertEqual(created_by, test_sequence_DB.created_by)
        self.assertEqual(date_created, test_sequence_DB.date_created)
        self.assertEqual(date_updated, test_sequence_DB.date_updated)
        self.assertEqual(description, test_sequence_DB.description)
        self.assertEqual(due_date, test_sequence_DB.due_date)
        self.assertEqual(duration, test_sequence_DB.duration)
        self.assertEqual(lead, test_sequence_DB.lead)
        self.assertEqual(name, test_sequence_DB.name)
        self.assertEqual(nice_name, test_sequence_DB.nice_name)
        self.assertEqual(notes, test_sequence_DB.notes)
        self.assertEqual(project, test_sequence_DB.project)
        self.assertEqual(references, test_sequence_DB.references)
        self.assertEqual(shots, test_sequence_DB.shots)
        self.assertEqual(start_date, test_sequence_DB.start_date)
        self.assertEqual(status, test_sequence_DB.status)
        self.assertEqual(status_list, test_sequence_DB.status_list)
        self.assertEqual(tags, test_sequence_DB.tags)
        self.assertEqual(tasks, test_sequence_DB.tasks)
        self.assertEqual(updated_by, test_sequence_DB.updated_by)
    
    def test_persistence_Shot(self):
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
            name="Commercial Project",
            target_entity_type=Project,
            )

        repo1 = Repository(
            name="Commercial Repository"
        )
        
        project1 = Project(
            name="Test project",
            status_list=project_status_list,
            type=commercial_project_type,
            repository=repo1,
            )
        
        lead = User(
            login_name="lead",
            email="lead@lead.com",
            first_name="lead",
            last_name="lead",
            password="password"
        )
        
        kwargs = {
            "name": "Test sequence",
            "description": "this is a test sequence",
            "project": project1,
            "lead": lead,
            "status_list": sequence_status_list,
        }
        
        test_sequence = Sequence(**kwargs)
        
        # now add the shots
        shot_kwargs = {
            "code": "SH001",
            "sequence": test_sequence,
            "status": 0,
            "status_list": shot_status_list
        }
        
        test_shot = Shot(**shot_kwargs)

        DBSession.add(test_shot)
        DBSession.add(test_sequence)
        DBSession.commit()
        
        # store the attributes
        code = test_shot.code
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
        sequence = test_shot.sequence
        status = test_shot.status
        status_list = test_shot.status_list
        tags = test_shot.tags
        tasks = test_shot.tasks
        updated_by = test_shot.updated_by
        
        # delete the shot
        del test_shot
        
        test_shot_DB = DBSession.query(Shot)\
            .filter_by(code=shot_kwargs["code"]).first()
        
        #self.assertEqual(test_shot, test_shot_DB)
        self.assertEqual(code, test_shot_DB.code)
        self.assertEqual(cut_duration, test_shot_DB.cut_duration)
        self.assertEqual(cut_in, test_shot_DB.cut_in)
        self.assertEqual(cut_out, test_shot_DB.cut_out)
        self.assertEqual(date_created, test_shot_DB.date_created)
        self.assertEqual(date_updated, test_shot_DB.date_updated)
        self.assertEqual(description, test_shot_DB.description)
        self.assertEqual(name, test_shot_DB.name)
        self.assertEqual(nice_name, test_shot_DB.nice_name)
        self.assertEqual(notes, test_shot_DB.notes)
        self.assertEqual(references, test_shot_DB.references)
        self.assertEqual(sequence, test_shot_DB.sequence)
        self.assertEqual(status, test_shot_DB.status)
        self.assertEqual(status_list, test_shot_DB.status_list)
        self.assertEqual(tags, test_shot_DB.tags)
        self.assertEqual(tasks, test_shot_DB.tasks)
        self.assertEqual(updated_by, test_shot_DB.updated_by)
    
    def test_persistence_SimpleEntity(self):
        """testing the persistence of SimpleEntity
        """
        
        kwargs = {
            "name": "SimpleEntity_test_creating_of_a_SimpleEntity",
            "description": "this is for testing purposes",
            }
        
        test_simple_entity = SimpleEntity(**kwargs)
        
        # persist it to the database
        DBSession.add(test_simple_entity)
        DBSession.commit()
        
        code = test_simple_entity.code
        created_by = test_simple_entity.created_by
        date_created = test_simple_entity.date_created
        date_updated = test_simple_entity.date_updated
        description = test_simple_entity.description
        name = test_simple_entity.name
        nice_name = test_simple_entity.nice_name
        updated_by = test_simple_entity.updated_by
        __stalker_version__ = test_simple_entity.__stalker_version__
        
        del test_simple_entity
        
        # now try to retrieve it
        test_simple_entity_DB = DBSession.query(SimpleEntity)\
            .filter(SimpleEntity.name == kwargs["name"]).first()
        
        assert(isinstance(test_simple_entity_DB, SimpleEntity))
        
        #self.assertEqual(test_simple_entity, test_simple_entity_DB)
        self.assertEqual(code, test_simple_entity_DB.code)
        self.assertEqual(created_by, test_simple_entity_DB.created_by)
        self.assertEqual(date_created, test_simple_entity_DB.date_created)
        self.assertEqual(date_updated, test_simple_entity_DB.date_updated)
        self.assertEqual(description, test_simple_entity_DB.description)
        self.assertEqual(name, test_simple_entity_DB.name)
        self.assertEqual(nice_name, test_simple_entity_DB.nice_name)
        self.assertEqual(updated_by, test_simple_entity_DB.updated_by)
        self.assertEqual(__stalker_version__,
                         test_simple_entity_DB.__stalker_version__)
    
    def test_persistence_Status(self):
        """testing the persistence of Status
        """
        
        # the status
        
        kwargs = {
            "name": "TestStatus_test_creating_Status",
            "description": "this is for testing purposes",
            "code": "TSTST",
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
        test_status_DB = DBSession.query(Status)\
            .filter(Status.name == kwargs["name"]).first()
        
        assert(isinstance(test_status_DB, Status))
        
        # just test the satuts part of the object
        #self.assertEqual(test_status, test_status_DB)
        self.assertEqual(code, test_status_DB.code)
        self.assertEqual(created_by, test_status_DB.created_by)
        self.assertEqual(date_created, test_status_DB.date_created)
        self.assertEqual(date_updated, test_status_DB.date_updated)
        self.assertEqual(description, test_status_DB.description)
        self.assertEqual(name, test_status_DB.name)
        self.assertEqual(nice_name, test_status_DB.nice_name)
        self.assertEqual(notes, test_status_DB.notes)
        self.assertEqual(tags, test_status_DB.tags)
        self.assertEqual(updated_by, test_status_DB.updated_by)
    
    def test_persistence_StatusList(self):
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
        code = sequence_status_list.code
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
        sequence_status_list_DB = StatusList.query()\
            .filter_by(name=kwargs["name"])\
            .first()
        
        assert(isinstance(sequence_status_list_DB, StatusList))
        
        #self.assertEqual(sequence_status_list, sequence_status_list_DB)
        self.assertEqual(code, sequence_status_list_DB.code)
        self.assertEqual(created_by, sequence_status_list_DB.created_by)
        self.assertEqual(date_created, sequence_status_list_DB.date_created)
        self.assertEqual(date_updated, sequence_status_list_DB.date_updated)
        self.assertEqual(description, sequence_status_list_DB.description)
        self.assertEqual(name, sequence_status_list_DB.name)
        self.assertEqual(nice_name, sequence_status_list_DB.nice_name)
        self.assertEqual(notes, sequence_status_list_DB.notes)
        self.assertEqual(statuses, sequence_status_list_DB.statuses)
        self.assertEqual(tags, sequence_status_list_DB.tags)
        self.assertEqual(target_entity_type,
                         sequence_status_list_DB.target_entity_type)
        self.assertEqual(updated_by, sequence_status_list_DB.updated_by)
        
        # try to create another StatusList for the same target_entity_type
        # and expect and IntegrityError
        
        kwargs["name"] = "new Sequence Status List"
        new_sequence_list = StatusList(**kwargs)
        
        DBSession.add(new_sequence_list)
        self.assertIn(new_sequence_list, DBSession)
        self.assertRaises(IntegrityError, DBSession.commit)
    
    def test_persistence_Structure(self):
        """testing the persistence of Structure
        """
        
        #admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create pipeline steps for character
        modeling_tType = Type(
            name="Modeling",
            description="This is the step where all the modeling job is done",
            code="MODEL",
            #created_by=admin,
            target_entity_type=Task
        )
        
        animation_tType = Type(
            name="Animation",
            description="This is the step where all the animation job is " +\
                        "done it is not limited with characters, other " +\
                        "things can also be animated",
            code="ANIM",
            #created_by=admin,
            target_entity_type=Task
        )
        
        # create a new asset Type
        char_asset_type = Type(
            name="Character Asset Type",
            description="This is the asset type which covers animated " +\
                        "charactes",
            #created_by=admin,
            target_entity_type=Asset,
        )
        
        # create a new type template for character assets
        assetTemplate = FilenameTemplate(
            name="Character Asset Template",
            description="This is the template for character assets",
            path="ASSETS/{{asset_type.name}}/{{pipeline_step.code}}",
            filename="{{asset.name}}_{{take.name}}_{{asset_type.name}}_\
            v{{version.version_number}}",
            target_entity_type=Asset,
        )
        
        # create a new link type
        image_link_type = Type(
            name="Image",
            description="It is used for links showing an image",
            #created_by=admin,
            target_entity_type=Link
        )
        
        # create a new template for references
        imageReferenceTemplate = FilenameTemplate(
            name="Image Reference Template",
            description="this is the template for image references, it "
                        "shows where to place the image files",
            #created_by=admin,
            path="REFS/{{reference.type.name}}",
            filename="{{reference.file_name}}",
            target_entity_type=Link
        )
        
        commercial_structure_type = Type(
            name="Commercial",
            target_entity_type=Structure
        )
        
        # create a new structure
        kwargs = {
            "name": "Commercial Structure",
            "description": "The structure for commercials",
            #"created_by": admin,
            "custom_template": """
                Assets
                Sequences
                Sequences/{% for sequence in project.sequences %}
                {{sequence.code}}""",
            "templates": [assetTemplate, imageReferenceTemplate],
            "type": commercial_structure_type
        }
        
        new_structure = Structure(**kwargs)
        
        DBSession.add(new_structure)
        DBSession.commit()
        
        # store the attributes
        templates = new_structure.templates
        code = new_structure.code
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
        
        new_structure_DB = DBSession.query(Structure).\
        filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(new_structure_DB, Structure))
        
        #self.assertEqual(new_structure, new_structure_DB)
        self.assertEqual(templates, new_structure_DB.templates)
        self.assertEqual(code, new_structure_DB.code)
        self.assertEqual(created_by, new_structure_DB.created_by)
        self.assertEqual(date_created, new_structure_DB.date_created)
        self.assertEqual(date_updated, new_structure_DB.date_updated)
        self.assertEqual(description, new_structure_DB.description)
        self.assertEqual(name, new_structure_DB.name)
        self.assertEqual(nice_name, new_structure_DB.nice_name)
        self.assertEqual(notes, new_structure_DB.notes)
        self.assertEqual(custom_template, new_structure_DB.custom_template)
        self.assertEqual(tags, new_structure_DB.tags)
        self.assertEqual(updated_by, new_structure_DB.updated_by)

    def test_persistence_Tag(self):
        """testing the persistence of Tag
        """
        
        name = "Tag_test_creating_a_Tag"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        date_created = date_updated = datetime.datetime.now()
        
        aTag = Tag(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated)

        # persist it to the database
        DBSession.add(aTag)
        DBSession.commit()
        
        # store the attributes
        description = aTag.description
        created_by = aTag.created_by
        updated_by = aTag.updated_by
        date_created = aTag.date_created
        date_updated = aTag.date_updated
        
        # delete the aTag
        del aTag
        
        # now try to retrieve it
        aTag_DB = DBSession.query(Tag).filter_by(name=name).first()
        
        assert(isinstance(aTag_DB, Tag))
        
        self.assertEqual(name, aTag_DB.name)
        self.assertEqual(description, aTag_DB.description)
        self.assertEqual(created_by, aTag_DB.created_by)
        self.assertEqual(updated_by, aTag_DB.updated_by)
        self.assertEqual(date_created, aTag_DB.date_created)
        self.assertEqual(date_updated, aTag_DB.date_updated)


    def test_persistence_Task(self):
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
        
        test_repo = Repository(
            name="Test Repo",
            linux_path="/mnt/M/JOBs",
            windows_path="M:/JOBs",
            osx_path="/Users/Shared/Servers/M",
        )
        
        test_project1 = Project(
            name="Tests Project",
            status_list=project_status_list,
            repository=test_repo,
        )
        
        char_asset_type = Type(
            name="Character Asset",
            target_entity_type=Asset
        )
        
        new_asset = Asset(
            name="Char1",
            status_list=asset_status_list,
            type=char_asset_type,
            project=test_project1,
        )
        
        user1 = User(
            login_name="user1",
            first_name="User1",
            last_name="User1",
            email="user1@user.com",
            password="1234",
        )
        
        user2 = User(
            login_name="user2",
            first_name="User2",
            last_name="User2",
            email="user2@user.com",
            password="1234",
        )
        
        user3 = User(
            login_name="user3",
            first_name="User3",
            last_name="User3",
            email="user3@user.com",
            password="1234",
        )
        
        test_task = Task(
            name="Test Task",
            resources=[user1, user2, user3],
            task_of=new_asset,
            status_list=task_status_list,
            effort=datetime.timedelta(5)
        )
        
        DBSession.add(test_task)
        DBSession.commit()
        
        bookings = test_task.bookings
        code = test_task.code
        created_by = test_task.created_by
        date_created = test_task.date_created
        date_updated = test_task.date_updated
        effort = test_task.effort
        is_complete = test_task.is_complete
        is_milestone = test_task.is_milestone
        name = test_task.name
        priority = test_task.priority
        resources = test_task.resources
#        reviews = test_task.reviews
        start_date = test_task.start_date
        status = test_task.status
        status_list = test_task.status_list
        tags = test_task.tags
        task_of = test_task.task_of
        type_ = test_task.type
        updated_by = test_task.updated_by
        versions = test_task.versions
    
        del test_task
        
        # now query it back
        test_task_DB = DBSession.query(Task).filter_by(name=name).first()
        
        assert(isinstance(test_task_DB, Task))
        
        self.assertEqual(bookings, test_task_DB.bookings)
        self.assertEqual(code, test_task_DB.code)
        self.assertEqual(created_by, test_task_DB.created_by)
        self.assertEqual(date_created, test_task_DB.date_created)
        self.assertEqual(date_updated, test_task_DB.date_updated)
        self.assertEqual(effort, test_task_DB.effort)
        self.assertEqual(is_complete, test_task_DB.is_complete)
        self.assertEqual(is_milestone, test_task_DB.is_milestone)
        self.assertEqual(name, test_task_DB.name)
        self.assertEqual(priority, test_task_DB.priority)
        self.assertEqual(resources, test_task_DB.resources)
#        self.assertEqual(reviews, test_task_DB.reviews)
        self.assertEqual(start_date, test_task_DB.start_date)
        self.assertEqual(status, test_task_DB.status)
        self.assertEqual(status_list, test_task_DB.status_list)
        self.assertEqual(tags, test_task_DB.tags)
        self.assertEqual(task_of, test_task_DB.task_of)
        self.assertEqual(type_, test_task_DB.type)
        self.assertEqual(updated_by, test_task_DB.updated_by)
        self.assertEqual(versions, test_task_DB.versions)

    def test_persistence_User(self):
        """testing the persistence of User
        """
        
        # create a new user save and retrieve it
        
        # create a Department for the user
        dep_kwargs = {
            "name": "Test Department",
            "description": "This department has been created for testing \
            purposes",
        }
        
        new_department = Department(**dep_kwargs)
        
        # create the user
        user_kwargs = {
            "login_name": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@test.com",
            "password": "12345",
            "description": "This user has been created for testing purposes",
            "department": new_department,
        }
        
        new_user = User(**user_kwargs)
        
        DBSession.add_all([new_user, new_department])
        DBSession.commit()
        
        # store attributes
        code = new_user.code
        created_by = new_user.created_by
        date_created = new_user.date_created
        date_updated = new_user.date_updated
        department = new_user.department
        description = new_user.description
        email = new_user.email
        first_name = new_user.first_name
        initials = new_user.initials
        last_login = new_user.last_login
        last_name = new_user.last_name
        login_name = new_user.login_name
        name = new_user.name
        nice_name = new_user.nice_name
        notes = new_user.notes
        password = new_user.password
        groups = new_user.groups
        projects = new_user.projects
        projects_lead = new_user.projects_lead
        sequences_lead = new_user.sequences_lead
        tags = new_user.tags
        tasks = new_user.tasks
        updated_by = new_user.updated_by
        
        # delete new_user
        del new_user
        
        new_user_DB = DBSession.query(User)\
            .filter(User.name == user_kwargs["login_name"])\
            .first()
        
        assert(isinstance(new_user_DB, User))
        
        # the user itself
        #self.assertEqual(new_user, new_user_DB)
        self.assertEqual(code, new_user_DB.code)
        self.assertEqual(created_by, new_user_DB.created_by)
        self.assertEqual(date_created, new_user_DB.date_created)
        self.assertEqual(date_updated, new_user_DB.date_updated)
        self.assertEqual(department, new_user_DB.department)
        self.assertEqual(description, new_user_DB.description)
        self.assertEqual(email, new_user_DB.email)
        self.assertEqual(first_name, new_user_DB.first_name)
        self.assertEqual(initials, new_user_DB.initials)
        self.assertEqual(last_login, new_user_DB.last_login)
        self.assertEqual(last_name, new_user_DB.last_name)
        self.assertEqual(login_name, new_user_DB.login_name)
        self.assertEqual(name, new_user_DB.name)
        self.assertEqual(nice_name, new_user_DB.nice_name)
        self.assertEqual(notes, new_user_DB.notes)
        self.assertEqual(password, new_user_DB.password)
        self.assertEqual(groups, new_user_DB.groups)
        self.assertEqual(projects, new_user_DB.projects)
        self.assertEqual(projects_lead, new_user_DB.projects_lead)
        self.assertEqual(sequences_lead, new_user_DB.sequences_lead)
        self.assertEqual(tags, new_user_DB.tags)
        self.assertEqual(tasks, new_user_DB.tasks)
        self.assertEqual(updated_by, new_user_DB.updated_by)

        # as the member of a department
        department_db = DBSession.query(Department)\
            .filter(Department.name == dep_kwargs["name"])\
            .first()
        
        self.assertEqual(new_user_DB, department_db.members[0])


    def test_persistence_Version(self):
        """testing the persistence of Version
        """
        
        # create a project
        test_project = Project(
            name="Test Project",
            status_list=StatusList(
                name="Project Status List",
                target_entity_type=Project,
                statuses=[
                    Status(
                        name="Work In Progress",
                        code="WIP"
                    ),
                    Status(
                        name="Completed",
                        code="Cmplt"
                    )
                ]
            ),
            repository=Repository(
                name="Film Projects",
                windows_path="M:/",
                linux_path="/mnt/M/",
                osx_path="/Users/Volumes/M/",
                )
        )

        # create a task
        test_task = Task(
            name="Modeling",
            task_of=test_project,
            status_list=StatusList(
                name="Task Status List",
                target_entity_type=Task,
                statuses=[
                    Status(
                        name="Waiting to be Approved",
                        code="WAPP",
                        ),
                    Status(
                        name="Started",
                        code="Strt",
                        ),
                    ]
            )
        )

        # create a new version
        test_version = Version(
            name="version for task modeling",
            version_of=test_task,
            version=10,
            take="MAIN",
            source=Link(
                name="Modeling",
                path="M:/JOBs/Proj1/Seq1/Shots/SH001/Ligting\
                /Proj1_Seq1_Sh001_MAIN_Lighting_v001.ma"
            ),
            outputs=[
                Link(
                    name="Renders",
                    path="M:/JOBs/Proj1/Seq1/Shots/SH001/Lighting/Output/test1\
                    .###.jpg"
                ),
                ],
            status_list=StatusList(
                name="Version Statuses",
                statuses=[
                    Status(name="Status1", code="STS1"),
                    Status(name="Status2", code="STS2"),
                    Status(name="Status3", code="STS3"),
                    Status(name="Published", code="PBL")
                ],
                target_entity_type=Version,
                ),
            status=3,
            )

        # now save it to the database
        DBSession.add(test_version)
        DBSession.commit()
        
        code = test_version.code
        created_by = test_version.created_by
        date_created = test_version.date_created
        date_updated = test_version.date_updated
        name = test_version.name
        nice_name = test_version.nice_name
        notes = test_version.notes
        outputs = test_version.outputs
        is_published = test_version.is_published
        #reviews = test_version.reviews
        source_file = test_version.source_file
        status = test_version.status
        status_list = test_version.status_list
        tags = test_version.tags
        take_name = test_version.take_name
        type = test_version.type
        updated_by = test_version.updated_by
        version_number = test_version.version_number
        version_of = test_version.version_of
        
        del test_version
        
        # get it back from the db
        test_version_DB = DBSession.query(Version).filter_by(name=name).first()
        
        assert(isinstance(test_version_DB, Version))
        
        self.assertEqual(code, test_version_DB.code)
        self.assertEqual(created_by, test_version_DB.created_by)
        self.assertEqual(date_created, test_version_DB.date_created)
        self.assertEqual(date_updated, test_version_DB.date_updated)
        self.assertEqual(name, test_version_DB.name)
        self.assertEqual(nice_name, test_version_DB.nice_name)
        self.assertEqual(notes, test_version_DB.notes)
        self.assertEqual(outputs, test_version_DB.outputs)
        self.assertEqual(is_published, test_version_DB.is_published)
        self.assertEqual(source_file, test_version_DB.source_file)
        self.assertEqual(status, test_version_DB.status)
        self.assertEqual(status_list, test_version_DB.status_list)
        self.assertEqual(tags, test_version_DB.tags)
        self.assertEqual(take_name, test_version_DB.take_name)
        self.assertEqual(type, test_version_DB.type)
        self.assertEqual(updated_by, test_version_DB.updated_by)
        self.assertEqual(version_number, test_version_DB.version_number)
        self.assertEqual(version_of, test_version_DB.version_of)

    #
    #class ExamplesTester(unittest.TestCase):
    #"""tests the examples
    #"""



    #
    #@classmethod
    #def setUpClass(cls):
    #"""setup the test
    #"""

    ## add the stalker/examples directory to the sys.path
    #import os, sys
    #import stalker

    #stalker_dir = os.path.sep.join(
    #stalker.__file__.split(
    #os.path.sep
    #)[:-2]
    #)

    #sys.path.append(stalker_dir)



    #
    #def test_ReferenceMixin_setup(self):
    #"""testing if the ReferenceMixin can be correctly setup with a new
    #class
    #"""

    ## the actual test
    #from examples.extending import great_entity
    #defaults.MAPPERS.append("examples.extending.great_entity")
    #defaults.CORE_MODEL_CLASSES.append(
    #"examples.extending.great_entity.GreatEntity"
    #)

    ##db.setup("sqlite:////tmp/mixin_test.db")
    #db.setup()

    #newGreatEntity = great_entity.GreatEntity(name="test")
    #DBSession.add(newGreatEntity)
    #DBSession.commit()

    #newLinkType = Type(name="Image", target_entity_type=Link)

    #newLink = Link(name="TestLink", path="nopath", filename="nofilename",
    #type=newLinkType)

    #newGreatEntity.references = [newLink]

    #DBSession.add_all([newLink, newLinkType])
    #DBSession.commit()

    ## query and check the equality
    #newGreatEntity_DB = DBSession.query(great_entity.GreatEntity).\
    #filter_by(name="test").first()

    #self.assertEqual(newGreatEntity, newGreatEntity_DB)

    ## clean up the test
    #defaults.MAPPERS.remove("examples.extending.great_entity")
    #defaults.CORE_MODEL_CLASSES.remove(
    #"examples.extending.great_entity.GreatEntity")



    #
    #def test_StatusMixin_setup(self):
    #"""testing if the StatusMixin can be correctly setup with a new class
    #"""

    ## the actual test
    #from examples.extending import statused_entity

    #defaults.MAPPERS.append("examples.extending.statused_entity")
    #defaults.CORE_MODEL_CLASSES.append(
    #"examples.extending.statused_entity.NewStatusedEntity")

    ##db.setup("sqlite:////tmp/mixin_test.db")
    #db.setup()

    #newStatusList = StatusList(
    #name="A Status List for testing StatusMixin",
    #statuses=[
    #Status(name="Mixin - On Hold", code="OH"),
    #Status(name="Mixin - Complete", code="CMPLT")
    #],
    #target_entity_type = statused_entity.NewStatusedEntity
    #)
    #DBSession.add(newStatusList)
    #DBSession.commit()

    #aStatusedEntity = statused_entity.NewStatusedEntity(
    #name="test")

    ## add the status list
    #aStatusedEntity.status_list = newStatusList

    #DBSession.add(aStatusedEntity)
    #DBSession.commit()

    ## query and check the equality
    #aStatusedEntity_DB = DBSession.query(statused_entity.NewStatusedEntity).\
    #first()

    #self.assertEqual(aStatusedEntity, aStatusedEntity_DB)

    ## clean up the test
    #defaults.MAPPERS.remove("examples.extending.statused_entity")
    #defaults.CORE_MODEL_CLASSES.remove(
    #"examples.extending.statused_entity.NewStatusedEntity")



    #
    #def test_camera_lens(self):
    #"""testing the camera_lens example
    #"""

    #from examples.extending import camera_lens
    #defaults.MAPPERS.append("examples.extending.camera_lens")
    #defaults.CORE_MODEL_CLASSES.append(
    #"examples.extending.camera_lens.Camera")
    #defaults.CORE_MODEL_CLASSES.append(
    #"examples.extending.camera_lens.Lens")

    ##db.setup("sqlite:////tmp/camera_lens.db")
    #db.setup("sqlite://")

    #new_camera = camera_lens.Camera(
    #name="Nikon D300",
    #make="Nikon",
    #model="D300",
    #horizontal_film_back=23.6,
    #vertical_film_back=15.8,
    #cropping_factor=1.5,
    #web_page="http://www.nikon.com",
    #)

    #new_lens = camera_lens.Lens(
    #name="Nikon 50 mm Lens",
    #make="Nikon",
    #model="Nikkor 50mm 1.8",
    #min_focal_length=50,
    #max_focal_length=50,
    #web_page="http://www.nikon.com",
    #)

    #DBSession.add_all([new_camera, new_lens])
    #DBSession.commit()

    ## retrieve them from the db
    #new_camera_DB = DBSession.query(camera_lens.Camera).first()
    #new_lens_DB = DBSession.query(camera_lens.Lens).first()

    #self.assertEqual(new_camera, new_camera_DB)
    #self.assertEqual(new_lens, new_lens_DB)
    
    
    
