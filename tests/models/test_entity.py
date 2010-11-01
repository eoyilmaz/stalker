#-*- coding: utf-8 -*-



import unittest
import mocker
import datetime
from stalker.models import entity, user, link, tag, status





########################################################################
class SimpleEntityTest(mocker.MockerTestCase):
    """testing the SimpleEntity class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """seting up some proper values
        """
        self.name = 'Test Entity'
        self.description = "This is a test entity, and this is a proper \
        description for it"
        
        # create some mock tag objects, not neccessarly needed but create them
        self.mock_tag1 = self.mocker.mock(tag.Tag)
        self.mock_tag2 = self.mocker.mock(tag.Tag)
        
        self.tags = [self.mock_tag1, self.mock_tag2]
        
        # now replay it
        self.mocker.replay()
        
        # create a proper SimpleEntity to use it later in the tests
        self.simple_entity = entity.SimpleEntity(
            name=self.name,
            description=self.description,
            tags=self.tags
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_attribute_init_as_empty(self):
        """testing if ValueError is raised for empty name attribute
        """
        
        self.assertRaises(
            ValueError,
            entity.SimpleEntity,
            name='',
            description=self.description,
            tags=self.tags,
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_attribute_init_as_None(self):
        """testing if ValueError is raised for None name attribute
        """
        
        self.assertRaises(
            ValueError,
            entity.SimpleEntity,
            name=None,
            description=self.description,
            tags=self.tags,
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_property_for_being_empty(self):
        """testing if ValueError is raised when trying to set the name to an
        empty string
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            "name",
            ""
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_property_for_being_None(self):
        """testing if ValueError is raised when trying to set the name to None
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            "name",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_property_not_being_string_or_unicode(self):
        """testing if ValueError is raised when trying to set the name
        something other than a string or unicode
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            "name",
            10
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_attribute_not_init_as_string_or_unicode(self):
        """testing if ValueError is raised when trying to initialize the name
        attribute to something else than a string or unicode
        """
        
        self.assertRaises(
            ValueError,
            entity.SimpleEntity,
            name=1,
            description=self.description,
            tags=self.tags,
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_property_is_conditioned(self):
        """testing if the name is conditioned correctly
        """
        
        test_group = [
            ("testName", "TestName"),
            ("1testName", "TestName"),
            ("_testName", "TestName"),
            ("2423$+^^+^'%+%%&_testName", "TestName"),
            ("2423$+^^+^'%+%%&_testName_35", "TestName_35"),
            ("2423$ +^^+^ '%+%%&_ testName_ 35", "TestName_35"),
        ]
        
        for test_value in test_group:
            # set the new name
            self.simple_entity.name = test_value[0]
            
            self.assertEquals(
                self.simple_entity.name,
                test_value[1],
                "the name property is not correctly conditioned for, " + \
                    test_value[0] + ", " + test_value[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_description_init_with_something_else_than_string_or_unicode(self):
        """testing if ValueError raised when trying to initialize the
        desription attribute with something else than a string or unicode
        """
        
        self.assertRaises(
            ValueError,
            entity.SimpleEntity,
            name=self.name,
            description=100,
            tags=self.tags,
        )
    
    
    
    #----------------------------------------------------------------------
    def test_description_property_being_string_or_unicode(self):
        """testing if ValueError raised when trying to set the description
        property to something else then a string or unicode
        """
        
        test_value = 1.0
        
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            "description",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_tags_being_not_intialized(self):
        """test if nothing is raised when creating an entity without setting a
        tags parameter
        """
        
        # this should work without errors
        aNewSimpleEntity = entity.SimpleEntity(
            name=self.name,
            description=self.description,
        )
    
    
    
    #----------------------------------------------------------------------
    def test_tags_being_initialized_as_an_empty_list(self):
        """test if tags is initialized as an empty list
        """
        
        # this should work without errors
        aNewSimpleEntity = entity.SimpleEntity(
            name=self.name,
            description=self.description,
        )
        
        expected_result = []
        
        self.assertEquals(aNewSimpleEntity.tags, expected_result)
    
    
    
    #----------------------------------------------------------------------
    def test_tags_init_with_something_other_than_a_list(self):
        """test if a ValueError is going to be raised when initializing the
        tags with something other than a list
        """
        
        #-----------------------
        # a string
        test_value = ""
        
        self.assertRaises(
            ValueError,
            entity.SimpleEntity,
            name=self.name,
            description=self.description,
            tags=test_value,
        )
        
        
        #-----------------------
        # an integer
        test_value = 1231
        
        self.assertRaises(
            ValueError,
            entity.SimpleEntity,
            name=self.name,
            description=self.description,
            tags=test_value,
        )
    
    
    
    #----------------------------------------------------------------------
    def test_tags_property_set_properly(self):
        """testing if the property is set correctly
        """
        
        test_value = [self.mock_tag1]
        
        self.simple_entity.tags = test_value
        
        self.assertEquals(self.simple_entity.tags, test_value)






########################################################################
class AuditEntity(mocker.MockerTestCase):
    """testing the AuditEntity class
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # create a couple of mock tag objects
        self.mock_tag1 = self.mocker.mock(tag.Tag)
        self.mock_tag2 = self.mocker.mock(tag.Tag)
        
        # create a mock user
        self.mock_user = self.mocker.mock(user.User)
        
        self.mocker.replay()
        
        self.name = 'The Entity Object'
        self.description = 'This is a test object, to be used in tests'
        self.tags = [self.mock_tag1, self.mock_tag2]
        self.date_created = datetime.datetime(2010, 10, 21, 3, 8, 0)
        self.date_updated = self.date_created
        
        # create a proper audit entity object
        self.audit_entity = entity.AuditEntity(
            name=self.name,
            description=self.description,
            tags=self.tags,
            created_by=self.mock_user,
            updated_by=self.mock_user,
            date_created=self.date_created,
            date_updated=self.date_updated,
        )
    
    
    
    #----------------------------------------------------------------------
    def test_created_by_attribute_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.modles.User object to created_by **attribute**
        """
        # the created_by attribute should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = 'A User Name'
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse( isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            'created_by',
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_created_by_property_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.modles.User object to created_by **property**
        """
        # the created_by attribute should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = 'A User Name'
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse( isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            'created_by',
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_created_by_attribute_empty(self):
        """testing if ValueError is raised when the created_by is tried to be
        set to None
        """
        
        # it can not be empty (the first created user going to have some
        # problems if we dont allow empty users, the database should be
        # initialized with an admin user)
        #
        
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            'created_by',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_created_by_property_empty(self):
        """testing if ValueError is raised when the created_by is tried to be
        set to None
        """
        
        # it can not be empty (the first created user going to have some
        # problems if we dont allow empty users, the database should be
        # initialized with an admin user)
        #
        
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            'created_by',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_updated_by_attribute_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.modles.User object to updated_by **attribute**
        """
        # the updated_by attribute should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = 'A User Name'
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse(isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            'updated_by',
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_updated_by_property_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.modles.User object to update_by **property**
        """
        # the updated_by attribute should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = 'A User Name'
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse( isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            'updated_by',
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_updated_by_attribute_empty(self):
        """testing if ValueError is raised when the updated_by is tried to be
        set to None
        """
        
        # it can not be empty (the first created user going to have some
        # problems if we dont allow empty users, the database should be
        # initialized with an admin user)
        #
        
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            'updated_by',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_created_by_property_empty(self):
        """testing if ValueError is raised when the created_by is tried to be
        set to None
        """
        
        # it can not be empty (the first created user going to have some
        # problems if we dont allow empty users, the database should be
        # initialized with an admin user)
        #
        
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            'created_by',
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_created_attribute_being_datetime(self):
        """testing if ValueError raises when the date_created attribute is set
        to something else than a datetime.datetime object
        """
        
        # the date_created attribute should be an instance of datetime.datetime
        
        # try to set something else and expect a ValueError
        
        test_value = "a string date time 2010-10-26 etc."
        
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse( isinstance(test_value, datetime.datetime) )
        
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            "date_created",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_created_property_being_datetime(self):
        """testing if ValueError raises when the date_created property is set
        to something else than a datetime.datetime object
        """
        
        # the date_created attribute should be an instance of datetime.datetime
        
        # try to set something else and expect a ValueError
        
        test_value = "a string date time 2010-10-26 etc."
        
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse( isinstance(test_value, datetime.datetime) )
        
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            "date_created",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_created_property_being_empty(self):
        """testing if ValueError is raised when the date_created property is
        set to None
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            "date_created",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_updated_attribute_being_datetime(self):
        """testing if ValueError raises when the date_updated attribute is set
        to something else than a datetime.datetime object
        """
        
        # try to set it to something else and expect a ValueError
        test_value = "a string date time 2010-10-26 etc."
        
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse( isinstance(test_value, datetime.datetime) )
        
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            "date_updated",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_updated_property_being_datetime(self):
        """testing if ValueError raises when the date_updated property is set
        to something else than a datetime.datetime object
        """
        
        # try to set something else and expect a ValueError
        test_value = "a string date time 2010-10-26 etc."
        
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse( isinstance(test_value, datetime.datetime) )
        
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            "date_updated",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_updated_property_being_empty(self):
        """testing if ValueError is raised when the date_updated property is
        set to None
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.audit_entity,
            "date_updated",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_created_is_before_date_updated(self):
        """testing if a ValueError is going to be raised when trying to set the
        date_updated to a time before date_created
        """
        
        date_created = datetime.datetime(2000, 1, 1, 1, 1, 1)
        date_updated = datetime.datetime(1990, 1, 1, 1, 1, 1)
        
        # create a new entity with these dates
        # and expect a ValueError
        self.assertRaises(
            ValueError,
            entity.AuditEntity,
            name=self.name,
            description=self.description,
            tags=self.tags,
            created_by=self.mock_user,
            updated_by=self.mock_user,
            date_created=date_created,
            date_updated=date_updated,
        )






########################################################################
class EntityTest(mocker.MockerTestCase):
    """tests the entity class
    
    all the attributes to objects needs a mock object of that object, that is:
    user
    link
    entity
    file
    note
    status_list
    tag
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        assert(isinstance(self.mocker, mocker.Mocker))
        
        # create
        # a mock user
        self.mock_user = self.mocker.mock(user.User)
        
        # a mock tag
        self.mock_tag1 = self.mocker.mock(tag.Tag)
        self.mock_tag2 = self.mocker.mock(tag.Tag)
        
        # a mock status_list
        self.mock_status_list = self.mocker.mock(status.StatusList)
        statusCnt = len(self.mock_status_list.statuses)
        self.mocker.result(5)
        self.mocker.count(0, None)
        
        self.mocker.replay()
        
        self.name = 'Test Entity'
        self.description = 'Just testing the very first entity'
        self.date_created = datetime.datetime(2010, 10, 21, 3, 8, 0)
        self.date_updated = self.date_created
        
        
        # create a proper entity object
        self.entity = entity.Entity(
            name=self.name,
            description=self.description,
            tags=[self.mock_tag1, self.mock_tag2],
            created_by=self.mock_user,
            updated_by=self.mock_user,
            status_list=self.mock_status_list,
            status=0,
            date_created=self.date_created,
            date_updated=self.date_updated,
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_init_with_something_else_then_StatusList_1(self):
        """testing if ValueError is going to be raised when trying to
        initialize status_list with something other than a StatusList
        """
        
        self.assertRaises(
            ValueError,
            entity.Entity,
            name=self.name,
            created_by=self.mock_user,
            updated_by=self.mock_user,
            status_list=100,
        )
        
        self.assertRaises(
            ValueError,
            entity.Entity,
            name=self.name,
            created_by=self.mock_user,
            updated_by=self.mock_user,
            status_list='',
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_init_with_something_else_then_StatusList_2(self):
        """testing if ValueError is going to be raised when trying to
        initialize status_list with None
        """
        
        self.assertRaises(
            ValueError,
            entity.Entity,
            name=self.name,
            created_by=self.mock_user,
            updated_by=self.mock_user,
            status_list=None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_property_set_to_something_other_than_StatusList(self):
        """testing if ValueError is going to be raised when trying to set the
        status_list to something else than a StatusList object
        """
        
        test_value = "a string"
        
        # be sure that the test value is not a StatusList
        self.assertFalse(isinstance(test_value, status.StatusList))
        
        # now try to set it
        self.assertRaises(
            ValueError,
            setattr,
            self.entity,
            "status_list",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_property_set_to_None(self):
        """testing if ValueError is going to be raised when trying to set the
        status_list to None
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.entity,
            "status_list",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_being_omited(self):
        """testing if a ValueError going to be raised when omiting the
        status_list attribute
        """
        
        self.assertRaises(
            ValueError,
            entity.Entity,
            name=self.name,
            created_by=self.mock_user,
            updated_by=self.mock_user
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_init_different_than_an_int(self):
        """testing if a ValueError is going to be raised if trying to initialize
        status with something else than an integer
        """
        
        # with a string
        test_value = '0'
        
        self.assertRaises(
            ValueError,
            entity.Entity,
            name=self.name,
            created_by=self.mock_user,
            updated_by=self.mock_user,
            status_list=self.mock_status_list,
            status=test_value
        )
        
        # with a list
        test_value = [0]
        
        self.assertRaises(
            ValueError,
            entity.Entity,
            name=self.name,
            created_by=self.mock_user,
            updated_by=self.mock_user,
            status_list=self.mock_status_list,
            status=test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_property_set_to_other_than_int(self):
        """testing if ValueError going to be raised when trying to set the
        current status to something other than an integer
        """
        
        test_value = "a string"
        
        self.assertRaises(
            ValueError,
            setattr,
            self.entity,
            "status",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_property_set_to_too_high(self):
        """testing if a ValueError is going to be raised when trying to set the
        current status to something higher than it is allowd to, that is it
        couldn't be set a value higher than len(statusList.statuses - 1)
        """
        
        test_value = len(self.mock_status_list.statuses)
        
        self.assertRaises(
            ValueError,
            setattr,
            self.entity,
            "status",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_property_set_to_too_low(self):
        """testing if a ValueError is going to be raised when trying to set the
        current status to something lower than it is allowed to, that is it
        couldn't be set to value lower than 0
        """
        
        test_value = -1
        self.assertRaises(
            ValueError,
            setattr,
            self.entity,
            "status",
            test_value
        )
    
    
    
    ##----------------------------------------------------------------------
    #def test_links_being_not_intialized(self):
        #"""test if nothing is raised when creating an entity without setting a
        #links parameter
        #"""
        
        ## this should work without errors
        #aNewEntity = entity.Entity(
            #name=self.name,
            #created_by=self.mock_user,
            #updated_by=self.mock_user,
            #status_list= self.mock_status_list
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_links_being_initialized_as_an_empty_list(self):
        #"""test if links is initialized as an empty list
        #"""
        
        ## this should work without errors
        #aNewEntity = entity.Entity(
            #name=self.name,
            #created_by=self.mock_user,
            #updated_by=self.mock_user,
            #status_list= self.mock_status_list
        #)
        
        #expected_result = []
        
        #self.assertEquals(aNewEntity.links, expected_result)
    
    
    
    ##----------------------------------------------------------------------
    #def test_links_init_with_something_other_than_a_list(self):
        #"""test if a ValueError is going to be raised when initializing the
        #links with something other than a list
        #"""
        
        ##-----------------------
        ## a string
        #test_value = ""
        
        #self.assertRaises(
            #ValueError,
            #entity.Entity,
            #name=self.name,
            #created_by=self.mock_user,
            #updated_by=self.mock_user,
            #status_list=self.mock_status_list,
            #status=0,
            #links=test_value
        #)
        
        
        ##-----------------------
        ## an integer
        #test_value = 1231
        
        #self.assertRaises(
            #ValueError,
            #entity.Entity,
            #name=self.name,
            #created_by=self.mock_user,
            #updated_by=self.mock_user,
            #status_list=self.mock_status_list,
            #status=0,
            #links=test_value
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_links_property_being_set_to_something_else_than_a_list(self):
        #"""testing if a ValueError is going to be reaised when setting the list
        #attribute something other than a list
        #"""
        
        #test_value = "a string"
        
        #self.assertRaises(
            #ValueError,
            #setattr,
            #self.entity,
            #"links",
            #test_value
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_links_property_set_properly(self):
        #"""testing if the property is set correctly
        #"""
        
        #test_value = [self.mock_link1]
        
        #self.entity.links = test_value
        
        #self.assertEquals( self.entity.links, test_value )
    
    
    
    #----------------------------------------------------------------------
    def test_notes_being_not_intialized(self):
        """test if nothing is raised when creating an entity without setting a
        notes parameter
        """
        
        # this should work without errors
        aNewEntity = entity.Entity(
            name=self.name,
            created_by=self.mock_user,
            updated_by=self.mock_user,
            status_list= self.mock_status_list
        )
    
    
    
    #----------------------------------------------------------------------
    def test_notes_being_initialized_as_an_empty_list(self):
        """test if notes is initialized as an empty list
        """
        
        # this should work without errors
        aNewEntity = entity.Entity(
            name=self.name,
            created_by=self.mock_user,
            updated_by=self.mock_user,
            status_list= self.mock_status_list
        )
        
        expected_result = []
        
        self.assertEquals(aNewEntity.notes, expected_result)
    
    
    
    #----------------------------------------------------------------------
    def test_notes_init_with_something_other_than_a_list(self):
        """test if a ValueError is going to be raised when initializing the
        notes with something other than a list
        """
        
        #-----------------------
        # a string
        test_value = ""
        
        self.assertRaises(
            ValueError,
            entity.Entity,
            name=self.name,
            created_by=self.mock_user,
            updated_by=self.mock_user,
            status_list=self.mock_status_list,
            status=0,
            notes=test_value
        )
        
        
        #-----------------------
        # an integer
        test_value = 1231
        
        self.assertRaises(
            ValueError,
            entity.Entity,
            name=self.name,
            created_by=self.mock_user,
            updated_by=self.mock_user,
            status_list=self.mock_status_list,
            status=0,
            notes=test_value
        )
    
    
    