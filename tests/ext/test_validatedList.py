#-*- coding: utf-8 -*-



import unittest
from stalker.ext.validatedList import ValidatedList




########################################################################
class ValidetedListTester(unittest.TestCase):
    """tests ValidatedList class
    """
    
    #----------------------------------------------------------------------
    def setUp(self):
        
        # create a mock ValidetedList
        
        self.normal_list = [1, 2, 3, 4, 5]
        
        self.mock_valideted_list1 = ValidatedList(self.normal_list)
        self.mock_valideted_list2 = ValidatedList()
        
        # now append something to the second list which is not initialized with
        # a list
        self.mock_valideted_list2.append(1)
    
    
    
    #----------------------------------------------------------------------
    def test___init__(self):
        """testing initialization
        """
        
        test_value = "a string value"
        
        mock_valideted_list = ValidatedList()
        mock_valideted_list.append(test_value)
        
        # check if the __type__ is set to str
        self.assertEquals(mock_valideted_list.__type__, type(test_value))
        
        # check if the __type_as_str__ is set to str
        self.assertEquals(mock_valideted_list.__type_as_str__, "str")
    
    
    
    #----------------------------------------------------------------------
    def test___init___2(self):
        """testing initialization with a list of different kind of objects will
        reduce the list to a list containing the objects of the type of first
        element
        """
        
        test_list = [1, 2, "ozgur", 3.2, 4, 5]
        test_expected_list = [1, 2, 4, 5]
        
        mock_validated_list = ValidatedList(test_list)
        
        self.assertEquals(mock_validated_list, test_expected_list)
    
    
    
    #----------------------------------------------------------------------
    def test___init___with_only_type_argument(self):
        """testing initialization with the type argument sticks the type to
        given type
        """
        
        # create a new ValidatedList with no list given
        vList1 = ValidatedList([], int)
        
        self.assertRaises(
            ValueError,
            vList1.append,
            "a string"
        )
        
        # no error
        vList1.append(10)
    
    
    
    #----------------------------------------------------------------------
    def test___init___with_list_and_matching_type_argument(self):
        """testing initialization with a list and a type argument sticks the
        type to given type with the list elements is also matching the type
        """
        
        # create a new ValidatedList with list
        vList1 = ValidatedList([0, 1, 2, 3], int)
        
        self.assertRaises(
            ValueError,
            vList1.append,
            "a string"
        )
        
        # no error
        vList1.append(4)
    
    
    
    #----------------------------------------------------------------------
    def test___init___with_list_and_non_matching_type_argument(self):
        """testing initialization with a list and a type argument sticks the 
        type to given type with list elements is not matching the given type
        """
        
        # create a new ValidatedList with list
        vList1 = ValidatedList([0, 1, 2, 3], str)
        
        self.assertRaises(
            ValueError,
            vList1.append,
            0
        )
        
        # no error
        vList1.append("4")
    
    
    
    #----------------------------------------------------------------------
    def test___init___with_list_and_non_mathcing_type_argument_2(self):
        """testing initialization with a list and non matching type will filter
        the non-matching elements in the list
        """
        
        vList1 = ValidatedList(["str", 1, 2.3, 2, 3, "another str", 4], int)
        self.assertEquals(vList1, [1, 2, 3, 4])
    
    
    
    #----------------------------------------------------------------------
    def test___init___with_string_type_argument(self):
        """testing __init__ with string values for type_ argument
        """
        
        test_list = ValidatedList([], "str")
        
        self.assertRaises(ValueError, test_list.append, 1)
        test_list.append("a str")
        
        # a real world example
        test_list2 = ValidatedList([], "datetime.datetime")
        import datetime
        test_list2.append(datetime.datetime.now())
        
        self.assertEquals(test_list2.__type__, datetime.datetime)
    
    
    
    #----------------------------------------------------------------------
    def test___setitem__(self):
        """testing __setitem__ method
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.__setitem__,
            -1,
            "string value"
        )
    
    
    
    #----------------------------------------------------------------------
    def test___setitem__2(self):
        """testing __setitem__ method with un-initialized class
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.__setitem__,
            -1,
            "string value"
        )
    
    
    
    #----------------------------------------------------------------------
    def test___setitem__3(self):
        """testing __setitem__ functionality
        """
        
        test_value = 5
        
        self.mock_valideted_list1[0] = test_value
        
        self.assertEquals(self.mock_valideted_list1[0], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test___setslice__(self):
        """testing __setslice__ method
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.__setslice__,
            0,
            3,
            "string value"
        )
    
    
    
    #----------------------------------------------------------------------
    def test___setslice__2(self):
        """testing __setslice__ method with un-initialized class
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.__setslice__,
            0,
            3,
            "string value"
        )
    
    
    
    #----------------------------------------------------------------------
    def test___setslice__3(self):
        """testing __setslice__ functionality
        """
        
        test_value = [7, 8, 9]
        self.mock_valideted_list1[1:3] = test_value
        self.assertEquals(self.mock_valideted_list1[1:4], test_value)
        
    
    
    
    #----------------------------------------------------------------------
    def test_append_with_wrong_type(self):
        """testing if a ValueError will be raised in append method when the
        given object is in wrong type
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.append,
            "a string value"
        )
    
    
    #----------------------------------------------------------------------
    def test_append_with_uninit_class(self):
        """testing append method with un-initialized class
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.append,
            "a string value"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_append_with_new_class_without_initialization(self):
        """testing if append method with newly created un-inialized class fills
        the self.__type__
        """
        
        new_list = ValidatedList()
        
        self.assertTrue(new_list.__type__ is None)
        
        new_list.append(1)
        self.assertEquals(new_list.__type__, type(1))
    
    
    
    #----------------------------------------------------------------------
    def test_append_works_properly(self):
        """testing append functionality
        """
        
        test_value = 45
        self.mock_valideted_list1.append(test_value)
        self.assertEquals(self.mock_valideted_list1[-1], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_append_when_type_argument_is_string(self):
        """testing if append works fine even when the type argument is given as
        string
        """
        
        new_list = ValidatedList([], "str")
        
        # now check if it only accepts strings
        self.assertRaises(ValueError, new_list.append, 12)
        
        # this should work
        new_list.append("test string")
    
    
    
    #----------------------------------------------------------------------
    def test_append_when_type_argument_is_type(self):
        """testing if append works fine when the type argument is instance of
        type
        """
        
        new_list = ValidatedList([], str)
        
        # now check if it only accpets strings
        self.assertRaises(ValueError, new_list.append, 12)
        
        # this should work
        new_list.append("test string")
    
    
    
    #----------------------------------------------------------------------
    def test_append_lazy_loading(self):
        """testing if the type will be lazily imported in append method when
        given as a string
        """
        
        new_list = ValidatedList([], "datetime.datetime")
        
        # check if it is still a string
        self.assertEquals(new_list.__type__, "datetime.datetime")
        
        # check if it is converted to a type instance when appended
        import datetime
        new_list.append(datetime.datetime.now())
        
        self.assertEquals(new_list.__type__, datetime.datetime)
    
    
    
    #----------------------------------------------------------------------
    def test_extend_with_wrong_type(self):
        """testing if a ValueError will be raised in extend method when the
        given object is in wrong type
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.extend,
            ["a", "string", "list"]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_extend_with_uninit_class(self):
        """testing extend method with un-initialized class
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.extend,
            ["a", "string", "list"]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_extend_with_zero_length_list(self):
        """testing extend with zero length list
        """
        
        new_list = ValidatedList()
        new_list.extend([])
    
    
    
    #----------------------------------------------------------------------
    def test_extend_works_properly(self):
        """testing extend functionality
        """
        
        test_value = [34, 32]
        
        self.mock_valideted_list1.extend(test_value)
        self.assertEquals(self.mock_valideted_list1[-2:], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_extend_when_type_argument_is_string(self):
        """testing if extend works fine even when the type argument is given as
        string
        """
        
        new_list = ValidatedList([], "str")
        
        # now check if it only accepts strings
        self.assertRaises(ValueError, new_list.extend, [12, 123])
        
        # this should work
        new_list.extend(["test", "string"])
    
    
    
    #----------------------------------------------------------------------
    def test_extend_when_type_argument_is_type(self):
        """testing if extend works fine when the type argument is instance of
        type
        """
        
        new_list = ValidatedList([], str)
        
        # now check if it only accpets strings
        self.assertRaises(ValueError, new_list.extend, [12, 123])
        
        # this should work
        new_list.extend(["test", "string"])
    
    
    
    #----------------------------------------------------------------------
    def test_extend_lazy_loading(self):
        """testing if the type will be lazily imported in extend method when
        given as a string
        """
        
        new_list = ValidatedList([], "datetime.datetime")
        
        # check if it is still a string
        self.assertEquals(new_list.__type__, "datetime.datetime")
        
        # check if it is converted to a type instance when appended
        import datetime
        new_list.extend([datetime.datetime.now()])
        
        self.assertEquals(new_list.__type__, datetime.datetime)
    
    
    
    #----------------------------------------------------------------------
    def test_insert_with_wrong_type(self):
        """testing if a ValueError will be raised in insert method when the
        given object is in wrong type
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.insert,
            0,
            "a str"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_insert_with_uninit_class(self):
        """testing if a ValueError will be raised in un-initialized classes
        insert method when the given item is in wrong type
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.insert,
            0,
            "a str"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_insert_new_uninit_class(self):
        """testing insert method with newly created un-initialized class
        """
        
        new_list = ValidatedList()
        # check if the __type__ is None
        self.assertTrue(new_list.__type__ is None)
        
        # insert element
        test_value = 1
        new_list.insert(0, test_value)
        
        # check the type is now set to type(test_value)
        self.assertEquals(new_list.__type__, type(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_insert_works_properly(self):
        """testing insert functionality
        """
        
        test_value = 101
        self.mock_valideted_list1.insert(0, test_value)
        self.assertEquals(self.mock_valideted_list1[0], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_insert_when_type_argument_is_string(self):
        """testing if insert works fine even when the type argument is given as
        string
        """
        
        new_list = ValidatedList([], "str")
        
        # now check if it only accepts strings
        self.assertRaises(ValueError, new_list.insert, 0, 12)
        
        # this should work
        new_list.insert(0, "test string")
    
    
    
    #----------------------------------------------------------------------
    def test_insert_when_type_argument_is_type(self):
        """testing if insert works fine when the type argument is instance of
        type
        """
        
        new_list = ValidatedList([], str)
        
        # now check if it only accpets strings
        self.assertRaises(ValueError, new_list.insert, 0, 12)
        
        # this should work
        new_list.insert(0, "test string")
    
    
    
    #----------------------------------------------------------------------
    def test_insert_lazy_loading(self):
        """testing if the type will be lazily imported in insert method when
        given as a string
        """
        
        new_list = ValidatedList([], "datetime.datetime")
        
        # check if it is still a string
        self.assertEquals(new_list.__type__, "datetime.datetime")
        
        # check if it is converted to a type instance when appended
        import datetime
        new_list.insert(0, datetime.datetime.now())
        
        self.assertEquals(new_list.__type__, datetime.datetime)
    
    
    
    #----------------------------------------------------------------------
    def test___add___with_wrong_type(self):
        """testing if a ValueError will be raised in the __add__ method when
        the given item is in wrong type
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.__add__,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test___add___with_uninit_class(self):
        """testing __add__ (+) method with un-initialized class
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.__add__,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test___add___with_new_uninit_class(self):
        """testing __add__ with newly created un-initialized list and an empty
        list
        """
        
        new_list = ValidatedList()
        # check if the __type__ is None
        self.assertTrue(new_list.__type__ is None)
        
        # add element
        new_list = new_list + []
    
    
    
    #----------------------------------------------------------------------
    def test___add___works_properly(self):
        """testing __add__ functionality
        """
        
        test_value = [1002, 1004]
        self.mock_valideted_list1 = self.mock_valideted_list1 + test_value
        self.assertEquals(self.mock_valideted_list1[-2:], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test___add___when_type_argument_is_string(self):
        """testing if __add__ works fine even when the type argument is given
        as string
        """
        
        new_list = ValidatedList([], "str")
        
        # now check if it only accepts strings
        self.assertRaises(ValueError, new_list.__add__, [12, 123])
        
        # this should work
        new_list.__add__(["test", "string"])
    
    
    
    #----------------------------------------------------------------------
    def test___add___when_type_argument_is_type(self):
        """testing if __add__ works fine when the type argument is instance of
        type
        """
        
        new_list = ValidatedList([], str)
        
        # now check if it only accpets strings
        self.assertRaises(ValueError, new_list.__add__, [12, 123])
        
        # this should work
        new_list.__add__(["test","string"])
    
    
    
    #----------------------------------------------------------------------
    def test___add___lazy_loading(self):
        """testing if the type will be lazily imported in __add__ method when
        given as a string
        """
        
        new_list = ValidatedList([], "datetime.datetime")
        
        # check if it is still a string
        self.assertEquals(new_list.__type__, "datetime.datetime")
        
        # check if it is converted to a type instance when appended
        import datetime
        new_list.__add__([datetime.datetime.now()])
        
        self.assertEquals(new_list.__type__, datetime.datetime)
    
    
    
    #----------------------------------------------------------------------
    def test___iadd___with_wrong_type(self):
        """testing if a ValueError will be raised in the __iadd__ (+=) method
        when the given item type is wrong
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.__iadd__,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test___iadd__with_uninit_class(self):
        """testing if a ValueErrorr will be raised in the __iadd__ (+=) method
        of the un-initialized class when the given item is in wrong type
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.__iadd__,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test___iadd__with_new_uninit_class(self):
        """testing __iadd__ with newly created un-initialized list and an empty
        list
        """
        
        new_list = ValidatedList()
        # check if the __type__ is None
        self.assertTrue(new_list.__type__ is None)
        
        # iadd element
        new_list += []
    
    
    
    #----------------------------------------------------------------------
    def test___iadd__works_properly(self):
        """testing __iadd__ functionality
        """
        
        test_value = [1032, 12304]
        self.mock_valideted_list1 += test_value
        self.assertEquals(self.mock_valideted_list1[-2:], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test___iadd___when_type_argument_is_string(self):
        """testing if __iadd__ works fine even when the type argument is given
        as string
        """
        
        new_list = ValidatedList([], "str")
        
        # now check if it only accepts strings
        self.assertRaises(ValueError, new_list.__iadd__, [12, 123])
        
        # this should work
        new_list.__iadd__(["test", "string"])
    
    
    
    #----------------------------------------------------------------------
    def test___iadd___when_type_argument_is_type(self):
        """testing if __iadd__ works fine when the type argument is instance of
        type
        """
        
        new_list = ValidatedList([], str)
        
        # now check if it only accpets strings
        self.assertRaises(ValueError, new_list.__iadd__, [12, 123])
        
        # this should work
        new_list.__iadd__(["test", "string"])
    
    
    
    #----------------------------------------------------------------------
    def test___iadd___lazy_loading(self):
        """testing if the type will be lazily imported in __iadd__ method when
        given as a string
        """
        
        new_list = ValidatedList([], "datetime.datetime")
        
        # check if it is still a string
        self.assertEquals(new_list.__type__, "datetime.datetime")
        
        # check if it is converted to a type instance when appended
        import datetime
        new_list.__iadd__([datetime.datetime.now()])
        
        self.assertEquals(new_list.__type__, datetime.datetime)
