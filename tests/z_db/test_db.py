#-*- coding: utf-8 -*-


import datetime
import unittest
import tempfile
from sqlalchemy.orm import clear_mappers
from stalker.conf import defaults
from stalker import db
from stalker.models import asset, assetBase, booking, comment, department, \
     entity, group, imageFormat, link, pipelineStep, project, repository, \
     sequence, shot, status, structure, tag, task, template, unit, user, \
     version









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
        
        self.TEST_DATABASE_FILE = tempfile.mktemp() + '.db'
        self.TEST_DATABASE_URI = 'sqlite:///' + self.TEST_DATABASE_FILE
    
    
    
    ##----------------------------------------------------------------------
    #def tearDown(self):
        #"""tearDown the tests
        #"""
        #del(db, models)
        #del(sys.modules['stalker'])
        #del(sys.modules['stalker.db'])
        #del(sys.modules['stalker.models'])
    
    
    
    #----------------------------------------------------------------------
    def test_creating_a_custom_in_memory_db(self):
        """testing if a custom in-memory sqlite database will be created
        """
        
        # create a database in memory
        db.setup(self.TEST_DATABASE_URI)
        
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_creating_a_custom_sqlite_db(self):
        """testing if a custom sqlite database will be created in the given
        location
        """
        
        self.fail('test is not implemented yet')
    
    
    
    #----------------------------------------------------------------------
    def test_default_admin_creation(self):
        """testing if a default admin is created
        """
        
        # set default admin creation to True
        defaults.AUTO_CREATE_ADMIN = True
        
        db.setup(self.TEST_DATABASE_URI)
        
        ## check if there is an admin
        #self.fail('test is not implemented yet')
        
        admin = db.meta.session.query(user.User).filter_by(name='admin').first()
        
        self.assertEquals(admin.name, defaults.ADMIN_NAME)
    
    
    
    #----------------------------------------------------------------------
    def test_default_admin_for_already_created_databases(self):
        """testing if no extra admin is going to be created for already setup
        databases
        """
        
        self.fail('test is not implemented yet')
    
    
    
    ##----------------------------------------------------------------------
    #def (self):
        #""""""
        






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
        
        # create a test database, possibly an in memory datase
        cls.TEST_DATABASE_FILE = tempfile.mktemp() + '.db'
        cls.TEST_DATABASE_URI = 'sqlite:///' + cls.TEST_DATABASE_FILE
        
        db.setup(database=cls.TEST_DATABASE_URI)
        
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def tearDownClass(cls):
        """tear-off the test
        """
        # delete the default test database file
        #import os
        #os.remove(defaults.TEST_DATABASE_FILE)
        
        
        
        # \033[22;30m is black
        # \033[22;31m is red
        # \033[22;32m is green
        # \033[22;37m is gray
     
        print "\033[22;31mtearDown class\033[22;37m"
        
        #import tempfile
        #file(tempfile.mktemp(), 'w').write('tests ended')
    
    
    
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
        Tag_from_DB = db.meta.session.query(tag.Tag).filter_by(name=name).first()
        
        self.assertEquals(aTag.name, Tag_from_DB.name)
        self.assertEquals(aTag.description, Tag_from_DB.description)
        self.assertEquals(aTag.created_by, Tag_from_DB.created_by)
        self.assertEquals(aTag.updated_by, Tag_from_DB.updated_by)
        self.assertEquals(aTag.date_created, Tag_from_DB.date_created)
        self.assertEquals(aTag.date_updated, Tag_from_DB.date_updated)
    
    
    
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
        
        self.fail('test is not implemented')
    
    
    
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
        
