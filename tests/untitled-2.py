


########################################################################
class myClass(object):
    """testing something about lists and __setitem__, append
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self):
        
        self._special_attr = []
    
    
    
    #----------------------------------------------------------------------
    def _check_special_attr_(self, special_attr_in):
        """checking the special attr
        """
        
        for element in special_attr_in:
            if not isinstance(element, int):
                raise(ValueError("it is not an instance of int"))
        
        return special_attr_in
    
    
    
    def special_attr():
        def fget(self):
            return self._special_attr
        
        def fset(self, special_attr_in):
            self._special_attr = self._check_special_attr_(special_attr_in)
        
        return locals()
    
    special_attr = property(**special_attr())



