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
from stalker.models import tag






########################################################################
class TagTest(unittest.TestCase):
    """tests the Tag class
    """
    
    
    
    #----------------------------------------------------------------------
    def test_name(self):
        """tests the name attribute
        """
        
        #----------------------------------------------------------------------
        # the name should be a string or unicode
        newName = 1
        self.assertRaises(ValueError, tag.Tag, newName)
        # check the name property
        name = 'a new tag'
        aTag = tag.Tag(name)
        self.assertRaises(ValueError, setattr, aTag, 'name', newName)
        
        #----------------------------------------------------------------------
        # the name can not be empty
        newName = ''
        self.assertRaises(ValueError, tag.Tag, newName)
        # check the name property
        name = 'a new tag'
        aTag = tag.Tag(name)
        self.assertRaises(ValueError, setattr, aTag, 'name', newName)
        
        #----------------------------------------------------------------------
        # test if we get the name attribute correctly by using the name
        # property
        name = 'a tag'
        aTag = tag.Tag(name)
        self.assertEquals(aTag.name, name)
        