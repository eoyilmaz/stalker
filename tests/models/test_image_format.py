# -*- coding: utf-8 -*-
"""Tests for the ImageFormat class."""

import sys
import pytest

from stalker import ImageFormat


@pytest.fixture(scope="function")
def setup_image_format_tests():
    """Set up test data for the ImageFormat."""
    data = dict()

    # some proper values
    data["kwargs"] = {
        "name": "HD",
        "width": 1920,
        "height": 1080,
        "pixel_aspect": 1.0,
        "print_resolution": 300,
    }

    data["test_image_format"] = ImageFormat(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for ImageFormat class."""
    assert ImageFormat.__auto_name__ is False


def test_width_argument_accepts_int_or_float_only(setup_image_format_tests):
    """TypeError is raised if the width argument is not integer or float."""
    data = setup_image_format_tests
    # the width should be an integer or float
    test_value = "1920"
    data["kwargs"]["width"] = test_value
    with pytest.raises(TypeError) as cm:
        ImageFormat(**data["kwargs"])

    assert (
        str(cm.value)
        == "ImageFormat.width should be an instance of int or float, not str: '1920'"
    )


def test_width_attribute_int_or_float(setup_image_format_tests):
    """TypeError is raised if the width attribute is not an integer or float."""
    data = setup_image_format_tests
    test_value = "1920"
    with pytest.raises(TypeError) as cm:
        data["test_image_format"].width = test_value

    assert (
        str(cm.value)
        == "ImageFormat.width should be an instance of int or float, not str: '1920'"
    )


def test_width_argument_float_to_int_conversion(setup_image_format_tests):
    """width argument is given as a float and converted to int successfully."""
    data = setup_image_format_tests
    # the given floats should be converted to integer
    data["kwargs"]["width"] = 1920.0
    an_image_format = ImageFormat(**data["kwargs"])
    assert isinstance(an_image_format.width, int)


def test_width_attribute_float_to_int_conversion(setup_image_format_tests):
    """width attribute against being converted to int successfully."""
    data = setup_image_format_tests
    # the given floats should be converted to integer
    data["test_image_format"].width = 1920.0
    assert isinstance(data["test_image_format"].width, int)


def test_width_argument_being_zero(setup_image_format_tests):
    """ValueError is raised if the width argument is zero."""
    data = setup_image_format_tests
    # could not be zero
    data["kwargs"]["width"] = 0
    with pytest.raises(ValueError) as cm:
        ImageFormat(**data["kwargs"])

    assert str(cm.value) == "ImageFormat.width cannot be zero or negative"


def test_width_attribute_being_zero(setup_image_format_tests):
    """ValueError is raised if the width attribute is zero."""
    data = setup_image_format_tests
    # also test the attribute for this
    with pytest.raises(ValueError) as cm:
        data["test_image_format"].width = 0

    assert str(cm.value) == "ImageFormat.width cannot be zero or negative"


def test_width_argument_being_negative(setup_image_format_tests):
    """ValueError is raised if the width argument is negative."""
    data = setup_image_format_tests
    data["kwargs"]["width"] = -10
    with pytest.raises(ValueError) as cm:
        ImageFormat(**data["kwargs"])

    assert str(cm.value) == "ImageFormat.width cannot be zero or negative"


def test_width_attribute_being_negative(setup_image_format_tests):
    """ValueError is raised if the width attribute is negative."""
    data = setup_image_format_tests
    # also test the attribute for this
    with pytest.raises(ValueError) as cm:
        data["test_image_format"].width = -100

    assert str(cm.value) == "ImageFormat.width cannot be zero or negative"


def test_height_argument_int_or_float(setup_image_format_tests):
    """TypeError is raised if the height argument is not an integer or float."""
    data = setup_image_format_tests
    test_value = "1080"
    data["kwargs"]["height"] = test_value
    with pytest.raises(TypeError) as cm:
        ImageFormat(**data["kwargs"])

    assert (
        str(cm.value)
        == "ImageFormat.height should be an instance of int or float, not str"
    )


def test_height_attribute_int_or_float(setup_image_format_tests):
    """TypeError is raised if the height attribute is not an integer or float."""
    data = setup_image_format_tests
    # test also the attribute
    test_value = "1080"
    with pytest.raises(TypeError) as cm:
        data["test_image_format"].height = test_value

    assert (
        str(cm.value)
        == "ImageFormat.height should be an instance of int or float, not str"
    )


def test_height_argument_float_to_int_conversion(setup_image_format_tests):
    """height argument given as float is converted to int successfully."""
    data = setup_image_format_tests
    data["kwargs"]["height"] = 1080.0
    an_image_format = ImageFormat(**data["kwargs"])
    assert isinstance(an_image_format.height, int)


def test_height_attribute_float_to_int_conversion(setup_image_format_tests):
    """height attribute given as float being converted to int successfully."""
    data = setup_image_format_tests
    # also test the attribute for this
    data["test_image_format"].height = 1080.0
    assert isinstance(data["test_image_format"].height, int)


def test_height_argument_being_zero(setup_image_format_tests):
    """ValueError is raised if the height argument is zero."""
    data = setup_image_format_tests
    data["kwargs"]["height"] = 0
    with pytest.raises(ValueError) as cm:
        ImageFormat(**data["kwargs"])
    assert str(cm.value) == "ImageFormat.height cannot be zero or negative"


def test_height_attribute_being_zero(setup_image_format_tests):
    """ValueError is raised if the height attribute is zero."""
    data = setup_image_format_tests
    with pytest.raises(ValueError) as cm:
        data["test_image_format"].height = 0
    assert str(cm.value) == "ImageFormat.height cannot be zero or negative"


def test_height_argument_being_negative(setup_image_format_tests):
    """ValueError is raised if the height argument is negative."""
    data = setup_image_format_tests
    data["kwargs"]["height"] = -10
    with pytest.raises(ValueError) as cm:
        ImageFormat(**data["kwargs"])
    assert str(cm.value) == "ImageFormat.height cannot be zero or negative"


def test_height_attribute_being_negative(setup_image_format_tests):
    """ValueError is raised if the height attribute is negative."""
    data = setup_image_format_tests
    with pytest.raises(ValueError) as cm:
        data["test_image_format"].height = -100
    assert str(cm.value) == "ImageFormat.height cannot be zero or negative"


def test_device_aspect_attribute_float(setup_image_format_tests):
    """device aspect ratio is calculated as a float value."""
    data = setup_image_format_tests
    assert isinstance(data["test_image_format"].device_aspect, float)


def test_device_aspect_ratio_correctly_calculated_1(setup_image_format_tests):
    """device aspect ratio is correctly calculated."""
    data = setup_image_format_tests
    # the device aspect is something calculated using width, height and
    # the pixel aspect ratio

    # Test HD
    data["kwargs"].update(
        {
            "name": "HD",
            "width": 1920,
            "height": 1080,
            "pixel_aspect": 1.0,
            "print_resolution": 300,
        }
    )

    an_image_format = ImageFormat(**data["kwargs"])

    # the device aspect for this setup should be around 1.7778
    assert "%1.4g" % an_image_format.device_aspect == "%1.4g" % 1.7778


def test_device_aspect_ratio_correctly_calculated_2(setup_image_format_tests):
    """device aspect ratio is correctly calculated."""
    data = setup_image_format_tests

    # test PAL
    data["kwargs"].update(
        {
            "name": "PAL",
            "width": 720,
            "height": 576,
            "pixel_aspect": 1.0667,
            "print_resolution": 300,
        }
    )

    an_image_format = ImageFormat(**data["kwargs"])

    # the device aspect for this setup should be around 4/3
    assert "%1.4g" % an_image_format.device_aspect == "%1.4g" % 1.3333


def test_device_aspect_attribute_updates(setup_image_format_tests):
    """device_aspect_ratio attr is updated if width, height or pixel_aspect updated."""
    data = setup_image_format_tests
    # just changing one of the width or height should be causing an update
    # in device_aspect

    # start with PAL
    data["kwargs"].update(
        {
            "name": "PAL",
            "width": 720,
            "height": 576,
            "pixel_aspect": 1.0667,
            "print_resolution": 300,
        }
    )
    an_image_format = ImageFormat(**data["kwargs"])
    previous_device_aspect = an_image_format.device_aspect

    # change to HD
    an_image_format.width = 1920
    an_image_format.height = 1080
    an_image_format.pixel_aspect = 1.0

    assert abs(an_image_format.device_aspect - 1.77778) < 0.001
    assert an_image_format.device_aspect != previous_device_aspect


def test_device_aspect_attribute_write_protected(setup_image_format_tests):
    """device_aspect attribute is write protected."""
    data = setup_image_format_tests
    # the device aspect should be write protected
    with pytest.raises(AttributeError) as cm:
        data["test_image_format"].device_aspect = 10

    error_message = (
        "can't set attribute 'device_aspect'"
        if sys.version_info.minor < 11
        else "property 'device_aspect' of 'ImageFormat' object has no setter"
    )

    assert str(cm.value) == error_message


def test_pixel_aspect_int_float(setup_image_format_tests):
    """TypeError is raised if the pixel aspect ratio is not an integer or float."""
    data = setup_image_format_tests
    # the pixel aspect ratio should be a given as float or integer number
    # any other variable type than int and float is not ok
    data["kwargs"]["pixel_aspect"] = "1.0"
    with pytest.raises(TypeError) as cm:
        ImageFormat(**data["kwargs"])

    assert (
        str(cm.value)
        == "ImageFormat.pixel_aspect should be an instance of int or float "
        "not str"
    )


def test_pixel_aspect_int_float_2(setup_image_format_tests):
    """TypeError is raised if the pixel aspect ratio is not an integer or float."""
    data = setup_image_format_tests
    # float is ok
    data["kwargs"]["pixel_aspect"] = 1.0
    ImageFormat(**data["kwargs"])


def test_pixel_aspect_int_float_3(setup_image_format_tests):
    """TypeError is raised if the pixel aspect ratio is not an integer or float."""
    data = setup_image_format_tests
    # int is ok
    data["kwargs"]["pixel_aspect"] = 2
    ImageFormat(**data["kwargs"])


def test_pixel_aspect_float_conversion(setup_image_format_tests):
    """pixel aspect ratio converted to float."""
    data = setup_image_format_tests
    # given an integer for the pixel aspect ratio,
    # the returned pixel aspect ratio should be a float
    data["kwargs"]["pixel_aspect"] = 1
    an_image_format = ImageFormat(**data["kwargs"])
    assert isinstance(an_image_format.pixel_aspect, float)


def test_pixel_aspect_argument_zero(setup_image_format_tests):
    """ValueError is raised if the pixel_aspect argument is zero."""
    data = setup_image_format_tests
    # the pixel aspect ratio can not be zero
    data["kwargs"]["pixel_aspect"] = 0
    with pytest.raises(ValueError) as cm:
        ImageFormat(**data["kwargs"])
    assert (
        str(cm.value) == "ImageFormat.pixel_aspect cannot be zero or a negative value"
    )


def test_pixel_aspect_attribute_zero(setup_image_format_tests):
    """ValueError is raised if the pixel_aspect attribute is zero."""
    data = setup_image_format_tests
    with pytest.raises(ValueError) as cm:
        data["test_image_format"].pixel_aspect = 0
    assert (
        str(cm.value) == "ImageFormat.pixel_aspect cannot be zero or a negative value"
    )


def test_pixel_aspect_argument_negative_float(setup_image_format_tests):
    """ValueError is raised if pixel_aspect argument is negative."""
    data = setup_image_format_tests
    # the pixel aspect ratio can not be negative
    data["kwargs"]["pixel_aspect"] = -1.0
    with pytest.raises(ValueError) as cm:
        ImageFormat(**data["kwargs"])
    assert (
        str(cm.value) == "ImageFormat.pixel_aspect cannot be zero or a negative value"
    )


def test_pixel_aspect_argument_negative_int(setup_image_format_tests):
    """ValueError is raised if pixel_aspect argument is negative."""
    data = setup_image_format_tests
    # the pixel aspect ratio can not be negative
    data["kwargs"]["pixel_aspect"] = -1
    with pytest.raises(ValueError) as cm:
        ImageFormat(**data["kwargs"])
    assert (
        str(cm.value) == "ImageFormat.pixel_aspect cannot be zero or a negative value"
    )


def test_pixel_aspect_attribute_negative_integer(setup_image_format_tests):
    """ValueError is raised if pixel_aspect attribute is negative."""
    data = setup_image_format_tests
    # also test the attribute
    with pytest.raises(ValueError) as cm:
        data["test_image_format"].pixel_aspect = -1.0
    assert (
        str(cm.value) == "ImageFormat.pixel_aspect cannot be zero or a negative value"
    )


def test_pixel_aspect_attribute_negative_float(setup_image_format_tests):
    """ValueError is raised if pixel_aspect attribute is negative."""
    data = setup_image_format_tests
    with pytest.raises(ValueError) as cm:
        data["test_image_format"].pixel_aspect = -1
    assert (
        str(cm.value) == "ImageFormat.pixel_aspect cannot be zero or a negative value"
    )


def test_pixel_aspect_attribute_if_being_initialized_correctly(
    setup_image_format_tests,
):
    """pixel_aspect attr is correctly initialized to its default value if omitted."""
    data = setup_image_format_tests
    data["kwargs"].pop("pixel_aspect")
    an_image_format = ImageFormat(**data["kwargs"])
    default_value = 1.0
    assert an_image_format.pixel_aspect == default_value


def test_print_resolution_omit(setup_image_format_tests):
    """print_resolution against being omitted."""
    data = setup_image_format_tests
    # the print timing_resolution can be omitted
    data["kwargs"].pop("print_resolution")
    imf = ImageFormat(**data["kwargs"])

    # and the default value should be a float instance
    assert isinstance(imf.print_resolution, float)


def test_print_resolution_argument_accepts_int_float_only(setup_image_format_tests):
    """TypeError is raised if the print_resolution arg is not an integer or float."""
    data = setup_image_format_tests
    # the print timing_resolution should be initialized with an integer or a float
    data["kwargs"]["print_resolution"] = "300.0"

    with pytest.raises(TypeError) as cm:
        ImageFormat(**data["kwargs"])

    assert (
        str(cm.value) == "ImageFormat.print_resolution should be an instance of int or "
        "float not str"
    )


def test_print_resolution_argument_accepts_int_float_only_2(setup_image_format_tests):
    """TypeError is raised if the print_resolution arg is not an integer or float."""
    # the print timing_resolution should be initialized with an integer or a float
    data = setup_image_format_tests
    data["kwargs"]["print_resolution"] = 300
    imf = ImageFormat(**data["kwargs"])
    assert isinstance(imf.print_resolution, float)


def test_print_resolution_argument_accepts_int_float_only_3(setup_image_format_tests):
    """TypeError is raised if the print_resolution arg is not an integer or float."""
    data = setup_image_format_tests
    # the print timing_resolution should be initialized with an integer or
    # a float
    data["kwargs"]["print_resolution"] = 300.0
    imf = ImageFormat(**data["kwargs"])
    assert isinstance(imf.print_resolution, float)


def test_print_resolution_argument_zero(setup_image_format_tests):
    """ValueError is raised if the print_resolution argument is zero."""
    data = setup_image_format_tests
    data["kwargs"]["print_resolution"] = 0

    # the print timing_resolution can not be zero
    with pytest.raises(ValueError) as cm:
        ImageFormat(**data["kwargs"])

    assert str(cm.value) == "ImageFormat.print_resolution cannot be zero or negative"


def test_print_resolution_attribute_zero(setup_image_format_tests):
    """ValueError is raised if the print_resolution attribute is zero."""
    data = setup_image_format_tests
    # also test the attribute
    with pytest.raises(ValueError) as cm:
        data["test_image_format"].print_resolution = 0

    assert str(cm.value) == "ImageFormat.print_resolution cannot be zero or negative"


def test_print_resolution_argument_negative_int(setup_image_format_tests):
    """ValueError is raised if the print_resolution argument is negative."""
    data = setup_image_format_tests
    # the print timing_resolution can not be negative
    data["kwargs"]["print_resolution"] = -300
    with pytest.raises(ValueError) as cm:
        ImageFormat(**data["kwargs"])

    assert str(cm.value) == "ImageFormat.print_resolution cannot be zero or negative"


def test_print_resolution_argument_negative_float(setup_image_format_tests):
    """ValueError is raised if the print_resolution argument is negative."""
    data = setup_image_format_tests
    # the print timing_resolution can not be negative
    data["kwargs"]["print_resolution"] = -300.0
    with pytest.raises(ValueError) as cm:
        ImageFormat(**data["kwargs"])

    assert str(cm.value) == "ImageFormat.print_resolution cannot be zero or negative"


def test_print_resolution_attribute_negative_int(setup_image_format_tests):
    """ValueError is raised if the print_resolution attribute is negative."""
    data = setup_image_format_tests
    with pytest.raises(ValueError) as cm:
        data["test_image_format"].print_resolution = -300

    assert str(cm.value) == "ImageFormat.print_resolution cannot be zero or negative"


def test_print_resolution_attribute_negative_float(setup_image_format_tests):
    """ValueError is raised if the print_resolution attribute is negative."""
    data = setup_image_format_tests
    with pytest.raises(ValueError) as cm:
        data["test_image_format"].print_resolution = -300.0

    assert str(cm.value) == "ImageFormat.print_resolution cannot be zero or negative"


def test_equality(setup_image_format_tests):
    """Equality operator."""
    data = setup_image_format_tests
    image_format1 = ImageFormat(**data["kwargs"])
    image_format2 = ImageFormat(**data["kwargs"])

    data["kwargs"].update(
        {
            "width": 720,
            "height": 480,
            "pixel_aspect": 0.888888,
        }
    )
    image_format3 = ImageFormat(**data["kwargs"])

    assert image_format1 == image_format2
    assert not image_format1 == image_format3


def test_inequality(setup_image_format_tests):
    """Inequality operator."""
    data = setup_image_format_tests
    image_format1 = ImageFormat(**data["kwargs"])
    image_format2 = ImageFormat(**data["kwargs"])

    data["kwargs"].update(
        {
            "name": "NTSC",
            "description": "The famous NTSC image format",
            "width": 720,
            "height": 480,
            "pixel_aspect": 0.888888,
        }
    )
    image_format3 = ImageFormat(**data["kwargs"])

    assert not image_format1 != image_format2
    assert image_format1 != image_format3


def test_plural_class_name(setup_image_format_tests):
    """Plural name of ImageFormat class."""
    data = setup_image_format_tests
    assert data["test_image_format"].plural_class_name == "ImageFormats"


def test_hash_value(setup_image_format_tests):
    """hash value is correctly calculated."""
    data = setup_image_format_tests
    assert data["test_image_format"].__hash__() == hash(
        data["test_image_format"].id
    ) + 2 * hash(data["test_image_format"].name) + 3 * hash(
        data["test_image_format"].entity_type
    )
