# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import unittest2
from stalker import Entity, Status
from stalker import config
defaults = config.Config()

class StatusTest(unittest2.TestCase):
    """tests the stalker.models.status.Status class
    """
    
    def setUp(self):
        """setup the test
        """
        self.kwargs = {
            'name': 'Complete',
            'description': 'use this when the object is complete',
            'code': 'CMPLT',
            'fg_color': 0x000000,
            'bg_color': 0x00ff00,
        }
        
        # create an entity object with same kwargs for __eq__ and __ne__ tests
        # (it should return False for __eq__ and True for __ne__ for same
        # kwargs)
        self.entity1 = Entity(**self.kwargs)
    
    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Status class
        """
        self.assertFalse(Status.__auto_name__)
     
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
            defaults.status_bg_color,
            new_status.bg_color
        )
    
    def test_bg_color_argument_is_None(self):
        """testing if the bg_color attribute will be filled with the default
        color when the bg_color argument is None
        """
        self.kwargs['bg_color'] = None
        new_status = Status(**self.kwargs)
        self.assertEqual(
            defaults.status_bg_color,
            new_status.bg_color
        )
    
    def test_bg_color_attribute_is_None(self):
        """testing if the bg_color attribute is set to None will reset the
        color to default color
        """
        new_status = Status(**self.kwargs)
        new_status.bg_color = None
        self.assertEqual(
            defaults.status_bg_color,
            new_status.bg_color
        )
    
    def test_bg_color_argument_is_not_an_integer(self):
        """testing if a TypeError will be raised when the bg_color argument is
        not an integer
        """
        self.kwargs['bg_color'] = ["2342", 53, 33 ]
        self.assertRaises(TypeError, Status, **self.kwargs)
    
    def test_bg_color_attribute_is_not_an_integer(self):
        """testing if a TypeError will be raised when the bg_color attribute is
        not an integer
        """
        new_status = Status(**self.kwargs)
        self.assertRaises(TypeError, setattr, new_status, 'bg_color',
            ["asdf", 65, 25])
    
    def test_bg_color_argument_is_negative(self):
        """testing if the bg_color attribute value is clamped to 0 if bg_color
        argument is negative
        """
        self.kwargs['bg_color'] = -10
        new_status = Status(**self.kwargs)
        self.assertEqual(new_status.bg_color, 0)
    
    def test_bg_color_attribute_is_negative(self):
        """testing if the bg_color attribute value is clamped to 0 if it is set
        to a negative value
        """
        new_status = Status(**self.kwargs)
        new_status.bg_color = -10
        self.assertEqual(new_status.bg_color, 0)
    
    def test_bg_color_argument_is_too_big(self):
        """testing if the bg_color attribute value is clamped to 0xffffff if
        bg_color argument is bigger than that value
        """
        self.kwargs['bg_color'] = 0xffffff + 10
        new_status = Status(**self.kwargs)
        self.assertEqual(new_status.bg_color, 0xffffff)
    
    def test_bg_color_attribute_is_too_big(self):
        """testing if the bg_color attribute value is clamped to 0xffffff if it
        is bigger than that value
        """
        new_status = Status(**self.kwargs)
        new_status.bg_color = 0xffffff + 10
        self.assertEqual(new_status.bg_color, 0xffffff)
    
    def test_bg_color_argument_is_working_properly(self):
        """testing if the bg_color argument is working properly by setting its
        value its value to the bg_color attribute
        """
        self.kwargs['bg_color'] = 0xa0a000
        new_status = Status(**self.kwargs)
        self.assertEqual(self.kwargs['bg_color'], new_status.bg_color)
    
    def test_bg_color_attribute_is_working_properly(self):
        """testing if the bg_color attribute is working properly
        """
        new_status = Status(**self.kwargs)
        test_color = 0x564852
        new_status.bg_color = test_color
        self.assertEqual(test_color, new_status.bg_color)
    
    def test_fg_color_argument_is_skipped(self):
        """testing if the fg_color attribute will be filled with the default
        color when the fg_color argument is skipped
        """
        self.kwargs.pop('fg_color')
        new_status = Status(**self.kwargs)
        self.assertEqual(
            defaults.status_fg_color,
            new_status.fg_color
        )
    
    def test_fg_color_argument_is_None(self):
        """testing if the fg_color attribute will be filled with the default
        color when the fg_color argument is None
        """
        self.kwargs['fg_color'] = None
        new_status = Status(**self.kwargs)
        self.assertEqual(
            defaults.status_fg_color,
            new_status.fg_color
        )
    
    def test_fg_color_attribute_is_None(self):
        """testing if the fg_color attribute is set to None will reset the
        color to default color
        """
        new_status = Status(**self.kwargs)
        new_status.fg_color = None
        self.assertEqual(
            defaults.status_fg_color,
            new_status.fg_color
        )
    
    def test_fg_color_argument_is_not_an_integer(self):
        """testing if a TypeError will be raised when the fg_color argument is
        not an integer
        """
        self.kwargs['fg_color'] = ["2342", 53, 33 ]
        self.assertRaises(TypeError, Status, **self.kwargs)
    
    def test_fg_color_attribute_is_not_an_integer(self):
        """testing if a TypeError will be raised when the fg_color attribute is
        not an integer
        """
        new_status = Status(**self.kwargs)
        self.assertRaises(TypeError, setattr, new_status, 'fg_color',
            ["asdf", 65, 25])
    
    def test_fg_color_argument_is_negative(self):
        """testing if the fg_color attribute value is clamped to 0 if fg_color
        argument is negative
        """
        self.kwargs['fg_color'] = -10
        new_status = Status(**self.kwargs)
        self.assertEqual(new_status.fg_color, 0)
    
    def test_fg_color_attribute_is_negative(self):
        """testing if the fg_color attribute value is clamped to 0 if it is set
        to a negative value
        """
        new_status = Status(**self.kwargs)
        new_status.fg_color = -10
        self.assertEqual(new_status.fg_color, 0)
    
    def test_fg_color_argument_is_too_big(self):
        """testing if the fg_color attribute value is clamped to 0xffffff if
        fg_color argument is bigger than that value
        """
        self.kwargs['fg_color'] = 0xffffff + 10
        new_status = Status(**self.kwargs)
        self.assertEqual(new_status.fg_color, 0xffffff)
    
    def test_fg_color_attribute_is_too_big(self):
        """testing if the fg_color attribute value is clamped to 0xffffff if it
        is bigger than that value
        """
        new_status = Status(**self.kwargs)
        new_status.fg_color = 0xffffff + 10
        self.assertEqual(new_status.fg_color, 0xffffff)
    
    def test_fg_color_argument_is_working_properly(self):
        """testing if the fg_color argument is working properly by setting its
        value its value to the fg_color attribute
        """
        self.kwargs['fg_color'] = 0xa0a000
        new_status = Status(**self.kwargs)
        self.assertEqual(self.kwargs['fg_color'], new_status.fg_color)
    
    def test_fg_color_attribute_is_working_properly(self):
        """testing if the fg_color attribute is working properly
        """
        new_status = Status(**self.kwargs)
        test_color = 0x564852
        new_status.fg_color = test_color
        self.assertEqual(test_color, new_status.fg_color)
    
