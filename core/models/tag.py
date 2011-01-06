#-*- coding: utf-8 -*-



from stalker.core.models import entity





########################################################################
class Tag(entity.SimpleEntity):
    """the tag class
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
    
    
    