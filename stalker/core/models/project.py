#-*- coding: utf-8 -*-



from stalker.core.models import entity






########################################################################
class Project(entity.StatusedEntity):
    """the project class
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        
        super(Project, self).__init__(**kwargs)
        
