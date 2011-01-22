#-*- coding: utf-8 -*-



import unittest
import mocker
import datetime
from stalker.core.models import entity, user, link, note, tag, status




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
            "name": "Test Entity",
            "description": "This is a test entity, and this is a proper \
            description for it",
            "created_by": self.mock_user,
            "updated_by": self.mock_user,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }
        
        # create a proper SimpleEntity to use it later in the tests
        self.simple_entity = entity.SimpleEntity(**self.kwargs)
        
        
        
        # a couple of test values
        
        self.name_test_values = [
            ("testName", "testName"),
            ("test-Name", "test-Name"),
            ("1testName", "testName"),
            ("_testName", "testName"),
            ("2423$+^^+^'%+%%&_testName", "testName"),
            ("2423$+^^+^'%+%%&_testName_35", "testName_35"),
            ("2423$ +^^+^ '%+%%&_ testName_ 35", "testName_ 35"),
            ("SH001","SH001"),
            ([1,"name"], "name"),
            ({"a": "name"}, "a name"),
        ]
        
        
        self.nice_name_test_values = [
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
        
        
        self.code_test_values = [
            ("testCode","TEST_CODE"),
            ("1testCode", "TEST_CODE"),
            ("_testCode", "TEST_CODE"),
            ("2423$+^^+^'%+%%&_testCode", "TEST_CODE"),
            ("2423$+^^+^'%+%%&_testCode_35", "TEST_CODE_35"),
            ("2423$ +^^+^ '%+%%&_ testCode_ 35", "TEST_CODE_35"),
            ("SH001","SH001"),
            ("My CODE is Ozgur", "MY_CODE_IS_OZGUR"),
            
            (" this is another code for an asset", 
             "THIS_IS_ANOTHER_CODE_FOR_AN_ASSET"),
            
            ([1, 3, "a", "list","for","testing",3],
             "A_LIST_FOR_TESTING_3"),
        ]
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_skipped(self):
        """testing if a value will be set if code argument is skipped
        """
        
        #code = None
        #name = "something"
        # code value ?
        
        # be sure that we don't have code keyword
        if self.kwargs.has_key("code"):
            self.kwargs.pop("code")
        
        new_simple_entity = entity.SimpleEntity(**self.kwargs)
        
        # check if it is not None and not an empty string and is an instance of
        # string or unicode
        self.assertTrue(new_simple_entity.code is not None)
        self.assertTrue(new_simple_entity.code != "")
        self.assertTrue(isinstance(new_simple_entity.code, (str, unicode)))
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_None(self):
        """testing if a value will be set if code argument is set to None
        """
        
        self.kwargs["code"] = None
        
        new_simple_entity = entity.SimpleEntity(**self.kwargs)
        
        self.assertTrue(new_simple_entity.code is not None)
        self.assertTrue(new_simple_entity.code != "")
        self.assertTrue(isinstance(new_simple_entity.code, (str, unicode)))
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_empty_string(self):
        """testing if a value will be set if code argument is set to an empty
        string
        """
        
        self.kwargs["code"] = ""
        
        new_simple_entity = entity.SimpleEntity(**self.kwargs)
        
        self.assertTrue(new_simple_entity.code is not None)
        self.assertTrue(new_simple_entity.code != "")
        self.assertTrue(isinstance(new_simple_entity.code, (str, unicode)))
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_format_when_code_argument_skipped(self):
        """testing if code property is formatted correctly when skipped as an
        argument
        """
        
        #code = None or ""
        #name = "something"
        # code format ?
        
        # set the name and check the code
        for test_value in self.code_test_values:
            self.kwargs["name"] = test_value[0]
            new_entity = entity.SimpleEntity(**self.kwargs)
            
            self.assertEquals(new_entity.code, test_value[1])
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_is_set_when_both_code_and_name_is_given(self):
        """testing if both code argument and name argument is given then it is
        just set to the formatted version of code
        """
        
        # set the name and code and test the code
        for test_value in self.code_test_values:
            self.kwargs["name"] = "aName"
            self.kwargs["code"] = test_value[0]
            
            new_entity = entity.SimpleEntity(**self.kwargs)
            
            self.assertEquals(new_entity.code, test_value[1])
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_is_changed_after_setting_name(self):
        """testing if code was 
        """
        
        code = "something"
        name = "some name"
        new_name = "something new"
        expected_new_code = "SOMETHING_NEW"
        
        self.kwargs["code"] = code
        self.kwargs["name"] = name
        
        new_simple_entity = entity.SimpleEntity(**self.kwargs)
        
        old_code = new_simple_entity.code
        
        # set the new name
        new_simple_entity.name = new_name
        
        # first check if it is different then the old_code
        self.assertNotEquals(new_simple_entity.code, old_code)
        
        # then check if it is set to the expected result
        self.assertEquals(new_simple_entity.code, expected_new_code)
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_set_to_empty_string(self):
        """testing if a ValueError will be raised when trying to set the code
        property to an empty string
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            "code",
            ""
        )
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_set_to_None(self):
        """testing if a ValueError will be raised when trying to set the code
        property to None
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            "code",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_being_empty(self):
        """testing if ValueError is raised for empty name argument
        """
        
        self.kwargs["name"] = ""
        self.assertRaises(ValueError, entity.SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_init_as_None(self):
        """testing if ValueError is raised for None name argument
        """
        
        self.kwargs["name"] = None
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
    def test_name_argument_not_init_as_string_or_unicode(self):
        """testing if a the name property is going to be formatted correctly
        when the given value for the name argument isn't a str or unicode
        """
        
        test_values = [
            ([1,"name"], "name"),
            ({"a": "name"}, "a name")
        ]
        
        for test_value in test_values:
            self.kwargs["name"] = test_value[0]
            a_new_simple_entity = entity.SimpleEntity(**self.kwargs)
            self.assertEquals(a_new_simple_entity.name, test_value[1])
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_not_init_as_string_or_unicode_2(self):
        """testing if a ValueError will be raised when the result of conversion
        is an empty string for the name argument
        """
        
        test_values = [1, 1.2, [1, 2]]
        
        for test_value in test_values:
            self.kwargs["name"] = test_value
            self.assertRaises(ValueError, entity.SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_name_property_is_formated_correctly(self):
        """testing if name is formated correctly
        """
        
        for test_value in self.name_test_values:
            # set the new name
            self.simple_entity.name = test_value[0]
            
            self.assertEquals(
                self.simple_entity.name,
                test_value[1],
                "the name property is not correctly formatted for, %s, %s" % \
                    (str(test_value[0]), test_value[1])
            )
    
    
    
    #----------------------------------------------------------------------
    def test_nice_name_property_is_formatted_correctly(self):
        """testing if nice name property is formatted correctly
        """
        
        for test_value in self.nice_name_test_values:
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
    def test_description_argument_None(self):
        """testing if description proeprty will be convertod to an empty string
        if None is given as the description argument
        """
        
        self.kwargs["description"] = None
        new_simple_entity = entity.SimpleEntity(**self.kwargs)
        
        self.assertEquals(new_simple_entity.description, "")
    
    
    
    #----------------------------------------------------------------------
    def test_description_property_None(self):
        """testing if description property will be converted to an empty string
        if None is given as the description property
        """
        
        self.simple_entity.description = None
        self.assertEquals(self.simple_entity.description, "")
    
    
    
    #----------------------------------------------------------------------
    def test_description_argument_string_conversion(self):
        """testing if description argument will be converted to string
        correctly
        """
        
        test_values = [["a description"], {"a": "description"}]
        
        for test_value in test_values:
            self.kwargs["description"] = test_value
            new_simple_entity = entity.SimpleEntity(**self.kwargs)
            
            self.assertIsInstance(new_simple_entity.description,
                                  (str, unicode))
    
    
    
    #----------------------------------------------------------------------
    def test_description_property_string_conversion(self):
        """testing if description property will be converted to string
        correctly
        """
        
        test_values = [["a description"], {"a": "description"}]
        
        for test_value in test_values:
            self.simple_entity.description = test_value
            self.assertIsInstance(self.simple_entity.description,
                                  (str, unicode))
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing the equality of two simple entities
        """
        
        # create two simple entities with same parameters and check for
        # equality
        simpleEntity1 = entity.SimpleEntity(**self.kwargs)
        simpleEntity2 = entity.SimpleEntity(**self.kwargs)
        
        self.kwargs["name"] = "a different simple entity"
        self.kwargs["description"] = "no description"
        simpleEntity3 = entity.SimpleEntity(**self.kwargs)
        self.assertTrue(simpleEntity1==simpleEntity2)
        self.assertFalse(simpleEntity1==simpleEntity3)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing the inequality of two simple entites
        """
        
        # create two simple entities with same parameters and check for
        # equality
        simpleEntity1 = entity.SimpleEntity(**self.kwargs)
        simpleEntity2 = entity.SimpleEntity(**self.kwargs)
        
        self.kwargs["name"] = "a different simple entity"
        self.kwargs["description"] = "no description"
        simpleEntity3 = entity.SimpleEntity(**self.kwargs)
        
        self.assertFalse(simpleEntity1!=simpleEntity2)
        self.assertTrue(simpleEntity1!=simpleEntity3)
    
    
    
    #----------------------------------------------------------------------
    def test_created_by_argument_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.core.models.user.User object to created_by argument
        """
        # the created_by argument should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = "A User Name"
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse( isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            "created_by",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_created_by_property_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.modles.User object to created_by **property**
        """
        # the created_by property should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = "A User Name"
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse( isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            "created_by",
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
            #"created_by",
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
            #"created_by",
            #None
        #)
    
    
    
    #----------------------------------------------------------------------
    def test_updated_by_argument_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.modles.User object to updated_by argument
        """
        # the updated_by argument should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = "A User Name"
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse(isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            "updated_by",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_updated_by_property_instance_of_User(self):
        """testing if ValueError is raised when assigned anything other than a
        stalker.modles.User object to update_by **property**
        """
        # the updated_by property should be an instance of User class, in any
        # other case it should raise a ValueError
        test_value = "A User Name"
        
        # be sure that the test value is not an instance of user.User
        self.assertFalse( isinstance(test_value, user.User))
        
        # check the value
        self.assertRaises(
            ValueError,
            setattr,
            self.simple_entity,
            "updated_by",
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
            #"updated_by",
            #None
        #)
        
        self.kwargs["updated_by"] = None
        
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
            #"created_by",
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
        
        
        self.kwargs["date_created"] = datetime.datetime(2000, 1, 1, 1, 1, 1)
        self.kwargs["date_updated"] = datetime.datetime(1990, 1, 1, 1, 1, 1)
        
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
        
        # create some mock Tag objects, not neccessarly needed but create them
        self.mock_tag1 = self.mocker.mock(tag.Tag)
        self.mock_tag2 = self.mocker.mock(tag.Tag)
        self.mock_tag3 = self.mocker.mock(tag.Tag)
        
        self.expect(self.mock_tag1.__eq__(self.mock_tag2))\
            .result(True).count(0, None)
        
        self.expect(self.mock_tag1.__ne__(self.mock_tag2))\
            .result(False).count(0, None)
        
        
        
        self.expect(self.mock_tag1.__eq__(self.mock_tag3))\
            .result(False).count(0, None)
        
        self.expect(self.mock_tag1.__ne__(self.mock_tag3))\
            .result(True).count(0, None)
        
        self.tags = [self.mock_tag1, self.mock_tag2]
        
        # create a couple of mock Note objects
        self.mock_note1 = self.mocker.mock(note.Note)
        self.mock_note2 = self.mocker.mock(note.Note)
        self.mock_note3 = self.mocker.mock(note.Note)
        
        self.notes = [self.mock_note1, self.mock_note2]
        
        # now replay it
        self.mocker.replay()
        
        self.kwargs = {
            "name": "Test Entity",
            "description": "This is a test entity, and this is a proper \
            description for it",
            "created_by": self.mock_user,
            "updated_by": self.mock_user,
            "tags": self.tags,
            "notes": self.notes,
        }
        
        # create a proper SimpleEntity to use it later in the tests
        self.mock_entity = entity.Entity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_notes_argument_being_omited(self):
        """testing if no error raised when omited the notes argument
        """
        
        self.kwargs.pop("notes")
        new_entity = entity.Entity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_notes_argument_is_set_to_None(self):
        """testing if a ValueError will be raised when setting the notes
        argument to None
        """
        
        self.kwargs["notes"] = None
        self.assertRaises(ValueError, entity.Entity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_notes_property_is_set_to_None(self):
        """testing if a ValueError will be raised when setting the notes
        property to None
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_entity,
            "notes",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_notes_argument_set_to_something_other_than_a_list(self):
        """testing if a ValueError will be raised when setting the notes
        argument something other than a list
        """
        
        test_values = [1, 1.2, "a string note"]
        
        for test_value in test_values:
            self.kwargs["notes"] = test_value
            self.assertRaises(ValueError, entity.Entity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_notes_property_set_to_something_other_than_a_list(self):
        """testing if a ValueError will be raised when setting the notes
        argument something other than a list
        """
        
        test_values = [1, 1.2, "a string note"]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_entity,
                "notes",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_notes_argument_set_to_a_list_of_other_objects(self):
        """testing if a ValueError will be raised when trying to set the notes
        argument to a list of other kind of objects than Note objects
        """
        
        self.kwargs["notes"] = [1, 12.2, "this is a string",
                                ["a list"], {"a": "note"}]
        
        self.assertRaises(ValueError, entity.Entity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_notes_property_set_to_a_list_of_other_objects(self):
        """testing if a ValueError will be raised when trying to set the notes
        property to a list of other kind of objects than Note objects
        """
        
        test_value = [1, 12.2, "this is a string", ["a list"], {"a": "note"}]
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_entity,
            "notes",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_notes_property_works_properly(self):
        """testing if the notes property works properly
        """
        
        test_value = [self.mock_note3]
        self.mock_entity.notes = test_value
        self.assertEquals(self.mock_entity.notes, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_tags_argument_being_omited(self):
        """testing if nothing is raised when creating an entity without setting
        a tags argument
        """
        
        self.kwargs.pop("tags")
        # this should work without errors
        aNewEntity = entity.Entity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tags_argument_being_initialized_as_an_empty_list(self):
        """testing if nothing happends when tags argument an empty list
        """
        
        # this should work without errors
        self.kwargs.pop("tags")
        aNewEntity = entity.Entity(**self.kwargs)
        
        expected_result = []
        
        self.assertEquals(aNewEntity.tags, expected_result)
    
    
    
    #----------------------------------------------------------------------
    def test_tags_argument_set_to_something_other_than_a_list(self):
        """testing if a ValueError is going to be raised when initializing the
        tags with something other than a list
        """
        
        test_values = [ "a tag", 1243, 12.12, {"a": "tag"}]
        
        for test_value in test_values:
            self.kwargs["tags"] = test_value
            self.assertRaises(ValueError, entity.Entity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tags_property_works_properly(self):
        """testing if tags property works properly
        """
        test_value = [self.mock_tag1]
        
        self.mock_entity.tags = test_value
        
        self.assertEquals(self.mock_entity.tags, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing equality of two entities
        """
        
        # create two entities with same parameters and check for equality
        entity1 = entity.Entity(**self.kwargs)
        entity2 = entity.Entity(**self.kwargs)
        
        self.kwargs["name"] = "another entity"
        self.kwargs["tags"] = [self.mock_tag3]
        self.kwargs["notes"] = []
        entity3 = entity.Entity(**self.kwargs)
        
        self.assertTrue(entity1==entity2)
        self.assertFalse(entity1==entity3)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing inequality of two entities
        """
        
        # change the tags and test it again, expect False
        entity1 = entity.Entity(**self.kwargs)
        entity2 = entity.Entity(**self.kwargs)
        
        self.kwargs["name"] = "another entity"
        self.kwargs["tags"] = [self.mock_tag3]
        self.kwargs["notes"] = []
        entity3 = entity.Entity(**self.kwargs)
        
        self.assertFalse(entity1!=entity2)
        self.assertTrue(entity1!=entity3)





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
        
        self.expect = mocker.Expect(self.mocker)
        
        # a mock StatusList object
        self.mock_status_list1 = self.mocker.mock(status.StatusList)
        self.expect(len(self.mock_status_list1.statuses)).result(5).\
            count(0, None)
        
        self.expect(self.mock_status_list1.target_entity_type).\
            result("StatusedEntity").count(0, None)
        
        # another mock StatusList object
        self.mock_status_list2 = self.mocker.mock(status.StatusList)
        self.expect(len(self.mock_status_list2.statuses)).result(5)\
            .count(0, None)
        
        self.expect(self.mock_status_list2.target_entity_type).\
            result("StatusedEntity").count(0, None)
        
        self.mock_status_list1.__eq__(self.mock_status_list2)
        self.mocker.result(False)
        self.mocker.count(0, None)
        
        self.mock_status_list1.__ne__(self.mock_status_list2)
        self.mocker.result(True)
        self.mocker.count(0, None)
        
        self.mocker.replay()
        
        
        
        self.kwargs = {
            "name": "Test Entity",
            "description": "Just testing the very first entity",
            "status_list": self.mock_status_list1,
            "status": 0,
        }
        
        # create a proper entity object
        self.statused_entity = entity.StatusedEntity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_init_with_something_else_then_StatusList_1(self):
        """testing if ValueError is going to be raised when trying to
        initialize status_list with something other than a StatusList
        """
        
        testValues = [100, "", 100.2]
        
        for testValue in testValues:
            self.kwargs["status_list"] = testValue
            self.assertRaises(ValueError, entity.StatusedEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_init_with_something_else_then_StatusList_2(self):
        """testing if ValueError is going to be raised when trying to
        initialize status_list with None
        """
        self.kwargs["status_list"] = None
        self.assertRaises(ValueError, entity.StatusedEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_property_set_to_something_other_than_StatusList(self):
        """testing if ValueError is going to be raised when trying to set the
        status_list to something else than a StatusList object
        """
        
        test_values = [ "a string", 1.0, 1, {"a": "statusList"}]
        
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
        self.kwargs.pop("status_list")
        self.assertRaises(ValueError, entity.StatusedEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_argument_suitable_for_the_current_class(self):
        """testing if a TypeError will be raised when the
        Status.target_entity_class is not compatible with the current
        StatusedEntity
        """
        
        # create a new status list suitable for another class with different
        # entity_type
        
        
        new_status_list = status.StatusList(
            name="Sequence Statuses",
            statuses=[
                status.Status(name="On Hold", code="OH"),
                status.Status(name="Complete", code="CMPLT"),
            ],
            target_entity_type="Sequence"
        )
        
        self.assertRaises(
            TypeError,
            setattr,
            self.statused_entity,
            "status_list",
            new_status_list
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_argument_set_to_None(self):
        """testing if a ValueError will be raised when setting the status
        argument to None
        """
        self.kwargs["status"] = None
        self.assertRaises(ValueError, entity.StatusedEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_property_set_to_None(self):
        """testing if a ValueError will be raised when setting the status
        property to None
        """
        self.assertRaises(
            ValueError,
            setattr,
            self.statused_entity,
            "status",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_status_argument_different_than_an_int(self):
        """testing if a ValueError is going to be raised if trying to
        initialize status with something else than an integer
        """
        
        # with a string
        test_values = ["0", 1.2, [0]]
        
        for test_value in test_values:
            self.kwargs["status"] = test_value
            self.assertRaises(ValueError, entity.StatusedEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_property_set_to_other_than_int(self):
        """testing if ValueError going to be raised when trying to set the
        current status to something other than an integer
        """
        
        test_values = ["a string", 1.2, [1], {"a": "status"}]
        
        for test_value in test_values:
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
        
        test_value = len(self.mock_status_list1.statuses)
        
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
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing equality
        """
        
        statusedEntity1 = entity.StatusedEntity(**self.kwargs)
        statusedEntity2 = entity.StatusedEntity(**self.kwargs)
        
        entity1 = entity.Entity(**self.kwargs)
        
        self.kwargs["name"] = "A different Statused Entity"
        statusedEntity3 = entity.StatusedEntity(**self.kwargs)
        
        self.assertTrue(statusedEntity1==statusedEntity2)
        self.assertFalse(statusedEntity1==statusedEntity3)
        self.assertFalse(statusedEntity1==entity1)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing inequality
        """
        
        statusedEntity1 = entity.StatusedEntity(**self.kwargs)
        statusedEntity2 = entity.StatusedEntity(**self.kwargs)
        
        entity1 = entity.Entity(**self.kwargs)
        
        self.kwargs["name"] = "A different Statused Entity"
        statusedEntity3 = entity.StatusedEntity(**self.kwargs)
        
        self.assertFalse(statusedEntity1!=statusedEntity2)
        self.assertTrue(statusedEntity1!=statusedEntity3)
        self.assertTrue(statusedEntity1!=entity1)







########################################################################
class TypeEntityTester(mocker.MockerTestCase):
    """tests the TypeEntity class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """set up the test
        """
        
        self.kwargs = {
            "name": "mock type entity",
            "description": "this is a mock type entity"
        }
        
        self.mock_typeEntity = entity.TypeEntity(**self.kwargs)
        
        # create another entity.Entity with the same name of the
        # mock_typeEntity for __eq__ and __ne__ tests
        self.entity1 = entity.Entity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing the equality operator
        """
        
        new_typeEntity2 = entity.TypeEntity(**self.kwargs)
        
        self.kwargs["name"] = "a different typeEntity"
        self.kwargs["description"] = "this is a different typeEntity"
        new_typeEntity3 = entity.TypeEntity(**self.kwargs)
        
        self.assertTrue(self.mock_typeEntity==new_typeEntity2)
        self.assertFalse(self.mock_typeEntity==new_typeEntity3)
        self.assertFalse(self.mock_typeEntity==self.entity1)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing the inequality operator
        """
        
        new_typeEntity2 = entity.TypeEntity(**self.kwargs)
        
        self.kwargs["name"] = "a different typeEntity"
        self.kwargs["description"] = "this is a different typeEntity"
        new_typeEntity3 = entity.TypeEntity(**self.kwargs)
        
        self.assertFalse(self.mock_typeEntity!=new_typeEntity2)
        self.assertTrue(self.mock_typeEntity!=new_typeEntity3)
        self.assertTrue(self.mock_typeEntity!=self.entity1)
    
    
    