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
        """testing the init arguments
        """
        # the initialization should have the attributes below:
        # id, name, shortName
        
        # these all should raise ValueErrors
        
        # empty arguments
        self.assertRaises(ValueError, unit.Unit, '', '')
        
        # this should work
        aUnit = unit.Unit('meter', 'm')
    
    
    
    #----------------------------------------------------------------------
    def test_name_empty(self):
        """testing the name attribute against being empty
        """
        # the unit should always have a name
        self.assertRaises(ValueError, unit.Unit, '', '')
    
    
    
    #----------------------------------------------------------------------
    def test_name_attribute_str_unicedo(self):
        """testing the name attribute not being string or unicode
        """
        # the name attribute should only accept string or unicode
        self.assertRaises(ValueError, unit.Unit, 1, 'm')
        self.assertRaises(ValueError, unit.Unit, [], 'm')
        self.assertRaises(ValueError, unit.Unit, {}, 'm')
    
    
    
    #----------------------------------------------------------------------
    def test_name_property_str_unicode(self):
        """testing the name attribute against being string or unicode
        """
        # the name should be string type
        aUnit = unit.Unit('meter', 'm')
        self.assertRaises(ValueError, setattr, aUnit, "name", 1)
    
    
    
    #----------------------------------------------------------------------
    def test_name_property(self):
        """testing the name property
        """
        # test name property
        name = 'meter'
        aUnit = unit.Unit(name, 'm')
        self.assertEquals( aUnit.name, name)
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation_empty(self):
        """testing the abbreviation attribute being empty
        """
        # the abbreviation shouldn't be empty
        self.assertRaises(ValueError, unit.Unit, 'meter', '')
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation_str_unicode(self):
        """testing the abbreviation attribute string or unicode
        """
        # the abbreviation shouldn't be anything other than a string or unicode
        self.assertRaises(ValueError, unit.Unit, 'meter', 1)
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation_property_str_unicode(self):
        """testing the abbreviation property string or unicode
        """
        # assigning values to abbreviation should also return ValueErrors
        aUnit = unit.Unit('meter', 'm')
        self.assertRaises(ValueError, setattr, aUnit, 'abbreviation', '')
        self.assertRaises(ValueError, setattr, aUnit, 'abbreviation', 1)
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation_property(self):
        """testing the abbreviation property
        """
        # test abbreviation property
        name = 'meter'
        abbreviation = 'm'
        aUnit = unit.Unit(name, abbreviation)
        
        self.assertEquals(aUnit.abbreviation, abbreviation)






########################################################################
class ConvertableUnitTest(unittest.TestCase):
    """tests the ConveratableUnit class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setting up some default values
        """
        self.name = 'meter'
        self.abbr = 'm'
        self.convRatio = 100
    
    
    
    #----------------------------------------------------------------------
    def test_conversionRatio_zero(self):
        """testing the conversionRatio attribute being zero
        """
        # shouldn't be zero
        self.assertRaises(ValueError, unit.ConvertableUnit, self.name,
                          self.abbr, 0)
    
    
    
    #----------------------------------------------------------------------
    def test_conversionRatio_negative(self):
        """testing the conversionRatio attribute being negative
        """
        
        # shouldn't be negative
        self.assertRaises(ValueError, unit.ConvertableUnit, self.name,
                          self.abbr, -1)
    
    
    
    #----------------------------------------------------------------------
    def test_conversionRatio_not_float(self):
        """testing the conversionRatio attribute against not initialized as
        float
        """
        
        # should only accept floats
        self.assertRaises(ValueError,
                          unit.ConvertableUnit,
                          self.name, self.abbr, 'a string')
        
        self.assertRaises(ValueError,
                          unit.ConvertableUnit,
                          self.name, self.abbr, u'a unicode')
    
    
    
    #----------------------------------------------------------------------
    def test_conversionRatio_float(self):
        """testing the conversionRatio attribute if set correctly as float
        """
        
        # check if the conversion ratio is instance of float
        aConvUnit = unit.ConvertableUnit(self.name, self.abbr, self.convRatio)
        self.assertTrue(isinstance(aConvUnit.conversionRatio, float))
    
    
    
    #----------------------------------------------------------------------
    def test_conversionRatio_property(self):
        """testing the conversionRatio property
        """
        
        # check if the conversion ratio is assigned correctly
        aConvUnit = unit.ConvertableUnit(self.name, self.abbr, self.convRatio)
        
        newConvRatio = 1000.0
        aConvUnit.conversionRatio = newConvRatio
        self.assertTrue(aConvUnit.conversionRatio, newConvRatio)






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
        
        # check if the fps is float
        name = 'PAL'
        abbr = 'PAL'
        convRatio = 25
        aTimeUnit = unit.Time( name, abbr, convRatio)
        self.assertTrue(isinstance(aTimeUnit.fps, float))
        
        # check if the fps is assigned correctly
        newFPS = 30.0
        aTimeUnit.fps = newFPS
        self.assertEquals(aTimeUnit.fps, newFPS)