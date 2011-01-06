#-*- coding: utf-8 -*-



import unittest
from stalker.core.models import imageFormat





########################################################################
class ImageFormatTest(unittest.TestCase):
    """the test case for the image format
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup some default values
        """
        #----------------------------------------------------------------------
        # some proper values
        self.name = 'HD'
        self.width = 1920
        self.height = 1080
        self.pixel_aspect = 1.0
        self.print_resolution = 300
    
    
    
    #----------------------------------------------------------------------
    def test_width_argument_accepts_int_or_float_only(self):
        """testing the width argument accepts integer or float and raises
        ValueError in any other case
        """
        
        #----------------------------------------------------------------------
        # the width should be an integer or float
        test_values = ['1920', [1920], {}, ()]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                imageFormat.ImageFormat,
                name=self.name,
                width=test_values,
                height=self.height,
                pixel_aspect=self.pixel_aspect,
                print_resolution=self.print_resolution
            )
    
    
    
    #----------------------------------------------------------------------
    def test_width_property_int_or_float(self):
        """testing the width property against not being an integer or float
        """
        
        # test also the property
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        test_values = ['1920', [1920], {}, ()]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                an_image_format,
                'width',
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_width_argument_float_to_int_conversion(self):
        """testing for width argument is given as a float and converted to int
        successfuly
        """
        
        #----------------------------------------------------------------------
        # the given floats should be converted to integer
        a_float_width = 1920.0
        
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=a_float_width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertTrue(isinstance(an_image_format.width, int))
    
    
    
    #----------------------------------------------------------------------
    def test_width_property_float_to_int_conversion(self):
        """testing the width property against being converted to int
        successfuly
        """
        
        #----------------------------------------------------------------------
        # the given floats should be converted to integer
        a_float_width = 1920.0
        
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        an_image_format.width = a_float_width
        self.assertTrue(isinstance(an_image_format.width, int))
    
    
    
    #----------------------------------------------------------------------
    def test_width_argument_being_zero(self):
        """testing the width argument against being zero
        """
        
        #----------------------------------------------------------------------
        # could not be zero
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=0,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
    
    
    #----------------------------------------------------------------------
    def test_width_property_being_zero(self):
        """testing the width property against being zero
        """
        
        # also test the property for this
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertRaises(ValueError, setattr, an_image_format, 'width', 0)
    
    
    
    #----------------------------------------------------------------------
    def test_width_argument_being_negative(self):
        """testing the width argument against being negative
        """
        
        #----------------------------------------------------------------------
        # could not be negative
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=-10,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
    
    
    
    #----------------------------------------------------------------------
    def test_width_property_being_negative(self):
        """testing the width property against being negative
        """
        
        # also test the property for this
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertRaises(ValueError, setattr, an_image_format, 'width', -100)
    
    
    
    #----------------------------------------------------------------------
    def test_height_argument_int_or_float(self):
        """testing the height argument against not being integer or float
        """
        
        test_values = ['1080', [1080], {}, ()]
        
        #----------------------------------------------------------------------
        # the height should be an integer
        
        
        for test_value in test_values:
            
            self.assertRaises(
                ValueError,
                imageFormat.ImageFormat,
                name=self.name,
                width=self.width,
                height=test_value,
                pixel_aspect=self.pixel_aspect,
                print_resolution=self.print_resolution
            )
    
    
    
    #----------------------------------------------------------------------
    def test_height_property_int_or_float(self):
        """testing the height property against not being an integer or float
        """
        
        # test also the property
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertRaises(
            ValueError, setattr, an_image_format, 'height', '1080'
        )
        self.assertRaises(
            ValueError, setattr, an_image_format, 'height', [1080]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_height_argument_float_to_int_conversion(self):
        """testing the height argument against being converted to int
        successfuly
        """
        
        #----------------------------------------------------------------------
        # the given floats should be converted to integer
        a_float_height = 1080.0
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=a_float_height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertTrue(isinstance(an_image_format.height, int))
    
    
    
    #----------------------------------------------------------------------
    def test_height_property_float_to_int_conversion(self):
        """testing the height property against being converted to int
        successfuly
        """
        
        a_float_height = 1080.0
        
        # also test the property for this
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        an_image_format.height = a_float_height
        self.assertTrue(isinstance(an_image_format.height, int))
    
    
    
    #----------------------------------------------------------------------
    def test_height_argument_being_zero(self):
        """testing the height argument against being zero
        """
        
        #----------------------------------------------------------------------
        # could not be zero
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=self.width,
            height=0,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
    
    
    
    #----------------------------------------------------------------------
    def test_height_property_being_zero(self):
        """testing the height property against being zero
        """
        
        # also test the property for this
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertRaises(ValueError, setattr, an_image_format, 'height', 0)
    
    
    
    #----------------------------------------------------------------------
    def test_height_argument_being_negative(self):
        """testing the height argument against being negative
        """
        
        #----------------------------------------------------------------------
        # could not be negative
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=self.width,
            height=-10,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
    
    
    
    #----------------------------------------------------------------------
    def test_height_property_being_negative(self):
        """testing the height property against being negative
        """
        
        # also test the property for this
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertRaises(ValueError, setattr, an_image_format, 'height', -100)
    
    
    
    #----------------------------------------------------------------------
    def test_device_aspect_property_float(self):
        """testing the device aspect ratio property against not being a float
        value
        """
        
        #----------------------------------------------------------------------
        # the device aspect should be a float
        #name = 'NTSC'
        #width = 720
        #height = 480
        #pixel_aspect = 0.9
        #print_resolution = 300
        
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertTrue(isinstance(an_image_format.device_aspect, float))
    
    
    
    #----------------------------------------------------------------------
    def test_device_aspect_ratio_correctly_calculated(self):
        """testing the device aspect ratio against being correctly calculated
        """
        
        #----------------------------------------------------------------------
        # the device aspect is something calculated using width, height and
        # the pixel aspect ratio
        
        #----------------------------------------------------------------------
        # Test HD
        name = 'HD'
        width = 1920
        height = 1080
        pixel_aspect = 1.0
        print_resolution = 300
        
        an_image_format = imageFormat.ImageFormat(
            name=name,
            width=width,
            height=height,
            pixel_aspect=pixel_aspect,
            print_resolution=print_resolution
        )
        
        # the device aspect for this setup should be around 1.7778
        self.assertEquals( "%1.4g" % an_image_format.device_aspect, "%1.4g" % 1.7778 )
        
        
        #----------------------------------------------------------------------
        # test PAL
        name = 'PAL'
        width = 720
        height = 576
        pixel_aspect = 1.0667
        print_resolution = 300
        
        an_image_format = imageFormat.ImageFormat(
            name=name,
            width=width,
            height=height,
            pixel_aspect=pixel_aspect,
            print_resolution=print_resolution
        )
        
        # the device aspect for this setup should be around 4/3
        self.assertEquals("%1.4g" % an_image_format.device_aspect, "%1.4g" % 1.3333)
    
    
    
    #----------------------------------------------------------------------
    def test_device_aspect_property_updates(self):
        """testing device_aspect_ratio property being updated on changes to any
        of the witdh, height or pixel_aspect
        """
        
        #----------------------------------------------------------------------
        # just changing one of the width or height should be causing an update
        # in device_aspect
        
        # start with PAL
        name = 'PAL'
        width = 720
        height = 576
        pixel_aspect = 1.0667
        print_resolution = 300
        
        an_image_format = imageFormat.ImageFormat(
            name=name,
            width=width,
            height=height,
            pixel_aspect=pixel_aspect,
            print_resolution=print_resolution
        )
        
        previous_device_aspect = an_image_format.device_aspect
        
        # change to HD
        an_image_format.width = 1920
        an_image_format.height = 1080
        an_image_format.pixel_aspect = 1.0
        
        self.assertTrue(abs(an_image_format.device_aspect - 1.77778) < 0.001)
        
        self.assertNotEqual(
            an_image_format.device_aspect,
            previous_device_aspect
        )
    
    
    
    #----------------------------------------------------------------------
    def test_device_aspect_property_write_protected(self):
        """testing if device_aspect property is write protected
        """
        
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        #----------------------------------------------------------------------
        # the device aspect should be write propetected
        self.assertRaises(AttributeError,
                          setattr, an_image_format, 'device_aspect', 10)
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_int_float(self):
        """testing the pixel aspect ratio against not being integer or float
        """
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio should be a given as float or integer number
        
        # any other variable type than int and float is not ok
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect='1.0',
            print_resolution=self.print_resolution
        )
        
        # float is ok
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=1.0,
            print_resolution=self.print_resolution
        )
        
        # int is ok
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=2,
            print_resolution=self.print_resolution
        )
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_float_conversion(self):
        """testing the pixel aspect ratio conversion to float
        """
        
        #----------------------------------------------------------------------
        # given an integer for the pixel aspect ratio,
        # the returned pixel aspect ratio should be a float
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=int(1),
            print_resolution=self.print_resolution
        )
        
        self.assertTrue(isinstance(an_image_format.pixel_aspect, float))
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_argument_zero(self):
        """testing if a ValueError will be raised when the pixel_aspect
        argument is zero
        """
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio can not be zero
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=0,
            print_resolution=self.print_resolution
        )
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_property_zero(self):
        """testing the pixel_aspect property against being zero
        """
        
        # also test the property
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertRaises(ValueError, setattr, an_image_format,
                          'pixel_aspect', 0 )
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_argument_negative(self):
        """testing if a ValueError will be raised when pixel_aspect argument
        against being negative
        """
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio can not be negative
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=-1.0,
            print_resolution=self.print_resolution
        )
        
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=-1,
            print_resolution=self.print_resolution
        )
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_property_negative(self):
        """testing pixel_aspect property against being negative
        """
        
        # also test the property
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertRaises(ValueError, setattr, an_image_format,
                          'pixel_aspect', -1.0 )
        
        self.assertRaises(ValueError, setattr, an_image_format,
                          'pixel_aspect', -1 )
    
    
    
    #----------------------------------------------------------------------
    def test_pixel_aspect_if_being_initialized_correctly(self):
        """testing if the pixel_aspect is correctly initialized to its default
        value when omitted
        """
        
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height
        )
        
        default_value = 1.0
        
        self.assertEquals(an_image_format.pixel_aspect, default_value)
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_omit(self):
        """testing the print resolution against being omited
        """
        
        #----------------------------------------------------------------------
        # the print resolution can be ommited
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect
        )
        
        # then the default value is going to be used
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect
        )
        
        get_print_resolution = an_image_format.print_resolution
        
        # and the default value should be a float instance
        self.assertTrue(isinstance(an_image_format.print_resolution, float))
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_argument_accepts_int_float_only(self):
        """testing the print_resolution argument accepts integer or float only
        """
        
        #----------------------------------------------------------------------
        # the print resolution should be initialized with an integer or a float
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution='300.0'
        )
        
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=float(self.print_resolution)
        )
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_argument_zero(self):
        """testing the print_resolution argument being zero
        """
        
        #----------------------------------------------------------------------
        # the print resolution can not be zero
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=0
        )
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_property_zero(self):
        """testing the print_resolution property being zero
        """
        
        # also test the property
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertRaises(ValueError, setattr, an_image_format,
                          'print_resolution', 0)
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_argument_negative(self):
        """testing the print_resolution argument being negative
        """
        
        #----------------------------------------------------------------------
        # the print resolution can not be negative
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=-300
        )
        
        self.assertRaises(
            ValueError,
            imageFormat.ImageFormat,
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=-300.0
        )
    
    
    
    #----------------------------------------------------------------------
    def test_print_resolution_property_negative(self):
        """testing the print_resolution property being negative
        """
        
        # also test the property
        an_image_format = imageFormat.ImageFormat(
            name=self.name,
            width=self.width,
            height=self.height,
            pixel_aspect=self.pixel_aspect,
            print_resolution=self.print_resolution
        )
        
        self.assertRaises(ValueError, setattr, an_image_format,
                          'print_resolution', -300)
        
        self.assertRaises(ValueError, setattr, an_image_format,
                          'print_resolution', -300.0)
        
        
        