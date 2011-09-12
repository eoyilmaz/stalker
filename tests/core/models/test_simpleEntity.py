#-*- coding: utf-8 -*-



import unittest
import datetime
import stalker
from stalker.core.models import (SimpleEntity, Type, User)




# create a new class deriving from the SimpleEntity
class newClass(SimpleEntity):
    __strictly_typed__ = True





########################################################################
class SimpleEntityTester(unittest.TestCase):
    """testing the SimpleEntity class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """seting up some proper values
        """
        # create a user
        self.test_user = User(
            first_name="Test",
            last_name="User",
            login_name="testuser",
            email="test@user.com",
            password="test"
        )
        
        self.date_created = datetime.datetime(2010, 10, 21, 3, 8, 0)
        self.date_updated = self.date_created
        
        self.kwargs = {
            "name": "Test Entity",
            "code": "TstEnt",
            "description": "This is a test entity, and this is a proper \
            description for it",
            "created_by": self.test_user,
            "updated_by": self.test_user,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }
        
        # create a proper SimpleEntity to use it later in the tests
        self.test_simple_entity = SimpleEntity(**self.kwargs)
        
        self.test_type = Type(
            name="Test Type",
            target_entity_type=SimpleEntity
        )
        
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
        
        
        #self.code_test_values = [
            #("testCode","TEST_CODE"),
            #("1testCode", "TEST_CODE"),
            #("_testCode", "TEST_CODE"),
            #("2423$+^^+^'%+%%&_testCode", "TEST_CODE"),
            #("2423$+^^+^'%+%%&_testCode_35", "TEST_CODE_35"),
            #("2423$ +^^+^ '%+%%&_ testCode_ 35", "TEST_CODE_35"),
            #("SH001","SH001"),
            #("My CODE is Ozgur", "MY_CODE_IS_OZGUR"),
            
            #(" this is another code for an asset", 
             #"THIS_IS_ANOTHER_CODE_FOR_AN_ASSET"),
            
            #([1, 3, "a", "list","for","testing",3],
             #"A_LIST_FOR_TESTING_3"),
        #]
    
    
    
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
        
        new_simple_entity = SimpleEntity(**self.kwargs)
        
        # check if it is not None and not an empty string and is an instance of
        # string or unicode
        self.assertTrue(new_simple_entity.code is not None)
        self.assertTrue(new_simple_entity.code != "")
        self.assertIsInstance(new_simple_entity.code, (str, unicode))
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_None(self):
        """testing if a value will be set if code argument is set to None
        """
        
        self.kwargs["code"] = None
        
        new_simple_entity = SimpleEntity(**self.kwargs)
        
        self.assertTrue(new_simple_entity.code is not None)
        self.assertTrue(new_simple_entity.code != "")
        self.assertIsInstance(new_simple_entity.code, (str, unicode))
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_empty_string(self):
        """testing if a value will be set if code argument is set to an empty
        string
        """
        
        self.kwargs["code"] = ""
        
        new_simple_entity = SimpleEntity(**self.kwargs)
        
        self.assertTrue(new_simple_entity.code is not None)
        self.assertTrue(new_simple_entity.code != "")
        self.assertIsInstance(new_simple_entity.code, (str, unicode))
    
    
    
    #----------------------------------------------------------------------
    def test_code_attribute_format_when_code_argument_skipped(self):
        """testing if code attribute is formatted correctly when skipped as an
        argument
        """
        
        #code = None or ""
        #name = "something"
        # code format ?
        
        # set the name and check the code
        code_test_values = [
            ("testCode","testCode"),
            ("1testCode", "testCode"),
            ("_testCode", "testCode"),
            ("2423$+^^+^'%+%%&_testCode", "testCode"),
            ("2423$+^^+^'%+%%&_testCode_35", "testCode_35"),
            ("2423$ +^^+^ '%+%%&_ testCode_ 35", "testCode_35"),
            ("SH001","SH001"),
            ("My CODE is Ozgur", "My_CODE_is_Ozgur"),
            
            (" this is another code for an asset", 
             "this_is_another_code_for_an_asset"),
            
            ([1, 3, "a", "list","for","testing",3],
             "a_list_for_testing_3"),
        ]
        
        self.kwargs.pop("code")
        
        for test_value in code_test_values:
            self.kwargs["name"] = test_value[0]
            new_entity = SimpleEntity(**self.kwargs)
            
            self.assertEqual(new_entity.code, test_value[1])
    
    
    
    #----------------------------------------------------------------------
    def test_code_attribute_is_set_when_both_code_and_name_is_given(self):
        """testing if both code argument and name argument is given then it is
        just set to the formatted version of code
        """
        
        code_test_values = [
            ("testCode","testCode"),
            ("1testCode", "testCode"),
            ("_testCode", "testCode"),
            ("2423$+^^+^'%+%%&_testCode", "testCode"),
            ("2423$+^^+^'%+%%&_testCode_35", "testCode_35"),
            ("2423$ +^^+^ '%+%%&_ testCode_ 35", "testCode_35"),
            ("SH001","SH001"),
            ("My CODE is Ozgur", "My_CODE_is_Ozgur"),
            
            (" this is another code for an asset", 
             "this_is_another_code_for_an_asset"),
            
            ([1, 3, "a", "list","for","testing",3],
             "a_list_for_testing_3"),
        ]
        
        # set the name and code and test the code
        for test_value in code_test_values:
            self.kwargs["name"] = "aName"
            self.kwargs["code"] = test_value[0]
            
            new_entity = SimpleEntity(**self.kwargs)
            
            self.assertEqual(new_entity.code, test_value[1])
    
    
    
    #----------------------------------------------------------------------
    def test_code_attribute_is_not_changed_after_setting_name(self):
        """testing if code attribute is not changed and reformatted after the
        name attribute has changed
        """
        
        # create a SimpleEntity with code and name has values in it
        code = "something"
        name = "some name"
        new_name = "something new"
        expected_new_code = "something"
        
        self.kwargs["code"] = code
        self.kwargs["name"] = name
        
        new_simple_entity = SimpleEntity(**self.kwargs)
        
        # store the old code
        old_code = new_simple_entity.code
        
        # set the new name
        new_simple_entity.name = new_name
        
        # first check if it is not different then the old_code
        self.assertEquals(new_simple_entity.code, old_code)
        
        # then check if it is set to the expected result
        self.assertEqual(new_simple_entity.code, expected_new_code)
    
    
    
    #----------------------------------------------------------------------
    def test_code_attribute_set_to_empty_string(self):
        """testing if the code attribute will be restored from the nice_name
        attribute when it is set to an empty string
        """
        
        self.test_simple_entity.code = ""
        self.assertEqual(self.test_simple_entity.code, "test_entity")
    
    
    
    #----------------------------------------------------------------------
    def test_code_attribute_set_to_None(self):
        """testing if the code is evauluated from the nice_name attribute when
        set to None.
        """
        
        self.test_simple_entity.code = None
        self.assertEqual(self.test_simple_entity.code, "test_entity")
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_init_as_None_and_also_the_code_is_None(self):
        """testing if ValueError is raised for None name argument
        """
        
        self.kwargs["name"] = None
        self.kwargs["code"] = None
        self.assertRaises(ValueError, SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_init_as_None_and_also_the_code_is_empty_string(self):
        """testing if TypeError is raised for None name argument
        """
        
        self.kwargs["name"] = None
        self.kwargs["code"] = ""
        self.assertRaises(ValueError, SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_init_as_empty_string_and_also_the_code_is_None(self):
        """testing if ValueError is raised for None name argument
        """
        
        self.kwargs["name"] = ""
        self.kwargs["code"] = None
        self.assertRaises(ValueError, SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_init_as_empty_string_and_also_the_code_is_empty_string(self):
        """testing if TypeError is raised for None name argument
        """
        
        self.kwargs["name"] = ""
        self.kwargs["code"] = ""
        self.assertRaises(ValueError, SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_is_None_but_there_is_code_argument(self):
        """testing if the name attribute will be calculated from the code
        arugment if the name argument is given as none
        """
        
        self.kwargs["name"] = None
        self.assertIsNot(self.kwargs["code"], None)
        
        new_simpleEntity = SimpleEntity(**self.kwargs)
        self.assertEquals(new_simpleEntity.name, new_simpleEntity.code)
    
    
    
    #----------------------------------------------------------------------
    def test_name_attribute_for_being_empty(self):
        """testing if ValueError is raised when trying to set the name to an
        empty string
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.test_simple_entity,
            "name",
            ""
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_attribute_for_being_None(self):
        """testing if TypeError is raised when trying to set the name to None
        """
        
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "name",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_not_init_as_string_or_unicode(self):
        """testing if a the name attribute is going to be formatted correctly
        when the given value for the name argument isn't a str or unicode
        """
        
        test_values = [
            ([1,"name"], "name"),
            ({"a": "name"}, "a name")
        ]
        
        for test_value in test_values:
            self.kwargs["name"] = test_value[0]
            a_new_simple_entity = SimpleEntity(**self.kwargs)
            self.assertEqual(a_new_simple_entity.name, test_value[1])
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_not_init_as_string_or_unicode_2(self):
        """testing if a ValueError will be raised when the result of conversion
        is an empty string for the name argument
        """
        
        test_values = [1, 1.2, [1, 2]]
        
        for test_value in test_values:
            self.kwargs["name"] = test_value
            self.assertRaises(ValueError, SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_name_attribute_is_formated_correctly(self):
        """testing if name is formated correctly
        """
        
        for test_value in self.name_test_values:
            # set the new name
            self.test_simple_entity.name = test_value[0]
            
            self.assertEqual(
                self.test_simple_entity.name,
                test_value[1],
                "the name attribute is not correctly formatted for, %s, %s" % \
                    (str(test_value[0]), test_value[1])
            )
    
    
    
    #----------------------------------------------------------------------
    def test_nice_name_attribute_is_formatted_correctly(self):
        """testing if nice name attribute is formatted correctly
        """
        
        for test_value in self.nice_name_test_values:
            self.test_simple_entity.name = test_value[0]
            
            self.assertEqual(
                self.test_simple_entity.nice_name,
                test_value[1],
                "the nice name attribute is not correctly formatted for, " + \
                    test_value[0] + ", " + test_value[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_nice_name_attribute_is_read_only(self):
        """testing if nice name attribute is read-only
        """
        
        self.assertRaises(
            AttributeError,
            setattr,
            self.test_simple_entity,
            "nice_name",
            "a text"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_description_argument_None(self):
        """testing if description proeprty will be convertod to an empty string
        if None is given as the description argument
        """
        
        self.kwargs["description"] = None
        new_simple_entity = SimpleEntity(**self.kwargs)
        
        self.assertEqual(new_simple_entity.description, "")
    
    
    
    #----------------------------------------------------------------------
    def test_description_attribute_None(self):
        """testing if description attribute will be converted to an empty
        string if None is given as the description attribute
        """
        
        self.test_simple_entity.description = None
        self.assertEqual(self.test_simple_entity.description, "")
    
    
    
    #----------------------------------------------------------------------
    def test_description_argument_string_conversion(self):
        """testing if description argument will be converted to string
        correctly
        """
        
        test_values = [["a description"], {"a": "description"}]
        
        for test_value in test_values:
            self.kwargs["description"] = test_value
            new_simple_entity = SimpleEntity(**self.kwargs)
            
            self.assertIsInstance(new_simple_entity.description,
                                  (str, unicode))
    
    
    
    #----------------------------------------------------------------------
    def test_description_attribute_string_conversion(self):
        """testing if description attribute will be converted to string
        correctly
        """
        
        test_values = [["a description"], {"a": "description"}]
        
        for test_value in test_values:
            self.test_simple_entity.description = test_value
            self.assertIsInstance(self.test_simple_entity.description,
                                  (str, unicode))
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing the equality of two simple entities
        """
        
        # create two simple entities with same parameters and check for
        # equality
        simpleEntity1 = SimpleEntity(**self.kwargs)
        simpleEntity2 = SimpleEntity(**self.kwargs)
        
        self.kwargs["name"] = "a different simple entity"
        self.kwargs["description"] = "no description"
        simpleEntity3 = SimpleEntity(**self.kwargs)
        self.assertTrue(simpleEntity1==simpleEntity2)
        self.assertFalse(simpleEntity1==simpleEntity3)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing the inequality of two simple entites
        """
        
        # create two simple entities with same parameters and check for
        # equality
        simpleEntity1 = SimpleEntity(**self.kwargs)
        simpleEntity2 = SimpleEntity(**self.kwargs)
        
        self.kwargs["name"] = "a different simple entity"
        self.kwargs["description"] = "no description"
        simpleEntity3 = SimpleEntity(**self.kwargs)
        
        self.assertFalse(simpleEntity1!=simpleEntity2)
        self.assertTrue(simpleEntity1!=simpleEntity3)
    
    
    
    #----------------------------------------------------------------------
    def test_created_by_argument_instance_of_User(self):
        """testing if TypeError is raised when assigned anything other than a
        stalker.core.models.User object to created_by argument
        """
        # the created_by argument should be an instance of User class, in any
        # other case it should raise a TypeError
        test_value = "A User Name"
        
        # be sure that the test value is not an instance of User
        self.assertFalse(isinstance(test_value, User))
        
        # check the value
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "created_by",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_created_by_attribute_instance_of_User(self):
        """testing if TypeError is raised when assigned anything other than a
        stalker.modles.User object to created_by attribute
        """
        # the created_by attribute should be an instance of User class, in any
        # other case it should raise a TypeError
        test_value = "A User Name"
        
        # be sure that the test value is not an instance of User
        self.assertFalse(isinstance(test_value, User))
        
        # check the value
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "created_by",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_updated_by_argument_instance_of_User(self):
        """testing if TypeError is raised when assigned anything other than a
        stalker.modles.User object to updated_by argument
        """
        # the updated_by argument should be an instance of User class, in any
        # other case it should raise a TypeError
        test_value = "A User Name"
        
        # be sure that the test value is not an instance of User
        self.assertFalse(isinstance(test_value, User))
        
        # check the value
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "updated_by",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_updated_by_attribute_instance_of_User(self):
        """testing if TypeError is raised when assigned anything other than a
        stalker.modles.User object to update_by attribute
        """
        # the updated_by attribute should be an instance of User class, in any
        # other case it should raise a TypeError
        test_value = "A User Name"
        
        # be sure that the test value is not an instance of User
        self.assertFalse(isinstance(test_value, User))
        
        # check the value
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "updated_by",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_updated_by_argument_empty(self):
        """testing if initializing updated_by with None causes it to be set to
        the same value with created_by argument
        """
        
        self.kwargs["updated_by"] = None
        
        aNewSimpleEntity = SimpleEntity(**self.kwargs)
        
        # now check if they are same
        self.assertEqual(aNewSimpleEntity.created_by,
                          aNewSimpleEntity.updated_by)
    
    
    
    #----------------------------------------------------------------------
    def test_date_created_argument_accepts_datetime_only(self):
        """testing if TypeError raises when the date_created argument is set
        to something else than a datetime.datetime object
        """
        
        # the date_created argument should be an instance of datetime.datetime
        
        # try to set something else and expect a TypeError
        
        test_value = "a string date time 2010-10-26 etc."
        
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse( isinstance(test_value, datetime.datetime) )
        
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_created",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_created_attribute_accepts_datetime_only(self):
        """testing if TypeError raises when the date_created attribute is set
        to something else than a datetime.datetime object
        """
        
        # the date_created attribute should be an instance of datetime.datetime
        
        # try to set something else and expect a TypeError
        
        test_value = "a string date time 2010-10-26 etc."
        
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse( isinstance(test_value, datetime.datetime) )
        
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_created",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_created_attribute_being_empty(self):
        """testing if TypeError is raised when the date_created attribute is
        set to None
        """
        
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_created",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_updated_argument_accepts_datetime_only(self):
        """testing if TypeError raises when the date_updated argument is set
        to something else than a datetime.datetime object
        """
        
        # try to set it to something else and expect a TypeError
        test_value = "a string date time 2010-10-26 etc."
        
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse( isinstance(test_value, datetime.datetime) )
        
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_updated",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_updated_attribute_being_datetime(self):
        """testing if TypeError raises when the date_updated attribute is set
        to something else than a datetime.datetime object
        """
        
        # try to set something else and expect a TypeError
        test_value = "a string date time 2010-10-26 etc."
        
        # be sure that the test_value is not an instance of datetime.datetime
        self.assertFalse(isinstance(test_value, datetime.datetime) )
        
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_updated",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_updated_attribute_is_set_to_None(self):
        """testing if TypeError is raised when the date_updated attribute is
        set to None
        """
        
        self.assertRaises(
            TypeError,
            setattr,
            self.test_simple_entity,
            "date_updated",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_date_updated_attribute_is_working_properly(self):
        """testing if the date_updated attribute is working properly
        """
        
        test_value = datetime.datetime.now()
        self.test_simple_entity.date_updated = test_value
        self.assertEqual(self.test_simple_entity.date_updated, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_date_created_is_before_date_updated(self):
        """testing if a ValueError is going to be raised when trying to set the
        date_updated to a time before date_created
        """
        
        
        self.kwargs["date_created"] = datetime.datetime(2000, 1, 1, 1, 1, 1)
        self.kwargs["date_updated"] = datetime.datetime(1990, 1, 1, 1, 1, 1)
        
        # create a new entity with these dates
        # and expect a ValueError
        self.assertRaises(ValueError, SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test___repr__(self):
        """testing the __repr__ works properly
        """
        
        self.assertEqual(
            self.test_simple_entity.__repr__(),
            "<%s (%s, %s)>" % (
                self.test_simple_entity.entity_type,
                self.test_simple_entity.name,
                self.test_simple_entity.code)
        )
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_is_None(self):
        """testing if nothing will happen the type argument is None
        """
        self.kwargs["type"] = None
        new_simple_entity = SimpleEntity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_is_set_to_None(self):
        """testing if nothing will be happend when the type attribute is set to
        None.
        """
        
        self.test_simple_entity.type = None
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_accepts_only_Type_instances(self):
        """testing if a TypeError will be raised when the given type attribute
        is not instance of stalker.core.models.Type class
        """
        
        test_values = [1, 1.2, "a type"]
        
        for test_value in test_values:
            self.kwargs["type"] = test_value
            self.assertRaises(TypeError, SimpleEntity, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_argument_accepts_Type_instances(self):
        """testing if no error will be raised when the type argument is given
        as a stalker.core.models.Type instance
        """
        
        # test with a proper Type
        self.kwargs["type"] = self.test_type
        # no error is expected
        new_simple_entity = SimpleEntity(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_accepts_only_Type_instances(self):
        """testing if a TypeError will be raised when the given type attribute
        is not instance of stalker.core.models.Type class
        """
        
        test_values = [1, 1.2, "a type"]
        
        for test_value in test_values:
            self.assertRaises(TypeError, setattr, self.test_simple_entity,
                              "type", test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_type_attribute_accepts_Type_instances(self):
        """testing if no error will be raised when the type attribute is given
        as a stalker.core.models.Type instance
        """
        
        # test with a proper Type
        self.test_simple_entity.type = self.test_type
    
    
    
    #----------------------------------------------------------------------
    def test___strictly_typed___class_attribute_is_init_as_False(self):
        """testing if the __strictly_typed__ class attribute is initialized as
        False
        """
        
        self.assertEqual(self.test_simple_entity.__strictly_typed__, False)
    
    
    
    #----------------------------------------------------------------------
    def test___strictly_typed___attribute_set_to_True_and_no_type_argument(self):
        """testing if a TypeError will be raised the __strictly_typed__
        attribute is set to true in a derived class but there is no type
        argument defined
        """
        
        ## create a new class deriving from the SimpleEntity
        #class newClass(SimpleEntity):
            #__strictly_typed__ = True
        
        self.assertEqual(newClass.__strictly_typed__, True)
        
        # create a new instance and skip the Type attribute and expect a
        # TypeError
        if self.kwargs.has_key("type"):
            self.kwargs.pop("type")
        
        self.assertRaises(TypeError, newClass, **self.kwargs)        
    
    
    
    #----------------------------------------------------------------------
    def test___strictly_typed___attribute_set_to_True_and_type_argument_is_None(self):
        """testing if a TypeError will be raised the __strictly_typed__
        attribute is set to true in a derived class but the given type argument
        is None
        """
        
        ## create a new class deriving from the SimpleEntity
        #class newClass(SimpleEntity):
            #__strictly_typed__ = True
        
        # set it to None and expect a TypeError
        self.kwargs["type"] = None
        self.assertRaises(TypeError, newClass, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test___strictly_typed___attribute_set_to_True_and_type_argument_is_not_Type(self):
        """testing if a TypeError will be raised the __strictly_typed__
        attribute is set to true in a derived class but the given type argument
        is not a string
        """
        
        ## create a new class deriving from the SimpleEntity
        #class newClass(SimpleEntity):
            #__strictly_typed__ = True
        
        test_values = [1, 1.2, ["a", "list"], {"a": "dict"}]
        
        for test_value in test_values:
            # set it and expect a TypeError
            self.kwargs["type"] = test_value
            self.assertRaises(TypeError, newClass, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test___stalker_version__attribute_is_automatically_set_to_the_current_version_of_Stalker(self):
        """testing if the __stalker_version__ is automatically set to the
        current version for the newly created SimpleEntities
        """
        
        new_simpleEntity = SimpleEntity(**self.kwargs)
        
        self.assertEqual(new_simpleEntity.__stalker_version__,
                         stalker.__version__)
        
        # update stalker.__version__ to a test value
        current_version = stalker.__version__
        
        test_version = "test_version"
        stalker.__version__ = test_version
        
        # test if it is updated
        self.assertEqual(stalker.__version__, test_version)
        
        # create a new SimpleEntity and check if it is following the version
        new_simpleEntity2 = SimpleEntity(**self.kwargs)
        self.assertEqual(new_simpleEntity2.__stalker_version__, test_version)
        
        # restore the stalker.__version__
        stalker.__version__ = current_version
        
        
    
    
    
    