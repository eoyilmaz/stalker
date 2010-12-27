#-*- coding: utf-8 -*-



from stalker.models import entity






########################################################################
class Department(entity.Entity):
    """A department holds information about a studios departments. The
    informations that a Department object holds is like:
    
      * The members of the department
      * The lead of the department
      * and all the other things those are inherited from the AuditEntity class
    
    so creating a department object needs the following parameters:
    
    :param members: it can be an empty list, so one department can be created
      without any member in it. But this parameter should be a list of User
      objects.
    
    :param lead: this is a User object, that holds the lead information, a lead
      could be in this department but it is not forced to be also a member of
      the department. So another departments member can be a lead for another
      department. Lead attribute can not be empty or None.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, members=[], lead=None, **kwargs):
        super(Department, self).__init__(**kwargs)
        
        self._members = self._check_members(members)
        self._lead = self._check_lead(lead)
    
    
    
    #----------------------------------------------------------------------
    def _check_members(self, members):
        """checks the given members attribute
        """
        
        from stalker.models import user
        
        for member in members:
            if not isinstance(member, user.User):
                raise(ValueError("every element in the members list should be \
                an instance of stalker.models.user.User class"))
        
        return members
    
    
    
    #----------------------------------------------------------------------
    def _check_lead(self, lead):
        """checks the given lead attribute
        """
        
        # the lead should not be None
        #if lead is None:
            #raise(ValueError("lead could not be set to None"))
        
        if lead is not None:
            from stalker.models import user
            # the lead should be an instance of user.User class
            if not isinstance(lead, user.User):
                raise(ValueError("lead should be an instance of user.User class"))
        
        return lead
    
    
    
    #----------------------------------------------------------------------
    def members():
        
        def fget(self):
            return self._members
        
        def fset(self, members):
            self._members = self._check_members(members)
        
        doc = """members are a list of users representing the members of this
        department"""
        
        return locals()
    
    members = property(**members())
    
    
    
    #----------------------------------------------------------------------
    def lead():
        
        def fget(self):
            return self._lead
        
        def fset(self, lead):
            self._lead = self._check_lead(lead)
        
        doc = """lead is the lead of this department, it is a User object"""
        
        return locals()
    
    lead = property(**lead())
    
    
    