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
from stalker.models import unit






########################################################################
class UnitTest(unittest.TestCase):
    """tests Unit base class
    """
    
    
    #----------------------------------------------------------------------
    def test_init_arguments(self):
        # the initialization should have the attributes below:
        # id, name, shortName
        
        # these all should raise ValueErrors
        
        # empty arguments
        self.assertRaises(ValueError, unit.Unit, '', '')
        
        # this should work
        aUnit = unit.Unit('meter', 'm')
    
    
    
    #----------------------------------------------------------------------
    def test_name(self):
        # the unit should always have a name
        self.assertRaises(ValueError, unit.Unit, '', '')
        
        # the name should be string type
        aUnit = unit.Unit('meter', 'm')
        
        self.assertRaises(ValueError, setattr, aUnit, "name", 1)
    
    
    
    #----------------------------------------------------------------------
    def test_abbriviation(self):
        # the unit should always have a shortName
        
        # the abbreviation shouldn't be empty
        self.assertRaises(ValueError, unit.Unit, 'meter', '')
        
        # the abbreviation shouldn't be anything other than a string or unicode
        self.assertRaises(ValueError, unit.Unit, 'meter', 1)
        
        # assigning values to abbreviation should also return ValueErrors
        aUnit = unit.Unit('meter', 'm')
        self.assertRaises(ValueError, setattr, aUnit, 'abbreviation', '')
        self.assertRaises(ValueError, setattr, aUnit, 'abbreviation', 1)






########################################################################
class ConvertableUnitTest(unittest.TestCase):
    """tests the ConveratableUnit class
    """
    
    
    
    #----------------------------------------------------------------------
    def test_conversionRatio(self):
        
        # shouldn't be zero
        self.assertRaises(ValueError, unit.ConvertableUnit, 'meter', 'm', 0)
        
        # shouldn't be below zero
        self.assertRaises(ValueError, unit.ConvertableUnit, 'meter', 'm', -1)
        
        # should only accept floats
        self.assertRaises(ValueError, unit.ConvertableUnit, 'meter', 'm', 'a string')
        self.assertRaises(ValueError, unit.ConvertableUnit, 'meter', 'm', u'a unicode')






########################################################################
class TimeTest(unittest.TestCase):
    """tests the models/unit/Time class
    """
    
    #----------------------------------------------------------------------
    def testFps(self):
        # the fps shouldn't be zero or negative
        self.assertRaises(ValueError, unit.Time, 'PAL', 'PAL', 0)
        self.assertRaises(ValueError, unit.Time, 'NTSC', 'NTSC', -20 )
        self.assertRaises(ValueError, unit.Time, '', '', -20 )
        self.assertRaises(ValueError, unit.Time, 'PAL', '', -20 )
        self.assertRaises(ValueError, unit.Time, '', 'PAL', -20 )
        
        