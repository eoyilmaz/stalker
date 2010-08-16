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



########################################################################
class Unit(object):
    """the base Unit class that keeps data about the units
    """
    
    #----------------------------------------------------------------------
    def __init__(self, name, abbreviation, conversionRatio):
        
        if not isinstance(conversionRatio, (int, float)) or \
           conversionRatio <= 0:
            raise( ValueError("conversionRatio should be instance of integer \
            or float") )
        
        self._name = self._checkName(name)
        self._abbreviation = self._checkAbbreviation(abbreviation)
        self._conversionRatio = float(conversionRatio)
    
    
    
    #----------------------------------------------------------------------
    def _checkName(self, name):
        """checks the name attribute
        """
        
        if not isinstance(name, (str, unicode)) or \
           len(name) == 0:
            raise( ValueError("name should be instance of string or unicode \
            and it shouldn't be empty") )
        
        return name
    
    
    
    #----------------------------------------------------------------------
    def _checkAbbreviation(self, abbreviation):
        """checks the abbreviation attribute
        """
        
        if not isinstance(abbreviation, (str, unicode)) or \
           len(abbreviation) == 0:
            raise( ValueError("abbreviation should be instance of string or \
            unicode and it shouldn't be empty") )
        
        return abbreviation
    
    
    
    #----------------------------------------------------------------------
    def name():
        def fget(self):
            """returns the name
            """
            return self._name
        
        def fset(self, name):
            self._name = self._checkName(name)
        
        return locals()
    
    name = property( **name() )
    
    
    
    #----------------------------------------------------------------------
    def abbreviation():
        def fget(self):
            """returns the abbreviation
            """
            return self._abbreviation
        
        def fset(self, abbr):
            self._abbreviation = self._checkAbbreviation(abbr)
        
        return locals()
    
    abbreviation = property( **abbreviation() )
    
    
    