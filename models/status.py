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
class StatusBase(object):
    """The StatusBase class
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, name, abbreviation, thumbnail=None):
        
        self._name = self._checkName(name)
        self._abbreviation = self._checkAbbreviation( abbreviation )
    
    
    
    #----------------------------------------------------------------------
    def _checkName(self, name):
        """checks the name attribute
        """
        
        if name == "" \
           or not isinstance(name, (str, unicode) ) \
           or name[0] in [str(i) for i in range(10)]:
            raise(ValueError("the name shouldn't be empty and it should be a \
            str or unicode"))
        
        return name.title()
    
    
    
    #----------------------------------------------------------------------
    def _checkAbbreviation(self, abbreviation):
        """checks the abbreviation attribute
        """
        
        if abbreviation == '' \
           or not isinstance(abbreviation, (str, unicode)):
            raise( ValueError("the abbreviation shouldn't be empty and it \
            should be a str or unicode"))
        
        return abbreviation
    
    
    
    #----------------------------------------------------------------------
    def name():
        def fget(self):
            """returns the name property
            """
            return self._name
        
        def fset(self, name):
            self._name = self._checkName(name)
        
        return locals()
    
    name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def abbreviation():
        def fget(self):
            """returns the abbreviation property
            """
            return self._abbreviation
        
        def fset(self, abbreviation):
            """sets the abbreviation
            """
            self._abbreviation = self._checkAbbreviation(abbreviation)
        
        return locals()
    
    abbreviation = property(**abbreviation())






########################################################################
class Status(StatusBase):
    """the general usage status class
    """
    pass





########################################################################
class StatusList(StatusBase):
    """the list version of the Status
    holds multiple statuses to be used as a multip list choice for several
    other classes
    """
    pass
