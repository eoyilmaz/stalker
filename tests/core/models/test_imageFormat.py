#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import imageFormat





########################################################################
class ImageFormatTest(mocker.MockerTestCase):
    """the test case for the image format
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup some default values
        """
        #----------------------------------------------------------------------
        # some proper values
        self.kwargs = {
            "name": "HD",
            "width": 1920,
            "height": 1080,
            "pixel_aspect": 1.0,
            "print_resolution": 300,
        }
        
        self.mock_imageFormat = imageFormat.ImageFormat(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_width_argument_accepts_int_or_float_only(self):
        """testing the width argument accepts integer or float and raises
        ValueError in any other case
        """
        
        #----------------------------------------------------------------------
        # the width should be an integer or float
        test_values = ["1920", [1920], {}, ()]
        
        for test_value in test_values:
            self.kwargs["width"] = test_value
            self.assertRaises(ValueError, imageFormat.ImageFormat,
                              **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_width_attribute_int_or_float(self):
        """testing the width attribute against not being an integer or float
        """
        
        test_values = ["1920", [1920], {}, ()]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_imageFormat,
                "width",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_width_argument_float_to_int_conversion(self):
        """testing for width argument is given as a float and converted to int
        successfuly
        """
        
        #----------------------------------------------------------------------
        # the given floats should be converted to integer
        self.kwargs["width"] = 1920.0
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
        self.assertIsInstance(an_image_format.width, int)
    
    
    
    #----------------------------------------------------------------------
    def test_width_attribute_float_to_int_conversion(self):
        """testing the width attribute against being converted to int
        successfuly
        """
        
        #----------------------------------------------------------------------
        # the given floats should be converted to integer
        self.mock_imageFormat.width = 1920.0
        self.assertIsInstance(self.mock_imageFormat.width, int)
    
    
    
    #----------------------------------------------------------------------
    def test_width_argument_being_zero(self):
        """testing the width argument against being zero
        """
        
        #----------------------------------------------------------------------
        # could not be zero
        self.kwargs["width"] = 0
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
    
    
    #----------------------------------------------------------------------
    def test_width_attribute_being_zero(self):
        """testing the width attribute against being zero
        """
        
        # also test the attribute for this
        self.assertRaises(ValueError, setattr, self.mock_imageFormat,
                          "width", 0)
    
    
    
    #----------------------------------------------------------------------
    def test_width_argument_being_negative(self):
        """testing the width argument against being negative
        """
        
        self.kwargs["width"] = -10
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_width_attribute_being_negative(self):
        """testing the width attribute against being negative
        """
        
        # also test the attribute for this
        self.assertRaises(ValueError, setattr, self.mock_imageFormat,
                          "width", -100)
    
    
    
    #----------------------------------------------------------------------
    def test_height_argument_int_or_float(self):
        """testing the height argument against not being integer or float
        """
        
        test_values = ["1080", [1080], {}, ()]
        
        for test_value in test_values:
            self.kwargs["height"] = test_value
            self.assertRaises(ValueError, imageFormat.ImageFormat,
                              **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_height_attribute_int_or_float(self):
        """testing the height attribute against not being an integer or float
        """
        
        # test also the attribute
        for test_value in ["1080", [1080]]:
            self.assertRaises(
                ValueError, setattr, self.mock_imageFormat, "height", "1080")
    
    
    
    #----------------------------------------------------------------------
    def test_height_argument_float_to_int_conversion(self):
        """testing the height argument against being converted to int
        successfuly
        """
        
        self.kwargs["height"] = 1080.0
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
        
        self.assertIsInstance(an_image_format.height, int)
    
    
    
    #----------------------------------------------------------------------
    def test_height_attribute_float_to_int_conversion(self):
        """testing the height attribute against being converted to int
        successfuly
        """
        
        # also test the attribute for this
        self.mock_imageFormat.height = 1080.0
        self.assertIsInstance(self.mock_imageFormat.height, int)
    
    
    
    #----------------------------------------------------------------------
    def test_height_argument_being_zero(self):
        """testing the height argument against being zero
        """
        
        self.kwargs["height"] = 0
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_height_attribute_being_zero(self):
        """testing the height attribute against being zero
        """
        
        self.assertRaises(ValueError, setattr, self.mock_imageFormat,
                          "height", 0)
    
    
    
    #----------------------------------------------------------------------
    def test_height_argument_being_negative(self):
        """testing the height argument against being negative
        """
        self.kwargs["height"] = -10
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_height_attribute_being_negative(self):
        """testing the height attribute against being negative
        """
        
        self.assertRaises(ValueError, setattr, self.mock_imageFormat,
                          "height", -100)
    
    
    
    #----------------------------------------------------------------------
    def test_device_aspect_attribute_float(self):
        """testing the device aspect ratio attribute against not being a float
        value
        """
        
        self.assertIsInstance(self.mock_imageFormat.device_aspect, float)
    
    
    
    #----------------------------------------------------------------------
    def test_device_aspect_ratio_correctly_calculated(self):
        """testing the device aspect ratio against being correctly calculated
        """
        
        #----------------------------------------------------------------------
        # the device aspect is something calculated using width, height and
        # the pixel aspect ratio
        
        #----------------------------------------------------------------------
        # Test HD
        self.kwargs.update({
            "name": "HD",
            "width": 1920,
            "height": 1080,
            "pixel_aspect": 1.0,
            "print_resolution": 300
        })
        
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
        
        # the device aspect for this setup should be around 1.7778
        self.assertEquals("%1.4g" % an_image_format.device_aspect,
                          "%1.4g" % 1.7778 )
        
        
        #----------------------------------------------------------------------
        # test PAL
        self.kwargs.update({
            "name": "PAL",
            "width": 720,
            "height": 576,
            "pixel_aspect": 1.0667,
            "print_resolution": 300
        })
        
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
        
        # the device aspect for this setup should be around 4/3
        self.assertEquals("%1.4g" % an_image_format.device_aspect,
                          "%1.4g" % 1.3333)
    
    
    
    #----------------------------------------------------------------------
    def test_device_aspect_attribute_updates(self):
        """testing device_aspect_ratio attribute being updated on changes to
        any of the witdh, height or pixel_aspect
        """
        
        #----------------------------------------------------------------------
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
        
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
        
        previous_device_aspect = an_image_format.device_aspect
        
        # change to HD
        an_image_format.width = 1920
        an_image_format.height = 1080
        an_image_format.pixel_aspect = 1.0
        
        self.assertTrue(abs(an_image_format.device_aspect - 1.77778) < 0.001)
        
        self.assertNotEqual(an_image_format.device_aspect,
                            previous_device_aspect)
    
    
    
    #----------------------------------------------------------------------
    def test_device_aspect_attribute_write_protected(self):
        """testing if device_aspect attribute is write protected
        """
        
        #----------------------------------------------------------------------
        # the device aspect should be write propetected
        self.assertRaises(AttributeError,
                          setattr, self.mock_imageFormat, "device_aspect", 10)
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_int_float(self):
        """testing the pixel aspect ratio against not being integer or float
        """
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio should be a given as float or integer number
        
        # any other variable type than int and float is not ok
        self.kwargs["pixel_aspect"] = "1.0"
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
        
        # float is ok
        self.kwargs["pixel_aspect"] = 1.0
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
        
        # int is ok
        self.kwargs["pixel_aspect"] = 2
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_float_conversion(self):
        """testing the pixel aspect ratio conversion to float
        """
        
        #----------------------------------------------------------------------
        # given an integer for the pixel aspect ratio,
        # the returned pixel aspect ratio should be a float
        self.kwargs["pixel_aspect"] = 1
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
        self.assertIsInstance(an_image_format.pixel_aspect, float)
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_argument_zero(self):
        """testing if a ValueError will be raised when the pixel_aspect
        argument is zero
        """
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio can not be zero
        self.kwargs["pixel_aspect"] = 0
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_attribute_zero(self):
        """testing the pixel_aspect attribute against being zero
        """
        
        self.assertRaises(ValueError, setattr, self.mock_imageFormat,
                          "pixel_aspect", 0 )
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_argument_negative(self):
        """testing if a ValueError will be raised when pixel_aspect argument
        against being negative
        """
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio can not be negative
        self.kwargs["pixel_aspect"] = -1.0
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
        
        self.kwargs["pixel_aspect"] = -1
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_attribute_negative(self):
        """testing pixel_aspect attribute against being negative
        """
        
        # also test the attribute
        self.assertRaises(ValueError, setattr, self.mock_imageFormat,
                          "pixel_aspect", -1.0 )
        
        self.assertRaises(ValueError, setattr, self.mock_imageFormat,
                          "pixel_aspect", -1 )
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_attribute_if_being_initialized_correctly(self):
        """testing if pixel_aspect attribute is correctly initialized to its
        default value when omitted
        """
        
        self.kwargs.pop("pixel_aspect")
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
        default_value = 1.0
        self.assertEquals(an_image_format.pixel_aspect, default_value)
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_omit(self):
        """testing the print resolution against being omited
        """
        
        #----------------------------------------------------------------------
        # the print resolution can be ommited
        self.kwargs.pop("print_resolution")
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
        
        print_resolution = an_image_format.print_resolution
        
        # and the default value should be a float instance
        self.assertIsInstance(an_image_format.print_resolution, float)
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_argument_accepts_int_float_only(self):
        """testing the print_resolution argument accepts integer or float only
        """
        
        #----------------------------------------------------------------------
        # the print resolution should be initialized with an integer or a float
        self.kwargs["print_resolution"] = "300.0"
        
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
        
        self.kwargs["print_resolution"] = 300
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
        
        self.kwargs["print_resolution"] = 300.0
        an_image_format = imageFormat.ImageFormat(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_argument_zero(self):
        """testing the print_resolution argument being zero
        """
        self.kwargs["print_resolution"] = 0
        #----------------------------------------------------------------------
        # the print resolution can not be zero
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_attribute_zero(self):
        """testing the print_resolution attribute being zero
        """
        
        # also test the attribute
        self.assertRaises(ValueError, setattr, self.mock_imageFormat,
                          "print_resolution", 0)
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_argument_negative(self):
        """testing the print_resolution argument being negative
        """
        
        #----------------------------------------------------------------------
        # the print resolution can not be negative
        self.kwargs["print_resolution"] = -300
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
        
        self.kwargs["print_resolution"] = -300.0
        self.assertRaises(ValueError, imageFormat.ImageFormat, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_attribute_negative(self):
        """testing the print_resolution attribute being negative
        """
        
        self.assertRaises(ValueError, setattr, self.mock_imageFormat,
                          "print_resolution", -300)
        
        self.assertRaises(ValueError, setattr, self.mock_imageFormat,
                          "print_resolution", -300.0)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing equality operator
        """
        
        image_format1 = imageFormat.ImageFormat(**self.kwargs)
        image_format2 = imageFormat.ImageFormat(**self.kwargs)
        
        self.kwargs.update({
            "width": 720,
            "height": 480,
            "pixel_aspect": 0.888888,
        })
        image_format3 = imageFormat.ImageFormat(**self.kwargs)
        
        self.assertTrue(image_format1==image_format2)
        self.assertFalse(image_format1==image_format3)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing inequality operator
        """
        
        image_format1 = imageFormat.ImageFormat(**self.kwargs)
        image_format2 = imageFormat.ImageFormat(**self.kwargs)
        
        self.kwargs.update({
            "name": "NTSC",
            "description": "The famous NTSC image format",
            "width": 720,
            "height": 480,
            "pixel_aspect": 0.888888,
        })
        image_format3 = imageFormat.ImageFormat(**self.kwargs)
        
        self.assertFalse(image_format1!=image_format2)
        self.assertTrue(image_format1!=image_format3)
    
    
    