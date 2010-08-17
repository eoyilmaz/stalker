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
class TestStatusBase(unittest.TestCase):
    """tests the status class
    """
    
    
    
    #----------------------------------------------------------------------
    def test_name(self):
        """test the name attribute
        """
        
        #----------------------------------------------------------------------
        # the name should be a str or unicode
        self.assertRaises(ValueError, status.StatusBase, 1, '1')
        # check the property
        aStatusBase = status.StatusBase('Complete', 'Cmpl')
        self.assertRaises(ValueError, setattr, aStatusBase, 'name', 1)
        
        
        #----------------------------------------------------------------------
        # the name could not be an empty string
        self.assertRaises(ValueError, status.StatusBase, '', 'Cmp')
        # check the property
        aStatusBase = status.StatusBase('Complete', 'Cmpl')
        self.assertRaises(ValueError, setattr, aStatusBase, 'name', '')
        
        
        #----------------------------------------------------------------------
        # the first letter of the name should be in upper case and the other
        # letters should be in lower case
        statusName = 'test'
        aStatusBase = status.StatusBase(statusName, 'tst')
        self.assertEqual(statusName.title(), aStatusBase.name)
        
        # check the property
        aStatusBase = status.StatusBase('Complete', 'Cmpl')
        aStatusBase.name = statusName
        self.assertEqual(statusName.title(), aStatusBase.name)
        
        #----------------------------------------------------------------------
        # the first letter of the name could not be an integer
        statusName = '1test'
        self.assertRaises(ValueError, status.StatusBase, statusName, \
                           statusName)
        
        # check the property
        aStatusBase = status.StatusBase('Complete', 'Cmpl')
        self.assertRaises(ValueError, setattr, aStatusBase, 'name', statusName)
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation(self):
        """tests the abbreviation attribute
        """
        
        #----------------------------------------------------------------------
        # the abbreviation should be a str or unicode
        self.assertRaises(ValueError, status.StatusBase, 'Complete', 1 )
        
        # check the property
        aStatusBase = status.StatusBase( 'Complete', 'Cmlt' )
        self.assertRaises(ValueError, setattr, aStatusBase, 'abbreviation', 1)
        
        #----------------------------------------------------------------------
        # the abbreviation can not be an empty string
        self.assertRaises(ValueError, status.StatusBase, 'Complete', '')
        
        # check the property
        aStatusBase = status.StatusBase( 'Complete', 'Cmlt' )
        self.assertRaises(ValueError, setattr, aStatusBase, 'abbreviation', '')