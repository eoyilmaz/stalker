# the module b


try:
    from stalker.models import a
except ImportError:
    pass


########################################################################
class B(object):
    """the base class
    """
    
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        self._a = a.A()
    
    