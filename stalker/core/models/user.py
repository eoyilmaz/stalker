#-*- coding: utf-8 -*-



import re
import base64
import datetime
from stalker.core.models import entity
from stalker.ext.validatedList import ValidatedList





########################################################################
class User(entity.Entity):
    """The user class is designed to hold data about a User in the system.
    
    :param email: holds the e-mail of the user, should be in [part1]@[part2]
      format
    
    :param login_name: it is the login name of the user, it should be all lower
      case. Giving a string or unicode that has uppercase letters, it will be
      converted to lower case. It can not be an empty string or None and it can
      not contain any white space inside. login_name parameter will be copied
      over name if both of them is given, if one of them given they will have
      the same value which is the formatted login_name value. Setting the name
      value also sets the login_name and setting the login_name property also
      sets the name, while creating a User object you don't need to specify
      both of them, one is enough and if the two is given `login_name` will be
      used.
    
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
    
    :param last_login: it is a datetime.datetime object holds the last login
      date of the user (not implemented yet)
    
    :param initials: it is the initials of the users name, if nothing given it
      will be calculated from the first and last names of the user
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 department=None,
                 email="",
                 first_name="",
                 last_name="",
                 login_name="",
                 password="",
                 permission_groups=[],
                 projects=[],
                 projects_lead=[],
                 sequences_lead=[],
                 tasks=[],
                 last_login=None,
                 initials="",
                 **kwargs
                 ):
        
        # use the login_name for name if there are no name attribute present
        name = kwargs.get("name")
        
        if login_name is not None and login_name != "":
            name = login_name
        else:
            login_name = name
        
        kwargs["name"] = name
        
        super(User, self).__init__(**kwargs)
        
        self._department = self._validate_department(department)
        self._email = self._validate_email(email)
        self._first_name = self._validate_first_name(first_name)
        self._last_name = self._validate_last_name(last_name)
        self._login_name = self._validate_login_name(login_name)
        self._initials = self._validate_initials(initials)
        
        # to be able to mangle the password do it like this
        self._password = None
        self.password = password
        
        self._permission_groups = \
            self._validate_permission_groups(permission_groups)
        self._projects = self._validate_projects(projects)
        self._projects_lead = self._validate_projects_lead(projects_lead)
        self._sequences_lead = self._validate_sequences_lead(sequences_lead)
        self._tasks = self._validate_tasks(tasks)
        
        self._last_login = self._validate_last_login(last_login)
    
    
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """return the representation of the current User
        """
        
        return "<user.User (%s %s ('%s'))>" % \
               (self.first_name, self.last_name, self.login_name)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(User, self).__eq__(other) and \
               isinstance(other, User) and \
               self.email == other.email and \
               self.login_name == other.login_name and \
               self.first_name == other.first_name and \
               self.last_name == other.last_name and \
               self.name == other.name
    
    
    
    #----------------------------------------------------------------------
    def __ne__(self, other):
        """the inequality operator
        """
        
        return not self.__eq__(other)
    
    
    
    #----------------------------------------------------------------------
    def _validate_department(self, department_in):
        """validates the given department value
        """
        
        ## check if department_in is None
        #if department_in is None:
            #raise ValueError("department could not be None")
        
        from stalker.core.models import department
        
        # check if it is intance of Department object
        if department_in is not None:
            if not isinstance(department_in, department.Department):
                raise ValueError("department should be instance of "
                                 "stalker.core.models.department.Department")
        
        return department_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_email(self, email_in):
        """validates the given email value
        """
        
        # check if email_in is an instance of string or unicode
        if not isinstance(email_in, (str, unicode)):
            raise ValueError("email should be an instance of string or "
                             "unicode")
        
        return self._validate_email_format(email_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_email_format(self, email_in):
        """formats the email
        """
        
        # split the mail from @ sign
        splits = email_in.split("@")
        len_splits = len(splits)
        
        # there should be one and only one @ sign
        if len_splits > 2:
            raise ValueError("check the email formatting, there are more than "
                             "one @ sign")
        
        if len_splits < 2:
            raise ValueError("check the email formatting, there are no @ sign")
        
        if splits[0] == "":
            raise ValueError("check the email formatting, the name part is "
                             "missing")
        
        if splits[1] == "":
            raise ValueError("check the email formatting, the domain part is "
                             "missing")
        
        return email_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_first_name(self, first_name_in):
        """validates the given first_name attribute
        """
        
        if first_name_in is None:
            raise ValueError("first_name cannot be none")
        
        if not isinstance(first_name_in, (str, unicode)):
            raise ValueError("first_name should be instance of string or "
                             "unicode")
        
        if first_name_in == "":
            raise ValueError("first_name can not be an empty string")
        
        return self._validate_first_name_formatting(first_name_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_first_name_formatting(self, first_name_in):
        """validates the given first_name formatting
        """
        
        return first_name_in.strip().title()
    
    
    
    #----------------------------------------------------------------------
    def _validate_initials(self, initials_in):
        """validates the given initials
        """
        
        initials_in = str(initials_in)
        
        if initials_in == "":
            # derive the initials from the first and last name
            
            initials_in = re.sub("[^A-Z]+", "",
                                 self.first_name.title() + " " + \
                                 self.last_name.title()).lower()
        
        return initials_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_last_login(self, last_login_in):
        """validates the given last_login argument
        """
        
        if not isinstance(last_login_in, datetime.datetime) and \
           last_login_in is not None:
            raise ValueError("last_login should be an instance of "
                             "datetime.datetime or None")
        
        return last_login_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_last_name(self, last_name_in):
        """validates the given last_name attribute
        """
        
        #if last_name_in is None:
            #raise ValueError("last_name cannot be none")
        if last_name_in is not None:
            if not isinstance(last_name_in, (str, unicode)):
                raise ValueError("last_name should be instance of string or "
                                 "unicode")
        else:
            last_name_in = ""
        
        #if last_name_in == "":
            #raise ValueError("last_name can not be an empty string")
        
        return self._validate_last_name_formatting(last_name_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_last_name_formatting(self, last_name_in):
        """validates the given last_name formatting
        """
        
        return last_name_in.strip().title()
    
    
    
    #----------------------------------------------------------------------
    def _validate_login_name(self, login_name_in):
        """validates the given login_name value
        """
        
        if login_name_in is None:
            raise ValueError("login name could not be None")
        
        if not isinstance(login_name_in, (str, unicode)):
            raise ValueError("login_name should be instance of string or "
                             "unicode")
        
        if login_name_in == "":
            raise ValueError("login name could not be empty string")
        
        return self._validate_login_name_formatting(login_name_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_login_name_formatting(self, login_name_in):
        """validates the given login_name formatting
        """
        assert(isinstance(login_name_in, str))
        login_name_in = login_name_in.strip()
        login_name_in = login_name_in.replace(" ","")
        login_name_in = login_name_in.lower()
        login_name_in = re.sub( "[^\\(a-zA-Z1-9)]+", "", login_name_in)
        login_name_in = re.sub( "^[0-9]+", "", login_name_in)
        
        return login_name_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_password(self, password_in):
        """validates the given password
        """
        
        if password_in is None:
            raise ValueError("password cannot be None")
        
        return password_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_permission_groups(self, permission_groups_in):
        """check the given permission_group
        """
        
        if permission_groups_in is None:
            raise ValueError("permission_groups attribute can not be None")
        
        if not isinstance(permission_groups_in, list):
            raise ValueError("permission_groups should be a list of group "
                             "objects")
        
        from stalker.core.models import group
        
        for permission_group in permission_groups_in:
            if not isinstance(permission_group, group.Group):
                raise ValueError("any group in permission_groups should be an "
                                 "instance of stalker.core.models.group.Group")
        
        #if len(permission_groups_in) == 0:
            #raise ValueError("users should be assigned at least to one "
            #                 "permission_group")
        
        return ValidatedList(permission_groups_in, group.Group)
    
    
    
    #----------------------------------------------------------------------
    def _validate_projects(self, projects_in):
        """validates the given projects attribute
        """
        
        # projects can not be None
        if projects_in is None:
            raise ValueError("projects can not be None")
        
        if not isinstance(projects_in, list):
            raise ValueError("projects should be a list of "
                             "stalker.core.models.project.Project objects")
        
        from stalker.core.models import project
        
        for a_project in projects_in:
            if not isinstance(a_project, project.Project):
                raise ValueError(
                    "any element in projects should be an instance of "
                    "stalker.core.models.project.Project"
                )
        
        return ValidatedList(projects_in, project.Project)
        
    
    
    #----------------------------------------------------------------------
    def _validate_projects_lead(self, projects_lead_in):
        """validates the given projects_lead attribute
        """
        
        if projects_lead_in is None:
            raise ValueError("projects_lead attribute could not be None, try "
                             "setting it to an empty list")
        
        if not isinstance(projects_lead_in, list):
            raise ValueError("projects_lead should be a list of "
                             "stalker.core.models.project.Project objects")
        
        from stalker.core.models import project
        
        for a_project in projects_lead_in:
            if not isinstance(a_project, project.Project):
                raise ValueError(
                    "any element in projects_lead should be an instance of "
                    "stalker.core.models.project.Project class")
        
        return ValidatedList(projects_lead_in, project.Project)
    
    
    
    #----------------------------------------------------------------------
    def _validate_sequences_lead(self, sequences_lead_in):
        """validates the given sequences_lead attribute
        """
        
        if sequences_lead_in is None:
            raise ValueError("sequences_lead attribute could not be None, try "
                             "setting it to an empty list")
        
        if not isinstance(sequences_lead_in, list):
            raise ValueError("sequences_lead should be a list of "
                             "stalker.core.models.sequence.Sequence objects")
        
        from stalker.core.models import sequence
        
        for a_sequence in sequences_lead_in:
            if not isinstance(a_sequence, sequence.Sequence):
                raise ValueError(
                    "any element in sequences_lead should be an instance of "
                    "stalker.core.models.sequence.Sequence class"
                )
        
        return ValidatedList(sequences_lead_in, sequence.Sequence)
    
    
    
    #----------------------------------------------------------------------
    def _validate_tasks(self, tasks_in):
        """validates the given taks attribute
        """
        
        if tasks_in is None:
            raise ValueError("tasks attribute could not be None, try setting "
                             "it to an empty list")
        
        if not isinstance(tasks_in, list):
            raise ValueError("tasks should be a list of "
                             "stalker.core.models.task.Task objects")
        
        from stalker.core.models import task
        
        for a_task in tasks_in:
            if not isinstance(a_task, task.Task):
                raise ValueError(
                    "any element in tasks should be an instance of "
                    "stalker.core.models.task.Task class")
        
        return ValidatedList(tasks_in, task.Task)
    
    
    
    #----------------------------------------------------------------------
    def department():
        
        def fget(self):
            return self._department
        
        def fset(self, department_in):
            self._department = self._validate_department(department_in)
        
        doc = """department of the user, it is a
        :class:`~stalker.core.models.department.Department` object"""
        
        return locals()
    
    department = property(**department())
    
    
    
    #----------------------------------------------------------------------
    def email():
        
        def fget(self):
            return self._email
        
        def fset(self, email_in):
            self._email = self._validate_email(email_in)
        
        doc = """email of the user, accepts strings or unicodes
        """
        
        return locals()
    
    email = property(**email())
    
    
    
    #----------------------------------------------------------------------
    def first_name():
        
        def fget(self):
            return self._first_name
        
        def fset(self, first_name_in):
            self._first_name = self._validate_first_name(first_name_in)
        
        doc = """first name of the user, accepts string or unicode"""
        
        return locals()
    
    first_name = property(**first_name())
    
    
    
    #----------------------------------------------------------------------
    def initials():
        
        def fget(self):
            return self._initials
        
        def fset(self, initials_in):
            self._intials = self._validate_initials(initials_in)
        
        return locals()
    
    initials = property(**initials())
    
    
    
    #----------------------------------------------------------------------
    def last_login():
        
        def fget(self):
            return self._last_login
        
        def fset(self, last_login_in):
            self._last_login = self._validate_last_login(last_login_in)
        
        doc = """last login time of the user as a datetime.datetime instance"""
        
        return locals()
    
    last_login = property(**last_login())
    
    
    
    #----------------------------------------------------------------------
    def last_name():
        
        def fget(self):
            return self._last_name
        
        def fset(self, last_name_in):
            self._last_name = self._validate_last_name(last_name_in)
        
        doc = """last name of the user, accepts string or unicode"""
        
        return locals()
    
    last_name = property(**last_name())
    
    
    
    #----------------------------------------------------------------------
    def login_name():
        
        def fget(self):
            return self._name
        
        def fset(self, login_name_in):
            self._name = self._validate_login_name(login_name_in)
            # set the name attribute
            #self._login_name = self._validate_name(login_name_in)
            self._login_name = self._name
            
            # also set the code
            self._code = self._validate_code(self._name)
        
        doc = """login name of the user, accepts string or unicode, also sets
        the name attribute"""
        
        return locals()
    
    login_name = property(**login_name())
    
    
    
    #----------------------------------------------------------------------
    def name():
        
        def fget(self):
            return self._name
        
        def fset(self, name_in):
            
            # set the login name first
            self._login_name = self._validate_login_name(name_in)
            self._name = self._login_name
            
            # also set the nice_name
            self._nice_name = self._condition_nice_name(self._name)
            
            # and also the code
            self.code = name_in
        
        doc = """the name of the user object, it is the synonym for the
        login_name"""
        
        return locals()
    
    name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def password():
        
        def fget(self):
            return base64.decodestring(self._password)
        
        def fset(self, password_in):
            self._password = base64.encodestring(
                self._validate_password(password_in)
            )
        
        doc = """password of the user, it is scrambled before stored in the
        _password attribute"""
        
        return locals()
    
    password = property(**password())
    
    
    
    #----------------------------------------------------------------------
    def permission_groups():
        
        def fget(self):
            return self._permission_groups
        
        def fset(self, permission_groups_in):
            self._permission_groups = \
                self._validate_permission_groups(permission_groups_in)
        
        doc = """permission groups that this users is a member of, accepts
        :class:`~stalker.core.models.group.Group` object"""
        
        return locals()
    
    permission_groups = property(**permission_groups())
    
    
    
    #----------------------------------------------------------------------
    def projects():
        
        def fget(self):
            return self._projects
        
        def fset(self, projects_in):
            self._projects = self._validate_projects(projects_in)
        
        doc = """projects those the current user assigned to, accepts
        :class:`~stalker.core.models.project.Project` object"""
        
        return locals()
    
    projects = property(**projects())
    
    
    
    #----------------------------------------------------------------------
    def projects_lead():
        
        def fget(self):
            return self._projects_lead
        
        def fset(self, projects_lead_in):
            self._projects_lead = \
                self._validate_projects_lead(projects_lead_in)
        
        doc = """projects lead by this current user, accepts
        :class:`~stalker.core.models.project.Project` object"""
        
        return locals()
    
    projects_lead = property(**projects_lead())
    
    
    
    #----------------------------------------------------------------------
    def sequences_lead():
        
        def fget(self):
            return self._sequences_lead
        
        def fset(self, sequences_lead_in):
            self._sequences_lead = \
                self._validate_sequences_lead(sequences_lead_in)
        
        doc = """sequences lead by this user, accpets
        :class:`~stalker.core.models.sequence.Sequence` objects"""
        
        return locals()
    
    sequences_lead = property(**sequences_lead())
    
    
    
    #----------------------------------------------------------------------
    def tasks():
        
        def fget(self):
            return self._tasks
        
        def fset(self, tasks_in):
            self._tasks = self._validate_tasks(tasks_in)
        
        doc = """tasks assigned to the current user, accepts
        :class:`~stalker.core.models.task.Task` objects"""
        
        return locals()
    
    tasks = property(**tasks())
    
    
    