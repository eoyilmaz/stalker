#-*- coding: utf-8 -*-


import os
import datetime
import unittest
import tempfile
from sqlalchemy.orm import clear_mappers
from sqlalchemy.exc import IntegrityError
from stalker.conf import defaults
from stalker import db
from stalker.db import auth
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
    pipelineStep,
    project,
    link,
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
        # setup the database
        clear_mappers()
        db.meta.__mappers__ = []
        
        # just set the default admin creation to true
        # some tests are relying on that
        defaults.AUTO_CREATE_ADMIN = True
        defaults.ADMIN_NAME = "admin"
        defaults.ADMIN_PASSWORD = "admin"
        
        self.TEST_DATABASE_FILE = tempfile.mktemp() + ".db"
        self.TEST_DATABASE_DIALECT = "sqlite:///"
        self.TEST_DATABASE_URI = self.TEST_DATABASE_DIALECT + \
            self.TEST_DATABASE_FILE
        
        self._createdDB = False
    
    
    
    #----------------------------------------------------------------------
    def tearDown(self):
        """tearDown the tests
        """
        
        if self._createdDB:
            os.remove(self.TEST_DATABASE_FILE)
    
    
    
    #----------------------------------------------------------------------
    def test_creating_a_custom_in_memory_db(self):
        """testing if a custom in-memory sqlite database will be created
        """
        
        # create a database in memory
        db.setup("sqlite:///:memory:")
        
        # try to persist a user and get it back
        session = db.meta.session
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
        session = db.meta.session
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
        
        drivername = db.meta.engine.url.drivername
        database = db.meta.engine.url.database
        
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
        
        admins = db.meta.session.query(user.User). \
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
    
    
    
    ##----------------------------------------------------------------------
    #def test_auth_login_creates_a_file_in_users_home(self):
        #"""testing if auth.login function creates a file called logged_user
        #in the $HOME/.stalker folder
        #"""
        
        #self.fail("test is not implemented yet")
        
    
    
    ##----------------------------------------------------------------------
    #def test_auth_login_stores_the_information(self):
        #"""testing if auth.login stores the information of latest login in
        #the users $HOME/.stalker/logged_user file as a pickled object
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_authentication(self):
        #"""testing the authentication system
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
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
        self.assertTrue(db.meta.session.query(user.User).\
                        filter_by(name=defaults.ADMIN_NAME).first()
                        is None )
        
        # check if there is a admins department
        self.assertTrue(db.meta.session.query(department.Department).\
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
        
        # try to create a user with the same name
        # expect IntegrityError
        
        kwargs = {
            "name": "user1",
            "first_name": "user1name",
            "login_name": "user1",
            "email": "user1@gmail.com",
            "password": "user1",
            "created_by": admin
        }
        
        user1 = user.User(**kwargs)
        db.meta.session.commit()
        
        # lets create the second user
        kwargs.update({
            "email": "user2@gmail.com",
            "login_name": "user2",
        })
        
        user2=user.User(**kwargs)
        
        self.assertRaises(IntegrityError, db.meta.session.commit)
    
    
    
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
        db.meta.session.commit()
        
        # lets create the second user
        kwargs.update({
            "first_name": "user1name",
            "login_name": "user1",
            "email": "user1@gmail.com",
            "password": "user1",
        })
        
        user1=user.User(**kwargs)
        
        # expect nothing, this should work without any error
        db.meta.session.commit()






########################################################################
class DatabaseModelsTester(unittest.TestCase):
    """tests the database model
    
    NOTE TO OTHER DEVELOPERS:
    
    Most of the tests in this TestCase uses parts of the system which are
    tested but probably not tested while running the individual tests.
    
    Incomplete isolation is against to the logic behind unittesting, every test
    should only cover a unit of the code, and a complete isolation should be
    created. But this can not be done in persistancy tests (AFAIK), it needs to
    be done in this way for now. Mocks can not be used because every created
    object goes to the database, so they need to be real objects.
    """
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """setup the test
        """
        
        # setup the database
        clear_mappers()
        db.meta.__mappers__ = []
        
        # create a test database, possibly an in memory datase
        cls.TEST_DATABASE_FILE = tempfile.mktemp() + ".db"
        cls.TEST_DATABASE_URI = "sqlite:///" + cls.TEST_DATABASE_FILE
        
        # setup using this db
        db.setup(database=cls.TEST_DATABASE_URI)
        
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def tearDownClass(cls):
        """tear-off the test
        """
        # delete the default test database file
        os.remove(cls.TEST_DATABASE_FILE)
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Asset(self):
        """testing the persistancy of Asset
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_AssetBase(self):
        """testing the persistancy of AssetBase
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_AssetType(self):
        """testing the persistancy of AssetType
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
        db.meta.session.add(aType)
        db.meta.session.commit()
        
        # retrieve it back and check it with the first one
        aType_DB = db.meta.session.query(types.AssetType). \
                 filter_by(name=kwargs["name"]).first()
        
        for i, pStep_DB in enumerate(aType_DB.steps):
            self.assertEquals(aType.steps[i].name, pStep_DB.name)
            self.assertEquals(aType.steps[i].description, pStep_DB.description) 
        
        
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Booking(self):
        """testing the persistancy of Booking
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Comment(self):
        """testing the persistancy of Comment
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Department(self):
        """testing the persistancy of Department
        """
        
        name = "TestDepartment_test_persisting_Department"
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
            name="user1_test_persisting_department",
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
            name="user2_test_persisting_department",
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
            name="user3_test_persisting_department",
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
        
        db.meta.session.add(testDepartment)
        db.meta.session.commit()
        
        # lets check the data
        # first get the department from the db
        dep_from_db = db.meta.session.query(department.Department). \
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
    def test_persisting_Entity(self):
        """testing the persistancy of Entity
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
        db.meta.session.add(testEntity)
        db.meta.session.commit()
        
        # now try to retrieve it
        testEntityDB = db.meta.session.query(entity.Entity). \
                     filter_by(name=name).first()
        
        # just test the entity part of the object
        for i, tag_ in enumerate(testEntity.tags):
            self.assertEquals(tag_, testEntityDB.tags[i])
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Group(self):
        """testing the persistancy of Group
        """
        
        self.fail("test is not implmented yet")
    
    
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_ImageFormat(self):
        """testing the persistancy of ImageFormat
        """
        
        # get the admin
        session = db.meta.session
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
        self.assertEquals(imFormat.width, imFormat_db.width)
        self.assertEquals(imFormat.height, imFormat_db.height)
        self.assertEquals(imFormat.pixel_aspect, imFormat_db.pixel_aspect)
        self.assertEquals(imFormat.print_resolution,
                          imFormat_db.print_resolution)
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_PipelineStep(self):
        """testing the persistancy of PipelineStep
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
        db.meta.session.add(pStep)
        
        # retrieve it back
        pStep_DB = db.meta.session.query(pipelineStep.PipelineStep). \
                 filter_by(name=kwargs["name"]). \
                 filter_by(description=kwargs["description"]). \
                 first()
        
        # lets compare it
        self.assertEquals(pStep.code, pStep_DB.code)
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Project(self):
        """testing the persistancy of Project
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Link(self):
        """testing the persistancy of Link
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
            "type_": sound_link_type
        }
        
        new_link = link.Link(**kwargs)
        
        # persist it
        db.meta.session.add_all([sound_link_type, new_link])
        db.meta.session.commit()
        
        print "new_link.name       : %s" % new_link.name
        print "new_link.path       : %s" % new_link.path
        print "new_link.filename   : %s" % new_link.filename
        print "new_link.type_.name : %s" % new_link.type_.name
        
        # retrieve it back
        link_DB = db.meta.session.query(link.Link).\
                filter_by(name=kwargs["name"]).first()
        print "link_DB.name        : %s" % link_DB.name
        
        self.assertTrue(new_link==link_DB)
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Repository(self):
        """testing the persistancy of Repository
        """
        
        # get the admin
        session = db.meta.session
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
    def test_persisting_Sequence(self):
        """testing the persistancy of Sequence
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Shot(self):
        """testing the persistancy of Shot
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_SimpleEntity(self):
        """testing the persistancy of SimpleEntity
        """
        
        name = "SimpleEntity_test_creating_of_a_SimpleEntity"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        date_created = date_updated = datetime.datetime.now()
        
        aSimpleEntity = entity.SimpleEntity(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated)
        
        # persist it to the database
        db.meta.session.add(aSimpleEntity)
        db.meta.session.commit()
        
        # now try to retrieve it
        SE_from_DB = db.meta.session.query(entity.SimpleEntity). \
            filter_by(name=name).first()
        
        self.assertEquals(aSimpleEntity.name, SE_from_DB.name)
        self.assertEquals(aSimpleEntity.description, SE_from_DB.description)
        self.assertEquals(aSimpleEntity.created_by, SE_from_DB.created_by)
        self.assertEquals(aSimpleEntity.updated_by, SE_from_DB.updated_by)
        self.assertEquals(aSimpleEntity.date_created, SE_from_DB.date_created)
        self.assertEquals(aSimpleEntity.date_updated, SE_from_DB.date_updated)
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Status(self):
        """testing the persistancy of Status
        """
        
        # the status
        name = "TestStatus_test_creating_Status"
        description = "this is for testing purposes"
        created_by = None
        updated_by = None
        date_created = datetime.datetime.now()
        date_updated = datetime.datetime.now()
        
        testStatus = status.Status(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated,
            short_name="tstSt"
        )
        
        # persist it to the database
        db.meta.session.add(testStatus)
        db.meta.session.commit()
        
        # now try to retrieve it
        testStatusDB = db.meta.session.query(status.Status).first()
        
        # just test the satuts part of the object
        self.assertEquals(testStatus.short_name, testStatusDB.short_name)
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_StatusList(self):
        """testing the persistancy of StatusList
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Structure(self):
        """testing the persistancy of Structure
        """
        
        session = db.meta.session
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
            type_=char_asset_type
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
            type_=image_link_type
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
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Tag(self):
        """testing the persistancy of Tag
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
        db.meta.session.add(aTag)
        db.meta.session.commit()
        
        # now try to retrieve it
        tag_query = db.meta.session.query(tag.Tag)
        Tag_from_DB = tag_query.filter_by(name=name).first()
        
        self.assertEquals(aTag.name, Tag_from_DB.name)
        self.assertEquals(aTag.description, Tag_from_DB.description)
        self.assertEquals(aTag.created_by, Tag_from_DB.created_by)
        self.assertEquals(aTag.updated_by, Tag_from_DB.updated_by)
        self.assertEquals(aTag.date_created, Tag_from_DB.date_created)
        self.assertEquals(aTag.date_updated, Tag_from_DB.date_updated)
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Task(self):
        """testing the persistancy of Task
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_TypeTemplate(self):
        """testing the persistancy of TypeTemplate
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
            "type_": movie_link_type,
        }
        
        aTypeTemplate = types.TypeTemplate(**kwargs)
        
        # persist it
        session = db.meta.session
        session.add(aTypeTemplate)
        session.commit()
        
        # get it back
        aTypeTemplate_DB = session.query(types.TypeTemplate).\
                     filter_by(name=kwargs["name"]).\
                     filter_by(description=kwargs["description"]).first()
        
        self.assertTrue(aTypeTemplate==aTypeTemplate_DB)
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_User(self):
        """testing the persistancy of User
        """
        
        self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Version(self):
        """testing the persistancy of Version
        """
        
        self.fail("test is not implemented yet")
        