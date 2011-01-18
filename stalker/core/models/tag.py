#-*- coding: utf-8 -*-



from stalker.core.models import entity





########################################################################
class Tag(entity.SimpleEntity):
    """the tag class
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Tag, self).__eq__(other) and isinstance(other, Tag)
    
    
    
    #----------------------------------------------------------------------
    def __ne__(self, other):
        """the inequality operator
        """
        
        return not self.__eq__(other)
    
    
    