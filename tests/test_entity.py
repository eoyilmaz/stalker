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
from stalker.models import entity






########################################################################
class EntityTest(unittest.TestCase):
    """tests the entity class
    """
    
    
    
    #----------------------------------------------------------------------
    def test_created_by(self):
        """testing the created_by attribute
        """
        
        # the created_by attribute should be an instance of User class
        # it can not be empty (the first created user going to have some
        # problems if we dont allow empty users)
        # 
        
        self.fail("tests are not implemented yet!")
    
    
    
    #----------------------------------------------------------------------
    def test_date_created(self):
        """testing the date_created attribute
        """
        
        # the date_created attribute should be an instance of datetime.datetime
        
        self.fail("tests are not implemented yet!")
    
    
    
    
    
    