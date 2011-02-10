#-*- coding: utf-8 -*-



from stalker.core.models import entity
from stalker.ext.validatedList import ValidatedList






########################################################################
class Department(entity.Entity):
    """The departments that forms the studio itself.
    
    The informations that a Department object holds is like:
    
      * The members of the department
      * The lead of the department
      * and all the other things those are inherited from the AuditEntity class
    
    Two Department object considered the same if they have the same name, the
    the members list nor the lead info is important, a "Modeling" department
    should of course be the same with another department which has the name
    "Modeling" again.
    
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
        
        self._members = self._validate_members(members)
        self._lead = self._validate_lead(lead)
    
    
    
    #----------------------------------------------------------------------
    def _validate_members(self, members):
        """validates the given members attribute
        """
        
        from stalker.core.models import user
        
        for member in members:
            if not isinstance(member, user.User):
                raise ValueError("every element in the members list should be "
                                 "an instance of stalker.core.models.user.User"
                                 " class")
        
        return ValidatedList(members, user.User)
    
    
    
    #----------------------------------------------------------------------
    def _validate_lead(self, lead):
        """validates the given lead attribute
        """
        
        # the lead should not be None
        #if lead is None:
            #raise ValueError("lead could not be set to None")
        
        if lead is not None:
            from stalker.core.models import user
            # the lead should be an instance of user.User class
            if not isinstance(lead, user.User):
                raise ValueError("lead should be an instance of "
                                 "satlker.core.models.user.User")
        
        return lead
    
    
    
    #----------------------------------------------------------------------
    def members():
        
        def fget(self):
            return self._members
        
        def fset(self, members):
            self._members = self._validate_members(members)
        
        doc = """members are a list of users representing the members of this
        department"""
        
        return locals()
    
    members = property(**members())
    
    
    
    #----------------------------------------------------------------------
    def lead():
        
        def fget(self):
            return self._lead
        
        def fset(self, lead):
            self._lead = self._validate_lead(lead)
        
        doc = """lead is the lead of this department, it is a User object"""
        
        return locals()
    
    lead = property(**lead())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Department, self).__eq__(other) and \
               isinstance(other, Department)
    
    