# the module a


try:
    from stalker.models import b
except ImportError:
    pass


########################################################################
class A(b.B):
    """the inherited class
    """
    
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        pass
    
    