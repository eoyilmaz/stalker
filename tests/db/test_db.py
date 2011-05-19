#-*- coding: utf-8 -*-



import sys
import os
import datetime
import unittest
import tempfile

import sqlalchemy
from sqlalchemy.orm import clear_mappers
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import select

from stalker.conf import defaults
from stalker import utils
from stalker import db
from stalker.db import tables
from stalker.ext import auth
from stalker.core.errors import LoginError, DBError
from stalker.core.models import (
    Asset,
    AssetType,
    Booking,
    Comment,
    Department,
    Entity,
    SimpleEntity,
    Group,
    ImageFormat,
    Link,
    LinkType,
    Note,
    Project,
    ProjectType,
    Repository,
    Sequence,
    Shot,
    Status,
    StatusList,
    Structure,
    Tag,
    Task,
    TaskType,
    TypeTemplate,
    User,
    Version
)






########################################################################
class DatabaseTester(unittest.TestCase):
    """tests the database and connection to the database
    """
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the tests
        """
        # just set the default admin creation to true
        # some tests are relying on that
        defaults.AUTO_CREATE_ADMIN = True
        defaults.ADMIN_NAME = "admin"
        defaults.ADMIN_PASSWORD = "admin"
        
        #self.TEST_DATABASE_FILE = tempfile.mktemp() + ".db"
        #self.TEST_DATABASE_DIALECT = "sqlite:///"
        #self.TEST_DATABASE_URI = self.TEST_DATABASE_DIALECT + \
            #self.TEST_DATABASE_FILE
        
        self.TEST_DATABASE_URI = "sqlite:///:memory:"
        
        self._createdDB = False
    
    
    
    #----------------------------------------------------------------------
    def tearDown(self):
        """tearDown the tests
        """
        
        #if self._createdDB:
            #try:
                #os.remove(self.TEST_DATABASE_FILE)
            #except OSError:
                #pass
        
        #clear_mappers()
        #db.__mappers__ = []
    
    
    
    #----------------------------------------------------------------------
    def test_creating_a_custom_in_memory_db(self):
        """testing if a custom in-memory sqlite database will be created
        """
        
        # create a database in memory
        db.setup("sqlite:///:memory:")
        #db.setup("sqlite://")
        
        # try to persist a user and get it back
        session = db.session
        query = session.query
        
        # create a new user
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        kwargs = {
            "name": "eoyilmaz",
            "first_name": "Erkan Ozgur",
            "last_name": "Yilmaz",
            "login_name": "eoyilmaz",
            "email": "eoyilmaz@gmail.com",
            "created_by": admin,
            "password": "password",
        }
        
        newUser = User(**kwargs)
        
        session.add(newUser)
        session.commit()
        
        # now check if the newUser is there
        newUser_DB = query(User).\
                   filter_by(name=kwargs["name"]).\
                   filter_by(first_name=kwargs["first_name"]).\
                   filter_by(last_name=kwargs["last_name"]).\
                   first()
        
        self.assertTrue(newUser_DB is not None)
    
    
    
    #----------------------------------------------------------------------
    def test_creating_a_custom_sqlite_db(self):
        """testing if a custom sqlite database will be created in the given
        location
        """
        
        self.TEST_DATABASE_FILE = tempfile.mktemp() + ".db"
        self.TEST_DATABASE_DIALECT = "sqlite:///"
        self.TEST_DATABASE_URI = self.TEST_DATABASE_DIALECT + \
            self.TEST_DATABASE_FILE
        
        # check if there is no file with the same name
        self.assertFalse(os.path.exists(self.TEST_DATABASE_FILE))
        
        # setup the database
        db.setup(self.TEST_DATABASE_URI)
        session = db.session
        query = session.query
        
        # check if the file is created
        self.assertTrue(os.path.exists(self.TEST_DATABASE_FILE))
        
        # create a new user
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        kwargs = {
            "name": "eoyilmaz",
            "first_name": "Erkan Ozgur",
            "last_name": "Yilmaz",
            "login_name": "eoyilmaz",
            "email": "eoyilmaz@gmail.com",
            "created_by": admin,
            "password": "password",
        }
        
        newUser = User(**kwargs)
        
        session.add(newUser)
        session.commit()
        
        # now reconnect and check if the newUser is there
        db.setup(self.TEST_DATABASE_URI)
        
        newUser_DB = query(User).\
                   filter_by(name=kwargs["name"]).\
                   filter_by(first_name=kwargs["first_name"]).\
                   filter_by(last_name=kwargs["last_name"]).\
                   first()
        
        self.assertTrue(newUser_DB is not None)
        
        # delete the temp file
        os.remove(self.TEST_DATABASE_FILE)
    
    
    
    #----------------------------------------------------------------------
    def test_creating_the_default_db(self):
        """testing if default.DATABASE is going to be used for the database
        address when nothgin is given for database in setup
        """
        # setup without any parameter
        db.setup()
        
        drivername = db.engine.url.drivername
        database = db.engine.url.database
        
        full_db_url = drivername + ":///" + database
        
        self.assertEqual(full_db_url, defaults.DATABASE)
    
    
    
    #----------------------------------------------------------------------
    def test_default_admin_creation(self):
        """testing if a default admin is created
        """
        
        # set default admin creation to True
        defaults.AUTO_CREATE_ADMIN = True
        
        db.setup(self.TEST_DATABASE_URI)
        self._createdDB = True
        
        # check if there is an admin
        admin = auth.authenticate(defaults.ADMIN_NAME,defaults.ADMIN_PASSWORD)
        
        self.assertEqual(admin.name, defaults.ADMIN_NAME)
        
    
    
    
    #----------------------------------------------------------------------
    def test_default_admin_for_already_created_databases(self):
        """testing if no extra admin is going to be created for already setup
        databases
        """
        
        # set default admin creation to True
        defaults.AUTO_CREATE_ADMIN = True
        
        db.setup(self.TEST_DATABASE_URI)
        self._createdDB = True
        
        # try to call the db.setup for a second time and see if there are more
        # than one admin
        
        db.setup(self.TEST_DATABASE_URI)
        
        # and get how many admin is created, (it is imipossible to create
        # second one because the tables.simpleEntity.c.nam.unique=True
        
        admins = db.session.query(User). \
               filter_by(name=defaults.ADMIN_NAME).all()
        
        self.assertFalse( len(admins) > 1 )
    
    
    
    #----------------------------------------------------------------------
    def test_auth_authenticate_LogginError_raised(self):
        """testing if stalker.core.models.LoginError will be raised when
        authentication information is wrong
        """
        
        db.setup(self.TEST_DATABASE_URI)
        self._createdDB = True
        
        test_datas = [
            ("",""),
            ("a user name", ""),
            ("", "just a pass"),
            ("no correct user", "wrong pass")
        ]
        
        for user_name, password in test_datas:
            self.assertRaises(
                LoginError,
                auth.authenticate,
                user_name,
                password
            )
    
    
    
    #----------------------------------------------------------------------
    def test_no_default_admin_creation(self):
        """testing if there is no user if default.AUTO_CREATE_ADMIN is False
        """
        
        # turn down auto admin creation
        defaults.AUTO_CREATE_ADMIN = False
        
        # setup the db
        db.setup(self.TEST_DATABASE_URI)
        self._createdDB = True
        
        # check if there is a use with name admin
        self.assertTrue(db.session.query(User).\
                        filter_by(name=defaults.ADMIN_NAME).first()
                        is None )
        
        # check if there is a admins department
        self.assertTrue(db.session.query(Department).\
                        filter_by(name=defaults.ADMIN_DEPARTMENT_NAME).\
                        first() is None)
    
    
    
    #----------------------------------------------------------------------
    def test_unique_names_on_same_entity_type(self):
        """testing if there are unique names for same entity types
        """
        
        db.setup(self.TEST_DATABASE_URI)
        self._createdDB = True
        
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # try to create a user with the same login_name
        # expect IntegrityError
        
        kwargs = {
            "first_name": "user1name",
            "login_name": "user1",
            "email": "user1@gmail.com",
            "password": "user1",
            "created_by": admin
        }
        
        user1 = User(**kwargs)
        db.session.commit()
        
        # lets create the second user
        kwargs.update({
            "email": "user2@gmail.com",
            "login_name": "user1",
        })
        
        user2=User(**kwargs)
        
        self.assertRaises(IntegrityError, db.session.commit)
    
    
    
    #----------------------------------------------------------------------
    def test_non_unique_names_on_different_entity_type(self):
        """testing if there can be non-unique names for different entity types
        """
        
        db.setup(self.TEST_DATABASE_URI)
        self._createdDB = True
        
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # try to create a user and an entity with same name
        # expect Nothing
        
        kwargs = {
            "name": "user1",
            "created_by": admin
        }
        
        entity1 = Entity(**kwargs)
        db.session.commit()
        
        # lets create the second user
        kwargs.update({
            "first_name": "user1name",
            "login_name": "user1",
            "email": "user1@gmail.com",
            "password": "user1",
        })
        
        user1=User(**kwargs)
        
        # expect nothing, this should work without any error
        db.session.commit()
    
    
    
    #----------------------------------------------------------------------
    def test_entity_types_table_is_created_properly(self):
        """testing if the entity_types table is created properly
        """
        
        db.setup()
        
        # check if db.metadata.tables has a table with name entity_types
        self.assertTrue("entity_types", db.metadata.tables)
    
    
    
    #----------------------------------------------------------------------
    def test_entity_types_table_is_filled_with_the_default_classes(self):
        """testing if the entity_types table is filled with the entity_types
        comming from the core.classes
        """
        
        db.setup()
        #self._createdDB = True
        
        # get the DEFAULTS.CORE_MODEL_CLASSES and create a list containing the
        # entity types of each of the classes
        
        entity_types = []
        
        for full_module_path in defaults.CORE_MODEL_CLASSES:
            import_info = utils.path_to_exec(full_module_path)
            
            exec_ = import_info[0]
            module = import_info[1]
            object_ = import_info[2]
            
            # execute the imports
            exec(exec_)
            
            # store the class.entity_names
            entity_types.append(eval(object_ + ".entity_type"))
        
        # check if all the entity_types are in the table
        
        # get the table content
        conn = db.engine.connect()
        s = select([tables.EntityTypes.c.entity_type])
        result = conn.execute(s)
        
        entity_types_DB = []
        for row in result:
            entity_types_DB.append( row[0] )
        
        result.close()
        
        
        # now check for all the elements
        self.assertTrue(
            all([entity_type in entity_types_DB
                 for entity_type in entity_types])
        )
    
    
    
    ##----------------------------------------------------------------------
    #def test_entity_types_table_contains_the_extension_classes(self):
        #"""testing if the entity_types table contains the user extended classes
        #"""
        
        ## create a new data type by extendind stalker.core.models (in a way
        ## that is not implemented yet)
        
        ## then check if the entity_type is listed in the entity_types table
        
        #self.fail("test is not implemented yet")






########################################################################
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
    
    
    
    #----------------------------------------------------------------------
    #@classmethod
    #def setUpClass(cls):
        #"""setup the test
        #"""
        
        ### setup the database
        ##clear_mappers()
        ##db.__mappers__ = []
        
        ### create a test database, possibly an in memory datase
        ##cls.TEST_DATABASE_FILE = tempfile.mktemp() + ".db"
        ##cls.TEST_DATABASE_URI = "sqlite:///" + cls.TEST_DATABASE_FILE
        
        ### setup using this db
        ##db.setup(database=cls.TEST_DATABASE_URI)
        
        #cls.TEST_DATABASE_FILE = ":memory:"
        #cls.TEST_DATABASE_URI = "sqlite:///" + cls.TEST_DATABASE_FILE
        
        
        ## setup using this db
        #db.setup(database=cls.TEST_DATABASE_URI)
    
    
    
    ##----------------------------------------------------------------------
    #@classmethod
    #def tearDownClass(cls):
        #"""tear-off the test
        #"""
        ## delete the default test database file
        #os.remove(cls.TEST_DATABASE_FILE)
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        ## create a test database, possibly an in memory datase
        self.TEST_DATABASE_FILE = tempfile.mktemp() + ".db"
        #self.TEST_DATABASE_URI = "sqlite:///" + self.TEST_DATABASE_FILE
        
        #self.TEST_DATABASE_FILE = ":memory:"
        self.TEST_DATABASE_URI = "sqlite:///" + self.TEST_DATABASE_FILE
        
        # setup using this db
        db.setup(database=self.TEST_DATABASE_URI)
    
    
    
    ##----------------------------------------------------------------------
    #def tearDown(self):
        #"""tear-off the test
        #"""
        ### delete the default test database file
        ##os.remove(self.TEST_DATABASE_FILE)
        
        #db.metadata.drop_all(db.engine)
        #clear_mappers()
        #db.engine.dispose()
        #db.session.close()
        #db.__mappers__ = []
        
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Asset(self):
        """testing the persistence of Asset
        """
        
        asset_type = AssetType(name="A new AssetType")
        
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Completed", code="CMPLT")
        status3 = Status(name="Work In Progress", code="WIP")
        
        task_status_list = StatusList(
            name="Task Status List",
            statuses=[status1, status2, status3],
            target_entity_type=Task.entity_type
        )
        
        mock_task1 = Task(name="test task 1", status=0,
                          status_list=task_status_list)
        mock_task2 = Task(name="test task 2", status=0,
                          status_list=task_status_list)
        mock_task3 = Task(name="test task 3", status=0,
                          status_list=task_status_list)
        
        asset_statusList = StatusList(
            name="Asset Status List",
            statuses=[status1, status2, status3],
            target_entity_type=Asset.entity_type
        )
        
        project_statusList = StatusList(
            name="Project Status List",
            statuses=[status1, status2, status3],
            target_entity_type="Project"
        )
        
        mock_project = Project(name="Test Project",
                               status_list=project_statusList,
                               status=0)
        
        kwargs = {
            "name": "Test Asset",
            "description": "This is a test Asset object",
            "type": asset_type,
            "tasks": [mock_task1, mock_task2, mock_task3],
            "project": mock_project,
            "status": 0,
            "status_list": asset_statusList,
        }
        
        test_asset = Asset(**kwargs)
        
        db.session.add(test_asset)
        db.session.commit()
        
        # create a couple of shots
        sequence_status_list = StatusList(
            name="Sequence Statuses",
            statuses=[status1, status2, status3],
            target_entity_type="Sequence"
        )
        
        mock_sequence = Sequence(name="Test Sequence",
                                 project=mock_project,
                                 status=0,
                                 status_list=sequence_status_list)
        
        shot_status_list = StatusList(
            name="Shot Statuses",
            statuses=[status1, status2, status3],
            target_entity_type="Shot",
        )
        
        mock_shot1 = Shot(code="SH001",
                          sequence=mock_sequence,
                          status=0,
                          status_list=shot_status_list)
        
        mock_shot2 = Shot(code="SH002",
                          sequence=mock_sequence,
                          status=0,
                          status_list=shot_status_list)
        
        mock_shot3 = Shot(code="SH003",
                          sequence=mock_sequence,
                          status=0,
                          status_list=shot_status_list)
        
        test_asset.shots = [mock_shot1, mock_shot2, mock_shot3]
        
        db.session.add_all([mock_shot1, mock_shot2, mock_shot3])
        db.session.commit()
        
        test_asset_DB = db.query(Asset).\
                      filter_by(name=kwargs["name"]).one()
        
        assert(isinstance(test_asset_DB, Asset))
        
        self.assertEqual(test_asset, test_asset_DB)
        self.assertEqual(test_asset.code, test_asset_DB.code)
        self.assertEqual(test_asset.created_by, test_asset_DB.created_by)
        self.assertEqual(test_asset.date_created, test_asset_DB.date_created)
        self.assertEqual(test_asset.date_updated, test_asset_DB.date_updated)
        self.assertEqual(test_asset.description, test_asset_DB.description)
        self.assertEqual(test_asset.name, test_asset_DB.name)
        self.assertEqual(test_asset.nice_name, test_asset_DB.nice_name)
        self.assertEqual(test_asset.notes, test_asset_DB.notes)
        self.assertEqual(test_asset.project, test_asset_DB.project)
        self.assertEqual(test_asset.references, test_asset_DB.references)
        self.assertEqual(test_asset.shots, test_asset_DB.shots)
        self.assertEqual(test_asset.status, test_asset_DB.status)
        self.assertEqual(test_asset.status_list, test_asset_DB.status_list)
        self.assertEqual(test_asset.tags, test_asset_DB.tags)
        self.assertEqual(test_asset.tasks, test_asset_DB.tasks)
        self.assertEqual(test_asset.type, test_asset_DB.type)
        self.assertEqual(test_asset.updated_by, test_asset_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_AssetType(self):
        """testing the persistence of AssetType
        """
        
        # first get the admin
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create a couple of PipelineStep objects
        tType1 = TaskType(
            name="Rigging",
            description="This is where a character asset is rigged",
            created_by=admin,
            updated_by=admin,
            code="RIG"
        )
        
        tType2 = TaskType(
            name="Lighting",
            description="lighting done in this stage, don't mix it with \
            shading",
            created_by=admin,
            updated_by=admin,
            code="LGHT"
        )
        
        # create a new AssetType object
        kwargs = {
            "name": "Character",
            "description": "this is a test asset type",
            "created_by": admin,
            "updated_by": admin,
            "task_types": [tType1, tType2],
        }
        
        aType = AssetType(**kwargs)
        
        # store it in the db
        db.session.add(aType)
        db.session.commit()
        
        # retrieve it back and check it with the first one
        aType_DB = db.session.query(AssetType). \
                 filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(aType_DB, AssetType))
        
        self.assertEqual(aType, aType_DB)
        self.assertEqual(aType.code, aType_DB.code)
        self.assertEqual(aType.created_by, aType_DB.created_by)
        self.assertEqual(aType.date_created, aType_DB.date_created)
        self.assertEqual(aType.date_updated, aType_DB.date_updated)
        self.assertEqual(aType.description, aType_DB.description)
        self.assertEqual(aType.name, aType_DB.name)
        self.assertEqual(aType.nice_name, aType_DB.nice_name)
        self.assertEqual(aType.notes, aType_DB.notes)
        self.assertEqual(aType.tags, aType_DB.tags)
        self.assertEqual(aType.task_types, aType_DB.task_types)
        self.assertEqual(aType.updated_by, aType_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Booking(self):
        """testing the persistence of Booking
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Comment(self):
        """testing the persistence of Comment
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Department(self):
        """testing the persistence of Department
        """
        
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
        
        db.session.add(test_dep)
        db.session.commit()
        
        # lets check the data
        # first get the department from the db
        test_dep_db = db.session.query(Department). \
                    filter_by(name=test_dep.name).first()
        
        assert(isinstance(test_dep_db, Department))
        
        self.assertEqual(test_dep, test_dep_db)
        self.assertEqual(test_dep.code, test_dep_db.code)
        self.assertEqual(test_dep.created_by, test_dep_db.created_by)
        self.assertEqual(test_dep.date_created, test_dep_db.date_created)
        self.assertEqual(test_dep.date_updated, test_dep_db.date_updated)
        self.assertEqual(test_dep.description, test_dep_db.description)
        self.assertEqual(test_dep.lead, test_dep_db.lead)
        self.assertEqual(test_dep.members, test_dep_db.members)
        self.assertEqual(test_dep.name, test_dep_db.name)
        self.assertEqual(test_dep.nice_name, test_dep_db.nice_name)
        self.assertEqual(test_dep.notes, test_dep_db.notes)
        self.assertEqual(test_dep.tags, test_dep_db.tags)
        self.assertEqual(test_dep.updated_by, test_dep_db.updated_by)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Entity(self):
        """testing the persistence of Entity
        """
        
        # create an Entity wiht a couple of tags
        
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
            date_updated=date_updated)
        
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
            date_updated=date_updated)
        
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
        )
        
        # persist it to the database
        db.session.add(test_entity)
        db.session.commit()
        
        # now try to retrieve it
        test_entity_DB = db.session.query(Entity). \
                     filter_by(name=name).first()
        
        assert(isinstance(test_entity_DB, Entity))
        
        self.assertEqual(test_entity, test_entity_DB)
        self.assertEqual(test_entity.code, test_entity_DB.code)
        self.assertEqual(test_entity.created_by, test_entity_DB.created_by)
        self.assertEqual(test_entity.date_created, test_entity_DB.date_created)
        self.assertEqual(test_entity.date_updated, test_entity_DB.date_updated)
        self.assertEqual(test_entity.description, test_entity_DB.description)
        self.assertEqual(test_entity.name, test_entity_DB.name)
        self.assertEqual(test_entity.nice_name, test_entity_DB.nice_name)
        self.assertEqual(test_entity.notes, test_entity_DB.notes)
        self.assertEqual(test_entity.tags, test_entity_DB.tags)
        self.assertEqual(test_entity.updated_by, test_entity_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Group(self):
        """testing the persistence of Group
        """
        
        self.fail("test is not implmented yet")
    
    
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_ImageFormat(self):
        """testing the persistence of ImageFormat
        """
        
        # get the admin
        session = db.session
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create a new ImageFormat object and try to read it back
        kwargs = {
        "name": "HD",
        "description": "test image format",
        "created_by": admin,
        "updated_by": admin,
        "width": 1920,
        "height": 1080,
        "pixel_aspect": 1.0,
        "print_resolution": 300.0
        }
        
        # create the ImageFormat object
        im_format = ImageFormat(**kwargs)
        
        # persist it
        session.add(im_format)
        session.commit()
        
        # get it back
        im_format_DB = session.query(ImageFormat). \
                filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(im_format_DB, ImageFormat))
        
        # just test the repository part of the attributes
        self.assertEqual(im_format, im_format_DB)
        self.assertEqual(im_format.code, im_format_DB.code)
        self.assertEqual(im_format.created_by, im_format_DB.created_by)
        self.assertEqual(im_format.date_created, im_format_DB.date_created)
        self.assertEqual(im_format.date_updated, im_format_DB.date_updated)
        self.assertEqual(im_format.description, im_format_DB.description)
        self.assertEqual(im_format.device_aspect, im_format_DB.device_aspect)
        self.assertEqual(im_format.height, im_format_DB.height)
        self.assertEqual(im_format.name, im_format_DB.name)
        self.assertEqual(im_format.nice_name, im_format_DB.nice_name)
        self.assertEqual(im_format.notes, im_format_DB.notes)
        self.assertEqual(im_format.pixel_aspect, im_format_DB.pixel_aspect)
        self.assertEqual(im_format.print_resolution,
                         im_format_DB.print_resolution)
        self.assertEqual(im_format.tags, im_format_DB.tags)
        self.assertEqual(im_format.updated_by, im_format_DB.updated_by)
        self.assertEqual(im_format.width, im_format_DB.width)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Link(self):
        """testing the persistence of Link
        """
        
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create a LinkType
        sound_link_type = LinkType(
            name="Sound",
            created_by=admin
        )
        
        # create a Link
        kwargs = {
            "name": "My Sound",
            "created_by": admin,
            "path": "M:/PROJECTS",
            "filename": "my_movie_sound.wav",
            "type": sound_link_type
        }
        
        new_link = Link(**kwargs)
        
        # persist it
        db.session.add_all([sound_link_type, new_link])
        db.session.commit()
        
        # retrieve it back
        new_link_DB = db.session.query(Link).\
                filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(new_link_DB, Link))
        
        self.assertEqual(new_link, new_link_DB)
        self.assertEqual(new_link.code, new_link_DB.code)
        self.assertEqual(new_link.created_by, new_link_DB.created_by)
        self.assertEqual(new_link.date_created, new_link_DB.date_created)
        self.assertEqual(new_link.date_updated, new_link_DB.date_updated)
        self.assertEqual(new_link.description, new_link_DB.description)
        self.assertEqual(new_link.filename, new_link_DB.filename)
        self.assertEqual(new_link.name, new_link_DB.name)
        self.assertEqual(new_link.nice_name, new_link_DB.nice_name)
        self.assertEqual(new_link.notes, new_link_DB.notes)
        self.assertEqual(new_link.path, new_link_DB.path)
        self.assertEqual(new_link.tags, new_link_DB.tags)
        self.assertEqual(new_link.type, new_link_DB.type)
        self.assertEqual(new_link.updated_by, new_link_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
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
        
        db.session.add_all([test_entity, test_note])
        db.session.commit()
        
        # try to get the note directly
        
        test_note_DB = db.query(Note).\
                     filter(Note.name==note_kwargs["name"]).first()
        
        assert(isinstance(test_note_DB, Note))
        
        # try to get the note from the entity
        test_entity_DB = db.query(Entity).\
                      filter(Entity.name==entity_kwargs["name"]).first()
        
        self.assertEqual(test_note, test_entity_DB.notes[0])
        
        self.assertEqual(test_note, test_note_DB)
        self.assertEqual(test_note.code, test_note_DB.code)
        self.assertEqual(test_note.content, test_note_DB.content)
        self.assertEqual(test_note.created_by, test_note_DB.created_by)
        self.assertEqual(test_note.date_created, test_note_DB.date_created)
        self.assertEqual(test_note.date_updated, test_note_DB.date_updated)
        self.assertEqual(test_note.description, test_note_DB.description)
        self.assertEqual(test_note.name, test_note_DB.name)
        self.assertEqual(test_note.nice_name, test_note_DB.nice_name)
        self.assertEqual(test_note.updated_by, test_note_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_TaskType(self):
        """testing the persistence of TaskType
        """
        
        # create a new TaskType
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        kwargs = {
            "name": "RENDER",
            "description": "this is the step where all the assets are \
            rendered",
            "created_by": admin,
            "code": "RNDR"
        }
        
        tType = TaskType(**kwargs)
        
        # save it to database
        db.session.add(tType)
        
        # retrieve it back
        tType_DB = db.session.query(TaskType). \
                 filter_by(name=kwargs["name"]). \
                 filter_by(description=kwargs["description"]). \
                 first()
        
        assert(isinstance(tType_DB, TaskType))
        
        # lets compare it
        self.assertEqual(tType, tType_DB)
        self.assertEqual(tType.code, tType_DB.code)
        self.assertEqual(tType.created_by, tType_DB.created_by)
        self.assertEqual(tType.date_created, tType_DB.date_created)
        self.assertEqual(tType.date_updated, tType_DB.date_updated)
        self.assertEqual(tType.description, tType_DB.description)
        self.assertEqual(tType.name, tType_DB.name)
        self.assertEqual(tType.nice_name, tType_DB.nice_name)
        self.assertEqual(tType.notes, tType_DB.notes)
        self.assertEqual(tType.tags, tType_DB.tags)
        self.assertEqual(tType.updated_by, tType_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Project(self):
        """testing the persistence of Project
        """
        
        # create mock objects
        start_date = datetime.date.today()
        due_date = start_date + datetime.timedelta(days=20)
        
        lead = User(login_name="lead", first_name="lead", last_name="lead",
                    email="lead@lead.com", password="password")
        
        user1 = User(login_name="user1", first_name="user1", last_name="user1",
                     email="user1@user1.com", password="password")
        user2 = User(login_name="user2", first_name="user2", last_name="user2",
                     email="user1@user2.com", password="password")
        user3 = User(login_name="user3", first_name="user3", last_name="user3",
                     email="user3@user3.com", password="password")
        
        image_format = ImageFormat(name="HD", width=1920, height=1080)
        
        project_type = ProjectType(name="Commercial")
        
        project_structure = Structure(
            name="Commercial Structure",
            project_template="{{project.code}}\n"
            "{{project.code}}/ASSETS\n"
            "{{project.code}}/SEQUENCES\n"
        )
        
        repo = Repository(name="Commercials Repository",
                          linux_path="/mnt/M/Projects",
                          windows_path="M:\\Projects",
                          osx_path="/Volumes/M/Projects")
        
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Complete", code="CMPLT")
        
        project_status_list = StatusList(
            name="A Status List for testing Project",
            statuses=[status1, status2],
            target_entity_type=Project.entity_type
        )
        
        db.session.add(project_status_list)
        db.session.commit()
        
        # create data for mixins
        # Reference Mixin
        link_type = LinkType(name="Image")
        ref1 = Link(name="Ref1", path="/mnt/M/JOBs/TEST_PROJECT",
                    filename="1.jpg", type=link_type)
        ref2 = Link(name="Ref2", path="/mnt/M/JOBs/TEST_PROJECT",
                    filename="1.jpg", type=link_type)
        
        # TaskMixin
        task_status_list = StatusList(
            name="Task Statuses",
            statuses=[status1, status2],
            target_entity_type=Task.entity_type
        )
        
        db.session.add(task_status_list)
        db.session.commit()
        
        task1 = Task(name="task1", status_list=task_status_list, status=0)
        task2 = Task(name="task2", status_list=task_status_list, status=0)
        
        db.session.add_all([ref1, ref2, task1, task2])
        db.session.commit()
        
        # create a project object
        kwargs = {
            "name": "Test Project",
            "description": "This is a project object for testing purposes",
            "lead": lead,
            "users": [user1, user2, user3],
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
            "tasks": [task1, task2],
        }
        
        new_project = Project(**kwargs)
        
        # persist it in the database
        db.session.add(new_project)
        db.session.commit()
        
        # now get it
        new_project_DB = db.query(Project).\
                       filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(new_project_DB, Project))
        
        self.assertEqual(new_project, new_project_DB)
        self.assertEqual(new_project.assets, new_project_DB.assets)
        self.assertEqual(new_project.code, new_project_DB.code)
        self.assertEqual(new_project.created_by, new_project_DB.created_by)
        self.assertEqual(new_project.date_created, new_project_DB.date_created)
        self.assertEqual(new_project.date_updated, new_project_DB.date_updated)
        self.assertEqual(new_project.description, new_project_DB.description)
        self.assertEqual(new_project.display_width,
                         new_project_DB.display_width)
        self.assertEqual(new_project.due_date, new_project_DB.due_date)
        self.assertEqual(new_project.duration, new_project_DB.duration)
        self.assertEqual(new_project.fps, new_project_DB.fps)
        self.assertEqual(new_project.image_format, new_project_DB.image_format)
        self.assertEqual(new_project.is_stereoscopic,
                         new_project_DB.is_stereoscopic)
        self.assertEqual(new_project.lead, new_project_DB.lead)
        self.assertEqual(new_project.name, new_project_DB.name)
        self.assertEqual(new_project.nice_name, new_project_DB.nice_name)
        self.assertEqual(new_project.notes, new_project_DB.notes)
        self.assertEqual(new_project.references, new_project_DB.references)
        self.assertEqual(new_project.repository, new_project_DB.repository)
        self.assertEqual(new_project.sequences, new_project_DB.sequences)
        self.assertEqual(new_project.start_date, new_project_DB.start_date)
        self.assertEqual(new_project.status, new_project_DB.status)
        self.assertEqual(new_project.status_list, new_project_DB.status_list)
        self.assertEqual(new_project.structure, new_project_DB.structure)
        self.assertEqual(new_project.tags, new_project_DB.tags)
        self.assertEqual(new_project.tasks, new_project_DB.tasks)
        self.assertEqual(new_project.type, new_project_DB.type)
        self.assertEqual(new_project.updated_by, new_project.updated_by)
        self.assertEqual(new_project.users, new_project_DB.users)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Repository(self):
        """testing the persistence of Repository
        """
        
        # get the admin
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create a new Repository object and try to read it back
        kwargs = {
        "name": "Movie-Repo",
        "description": "test repository",
        "created_by": admin,
        "updated_by": admin,
        "linux_path": "/mnt/M",
        "osx_path": "/Volumes/M",
        "windows_path": "M:\\"
        }
        
        # create the repository object
        repo = Repository(**kwargs)
        
        # persist it
        db.session.add(repo)
        db.session.commit()
        
        # get it back
        repo_db = db.query(Repository).\
                  filter_by(name=kwargs["name"]).\
                  first()
        
        assert(isinstance(repo_db, Repository))
        
        self.assertEqual(repo.code, repo_db.code)
        self.assertEqual(repo.created_by, repo_db.created_by)
        self.assertEqual(repo.date_created, repo_db.date_created)
        self.assertEqual(repo.date_updated, repo_db.date_updated)
        self.assertEqual(repo.description, repo_db.description)
        self.assertEqual(repo.linux_path, repo_db.linux_path)
        self.assertEqual(repo.name, repo_db.name)
        self.assertEqual(repo.nice_name, repo_db.nice_name)
        self.assertEqual(repo.notes, repo_db.notes)
        self.assertEqual(repo.osx_path, repo_db.osx_path)
        self.assertEqual(repo.path, repo_db.path)
        self.assertEqual(repo.tags, repo_db.tags)
        self.assertEqual(repo.updated_by, repo_db.updated_by)
        self.assertEqual(repo.windows_path, repo_db.windows_path)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Sequence(self):
        """testing the persistence of Sequence
        """
        
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Work In Progress", code="WIP")
        status3 = Status(name="Finished", code="FIN")
        
        project_status_list = StatusList(
            name="Project Statuses",
            statuses=[status1, status2, status3],
            target_entity_type = Project.entity_type
        )
        
        sequence_status_list = StatusList(
            name="Sequence Statuses",
            statuses=[status1, status2, status3],
            target_entity_type = Sequence.entity_type
        )
        
        shot_status_list = StatusList(
            name="Shot Statuses",
            statuses=[status1, status2, status3],
            target_entity_type = Shot.entity_type
        )
        
        project1 = Project(name="Test project",
                                   status_list=project_status_list)
        
        lead = User(login_name="lead", email="lead@lead.com",
                    first_name="lead", last_name="lead", password="password")
        
        kwargs = {
            "name": "Test sequence",
            "description": "this is a test sequence",
            "project": project1,
            "lead": lead,
            #"shots": [shot1, shot2, shot3],
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
        
        db.session.add(test_sequence)
        db.session.commit()
        
        test_sequence_DB = db.query(Sequence).\
                         filter_by(name=kwargs["name"]).one()
        
        self.assertEqual(test_sequence, test_sequence_DB)
        self.assertEqual(test_sequence.code, test_sequence_DB.code)
        self.assertEqual(test_sequence.created_by, test_sequence_DB.created_by)
        self.assertEqual(test_sequence.date_created,
                         test_sequence_DB.date_created)
        self.assertEqual(test_sequence.date_updated,
                         test_sequence_DB.date_updated)
        self.assertEqual(test_sequence.description,
                         test_sequence_DB.description)
        self.assertEqual(test_sequence.due_date, test_sequence_DB.due_date)
        self.assertEqual(test_sequence.duration, test_sequence_DB.duration)
        self.assertEqual(test_sequence.lead, test_sequence_DB.lead)
        self.assertEqual(test_sequence.name, test_sequence_DB.name)
        self.assertEqual(test_sequence.nice_name, test_sequence_DB.nice_name)
        self.assertEqual(test_sequence.notes, test_sequence_DB.notes)
        self.assertEqual(test_sequence.project, test_sequence_DB.project)
        self.assertEqual(test_sequence.references, test_sequence_DB.references)
        self.assertEqual(test_sequence.shots, test_sequence_DB.shots)
        self.assertEqual(test_sequence.start_date, test_sequence_DB.start_date)
        self.assertEqual(test_sequence.status, test_sequence_DB.status)
        self.assertEqual(test_sequence.status_list,
                         test_sequence_DB.status_list)
        self.assertEqual(test_sequence.tags, test_sequence_DB.tags)
        self.assertEqual(test_sequence.tasks, test_sequence_DB.tasks)
        self.assertEqual(test_sequence.updated_by, test_sequence_DB.updated_by)
        
        
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Shot(self):
        """testing the persistence of Shot
        """
        
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Work In Progress", code="WIP")
        status3 = Status(name="Finished", code="FIN")
        
        project_status_list = StatusList(
            name="Project Statuses",
            statuses=[status1, status2, status3],
            target_entity_type = Project.entity_type
        )
        
        sequence_status_list = StatusList(
            name="Sequence Statuses",
            statuses=[status1, status2, status3],
            target_entity_type = Sequence.entity_type
        )
        
        shot_status_list = StatusList(
            name="Shot Statuses",
            statuses=[status1, status2, status3],
            target_entity_type = Shot.entity_type
        )
        
        project1 = Project(name="Test project",
                           status_list=project_status_list)
        
        lead = User(login_name="lead", email="lead@lead.com",
                    first_name="lead", last_name="lead", password="password")
        
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
        
        db.session.add(test_shot)
        db.session.add(test_sequence)
        db.session.commit()
        
        test_shot_DB = db.query(Shot).\
                     filter_by(code=shot_kwargs["code"]).first()
        
        self.assertEqual(test_shot, test_shot_DB)
        self.assertEqual(test_shot.assets, test_shot_DB.assets)
        self.assertEqual(test_shot.code, test_shot_DB.code)
        self.assertEqual(test_shot.cut_duration, test_shot_DB.cut_duration)
        self.assertEqual(test_shot.cut_in, test_shot_DB.cut_in)
        self.assertEqual(test_shot.cut_out, test_shot_DB.cut_out)
        self.assertEqual(test_shot.date_created, test_shot_DB.date_created)
        self.assertEqual(test_shot.date_updated, test_shot_DB.date_updated)
        self.assertEqual(test_shot.description, test_shot_DB.description)
        self.assertEqual(test_shot.name, test_shot_DB.name)
        self.assertEqual(test_shot.nice_name, test_shot_DB.nice_name)
        self.assertEqual(test_shot.notes, test_shot_DB.notes)
        self.assertEqual(test_shot.references, test_shot_DB.references)
        self.assertEqual(test_shot.sequence, test_shot_DB.sequence)
        self.assertEqual(test_shot.status, test_shot_DB.status)
        self.assertEqual(test_shot.status_list, test_shot_DB.status_list)
        self.assertEqual(test_shot.tags, test_shot_DB.tags)
        self.assertEqual(test_shot.tasks, test_shot_DB.tasks)
        self.assertEqual(test_shot.updated_by, test_shot_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_SimpleEntity(self):
        """testing the persistence of SimpleEntity
        """
        
        kwargs = {
            "name": "SimpleEntity_test_creating_of_a_SimpleEntity",
            "description": "this is for testing purposes",
        }
        
        test_simple_entity = SimpleEntity(**kwargs)
        
        # persist it to the database
        db.session.add(test_simple_entity)
        db.session.commit()
        
        # now try to retrieve it
        test_simple_entity_DB = db.session.query(SimpleEntity).\
            filter(SimpleEntity.name==kwargs["name"]).first()
        
        assert(isinstance(test_simple_entity_DB, SimpleEntity))
        
        self.assertEqual(test_simple_entity, test_simple_entity_DB)
        self.assertEqual(test_simple_entity.code, test_simple_entity_DB.code)
        self.assertEqual(test_simple_entity.created_by,
                         test_simple_entity_DB.created_by)
        self.assertEqual(test_simple_entity.date_created,
                         test_simple_entity_DB.date_created)
        self.assertEqual(test_simple_entity.date_updated,
                         test_simple_entity_DB.date_updated)
        self.assertEqual(test_simple_entity.description,
                         test_simple_entity_DB.description)
        self.assertEqual(test_simple_entity.name, test_simple_entity_DB.name)
        self.assertEqual(test_simple_entity.nice_name,
                         test_simple_entity_DB.nice_name)
        self.assertEqual(test_simple_entity.updated_by,
                         test_simple_entity_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
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
        db.session.add(test_status)
        db.session.commit()
        
        # now try to retrieve it
        test_status_DB = db.query(Status).\
                     filter(Status.name==kwargs["name"]).first()
        
        assert(isinstance(test_status_DB, Status))
        
        # just test the satuts part of the object
        self.assertEqual(test_status, test_status_DB)
        self.assertEqual(test_status.code, test_status_DB.code)
        self.assertEqual(test_status.created_by, test_status_DB.created_by)
        self.assertEqual(test_status.date_created, test_status_DB.date_created)
        self.assertEqual(test_status.date_updated, test_status_DB.date_updated)
        self.assertEqual(test_status.description, test_status_DB.description)
        self.assertEqual(test_status.name, test_status_DB.name)
        self.assertEqual(test_status.nice_name, test_status_DB.nice_name)
        self.assertEqual(test_status.notes, test_status_DB.notes)
        self.assertEqual(test_status.tags, test_status_DB.tags)
        self.assertEqual(test_status.updated_by, test_status_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
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
        
        # send it to db
        db.session.add(sequence_status_list)
        db.session.commit()
        
        # now get it back
        sequence_status_list_DB = db.query(StatusList).\
                                filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(sequence_status_list_DB, StatusList))
        
        self.assertEqual(sequence_status_list, sequence_status_list_DB)
        self.assertEqual(sequence_status_list.code,
                         sequence_status_list_DB.code)
        self.assertEqual(sequence_status_list.created_by,
                         sequence_status_list_DB.created_by)
        self.assertEqual(sequence_status_list.date_created,
                         sequence_status_list_DB.date_created)
        self.assertEqual(sequence_status_list.date_updated,
                         sequence_status_list_DB.date_updated)
        self.assertEqual(sequence_status_list.description,
                         sequence_status_list_DB.description)
        self.assertEqual(sequence_status_list.name,
                         sequence_status_list_DB.name)
        self.assertEqual(sequence_status_list.nice_name,
                         sequence_status_list_DB.nice_name)
        self.assertEqual(sequence_status_list.notes,
                         sequence_status_list_DB.notes)
        self.assertEqual(sequence_status_list.statuses,
                         sequence_status_list_DB.statuses)
        self.assertEqual(sequence_status_list.tags,
                         sequence_status_list_DB.tags)
        self.assertEqual(sequence_status_list.target_entity_type,
                         sequence_status_list_DB.target_entity_type)
        self.assertEqual(sequence_status_list.updated_by,
                         sequence_status_list_DB.updated_by)
        
        # try to create another StatusList for the same target_entity_type
        # and expect and IntegrityError
        
        kwargs["name"] = "new Sequence Status List"
        new_sequence_list = StatusList(**kwargs)
        
        db.session.add(new_sequence_list)
        self.assertRaises(IntegrityError, db.session.commit)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Structure(self):
        """testing the persistence of Structure
        """
        
        session = db.session
        query = session.query
        
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create pipeline steps for character
        modeling_tType = TaskType(
            name="Modeling",
            description="This is the step where all the modeling job is done",
            code="MODEL",
            created_by=admin
        )
        
        animation_tType = TaskType(
            name="Animation",
            description="This is the step where all the animation job is " + \
                        "done it is not limited with characters, other " + \
                        "things can also be animated",
            code="ANIM",
            created_by=admin
        )
        
        # create a new assetType
        char_asset_type = AssetType(
            name="Character Asset Type",
            description="This is the asset type which covers animated " + \
                        "charactes",
            created_by=admin,
            task_types= [modeling_tType, animation_tType]
        )
        
        # create a new type template for character assets
        assetTemplate = TypeTemplate(
            name="Character Asset Template",
            description="This is the template for character assets",
            path_code="ASSETS/{{asset_type.name}}/{{pipeline_step.code}}",
            file_code="{{asset.name}}_{{take.name}}_{{asset_type.name}}_\
            v{{version.version_number}}",
            type=char_asset_type
        )
        
        # create a new link type
        image_link_type = LinkType(
            name="Image",
            description="It is used for links showing an image",
            created_by=admin
        )
        
        # create a new template for references
        imageReferenceTemplate = TypeTemplate(
            name="Image Reference Template",
            description="this is the template for image references, it " + \
                        "shows where to place the image files",
            created_by=admin,
            path_code="REFS/{{reference.type.name}}",
            file_code="{{reference.file_name}}",
            type=image_link_type
        )
        
        # create a new structure
        kwargs = {
            "name": "Commercial Structure",
            "description": "The structure for commercials",
            "created_by": admin,
            "project_template": """ASSETS
            SEQUENCES
            SEQUENCES/{% for sequence in project.sequences %}
            {{sequence.code}}""",
            "asset_templates": [assetTemplate],
            "reference_template": [imageReferenceTemplate]
        }
        
        new_structure = Structure(**kwargs)
        
        db.session.add(new_structure)
        db.session.commit()
        
        new_structure_DB = db.query(Structure).\
                         filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(new_structure_DB, Structure))
        
        self.assertEqual(new_structure, new_structure_DB)
        self.assertEqual(new_structure.asset_templates,
                         new_structure_DB.asset_templates)
        self.assertEqual(new_structure.code, new_structure_DB.code)
        self.assertEqual(new_structure.created_by, new_structure_DB.created_by)
        self.assertEqual(new_structure.date_created,
                         new_structure_DB.date_created)
        self.assertEqual(new_structure.date_updated,
                         new_structure_DB.date_updated)
        self.assertEqual(new_structure.description,
                         new_structure_DB.description)
        self.assertEqual(new_structure.name, new_structure_DB.name)
        self.assertEqual(new_structure.nice_name, new_structure_DB.nice_name)
        self.assertEqual(new_structure.notes, new_structure_DB.notes)
        self.assertEqual(new_structure.project_template,
                         new_structure_DB.project_template)
        self.assertEqual(new_structure.reference_templates,
                         new_structure_DB.reference_templates)
        self.assertEqual(new_structure.tags, new_structure_DB.tags)
        self.assertEqual(new_structure.updated_by, new_structure_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
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
        db.session.add(aTag)
        db.session.commit()
        
        # now try to retrieve it
        tag_query = db.session.query(Tag)
        Tag_from_DB = tag_query.filter_by(name=name).first()
        
        self.assertEqual(aTag.name, Tag_from_DB.name)
        self.assertEqual(aTag.description, Tag_from_DB.description)
        self.assertEqual(aTag.created_by, Tag_from_DB.created_by)
        self.assertEqual(aTag.updated_by, Tag_from_DB.updated_by)
        self.assertEqual(aTag.date_created, Tag_from_DB.date_created)
        self.assertEqual(aTag.date_updated, Tag_from_DB.date_updated)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Task(self):
        """testing the persistence of Task
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_TypeTemplate(self):
        """testing the persistence of TypeTemplate
        """
        
        # get the admin
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create a LinkType object
        movie_link_type = LinkType(
            name="Movie",
            created_by=admin
        )
        
        # create a TypeTemplate object for movie links
        kwargs = {
            "name": "Movie Links Template",
            "description": "this is a template to be used for links to movie"
                           "files",
            "created_by": admin,
            "path_code": "REFS/{{link_type.name}}",
            "file_code": "{{link.file_name}}",
            "type": movie_link_type,
        }
        
        new_type_template = TypeTemplate(**kwargs)
        
        # persist it
        session = db.session
        session.add(new_type_template)
        session.commit()
        
        # get it back
        new_type_template_DB = session.query(TypeTemplate).\
                             filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(new_type_template_DB, TypeTemplate))
        
        self.assertEqual(new_type_template, new_type_template_DB)
        self.assertEqual(new_type_template.code, new_type_template_DB.code)
        self.assertEqual(new_type_template.created_by,
                         new_type_template_DB.created_by)
        self.assertEqual(new_type_template.date_created,
                         new_type_template_DB.date_created)
        self.assertEqual(new_type_template.date_updated,
                         new_type_template_DB.date_updated)
        self.assertEqual(new_type_template.description,
                         new_type_template_DB.description)
        self.assertEqual(new_type_template.file_code,
                         new_type_template_DB.file_code)
        self.assertEqual(new_type_template.name, new_type_template_DB.name)
        self.assertEqual(new_type_template.nice_name,
                         new_type_template_DB.nice_name)
        self.assertEqual(new_type_template.notes,
                         new_type_template_DB.notes)
        self.assertEqual(new_type_template.path_code,
                         new_type_template_DB.path_code)
        self.assertEqual(new_type_template.tags, new_type_template_DB.tags)
        self.assertEqual(new_type_template.type, new_type_template_DB.type)
        self.assertEqual(new_type_template.updated_by,
                         new_type_template_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
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
        
        db.session.add_all([new_user, new_department])
        db.session.commit()
        
        new_user_DB = db.query(User).\
                    filter(User.name==user_kwargs["login_name"]).first()
        
        assert(isinstance(new_user_DB, User))
        
        # the user itself
        self.assertEqual(new_user, new_user_DB)
        self.assertEqual(new_user.code, new_user_DB.code)
        self.assertEqual(new_user.created_by, new_user_DB.created_by)
        self.assertEqual(new_user.date_created, new_user_DB.date_created)
        self.assertEqual(new_user.date_updated, new_user_DB.date_updated)
        self.assertEqual(new_user.department, new_user_DB.department)
        self.assertEqual(new_user.description, new_user_DB.description)
        self.assertEqual(new_user.email, new_user_DB.email)
        self.assertEqual(new_user.first_name, new_user_DB.first_name)
        self.assertEqual(new_user.initials, new_user_DB.initials)
        self.assertEqual(new_user.last_login, new_user_DB.last_login)
        self.assertEqual(new_user.last_name, new_user_DB.last_name)
        self.assertEqual(new_user.login_name, new_user_DB.login_name)
        self.assertEqual(new_user.name, new_user_DB.name)
        self.assertEqual(new_user.nice_name, new_user_DB.nice_name)
        self.assertEqual(new_user.notes, new_user_DB.notes)
        self.assertEqual(new_user.password, new_user_DB.password)
        self.assertEqual(new_user.permission_groups,
                         new_user_DB.permission_groups)
        self.assertEqual(new_user.projects, new_user_DB.projects)
        self.assertEqual(new_user.projects_lead, new_user_DB.projects_lead)
        self.assertEqual(new_user.sequences_lead, new_user_DB.sequences_lead)
        self.assertEqual(new_user.tags, new_user_DB.tags)
        self.assertEqual(new_user.tasks, new_user_DB.tasks)
        self.assertEqual(new_user.updated_by, new_user_DB.updated_by)
        
        # as the member of a department
        department_db = db.query(Department).\
                      filter(Department.name==dep_kwargs["name"]).\
                      first()
        
        self.assertEqual(new_user, department_db.members[0])
        
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Version(self):
        """testing the persistence of Version
        """
        
        self.fail("test is not implemented yet")






########################################################################
class ExamplesTester(unittest.TestCase):
    """tests the examples
    """
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """setup the test
        """
        
        # add the stalker/examples directory to the sys.path
        import os, sys
        import stalker
        
        stalker_dir = os.path.sep.join(
            stalker.__file__.split(
                os.path.sep
            )[:-2]
        )
        
        sys.path.append(stalker_dir)
    
    
    
    #----------------------------------------------------------------------
    def test_ReferenceMixin_setup(self):
        """testing if the ReferenceMixin can be correctly setup with a new
        class
        """
        
        # the actual test
        from examples.extending import great_entity
        defaults.MAPPERS.append("examples.extending.great_entity")
        defaults.CORE_MODEL_CLASSES.append(
            "examples.extending.great_entity.GreatEntity"
        )
        
        #db.setup("sqlite:////tmp/mixin_test.db")
        db.setup()
        
        newGreatEntity = great_entity.GreatEntity(name="test")
        db.session.add(newGreatEntity)
        db.session.commit()
        
        newLinkType = LinkType(name="Image")
        
        newLink = Link(name="TestLink", path="nopath", filename="nofilename",
                       type=newLinkType)
        
        newGreatEntity.references = [newLink]
        
        db.session.add_all([newLink, newLinkType])
        db.session.commit()
        
        # query and check the equality
        newGreatEntity_DB = db.query(great_entity.GreatEntity).\
                          filter_by(name="test").first()
        
        self.assertEqual(newGreatEntity, newGreatEntity_DB)
        
        # clean up the test
        defaults.MAPPERS.remove("examples.extending.great_entity")
        defaults.CORE_MODEL_CLASSES.remove(
            "examples.extending.great_entity.GreatEntity")
    
    
    
    #----------------------------------------------------------------------
    def test_StatusMixin_setup(self):
        """testing if the StatusMixin can be correctly setup with a new class
        """
        
        # the actual test
        from examples.extending import statused_entity
        
        defaults.MAPPERS.append("examples.extending.statused_entity")
        defaults.CORE_MODEL_CLASSES.append(
            "examples.extending.statused_entity.NewStatusedEntity")
        
        #db.setup("sqlite:////tmp/mixin_test.db")
        db.setup()
        
        newStatusList = StatusList(
            name="A Status List for testing StatusMixin",
            statuses=[
                Status(name="Mixin - On Hold", code="OH"),
                Status(name="Mixin - Complete", code="CMPLT")
            ],
            target_entity_type = statused_entity.NewStatusedEntity.entity_type
        )
        db.session.add(newStatusList)
        db.session.commit()
        
        aStatusedEntity = statused_entity.NewStatusedEntity(
            name="test")
        
        # add the status list
        aStatusedEntity.status_list = newStatusList
        
        db.session.add(aStatusedEntity)
        db.session.commit()
        
        # query and check the equality
        aStatusedEntity_DB = db.query(statused_entity.NewStatusedEntity).\
                           first()
        
        self.assertEqual(aStatusedEntity, aStatusedEntity_DB)
        
        # clean up the test
        defaults.MAPPERS.remove("examples.extending.statused_entity")
        defaults.CORE_MODEL_CLASSES.remove(
            "examples.extending.statused_entity.NewStatusedEntity")
    
    
    
    #----------------------------------------------------------------------
    def test_camera_lens(self):
        """testing the camera_lens example
        """
        
        from examples.extending import camera_lens
        defaults.MAPPERS.append("examples.extending.camera_lens")
        defaults.CORE_MODEL_CLASSES.append(
            "examples.extending.camera_lens.Camera")
        defaults.CORE_MODEL_CLASSES.append(
            "examples.extending.camera_lens.Lens")
        
        #db.setup("sqlite:////tmp/camera_lens.db")
        db.setup("sqlite://")
        
        new_camera = camera_lens.Camera(
            name="Nikon D300",
            make="Nikon",
            model="D300",
            horizontal_film_back=23.6,
            vertical_film_back=15.8,
            cropping_factor=1.5,
            web_page="http://www.nikon.com",
        )
        
        new_lens = camera_lens.Lens(
            name="Nikon 50 mm Lens",
            make="Nikon",
            model="Nikkor 50mm 1.8",
            min_focal_length=50,
            max_focal_length=50,
            web_page="http://www.nikon.com",
        )
        
        db.session.add_all([new_camera, new_lens])
        db.session.commit()
        
        # retrieve them from the db
        new_camera_DB = db.query(camera_lens.Camera).first()
        new_lens_DB = db.query(camera_lens.Lens).first()
        
        self.assertEqual(new_camera, new_camera_DB)
        self.assertEqual(new_lens, new_lens_DB)
    
    
    
    