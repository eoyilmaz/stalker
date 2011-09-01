#-*- coding: utf-8 -*-



import unittest
from stalker.ext.validatedList import ValidatedList



########################################################################
class FunctionCalled(Exception):
    """An exception to be used in the test
    """
    
    #----------------------------------------------------------------------
    def __init__(self):
        pass
        
    
    




########################################################################
class ValidetedListTester(unittest.TestCase):
    """tests ValidatedList class
    """
    
    #----------------------------------------------------------------------
    def setUp(self):
        
        # create a test ValidetedList
        
        self.normal_list = [1, 2, 3, 4, 5]
        
        self.test_validated_list1 = ValidatedList(self.normal_list)
        self.test_validated_list2 = ValidatedList()
        
        # now append something to the second list which is not initialized with
        # a list
        self.test_validated_list2.append(1)
    
    
    
    #----------------------------------------------------------------------
    def test___init__(self):
        """testing initialization
        """
        
        test_value = "a string value"
        
        test_valideted_list = ValidatedList()
        test_valideted_list.append(test_value)
        
        # check if the __type__ is set to str
        self.assertEqual(test_valideted_list.__type__, type(test_value))
        
        # check if the __type_as_str__ is set to str
        self.assertEqual(test_valideted_list.__type_as_str__, "str")
    
    
    
    #----------------------------------------------------------------------
    def test___init___2(self):
        """testing initialization with a list of different kind of objects will
        reduce the list to a list containing the objects of the type of first
        element
        """
        
        test_list = [1, 2, "ozgur", 3.2, 4, 5]
        test_expected_list = [1, 2, 4, 5]
        
        test_validated_list = ValidatedList(test_list)
        
        self.assertEqual(test_validated_list, test_expected_list)
    
    
    
    #----------------------------------------------------------------------
    def test___init___with_only_type_argument(self):
        """testing initialization with the type argument sticks the type to
        given type
        """
        
        # create a new ValidatedList with no list given
        vList1 = ValidatedList([], int)
        
        self.assertRaises(
            TypeError,
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
            TypeError,
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
            TypeError,
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
        self.assertEqual(vList1, [1, 2, 3, 4])
    
    
    
    #----------------------------------------------------------------------
    def test___init___with_string_type_argument(self):
        """testing __init__ with string values for type_ argument
        """
        
        test_list = ValidatedList([], "str")
        
        self.assertRaises(TypeError, test_list.append, 1)
        test_list.append("a str")
        
        # a real world example
        test_list2 = ValidatedList([], "datetime.datetime")
        import datetime
        test_list2.append(datetime.datetime.now())
        
        self.assertEqual(test_list2.__type__, datetime.datetime)
    
    
    
    #----------------------------------------------------------------------
    def test___setitem__with_wrong_type(self):
        """testing __setitem__ method
        """
        
        self.assertRaises(
            TypeError,
            self.test_validated_list1.__setitem__,
            -1,
            "string value"
        )
    
    
    
    #----------------------------------------------------------------------
    def test___setitem__with_uninitialized_class(self):
        """testing __setitem__ method with un-initialized class
        """
        
        self.assertRaises(
            TypeError,
            self.test_validated_list2.__setitem__,
            -1,
            "string value"
        )
    
    
    
    #----------------------------------------------------------------------
    def test___setitem__works_properly(self):
        """testing __setitem__ functionality
        """
        test_value = 50
        self.test_validated_list1[0] = test_value
        self.assertEqual(self.test_validated_list1[0], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test__setitem___works_uniquely(self):
        """testing if __setitem__ works uniquely
        """
        
        new_list = ValidatedList()
        new_list.extend([1, 2, 3])
        new_list[1] = 3
        self.assertItemsEqual(new_list, [1, 2, 3])
    
    
    
    #----------------------------------------------------------------------
    def test___setslice___with_wrong_type(self):
        """testing __setslice__ method
        """
        
        self.assertRaises(
            TypeError,
            self.test_validated_list1.__setslice__,
            0,
            3,
            "string value"
        )
    
    
    
    #----------------------------------------------------------------------
    def test___setslice___uninitialized_class(self):
        """testing __setslice__ method with un-initialized class
        """
        
        self.assertRaises(
            TypeError,
            self.test_validated_list2.__setslice__,
            0,
            3,
            "string value"
        )
    
    
    
    #----------------------------------------------------------------------
    def test___setslice___works_properly(self):
        """testing __setslice__ functionality
        """
        
        test_value = [7, 8, 9]
        self.test_validated_list1[1:3] = test_value
        self.assertEqual(self.test_validated_list1[1:4], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test___setslice___works_uniquly(self):
        """testing if __setslice__ works uniquely
        """
        
        new_list = ValidatedList([1, 2, 3, 4, 5])
        new_list[0:2] = [3, 4]
        self.assertItemsEqual(new_list, [3, 4, 5])
        
        new_list = ValidatedList([1, 2, 3, 4, 5])
        new_list[0:2] = [1, 2, 3]
        self.assertItemsEqual(new_list, [1, 2, 3, 4, 5])
        
        new_lislt = ValidatedList([1, 2, 3, 4, 5])
        new_list[3:1] = [1, 2, 3, 4, 5, 6]
        #[1, 2, 3, 1, 2, 3, 4, 5, 6, 4, 5]
        self.assertItemsEqual([1, 2, 3, 4, 5, 6], new_list)
        
        new_list = ValidatedList([1, 2, 3, 4, 5])
        new_list[3:1] = [11, 12, 13, 14, 15, 16]
        #[1, 2, 3, 11, 12, 13, 14, 15, 16, 4, 5]
        self.assertItemsEqual([1, 2, 3, 11, 12, 13, 14, 15, 16, 4, 5],
                              new_list)
    
    
    
    #----------------------------------------------------------------------
    def test_append_with_wrong_type(self):
        """testing if a TypeError will be raised in append method when the
        given object is in wrong type
        """
        
        self.assertRaises(
            TypeError,
            self.test_validated_list1.append,
            "a string value"
        )
    
    
    #----------------------------------------------------------------------
    def test_append_with_uninit_class(self):
        """testing append method with un-initialized class
        """
        
        self.assertRaises(
            TypeError,
            self.test_validated_list2.append,
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
        self.assertEqual(new_list.__type__, type(1))
    
    
    
    #----------------------------------------------------------------------
    def test_append_works_properly(self):
        """testing append functionality
        """
        
        test_value = 45
        self.test_validated_list1.append(test_value)
        self.assertEqual(self.test_validated_list1[-1], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_append_works_uniquely(self):
        """testing if append will not add same item twice
        """
        
        test_value = 45
        self.test_validated_list1.append(test_value)
        
        # append it again
        self.test_validated_list1.append(test_value)
        
        # now check if it is equal to the set of the items
        self.assertItemsEqual(
            self.test_validated_list1,
            list(set(self.test_validated_list1))
        )
    
    
    
    #----------------------------------------------------------------------
    def test_append_when_type_argument_is_string(self):
        """testing if append works fine even when the type argument is given as
        string
        """
        
        new_list = ValidatedList([], "str")
        
        # now check if it only accepts strings
        self.assertRaises(TypeError, new_list.append, 12)
        
        # this should work
        new_list.append("test string")
    
    
    
    #----------------------------------------------------------------------
    def test_append_when_type_argument_is_type(self):
        """testing if append works fine when the type argument is instance of
        type
        """
        
        new_list = ValidatedList([], str)
        
        # now check if it only accpets strings
        self.assertRaises(TypeError, new_list.append, 12)
        
        # this should work
        new_list.append("test string")
    
    
    
    #----------------------------------------------------------------------
    def test_append_lazy_loading(self):
        """testing if the type will be lazily imported in append method when
        given as a string
        """
        
        new_list = ValidatedList([], "datetime.datetime")
        
        # check if it is still a string
        self.assertEqual(new_list.__type__, "datetime.datetime")
        
        # check if it is converted to a type instance when appended
        import datetime
        new_list.append(datetime.datetime.now())
        
        self.assertEqual(new_list.__type__, datetime.datetime)
    
    
    
    #----------------------------------------------------------------------
    def test_extend_with_wrong_type(self):
        """testing if a TypeError will be raised in extend method when the
        given object is in wrong type
        """
        
        self.assertRaises(
            TypeError,
            self.test_validated_list1.extend,
            ["a", "string", "list"]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_extend_with_uninit_class(self):
        """testing extend method with un-initialized class
        """
        
        self.assertRaises(
            TypeError,
            self.test_validated_list2.extend,
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
        
        self.test_validated_list1.extend(test_value)
        self.assertEqual(self.test_validated_list1[-2:], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_extend_works_uniquely(self):
        """testing if extend will not add same item twice
        """
        
        test_value = [1, 2, 45]
        self.test_validated_list1.extend(test_value)
        
        # extend it again
        self.test_validated_list1.extend(test_value)
        
        # now check if it is equal to the set of the items
        self.assertItemsEqual(
            self.test_validated_list1,
            list(set(self.test_validated_list1))
        )
    
    
    
    #----------------------------------------------------------------------
    def test_extend_when_type_argument_is_string(self):
        """testing if extend works fine even when the type argument is given as
        string
        """
        
        new_list = ValidatedList([], "str")
        
        # now check if it only accepts strings
        self.assertRaises(TypeError, new_list.extend, [12, 123])
        
        # this should work
        new_list.extend(["test", "string"])
    
    
    
    #----------------------------------------------------------------------
    def test_extend_when_type_argument_is_type(self):
        """testing if extend works fine when the type argument is instance of
        type
        """
        
        new_list = ValidatedList([], str)
        
        # now check if it only accpets strings
        self.assertRaises(TypeError, new_list.extend, [12, 123])
        
        # this should work
        new_list.extend(["test", "string"])
    
    
    
    #----------------------------------------------------------------------
    def test_extend_lazy_loading(self):
        """testing if the type will be lazily imported in extend method when
        given as a string
        """
        
        new_list = ValidatedList([], "datetime.datetime")
        
        # check if it is still a string
        self.assertEqual(new_list.__type__, "datetime.datetime")
        
        # check if it is converted to a type instance when appended
        import datetime
        new_list.extend([datetime.datetime.now()])
        
        self.assertEqual(new_list.__type__, datetime.datetime)
    
    
    
    #----------------------------------------------------------------------
    def test_insert_with_wrong_type(self):
        """testing if a TypeError will be raised in insert method when the
        given object is in wrong type
        """
        
        self.assertRaises(
            TypeError,
            self.test_validated_list1.insert,
            0,
            "a str"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_insert_with_uninit_class(self):
        """testing if a TypeError will be raised in un-initialized classes
        insert method when the given item is in wrong type
        """
        
        self.assertRaises(
            TypeError,
            self.test_validated_list2.insert,
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
        self.assertEqual(new_list.__type__, type(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_insert_works_properly(self):
        """testing insert functionality
        """
        
        test_value = 101
        self.test_validated_list1.insert(0, test_value)
        self.assertEqual(self.test_validated_list1[0], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_insert_works_uniquely(self):
        """testing if insert will not add same item twice
        """
        
        test_value = 1
        self.test_validated_list1.insert(1, test_value)
        
        # insert it again
        self.test_validated_list1.insert(2, test_value)
        
        # now check if it is equal to the set of the items
        self.assertItemsEqual(
            self.test_validated_list1,
            list(set(self.test_validated_list1))
        )
    
    
    
    #----------------------------------------------------------------------
    def test_insert_when_type_argument_is_string(self):
        """testing if insert works fine even when the type argument is given as
        string
        """
        
        new_list = ValidatedList([], "str")
        
        # now check if it only accepts strings
        self.assertRaises(TypeError, new_list.insert, 0, 12)
        
        # this should work
        new_list.insert(0, "test string")
    
    
    
    #----------------------------------------------------------------------
    def test_insert_when_type_argument_is_type(self):
        """testing if insert works fine when the type argument is instance of
        type
        """
        
        new_list = ValidatedList([], str)
        
        # now check if it only accpets strings
        self.assertRaises(TypeError, new_list.insert, 0, 12)
        
        # this should work
        new_list.insert(0, "test string")
    
    
    
    #----------------------------------------------------------------------
    def test_insert_lazy_loading(self):
        """testing if the type will be lazily imported in insert method when
        given as a string
        """
        
        new_list = ValidatedList([], "datetime.datetime")
        
        # check if it is still a string
        self.assertEqual(new_list.__type__, "datetime.datetime")
        
        # check if it is converted to a type instance when appended
        import datetime
        new_list.insert(0, datetime.datetime.now())
        
        self.assertEqual(new_list.__type__, datetime.datetime)
    
    
    
    #----------------------------------------------------------------------
    def test___add___with_wrong_type(self):
        """testing if a TypeError will be raised in the __add__ method when
        the given item is in wrong type
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            TypeError,
            self.test_validated_list1.__add__,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test___add___with_uninit_class(self):
        """testing __add__ (+) method with un-initialized class
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            TypeError,
            self.test_validated_list2.__add__,
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
        self.test_validated_list1 = self.test_validated_list1 + test_value
        self.assertEqual(self.test_validated_list1[-2:], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test___add___when_type_argument_is_string(self):
        """testing if __add__ works fine even when the type argument is given
        as string
        """
        
        new_list = ValidatedList([], "str")
        
        # now check if it only accepts strings
        self.assertRaises(TypeError, new_list.__add__, [12, 123])
        
        # this should work
        new_list.__add__(["test", "string"])
    
    
    
    #----------------------------------------------------------------------
    def test___add___when_type_argument_is_type(self):
        """testing if __add__ works fine when the type argument is instance of
        type
        """
        
        new_list = ValidatedList([], str)
        
        # now check if it only accpets strings
        self.assertRaises(TypeError, new_list.__add__, [12, 123])
        
        # this should work
        new_list.__add__(["test","string"])
    
    
    
    #----------------------------------------------------------------------
    def test___add___lazy_loading(self):
        """testing if the type will be lazily imported in __add__ method when
        given as a string
        """
        
        new_list = ValidatedList([], "datetime.datetime")
        
        # check if it is still a string
        self.assertEqual(new_list.__type__, "datetime.datetime")
        
        # check if it is converted to a type instance when appended
        import datetime
        new_list.__add__([datetime.datetime.now()])
        
        self.assertEqual(new_list.__type__, datetime.datetime)
    
    
    
    #----------------------------------------------------------------------
    def test___add___returns_ValidatedList(self):
        """testing if __add__ returns a ValidatedList
        """
        
        new_list = ValidatedList()
        new_list.append(1)
        self.assertIsInstance( new_list + [1, 2, 3], ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test___add___works_uniquely(self):
        """testing if __add__ works uniquely
        """
        
        new_list = ValidatedList([1, 2, 3])
        new_list = new_list + [1, 2, 3, 4]
        
        self.assertItemsEqual(list(set(new_list)), new_list)
    
    
    
    #----------------------------------------------------------------------
    def test___iadd___with_wrong_type(self):
        """testing if a TypeError will be raised in the __iadd__ (+=) method
        when the given item type is wrong
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            TypeError,
            self.test_validated_list1.__iadd__,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test___iadd___with_uninit_class(self):
        """testing if a TypeError will be raised in the __iadd__ (+=) method
        of the un-initialized class when the given item is in wrong type
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            TypeError,
            self.test_validated_list2.__iadd__,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test___iadd___with_new_uninit_class(self):
        """testing __iadd__ with newly created un-initialized list and an empty
        list
        """
        
        new_list = ValidatedList()
        # check if the __type__ is None
        self.assertTrue(new_list.__type__ is None)
        
        # iadd element
        new_list += []
    
    
    
    #----------------------------------------------------------------------
    def test___iadd___works_properly(self):
        """testing __iadd__ functionality
        """
        # id should not change
        prev_id = id(self.test_validated_list1)
        test_value = [1032, 12304]
        self.test_validated_list1 += test_value
        self.assertEqual(self.test_validated_list1[-2:], test_value)
        self.assertEqual(prev_id, id(self.test_validated_list1))
    
    
    
    #----------------------------------------------------------------------
    def test___iadd___when_type_argument_is_string(self):
        """testing if __iadd__ works fine even when the type argument is given
        as string
        """
        
        new_list = ValidatedList([], "str")
        
        # now check if it only accepts strings
        self.assertRaises(TypeError, new_list.__iadd__, [12, 123])
        
        # this should work
        new_list.__iadd__(["test", "string"])
    
    
    
    #----------------------------------------------------------------------
    def test___iadd___when_type_argument_is_type(self):
        """testing if __iadd__ works fine when the type argument is instance of
        type
        """
        
        new_list = ValidatedList([], str)
        
        # now check if it only accpets strings
        self.assertRaises(TypeError, new_list.__iadd__, [12, 123])
        
        # this should work
        new_list.__iadd__(["test", "string"])
    
    
    
    #----------------------------------------------------------------------
    def test___iadd___lazy_loading(self):
        """testing if the type will be lazily imported in __iadd__ method when
        given as a string
        """
        
        new_list = ValidatedList([], "datetime.datetime")
        
        # check if it is still a string
        self.assertEqual(new_list.__type__, "datetime.datetime")
        
        # check if it is converted to a type instance when appended
        import datetime
        new_list.__iadd__([datetime.datetime.now()])
        
        self.assertEqual(new_list.__type__, datetime.datetime)
    
    
    #----------------------------------------------------------------------
    def test___iadd___works_uniquely(self):
        """testing if __iadd__ works uniquely
        """
        new_list = ValidatedList([1, 2, 3])
        new_list += [1, 2, 3]
        self.assertItemsEqual(list(set(new_list)), new_list)
    
    
    
    #----------------------------------------------------------------------
    def test___iadd__returns_ValidatedList(self):
        """test if __iadd__ returns ValidatedList instance
        """
        new_list = ValidatedList([1, 2, 3])
        new_list += [1, 2, 3]
        self.assertIsInstance(new_list, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_validator_argument_is_skipped(self):
        """testing if nothing happens when the validator argument is skipped
        """
        
        new_list = ValidatedList([], "datetime.datetime")
    
    
    
    #----------------------------------------------------------------------
    def test_validator_will_be_called_for___setitem__(self):
        """testing if the given validator will be called when __setitem__ is
        called
        """
        
        # create a function returning a defined value
        def Func1(*args):
            raise FunctionCalled
        
        try:
            new_list = ValidatedList([], str, Func1)
        except FunctionCalled:
            pass
        
        # a little cheat
        validator = new_list._validator
        new_list._validator = None
        new_list.append("start value")
        new_list._validator = validator
        
        self.assertRaises(FunctionCalled, new_list.__setitem__, 0,
                          "test_value")
    
    
    
    #----------------------------------------------------------------------
    def test_validator_will_be_called_for___setslice__(self):
        """testing if the given validator will be called when __setslice__ is
        called
        """
        
        # create a function returning a defined value
        def Func1(*args):
            raise FunctionCalled
        
        new_list = ValidatedList([], str, Func1)
        
        self.assertRaises(FunctionCalled, new_list.__setslice__, 0, 1,
                          ["test_value"])
    
    
    
    #----------------------------------------------------------------------
    def test_validator_will_be_called_for_append(self):
        """testing if the given validator will be called when append is called
        """
        
        # create a function returning a defined value
        def Func1(*args):
            raise FunctionCalled
        
        new_list = ValidatedList([], str, Func1)
        
        self.assertRaises(FunctionCalled, new_list.append, "test_value")
    
    
    
    #----------------------------------------------------------------------
    def test_validator_will_be_called_for_extend(self):
        """testing if the given validator will be called when extend is called
        """
        
        # create a function returning a defined value
        def Func1(*args):
            raise FunctionCalled
        
        new_list = ValidatedList([], str, Func1)
        
        self.assertRaises(FunctionCalled, new_list.extend, ["test_value"])
    
    
    
    #----------------------------------------------------------------------
    def test_validator_will_be_called_for_insert(self):
        """testing if the given validator will be called when insert is called
        """
        
        # create a function returning a defined value
        def Func1(*args):
            raise FunctionCalled
        
        new_list = ValidatedList([], str, Func1)
        
        self.assertRaises(FunctionCalled, new_list.insert, 0, "test_value")
    
    
    
    #----------------------------------------------------------------------
    def test_validator_will_be_called_for___add__(self):
        """testing if the given validator will be called when __add__ is called
        """
        
        # create a function returning a defined value
        def Func1(*args):
            raise FunctionCalled
        
        new_list = ValidatedList([], str, Func1)
        
        self.assertRaises(FunctionCalled, new_list.__add__, ["test_value"])
    
    
    
    #----------------------------------------------------------------------
    def test_validator_will_be_called_for___iadd__(self):
        """testing if the given validator will be called when __iadd__ is
        called
        """
        
        # create a function returning a defined value
        def Func1(*args):
            raise FunctionCalled
        
        new_list = ValidatedList([], str, Func1)
        
        self.assertRaises(FunctionCalled, new_list.__iadd__, ["test_value"])
    
    
    
    #----------------------------------------------------------------------
    def test_validator_will_be_called_for_pop(self):
        """testing if the given validator will be called when pop is called
        """
        
        # create a function returning a defined value
        def Func1(*args):
            raise FunctionCalled
        
        new_list = ValidatedList([], str, Func1)
        
        # a little cheat
        validator = new_list._validator
        new_list._validator = None
        new_list.append("start value")
        new_list._validator = validator
        
        self.assertRaises(FunctionCalled, new_list.pop, 0)
    
    
    
    #----------------------------------------------------------------------
    def test_validator_will_be_called_for_remove(self):
        """testing if the given validator will be called when remove is called
        """
        
        # create a function returning a defined value
        def Func1(*args):
            raise FunctionCalled
        
        new_list = ValidatedList([], str, Func1)
        
        # a little cheat
        validator = new_list._validator
        new_list._validator = None
        new_list.append("start value")
        new_list._validator = validator
        
        self.assertRaises(FunctionCalled, new_list.remove, "start value")
    
    
    
    ##----------------------------------------------------------------------
    #def test_validator_will_be_called_for___delitem__(self):
        #"""testing if the given validator will be called when __delitem__ is
        #called
        #"""
        
        ## create a function returning a defined value
        #def Func1(*args):
            #raise FunctionCalled
        
        #new_list = ValidatedList([], str, Func1)
        
        ## a little cheat
        #validator = new_list._validator
        #new_list._validator = None
        #new_list.append("start value")
        #new_list._validator = validator
        
        #self.assertRaises(FunctionCalled, new_list.__delitem__, 0)
    
    
    
    ##----------------------------------------------------------------------
    #def test_validator_will_be_called_for___delslice__(self):
        #"""testing if the given validator will be called when __delslice__ is
        #called
        #"""
        
        ## create a function returning a defined value
        #def Func1(*args):
            #raise FunctionCalled
        
        #new_list = ValidatedList([], str, Func1)
        
        ## a little cheat
        #validator = new_list._validator
        #new_list._validator = None
        #new_list.append("start value")
        #new_list.append("end value")
        #new_list._validator = validator
        
        #self.assertRaises(FunctionCalled, new_list.__delslice__, 0, 1)
    
    
    
    
    
    