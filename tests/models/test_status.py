# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest
from stalker import Entity, Status, Color
from stalker.conf import defaults

class ColorTest(unittest.TestCase):
    """tests the stalker.models.status.Color class
    """
    
    def setUp(self):
        """set up the test
        """
        self.kwargs = {
            "r": 100,
            "g": 255,
            "b": 10
        }
        
        self.test_color = Color(**self.kwargs)
    
    def test_r_argument_is_skipped(self):
        """testing if the r attribute is going to be 0 when the r argument is
        skipped
        """
        self.kwargs.pop('r')
        new_color = Color(**self.kwargs)
        self.assertEqual(0, new_color.r)
    
    def test_r_argument_is_None(self):
        """testing if the r attribute is going to be 0 when the r argument is
        None
        """
        self.kwargs['r'] = None
        new_color = Color(**self.kwargs)
        self.assertEqual(0, new_color.r)
    
    def test_r_attribute_is_None(self):
        """testing if the r attribute is going to be 0 when it is set to None
        """
        self.test_color.r = None
        self.assertEqual(0, self.test_color.r)
    
    def test_r_argument_is_not_an_integer(self):
        """testing if a TypeError will be raised when the r argument is not an
        int
        """
        self.kwargs['r'] = 'asdfas'
        self.assertRaises(TypeError, Color, **self.kwargs)
    
    def test_r_attribute_is_not_an_integer(self):
        """testing if a TypeError will be raised when the r attribute is not
        set to an integer
        """
        self.assertRaises(TypeError, setattr, self.test_color, 'r', 'swefra')
    
    def test_r_argument_is_negative(self):
        """testing if the r attribute will be clamped to 0 when the r argument
        is negative
        """
        self.kwargs['r'] = -123
        new_color = Color(**self.kwargs)
        self.assertEqual(0, new_color.r)
    
    def test_r_attribute_is_negative(self):
        """testing if the r attribute will be clamped to 0 when it is set to a
        negative value
        """
        self.test_color.r = -32
        self.assertEqual(0, self.test_color.r)
    
    def test_r_argument_is_bigger_than_255(self):
        """testing if the r attribute will be clamped to 255 if the r argument
        is bigger than 255
        """
        self.kwargs['r'] = 256
        new_color = Color(**self.kwargs)
        self.assertEqual(255, new_color.r)
    
    def test_r_attribute_is_bigger_than_255(self):
        """testing if the r attribute is clamped to 255 if it is bigger than
        255
        """
        self.test_color.r = 256
        self.assertEqual(255, self.test_color.r)
    
    def test_g_argument_is_skipped(self):
        """testing if the g attribute is going to be 0 when the g argument is
        skipped
        """
        self.kwargs.pop('g')
        new_color = Color(**self.kwargs)
        self.assertEqual(0, new_color.g)
    
    def test_g_argument_is_None(self):
        """testing if the g attribute is going to be 0 when the g argument is
        None
        """
        self.kwargs['g'] = None
        new_color = Color(**self.kwargs)
        self.assertEqual(0, new_color.g)
    
    def test_g_attribute_is_None(self):
        """testing if the g attribute is going to be 0 when it is set to None
        """
        self.test_color.g = None
        self.assertEqual(0, self.test_color.g)
    
    def test_g_argument_is_not_an_integer(self):
        """testing if a TypeError will be raised when the g argument is not an
        int
        """
        self.kwargs['g'] = 'asdfas'
        self.assertRaises(TypeError, Color, **self.kwargs)
    
    def test_g_attribute_is_not_an_integer(self):
        """testing if a TypeError will be raised when the g attribute is not
        set to an integer
        """
        self.assertRaises(TypeError, setattr, self.test_color, 'g', 'swefra')
    
    def test_g_argument_is_negative(self):
        """testing if the g attribute will be clamped to 0 when the g argument
        is negative
        """
        self.kwargs['g'] = -123
        new_color = Color(**self.kwargs)
        self.assertEqual(0, new_color.g)
    
    def test_g_attribute_is_negative(self):
        """testing if the g attribute will be clamped to 0 when it is set to a
        negative value
        """
        self.test_color.g = -32
        self.assertEqual(0, self.test_color.g)
    
    def test_g_argument_is_bigger_than_255(self):
        """testing if the g attribute will be clamped to 255 if the g argument
        is bigger than 255
        """
        self.kwargs['g'] = 256
        new_color = Color(**self.kwargs)
        self.assertEqual(255, new_color.g)
    
    def test_g_attribute_is_bigger_than_255(self):
        """testing if the g attribute is clamped to 255 if it is bigger than
        255
        """
        self.test_color.g = 256
        self.assertEqual(255, self.test_color.g)
    
    def test_b_argument_is_skipped(self):
        """testing if the b attribute is going to be 0 when the b argument is
        skipped
        """
        self.kwargs.pop('b')
        new_color = Color(**self.kwargs)
        self.assertEqual(0, new_color.b)
    
    def test_b_argument_is_None(self):
        """testing if the b attribute is going to be 0 when the b argument is
        None
        """
        self.kwargs['b'] = None
        new_color = Color(**self.kwargs)
        self.assertEqual(0, new_color.b)
    
    def test_b_attribute_is_None(self):
        """testing if the b attribute is going to be 0 when it is set to None
        """
        self.test_color.b = None
        self.assertEqual(0, self.test_color.b)
    
    def test_b_argument_is_not_an_integer(self):
        """testing if a TypeError will be raised when the b argument is not an
        int
        """
        self.kwargs['b'] = 'asdfas'
        self.assertRaises(TypeError, Color, **self.kwargs)
    
    def test_b_attribute_is_not_an_integer(self):
        """testing if a TypeError will be raised when the b attribute is not
        set to an integer
        """
        self.assertRaises(TypeError, setattr, self.test_color, 'b', 'swefra')
    
    def test_b_argument_is_negative(self):
        """testing if the b attribute will be clamped to 0 when the b argument
        is negative
        """
        self.kwargs['b'] = -123
        new_color = Color(**self.kwargs)
        self.assertEqual(0, new_color.b)
    
    def test_b_attribute_is_negative(self):
        """testing if the b attribute will be clamped to 0 when it is set to a
        negative value
        """
        self.test_color.b = -32
        self.assertEqual(0, self.test_color.b)
    
    def test_b_argument_is_bigger_than_255(self):
        """testing if the b attribute will be clamped to 255 if the b argument
        is bigger than 255
        """
        self.kwargs['b'] = 256
        new_color = Color(**self.kwargs)
        self.assertEqual(255, new_color.b)
    
    def test_b_attribute_is_bigger_than_255(self):
        """testing if the b attribute is clamped to 255 if it is bigger than
        255
        """
        self.test_color.b = 256
        self.assertEqual(255, self.test_color.b)
 
class StatusTest(unittest.TestCase):
    """tests the stalker.models.status.Status class
    """
    
    def setUp(self):
        """setup the test
        """
        self.kwargs = {
            'name': 'Complete',
            'description': 'use this when the object is complete',
            'code': 'CMPLT',
            'fg_color': Color(0, 0, 0),
            'bg_color': Color(0, 255, 0),
        }
        
        # create an entity object with same kwargs for __eq__ and __ne__ tests
        # (it should return False for __eq__ and True for __ne__ for same
        # kwargs)
        self.entity1 = Entity(**self.kwargs)

    def test_equality(self):
        """testing equality of two statuses
        """
        status1 = Status(**self.kwargs)
        status2 = Status(**self.kwargs)

        self.kwargs["name"] = "Work In Progress"
        self.kwargs["description"] = "use this when the object is still in \
        progress"
        self.kwargs["code"] = "WIP"

        status3 = Status(**self.kwargs)

        self.assertTrue(status1 == status2)
        self.assertFalse(status1 == status3)
        self.assertFalse(status1 == self.entity1)

    def test_status_and_string_equality_in_status_name(self):
        """testing a status can be compared with a string and returns True if
        the string matches the name and vice versa
        """
        a_status = Status(**self.kwargs)
        self.assertTrue(a_status == self.kwargs["name"])
        self.assertTrue(a_status == self.kwargs["name"].lower())
        self.assertTrue(a_status == self.kwargs["name"].upper())
        self.assertTrue(a_status == unicode(self.kwargs["name"]))
        self.assertTrue(a_status == unicode(self.kwargs["name"].lower()))
        self.assertTrue(a_status == unicode(self.kwargs["name"].upper()))
        self.assertFalse(a_status == "another name")
        self.assertFalse(a_status == u"another name")

    def test_status_and_string_equality_in_status_code(self):
        """testing a status can be compared with a string and returns True if
        the string matches the code and vice versa
        """
        a_status = Status(**self.kwargs)
        self.assertTrue(a_status == self.kwargs["code"])
        self.assertTrue(a_status == self.kwargs["code"].lower())
        self.assertTrue(a_status == self.kwargs["code"].upper())
        self.assertTrue(a_status == unicode(self.kwargs["code"]))
        self.assertTrue(a_status == unicode(self.kwargs["code"].lower()))
        self.assertTrue(a_status == unicode(self.kwargs["code"].upper()))

    def test_inequality(self):
        """testing inequality of two statuses
        """
        status1 = Status(**self.kwargs)
        status2 = Status(**self.kwargs)

        self.kwargs["name"] = "Work In Progress"
        self.kwargs["description"] = "use this when the object is still in \
        progress"
        self.kwargs["code"] = "WIP"

        status3 = Status(**self.kwargs)

        self.assertFalse(status1 != status2)
        self.assertTrue(status1 != status3)
        self.assertTrue(status1 != self.entity1)

    def test_status_and_string_inequality_in_status_name(self):
        """testing a status can be compared with a string and returns False if
        the string matches the name and vice versa
        """
        a_status = Status(**self.kwargs)
        self.assertFalse(a_status != self.kwargs["name"])
        self.assertFalse(a_status != self.kwargs["name"].lower())
        self.assertFalse(a_status != self.kwargs["name"].upper())
        self.assertFalse(a_status != unicode(self.kwargs["name"]))
        self.assertFalse(a_status != unicode(self.kwargs["name"].lower()))
        self.assertFalse(a_status != unicode(self.kwargs["name"].upper()))
        self.assertTrue(a_status != "another name")
        self.assertTrue(a_status != u"another name")

    def test_status_and_string_inequality_in_status_code(self):
        """testing a status can be compared with a string and returns False if
        the string matches the code and vice versa
        """
        a_status = Status(**self.kwargs)
        self.assertFalse(a_status != self.kwargs["code"])
        self.assertFalse(a_status != self.kwargs["code"].lower())
        self.assertFalse(a_status != self.kwargs["code"].upper())
        self.assertFalse(a_status != unicode(self.kwargs["code"]))
        self.assertFalse(a_status != unicode(self.kwargs["code"].lower()))
        self.assertFalse(a_status != unicode(self.kwargs["code"].upper()))
    
    def test_bg_color_argument_is_skipped(self):
        """testing if the bg_color attribute will be filled with the default
        color when the bg_color argument is skipped
        """
        self.kwargs.pop('bg_color')
        new_status = Status(**self.kwargs)
        self.assertEqual(
            Color(*defaults.DEFAULT_BG_COLOR),
            new_status.bg_color
        )
    
    def test_bg_color_argument_is_None(self):
        """testing if the bg_color attribute will be filled with the default
        color when the bg_color argument is None
        """
        self.kwargs['bg_color'] = None
        new_status = Status(**self.kwargs)
        self.assertEqual(
            Color(*defaults.DEFAULT_BG_COLOR),
            new_status.bg_color
        )
    
    def test_bg_color_argument_is_not_a_Color_instance(self):
        """testing if a TypeError will be raised when the bg_color argument is
        not a stalker.models.status.Color instance
        """
        self.kwargs['bg_color'] = ["2342", 53, 33 ]
        self.assertRaises(TypeError, Status, **self.kwargs)
    
    def test_bg_color_attribute_is_None(self):
        """testing if the bg_color attribute is set to None will reset the
        color to default color
        """
        new_status = Status(**self.kwargs)
        new_status.bg_color = None
        self.assertEqual(
            Color(*defaults.DEFAULT_BG_COLOR),
            new_status.bg_color
        )
    
    def test_bg_color_attribute_is_not_a_Color_instance(self):
        """testing if a TypeError will be raised when the bg_color attribute is
        not a stalker.models.status.Color instance
        """
        new_status = Status(**self.kwargs)
        self.assertRaises(TypeError, setattr, new_status, 'bg_color',
            ["asdf", 65, 25])
    
    def test_bg_color_argument_is_working_properly(self):
        """testing if the bg_color argument is working properly by setting its
        value its value to the bg_color attribute
        """
        self.kwargs['bg_color'] = Color(15, 25, 35)
        new_status = Status(**self.kwargs)
        self.assertEqual(self.kwargs['bg_color'], new_status.bg_color)
    
    def test_bg_color_attribute_is_working_properly(self):
        """testing if the bg_color attribute is working properly
        """
        new_status = Status(**self.kwargs)
        test_color = Color(15, 25, 35)
        new_status.bg_color = test_color
        self.assertEqual(test_color, new_status.bg_color)
    
    def test_fg_color_argument_is_skipped(self):
        """testing if the fg_color attribute will be filled with the default
        color when the fg_color argument is skipped
        """
        self.kwargs.pop('fg_color')
        new_status = Status(**self.kwargs)
        self.assertEqual(
            Color(*defaults.DEFAULT_FG_COLOR),
            new_status.fg_color
        )
    
    def test_fg_color_argument_is_None(self):
        """testing if the fg_color attribute will be filled with the default
        color when the fg_color argument is None
        """
        self.kwargs['fg_color'] = None
        new_status = Status(**self.kwargs)
        self.assertEqual(
            Color(*defaults.DEFAULT_FG_COLOR),
            new_status.fg_color
        )
    
    def test_fg_color_argument_is_not_a_Color_instance(self):
        """testing if a TypeError will be raised when the fg_color argument is
        not a stalker.models.status.Color instance
        """
        self.kwargs['fg_color'] = ["2342", 53, 33 ]
        self.assertRaises(TypeError, Status, **self.kwargs)
    
    def test_fg_color_attribute_is_None(self):
        """testing if the fg_color attribute is set to None will reset the
        color to default color
        """
        new_status = Status(**self.kwargs)
        new_status.fg_color = None
        self.assertEqual(
            Color(*defaults.DEFAULT_FG_COLOR),
            new_status.fg_color
        )
    
    def test_fg_color_attribute_is_not_a_Color_instance(self):
        """testing if a TypeError will be raised when the fg_color attribute is
        not a Color instance
        """
        new_status = Status(**self.kwargs)
        self.assertRaises(TypeError, setattr, new_status, 'fg_color',
            ["asdf", 65, 25])
    
    def test_fg_color_argument_is_working_properly(self):
        """testing if the fg_color argument is working properly by setting its
        value its value to the fg_color attribute
        """
        self.kwargs['fg_color'] = Color(15, 25, 35)
        new_status = Status(**self.kwargs)
        self.assertEqual(self.kwargs['fg_color'], new_status.fg_color)
    
    def test_fg_color_attribute_is_working_properly(self):
        """testing if the fg_color attribute is working properly
        """
        new_status = Status(**self.kwargs)
        test_color = Color(15, 25, 35)
        new_status.fg_color = test_color
        self.assertEqual(test_color, new_status.fg_color)
