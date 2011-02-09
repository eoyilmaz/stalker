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
from stalker.db import auth, tables
from stalker.core.models import (
    asset,
    assetBase,
    booking,
    comment,
    department,
    entity,
    error,
    group,
    imageFormat,
    link,
    note,
    pipelineStep,
    project,
    repository,
    sequence,
    shot,
    status,
    structure,
    tag,
    task,
    types,
    user,
    version
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
        
        clear_mappers()
        db.__mappers__ = []
    
    
    
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
        }
        
        newUser = user.User(**kwargs)
        
        session.add(newUser)
        session.commit()
        
        # now check if the newUser is there
        newUser_DB = query(user.User).\
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
        }
        
        newUser = user.User(**kwargs)
        
        session.add(newUser)
        session.commit()
        
        # now reconnect and check if the newUser is there
        db.setup(self.TEST_DATABASE_URI)
        
        newUser_DB = query(user.User).\
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
        
        self.assertEquals(full_db_url, defaults.DATABASE)
    
    
    
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
        
        self.assertEquals(admin.name, defaults.ADMIN_NAME)
        
    
    
    
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
        
        admins = db.session.query(user.User). \
               filter_by(name=defaults.ADMIN_NAME).all()
        
        self.assertFalse( len(admins) > 1 )
    
    
    
    #----------------------------------------------------------------------
    def test_auth_authenticate_LogginError_raised(self):
        """testing if stalker.core.models.error.LoginError will be raised when
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
                error.LoginError,
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
        self.assertTrue(db.session.query(user.User).\
                        filter_by(name=defaults.ADMIN_NAME).first()
                        is None )
        
        # check if there is a admins department
        self.assertTrue(db.session.query(department.Department).\
                        filter_by(name=defaults.ADMIN_DEPARTMENT_NAME).\
                        first() is None)
    
    
    
    #----------------------------------------------------------------------
    def test_unique_names_on_same_entity_type(self):
        """testing if there are unique names for same entity types
        """
        
        db.setup(self.TEST_DATABASE_URI)
        self._createdDB = True
        
        admin = db.auth.authenticate(defaults.ADMIN_NAME,
                                     defaults.ADMIN_PASSWORD)
        
        # try to create a user with the same login_name
        # expect IntegrityError
        
        kwargs = {
            "first_name": "user1name",
            "login_name": "user1",
            "email": "user1@gmail.com",
            "password": "user1",
            "created_by": admin
        }
        
        user1 = user.User(**kwargs)
        db.session.commit()
        
        # lets create the second user
        kwargs.update({
            "email": "user2@gmail.com",
            "login_name": "user1",
        })
        
        user2=user.User(**kwargs)
        
        self.assertRaises(IntegrityError, db.session.commit)
    
    
    
    #----------------------------------------------------------------------
    def test_non_unique_names_on_different_entity_type(self):
        """testing if there can be non-unique names for different entity types
        """
        
        db.setup(self.TEST_DATABASE_URI)
        self._createdDB = True
        
        admin = db.auth.authenticate(defaults.ADMIN_NAME,
                                     defaults.ADMIN_PASSWORD)
        
        # try to create a user and an entity with same name
        # expect Nothing
        
        kwargs = {
            "name": "user1",
            "created_by": admin
        }
        
        entity1 = entity.Entity(**kwargs)
        db.session.commit()
        
        # lets create the second user
        kwargs.update({
            "first_name": "user1name",
            "login_name": "user1",
            "email": "user1@gmail.com",
            "password": "user1",
        })
        
        user1=user.User(**kwargs)
        
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
        s = select([tables.entity_types.c.entity_type])
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
        #self.TEST_DATABASE_FILE = tempfile.mktemp() + ".db"
        #self.TEST_DATABASE_URI = "sqlite:///" + self.TEST_DATABASE_FILE
        
        self.TEST_DATABASE_FILE = ":memory:"
        self.TEST_DATABASE_URI = "sqlite:///" + self.TEST_DATABASE_FILE
        
        # setup using this db
        db.setup(database=self.TEST_DATABASE_URI)
    
    
    
    #----------------------------------------------------------------------
    def tearDown(self):
        """tear-off the test
        """
        ## delete the default test database file
        #os.remove(self.TEST_DATABASE_FILE)
        
        db.metadata.drop_all(db.engine)
        clear_mappers()
        db.engine.dispose()
        db.session.close()
        db.__mappers__ = []
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Asset(self):
        """testing the persistence of Asset
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_AssetBase(self):
        """testing the persistence of AssetBase
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_AssetType(self):
        """testing the persistence of AssetType
        """
        
        
        # first get the admin
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create a couple of PipelineStep objects
        pStep1 = pipelineStep.PipelineStep(
            name="Rigging",
            description="This is where a character asset is rigged",
            created_by=admin,
            updated_by=admin,
            code="RIG"
        )
        
        pStep2 = pipelineStep.PipelineStep(
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
            "steps": [pStep1, pStep2],
        }
        
        aType = types.AssetType(**kwargs)
        
        # store it in the db
        db.session.add(aType)
        db.session.commit()
        
        # retrieve it back and check it with the first one
        aType_DB = db.session.query(types.AssetType). \
                 filter_by(name=kwargs["name"]).first()
        
        for i, pStep_DB in enumerate(aType_DB.steps):
            self.assertEquals(aType.steps[i].name, pStep_DB.name)
            self.assertEquals(aType.steps[i].description, pStep_DB.description) 
        
        
    
    
    
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
        
        testDepartment = department.Department(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated
        )
        
        # create three users, one for lead and two for members
        
        # user1
        user1 = user.User(
            name="user1_test_persistence_department",
            description="this is for testing purposes",
            created_by=None,
            updated_by=None,
            login_name="user1_tp_department",
            first_name="user1_first_name",
            last_name="user1_last_name",
            email="user1@department.com",
            department=testDepartment
        )
        
        # user2
        user2 = user.User(
            name="user2_test_persistence_department",
            description="this is for testing purposes",
            created_by=None,
            updated_by=None,
            login_name="user2_tp_department",
            first_name="user2_first_name",
            last_name="user2_last_name",
            email="user2@department.com",
            department=testDepartment
        )
        
        # user3
        # create three users, one for lead and two for members
        user3 = user.User(
            name="user3_test_persistence_department",
            description="this is for testing purposes",
            created_by=None,
            updated_by=None,
            login_name="user3_tp_department",
            first_name="user3_first_name",
            last_name="user3_last_name",
            email="user3@department.com",
            department=testDepartment
        )
        
        # add as the members and the lead
        testDepartment.lead = user1
        testDepartment.members = [user1, user2, user3]
        
        db.session.add(testDepartment)
        db.session.commit()
        
        # lets check the data
        # first get the department from the db
        dep_from_db = db.session.query(department.Department). \
                    filter_by(name=testDepartment.name).first()
        
        # members
        for i, member in enumerate(dep_from_db.members):
            self.assertEquals( testDepartment.members[i].name, member.name)
            self.assertEquals( testDepartment.members[i].last_name,
                               member.last_name)
            self.assertEquals( testDepartment.members[i].login_name,
                               member.login_name)
        
        # lead
        self.assertEquals(testDepartment.lead, dep_from_db.lead)
    
    
    
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
        
        tag1 = tag.Tag(
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
        
        tag2 = tag.Tag(
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
        
        testEntity = entity.Entity(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated,
            tags=[tag1, tag2],
        )
        
        # persist it to the database
        db.session.add(testEntity)
        db.session.commit()
        
        # now try to retrieve it
        testEntityDB = db.session.query(entity.Entity). \
                     filter_by(name=name).first()
        
        # just test the entity part of the object
        for i, tag_ in enumerate(testEntity.tags):
            self.assertEquals(tag_, testEntityDB.tags[i])
    
    
    
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
        imFormat = imageFormat.ImageFormat(**kwargs)
        
        # persist it
        session.add(imFormat)
        session.commit()
        
        # get it back
        imFormat_db = session.query(imageFormat.ImageFormat). \
                filter_by(name=kwargs["name"]).first()
        
        # just test the repository part of the attributes
        self.assertEquals(imFormat, imFormat_db)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Link(self):
        """testing the persistence of Link
        """
        
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        # create a LinkType
        sound_link_type = types.LinkType(
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
        
        new_link = link.Link(**kwargs)
        
        # persist it
        db.session.add_all([sound_link_type, new_link])
        db.session.commit()
        
        # retrieve it back
        link_DB = db.session.query(link.Link).\
                filter_by(name=kwargs["name"]).first()
        
        self.assertTrue(new_link==link_DB)
    
    
    
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
        
        a_note_obj = note.Note(**note_kwargs)
        
        # create an entity
        entity_kwargs = {
            "name": "Entity with Note",
            "description": "This Entity is created for testing purposes",
            "notes": [a_note_obj],
        }
        
        an_entity_obj = entity.Entity(**entity_kwargs)
        
        db.session.add_all([an_entity_obj, a_note_obj])
        db.session.commit()
        
        # try to get the note directly
        
        note_DB = db.query(note.Note).\
                filter(note.Note.name==note_kwargs["name"]).first()
        
        self.assertEquals(a_note_obj, note_DB)
        
        # try to get the note from the entity
        entity_DB = db.query(entity.Entity).\
                  filter(entity.Entity.name==entity_kwargs["name"]).first()
        
        self.assertEquals(a_note_obj, entity_DB.notes[0])
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_PipelineStep(self):
        """testing the persistence of PipelineStep
        """
        
        # create a new PipelineStep
        admin = auth.authenticate(defaults.ADMIN_NAME, defaults.ADMIN_PASSWORD)
        
        kwargs = {
            "name": "RENDER",
            "description": "this is the step where all the assets are \
            rendered",
            "created_by": admin,
            "code": "RNDR"
        }
        
        pStep = pipelineStep.PipelineStep(**kwargs)
        
        # save it to database
        db.session.add(pStep)
        
        # retrieve it back
        pStep_DB = db.session.query(pipelineStep.PipelineStep). \
                 filter_by(name=kwargs["name"]). \
                 filter_by(description=kwargs["description"]). \
                 first()
        
        # lets compare it
        self.assertEquals(pStep.code, pStep_DB.code)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Project(self):
        """testing the persistence of Project
        """
        
        # create mock objects
        start_date = datetime.date.today()
        due_date = start_date + datetime.timedelta(days=20)
        
        lead = user.User(login_name="lead", first_name="lead",
                                   last_name="lead", email="lead@lead.com")
        
        user1 = user.User(login_name="user1", first_name="user1",
                          last_name="user1", email="user1@user1.com")
        user2 = user.User(login_name="user2", first_name="user2",
                          last_name="user2", email="user1@user2.com")
        user3 = user.User(login_name="user3", first_name="user3",
                          last_name="user3", email="user3@user3.com")
        
        image_format = imageFormat.ImageFormat(name="HD", width=1920,
                                               height=1080)
        
        project_type = types.ProjectType(name="Commercial")
        
        project_structure = structure.Structure(name="Commercial Structure",
                                                project_template="")
        
        repo = repository.Repository(name="Commercials Repository",
                                     linux_path="/mnt/Projects",
                                     windows_path="M:\\Projects",
                                     osx_path="/Volumes/Projects")
        
        project_status_list = status.StatusList(
            name="A Status List for testing project.Project",
            statuses=[
                status.Status(name="On Hold", code="OH"),
                status.Status(name="Complete", code="CMPLT")
            ],
            target_entity_type = project.Project.entity_type
        )
        
        db.session.add(project_status_list)
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
            "status": 0
        }
        
        new_project = project.Project(**kwargs)
        
        # persist it in the database
        db.session.add(new_project)
        db.session.commit()
        
        # now get it
        new_project_DB = db.query(project.Project).\
                       filter_by(name=kwargs["name"]).first()
        
        self.assertEquals(new_project, new_project_DB)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Repository(self):
        """testing the persistence of Repository
        """
        
        # get the admin
        session = db.session
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
        repo = repository.Repository(**kwargs)
        
        # persist it
        session.add(repo)
        session.commit()
        
        # get it back
        repo_db = session.query(repository.Repository). \
                filter_by(name=kwargs["name"]).first()
        
        # just test the repository part of the attributes
        self.assertEquals(repo.linux_path, repo_db.linux_path)
        self.assertEquals(repo.windows_path, repo_db.windows_path)
        self.assertEquals(repo.osx_path, repo_db.osx_path)
        self.assertEquals(repo.path, repo_db.path)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Sequence(self):
        """testing the persistence of Sequence
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Shot(self):
        """testing the persistence of Shot
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_SimpleEntity(self):
        """testing the persistence of SimpleEntity
        """
        
        kwargs = {
            "name": "SimpleEntity_test_creating_of_a_SimpleEntity",
            "description": "this is for testing purposes",
        }
        
        aSimpleEntity = entity.SimpleEntity(**kwargs)
        
        # persist it to the database
        db.session.add(aSimpleEntity)
        db.session.commit()
        
        # now try to retrieve it
        SE_from_DB = db.session.query(entity.SimpleEntity).\
            filter(entity.SimpleEntity.name==kwargs["name"]).first()
        
        self.assertEquals(aSimpleEntity, SE_from_DB)
    
    
    
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
        
        testStatus = status.Status(**kwargs)
        
        # persist it to the database
        db.session.add(testStatus)
        db.session.commit()
        
        # now try to retrieve it
        testStatusDB = db.query(status.Status).\
                     filter(status.Status.name==kwargs["name"]).first()
        
        # just test the satuts part of the object
        self.assertEquals(testStatus, testStatusDB)
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_StatusList(self):
        """testing the persistence of StatusList
        """
        
        # create a couple of statuses
        
        statuses = [
            status.Status(name="Waiting To Start", code="WTS"),
            status.Status(name="On Hold", code="OH"),
            status.Status(name="In Progress", code="WIP"),
            status.Status(name="Complete", code="CMPLT"),
        ]
        
        kwargs = dict(
            name="Sequence Status List",
            statuses=statuses,
            target_entity_type="Sequence"
        )
        
        sequence_status_list = status.StatusList(**kwargs)
        
        # send it to db
        db.session.add(sequence_status_list)
        db.session.commit()
        
        # now get it back
        sequence_status_list_DB = db.query(status.StatusList).\
                                filter_by(name=kwargs["name"]).first()
        
        self.assertEquals(sequence_status_list, sequence_status_list_DB)
        
        # try to create another StatusList for the same target_entity_type
        # and expect and IntegrityError
        
        kwargs["name"] = "new Sequence Status List"
        new_sequence_list = status.StatusList(**kwargs)
        
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
        modeling_pStep = pipelineStep.PipelineStep(
            name="Modeling",
            description="This is the step where all the modeling job is done",
            code="MODEL",
            created_by=admin
        )
        
        animation_pStep = pipelineStep.PipelineStep(
            name="Animation",
            description="This is the step where all the animation job is done\
            it is not limited with characters, other things can also be\
            animated",
            code="ANIM",
            created_by=admin
        )
        
        # create a new assetType
        char_asset_type = types.AssetType(
            name="Character Asset Type",
            description="This is the asset type which covers animated\
            charactes",
            created_by=admin,
            steps= [modeling_pStep, animation_pStep]
        )
        
        # create a new type template for character assets
        assetTemplate = types.TypeTemplate(
            name="Character Asset Template",
            description="This is the template for character assets",
            path_code="ASSETS/{{asset_type.name}}/{{pipeline_step.code}}",
            file_code="{{asset.name}}_{{take.name}}_{{asset_type.name}}_\
            v{{version.version_number}}",
            type=char_asset_type
        )
        
        # create a new link type
        image_link_type = types.LinkType(
            name="Image",
            description="It is used for links showing an image",
            created_by=admin
        )
        
        # create a new template for references
        imageReferenceTemplate = types.TypeTemplate(
            name="Image Reference Template",
            description="this is the template for image references, it shows \
            where to place the image files",
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
            "project_template": "ASSETS\n\
            SEQUENCES\n\
            SEQUENCES/{% for sequence in project.sequences %}\
            {{sequence.code}}\n",
            "asset_templates": [assetTemplate],
            "reference_template": [imageReferenceTemplate]
        }
        
        # persist it to the database
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persistence_Tag(self):
        """testing the persistence of Tag
        """
        
        name = "Tag_test_creating_a_Tag"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        date_created = date_updated = datetime.datetime.now()
        
        aTag = tag.Tag(
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
        tag_query = db.session.query(tag.Tag)
        Tag_from_DB = tag_query.filter_by(name=name).first()
        
        self.assertEquals(aTag.name, Tag_from_DB.name)
        self.assertEquals(aTag.description, Tag_from_DB.description)
        self.assertEquals(aTag.created_by, Tag_from_DB.created_by)
        self.assertEquals(aTag.updated_by, Tag_from_DB.updated_by)
        self.assertEquals(aTag.date_created, Tag_from_DB.date_created)
        self.assertEquals(aTag.date_updated, Tag_from_DB.date_updated)
    
    
    
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
        movie_link_type = types.LinkType(
            name="Movie",
            created_by=admin
        )
        
        # create a TypeTemplate object for movie links
        kwargs = {
            "name": "Movie Links Template",
            "description": "this is a template to be used for links to movie\
                files",
            "created_by": admin,
            "path_code": "REFS/{{link_type.name}}",
            "file_code": "{{link.file_name}}",
            "type": movie_link_type,
        }
        
        aTypeTemplate = types.TypeTemplate(**kwargs)
        
        # persist it
        session = db.session
        session.add(aTypeTemplate)
        session.commit()
        
        # get it back
        aTypeTemplate_DB = session.query(types.TypeTemplate).\
                     filter_by(name=kwargs["name"]).first()
        
        self.assertEquals(aTypeTemplate, aTypeTemplate_DB)
    
    
    
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
        
        new_department = department.Department(**dep_kwargs)
        
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
        
        new_user = user.User(**user_kwargs)
        
        db.session.add_all([new_user, new_department])
        db.session.commit()
        
        user_DB = db.query(user.User).\
                filter(user.User.name==user_kwargs["login_name"]).first()
        
        # the user itself
        self.assertEquals(new_user, user_DB)
        
        # as the member of a department
        department_db = db.query(department.Department).\
                      filter(department.Department.name==dep_kwargs["name"]).\
                      first()
        
        self.assertEquals(new_user, department_db.members[0])
        
        # get the user initials and check if they are same
        self.assertEquals(new_user.initials, user_DB.initials)
    
    
    
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
    def setUp(self):
        """setup per test basis
        """
        
        # setup the database
        clear_mappers()
        db.__mappers__ = []
    
    
    
    #----------------------------------------------------------------------
    def test_ReferenceMixin_setup(self):
        """testing if the ReferenceMixin can be correctly setup with a new
        class
        """
        
        clear_mappers()
        db.__mappers__ = []
        
        # the actual test
        from examples.extending import great_entity
        defaults.MAPPERS.append("examples.extending.great_entity")
        defaults.CORE_MODEL_CLASSES.append("examples.extending.great_entity.\
GreatEntity")
        
        #db.setup("sqlite:////tmp/mixin_test.db")
        db.setup("sqlite://")
        
        newGreatEntity = great_entity.GreatEntity(name="test")
        db.session.add(newGreatEntity)
        db.session.commit()
        
        newLinkType = types.LinkType(name="Image")
        
        newLink = link.Link(name="TestLink",
                            path="nopath",
                            filename="nofilename",
                            type=newLinkType)
        
        newGreatEntity.references = [newLink]
        
        db.session.add_all([newLink, newLinkType])
        db.session.commit()
        
        # query and check the equality
        newGreatEntity_DB = db.query(great_entity.GreatEntity).\
                          filter_by(name="test").first()
        
        self.assertEquals(newGreatEntity, newGreatEntity_DB)
        
        # clean up the test
        defaults.MAPPERS.remove("examples.extending.great_entity")
        defaults.CORE_MODEL_CLASSES.remove("examples.extending.great_entity.\
GreatEntity")
    
    
    
    #----------------------------------------------------------------------
    def test_StatusMixin_setup(self):
        """testing if the StatusMixin can be correctly setup with a new class
        """
        clear_mappers()
        db.__mappers__ = []
        
        # the actual test
        from examples.extending import statused_entity

        defaults.MAPPERS.append("examples.extending.statused_entity")
        defaults.CORE_MODEL_CLASSES.append("examples.extending.\
statused_entity.NewStatusedEntity")
        
        #db.setup("sqlite:////tmp/mixin_test.db")
        db.setup("sqlite://")
        
        newStatusList = status.StatusList(
            name="A Status List for testing StatusMixin",
            statuses=[
                status.Status(name="Mixin - On Hold", code="OH"),
                status.Status(name="Mixin - Complete", code="CMPLT")
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
        
        self.assertEquals(aStatusedEntity, aStatusedEntity_DB)
        
        # clean up the test
        defaults.MAPPERS.remove("examples.extending.statused_entity")
        defaults.CORE_MODEL_CLASSES.remove("examples.extending.\
statused_entity.NewStatusedEntity")

    
    
    
    #----------------------------------------------------------------------
    def test_multiple_mixin_case(self):
        """testing multiple mixin case
        """
        
        self.fail("test is not implemented yet")
    
    
    
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
        
        self.assertEquals(new_camera, new_camera_DB)
        self.assertEquals(new_lens, new_lens_DB)
    
    
    