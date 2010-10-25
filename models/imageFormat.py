#-*- coding: utf-8 -*-
########################################################################
# 
# Copyright (C) 2010  Erkan Ozgur Yilmaz
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# 
########################################################################






########################################################################
class ImageFormat(object):
    """the image format class
    """
    
    #----------------------------------------------------------------------
    def __init__(self, name, width, height, pixelAspect, printResolution=300 ):
        
        self._name = self._checkName(name)
        self._width = self._checkWidth(width)
        self._height = self._checkHeight(height)
        self._pixelAspect = self._checkPixelAspect(pixelAspect)
        self._printResolution = self._checkPrintResolution(printResolution)
        self._deviceAspect = 1.0
        
        self._updateDeviceAspect()
        
    
    
    #----------------------------------------------------------------------
    def _updateDeviceAspect(self):
        """updates the device aspect ratio for the given width and height
        """
        self._deviceAspect = float(self._width) / float(self._height) \
            * float(self._pixelAspect)
    
    
    
    #----------------------------------------------------------------------
    def _checkName(self, name):
        """checks the given name
        """
        
        if not isinstance(name, (str, unicode)):
            raise(ValueError("name should be instance of str or unicode"))
        
        if name == '' or len(name) < 1:
            raise(ValueError("name should not be an empty string"))
        
        return name
    
    
    
    #----------------------------------------------------------------------
    def _checkWidth(self, width):
        """checks the given width
        """
        if not isinstance(width, (int, float)):
            raise(ValueError("width should be an instance of int or float"))
        
        if width <= 0:
            raise(ValueError("width shouldn't be zero or negative"))
        
        return int(width)
    
    
    
    #----------------------------------------------------------------------
    def _checkHeight(self, height):
        """checks the given height
        """
        if not isinstance(height, (int, float)):
            raise(ValueError("height should be an instance of int or float"))
        
        if height <= 0:
            raise(ValueError("height shouldn't be zero or negative"))
        
        return int(height)
    
    
    
    #----------------------------------------------------------------------
    def _checkPixelAspect(self, pixelAspect):
        """checks the given pixel aspect
        """
        if not isinstance(pixelAspect, (int, float)):
            raise(ValueError("pixelAspect should be an instance of int or \
            float"))
        
        if pixelAspect <= 0:
            raise(ValueError("pixelAspect can not be zero or a negative \
            value"))
        
        return float(pixelAspect)
    
    
    
    #----------------------------------------------------------------------
    def _checkPrintResolution(self, printResolution):
        """checks the print resolution
        """
        if not isinstance(printResolution, (int, float)):
            raise(ValueError("print resolution should be an instance of int \
            or float"))
        
        if printResolution <= 0:
            raise(ValueError("print resolution should not be zero or \
            negative"))
        
        return float(printResolution)
    
    
    
    #----------------------------------------------------------------------
    def name():
        def fget(self):
            """returns the name attribute
            """
            return self._name
        
        def fset(self, name):
            """sets the name attribute
            """
            self._name = self._checkName(name)
        
        doc = """this is a property to set and get the name of the
        imageFormat
        
        the name should be:
        * a string or unicode value
        * can not be None
        * can not be an empty string or empty unicode
        """
        
        return locals()
    
    name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def width():
        def fget(self):
            """returns the width
            """
            return self._width
        
        def fset(self, width):
            """sets the width
            """
            self._width = self._checkWidth(width)
            # also update the deviceAspect
            self._updateDeviceAspect()
        
        doc = """this is a property to set and get the width of the
        imageFormat
        
        * the width should be set to a positif non-zero integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise a ValueError
        """
        
        return locals()
    
    width = property(**width())
    
    
    
    #----------------------------------------------------------------------
    def height():
        def fget(self):
            """returns the height
            """
            return self._height
        
        def fset(self, height):
            """sets the height
            """
            self._height = self._checkHeight(height)
            
            # also update the deviceAspect
            self._updateDeviceAspect()
        
        doc = """this is a property to set and get the height of the
        imageFormat
        
        * the height should be set to a positif non-zero integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise a ValueError
        """
        
        return locals()
    
    height = property(**height())
    
    
    
    #----------------------------------------------------------------------
    def pixelAspect():
        def fget(self):
            """returns the pixelAspect ratio
            """
            return self._pixelAspect
        
        def fset(self, pixelAspect):
            """sets the pixelAspect ratio
            """
            self._pixelAspect = self._checkPixelAspect(pixelAspect)
            
            # also update the deviceAspect
            self._updateDeviceAspect()
        
        doc = """this is a property to set and get the pixelAspect of the
        imageFormat
        
        * the pixelAspect should be set to a positif non-zero float
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise a ValueError
        """
        
        return locals()
    
    pixelAspect = property(**pixelAspect())
    
    
    
    #----------------------------------------------------------------------
    @property
    def deviceAspect(self):
        """returns the device aspect
        
        because the deviceAspect is calculated from the width/height*pixel
        formula, this property is read-only.
        """
        return self._deviceAspect
    
    
    
    #----------------------------------------------------------------------
    def printResolution():
        
        def fget(self):
            """returns the print resolution
            """
            return self._printResolution
        
        def fset(self, printResolution):
            """sets the print resolution
            """
            self._printResolution = self._checkPrintResolution(printResolution)
        
        doc = """this is a property to set and get the printResolution of the
        imageFormat
        
        * it should be set to a positif non-zero float or integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise a ValueError
        """
        
        return locals()
    
    printResolution = property(**printResolution())
    
    
    
    