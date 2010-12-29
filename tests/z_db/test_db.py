#-*- coding: utf-8 -*-


import os
import datetime
import unittest
import tempfile
from sqlalchemy.orm import clear_mappers
from stalker.conf import defaults
from stalker import db
from stalker.models import (
    asset,
    assetBase,
    assetType,
    booking,
    comment,
    department,
    entity,
    group,
    imageFormat,
    link,
    pipelineStep,
    project,
    repository,
    sequence,
    shot,
    status,
    structure,
    tag,
    task,
    template,
    user,
    version
)



#----------------------------------------------------------------------
def get_admin():
    """returns the admin user from the current database
    """
    
    return db.meta.session.query(user.User). \
          filter_by(name=defaults.ADMIN_NAME).first()






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
        
        self.TEST_DATABASE_FILE = tempfile.mktemp() + '.db'
        self.TEST_DATABASE_DIALECT = 'sqlite:///'
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
        #db.setup(self.TEST_DATABASE_URI)
        
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_creating_a_custom_sqlite_db(self):
        """testing if a custom sqlite database will be created in the given
        location
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_temp_user_deleted(self):
        """testing if the temp user is deleted
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_default_admin_creation(self):
        """testing if a default admin is created
        """
        
        # set default admin creation to True
        defaults.AUTO_CREATE_ADMIN = True
        
        db.setup(self.TEST_DATABASE_URI)
        self._createdDB = True
        
        # check if there is an admin
        admin = get_admin()
        
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
    def test_no_default_admin_creation(self):
        """testing if there is no user if default.AUTO_CREATE_ADMIN is False
        """
        
        # turn down auto admin creation
        defaults.AUTO_CREATE_ADMIN = False
        
        # setup the db
        db.setup(self.TEST_DATABASE_URI)
        self._createdDB = True
        
        # check if there is a use with name admin
        self.assertTrue(get_admin() is None )
        
        # check if there is a admins department
        self.assertTrue(db.meta.session.query(department.Department). \
                        filter_by(name=defaults.ADMIN_DEPARTMENT_NAME). \
                        first() is None)






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
        cls.TEST_DATABASE_FILE = tempfile.mktemp() + '.db'
        cls.TEST_DATABASE_URI = 'sqlite:///' + cls.TEST_DATABASE_FILE
        
        # setup using this db
        db.setup(database=cls.TEST_DATABASE_URI)
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def tearDownClass(cls):
        """tear-off the test
        """
        # delete the default test database file
        os.remove(cls.TEST_DATABASE_FILE)
    
    
    
    ##----------------------------------------------------------------------
    #def test_persisting_Angular(self):
        #"""testing the persistancy of Angular
        #"""
        
        #self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Asset(self):
        """testing the persistancy of Asset
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_AssetBase(self):
        """testing the persistancy of AssetBase
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_AssetType(self):
        """testing the persistancy of AssetType
        """
        
        
        # first get the admin
        admin = get_admin()
        
        # create a couple of PipelineStep objects
        pStep1 = pipelineStep.PipelineStep(
            name='Modeling',
            description='This is where an asset is modeled',
            created_by=admin,
            updated_by=admin,
            code='MDL'
        )
        
        pStep2 = pipelineStep.PipelineStep(
            name='Lighting',
            description="lighting done in this stage, don't mix it with \
            shading",
            created_by=admin,
            updated_by=admin,
            code='LGHT'
        )
        
        # create a new AssetType object
        kwargs = {
            'name': 'Character',
            'description': 'this is a test asset type',
            'created_by': admin,
            'updated_by': admin,
            'steps': [pStep1, pStep2],
        }
        
        aType = assetType.AssetType(**kwargs)
        
        # store it in the db
        db.meta.session.add(aType)
        db.meta.session.commit()
        
        # retrieve it back and check it with the first one
        aType_DB = db.meta.session.query(assetType.AssetType). \
                 filter_by(name=kwargs['name']).first()
        
        for i, pStep_DB in enumerate(aType_DB.steps):
            self.assertEquals(aType.steps[i].name, pStep_DB.name)
            self.assertEquals(aType.steps[i].description, pStep_DB.description) 
        
        
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Booking(self):
        """testing the persistancy of Booking
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Comment(self):
        """testing the persistancy of Comment
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Department(self):
        """testing the persistancy of Department
        """
        
        name = 'TestDepartment_test_persisting_Department'
        description = 'this is for testing purposes'
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
            name='user1_test_persisting_department',
            description='this is for testing purposes',
            created_by=None,
            updated_by=None,
            login_name='user1_tp_department',
            first_name='user1_first_name',
            last_name='user1_last_name',
            email='user1@department.com',
            department=testDepartment
        )
        
        # user2
        user2 = user.User(
            name='user2_test_persisting_department',
            description='this is for testing purposes',
            created_by=None,
            updated_by=None,
            login_name='user2_tp_department',
            first_name='user2_first_name',
            last_name='user2_last_name',
            email='user2@department.com',
            department=testDepartment
        )
        
        # user3
        # create three users, one for lead and two for members
        user3 = user.User(
            name='user3_test_persisting_department',
            description='this is for testing purposes',
            created_by=None,
            updated_by=None,
            login_name='user3_tp_department',
            first_name='user3_first_name',
            last_name='user3_last_name',
            email='user3@department.com',
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
        name = 'Tag1_test_creating_an_Entity'
        description = 'this is for testing purposes'
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
        name = 'Tag2_test_creating_an_Entity'
        description = 'this is for testing purposes'
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
        name = 'TestEntity'
        description = 'this is for testing purposes'
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
        
        self.fail('test is not implmented yet')
    
    
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_ImageFormat(self):
        """testing the persistancy of ImageFormat
        """
        
        # get the admin
        session = db.meta.session
        admin = get_admin()
        
        # create a new ImageFormat object and try to read it back
        kwargs = {
        'name': 'HD',
        'description': 'test image format',
        'created_by': admin,
        'updated_by': admin,
        'width': 1920,
        'height': 1080,
        'pixel_aspect': 1.0,
        'print_resolution': 300.0
        }
        
        # create the ImageFormat object
        imFormat = imageFormat.ImageFormat(**kwargs)
        
        # persist it
        session.add(imFormat)
        session.commit()
        
        # get it back
        imFormat_db = session.query(imageFormat.ImageFormat). \
                filter_by(name=kwargs['name']).first()
        
        # just test the repository part of the attributes
        self.assertEquals(imFormat.width, imFormat_db.width)
        self.assertEquals(imFormat.height, imFormat_db.height)
        self.assertEquals(imFormat.pixel_aspect, imFormat_db.pixel_aspect)
        self.assertEquals(imFormat.print_resolution,
                          imFormat_db.print_resolution)
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Link(self):
        """testing the persistancy of Link
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_PipelineStep(self):
        """testing the persistancy of PipelineStep
        """
        
        # create a new PipelineStep
        admin = get_admin()
        
        kwargs = {
            'name': 'RENDER',
            'description': 'this is the step where all the assets are \
            rendered',
            'created_by': admin,
            'code': 'RNDR'
        }
        
        pStep = pipelineStep.PipelineStep(**kwargs)
        
        # save it to database
        db.meta.session.add(pStep)
        
        # retrieve it back
        pStep_DB = db.meta.session.query(pipelineStep.PipelineStep). \
                 filter_by(name=kwargs['name']). \
                 filter_by(description=kwargs['description']). \
                 first()
        
        # lets compare it
        self.assertEquals(pStep.code, pStep_DB.code)
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Project(self):
        """testing the persistancy of Project
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Repository(self):
        """testing the persistancy of Repository
        """
        
        # get the admin
        session = db.meta.session
        admin = get_admin()
        
        # create a new Repository object and try to read it back
        kwargs = {
        'name': 'Movie-Repo',
        'description': 'test repository',
        'created_by': admin,
        'updated_by': admin,
        'linux_path': '/mnt/M',
        'osx_path': '/mnt/M',
        'windows_path': 'M:\\'
        }
        
        # create the repository object
        repo = repository.Repository(**kwargs)
        
        # persist it
        session.add(repo)
        session.commit()
        
        # get it back
        repo_db = session.query(repository.Repository). \
                filter_by(name=kwargs['name']).first()
        
        # just test the repository part of the attributes
        self.assertEquals(repo.linux_path, repo_db.linux_path)
        self.assertEquals(repo.windows_path, repo_db.windows_path)
        self.assertEquals(repo.osx_path, repo_db.osx_path)
        self.assertEquals(repo.path, repo_db.path)
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Sequence(self):
        """testing the persistancy of Sequence
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Shot(self):
        """testing the persistancy of Shot
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_SimpleEntity(self):
        """testing the persistancy of SimpleEntity
        """
        
        name = 'SimpleEntity_test_creating_of_a_SimpleEntity'
        description = 'this is for testing purposes'
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
        name = 'TestStatus_test_creating_Status'
        description = 'this is for testing purposes'
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
            short_name='tstSt'
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
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Structure(self):
        """testing the persistancy of Structure
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Tag(self):
        """testing the persistancy of Tag
        """
        
        name = 'Tag_test_creating_a_Tag'
        description = 'this is for testing purposes'
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
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Template(self):
        """testing the persistancy of Template
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_User(self):
        """testing the persistancy of User
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_persisting_Version(self):
        """testing the persistancy of Version
        """
        
        self.fail('test is not implemented yet')
        