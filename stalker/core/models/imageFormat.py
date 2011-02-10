#-*- coding: utf-8 -*-



from stalker.core.models import entity





########################################################################
class ImageFormat(entity.Entity):
    """Common image formats for the projects.
    
    adds up this parameters to the SimpleEntity:
    
    :param width: the width of the format, it cannot be zero or negative, if a
      float number is given it will be converted to integer
    
    :param height: the height of the format, it cannot be zero or negative, if
      a float number is given it will be converted to integer
    
    :param pixel_aspect: the pixel aspect ratio of the current ImageFormat
      object, it can not be zero or negative, and if given as an integer it
      will be converted to a float, the default value is 1.0
    
    :param print_resolution: the print resolution of the ImageFormat given as
      DPI (dot-per-inch). It can not be zero or negative
    
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 width=None,
                 height=None,
                 pixel_aspect=1.0,
                 print_resolution=300,
                 **kwargs
                 ):
        
        super(ImageFormat,self).__init__(**kwargs)
        
        self._width = self._validate_width(width)
        self._height = self._validate_height(height)
        self._pixel_aspect = self._validate_pixel_aspect(pixel_aspect)
        self._print_resolution = \
            self._validate_print_resolution(print_resolution)
        self._device_aspect = 1.0
        
        self._update_device_aspect()
        
    
    
    #----------------------------------------------------------------------
    def _update_device_aspect(self):
        """updates the device aspect ratio for the given width and height
        """
        self._device_aspect = float(self._width) / float(self._height) \
            * float(self._pixel_aspect)
    
    
    
    #----------------------------------------------------------------------
    def _validate_width(self, width):
        """validates the given width
        """
        if not isinstance(width, (int, float)):
            raise ValueError("width should be an instance of int or float")
        
        if width <= 0:
            raise ValueError("width shouldn't be zero or negative")
        
        return int(width)
    
    
    
    #----------------------------------------------------------------------
    def _validate_height(self, height):
        """validates the given height
        """
        if not isinstance(height, (int, float)):
            raise ValueError("height should be an instance of int or float")
        
        if height <= 0:
            raise ValueError("height shouldn't be zero or negative")
        
        return int(height)
    
    
    
    #----------------------------------------------------------------------
    def _validate_pixel_aspect(self, pixel_aspect):
        """validates the given pixel aspect
        """
        if not isinstance(pixel_aspect, (int, float)):
            raise ValueError("pixel_aspect should be an instance of int or "
                             "float")
        
        if pixel_aspect <= 0:
            raise ValueError("pixel_aspect can not be zero or a negative "
                             "value")
        
        return float(pixel_aspect)
    
    
    
    #----------------------------------------------------------------------
    def _validate_print_resolution(self, print_resolution):
        """validates the print resolution
        """
        if not isinstance(print_resolution, (int, float)):
            raise ValueError("print resolution should be an instance of int "
                             "or float")
        
        if print_resolution <= 0:
            raise ValueError("print resolution should not be zero or "
                             "negative")
        
        return float(print_resolution)
    
    
    
    #----------------------------------------------------------------------
    def width():
        def fget(self):
            """returns the width
            """
            return self._width
        
        def fset(self, width):
            """sets the width
            """
            self._width = self._validate_width(width)
            # also update the device_aspect
            self._update_device_aspect()
        
        doc = """this is a property to set and get the width of the
        image_format
        
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
            self._height = self._validate_height(height)
            
            # also update the device_aspect
            self._update_device_aspect()
        
        doc = """this is a property to set and get the height of the
        image_format
        
        * the height should be set to a positif non-zero integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise a ValueError
        """
        
        return locals()
    
    height = property(**height())
    
    
    
    #----------------------------------------------------------------------
    def pixel_aspect():
        def fget(self):
            """returns the pixel_aspect ratio
            """
            return self._pixel_aspect
        
        def fset(self, pixel_aspect):
            """sets the pixel_aspect ratio
            """
            self._pixel_aspect = self._validate_pixel_aspect(pixel_aspect)
            
            # also update the device_aspect
            self._update_device_aspect()
        
        doc = """this is a property to set and get the pixel_aspect of the
        ImageFormat
        
        * the pixel_aspect should be set to a positif non-zero float
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise a ValueError
        """
        
        return locals()
    
    pixel_aspect = property(**pixel_aspect())
    
    
    
    #----------------------------------------------------------------------
    @property
    def device_aspect(self):
        """returns the device aspect
        
        because the device_aspect is calculated from the width/height*pixel
        formula, this property is read-only.
        """
        return self._device_aspect
    
    
    
    #----------------------------------------------------------------------
    def print_resolution():
        
        def fget(self):
            """returns the print resolution
            """
            return self._print_resolution
        
        def fset(self, print_resolution):
            """sets the print resolution
            """
            self._print_resolution = \
                self._validate_print_resolution(print_resolution)
        
        doc = """this is a property to set and get the print_resolution of the
        ImageFormat
        
        * it should be set to a positif non-zero float or integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise a ValueError
        """
        
        return locals()
    
    print_resolution = property(**print_resolution())
    
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(ImageFormat, self).__eq__(other) and \
               isinstance(other, ImageFormat) and \
               self.width == other.width and \
               self.height == other.height and \
               self.pixel_aspect == other.pixel_aspect
        