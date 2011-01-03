#-*- coding: utf-8 -*-



import re
import base64
import datetime
from stalker.models import entity






########################################################################
class User(entity.Entity):
    """The user class is designed to hold data about a User in the system. It
    is derived from the entity.AuditEntity class
    
    it adds these parameters to the AuditEntity class
    
    :param email: holds the e-mail of the user, should be in [part1]@[part2]
      format
    
    :param last_login: it is a datetime.datetime object holds the last login
      date of the user (not implemented yet)
    
    :param login_name: it is the login name of the user, it should be all lower
      case. Giving a string or unicode that has uppercase letters, it will be
      converted to lower case. It can not be an empty string or None
    
    :param first_name: it is the first name of the user, must be a string or
      unicode, middle name also can be added here, so it accepts white-spaces
      in the variable, but it will truncate the white spaces at the beginin and
      at the end of the variable and it can not be empty or None
    
    :param last_name: it is the last name of the user, must be a string or
      unicode, again it can not contain any white spaces at the beggining and
      at the end of the variable and it can be an empty string or None
    
    :param department: it is the department of the current user. It should be
      a Department object. One user can only be listed in one department. A
      user is allowed to have no department to make it easy to create a new
      user and create the department and assign the user it later.
    
    :param password: it is the password of the user, can contain any character
      and it should be scrambled by using the key from the system preferences
    
    :param permission_groups: it is a list of permission groups that this user
      is belong to
    
    :param tasks: it is a list of Task objects which holds the tasks that this
      user has been assigned to
    
    :param projects: it is a list of Project objects which holds the projects
      that this user is a part of
    
    :param projects_lead: it is a list of Project objects that this user
      is the leader of, it is for back refefrencing purposes
    
    :param sequences_lead: it is a list of Sequence objects that this
      user is the leader of, it is for back referencing purposes
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 department=None,
                 email='',
                 first_name='',
                 last_name='',
                 login_name='',
                 password='',
                 permission_groups=[],
                 projects=[],
                 projects_lead=[],
                 sequences_lead=[],
                 tasks=[],
                 **kwargs
                 ):
        
        # use
        
        super(User, self).__init__(**kwargs)
        
        self._department = self._check_department(department)
        self._email = self._check_email(email)
        self._first_name = self._check_first_name(first_name)
        self._last_name = self._check_last_name(last_name)
        self._login_name = self._check_login_name(login_name)
        
        # to be able to mangle the password do it like this
        self._password = None
        self.password = password
        
        self._permission_groups = \
            self._check_permission_groups(permission_groups)
        self._projects = self._check_projects(projects)
        self._projects_lead = self._check_projects_lead(projects_lead)
        self._sequence_lead = self._check_sequences_lead(sequences_lead)
        self._tasks = self._check_tasks(tasks)
    
    
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """return the representation of the current User
        """
        
        return "<user.User (%s %s ('%s'))>" % \
               (self.first_name, self.last_name, self.login_name)
    
    
    
    #----------------------------------------------------------------------
    def _check_department(self, department_in):
        """checks the given department value
        """
        
        ## check if department_in is None
        #if department_in is None:
            #raise(ValueError('department could not be None'))
        
        from stalker.models import department
        
        # check if it is intance of Department object
        if department is not None:
            if not isinstance(department_in, department.Department):
                raise(ValueError('department should be instance of \
                stalker.models.department.Department'))
        
        return department_in
    
    
    
    #----------------------------------------------------------------------
    def _check_email(self, email_in):
        """checks the given email value
        """
        
        # check if email_in is an instance of string or unicode
        if not isinstance(email_in, (str, unicode)):
            raise(ValueError('email should be an instance of string or \
            unicode'))
        
        return self._check_email_format(email_in)
    
    
    
    #----------------------------------------------------------------------
    def _check_email_format(self, email_in):
        """formats the email
        """
        
        # split the mail from @ sign
        splits = email_in.split('@')
        len_splits = len(splits)
        
        # there should be one and only one @ sign
        if len_splits > 2:
            raise(ValueError('check the email formatting, there are more than \
            one @ sign'))
        
        if len_splits < 2:
            raise(ValueError('check the email formatting, there are no @ \
            sign'))
        
        if splits[0] == '':
            raise(ValueError('check the email formatting, the name part is \
            missing'))
        
        if splits[1] == '':
            raise(ValueError('check the email formatting, the domain part is \
            missing'))
        
        return email_in
    
    
    
    #----------------------------------------------------------------------
    def _check_first_name(self, first_name_in):
        """checks the given first_name attribute
        """
        
        if first_name_in is None:
            raise(ValueError('first_name cannot be none'))
        
        if not isinstance(first_name_in, (str, unicode)):
            raise(ValueError('first_name should be instance of string or \
            unicode'))
        
        if first_name_in == '':
            raise(ValueError('first_name can not be an empty string'))
        
        return self._check_first_name_formatting(first_name_in)
    
    
    
    #----------------------------------------------------------------------
    def _check_first_name_formatting(self, first_name_in):
        """checks the given first_name formatting
        """
        
        return first_name_in.strip().title()
    
    
    
    #----------------------------------------------------------------------
    def _check_last_name(self, last_name_in):
        """checks the given last_name attribute
        """
        
        #if last_name_in is None:
            #raise(ValueError('last_name cannot be none'))
        if last_name_in is not None:
            if not isinstance(last_name_in, (str, unicode)):
                raise(ValueError('last_name should be instance of string or \
                unicode'))
        else:
            last_name_in = ''
        
        #if last_name_in == '':
            #raise(ValueError('last_name can not be an empty string'))
        
        return self._check_last_name_formatting(last_name_in)
    
    
    
    #----------------------------------------------------------------------
    def _check_last_name_formatting(self, last_name_in):
        """checks the given last_name formatting
        """
        
        return last_name_in.strip().title()
    
    
    
    #----------------------------------------------------------------------
    def _check_login_name(self, login_name_in):
        """checks the given login_name value
        """
        
        if login_name_in is None:
            raise(ValueError('login name could not be None'))
        
        if not isinstance(login_name_in, (str, unicode)):
            raise(ValueError('login_name should be instance of string or \
            unicode'))
        
        if login_name_in == '':
            raise(ValueError('login name could not be empty string'))
        
        return self._check_login_name_formatting(login_name_in)
    
    
    
    #----------------------------------------------------------------------
    def _check_login_name_formatting(self, login_name_in):
        """checks the given login_name formatting
        """
        assert(isinstance(login_name_in, str))
        login_name_in = login_name_in.strip()
        login_name_in = login_name_in.replace(' ','')
        login_name_in = login_name_in.lower()
        login_name_in = re.sub( '[^\\(a-zA-Z1-9)]+', '', login_name_in)
        login_name_in = re.sub( '^[0-9]+', '', login_name_in)
        
        return login_name_in
    
    
    
    #----------------------------------------------------------------------
    def _check_password(self, password_in):
        """checks the given password
        """
        
        if password_in is None:
            raise(ValueError('password cannot be None'))
        
        return password_in
    
    
    
    #----------------------------------------------------------------------
    def _check_permission_groups(self, permission_groups_in):
        """check the given permission_group
        """
        
        if permission_groups_in is None:
            raise(ValueError('permission_groups attribute can not be None'))
        
        if not isinstance(permission_groups_in, list):
            raise(ValueError('permission_groups should be a list of group \
            objects'))
        
        from stalker.models import group
        
        for permission_group in permission_groups_in:
            if not isinstance(permission_group, group.Group):
                raise(ValueError('any group in permission_groups should be \
                an instance of stalker.models.group.Group'))
        
        #if len(permission_groups_in) == 0:
            #raise(ValueError('users should be assigned at least to one \
            #permission_group'))
        
        return permission_groups_in
    
    
    
    #----------------------------------------------------------------------
    def _check_projects(self, projects_in):
        """checks the given projects attribute
        """
        
        # projects can not be None
        if projects_in is None:
            raise(ValueError('projects can not be None'))
        
        if not isinstance(projects_in, list):
            raise(ValueError('projects should be a list of \
            stalker.models.project.Project objects'))
        
        from stalker.models import project
        
        for a_project in projects_in:
            if not isinstance(a_project, project.Project):
                raise(ValueError('any element in projects should be an \
                instance of stalker.models.project.Project'))
        
        return projects_in
        
    
    
    #----------------------------------------------------------------------
    def _check_projects_lead(self, projects_lead_in):
        """checks the given projects_lead attribute
        """
        
        if projects_lead_in is None:
            raise(ValueError('projects_lead attribute could not be None, try \
            setting it to an empty list'))
        
        if not isinstance(projects_lead_in, list):
            raise(ValueError('projects_lead should be a list of \
            stalker.models.project.Project objects'))
        
        from stalker.models import project
        
        for a_project in projects_lead_in:
            if not isinstance(a_project, project.Project):
                raise(ValueError('any element in projects_lead should be an \
                instance of stalker.models.project.Project class'))
        
        return projects_lead_in
    
    
    
    #----------------------------------------------------------------------
    def _check_sequences_lead(self, sequences_lead_in):
        """checks the given sequences_lead attribute
        """
        
        if sequences_lead_in is None:
            raise(ValueError('sequences_lead attribute could not be None, try \
            setting it to an empty list'))
        
        if not isinstance(sequences_lead_in, list):
            raise(ValueError('sequences_lead should be a list of \
            stalker.models.sequence.Sequence objects'))
        
        from stalker.models import sequence
        
        for a_sequence in sequences_lead_in:
            if not isinstance(a_sequence, sequence.Sequence):
                raise(ValueError('any element in sequences_lead should be an \
                instance of stalker.models.sequence.Sequence class'))
        
        return sequences_lead_in
    
    
    
    #----------------------------------------------------------------------
    def _check_tasks(self, tasks_in):
        """checks the given taks attribute
        """
        
        if tasks_in is None:
            raise(ValueError('tasks attribute could not be None, try setting \
            it to an empty list'))
        
        if not isinstance(tasks_in, list):
            raise(ValueError('tasks should be a list of \
            stalker.models.task.Task objects'))
        
        from stalker.models import task
        
        for a_task in tasks_in:
            if not isinstance(a_task, task.Task):
                raise(ValueError('any element in tasks should be an instance \
                of stalker.models.task.Task class'))
        
        return tasks_in
    
    
    
    #----------------------------------------------------------------------
    def department():
        
        def fget(self):
            return self._department
        
        def fset(self, department_in):
            self._department = self._check_department(department_in)
        
        doc = """This is the property that helps to get and set department
        values
        """
        
        return locals()
    
    department = property(**department())
    
    
    
    #----------------------------------------------------------------------
    def email():
        
        def fget(self):
            return self._email
        
        def fset(self, email_in):
            self._email = self._check_email(email_in)
        
        doc = """This is the property that helps to get and set email values
        """
        
        return locals()
    
    email = property(**email())
    
    
    
    #----------------------------------------------------------------------
    def first_name():
        
        def fget(self):
            return self._first_name
        
        def fset(self, first_name_in):
            self._first_name = self._check_first_name(first_name_in)
        
        doc = """This is the property that helps to get and set first_name
        values
        """
        
        return locals()
    
    first_name = property(**first_name())
    
    
    
    #----------------------------------------------------------------------
    def last_name():
        
        def fget(self):
            return self._last_name
        
        def fset(self, last_name_in):
            self._last_name = self._check_last_name(last_name_in)
        
        doc = """This is the property that helps to get and set last_name
        values
        """
        
        return locals()
    
    last_name = property(**last_name())
    
    
    
    #----------------------------------------------------------------------
    def login_name():
        
        def fget(self):
            return self._login_name
        
        def fset(self, login_name_in):
            self._login_name = self._check_login_name(login_name_in)
        
        doc = """This is the property that helps to get and set login_name
        values"""
        
        return locals()
    
    login_name = property(**login_name())
    
    
    
    #----------------------------------------------------------------------
    def password():
        
        def fget(self):
            return base64.decodestring(self._password)
        
        def fset(self, password_in):
            self._password = base64.encodestring(
                self._check_password(password_in)
            )
        
        doc = """This is the password of the user, it is scrambled before
        stored in the _password attribute"""
        
        return locals()
    
    password = property(**password())
    
    
    
    #----------------------------------------------------------------------
    def permission_groups():
        
        def fget(self):
            return self._permission_groups
        
        def fset(self, permission_groups_in):
            self._permission_groups = \
                self._check_permission_groups(permission_groups_in)
        
        doc = """This is the property that helps to get and set
        permission_groups values"""
        
        return locals()
    
    permission_groups = property(**permission_groups())
    
    
    
    #----------------------------------------------------------------------
    def projects():
        
        def fget(self):
            return self._projects
        
        def fset(self, projects_in):
            self._projects = self._check_projects(projects_in)
        
        doc = """This is the property that helps to get and set projects
        values
        """
        
        return locals()
    
    projects = property(**projects())
    
    
    
    #----------------------------------------------------------------------
    def projects_lead():
        
        def fget(self):
            return self._projects_lead
        
        def fset(self, projects_lead_in):
            self._projects_lead = self._check_projects_lead(projects_lead_in)
        
        doc = """This is the property that helps to get and set projects_lead
        values
        """
        
        return locals()
    
    projects_lead = property(**projects_lead())
    
    
    
    #----------------------------------------------------------------------
    def sequences_lead():
        
        def fget(self):
            return self._sequences_lead
        
        def fset(self, sequences_lead_in):
            self._sequences_lead = \
                self._check_sequences_lead(sequences_lead_in)
        
        doc = """This is the property that helps to get and set sequences_lead
        values
        """
        
        return locals()
    
    sequences_lead = property(**sequences_lead())
    
    
    
    #----------------------------------------------------------------------
    def tasks():
        
        def fget(self):
            return self._tasks
        
        def fset(self, tasks_in):
            self._tasks = self._check_tasks(tasks_in)
        
        doc = """This is the property that helps to get and set tasks
        values
        """
        
        return locals()
    
    tasks = property(**tasks())