#-*- coding: utf-8 -*-
"""Errors for the system.

This module contains the Errors in Stalker.
"""






########################################################################
class LoginError(Exception):
    """Raised when the login information is not correct or not correlate with the data in the database.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, value=""):
        self.value = value
    
    
    
    #----------------------------------------------------------------------
    def __str__(self):
        return repr(self.value)






########################################################################
class DBError(Exception):
    """Raised when there is no database and a database related action has been placed.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, value=""):
        self.value = value
    
    
    
    #----------------------------------------------------------------------
    def __str__(self):
        return repr(self.value)






