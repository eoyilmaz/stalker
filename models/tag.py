#-*- coding: utf-8 -*-






########################################################################
class Tag(object):
    """the tag class
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, name=None):
        
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
    