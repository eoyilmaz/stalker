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
    Booking,
    Comment,
    Department,
    Entity,
    SimpleEntity,
    ImageFormat,
    Link,
    Note,
    PermissionGroup,
    Project,
    Repository,
    Sequence,
    Shot,
    Status,
    StatusList,
    Structure,
    Tag,
    Task,
    Type,
    FilenameTemplate,
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
        
        # create a test database, possibly an in memory datase
        #self.TEST_DATABASE_FILE = tempfile.mktemp() + ".db"
        #self.TEST_DATABASE_URI = "sqlite:///" + self.TEST_DATABASE_FILE
        
        self.TEST_DATABASE_FILE = ":memory:"
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
        
        asset_type = Type(name="A new asset type", target_entity_type=Asset)
        
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Completed", code="CMPLT")
        status3 = Status(name="Work In Progress", code="WIP")
        
        test_repository_type = Type(
            name="Test Repository",
            target_entity_type=Repository,
        )
        
        test_repository = Repository(
            name="Test Repository",
            type=test_repository_type
        )
        
        project_statusList = StatusList(
            name="Project Status List",
            statuses=[status1, status2, status3],
            target_entity_type="Project",
        )
        
        commercial_type = Type(name="Commercial", target_entity_type=Project)
        
        test_project = Project(
            name="Test Project",
            status_list=project_statusList,
            type=commercial_type,
            repository=test_repository,
        )
        
        #print test_project.project
        #print test_project._project
        
        db.session.add(test_project)
        db.session.commit()
        
        task_status_list = StatusList(
            name="Task Status List",
            statuses=[status1, status2, status3],
            target_entity_type=Task.entity_type,
        )
        
        asset_statusList = StatusList(
            name="Asset Status List",
            statuses=[status1, status2, status3],
            target_entity_type=Asset.entity_type
        )
        
        kwargs = {
            "name": "Test Asset",
            "description": "This is a test Asset object",
            "type": asset_type,
            "project": test_project,
            "status": 0,
            "status_list": asset_statusList,
        }
        
        test_asset = Asset(**kwargs)
        
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
        
        db.session.add(test_asset)
        db.session.commit()
        
        # create a couple of shots
        sequence_status_list = StatusList(
            name="Sequence Statuses",
            statuses=[status1, status2, status3],
            target_entity_type="Sequence"
        )
        
        mock_sequence = Sequence(
            name="Test Sequence",
            project=test_project,
            status=0,
            status_list=sequence_status_list
        )
        
        shot_status_list = StatusList(
            name="Shot Statuses",
            statuses=[status1, status2, status3],
            target_entity_type="Shot",
        )
        
        mock_shot1 = Shot(
            code="SH001",
            sequence=mock_sequence,
            status_list=shot_status_list
        )
        
        mock_shot2 = Shot(
            code="SH002",
            sequence=mock_sequence,
            status_list=shot_status_list
        )
        
        mock_shot3 = Shot(
            code="SH003",
            sequence=mock_sequence,
            status_list=shot_status_list
        )
        
        test_asset.shots = [mock_shot1, mock_shot2, mock_shot3]
        
        db.session.add_all([mock_shot1, mock_shot2, mock_shot3])
        db.session.commit()
        
        code = test_asset.code
        created_by = test_asset.created_by
        date_created = test_asset.date_created
        date_updated = test_asset.date_updated
        description = test_asset.description
        name = test_asset.name
        nice_name = test_asset.nice_name
        notes = test_asset.notes
        project= test_asset.project
        references = test_asset.references
        shots = test_asset.shots
        status = test_asset.status
        status_list = test_asset.status_list
        tags = test_asset.tags
        tasks = test_asset.tasks
        type = test_asset.type
        updated_by = test_asset.updated_by
        
        del(test_asset)
        
        test_asset_DB = db.query(Asset).\
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
        self.assertEqual(shots, test_asset_DB.shots)
        self.assertEqual(status, test_asset_DB.status)
        self.assertEqual(status_list, test_asset_DB.status_list)
        self.assertEqual(tags, test_asset_DB.tags)
        self.assertEqual(tasks, test_asset_DB.tasks)
        self.assertEqual(type, test_asset_DB.type)
        self.assertEqual(updated_by, test_asset_DB.updated_by)
    
    
    
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
        
        del(test_dep)
        
        # lets check the data
        # first get the department from the db
        test_dep_db = db.session.query(Department). \
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
        del(test_entity)
        
        # now try to retrieve it
        test_entity_DB = db.session.query(Entity). \
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
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_FilenameTemplate(self):
        """testing the persistence of FilenameTemplate
        """
        
        # get the admin
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create a FilenameTemplate object for movie links
        kwargs = {
            "name": "Movie Links Template",
            "target_entity_type": Link,
            "description": "this is a template to be used for links to movie"
                           "files",
            "created_by": admin,
            "path_code": "REFS/{{link_type.name}}",
            "file_code": "{{link.file_name}}",
            "output_path_code": "OUTPUT",
            "output_file_code": "{{link.file_name}}",
        }
        
        new_type_template = FilenameTemplate(**kwargs)
        #new_type_template2 = FilenameTemplate(**kwargs)
        
        # persist it
        session = db.session
        session.add(new_type_template)
        session.commit()
        
        code = new_type_template.code
        created_by = new_type_template.created_by
        date_created = new_type_template.date_created
        date_updated = new_type_template.date_updated
        description = new_type_template.description
        file_code = new_type_template.file_code
        name = new_type_template.name
        nice_name = new_type_template.nice_name
        notes = new_type_template.notes
        output_path_code = new_type_template.output_path_code
        output_file_code = new_type_template.output_file_code
        output_is_relative = new_type_template.output_is_relative
        path_code = new_type_template.path_code
        tags = new_type_template.tags
        target_entity_type = new_type_template.target_entity_type
        updated_by = new_type_template.updated_by
        
        del(new_type_template)
        
        # get it back
        new_type_template_DB = session.query(FilenameTemplate).\
                             filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(new_type_template_DB, FilenameTemplate))
        
        #self.assertEqual(new_type_template, new_type_template_DB)
        self.assertEqual(code, new_type_template_DB.code)
        self.assertEqual(created_by, new_type_template_DB.created_by)
        self.assertEqual(date_created, new_type_template_DB.date_created)
        self.assertEqual(date_updated, new_type_template_DB.date_updated)
        self.assertEqual(description, new_type_template_DB.description)
        self.assertEqual(file_code, new_type_template_DB.file_code)
        self.assertEqual(name, new_type_template_DB.name)
        self.assertEqual(nice_name, new_type_template_DB.nice_name)
        self.assertEqual(notes, new_type_template_DB.notes)
        self.assertEqual(output_path_code,
                         new_type_template_DB.output_path_code)
        self.assertEqual(output_file_code,
                         new_type_template_DB.output_file_code)
        self.assertEqual(output_is_relative,
                         new_type_template_DB.output_is_relative)
        self.assertEqual(path_code, new_type_template_DB.path_code)
        self.assertEqual(tags, new_type_template_DB.tags)
        self.assertEqual(target_entity_type,
                         new_type_template_DB.target_entity_type)
        self.assertEqual(updated_by, new_type_template_DB.updated_by)
    
    
    
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
        del(im_format)
        
        # get it back
        im_format_DB = session.query(ImageFormat). \
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
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Link(self):
        """testing the persistence of Link
        """
        
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create a link Type
        sound_link_type = Type(
            name="Sound",
            created_by=admin,
            target_entity_type=Link
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
        
        # store attributes
        code = new_link.code
        created_by = new_link.created_by
        date_created = new_link.date_created
        date_updated = new_link.date_updated
        description = new_link.description
        filename = new_link.filename
        name = new_link.name
        nice_name = new_link.nice_name
        notes = new_link.notes
        path = new_link.path
        tags = new_link.tags
        type = new_link.type
        updated_by = new_link.updated_by
        
        
        # delete the link
        del(new_link)
        
        # retrieve it back
        new_link_DB = db.session.query(Link).\
                filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(new_link_DB, Link))
        
        #self.assertEqual(new_link, new_link_DB)
        self.assertEqual(code, new_link_DB.code)
        self.assertEqual(created_by, new_link_DB.created_by)
        self.assertEqual(date_created, new_link_DB.date_created)
        self.assertEqual(date_updated, new_link_DB.date_updated)
        self.assertEqual(description, new_link_DB.description)
        self.assertEqual(filename, new_link_DB.filename)
        self.assertEqual(name, new_link_DB.name)
        self.assertEqual(nice_name, new_link_DB.nice_name)
        self.assertEqual(notes, new_link_DB.notes)
        self.assertEqual(path, new_link_DB.path)
        self.assertEqual(tags, new_link_DB.tags)
        self.assertEqual(type, new_link_DB.type)
        self.assertEqual(updated_by, new_link_DB.updated_by)
    
    
    
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
        del(test_note)
        
        # try to get the note directly
        test_note_DB = db.query(Note).\
                     filter(Note.name==note_kwargs["name"]).first()
        
        assert(isinstance(test_note_DB, Note))
        
        # try to get the note from the entity
        test_entity_DB = db.query(Entity).\
                      filter(Entity.name==entity_kwargs["name"]).first()
        
        #self.assertEqual(test_note, test_entity_DB.notes[0])
        
        #self.assertEqual(test_note, test_note_DB)
        self.assertEqual(code, test_note_DB.code)
        self.assertEqual(content, test_note_DB.content)
        self.assertEqual(created_by, test_note_DB.created_by)
        self.assertEqual(date_created, test_note_DB.date_created)
        self.assertEqual(date_updated, test_note_DB.date_updated)
        self.assertEqual(description, test_note_DB.description)
        self.assertEqual(name, test_note_DB.name)
        self.assertEqual(nice_name, test_note_DB.nice_name)
        self.assertEqual(updated_by, test_note_DB.updated_by)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_PermissionGroup(self):
        """testing the persistence of PermissionGroup
        """
        
        self.fail("test is not implmented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Project(self):
        """testing the persistence of Project
        """
        
        # create mock objects
        start_date = datetime.date.today() + datetime.timedelta(10)
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
        
        project_type = Type(name="Commercial Project",
                            target_entity_type=Project)
        structure_type = Type(name="Commercial Structure",
                              target_entity_type=Project)
        
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
            windows_path="M:\\Projects",
            osx_path="/Volumes/M/Projects"
        )
        
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
        link_type = Type(name="Image", target_entity_type="Link")
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
        
        db.session.add_all([ref1, ref2])
        db.session.commit()
        
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
        db.session.add(new_project)
        db.session.commit()
        
        
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
        
        db.session.add_all([task1, task2])
        db.session.commit()
        
        # store the attributes
        assets = new_project.assets
        code = new_project.code
        created_by = new_project.created_by
        date_created = new_project.date_created
        date_updated = new_project.date_updated
        description = new_project.description
        display_width = new_project.display_width
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
        del(new_project)
        
        # now get it
        new_project_DB = db.query(Project).\
                       filter_by(name=kwargs["name"]).first()
        
        assert(isinstance(new_project_DB, Project))
        
        #self.assertEqual(new_project, new_project_DB)
        self.assertEqual(assets, new_project_DB.assets)
        self.assertEqual(code, new_project_DB.code)
        self.assertEqual(created_by, new_project_DB.created_by)
        self.assertEqual(date_created, new_project_DB.date_created)
        self.assertEqual(date_updated, new_project_DB.date_updated)
        self.assertEqual(description, new_project_DB.description)
        self.assertEqual(display_width, new_project_DB.display_width)
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
        del(repo)
        
        # get it back
        repo_db = db.query(Repository).\
                  filter_by(name=kwargs["name"]).\
                  first()
        
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
        
        commercial_project_type = Type(name="Commercial Project",
                                       target_entity_type=Project)
        
        project1 = Project(name="Test project",
                           status_list=project_status_list,
                           type=commercial_project_type)
        
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
        del(test_sequence)
        
        test_sequence_DB = db.query(Sequence).\
                         filter_by(name=kwargs["name"]).one()
        
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
        
        commercial_project_type = Type(name="Commercial Project",
                                       target_entity_type=Project)
        
        project1 = Project(name="Test project",
                           status_list=project_status_list,
                           type=commercial_project_type)
        
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
        del(test_shot)
        
        test_shot_DB = db.query(Shot).\
                     filter_by(code=shot_kwargs["code"]).first()
        
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
        
        code = test_simple_entity.code
        created_by = test_simple_entity.created_by
        date_created = test_simple_entity.date_created
        date_updated = test_simple_entity.date_updated
        description = test_simple_entity.description
        name = test_simple_entity.name
        nice_name = test_simple_entity.nice_name
        updated_by = test_simple_entity.updated_by
        
        del(test_simple_entity)
        
        # now try to retrieve it
        test_simple_entity_DB = db.session.query(SimpleEntity).\
            filter(SimpleEntity.name==kwargs["name"]).first()
        
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
        del(test_status)
        
        # now try to retrieve it
        test_status_DB = db.query(Status).\
                     filter(Status.name==kwargs["name"]).first()
        
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
        del(sequence_status_list)
        
        # now get it back
        sequence_status_list_DB = db.query(StatusList).\
                                filter_by(name=kwargs["name"]).first()
        
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
        modeling_tType = Type(
            name="Modeling",
            description="This is the step where all the modeling job is done",
            code="MODEL",
            created_by=admin,
            target_entity_type=Task
        )
        
        animation_tType = Type(
            name="Animation",
            description="This is the step where all the animation job is " + \
                        "done it is not limited with characters, other " + \
                        "things can also be animated",
            code="ANIM",
            created_by=admin,
            target_entity_type=Task
        )
        
        # create a new asset Type
        char_asset_type = Type(
            name="Character Asset Type",
            description="This is the asset type which covers animated " + \
                        "charactes",
            created_by=admin,
            target_entity_type=Asset,
        )
        
        # create a new type template for character assets
        assetTemplate = FilenameTemplate(
            name="Character Asset Template",
            description="This is the template for character assets",
            path_code="ASSETS/{{asset_type.name}}/{{pipeline_step.code}}",
            file_code="{{asset.name}}_{{take.name}}_{{asset_type.name}}_\
            v{{version.version_number}}",
            target_entity_type=Asset,
        )
        
        # create a new link type
        image_link_type = Type(
            name="Image",
            description="It is used for links showing an image",
            created_by=admin,
            target_entity_type=Link
        )
        
        # create a new template for references
        imageReferenceTemplate = FilenameTemplate(
            name="Image Reference Template",
            description="this is the template for image references, it " + \
                        "shows where to place the image files",
            created_by=admin,
            path_code="REFS/{{reference.type.name}}",
            file_code="{{reference.file_name}}",
            target_entity_type=Link
        )
        
        commercial_structure_type = Type(name="Commercial",
                                         target_entity_type=Structure)
        
        # create a new structure
        kwargs = {
            "name": "Commercial Structure",
            "description": "The structure for commercials",
            "created_by": admin,
            "custom_template": """ASSETS
SEQUENCES
SEQUENCES/{% for sequence in project.sequences %}
{{sequence.code}}""",
            "templates": [assetTemplate, imageReferenceTemplate],
            "type": commercial_structure_type
        }
        
        new_structure = Structure(**kwargs)
        
        db.session.add(new_structure)
        db.session.commit()
        
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
        del(new_structure)
        
        new_structure_DB = db.query(Structure).\
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
        
        # store the attributes
        description = aTag.description
        created_by = aTag.created_by
        updated_by = aTag.updated_by
        date_created = aTag.date_created
        date_updated = aTag.date_updated
        
        
        # delete the aTag
        del(aTag)
        
        # now try to retrieve it
        aTag_DB = db.session.query(Tag).filter_by(name=name).first()
        
        assert(isinstance(aTag_DB, Tag))
        
        self.assertEqual(name, aTag_DB.name)
        self.assertEqual(description, aTag_DB.description)
        self.assertEqual(created_by, aTag_DB.created_by)
        self.assertEqual(updated_by, aTag_DB.updated_by)
        self.assertEqual(date_created, aTag_DB.date_created)
        self.assertEqual(date_updated, aTag_DB.date_updated)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Task(self):
        """testing the persistence of Task
        """
        
        # lets create a task for an asset
        self.fail("test is not implemented yet")
        
    
    
    
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
        permission_groups = new_user.permission_groups
        projects = new_user.projects
        projects_lead = new_user.projects_lead
        sequences_lead = new_user.sequences_lead
        tags = new_user.tags
        tasks = new_user.tasks
        updated_by = new_user.updated_by
        
        
        # delete new_user
        del(new_user)
        
        new_user_DB = db.query(User).\
                    filter(User.name==user_kwargs["login_name"]).first()
        
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
        self.assertEqual(permission_groups, new_user_DB.permission_groups)
        self.assertEqual(projects, new_user_DB.projects)
        self.assertEqual(projects_lead, new_user_DB.projects_lead)
        self.assertEqual(sequences_lead, new_user_DB.sequences_lead)
        self.assertEqual(tags, new_user_DB.tags)
        self.assertEqual(tasks, new_user_DB.tasks)
        self.assertEqual(updated_by, new_user_DB.updated_by)
        
        # as the member of a department
        department_db = db.query(Department).\
                      filter(Department.name==dep_kwargs["name"]).\
                      first()
        
        self.assertEqual(new_user_DB, department_db.members[0])
        
    
    
    
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
        
        newLinkType = Type(name="Image", target_entity_type=Link)
        
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
    
    
    
    