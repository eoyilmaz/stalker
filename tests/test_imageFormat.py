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
from stalker.models import imageFormat





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
        self.pixelAspect = 1.0
        self.printResolution = 300
    
    
    
    #----------------------------------------------------------------------
    def test_name_str_or_unicode(self):
        """testing the name attribute against not being string or unicode
        """
        
        #----------------------------------------------------------------------
        # the name should be string or unicode
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          1920,
                          self.width,
                          self.height,
                          self.pixelAspect,
                          self.printResolution)
    
    
    
    #----------------------------------------------------------------------
    def test_name_property_str_or_unicode(self):
        """testing the name property against not being string or unicode
        """
        
        # test also the name property
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'name', 1920)
    
    
    
    #----------------------------------------------------------------------
    def test_name_empty_sting(self):
        """testing the name attribute against being an empty string
        """
        
        #----------------------------------------------------------------------
        # the name could not be an empty string
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          '',
                          self.width,
                          self.height,
                          self.pixelAspect,
                          self.printResolution)
    
    
    
    #----------------------------------------------------------------------
    def test_name_property_empty_string(self):
        """testing the name property against being an empty string
        """
        
        # test also the name property
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'name', '')
    
    
    
    #----------------------------------------------------------------------
    def test_width_int_or_float(self):
        """testing the width attribute against not being an integer or float
        """
        
        #----------------------------------------------------------------------
        # the width should be an integer or float
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          self.name,
                          '1920',
                          self.height,
                          self.pixelAspect,
                          self.printResolution)
        
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          self.name,
                          [1920],
                          self.height,
                          self.pixelAspect,
                          self.printResolution)
    
    
    
    #----------------------------------------------------------------------
    def test_width_property_int_or_float(self):
        """testing the width property against not being an integer or float
        """
        
        # test also the property
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'width', '1920')
        self.assertRaises(ValueError, setattr, anImageFormat, 'width', [1920])
    
    
    
    #----------------------------------------------------------------------
    def test_width_float_to_int_conversion(self):
        """testing the width attribute against being converted to int
        successfuly
        """
        
        #----------------------------------------------------------------------
        # the given floats should be converted to integer
        aFloatWidth = 1920.0
        
        anImageFormat = imageFormat.ImageFormat(
            self.name, aFloatWidth, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertTrue(isinstance(anImageFormat.width, int))
    
    
    
    #----------------------------------------------------------------------
    def test_width_property_float_to_int_conversion(self):
        """testing the width property against being converted to int
        successfuly
        """
        
        #----------------------------------------------------------------------
        # the given floats should be converted to integer
        aFloatWidth = 1920.0
        
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        anImageFormat.width = aFloatWidth
        self.assertTrue(isinstance(anImageFormat.width, int))
    
    
    
    #----------------------------------------------------------------------
    def test_width_being_zero(self):
        """testing the width attribute against being zero
        """
        
        #----------------------------------------------------------------------
        # could not be zero
        self.assertRaises(ValueError, imageFormat.ImageFormat, self.name,
                          0, self.height, self.pixelAspect,
                          self.printResolution)
    
    
    #----------------------------------------------------------------------
    def test_width_property_being_zero(self):
        """testing the width property against being zero
        """
        
        # also test the property for this
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'width', 0)
    
    
    
    #----------------------------------------------------------------------
    def test_width_being_negative(self):
        """testing the width attribute against being negative
        """
        
        #----------------------------------------------------------------------
        # could not be negative
        self.assertRaises(ValueError, imageFormat.ImageFormat, self.name, -10,
                          self.height, self.pixelAspect, self.printResolution)
    
    
    
    #----------------------------------------------------------------------
    def test_width_property_being_negative(self):
        """testing the width property against being negative
        """
        
        # also test the property for this
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'width', -100)
    
    
    
    #----------------------------------------------------------------------
    def test_height_int_or_float(self):
        """testing the height attribute against not being integer or float
        """
        
        #----------------------------------------------------------------------
        # the height should be an integer
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          self.name,
                          self.width,
                          '1080',
                          self.pixelAspect,
                          self.printResolution)
        
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          self.name,
                          self.width,
                          [1080],
                          self.pixelAspect,
                          self.printResolution)
    
    
    
    #----------------------------------------------------------------------
    def test_height_property_int_or_float(self):
        """testing the height property against not being an integer or float
        """
        
        # test also the property
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'height', '1080')
        self.assertRaises(ValueError, setattr, anImageFormat, 'height', [1080])
    
    
    
    #----------------------------------------------------------------------
    def test_height_float_to_int_conversion(self):
        """testing the height attribute against being converted to int
        successfuly
        """
        
        #----------------------------------------------------------------------
        # the given floats should be converted to integer
        aFloatHeight = 1080.0
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, aFloatHeight, self.pixelAspect,
            self.printResolution
        )
        
        self.assertTrue(isinstance(anImageFormat.height, int))
    
    
    
    #----------------------------------------------------------------------
    def test_height_property_float_to_int_conversion(self):
        """testing the height property against being converted to int
        successfuly
        """
        
        aFloatHeight = 1080.0
        
        # also test the property for this
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        anImageFormat.height = aFloatHeight
        self.assertTrue(isinstance(anImageFormat.height, int))
    
    
    
    #----------------------------------------------------------------------
    def test_height_being_zero(self):
        """testing the height attribute against being zero
        """
        
        #----------------------------------------------------------------------
        # could not be zero
        self.assertRaises(ValueError, imageFormat.ImageFormat,
                          self.name, self.width, 0, self.pixelAspect,
                          self.printResolution)
    
    
    
    #----------------------------------------------------------------------
    def test_height_property_being_zero(self):
        """testing the height property against being zero
        """
        
        # also test the property for this
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'height', 0)
    
    
    
    #----------------------------------------------------------------------
    def test_height_being_negative(self):
        """testing the height attribute against being negative
        """
        
        #----------------------------------------------------------------------
        # could not be negative
        self.assertRaises(ValueError, imageFormat.ImageFormat,
                          self.name, self.width, -10, self.pixelAspect,
                          self.printResolution)
    
    
    
    #----------------------------------------------------------------------
    def test_height_property_being_negative(self):
        """testing the height property against being negative
        """
        
        # also test the property for this
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'height', -100)
    
    
    
    #----------------------------------------------------------------------
    def test_deviceAspectRatio_float(self):
        """testing the device aspect ratio attribute against not being a float
        value
        """
        
        #----------------------------------------------------------------------
        # the device aspect should be a float
        #name = 'NTSC'
        #width = 720
        #height = 480
        #pixelAspect = 0.9
        #printResolution = 300
        
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution)
        
        self.assertTrue(isinstance(anImageFormat.deviceAspect, float))
    
    
    
    #----------------------------------------------------------------------
    def test_deviceAspectRatio_correctly_calculated(self):
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
        pixelAspect = 1.0
        printResolution = 300
        
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        # the device aspect for this setup should be around 1.7778
        self.assertEquals( "%1.4g" % anImageFormat.deviceAspect, "%1.4g" % 1.7778 )
        
        
        #----------------------------------------------------------------------
        # test PAL
        name = 'PAL'
        width = 720
        height = 576
        pixelAspect = 1.0667
        printResolution = 300
        
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        # the device aspect for this setup should be around 4/3
        self.assertEquals("%1.4g" % anImageFormat.deviceAspect, "%1.4g" % 1.3333)
    
    
    
    #----------------------------------------------------------------------
    def test_deviceAspectRatio_updates(self):
        """testing deviceAspectRatio attribute being updated on changes to any
        of the witdh, height or pixelAspect
        """
        
        #----------------------------------------------------------------------
        # just changing one of the width or height should be causing an update
        # in deviceAspect
        
        # start with PAL
        name = 'PAL'
        width = 720
        height = 576
        pixelAspect = 1.0667
        printResolution = 300
        
        anImageFormat = imageFormat.ImageFormat(
            name, width, height, pixelAspect, printResolution
        )
        
        previousDeviceAspect = anImageFormat.deviceAspect
        
        # change to HD
        anImageFormat.width = 1920
        anImageFormat.height = 1080
        anImageFormat.pixelAspect = 1.0
        self.assertTrue(abs(anImageFormat.deviceAspect - 1.77778) < 0.001)
        self.assertNotEqual(anImageFormat.deviceAspect, previousDeviceAspect)
    
    
    
    #----------------------------------------------------------------------
    def test_deviceAspectRatio_write_protected(self):
        """testing if deviceAspectRatio is write protected
        """
        
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        #----------------------------------------------------------------------
        # the device aspect should be write propetected
        self.assertRaises(AttributeError,
                          setattr, anImageFormat, 'deviceAspect', 10)
    
    
    
    #----------------------------------------------------------------------
    def test_pixelAspect_int_float(self):
        """testing the pixel aspect ratio against not being integer or float
        """
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio should be a given as float or integer number
        
        # any other variable type than int and float is not ok
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          self.name,
                          self.width,
                          self.height,
                          '1.0',
                          self.printResolution)
        
        # float is ok
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, 1.0, self.printResolution)
        
        # int is ok
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, 2, self.printResolution)
    
    
    
    #----------------------------------------------------------------------
    def test_pixelAspect_float_conversion(self):
        """testing the pixel aspect ratio conversion to float
        """
        
        #----------------------------------------------------------------------
        # given an integer for the pixel aspect ratio,
        # the returned pixel aspect ratio should be a float
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, int(1), self.printResolution)
        
        self.assertTrue(isinstance(anImageFormat.pixelAspect, float))
    
    
    
    #----------------------------------------------------------------------
    def test_pixelAspect_zero(self):
        """testing the pixel aspect ratio attribute being zero
        """
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio can not be zero
        self.assertRaises(ValueError, imageFormat.ImageFormat,
                          self.name, self.width, self.height, 0,
                          self.printResolution)
    
    
    
    #----------------------------------------------------------------------
    def test_pixelAspect_property_zero(self):
        """testing the pixelAspect property against being zero
        """
        
        # also test the property
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'pixelAspect', 0 )
    
    
    
    #----------------------------------------------------------------------
    def test_pixelAspect_negative(self):
        """testing pixelAspect attribute against being negative
        """
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio can not be negative
        self.assertRaises(ValueError, imageFormat.ImageFormat, self.name,
                          self.width, self.height, -1.0, self.printResolution)
        
        self.assertRaises(ValueError, imageFormat.ImageFormat, self.name,
                          self.width, self.height, -1, self.printResolution)
    
    
    
    #----------------------------------------------------------------------
    def test_pixelAspect_property_negative(self):
        """testing pixelAspect property against being negative
        """
        
        # also test the property
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'pixelAspect', -1.0 )
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'pixelAspect', -1 )
    
    
    
    #----------------------------------------------------------------------
    def test_printResolution_omit(self):
        """testing the print resolution against being omited
        """
        
        #----------------------------------------------------------------------
        # the print resolution can be ommited
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect
        )
        
        # then the default value is going to be used
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect
        )
        
        get_printResolution = anImageFormat.printResolution
        
        # and the default value should be a float instance
        self.assertTrue(isinstance(anImageFormat.printResolution, float))
    
    
    
    #----------------------------------------------------------------------
    def test_printResolution_int_float_initialize(self):
        """testing the printResolution attribute being initialized as integer
        or float
        """
        
        #----------------------------------------------------------------------
        # the print resolution should be initialized with an integer or a float
        self.assertRaises(ValueError, imageFormat.ImageFormat, self.name,
                          self.width, self.height, self.pixelAspect, '300.0')
        
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            float(self.printResolution)
        )
    
    
    
    #----------------------------------------------------------------------
    def test_printResolution_zero(self):
        """testing the printResolution attribute being zero
        """
        
        #----------------------------------------------------------------------
        # the print resolution can not be zero
        self.assertRaises(ValueError, imageFormat.ImageFormat, self.name,
                          self.width, self.height, self.pixelAspect, 0)
    
    
    
    #----------------------------------------------------------------------
    def test_printResolution_property_zero(self):
        """testing the printResolution property being zero
        """
        
        # also test the property
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'printResolution', 0)
    
    
    
    #----------------------------------------------------------------------
    def test_printResolution_negative(self):
        """testing the printResolution attribute being negative
        """
        
        #----------------------------------------------------------------------
        # the print resolution can not be negative
        self.assertRaises(ValueError, imageFormat.ImageFormat, self.name,
                          self.width, self.height, self.pixelAspect, -300)
        
        self.assertRaises(ValueError, imageFormat.ImageFormat, self.name,
                          self.width, self.height, self.pixelAspect, -300.0)
    
    
    
    #----------------------------------------------------------------------
    def test_printResolution_property_negative(self):
        """testing the printResolution property being negative
        """
        
        # also test the property
        anImageFormat = imageFormat.ImageFormat(
            self.name, self.width, self.height, self.pixelAspect,
            self.printResolution
        )
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'printResolution', -300)
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'printResolution', -300.0)
        
        
        