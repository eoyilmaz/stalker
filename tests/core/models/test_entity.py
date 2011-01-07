#-*- coding: utf-8 -*-



import unittest
import mocker
import datetime
from stalker.core.models import entity, user, link, tag, status





########################################################################
class SimpleEntityTester(mocker.MockerTestCase):
    """testing the SimpleEntity class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """seting up some proper values
        """
        # create a mock user
        self.mock_user = self.mocker.mock(user.User)
        self.mocker.replay()
        
        self.date_created = datetime.datetime(2010, 10, 21, 3, 8, 0)
        self.date_updated = self.date_created
        
        self.kwargs = {
            'name': 'Test Entity',
            'description': "This is a test entity, and this is a proper \
            description for it",
            'created_by': self.mock_user,
            'updated_by': self.mock_user,
            'date_created': self.date_created,
            'date_updated': self.date_updated,
        }
        
        # create a proper SimpleEntity to use it later in the tests
        self.simple_entity = entity.SimpleEntity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_being_empty(self):
        """testing if ValueError is raised for empty name argument
        """
        
        self.kwargs['name'] = ''
        self.assertRaises(ValueError, entity.SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_init_as_None(self):
        """testing if ValueError is raised for None name argument
        """
        
        self.kwargs['name'] = None
        self.assertRaises(ValueError, entity.SimpleEntity, **self.kwargs)
    
    
    
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
    def test_name_argument_not_init_as_string_or_unicode(self):
        """testing if ValueError is raised when trying to initialize the name
        argument to something else than a string or unicode
        """
        
        test_values = [1, 1.2, ['a name'], {'a': 'name'}]
        for test_value in test_values:
            self.kwargs['name'] = test_value
            self.assertRaises(ValueError, entity.SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_name_property_is_conditioned(self):
        """testing if name is conditioned correctly
        """
        
        test_values = [
            ("testName", "testName"),
            ("1testName", "testName"),
            ("_testName", "testName"),
            ("2423$+^^+^'%+%%&_testName", "testName"),
            ("2423$+^^+^'%+%%&_testName_35", "testName_35"),
            ("2423$ +^^+^ '%+%%&_ testName_ 35", "testName_ 35"),
            ("SH001","SH001"),
        ]
        
        for test_value in test_values:
            # set the new name
            self.simple_entity.name = test_value[0]
            
            self.assertEquals(
                self.simple_entity.name,
                test_value[1],
                "the name property is not correctly formatted for, " + \
                    test_value[0] + ", " + test_value[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_nice_name_is_formatted_correctly(self):
        """testing if nice name is formatted correctly
        """
        
        test_values = [
            ("testName", "test_name"),
            ("1testName", "test_name"),
            ("_testName", "test_name"),
            ("2423$+^^+^'%+%%&_testName", "test_name"),
            ("2423$+^^+^'%+%%&_testName_35", "test_name_35"),
            ("2423$ +^^+^ '%+%%&_ testName_ 35", "test_name_35"),
            ("SH001","sh001"),
            ("My name is Ozgur", "my_name_is_ozgur"),
            (" this is another name for an asset", 
             "this_is_another_name_for_an_asset"),
        ]
        
        for test_value in test_values:
            self.simple_entity.name = test_value[0]
            
            self.assertEquals(
                self.simple_entity.nice_name,
                test_value[1],
                "the nice name property is not correctly formatted for, " + \
                    test_value[0] + ", " + test_value[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_nice_name_property_is_read_only(self):
        """testing if nice name property is read-only
        """
        
        self.assertRaises(
            AttributeError,
            setattr,
            self.simple_entity,
            "nice_name",
            "a text"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_description_argument_accepts_string_or_unicode_only(self):
        """testing if ValueError raised when trying to initialize the
        desription argument with something else than a string or unicode
        """
        
        test_values = [1, 1.2, ['a description'], {'a': 'description'}]
        
        for test_value in test_values:
            self.kwargs['description'] = test_value
            
            self.assertRaises(ValueError, entity.SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_description_property_being_string_or_unicode(self):
        """testing if ValueError raised when trying to set the description
        property to something else then a string or unicode
        """
        
        test_values = [1, 1.2, ['a description'], {'a': 'description'}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.simple_entity,
                "description",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_created_by_argument_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.core.models.user.User object to created_by argument
        """
        # the created_by argument should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = 'A User Name'
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse( isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            'created_by',
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_created_by_property_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.modles.User object to created_by **property**
        """
        # the created_by property should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = 'A User Name'
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse( isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            'created_by',
            test_value
        )
    
    
    
    ##----------------------------------------------------------------------
    #def test_created_by_argument_empty(self):
        #"""testing if ValueError is raised when the created_by is tried to be
        #set to None
        #"""
        
        ## it can not be empty (the first created user going to have some
        ## problems if we dont allow empty users, the database should be
        ## initialized with an admin user)
        ##
        
        #self.assertRaises(
            #ValueError,
            #setattr,
            #self.simple_entity,
            #'created_by',
            #None
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_created_by_property_empty(self):
        #"""testing if ValueError is raised when the created_by is tried to be
        #set to None
        #"""
        
        ## it can not be empty (the first created user going to have some
        ## problems if we dont allow empty users, the database should be
        ## initialized with an admin user)
        ##
        
        #self.assertRaises(
            #ValueError,
            #setattr,
            #self.simple_entity,
            #'created_by',
            #None
        #)
    
    
    
    #----------------------------------------------------------------------
    def test_updated_by_argument_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.modles.User object to updated_by argument
        """
        # the updated_by argument should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = 'A User Name'
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse(isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            'updated_by',
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_updated_by_property_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.modles.User object to update_by **property**
        """
        # the updated_by property should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = 'A User Name'
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse( isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            'updated_by',
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_updated_by_argument_empty(self):
        """testing if initializing updated_by with None causes it to be set to
        the same value with created_by argument
        """
        
        #self.assertRaises(
            #ValueError,
            #setattr,
            #self.simple_entity,
            #'updated_by',
            #None
        #)
        
        self.kwargs['updated_by'] = None
        
        aNewSimpleEntity = entity.SimpleEntity(**self.kwargs)
        
        # now check if they are same
        self.assertEquals(aNewSimpleEntity.created_by,
                          aNewSimpleEntity.updated_by)
    
    
    
    ##----------------------------------------------------------------------
    #def test_created_by_property_empty(self):
        #"""testing if ValueError is raised when the created_by is tried to be
        #set to None
        #"""
        
        ## it can not be empty (the first created user going to have some
        ## problems if we dont allow empty users, the database should be
        ## initialized with an admin user)
        ##
        
        #self.assertRaises(
            #ValueError,
            #setattr,
            #self.simple_entity,
            #'created_by',
            #None
        #)
    
    
    
    #----------------------------------------------------------------------
    def test_date_created_argument_accepts_datetime_only(self):
        """testing if ValueError raises when the date_created argument is set
        to something else than a datetime.datetime object
        """
        
        # the date_created argument should be an instance of datetime.datetime
        
        # try to set something else and expect a ValueError
        
        test_value = "a string date time 2010-10-26 etc."
        
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse( isinstance(test_value, datetime.datetime) )
        
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            "date_created",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_created_property_accepts_datetime_only(self):
        """testing if ValueError raises when the date_created property is set
        to something else than a datetime.datetime object
        """
        
        # the date_created property should be an instance of datetime.datetime
        
        # try to set something else and expect a ValueError
        
        test_value = "a string date time 2010-10-26 etc."
        
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse( isinstance(test_value, datetime.datetime) )
        
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
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
            self.simple_entity,
            "date_created",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_updated_argument_accepts_datetime_only(self):
        """testing if ValueError raises when the date_updated argument is set
        to something else than a datetime.datetime object
        """
        
        # try to set it to something else and expect a ValueError
        test_value = "a string date time 2010-10-26 etc."
        
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse( isinstance(test_value, datetime.datetime) )
        
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
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
            self.simple_entity,
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
            self.simple_entity,
            "date_updated",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_created_is_before_date_updated(self):
        """testing if a ValueError is going to be raised when trying to set the
        date_updated to a time before date_created
        """
        
        
        self.kwargs['date_created'] = datetime.datetime(2000, 1, 1, 1, 1, 1)
        self.kwargs['date_updated'] = datetime.datetime(1990, 1, 1, 1, 1, 1)
        
        # create a new entity with these dates
        # and expect a ValueError
        self.assertRaises(ValueError, entity.SimpleEntity, **self.kwargs)





########################################################################
class EntityTester(mocker.MockerTestCase):
    """tests the Entity class
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """seting up some proper values
        """
        # create a mock user
        self.mock_user = self.mocker.mock(user.User)
        
        # create some mock tag objects, not neccessarly needed but create them
        self.mock_tag1 = self.mocker.mock(tag.Tag)
        self.mock_tag2 = self.mocker.mock(tag.Tag)
        
        self.tags = [self.mock_tag1, self.mock_tag2]
        
        # now replay it
        self.mocker.replay()
        
        self.kwargs = {
            'name': 'Test Entity',
            'description': "This is a test entity, and this is a proper \
            description for it",
            'created_by': self.mock_user,
            'updated_by': self.mock_user,
            'tags': self.tags
        }
        
        # create a proper SimpleEntity to use it later in the tests
        self.entity = entity.Entity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tags_being_not_intialized(self):
        """testing if nothing is raised when creating an entity without setting
        a tags parameter
        """
        
        self.kwargs.pop('tags')
        # this should work without errors
        aNewEntity = entity.Entity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tags_being_initialized_as_an_empty_list(self):
        """testing if tags is initialized as an empty list
        """
        
        # this should work without errors
        self.kwargs.pop('tags')
        aNewEntity = entity.Entity(**self.kwargs)
        
        expected_result = []
        
        self.assertEquals(aNewEntity.tags, expected_result)
    
    
    
    #----------------------------------------------------------------------
    def test_tags_init_with_something_other_than_a_list(self):
        """testing if a ValueError is going to be raised when initializing the
        tags with something other than a list
        """
        
        test_values = [ "a tag", 1243, 12.12, {'a': 'tag'}]
        
        for test_value in test_values:
            self.kwargs['tags'] = test_value
            self.assertRaises(ValueError, entity.Entity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tags_property_set_properly(self):
        """testing if property is set correctly
        """
        test_value = [self.mock_tag1]
        
        self.entity.tags = test_value
        
        self.assertEquals(self.entity.tags, test_value)






########################################################################
class StatusedEntityTester(mocker.MockerTestCase):
    """tests the statused entity class
    
    these classes need to be mocked:
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
        
        # a mock note list
        
        self.mocker.replay()
        
        self.date_created = datetime.datetime(2010, 10, 21, 3, 8, 0)
        self.date_updated = self.date_created
        
        self.kwargs = {
            'name': 'Test Entity',
            'description': 'Just testing the very first entity',
            'tags': [self.mock_tag1, self.mock_tag2],
            'created_by': self.mock_user,
            'updated_by': self.mock_user,
            'status_list': self.mock_status_list,
            'status': 0,
            'date_created': self.date_created,
            'date_updated': self.date_updated,
        }
        
        # create a proper entity object
        self.statused_entity = entity.StatusedEntity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_init_with_something_else_then_StatusList_1(self):
        """testing if ValueError is going to be raised when trying to
        initialize status_list with something other than a StatusList
        """
        
        testValues = [100, '', 100.2]
        
        for testValue in testValues:
            self.kwargs['status_list'] = testValue
            self.assertRaises(ValueError, entity.StatusedEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_init_with_something_else_then_StatusList_2(self):
        """testing if ValueError is going to be raised when trying to
        initialize status_list with None
        """
        self.kwargs['status_list'] = None
        self.assertRaises(ValueError, entity.StatusedEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_property_set_to_something_other_than_StatusList(self):
        """testing if ValueError is going to be raised when trying to set the
        status_list to something else than a StatusList object
        """
        
        test_values = [ "a string", 1.0, 1, {'a': 'statusList'}]
        
        for test_value in test_values:
            # now try to set it
            self.assertRaises(
                ValueError,
                setattr,
                self.statused_entity,
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
            self.statused_entity,
            "status_list",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_argument_being_omited(self):
        """testing if a ValueError going to be raised when omiting the
        status_list argument
        """
        self.kwargs.pop('status_list')
        self.assertRaises(ValueError, entity.StatusedEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_argument_different_than_an_int(self):
        """testing if a ValueError is going to be raised if trying to
        initialize status with something else than an integer
        """
        
        # with a string
        test_values = ['0', [0]]
        
        for test_value in test_values:
            self.kwargs['status'] = test_value
            self.assertRaises(ValueError, entity.StatusedEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_property_set_to_other_than_int(self):
        """testing if ValueError going to be raised when trying to set the
        current status to something other than an integer
        """
        
        test_value = "a string"
        
        self.assertRaises(
            ValueError,
            setattr,
            self.statused_entity,
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
            self.statused_entity,
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
            self.statused_entity,
            "status",
            test_value
        )
    
    
    
    ##----------------------------------------------------------------------
    #def test_references_being_not_intialized(self):
        #"""testing if nothing is raised when creating an entity without setting
        # a references parameter
        #"""
        
        ## this should work without errors
        #aNewEntity = entity.StatusedEntity(
            #name=self.name,
            #created_by=self.mock_user,
            #updated_by=self.mock_user,
            #status_list= self.mock_status_list
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_references_being_initialized_as_an_empty_list(self):
        #"""testing if references is initialized as an empty list
        #"""
        
        ## this should work without errors
        #aNewEntity = entity.StatusedEntity(
            #name=self.name,
            #created_by=self.mock_user,
            #updated_by=self.mock_user,
            #status_list= self.mock_status_list
        #)
        
        #expected_result = []
        
        #self.assertEquals(aNewEntity.references, expected_result)
    
    
    
    ##----------------------------------------------------------------------
    #def test_references_init_with_something_other_than_a_list(self):
        #"""testing if a ValueError is going to be raised when initializing the
        #references with something other than a list
        #"""
        
        ##-----------------------
        ## a string
        #test_value = ""
        
        #self.assertRaises(
            #ValueError,
            #entity.StatusedEntity,
            #name=self.name,
            #created_by=self.mock_user,
            #updated_by=self.mock_user,
            #status_list=self.mock_status_list,
            #status=0,
            #references=test_value
        #)
        
        
        ##-----------------------
        ## an integer
        #test_value = 1231
        
        #self.assertRaises(
            #ValueError,
            #entity.StatusedEntity,
            #name=self.name,
            #created_by=self.mock_user,
            #updated_by=self.mock_user,
            #status_list=self.mock_status_list,
            #status=0,
            #references=test_value
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_references_property_being_set_to_something_else_than_a_list(self):
        #"""testing if a ValueError is going to be reaised when setting the list
        #property something other than a list
        #"""
        
        #test_value = "a string"
        
        #self.assertRaises(
            #ValueError,
            #setattr,
            #self.statused_entity,
            #"references",
            #test_value
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_references_property_set_properly(self):
        #"""testing if property is set correctly
        #"""
        
        #test_value = [self.mock_reference1]
        
        #self.statused_entity.references = test_value
        
        #self.assertEquals( self.statused_entity.references, test_value )
    
    
    
    ##----------------------------------------------------------------------
    #def test_notes_being_not_intialized(self):
        #"""testing if nothing is raised when creating an entity without setting
        #a notes parameter
        #"""
        
        ## this should work without errors
        #aNewEntity = entity.StatusedEntity(
            #name=self.name,
            #created_by=self.mock_user,
            #updated_by=self.mock_user,
            #status_list= self.mock_status_list
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_notes_being_initialized_as_an_empty_list(self):
        #"""testing if notes is initialized as an empty list
        #"""
        
        ## this should work without errors
        #aNewEntity = entity.StatusedEntity(
            #name=self.name,
            #created_by=self.mock_user,
            #updated_by=self.mock_user,
            #status_list= self.mock_status_list
        #)
        
        #expected_result = []
        
        #self.assertEquals(aNewEntity.notes, expected_result)
    
    
    
    ##----------------------------------------------------------------------
    #def test_notes_init_with_something_other_than_a_list(self):
        #"""testing if a ValueError is going to be raised when initializing the
        #notes with something other than a list
        #"""
        
        #test_values = [1, 12.3, "a string", {}]
        
        ##-----------------------
        ## a string
        #for test_value in test_values:
            #self.assertRaises(
                #ValueError,
                #entity.StatusedEntity,
                #name=self.name,
                #created_by=self.mock_user,
                #updated_by=self.mock_user,
                #status_list=self.mock_status_list,
                #status=0,
                #notes=test_value
            #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_notes_property_working_properly(self):
        #"""testing if notes property working properly
        #"""
        
        ## assign a new note object to the notes property and check if it is
        ## assigned correctly
        
        #self.fail("test not implemented yet!")
    
    
    