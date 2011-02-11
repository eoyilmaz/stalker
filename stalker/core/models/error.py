#-*- coding: utf-8 -*-






########################################################################
class LoginError(Exception):
    """Raised when the login information is not correct or not correlate with
    the data in the database
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, value):
        self.value = value
    
    
    
    #----------------------------------------------------------------------
    def __str__(self):
        return repr(self.value)