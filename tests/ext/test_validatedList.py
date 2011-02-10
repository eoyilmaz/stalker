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
    def test___init__2(self):
        """testing initialization with a list of different kind of objects will
        reduce the list to a list containing the objects of the type of first
        element
        """
        
        test_list = [1, 2, "ozgur", 3.2, 4, 5]
        test_expected_list = [1, 2, 4, 5]
        
        mock_validated_list = ValidatedList(test_list)
        
        self.assertEquals(mock_validated_list, test_expected_list)
    
    
    
    #----------------------------------------------------------------------
    def test___init__with_only_type_argument(self):
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
    def test___init__with_list_and_matching_type_argument(self):
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
    def test___init__with_list_and_non_matching_type_argument(self):
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
    def test___init__with_list_and_non_mathcing_type_argument_2(self):
        """testing initialization with a list and non matching type will filter
        the non-matching elements in the list
        """
        
        vList1 = ValidatedList(["str", 1, 2.3, 2, 3, "another str", 4], int)
        self.assertEquals(vList1, [1, 2, 3, 4])
    
    
    
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
    def test_append(self):
        """testing append method
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.append,
            "a string value"
        )
    
    
    #----------------------------------------------------------------------
    def test_append_2(self):
        """testing append method with un-initialized class
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.append,
            "a string value"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_append_3(self):
        """testing if append method with newly created un-inialized class fills
        the self.__type__
        """
        
        new_list = ValidatedList()
        
        self.assertTrue(new_list.__type__ is None)
        
        new_list.append(1)
        self.assertEquals(new_list.__type__, type(1))
    
    
    
    #----------------------------------------------------------------------
    def test_append_4(self):
        """testing append functionality
        """
        
        test_value = 45
        self.mock_valideted_list1.append(test_value)
        self.assertEquals(self.mock_valideted_list1[-1], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_extend(self):
        """testing extend method
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.extend,
            ["a", "string", "list"]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_extend_2(self):
        """testing extend method with un-initialized class
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.extend,
            ["a", "string", "list"]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_extend_3(self):
        """testing extend with zero length list
        """
        
        new_list = ValidatedList()
        new_list.extend([])
    
    
    
    #----------------------------------------------------------------------
    def test_extend_4(self):
        """testing extend functionality
        """
        
        test_value = [34, 32]
        
        self.mock_valideted_list1.extend(test_value)
        self.assertEquals(self.mock_valideted_list1[-2:], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_insert(self):
        """testing insert method
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.insert,
            0,
            "a str"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_insert_2(self):
        """testing insert method with un-initialized class
        """
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.insert,
            0,
            "a str"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_insert_3(self):
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
    def test_insert_4(self):
        """testing insert functionality
        """
        
        test_value = 101
        self.mock_valideted_list1.insert(0, test_value)
        self.assertEquals(self.mock_valideted_list1[0], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test___add__(self):
        """testing __add__ method
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.__add__,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test___add__2(self):
        """testing __add__ (+) method with un-initialized class
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.__add__,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test___add__3(self):
        """testing __add__ with newly created un-initialized list and an empty
        list
        """
        
        new_list = ValidatedList()
        # check if the __type__ is None
        self.assertTrue(new_list.__type__ is None)
        
        # add element
        new_list = new_list + []
    
    
    
    #----------------------------------------------------------------------
    def test___add__4(self):
        """testing __add__ functionality
        """
        
        test_value = [1002, 1004]
        self.mock_valideted_list1 = self.mock_valideted_list1 + test_value
        self.assertEquals(self.mock_valideted_list1[-2:], test_value)
    
    
    
    #----------------------------------------------------------------------
    def test___iadd__(self):
        """testing __iadd__ (+=) method
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list1.__iadd__,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test___iadd__2(self):
        """testing __iadd__ (+=) method with un-initialized class
        """
        
        test_value = ["a", "b", "c"]
        
        self.assertRaises(
            ValueError,
            self.mock_valideted_list2.__iadd__,
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test___iadd__3(self):
        """testing __iadd__ with newly created un-initialized list and an empty
        list
        """
        
        new_list = ValidatedList()
        # check if the __type__ is None
        self.assertTrue(new_list.__type__ is None)
        
        # iadd element
        new_list += []
    
    
    
    #----------------------------------------------------------------------
    def test___iadd__4(self):
        """testing __iadd__ functionality
        """
        
        test_value = [1032, 12304]
        self.mock_valideted_list1 += test_value
        self.assertEquals(self.mock_valideted_list1[-2:], test_value)
    
    
    