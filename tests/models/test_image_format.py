# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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

import unittest
from stalker import ImageFormat


class ImageFormatTest(unittest.TestCase):
    """the test case for the image format
    """

    def setUp(self):
        """setup some default values
        """
        # some proper values
        self.kwargs = {
            "name": "HD",
            "width": 1920,
            "height": 1080,
            "pixel_aspect": 1.0,
            "print_resolution": 300,
        }

        self.test_image_format = ImageFormat(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        ImageFormat class
        """
        self.assertFalse(ImageFormat.__auto_name__)

    def test_width_argument_accepts_int_or_float_only(self):
        """testing the width argument accepts integer or float and raises
        TypeError in any other case
        """
        # the width should be an integer or float
        test_values = ["1920", [1920], {}, ()]

        for test_value in test_values:
            self.kwargs["width"] = test_value
            self.assertRaises(TypeError, ImageFormat,
                              **self.kwargs)

    def test_width_attribute_int_or_float(self):
        """testing if a TypeError will be raised when the width attribute
        is not an integer or float
        """
        test_values = ["1920", [1920], {}, ()]

        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_image_format,
                "width",
                test_value
            )

    def test_width_argument_float_to_int_conversion(self):
        """testing for width argument is given as a float and converted to int
        successfully
        """
        # the given floats should be converted to integer
        self.kwargs["width"] = 1920.0
        an_image_format = ImageFormat(**self.kwargs)
        self.assertTrue(isinstance(an_image_format.width, int))

    def test_width_attribute_float_to_int_conversion(self):
        """testing the width attribute against being converted to int
        successfully
        """
        # the given floats should be converted to integer
        self.test_image_format.width = 1920.0
        self.assertTrue(isinstance(self.test_image_format.width, int))

    def test_width_argument_being_zero(self):
        """testing if a ValueError will be raised when the width argument is
        zero
        """
        # could not be zero
        self.kwargs["width"] = 0
        self.assertRaises(ValueError, ImageFormat, **self.kwargs)

    def test_width_attribute_being_zero(self):
        """testing if a ValueError will be raised when the width attribute is
        zero
        """
        # also test the attribute for this
        self.assertRaises(ValueError, setattr, self.test_image_format,
                          "width", 0)

    def test_width_argument_being_negative(self):
        """testing if a ValueError will be raised when the width argument is
        negative
        """
        self.kwargs["width"] = -10
        self.assertRaises(ValueError, ImageFormat, **self.kwargs)

    def test_width_attribute_being_negative(self):
        """testing if a ValueError will be raised when the width attribute is
        negative
        """
        # also test the attribute for this
        self.assertRaises(ValueError, setattr, self.test_image_format,
                          "width", -100)

    def test_height_argument_int_or_float(self):
        """testing if a TypeError will be raised when the height argument is
        not an integer or float
        """
        test_values = ["1080", [1080], {}, ()]

        for test_value in test_values:
            self.kwargs["height"] = test_value
            self.assertRaises(TypeError, ImageFormat,
                              **self.kwargs)

    def test_height_attribute_int_or_float(self):
        """testing if a TypeError will be raised when the height attribute is
        not an integer or float
        """
        # test also the attribute
        for test_value in ["1080", [1080]]:
            self.assertRaises(TypeError, setattr, self.test_image_format,
                              "height", test_value)

    def test_height_argument_float_to_int_conversion(self):
        """testing the height argument given as float will be converted to int
        successfully
        """
        self.kwargs["height"] = 1080.0
        an_image_format = ImageFormat(**self.kwargs)

        self.assertTrue(isinstance(an_image_format.height, int))

    def test_height_attribute_float_to_int_conversion(self):
        """testing the height attribute given as float being converted to int
        successfully
        """
        # also test the attribute for this
        self.test_image_format.height = 1080.0
        self.assertTrue(isinstance(self.test_image_format.height, int))

    def test_height_argument_being_zero(self):
        """testing if a ValueError will be raised when the height argument is
        zero
        """
        self.kwargs["height"] = 0
        self.assertRaises(ValueError, ImageFormat, **self.kwargs)

    def test_height_attribute_being_zero(self):
        """testing if a ValueError will be raised when the height attribute is
        zero
        """
        self.assertRaises(ValueError, setattr, self.test_image_format,
                          "height", 0)

    def test_height_argument_being_negative(self):
        """testing if a ValueError will be raised when the height argument is
        negative
        """
        self.kwargs["height"] = -10
        self.assertRaises(ValueError, ImageFormat, **self.kwargs)

    def test_height_attribute_being_negative(self):
        """testing if a ValueError will be raised when the height attribute is
        negative
        """
        self.assertRaises(ValueError, setattr, self.test_image_format,
                          "height", -100)

    def test_device_aspect_attribute_float(self):
        """testing the if device aspect ratio is calculated as a float value
        """
        self.assertTrue(
            isinstance(self.test_image_format.device_aspect, float)
        )

    def test_device_aspect_ratio_correctly_calculated(self):
        """testing if the device aspect ratio is correctly calculated
        """
        # the device aspect is something calculated using width, height and
        # the pixel aspect ratio

        # Test HD
        self.kwargs.update({
            "name": "HD",
            "width": 1920,
            "height": 1080,
            "pixel_aspect": 1.0,
            "print_resolution": 300
        })

        an_image_format = ImageFormat(**self.kwargs)

        # the device aspect for this setup should be around 1.7778
        self.assertEqual("%1.4g" % an_image_format.device_aspect,
                         "%1.4g" % 1.7778)

        # test PAL
        self.kwargs.update({
            "name": "PAL",
            "width": 720,
            "height": 576,
            "pixel_aspect": 1.0667,
            "print_resolution": 300
        })

        an_image_format = ImageFormat(**self.kwargs)

        # the device aspect for this setup should be around 4/3
        self.assertEqual("%1.4g" % an_image_format.device_aspect,
                         "%1.4g" % 1.3333)

    def test_device_aspect_attribute_updates(self):
        """testing if the device_aspect_ratio attribute is updated when any of
        the width, height or pixel_aspect attributes are changed
        """
        # just changing one of the width or height should be causing an update
        # in device_aspect

        # start with PAL
        self.kwargs.update({
            "name": "PAL",
            "width": 720,
            "height": 576,
            "pixel_aspect": 1.0667,
            "print_resolution": 300
        })

        an_image_format = ImageFormat(**self.kwargs)

        previous_device_aspect = an_image_format.device_aspect

        # change to HD
        an_image_format.width = 1920
        an_image_format.height = 1080
        an_image_format.pixel_aspect = 1.0

        self.assertTrue(abs(an_image_format.device_aspect - 1.77778) < 0.001)

        self.assertNotEqual(an_image_format.device_aspect,
                            previous_device_aspect)

    def test_device_aspect_attribute_write_protected(self):
        """testing if device_aspect attribute is write protected
        """
        # the device aspect should be write protected
        self.assertRaises(AttributeError,
                          setattr, self.test_image_format, "device_aspect", 10)

    def test_pixel_aspect_int_float(self):
        """testing if a TypeError will be raised when the pixel aspect ratio
        is not an integer or float
        """
        # the pixel aspect ratio should be a given as float or integer number

        # any other variable type than int and float is not ok
        self.kwargs["pixel_aspect"] = "1.0"
        self.assertRaises(TypeError, ImageFormat, **self.kwargs)

        # float is ok
        self.kwargs["pixel_aspect"] = 1.0
        imf1 = ImageFormat(**self.kwargs)

        # int is ok
        self.kwargs["pixel_aspect"] = 2
        imf1 = ImageFormat(**self.kwargs)

    def test_pixel_aspect_float_conversion(self):
        """testing if the pixel aspect ratio converted to float
        """
        # given an integer for the pixel aspect ratio,
        # the returned pixel aspect ratio should be a float
        self.kwargs["pixel_aspect"] = 1
        an_image_format = ImageFormat(**self.kwargs)
        self.assertTrue(isinstance(an_image_format.pixel_aspect, float))

    def test_pixel_aspect_argument_zero(self):
        """testing if a ValueError will be raised when the pixel_aspect
        argument is zero
        """
        # the pixel aspect ratio can not be zero
        self.kwargs["pixel_aspect"] = 0
        self.assertRaises(ValueError, ImageFormat, **self.kwargs)

    def test_pixel_aspect_attribute_zero(self):
        """testing if a ValueError will be raised when the pixel_aspect
        attribute is zero
        """
        self.assertRaises(ValueError, setattr, self.test_image_format,
                          "pixel_aspect", 0)

    def test_pixel_aspect_argument_negative(self):
        """testing if a ValueError will be raised when pixel_aspect argument is
        negative
        """
        # the pixel aspect ratio can not be negative
        self.kwargs["pixel_aspect"] = -1.0
        self.assertRaises(ValueError, ImageFormat, **self.kwargs)

        self.kwargs["pixel_aspect"] = -1
        self.assertRaises(ValueError, ImageFormat, **self.kwargs)

    def test_pixel_aspect_attribute_negative(self):
        """testing if a ValueError will be raised when pixel_aspect attribute
        is negative
        """
        # also test the attribute
        self.assertRaises(ValueError, setattr, self.test_image_format,
                          "pixel_aspect", -1.0)

        self.assertRaises(ValueError, setattr, self.test_image_format,
                          "pixel_aspect", -1)

    def test_pixel_aspect_attribute_if_being_initialized_correctly(self):
        """testing if pixel_aspect attribute is correctly initialized to its
        default value when omitted
        """
        self.kwargs.pop("pixel_aspect")
        an_image_format = ImageFormat(**self.kwargs)
        default_value = 1.0
        self.assertEqual(an_image_format.pixel_aspect, default_value)

    def test_print_resolution_omit(self):
        """testing the print timing_resolution against being omitted
        """
        # the print timing_resolution can be omitted
        self.kwargs.pop("print_resolution")
        imf = ImageFormat(**self.kwargs)

        # and the default value should be a float instance
        self.assertTrue(isinstance(imf.print_resolution, float))

    def test_print_resolution_argument_accepts_int_float_only(self):
        """testing if a TypeError will be raised when the print_resolution
        argument is not an integer or float
        """
        # the print timing_resolution should be initialized with an integer or
        # a float
        self.kwargs["print_resolution"] = "300.0"

        self.assertRaises(TypeError, ImageFormat, **self.kwargs)

        self.kwargs["print_resolution"] = 300
        imf = ImageFormat(**self.kwargs)
        self.assertTrue(isinstance(imf.print_resolution, float))

        self.kwargs["print_resolution"] = 300.0
        imf = ImageFormat(**self.kwargs)
        self.assertTrue(isinstance(imf.print_resolution, float))

    def test_print_resolution_argument_zero(self):
        """testing if a ValueError will be raised when the print_resolution
        argument is zero
        """
        self.kwargs["print_resolution"] = 0

        # the print timing_resolution can not be zero
        self.assertRaises(ValueError, ImageFormat, **self.kwargs)

    def test_print_resolution_attribute_zero(self):
        """testing if a ValueError will be raised when the print_resolution
        attribute is zero
        """
        # also test the attribute
        self.assertRaises(ValueError, setattr, self.test_image_format,
                          "print_resolution", 0)

    def test_print_resolution_argument_negative(self):
        """testing if a ValueError will be raised when the print_resolution
        argument is negative
        """
        # the print timing_resolution can not be negative
        self.kwargs["print_resolution"] = -300
        self.assertRaises(ValueError, ImageFormat, **self.kwargs)

        self.kwargs["print_resolution"] = -300.0
        self.assertRaises(ValueError, ImageFormat, **self.kwargs)

    def test_print_resolution_attribute_negative(self):
        """testing if a ValueError will be raised when the print_resolution
        attribute is negative
        """
        self.assertRaises(ValueError, setattr, self.test_image_format,
                          "print_resolution", -300)

        self.assertRaises(ValueError, setattr, self.test_image_format,
                          "print_resolution", -300.0)

    def test_equality(self):
        """testing equality operator
        """
        image_format1 = ImageFormat(**self.kwargs)
        image_format2 = ImageFormat(**self.kwargs)

        self.kwargs.update({
            "width": 720,
            "height": 480,
            "pixel_aspect": 0.888888,
        })
        image_format3 = ImageFormat(**self.kwargs)

        self.assertTrue(image_format1 == image_format2)
        self.assertFalse(image_format1 == image_format3)

    def test_inequality(self):
        """testing inequality operator
        """
        image_format1 = ImageFormat(**self.kwargs)
        image_format2 = ImageFormat(**self.kwargs)

        self.kwargs.update({
            "name": "NTSC",
            "description": "The famous NTSC image format",
            "width": 720,
            "height": 480,
            "pixel_aspect": 0.888888,
        })
        image_format3 = ImageFormat(**self.kwargs)

        self.assertFalse(image_format1 != image_format2)
        self.assertTrue(image_format1 != image_format3)

    def test_plural_class_name(self):
        """testing the plural name of ImageFormat class
        """
        self.assertTrue(self.test_image_format.plural_class_name,
                        "ImageFormats")

    # def test_hash_value(self):
    #     """testing if the hash value is correctly calculated
    #     """
    #     self.assertEqual(
    #         hash(self.test_image_format),
    #         hash(self.test_image_format.id) +
    #         2 * hash(self.test_image_format.name) +
    #         3 * hash(self.test_image_format.entity_type)
    #     )
