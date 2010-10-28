#-*- coding: utf-8 -*-






########################################################################
class Unit(object):
    """the base Unit class that keeps data about the units
    
    :param name: the name of the unit, should be a string or unicode
    
    :param abbreviation: the abbreviation of the unit, cm for centimeters, m
      for meters, km for kilometers and so on, it should be a string or unicode
    
    :param conversion_ratio: the conversion ratio to the base unit. the base
        unit is:
        
            * centimeter (cm) for Linear Units
            * degree (deg) for Angular Units
            * 1.0 for Time Units, because it is useless for Time Units
        
        the default value is 1.0 and it only accepts integers or floats, if
        given an integer it will be converted to float.
    """
    
    #----------------------------------------------------------------------
    def __init__(self,
                 name=None,
                 abbreviation=None,
                 conversion_ratio=1.0
                 ):
        self._name = self._check_name(name)
        self._abbreviation = self._check_abbreviation(abbreviation)
        self._conversion_ratio = self._check_conversion_ratio(conversion_ratio) #float(conversion_ratio)
    
    
    
    #----------------------------------------------------------------------
    def _check_name(self, name):
        """checks the name attribute
        """
        
        if not isinstance(name, (str, unicode)) or \
           len(name) == 0:
            raise(ValueError("name should be instance of string or unicode \
            and it shouldn't be empty"))
        
        return name
    
    
    
    #----------------------------------------------------------------------
    def _check_abbreviation(self, abbreviation):
        """checks the abbreviation attribute
        """
        
        if not isinstance(abbreviation, (str, unicode)) or \
           len(abbreviation) == 0:
            raise(ValueError("abbreviation should be instance of string or \
            unicode and it shouldn't be empty"))
        
        return abbreviation
    
    
    
    #----------------------------------------------------------------------
    def name():
        def fget(self):
            return self._name
        
        def fset(self, name):
            self._name = self._check_name(name)
        
        doc = """the name property, sets and returns the name of the current
        unit"""
        
        
        return locals()
    
    name = property( **name() )
    
    
    
    #----------------------------------------------------------------------
    def abbreviation():
        def fget(self):
            return self._abbreviation
        
        def fset(self, abbr):
            self._abbreviation = self._check_abbreviation(abbr)
        
        doc = """the abbreviation property, sets and returns the name of the
        current unit"""
        
        return locals()
    
    abbreviation = property( **abbreviation() )
    
    
    
    #----------------------------------------------------------------------
    def _check_conversion_ratio(self, conversion_ratio):
        """checks the conversion ratio
        """
        
        if not isinstance(conversion_ratio, (int, float)) or \
           conversion_ratio <= 0:
            raise(ValueError("conversion_ratio should be instance of integer \
            or float and cannot be negative or zero"))
        
        return float(conversion_ratio)
    
    
    
    #----------------------------------------------------------------------
    def conversion_ratio():
        def fget(self):
            return self._conversion_ratio
        
        def fset(self, conversion_ratio):
            self._conversion_ratio = \
                self._check_conversion_ratio(conversion_ratio)
        
        doc = """the conversion_ratio property, sets and returns the
        conversion_ratio of the current unit"""
        
        return locals()
    
    conversion_ratio = property( **conversion_ratio() )






########################################################################
class Linear(Unit):
    """The conversion ratio is the ratio to the centimeter. It shows how much
    centimeter is equal to 1 unit of this. 1 meter is 100 centimeter so the
    conversion ratio is 100
    """
    pass






########################################################################
class Angular(Unit):
    """The conversion ratio is the ratio to degree. It means how much
    degree is equal to this unit, 1 raidan is equal to 57.2957795 degree so the
    conversion ratio is 57.2957795
    """
    pass






########################################################################
class Time(Unit):
    """Time units like PAL, NTSC etc.
      
      :param fps: frames-per-second (fps) for Time Units (I know it sounds
        wrong  it should be named MediaSpeed if we are going to use fps as the
        unit, and if we are talking about time then the unit should be seconds,
        but in animation/vfx world media speed as time unit is much meaningful)
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 name=None,
                 abbreviation=None,
                 fps=None):
        super(Time, self).__init__(name, abbreviation, 1.0)
        self._fps = self._check_fps(fps)
    
    
    
    #----------------------------------------------------------------------
    def _check_fps(self, fps):
        """checks the fps
        """
        
        if not isinstance(fps, (int, float)) or \
           fps <= 0:
            raise(ValueError("fps should be instance of integer \
            or float and cannot be negative or zero"))
        
        return float(fps)
    
    
    
    #----------------------------------------------------------------------
    def fps():
        def fget(self):
            """returns the fps
            """
            return self._fps
        
        def fset(self, fps):
            """sets the fps
            """
            self._fps = self._check_fps(fps)
        
        return locals()
    
    fps = property( **fps() )




