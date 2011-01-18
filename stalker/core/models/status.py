#-*- coding: utf-8 -*-



from stalker.core.models import entity



########################################################################
class Status(entity.Entity):
    """The Status class
    
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
    """the list version of the Status
    
    Holds multiple statuses to be used as a choice list for several other
    classes
    
    :param statuses: this is a list of status objects, so you can prepare
      different StatusList objects for different kind of entities
    """
    
    #----------------------------------------------------------------------
    def __init__(self,
                 #name=None,
                 statuses=[],
                 **kwargs
                 ):
        
        super(StatusList,self).__init__(**kwargs)
        
        #self._name = self._check_name(name)
        self._statuses = self._check_statuses(statuses)
    
    
    
    #----------------------------------------------------------------------
    def _check_statuses(self, statuses):
        """checks the given status_list
        """
        
        if not isinstance(statuses, list):
            raise(ValueError("statuses should be an instance of list"))
        
        if len(statuses) < 1:
            raise(ValueError("statuses should not be an empty list"))
        
        for status in statuses:
            if not isinstance(status, Status):
                raise(ValueError("all elements must be an object of Status in \
                the given statuses list"))
        
        return statuses
    
    
    
    #----------------------------------------------------------------------
    def statuses():
        
        def fget(self):
            return self._statuses
        
        def fset(self, statuses):
            self._statuses = self._check_statuses(statuses)
        
        doc = """this is the property that sets and returns the statuses, or
        namely the status list of this StatusList object"""
        
        return locals()
    
    statuses = property(**statuses())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(StatusList, self).__eq__(other) and \
               isinstance(other, StatusList) and \
               self.statuses == other.statuses
    
    
    