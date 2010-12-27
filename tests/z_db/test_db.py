#-*- coding: utf-8 -*-


import datetime
import unittest
from stalker import db, models






########################################################################
class DatabaseTester(unittest.TestCase):
    """tests the database and connection to the database
    """
    
    ##----------------------------------------------------------------------
    #def setUp(self):
        #"""setup the tests
        #"""
        
        #print "seting up the tests"
        #from stalker import db, models
    
    
    
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
        databaseAddress = 'sqlite:///:memory:'
        
        db.setup(databaseAddress)
        
        
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
        
        self.fail('test is not implemented yet')
    
    
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
    def setUp(self):
        """setup the test
        """
        
        # setup the database
        
        # create a test database, possibly an in memory datase
        db.setup(database='sqlite:///:memory:')
        self.session = db.meta.session
    
    
    
    ##----------------------------------------------------------------------
    #def tearDown(self):
        #"""tear-off the test
        #"""
        
        ## just delete the session
        #del(self.session)
    
    
    
    #----------------------------------------------------------------------
    def test_creating_of_a_SimpleEntity(self):
        """testing persistancy of a SimpleEntity object
        """
        
        name = 'aSimpleEntity'
        description = 'this is for testing purposes'
        created_by = None
        updated_by = None
        date_created = date_updated = datetime.datetime.now()
        
        aSimpleEntity = models.entity.SimpleEntity(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated)
        
        # persist it to the database
        self.session.add(aSimpleEntity)
        self.session.commit()
        
        # now try to retrieve it
        SE_from_DB = self.session.query(models.entity.SimpleEntity).first()
        
        self.assertEquals(aSimpleEntity.name, SE_from_DB.name)
        self.assertEquals(aSimpleEntity.description, SE_from_DB.description)
        self.assertEquals(aSimpleEntity.created_by, SE_from_DB.created_by)
        self.assertEquals(aSimpleEntity.updated_by, SE_from_DB.updated_by)
        self.assertEquals(aSimpleEntity.date_created, SE_from_DB.date_created)
        self.assertEquals(aSimpleEntity.date_updated, SE_from_DB.date_updated)
    
    
    
    #----------------------------------------------------------------------
    def test_creating_a_Tag(self):
        """testing persistancy of a Tag object
        """
        
        name = 'aTag'
        description = 'this is for testing purposes'
        created_by = None
        updated_by = None
        date_created = date_updated = datetime.datetime.now()
        
        aTag = models.tag.Tag(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated)
        
        # persist it to the database
        self.session.add(aTag)
        self.session.commit()
        
        # now try to retrieve it
        Tag_from_DB = self.session.query(models.tag.Tag).first()
        
        self.assertEquals(aTag.name, Tag_from_DB.name)
        self.assertEquals(aTag.description, Tag_from_DB.description)
        self.assertEquals(aTag.created_by, Tag_from_DB.created_by)
        self.assertEquals(aTag.updated_by, Tag_from_DB.updated_by)
        self.assertEquals(aTag.date_created, Tag_from_DB.date_created)
        self.assertEquals(aTag.date_updated, Tag_from_DB.date_updated)
    
    
    
    #----------------------------------------------------------------------
    def test_creating_an_Entity(self):
        """testing persistancy of an Entity object
        """
        
        # create an Entity wiht a couple of tags
        
        # the Tag1
        name = 'Tag1'
        description = 'this is for testing purposes'
        created_by = None
        updated_by = None
        date_created = date_updated = datetime.datetime.now()
        
        tag1 = models.tag.Tag(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated)
        
        # the Tag2
        name = 'Tag2'
        description = 'this is for testing purposes'
        created_by = None
        updated_by = None
        date_created = date_updated = datetime.datetime.now()
        
        tag2 = models.tag.Tag(
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
        
        testEntity = models.entity.Entity(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated,
            tags=[tag1, tag2],
        )
        
        # persist it to the database
        self.session.add(testEntity)
        self.session.commit()
        
        # now try to retrieve it
        testEntityDB = self.session.query(models.entity.Entity).first()
        
        # just test the entity part of the object
        self.assertEquals(testEntity.tags, testEntityDB.tags)
    
    
    
    #----------------------------------------------------------------------
    def test_creating_a_Status(self):
        """testing persistancy of a Status object
        """
        
        # the status
        name = 'TestStatus'
        description = 'this is for testing purposes'
        created_by = None
        updated_by = None
        date_created = date_updated = datetime.datetime.now()
        
        testStatus = models.status.Status(
            name=name,
            description=description,
            created_by=created_by,
            updated_by=updated_by,
            date_created=date_created,
            date_updated=date_updated,
        )
        
        # persist it to the database
        self.session.add(testEntity)
        self.session.commit()
        
        # now try to retrieve it
        testEntityDB = self.session.query(models.entity.Entity).first()
        
        # just test the entity part of the object
        self.assertEquals(testEntity.tags, testEntityDB.tags)
        