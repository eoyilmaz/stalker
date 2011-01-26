#-*- coding: utf-8 -*-



from stalker.core.models import entity, mixin






########################################################################
class Project(entity.Entity, mixin.StatusMixin):
    """the project class
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        
        super(Project, self).__init__(**kwargs)
        
