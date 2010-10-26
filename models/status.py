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
class Status(object):
    """The Status class
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, name, abbreviation, thumbnail=None):
        
        self._name = self._check_name(name)
        self._abbreviation = self._check_abbreviation( abbreviation )
    
    
    
    #----------------------------------------------------------------------
    def _check_name(self, name):
        """checks the name attribute
        """
        
        if name == "" \
           or not isinstance(name, (str, unicode) ) \
           or name[0] in [str(i) for i in range(10)]:
            raise(ValueError("the name shouldn't be empty and it should be a \
            str or unicode"))
        
        return name.title()
    
    
    
    #----------------------------------------------------------------------
    def _check_abbreviation(self, abbreviation):
        """checks the abbreviation attribute
        """
        
        if abbreviation == '' \
           or not isinstance(abbreviation, (str, unicode)):
            raise(ValueError("the abbreviation shouldn't be empty and it \
            should be a str or unicode"))
        
        return abbreviation
    
    
    
    #----------------------------------------------------------------------
    def name():
        def fget(self):
            """returns the name property
            """
            return self._name
        
        def fset(self, name):
            self._name = self._check_name(name)
        
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
            self._abbreviation = self._check_abbreviation(abbreviation)
        
        return locals()
    
    abbreviation = property(**abbreviation())






########################################################################
class StatusList(object):
    """the list version of the Status
    holds multiple statuses to be used as a choice list for several
    other classes
    """
    
    #----------------------------------------------------------------------
    def __init__(self, name, statuses):
        
        
        self._name = self._check_name(name)
        self._statuses = self._check_statuses(statuses)
    
    
    
    #----------------------------------------------------------------------
    def _check_name(self, name):
        """checks the given name
        """
        
        if name == '':
            raise(ValueError('name can not be empty'))
        
        if not isinstance( name, (str, unicode) ):
            raise(ValueError('name should be a string or unicode'))
        
        return name
    
    
    
    #----------------------------------------------------------------------
    def _check_statuses(self, statuses):
        """checks the given status_list
        """
        
        if not isinstance(statuses, list):
            raise(ValueError('statuses should be an instance of list'))
        
        if len(statuses) < 1:
            raise(ValueError('statuses should not be an empty list'))
        
        for status in statuses:
            if not isinstance(status, Status):
                raise(ValueError('all elements must be an object of Status in \
                the given statuses list'))
        
        return statuses
    
    
    
    #----------------------------------------------------------------------
    def name():
        
        def fget(self):
            """returns the name attribute
            """
            return self._name
        
        def fset(self, name):
            """sets the name attribute
            """
            self._name = self._check_name(name)
        
        return locals()
    
    name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def statuses():
        
        def fget(self):
            """returns the status_list
            """
            return self._statuses
        
        def fset(self, statuses):
            """sets the statuses
            """
            self._statuses = self._check_statuses(statuses)
        
        return locals()
    
    statuses = property(**statuses())
    
    
    