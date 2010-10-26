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
class Unit(object):
    """the base Unit class that keeps data about the units
    """
    
    #----------------------------------------------------------------------
    def __init__(self, name, abbreviation):
        self._name = self._check_name(name)
        self._abbreviation = self._check_abbreviation(abbreviation)
    
    
    
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
            """returns the name
            """
            return self._name
        
        def fset(self, name):
            self._name = self._check_name(name)
        
        return locals()
    
    name = property( **name() )
    
    
    
    #----------------------------------------------------------------------
    def abbreviation():
        def fget(self):
            """returns the abbreviation
            """
            return self._abbreviation
        
        def fset(self, abbr):
            self._abbreviation = self._check_abbreviation(abbr)
        
        return locals()
    
    abbreviation = property( **abbreviation() )






########################################################################
class ConvertableUnit(Unit):
    """Convertable units like linear and angular units will derive from this
    class
    """
    
    #----------------------------------------------------------------------
    def __init__(self, name, abbreviation, conversion_ratio):
        super(ConvertableUnit, self).__init__(name, abbreviation)
        self._conversion_ratio = self._check_conversion_ratio(conversion_ratio) #float(conversion_ratio)
    
    
    
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
            """returns the conversion_ratio
            """
            return self._conversion_ratio
        
        def fset(self, conversion_ratio):
            """sets the conversion_ratio
            """
            self._conversion_ratio = self._check_conversion_ratio(conversion_ratio)
        
        return locals()
    
    conversion_ratio = property( **conversion_ratio() )






########################################################################
class Linear(ConvertableUnit):
    """The conversion ratio is the ratio to the centimeter. It shows how much
    centimeter is equal to 1 unit of this. 1 meter is 100 centimeter so the
    conversion ratio is 100
    """
    pass






########################################################################
class Angular(ConvertableUnit):
    """The conversion ratio is the ratio to degree. It means how much
    degree is equal to this unit, 1 raidan is equal to 57.2957795 degree so the
    conversion ratio is 57.2957795
    """
    pass






########################################################################
class Time(Unit):
    """Time units like PAL, NTSC etc.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, name, abberation, fps):
        super(Time, self).__init__(name, abberation)
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




