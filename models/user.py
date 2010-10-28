#-*- coding: utf-8 -*-



from stalker.models import entity






########################################################################
class User(entity.Entity):
    """The user class is designed to hold data about a User in the system. It
    is derived from the entity.Entity class
    
    it adds these parameters to the EntityClass
    
    :param email: holds the e-mail of the user
    
    :param login_name: it is the login name of the user, it should be all lower
      case. Giving a string or unicode that has uppercase letters, it will be
      converted to lower case.
    
    :param first_name: it is the first name of the user, must be a string or
      unicode, middle name also can be added here, so it accepts white-spaces
      in the variable, but it will truncate the white spaces at the beginin and
      at the end of the variable.
    
    :param last_name: it is the last name of the user, must be a string or
      unicode, again it can not contain any white spaces at the beggining and
      at the end of the variable
    
    :param departments: it is a list that holds Department objects and it shows
      which department of this user belongs to, a user can be a member of more
      than one department
    
    :param password: it is the password of the user, can contain any character
      and it should be mangled by using the key
    
    :param permission_groups: it is a list of permission groups that this user
      is belong to
    
    :param tasks: it is a list of Task objects which holds the tasks that this
      user has been assigned to
    
    :param projects: it is a list of Project objects which holds the projects
      that this user is a part of
    
    :param responsible_sequences: it is a list of Sequence objects that this
      user is responsible of
    """
    
    
    
    pass
