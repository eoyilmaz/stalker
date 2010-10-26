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
class Tag(object):
    """the tag class
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, name):
        
        self._name = self._check_name(name)
    
    
    
    #----------------------------------------------------------------------
    def _check_name(self, name):
        """checks the given name attribute
        """
        
        if name=='' or not isinstance(name, (str, unicode) ):
            raise(ValueError("the name couldn't be empty or anything other \
            than a string or unicode"))
        
        return name
    
    
    
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
    