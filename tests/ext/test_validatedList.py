#-*- coding: utf-8 -*-



import unittest
from stalker.utils import validatedList




########################################################################
class ValidetedListTester(unittest.TestCase):
    """tests ValidatedList class
    """
    
    #----------------------------------------------------------------------
    def setUp(self):
        
        
        # create a mock ValidetedList
        
        self.normal_list = [1, 2, 3, 4, 5]
        
        self.mock_valideted_list1 = validatedList.ValidatedList(self.normal_list)
        self.mock_valideted_list2 = validatedList.ValidatedList()
        
        # now append something to the second list which is not initialized with
        # a list
        self.mock_valideted_list2.append(1)
    
    
    
    #----------------------------------------------------------------------
    def test___init__(self):
        """testing initialization
        """
        
        test_value = "a string value"
        
        mock_valideted_list3 = validatedList.ValidatedList()
        mock_valideted_list3.append(test_value)
        
        # check if the __type__ is set to str
        self.assertEquals(mock_valideted_list3.__type__, type(test_value))
        
        # check if the __type_as_str__ is set to str
        self.assertEquals(mock_valideted_list3.__type_as_str__, "str")
    
    
    
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
            1,
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
            1,
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
        """testing __iadd__ functionality
        """
        
        test_value = [1032, 12304]
        self.mock_valideted_list1 += test_value
        self.assertEquals(self.mock_valideted_list1[-2:], test_value)
    
    
    