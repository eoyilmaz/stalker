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
    def test_name(self):
        """tests the name attribute
        """
        
        #----------------------------------------------------------------------
        # some proper values
        name = 'HD'
        width = 1920
        height = 1080
        pixelAspect = 1.0
        printResolution = 300
        
        #----------------------------------------------------------------------
        # the name should be string or unicode
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          1920,
                          width,
                          height,
                          pixelAspect,
                          printResolution)
        
        # test also the name property
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        self.assertRaises(ValueError, setattr, anImageFormat, 'name', 1920)
        
        #----------------------------------------------------------------------
        # the name could not be an empty string
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          '',
                          width,
                          height,
                          pixelAspect,
                          printResolution)
        
        # test also the name property
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'name', '')
    
    
    
    #----------------------------------------------------------------------
    def test_width(self):
        """tests the width attribute
        """
        
        #----------------------------------------------------------------------
        # some proper values
        name = 'HD'
        width = 1920
        height = 1080
        pixelAspect = 1.0
        printResolution = 300
        
        #----------------------------------------------------------------------
        # the width should be an integer
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          name,
                          '1920',
                          height,
                          pixelAspect,
                          printResolution)
        
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          name,
                          [1920],
                          height,
                          pixelAspect,
                          printResolution)
        
        # test also the property
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'width', '1920')
        self.assertRaises(ValueError, setattr, anImageFormat, 'width', [1920])
        
        #----------------------------------------------------------------------
        # the given floats should be converted to integer
        aFloatWidth = 1920.0
        anImageFormat = imageFormat.ImageFormat(name, aFloatWidth, height,
                                                pixelAspect, printResolution)
        
        self.assertTrue(isinstance(anImageFormat.width, int))
        
        # also test the property for this
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        anImageFormat.width = aFloatWidth
        self.assertTrue(isinstance(anImageFormat.width, int))
        
        
        #----------------------------------------------------------------------
        # could not be zero
        self.assertRaises(ValueError, imageFormat.ImageFormat, name, 0, height,
                          pixelAspect, printResolution)
        
        # also test the property for this
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'width', 0)
        
        #----------------------------------------------------------------------
        # could not be negative
        self.assertRaises(ValueError, imageFormat.ImageFormat, name, -10,
                          height, pixelAspect, printResolution)
        
        # also test the property for this
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'width', -100)
    
    
    
    #----------------------------------------------------------------------
    def test_height(self):
        """tests the height attribute
        """
        
        #----------------------------------------------------------------------
        # some proper values
        name = 'HD'
        width = 1920
        height = 1080
        pixelAspect = 1.0
        printResolution = 300
        
        #----------------------------------------------------------------------
        # the height should be an integer
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          name,
                          width,
                          '1080',
                          pixelAspect,
                          printResolution)
        
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          name,
                          width,
                          [1080],
                          pixelAspect,
                          printResolution)
        
        # test also the property
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'height', '1080')
        self.assertRaises(ValueError, setattr, anImageFormat, 'height', [1080])
        
        #----------------------------------------------------------------------
        # the given floats should be converted to integer
        aFloatHeight = 1080.0
        anImageFormat = imageFormat.ImageFormat(name, width, aFloatHeight,
                                                pixelAspect, printResolution)
        
        self.assertTrue(isinstance(anImageFormat.height, int))
        
        # also test the property for this
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        anImageFormat.height = aFloatHeight
        self.assertTrue(isinstance(anImageFormat.height, int))
        
        
        #----------------------------------------------------------------------
        # could not be zero
        self.assertRaises(ValueError, imageFormat.ImageFormat, name, width, 0,
                          pixelAspect, printResolution)
        
        # also test the property for this
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'height', 0)
        
        #----------------------------------------------------------------------
        # could not be negative
        self.assertRaises(ValueError, imageFormat.ImageFormat, name, width,
                          -10, pixelAspect, printResolution)
        
        # also test the property for this
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertRaises(ValueError, setattr, anImageFormat, 'height', -100)
    
    
    
    #----------------------------------------------------------------------
    def test_deviceAspectRatio(self):
        """tests the device aspect ratio attribute
        """
        
        #----------------------------------------------------------------------
        # the device aspect should be a float
        name = 'NTSC'
        width = 720
        height = 480
        pixelAspect = 0.9
        printResolution = 300
        
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertTrue(isinstance(anImageFormat.deviceAspect, float))
        
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
        self.assertAlmostEquals(anImageFormat.deviceAspect, 1.7778)
        
        
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
        self.assertAlmostEquals(anImageFormat.deviceAspect, 1.3333)
        
        
        #----------------------------------------------------------------------
        # the device aspect should be write propetected
        self.assertRaises(AttributeError,
                          setattr, anImageFormat, 'deviceAspect', 10)
        
    
    
    #----------------------------------------------------------------------
    def test_pixelAspectRatio(self):
        """tests the pixel aspect ratio
        """
        
        #----------------------------------------------------------------------
        # some proper values
        name = 'HD'
        width = 1920
        height = 1080
        pixelAspect = 1.0
        printResolution = 300
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio should be a given as float or integer number
        
        # any other variable type than int and float is not ok
        self.assertRaises(ValueError,
                          imageFormat.ImageFormat,
                          name,
                          width,
                          height,
                          '1.0',
                          printResolution)
        
        # float is ok
        anImageFormat = imageFormat.ImageFormat(name, width, height, 1.0,
                                                printResolution)
        
        # int is ok
        anImageFormat = imageFormat.ImageFormat(name, width, height, 2,
                                                printResolution)
        
        #----------------------------------------------------------------------
        # given an integer for the pixel aspect ratio,
        # the returned pixel aspect ratio should be a float
        anImageFormat = imageFormat.ImageFormat(name, width, height, int(1),
                                                printResolution)
        
        self.assertTrue(isinstance(anImageFormat.pixelAspectRatio, float))
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio can not be zero
        self.assertRaises(ValueError, imageFormat.ImageFormat, name, width,
                          height, 0, printResolution)
        
        # also test the property
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'pixelAspectRatio', 0 )
        
        #----------------------------------------------------------------------
        # the pixel aspect ratio can not be negative
        self.assertRaises(ValueError, imageFormat.ImageFormat, name, width,
                          height, -1.0, printResolution)
        
        self.assertRaises(ValueError, imageFormat.ImageFormat, name, width,
                          height, -1, printResolution)
        
        # also test the property
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'pixelAspectRatio', -1.0 )
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'pixelAspectRatio', -1 )
    
    
    
    #----------------------------------------------------------------------
    def test_printResolution(self):
        """tests the print resolution
        """
        #----------------------------------------------------------------------
        # some proper values
        name = 'HD'
        width = 1920
        height = 1080
        pixelAspect = 1.0
        printResolution = 300
        
        
        #----------------------------------------------------------------------
        # the print resolution can be ommited
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect)
        
        # then the default value is going to be used
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect)
        
        get_printResolution = anImageFormat.printResolution
        
        # and the default value should be a float instance
        self.assertTrue(isinstance(anImageFormat.printResolution, float))
        
        
        
        #----------------------------------------------------------------------
        # the print resolution should be initialized with an integer or a float
        self.assertRaises(ValueError, imageFormat.ImageFormat, name, width,
                          height, pixelAspect, '300.0')
        
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect,
                                                float(printResolution))
        
        
        
        #----------------------------------------------------------------------
        # the print resolution can not be zero
        self.assertRaises(ValueError, imageFormat.ImageFormat, name, width,
                          height, pixelAspect, 0)
        
        # also test the property
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'printResolution', 0)
        
        #----------------------------------------------------------------------
        # the print resolution can not be negative
        self.assertRaises(ValueError, imageFormat.ImageFormat, name, width,
                          height, pixelAspect, -300)
        
        self.assertRaises(ValueError, imageFormat.ImageFormat, name, width,
                          height, pixelAspect, -300.0)
        
        # also test the property
        anImageFormat = imageFormat.ImageFormat(name, width, height,
                                                pixelAspect, printResolution)
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'printResolution', -300)
        
        self.assertRaises(ValueError, setattr, anImageFormat,
                          'printResolution', -300.0)
        
        
        