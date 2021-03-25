# -*- coding: utf-8 -*-

import unittest
import pytest
from stalker import ImageFormat


class ImageFormatTest(unittest.TestCase):
    """the test case for the image format
    """

    def setUp(self):
        """setup some default values
        """
        super(ImageFormatTest, self).setUp()

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
        assert ImageFormat.__auto_name__ is False

    def test_width_argument_accepts_int_or_float_only(self):
        """testing the width argument accepts integer or float and raises
        TypeError in any other case
        """
        # the width should be an integer or float
        test_value = "1920"
        self.kwargs["width"] = test_value
        with pytest.raises(TypeError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            'ImageFormat.width should be an instance of int or float not str'

    def test_width_attribute_int_or_float(self):
        """testing if a TypeError will be raised when the width attribute
        is not an integer or float
        """
        test_value = "1920"

        with pytest.raises(TypeError) as cm:
            self.test_image_format.width = test_value

        assert str(cm.value) == \
            'ImageFormat.width should be an instance of int or float not str'

    def test_width_argument_float_to_int_conversion(self):
        """testing for width argument is given as a float and converted to int
        successfully
        """
        # the given floats should be converted to integer
        self.kwargs["width"] = 1920.0
        an_image_format = ImageFormat(**self.kwargs)
        assert isinstance(an_image_format.width, int)

    def test_width_attribute_float_to_int_conversion(self):
        """testing the width attribute against being converted to int
        successfully
        """
        # the given floats should be converted to integer
        self.test_image_format.width = 1920.0
        assert isinstance(self.test_image_format.width, int)

    def test_width_argument_being_zero(self):
        """testing if a ValueError will be raised when the width argument is
        zero
        """
        # could not be zero
        self.kwargs["width"] = 0
        with pytest.raises(ValueError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            'ImageFormat.width cannot be zero or negative'

    def test_width_attribute_being_zero(self):
        """testing if a ValueError will be raised when the width attribute is
        zero
        """
        # also test the attribute for this
        with pytest.raises(ValueError) as cm:
            self.test_image_format.width = 0

        assert str(cm.value) == \
            'ImageFormat.width cannot be zero or negative'

    def test_width_argument_being_negative(self):
        """testing if a ValueError will be raised when the width argument is
        negative
        """
        self.kwargs["width"] = -10
        with pytest.raises(ValueError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            "ImageFormat.width cannot be zero or negative"

    def test_width_attribute_being_negative(self):
        """testing if a ValueError will be raised when the width attribute is
        negative
        """
        # also test the attribute for this
        with pytest.raises(ValueError) as cm:
            self.test_image_format.width = -100

        assert str(cm.value) == \
            'ImageFormat.width cannot be zero or negative'

    def test_height_argument_int_or_float(self):
        """testing if a TypeError will be raised when the height argument is
        not an integer or float
        """
        test_value = "1080"

        self.kwargs["height"] = test_value
        with pytest.raises(TypeError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            'ImageFormat.height should be an instance of int or float not str'

    def test_height_attribute_int_or_float(self):
        """testing if a TypeError will be raised when the height attribute is
        not an integer or float
        """
        # test also the attribute
        test_value = "1080"
        with pytest.raises(TypeError) as cm:
            self.test_image_format.height = test_value

        assert str(cm.value) == \
            'ImageFormat.height should be an instance of int or float not str'

    def test_height_argument_float_to_int_conversion(self):
        """testing the height argument given as float will be converted to int
        successfully
        """
        self.kwargs["height"] = 1080.0
        an_image_format = ImageFormat(**self.kwargs)

        assert isinstance(an_image_format.height, int)

    def test_height_attribute_float_to_int_conversion(self):
        """testing the height attribute given as float being converted to int
        successfully
        """
        # also test the attribute for this
        self.test_image_format.height = 1080.0
        assert isinstance(self.test_image_format.height, int)

    def test_height_argument_being_zero(self):
        """testing if a ValueError will be raised when the height argument is
        zero
        """
        self.kwargs["height"] = 0
        with pytest.raises(ValueError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == "ImageFormat.height cannot be zero or negative"

    def test_height_attribute_being_zero(self):
        """testing if a ValueError will be raised when the height attribute is
        zero
        """
        with pytest.raises(ValueError) as cm:
            self.test_image_format.height = 0

        assert str(cm.value) == 'ImageFormat.height cannot be zero or negative'

    def test_height_argument_being_negative(self):
        """testing if a ValueError will be raised when the height argument is
        negative
        """
        self.kwargs["height"] = -10
        with pytest.raises(ValueError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == "ImageFormat.height cannot be zero or negative"

    def test_height_attribute_being_negative(self):
        """testing if a ValueError will be raised when the height attribute is
        negative
        """
        with pytest.raises(ValueError) as cm:
            self.test_image_format.height = -100

        assert str(cm.value) == 'ImageFormat.height cannot be zero or negative'

    def test_device_aspect_attribute_float(self):
        """testing the if device aspect ratio is calculated as a float value
        """
        assert isinstance(self.test_image_format.device_aspect, float)

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
        assert "%1.4g" % an_image_format.device_aspect == "%1.4g" % 1.7778

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
        assert "%1.4g" % an_image_format.device_aspect == "%1.4g" % 1.3333

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

        assert abs(an_image_format.device_aspect - 1.77778) < 0.001

        assert an_image_format.device_aspect != previous_device_aspect

    def test_device_aspect_attribute_write_protected(self):
        """testing if device_aspect attribute is write protected
        """
        # the device aspect should be write protected
        with pytest.raises(AttributeError) as cm:
            self.test_image_format.device_aspect = 10

        assert str(cm.value) == "can't set attribute"

    def test_pixel_aspect_int_float(self):
        """testing if a TypeError will be raised when the pixel aspect ratio
        is not an integer or float
        """
        # the pixel aspect ratio should be a given as float or integer number

        # any other variable type than int and float is not ok
        self.kwargs["pixel_aspect"] = "1.0"
        with pytest.raises(TypeError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            'ImageFormat.pixel_aspect should be an instance of int or float ' \
            'not str'

    def test_pixel_aspect_int_float_2(self):
        """testing if a TypeError will be raised when the pixel aspect ratio
        is not an integer or float
        """
        # float is ok
        self.kwargs["pixel_aspect"] = 1.0
        ImageFormat(**self.kwargs)

    def test_pixel_aspect_int_float_3(self):
        """testing if a TypeError will be raised when the pixel aspect ratio
        is not an integer or float
        """
        # int is ok
        self.kwargs["pixel_aspect"] = 2
        ImageFormat(**self.kwargs)

    def test_pixel_aspect_float_conversion(self):
        """testing if the pixel aspect ratio converted to float
        """
        # given an integer for the pixel aspect ratio,
        # the returned pixel aspect ratio should be a float
        self.kwargs["pixel_aspect"] = 1
        an_image_format = ImageFormat(**self.kwargs)
        assert isinstance(an_image_format.pixel_aspect, float)

    def test_pixel_aspect_argument_zero(self):
        """testing if a ValueError will be raised when the pixel_aspect
        argument is zero
        """
        # the pixel aspect ratio can not be zero
        self.kwargs["pixel_aspect"] = 0
        with pytest.raises(ValueError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            'ImageFormat.pixel_aspect cannot be zero or a negative value'

    def test_pixel_aspect_attribute_zero(self):
        """testing if a ValueError will be raised when the pixel_aspect
        attribute is zero
        """
        with pytest.raises(ValueError) as cm:
            self.test_image_format.pixel_aspect = 0

        assert str(cm.value) == \
            'ImageFormat.pixel_aspect cannot be zero or a negative value'

    def test_pixel_aspect_argument_negative_float(self):
        """testing if a ValueError will be raised when pixel_aspect argument is
        negative
        """
        # the pixel aspect ratio can not be negative
        self.kwargs["pixel_aspect"] = -1.0
        with pytest.raises(ValueError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            'ImageFormat.pixel_aspect cannot be zero or a negative value'

    def test_pixel_aspect_argument_negative_int(self):
        """testing if a ValueError will be raised when pixel_aspect argument is
        negative
        """
        # the pixel aspect ratio can not be negative
        self.kwargs["pixel_aspect"] = -1
        with pytest.raises(ValueError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            'ImageFormat.pixel_aspect cannot be zero or a negative value'

    def test_pixel_aspect_attribute_negative_integer(self):
        """testing if a ValueError will be raised when pixel_aspect attribute
        is negative
        """
        # also test the attribute
        with pytest.raises(ValueError) as cm:
            self.test_image_format.pixel_aspect = -1.0

        assert str(cm.value) == \
            'ImageFormat.pixel_aspect cannot be zero or a negative value'

    def test_pixel_aspect_attribute_negative_float(self):
        """testing if a ValueError will be raised when pixel_aspect attribute
        is negative
        """
        with pytest.raises(ValueError) as cm:
            self.test_image_format.pixel_aspect = -1

        assert str(cm.value) == \
            'ImageFormat.pixel_aspect cannot be zero or a negative value'

    def test_pixel_aspect_attribute_if_being_initialized_correctly(self):
        """testing if pixel_aspect attribute is correctly initialized to its
        default value when omitted
        """
        self.kwargs.pop("pixel_aspect")
        an_image_format = ImageFormat(**self.kwargs)
        default_value = 1.0
        assert an_image_format.pixel_aspect == default_value

    def test_print_resolution_omit(self):
        """testing the print timing_resolution against being omitted
        """
        # the print timing_resolution can be omitted
        self.kwargs.pop("print_resolution")
        imf = ImageFormat(**self.kwargs)

        # and the default value should be a float instance
        assert isinstance(imf.print_resolution, float)

    def test_print_resolution_argument_accepts_int_float_only(self):
        """testing if a TypeError will be raised when the print_resolution
        argument is not an integer or float
        """
        # the print timing_resolution should be initialized with an integer or
        # a float
        self.kwargs["print_resolution"] = "300.0"

        with pytest.raises(TypeError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            'ImageFormat.print_resolution should be an instance of int or ' \
            'float not str'

    def test_print_resolution_argument_accepts_int_float_only_2(self):
        """testing if a TypeError will be raised when the print_resolution
        argument is not an integer or float
        """
        # the print timing_resolution should be initialized with an integer or
        # a float
        self.kwargs["print_resolution"] = 300
        imf = ImageFormat(**self.kwargs)
        assert isinstance(imf.print_resolution, float)

    def test_print_resolution_argument_accepts_int_float_only_3(self):
        """testing if a TypeError will be raised when the print_resolution
        argument is not an integer or float
        """
        # the print timing_resolution should be initialized with an integer or
        # a float
        self.kwargs["print_resolution"] = 300.0
        imf = ImageFormat(**self.kwargs)
        assert isinstance(imf.print_resolution, float)

    def test_print_resolution_argument_zero(self):
        """testing if a ValueError will be raised when the print_resolution
        argument is zero
        """
        self.kwargs["print_resolution"] = 0

        # the print timing_resolution can not be zero
        with pytest.raises(ValueError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            'ImageFormat.print_resolution cannot be zero or negative'

    def test_print_resolution_attribute_zero(self):
        """testing if a ValueError will be raised when the print_resolution
        attribute is zero
        """
        # also test the attribute
        with pytest.raises(ValueError) as cm:
            self.test_image_format.print_resolution = 0

        assert str(cm.value) == \
            'ImageFormat.print_resolution cannot be zero or negative'

    def test_print_resolution_argument_negative_int(self):
        """testing if a ValueError will be raised when the print_resolution
        argument is negative
        """
        # the print timing_resolution can not be negative
        self.kwargs["print_resolution"] = -300
        with pytest.raises(ValueError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            'ImageFormat.print_resolution cannot be zero or negative'

    def test_print_resolution_argument_negative_float(self):
        """testing if a ValueError will be raised when the print_resolution
        argument is negative
        """
        # the print timing_resolution can not be negative
        self.kwargs["print_resolution"] = -300.0
        with pytest.raises(ValueError) as cm:
            ImageFormat(**self.kwargs)

        assert str(cm.value) == \
            'ImageFormat.print_resolution cannot be zero or negative'

    def test_print_resolution_attribute_negative_int(self):
        """testing if a ValueError will be raised when the print_resolution
        attribute is negative
        """
        with pytest.raises(ValueError) as cm:
            self.test_image_format.print_resolution = -300

        assert str(cm.value) == \
            'ImageFormat.print_resolution cannot be zero or negative'

    def test_print_resolution_attribute_negative_float(self):
        """testing if a ValueError will be raised when the print_resolution
        attribute is negative
        """
        with pytest.raises(ValueError) as cm:
            self.test_image_format.print_resolution = -300.0

        assert str(cm.value) == \
            'ImageFormat.print_resolution cannot be zero or negative'

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

        assert image_format1 == image_format2
        assert not image_format1 == image_format3

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

        assert not image_format1 != image_format2
        assert image_format1 != image_format3

    def test_plural_class_name(self):
        """testing the plural name of ImageFormat class
        """
        assert self.test_image_format.plural_class_name == "ImageFormats"

    def test_hash_value(self):
        """testing if the hash value is correctly calculated
        """
        assert self.test_image_format.__hash__() == \
            hash(self.test_image_format.id) + \
            2 * hash(self.test_image_format.name) + \
            3 * hash(self.test_image_format.entity_type)
