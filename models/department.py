#-*- coding: utf-8 -*-



from stalker.models import entity






########################################################################
class Department(entity.AuditEntity):
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
      department.
    """
    
    
    
    pass
