#-*- coding: utf-8 -*-



from stalker.models import entity






########################################################################
class User(entity.AuditEntity):
    """The user class is designed to hold data about a User in the system. It
    is derived from the entity.AuditEntity class
    
    it adds these parameters to the AuditEntity class
    
    :param email: holds the e-mail of the user, should be in [part1]@[part2]
      format
    
    :param login_name: it is the login name of the user, it should be all lower
      case. Giving a string or unicode that has uppercase letters, it will be
      converted to lower case. It can not be an empty string or None
    
    :param first_name: it is the first name of the user, must be a string or
      unicode, middle name also can be added here, so it accepts white-spaces
      in the variable, but it will truncate the white spaces at the beginin and
      at the end of the variable and it can not be empty or None
    
    :param last_name: it is the last name of the user, must be a string or
      unicode, again it can not contain any white spaces at the beggining and
      at the end of the variable and it can not be an empty string or None
    
    :param department: it is the department of the current user. It should be
      a Department object. One user can only be listed in one department.
    
    :param password: it is the password of the user, can contain any character
      and it should be mangled by using the key from the system preferences
    
    :param permission_groups: it is a list of permission groups that this user
      is belong to
    
    :param tasks: it is a list of Task objects which holds the tasks that this
      user has been assigned to
    
    :param projects: it is a list of Project objects which holds the projects
      that this user is a part of
    
    :param leader_of_projects: it is a list of Project objects that this user
      is the leader of, it is for back refefrencing purposes
    
    :param leader_of_sequences: it is a list of Sequence objects that this
      user is the leader of, it is for back referencing purposes
    """
    
    
    
    pass
