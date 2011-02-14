#-*- coding: utf-8 -*-



from stalker.core.models import entity, mixin






########################################################################
class Task(entity.Entity, mixin.StatusMixin, mixin.ScheduleMixin):
    """Manages Task related data.
    
    WARNING: (obviously) not implemented yet!
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)
