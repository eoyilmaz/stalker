#-*- coding: utf-8 -*-



from stalker.core.models import entity, mixin
from stalker.ext.validatedList import ValidatedList





########################################################################
class AssetBase(entity.Entity, mixin.ReferenceMixin, mixin.StatusMixin):
    """The base class for :class:`~stalker.core.models.shot.Shot` and :class:`~stalker.core.models.asset.Asset` classes.
    
    This the base class for :class:`~stalker.core.models.shot.Shot` and
    :class:`~stalker.core.models.asset.Asset` classes which gathers the common
    attributes of these two entities.
    
    :param type: The type of the asset or shot. The default value is None.
    
    :type type: :class:`~stalker.core.models.types.AssetType`
    
    :param list tasks: The list of tasks. Should be a list of
      :class:`~stalker.core.models.task.Task` instances. Default value is an
      empty list.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, type=None, tasks=[], **kwargs):
        super(AssetBase, self).__init__(**kwargs)
        self._tasks = self._validate_tasks(tasks)
        self._type = self._validate_type(type)
    
    
    
    #----------------------------------------------------------------------
    def _validate_tasks(self, tasks_in):
        """validates the given tasks_in value
        """
        
        if tasks_in is None:
            tasks_in = []
        
        if not isinstance(tasks_in, list):
            raise ValueError("tasks should be a list")
        
        from stalker.core.models.task import Task
        
        for item in tasks_in:
            if not isinstance(item, Task):
                raise ValueError("tasks should be a list of "
                "stalker.core.models.task.Task instances")
        
        return ValidatedList(tasks_in, Task)
    
    
    
    #----------------------------------------------------------------------
    def _validate_type(self, type_in):
        """validates the given type_in value
        """
        
        if type_in is not None:
            from stalker.core.models.types import AssetType
            
            if not isinstance(type_in, AssetType):
                raise ValueError("type should be an instance of "
                                 "stalker.core.models.types.AssetType")
        
        return type_in
    
    
    
    #----------------------------------------------------------------------
    def tasks():
        def fget(self):
            return self._tasks
        def fset(self, task_in):
            self._tasks = self._validate_tasks(task_in)
        
        doc = """The list of :class:`~stakler.core.models.task.Task` instances.
        """
        
        return locals()
    
    tasks = property(**tasks())
    
    
    
    #----------------------------------------------------------------------
    def type():
        def fget(self):
            return self._type
        def fset(self, type_in):
            self._type = self._validate_type(type_in)
        
        doc = """The type of this object."""
        
        return locals()
    
    type = property(**type())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(AssetBase, self).__eq__(other) and \
               isinstance(other, AssetBase) and self.type == other.type
        


