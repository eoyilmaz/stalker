#-*- coding: utf-8 -*-



from stalker.core.models import entity
from stalker.ext.validatedList import ValidatedList






########################################################################
class Status(entity.Entity):
    """Defins object statutes.
    
    No extra parameters, use the *code* attribute to give a short name for the
    status.
    
    A Status object can be compared with a string or unicode value and it will
    return if the lower case name or lower case code of the status matches the
    lower case form of the given string:
    
    >>> from stalker.core.models.status import Status
    >>> a_status = Status(name="On Hold", "OH")
    >>> a_status == "on hold"
    True
    >>> a_status != "complete"
    True
    >>> a_status == "oh"
    True
    >>> a_status == "another status"
    False
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        
        super(Status,self).__init__(**kwargs)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        if isinstance(other, (str, unicode)):
            return self.name.lower() == other.lower() or \
                   self.code.lower() == other.lower()
        else:
            return super(Status, self).__eq__(other) and \
                   isinstance(other, Status)






########################################################################
class StatusList(entity.Entity):
    """the type specific list of :class:`~stalker.core.models.status.Status`
    
    Holds multiple statuses to be used as a choice list for several other
    classes.
    
    A StatusList can only be assigned to only one entity type. So a Project can
    only have a suitable StatusList object which is designed for Project
    entities.
    
    The list of statuses in StatusList can be accessed by using a list like
    indexing and it also supports string indexes only for getting the item,
    you can not set an item with string indices:
    
    >>> from stalker.core.models.status import Status, StatusList
    >>> status1 = Status(name="Complete", code="CMPLT")
    >>> status2 = Status(name="Work in Progress", code="WIP")
    >>> status3 = Status(name="Pending Review", code="PRev")
    >>> a_status_list = StatusList(name="Asset Status List",
                                   statuses=[status1, status2, status3],
                                   target_entity_type="Asset")
    >>> a_status_list[0]
    <Status (Complete, CMPLT)>
    >>> a_status_list["complete"]
    <Status (Complete, CMPLT)>
    >>> a_status_list["wip"]
    <Status (Work in Progress, WIP)>
    
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
        
        for item in statuses:
            self._validate_status(item)
        
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
            raise ValueError("all elements must be an instance of Status in "
                             "the given statuses list")
        
        return status_in
    
    
    
    #----------------------------------------------------------------------
    def statuses():
        
        def fget(self):
            return self._statuses
        
        def fset(self, statuses):
            self._statuses = self._validate_statuses(statuses)
        
        doc = """list of :class:`~stalker.core.models.status.Status` objects,
        showing the possible statuses"""
        
        return locals()
    
    statuses = property(**statuses())
    
    
    
    #----------------------------------------------------------------------
    def target_entity_type():
        
        def fget(self):
            return self._target_entity_type
        
        doc="""the entity type which this StatusList is valid for, usally it
        is set to the TargetClass.entity_type class attribute of the target
        class::
          
          from stalker.core.models import status, asset
          
          # now create a StatusList valid only for assets
          status1 = status.Status(name="Waiting To Start", code="WTS")
          status2 = status.Status(name="Work In Progress", code="WIP")
          status3 = status.Status(name="Complete", code="CMPLT")
        """
        
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
        if isinstance(key, (str, unicode)):
            for item in self._statuses:
                if item==key:
                    return item
        else:
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
    
    
    