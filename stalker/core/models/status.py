#-*- coding: utf-8 -*-



from stalker.core.models import entity
from stalker.ext.validatedList import ValidatedList






########################################################################
class Status(entity.Entity):
    """Defins object statutes.
    
    No extra parameters, use the *code* attribute to give a short name for the
    status.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        
        super(Status,self).__init__(**kwargs)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Status, self).__eq__(other) and isinstance(other, Status)






########################################################################
class StatusList(entity.Entity):
    """the type specific list of :class:`~stalker.core.models.status.Status`
    
    Holds multiple statuses to be used as a choice list for several other
    classes.
    
    A StatusList can only be assigned to only one entity type. So a Project can
    only have a suitable StatusList object which is designed for Project
    entities.
    
    :param statuses: this is a list of status objects, so you can prepare
      different StatusList objects for different kind of entities
    
    :param target_entity_type: use this parameter to specify the target entity
      type that this StatusList is designed for. It accepts entity_type names.
      For example::
        
        from stalker.core.models import status, project
        
        status_list = [
            status.status(name="Waiting To Start", code="WTS"),
            status.status(name="On Hold", code="OH"),
            status.status(name="In Progress", code="WIP"),
            status.status(name="Waiting Review", code="WREV"),
            status.status(name="Approved", code="APP"),
            status.status(name="Completed", code="CMPLT"),
        ]
        
        project_status_list = status.statusList(
            name="Project Status List",
            statuses=status_list,
            target_type=project.Project.entit_type
        )
      
      now with the code above you can not assign the ``project_status_list``
      object to any other class than a ``Project`` object.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 statuses=[],
                 target_entity_type="",
                 **kwargs
                 ):
        
        super(StatusList,self).__init__(**kwargs)
        
        self._statuses = self._validate_statuses(statuses)
        
        self._target_entity_type = \
            self._validate_target_entity_type(target_entity_type)
    
    
    
    #----------------------------------------------------------------------
    def _validate_statuses(self, statuses):
        """validates the given status_list
        """
        
        if not isinstance(statuses, list):
            raise ValueError("statuses should be an instance of list")
        
        if len(statuses) < 1:
            raise ValueError("statuses should not be an empty list")
        
        for status in statuses:
            #if not isinstance(status, Status):
                #raise ValueError(self.__err_status)
            self._validate_status(status)
        
        return ValidatedList(statuses)
    
    
    
    #----------------------------------------------------------------------
    def _validate_target_entity_type(self, target_entity_type_in):
        """validates the given target_entity_type value
        """
        
        # it can not be None
        if target_entity_type_in is None:
            raise ValueError("target_entity_type can not be None")
        
        if str(target_entity_type_in)=="":
            raise ValueError("target_entity_type can not be empty string")
        
        return str(target_entity_type_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_status(self, status_in):
        """validates the given status_in
        """
        
        if not isinstance(status_in, Status):
            raise ValueError("all elements must be an object of Status in "
                             "the given statuses list")
        
        return status_in
    
    
    
    #----------------------------------------------------------------------
    def statuses():
        
        def fget(self):
            return self._statuses
        
        def fset(self, statuses):
            self._statuses = self._validate_statuses(statuses)
        
        doc = """this is the property that sets and returns the statuses, or
        namely the status list of this StatusList object"""
        
        return locals()
    
    statuses = property(**statuses())
    
    
    
    #----------------------------------------------------------------------
    def target_entity_type():
        
        def fget(self):
            return self._target_entity_type
        
        doc="""the target_entity_type which this StatusList is valid for"""
        
        return locals()
    
    target_entity_type = property(**target_entity_type())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(StatusList, self).__eq__(other) and \
               isinstance(other, StatusList) and \
               self.statuses == other.statuses and \
               self.target_entity_type == other.target_entity_type
    
    
    
    #----------------------------------------------------------------------
    def __getitem__(self, key):
        """the indexing attributes for getting item
        """
        
        return self._statuses[key]
    
    
    #----------------------------------------------------------------------
    def __setitem__(self, key, value):
        """the indexing attributes for setting item
        """
        
        self._statuses[key] = self._validate_status(value)
    
    
    
    #----------------------------------------------------------------------
    def __delitem__(self, key):
        """the indexing attributes for deleting item
        """
        
        del self._statuses[key]
    
    
    
    #----------------------------------------------------------------------
    def __len__(self):
        """the indexing attributes for getting the length
        """
        
        return len(self._statuses)
    
    
    