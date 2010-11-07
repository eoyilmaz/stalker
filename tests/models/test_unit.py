#-*- coding: utf-8 -*-



import unittest
from stalker.models import unit






########################################################################
class UnitTest(unittest.TestCase):
    """tests Unit base class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setting up some default values
        """
        self.name = 'Meter'
        self.abbr = 'm'
        self.conv_ratio = 100
    
    
    
    ##----------------------------------------------------------------------
    #def test_init_arguments(self):
        #"""testing the init arguments
        #"""
        ## the initialization should have the attributes below:
        ## id, name, short_name
        
        ## these all should raise ValueErrors
        
        ## empty arguments
        #self.assertRaises(ValueError, unit.Unit, '', '')
        
        ## this should work
        #a_unit = unit.Unit('Meter', 'm', 100.0)
    
    
    
    #----------------------------------------------------------------------
    def test_name_empty(self):
        """testing the name attribute against being empty
        """
        # the unit should always have a name
        self.assertRaises(
            ValueError,
            unit.Unit,
            name='',
            abbreviation=self.abbr
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_attribute_str_unicedo(self):
        """testing the name attribute not being string or unicode
        """
        # the name attribute should only accept string or unicode
        self.assertRaises(
            ValueError,
            unit.Unit,
            name=1,
            abbreviation='m'
        )
        
        self.assertRaises(
            ValueError,
            unit.Unit,
            name=[],
            abbreviation='m'
        )
        
        self.assertRaises(
            ValueError,
            unit.Unit,
            name={},
            abbreviation='m'
        )
    
    
    
    #----------------------------------------------------------------------
    def test_name_property_str_unicode(self):
        """testing the name attribute against being string or unicode
        """
        # the name should be string type
        a_unit = unit.Unit(name='Meter', abbreviation='m')
        self.assertRaises(ValueError, setattr, a_unit, "name", 1)
    
    
    
    #----------------------------------------------------------------------
    def test_name_property(self):
        """testing the name property
        """
        # test name property
        name = 'Meter'
        a_unit = unit.Unit(name=name, abbreviation='m')
        self.assertEquals( a_unit.name, name)
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation_empty(self):
        """testing the abbreviation attribute being empty
        """
        # the abbreviation shouldn't be empty
        self.assertRaises(
            ValueError,
            unit.Unit,
            name='Meter',
            abbreviation=''
        )
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation_str_unicode(self):
        """testing the abbreviation attribute string or unicode
        """
        # the abbreviation shouldn't be anything other than a string or
        # unicode
        self.assertRaises(
            ValueError,
            unit.Unit,
            name='Meter',
            abbreviation=1
        )
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation_property_str_unicode(self):
        """testing the abbreviation property string or unicode
        """
        # assigning values to abbreviation should also return ValueErrors
        a_unit = unit.Unit(name='Meter', abbreviation='m')
        self.assertRaises(ValueError, setattr, a_unit, 'abbreviation', '')
        self.assertRaises(ValueError, setattr, a_unit, 'abbreviation', 1)
    
    
    
    #----------------------------------------------------------------------
    def test_abbreviation_property(self):
        """testing the abbreviation property
        """
        # test abbreviation property
        name = 'Meter'
        abbreviation = 'm'
        a_unit = unit.Unit(name=name, abbreviation=abbreviation)
        
        self.assertEquals(a_unit.abbreviation, abbreviation)
    
    
    
    #----------------------------------------------------------------------
    def test_conversion_ratio_zero(self):
        """testing the conversion_ratio attribute being zero
        """
        # shouldn't be zero
        self.assertRaises(
            ValueError,
            unit.Unit,
            name=self.name,
            abbreviation=self.abbr,
            conversion_ratio=0
        )
    
    
    
    #----------------------------------------------------------------------
    def test_conversion_ratio_negative(self):
        """testing the conversion_ratio attribute being negative
        """
        
        # shouldn't be negative
        self.assertRaises(
            ValueError,
            unit.Unit,
            name=self.name,
            abbreviation=self.abbr,
            conversion_ratio=-1
        )
    
    
    
    #----------------------------------------------------------------------
    def test_conversion_ratio_not_float(self):
        """testing the conversion_ratio attribute against not initialized as
        float
        """
        
        # should only accept floats
        self.assertRaises(
            ValueError,
            unit.Unit,
            name=self.name,
            abbreviation=self.abbr,
            conversion_ratio='a string'
        )
        
        self.assertRaises(
            ValueError,
            unit.Unit,
            name=self.name,
            abbreviation=self.abbr,
            conversion_ratio=u'a unicode'
        )
    
    
    
    #----------------------------------------------------------------------
    def test_conversion_ratio_float(self):
        """testing the conversion_ratio attribute if set correctly as float
        """
        
        # check if the conversion ratio is instance of float
        a_conv_unit = unit.Unit(
            name=self.name,
            abbreviation=self.abbr,
            conversion_ratio=self.conv_ratio
        )
        
        self.assertTrue(isinstance(a_conv_unit.conversion_ratio, float))
    
    
    
    #----------------------------------------------------------------------
    def test_conversion_ratio_property(self):
        """testing the conversion_ratio property
        """
        
        # check if the conversion ratio is assigned correctly
        a_conv_unit = unit.Unit(
            name=self.name,
            abbreviation=self.abbr,
            conversion_ratio=self.conv_ratio
        )
        
        new_conv_ratio = 1000.0
        a_conv_unit.conversion_ratio = new_conv_ratio
        self.assertTrue(a_conv_unit.conversion_ratio, new_conv_ratio)













########################################################################
class TimeTest(unittest.TestCase):
    """tests the models/unit/Time class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup some values
        """
        self.name = 'PAL'
        self.abbr = 'PAL'
        self.fps = 25.0
    
    
    
    #----------------------------------------------------------------------
    def test_fps_zero(self):
        """testing the fps attribute against being zero
        """
        # the fps shouldn't be zero
        self.assertRaises(
            ValueError,
            unit.Time,
            name=self.name,
            abbreviation=self.abbr,
            fps=0
        )
    
    
    
    #----------------------------------------------------------------------
    def test_fps_negative(self):
        """testing the fps attribute against being negative
        """
        # the fps shouldn't be negative
        self.assertRaises(
            ValueError,
            unit.Time,
            name=self.name,
            abbreviation=self.abbr,
            fps=-20
        )
    
    
    
    #----------------------------------------------------------------------
    def test_fps_float(self):
        """testing the fps attribute against being float
        """
        # check if the fps is float
        int_fps = 25
        a_time_unit = unit.Time(
            name=self.name,
            abbreviation=self.abbr,
            fps=int_fps
        )
        
        self.assertTrue(isinstance(a_time_unit.fps, float))
    
    
    
    #----------------------------------------------------------------------
    def test_fps_property(self):
        """testing the fps property
        """
        # check if the fps is assigned correctly
        newFPS = 30.0
        a_time_unit = unit.Time(
            name=self.name,
            abbreviation=self.abbr,
            fps=self.fps
        )
        a_time_unit.fps = newFPS
        self.assertEquals(a_time_unit.fps, newFPS)