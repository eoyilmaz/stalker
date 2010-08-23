#-*- coding: utf-8 -*-
"""
Copyright (C) 2010  Erkan Ozgur Yilmaz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""



import unittest
from stalker.models import status



########################################################################
class TestStatus(unittest.TestCase):
    """tests the status class
    """
    
    
    
    #----------------------------------------------------------------------
    def test_name(self):
        """test the name attribute
        """
        
        #----------------------------------------------------------------------
        # the name should be a str or unicode
        self.assertRaises(ValueError, status.Status, 1, '1')
        # check the property
        aStatus = status.Status('Complete', 'Cmpl')
        self.assertRaises(ValueError, setattr, aStatus, 'name', 1)
        
        
        #----------------------------------------------------------------------
        # the name could not be an empty string
        self.assertRaises(ValueError, status.Status, '', 'Cmp')
        # check the property
        aStatus = status.Status('Complete', 'Cmpl')
        self.assertRaises(ValueError, setattr, aStatus, 'name', '')
        
        
        #----------------------------------------------------------------------
        # the first letter of the name should be in upper case and the other
        # letters should be in lower case
        statusName = 'test'
        aStatus = status.Status(statusName, 'tst')
        self.assertEqual(statusName.title(), aStatus.name)
        
        # check the property
        aStatus = status.Status('Complete', 'Cmpl')
        aStatus.name = statusName
        self.assertEqual(statusName.title(), aStatus.name)
        
        #----------------------------------------------------------------------
        # the first letter of the name could not be an integer
        statusName = '1test'
        self.assertRaises(ValueError, status.Status, statusName, \
                           statusName)
        
        # check the property
        aStatus = status.Status('Complete', 'Cmpl')
        self.assertRaises(ValueError, setattr, aStatus, 'name', statusName)
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation(self):
        """tests the abbreviation attribute
        """
        
        #----------------------------------------------------------------------
        # the abbreviation should be a str or unicode
        self.assertRaises(ValueError, status.Status, 'Complete', 1)
        
        # check the property
        aStatus = status.Status('Complete', 'Cmlt')
        self.assertRaises(ValueError, setattr, aStatus, 'abbreviation', 1)
        
        #----------------------------------------------------------------------
        # the abbreviation can not be an empty string
        self.assertRaises(ValueError, status.Status, 'Complete', '')
        
        # check the property
        aStatus = status.Status('Complete', 'Cmlt')
        self.assertRaises(ValueError, setattr, aStatus, 'abbreviation', '')
        
        #----------------------------------------------------------------------
        # check if the abbreviation is get correctly
        name = 'Complete'
        abbr = 'Cmplt'
        aStatus = status.Status(name, abbr)
        self.assertEquals( aStatus.abbreviation, abbr)






########################################################################
class StatusListTest(unittest.TestCase):
    """tests the StatusList class
    """
    
    
    
    #----------------------------------------------------------------------
    def test_name(self):
        """tests the name attribute
        """
        
        # proper values
        listName = 'aStatusList'
        aStatusList = [
            status.Status('Not Available', 'N/A'),
            status.Status('Waiting To Start', 'WStrt'),
            status.Status('Started', 'Strt'),
            status.Status('Waiting For Approve', 'WAppr'),
            status.Status('Approved', 'Appr'),
            status.Status('Finished', 'Fnsh'),
            status.Status('On Hold', 'OH'),
            ]
        
        #----------------------------------------------------------------------
        # the name couldn't be empty
        self.assertRaises(ValueError, status.StatusList, '', aStatusList)
        
        # test the name property
        aStatusList_obj = status.StatusList(listName, aStatusList)
        self.assertRaises(ValueError, setattr, aStatusList_obj, 'name', '')
        
        #----------------------------------------------------------------------
        # the name should be a string or unicode
        self.assertRaises(ValueError, status.StatusList, 1, aStatusList)
        
        aStatusList_obj = status.StatusList(listName, aStatusList)
        self.assertRaises(ValueError, setattr, aStatusList_obj, 'name', 1)
        self.assertRaises(ValueError, setattr, aStatusList_obj, 'name', [])
        self.assertRaises(ValueError, setattr, aStatusList_obj, 'name', {})
        
        #----------------------------------------------------------------------
        # it should be property
        newListName = 'new status list name'
        
        # check if we can properly assign new values to name property
        aStatusList_obj = status.StatusList(listName, aStatusList)
        aStatusList_obj.name = newListName
        self.assertEquals(aStatusList_obj.name, newListName)
    
    
    
    #----------------------------------------------------------------------
    def test_statusList(self):
        """tests the statuses list attribute
        """
        
        # proper values
        statusListName = 'aStatusList'
        aStatusList = [
            status.Status('Not Available', 'N/A'),
            status.Status('Waiting To Start', 'WStrt'),
            status.Status('Started', 'Strt'),
            status.Status('Waiting For Approve', 'WAppr'),
            status.Status('Approved', 'Appr'),
            status.Status('Finished', 'Fnsh'),
            status.Status('On Hold', 'OH'),
            ]
        
        
        # the statuses attribute should be a list of statuses
        # can be empty?
        #
        
        #----------------------------------------------------------------------
        # it should only accept lists of statuses
        self.assertRaises(ValueError,
                          status.StatusList, statusListName, 'a str')
        self.assertRaises(ValueError,
                          status.StatusList, statusListName, {})
        self.assertRaises(ValueError,
                          status.StatusList, statusListName, 1)
        
        # check the property
        
        
        
        #----------------------------------------------------------------------
        # the list couldn't be empty
        self.assertRaises(ValueError,
                          status.StatusList, statusListName, [])
        
        #----------------------------------------------------------------------
        # every element should be an object derived from Status
        aFakeStatusList = [1, 2, 'a string', u'a unicode', 4.5]
        
        self.assertRaises(ValueError,
                          status.StatusList, statusListName, aFakeStatusList)
        
        #----------------------------------------------------------------------
        # it should be a property so check if it sets property correctly
        aStatusList_obj = status.StatusList( statusListName, aStatusList)
        newListOfStatutes = [ status.Status('New Status', 'abbr') ]
        aStatusList_obj.statuses = newListOfStatutes
        self.assertEquals( aStatusList_obj.statuses, newListOfStatutes)
        
        