# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
import re
import base64
import datetime

from pyramid.security import Allow, Everyone
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, synonym, reconstructor, validates

from stalker.db.declarative import Base
from stalker.models.entity import SimpleEntity, Entity

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class RootFactory(object):
    __acl__ = [
        #(Allow, Everyone, 'view'),
        #(Allow, 'group:editors', 'edit')
        (Allow, 'admin', 'view'),
        (Allow, 'admins', 'view')
    ]
    def __init__(self, request):
        pass

class Group(SimpleEntity):
    """Manages permission in the system.
    
    A Group object maps permission for tasks like Create, Read,
    Update, Delete operations in the system to available classes in the system.
    
    It reads the :attr:`~stalker.conf.defaults.CORE_MODEL_CLASSES` list to get
    the list of available classes which can be created. It then stores a binary
    value for each of the class.
    
    A :class:`~stalker.models.auth.User` can be in several
    :class:`~stalker.models.auth.Group`\ s. The combined permission
    for an object is calculated with an ``OR`` (``^``) operation. So if one of
    the :class:`~stalker.models.auth.Group`\ s of the
    :class:`~stalker.models.auth.User` is allowing the action then the user is
    allowed to do the operation.
    
    The permissions are stored in a dictionary. The key is the class name and
    the value is a 4-bit binary integer value like 0b0001.
    
    +-------------------+--------+--------+--------+------+
    |        0b         |   0    |   0    |   0    |  0   |
    +-------------------+--------+--------+--------+------+
    | binary identifier | Delete | Update | Create | Read |
    |                   | Bit    | Bit    | Bit    | Bit  |
    +-------------------+--------+--------+--------+------+
    
    :param dict permissions: A Python dictionary showing the permissions. The
      key is the name of the Class and the value is the permission bit.
    
    
    NOTE TO DEVELOPERS: a Dictionary-Based Collections should be used in
    SQLAlchemy.
    """
    
    # TODO: Update Group class documentation

    __tablename__ = "Groups"
    __mapper_args__ = {"polymorphic_identity": "Group"}

    gid = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                                primary_key=True)
    
    def __init__(self, **kwargs):
        super(Group, self).__init__(**kwargs)

class User(Entity):
    """The user class is designed to hold data about a User in the system.
    
    There are a couple of points to take your attention to:
    
    * The :attr:`~stalker.models.auth.User.code` attribute is derived from
      the :attr:`~stalker.models.auth.User.nice_name` as it is in a
      :class:`~stalker.models.entity.SimpleEntity`, but the
      :attr:`~stalker.models.auth.User.nice_name` is derived from the
      :attr:`~stalker.models.auth.User.login_name` instead of the
      :attr:`~stalker.models.auth.User.name` attribute, so the
      :attr:`~stalker.models.auth.User.code` of a
      :class:`~stalker.models.auth.User` and a
      :class:`~stalker.models.entity.SimpleEntity` will be different then each
      other. The formatting of the :attr:`~stalker.models.auth.User.code`
      attribute is as follows:
      
      * no underscore character is allowed, so while in the
        :class:`~stalker.models.entity.SimpleEntity` class the code could have
        underscores, in :class:`~stalker.models.auth.User` class it is not
        allowed.
      * all the letters in the code will be converted to lower case.
      
      Other than this two new rules all the previous formatting rules from the
      :class:`~stalker.models.entity.SimpleEntity` are still in charge.
      
    * The :attr:`~stalker.models.auth.User.name` is a synonym of the
      :attr:`~stalker.models.auth.User.login_name`, so changing one of them
      will change the other.
    
    :param email: holds the e-mail of the user, should be in [part1]@[part2]
      format
    
    :type email: unicode
    
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
    
    :type login_name: unicode
    
    :param first_name: it is the first name of the user, must be a string or
      unicode, middle name also can be added here, so it accepts white-spaces
      in the variable, but it will truncate the white spaces at the beginin and
      at the end of the variable and it can not be empty or None
    
    :type first_name: unicode
    
    :param last_name: it is the last name of the user, must be a string or
      unicode, again it can not contain any white spaces at the beggining and
      at the end of the variable and it can be an empty string or None
    
    :type last_name: unicode
    
    :param department: it is the department of the current user. It should be
      a Department object. One user can only be listed in one department. A
      user is allowed to have no department to make it easy to create a new
      user and create the department and assign the user it later.
    
    :type department: :class:`~stalker.models.department.Department`
    
    :param password: it is the password of the user, can contain any character.
      Stalker doesn't store the raw passwords of the users. To check a stored
      password with a raw password use
      :meth:`~stalker.models.auth.User.check_password` and to set the password
      you can use the :attr:`~stalker.models.auth.User.password` property
      directly.
    
    :type password: unicode
    
    :param groups: it is a list of groups that this user belongs to
    
    :type groups: :class:`~stalker.models.auth.Group`
    
    :param tasks: it is a list of Task objects which holds the tasks that this
      user has been assigned to
    
    :type tasks: list of :class:`~stalker.models.task.Task`\ s
    
    :param projects_lead: it is a list of Project objects that this user
      is the leader of, it is for back referencing purposes.
    
    :type projects_lead: list of :class:`~stalker.models.project.Project`\ s
    
    :param sequences_lead: it is a list of Sequence objects that this
      user is the leader of, it is for back referencing purposes
    
    :type sequences_lead: list of :class:`~stalker.models.sequence.Sequence`
    
    :param last_login: it is a datetime.datetime object holds the last login
      date of the user (not implemented yet)
    
    :type last_login: datetime.datetime
    
    :param initials: it is the initials of the users name, if nothing given it
      will be calculated from the first and last names of the user
    
    :type initials: unicode
    """

    __tablename__ = "Users"
    __mapper_args__ = {"polymorphic_identity": "User"}

    user_id = Column("id", Integer, ForeignKey("Entities.id"),
                     primary_key=True)

    department_id = Column(
        Integer,
        ForeignKey("Departments.id", use_alter=True, name="department_x"),
        )

    department = relationship(
        "Department",
        primaryjoin="Users.c.department_id==Departments.c.id",
        back_populates="members",
        uselist=False,
        doc=""":class:`~stalker.models.department.Department` of the user""",
        )

    email = Column(
        String(256),
        unique=True,
        nullable=False,
        doc="""email of the user, accepts strings or unicodes"""
    )

    first_name = Column(
        String(256),
        nullable=False,
        doc="""first name of the user, accepts string or unicode"""
    )

    last_name = Column(
        String(256),
        nullable=True,
        doc="""The last name of the user.
        
        It is a string and can be None or empty string"""
    )

    password = Column(
        String(256),
        nullable=False,
        doc="""The password of the user.
        
        It is scrambled before it is stored.
        """
    )

    last_login = Column(
        DateTime,
        doc="""The last login time of this user.
        
        It is an instance of datetime.datetime class."""
    )

    login_name = synonym(
        "name",
        doc="""The login name of the user.
        
        It is a synonym for the :attr:`~stalker.models.auth.User.name`
        attribute.
        """
    )

    initials = Column(
        String(16),
        doc="""The initials of the user.
        
        If not specified, it is the upper case form of first letters of the
        :attr:`~stalker.models.auth.User.first_name` and
        :attr:`~stalker.models.auth.User.last_name`"""
    )

    groups = relationship(
        "Group",
        secondary="User_Groups",
        doc="""Permission groups that this users is a member of.
        
        Accepts :class:`~stalker.models.auth.Group` object.
        """
    )

    projects_lead = relationship(
        "Project",
        primaryjoin="Projects.c.lead_id==Users.c.id",
        #uselist=True,
        back_populates="lead",
        doc=""":class:`~stalker.models.project.Project`\ s lead by this user.
        
        It is a list of :class:`~stalker.models.project.Project` instances.
        """
    )

    sequences_lead = relationship(
        "Sequence",
        primaryjoin="Sequences.c.lead_id==Users.c.id",
        uselist=True,
        back_populates="lead",
        doc=""":class:`~stalker.models.sequence.Sequence`\ s lead by this user.
        
        It is a list of :class:`~stalker.models.sequence.Sequence` instances.
        """
    )

    tasks = relationship(
        "Task",
        secondary="Task_Resources",
        back_populates="resources",
        doc=""":class:`~stalker.models.task.Task`\ s assigned to this user.
        
        It is a list of :class:`~stalker.models.task.Task` instances.
        """
    )

    bookings = relationship(
        "Booking",
        primaryjoin="Bookings.c.resource_id==Users.c.id",
        back_populates="resource",
        doc="""A list of :class:`~stalker.models.task.Booking` instances which
        holds the bookings created for this :class:`~stalker.models.auth.User`.
        """
    )

    def __init__(
        self,
        department=None,
        email="",
        first_name="",
        last_name="",
        login_name="",
        password="",
        groups=None,
        projects_lead=None,
        sequences_lead=None,
        tasks=None,
        last_login=None,
        initials="",
        **kwargs
    ):
        # use the login_name for name if there are no name attribute present
        name = kwargs.get("name")

        if name is None:
            name = login_name

        if login_name == "":
            login_name = name

        name = login_name
        kwargs["name"] = name

        super(User, self).__init__(**kwargs)

        self.department = department

        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.name = name
        self.login_name = login_name
        self.initials = initials

        # to be able to mangle the password do it like this
        self.password = password

        if groups is None:
            groups = []
        self.groups = groups

        self._projects = []

        if projects_lead is None:
            projects_lead = []
        self.projects_lead = projects_lead

        if sequences_lead is None:
            sequences_lead = []
        self.sequences_lead = sequences_lead

        if tasks is None:
            tasks = []

        self.tasks = tasks

        self.last_login = last_login

    @reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """

        self._projects = []
        # call the Entity __init_on_load__
        super(User, self).__init_on_load__()

    def __repr__(self):
        """return the representation of the current User
        """

        return "<User (%s %s ('%s'))>" %\
               (self.first_name, self.last_name, self.login_name)

    def __eq__(self, other):
        """the equality operator
        """

        return super(User, self).__eq__(other) and\
               isinstance(other, User) and\
               self.email == other.email and\
               self.login_name == other.login_name and\
               self.first_name == other.first_name and\
               self.last_name == other.last_name and\
               self.name == other.name

    def __ne__(self, other):
        """the inequality operator
        """

        return not self.__eq__(other)

    @validates("name")
    def _validate_name(self, key, name):
        """validates the given name value
        """

        logger.debug("name in: %s" % name)

        name = self._format_login_name(name)

        # also set the nice_name
        self._nice_name = self._format_nice_name(name)

        # and also the code
        self.code = name

        logger.debug("name out: %s" % name)

        return name

    @validates("department")
    def _validate_department(self, key, department):
        """validates the given department value
        """
        
        from stalker.models.department import Department

        # check if it is intance of Department object
        if department is not None:
            if not isinstance(department, Department):
                raise TypeError("%s.department should be instance of "
                                "stalker.models.department.Department not %s" %
                                (self.__class__.__name__,
                                 department.__class__.__name__))

        return department

    @validates("email")
    def _validate_email(self, key, email_in):
        """validates the given email value
        """

        # check if email_in is an instance of string or unicode
        if not isinstance(email_in, (str, unicode)):
            raise TypeError("%s.email should be an instance of string or "
                            "unicode not %s" %
                            (self.__class__.__name__,
                             email_in.__class__.__name__))

        return self._validate_email_format(email_in)

    def _validate_email_format(self, email_in):
        """formats the email
        """

        # split the mail from @ sign
        splits = email_in.split("@")
        len_splits = len(splits)

        # there should be one and only one @ sign
        if len_splits > 2:
            raise ValueError("check the %s.email formatting, there are more "
                             "than one @ sign" % self.__class__.__name__)

        if len_splits < 2:
            raise ValueError("check the %s.email formatting, there are no @ "
                             "sign" % self.__class__.__name__)

        if splits[0] == "":
            raise ValueError("check the %s.email formatting, the name part "
                             "is missing" % self.__class__.__name__)

        if splits[1] == "":
            raise ValueError("check the %s.email formatting, the domain part "
                             "is missing" % self.__class__.__name__)

        return email_in

    @validates("first_name")
    def _validate_first_name(self, key, first_name_in):
        """validates the given first_name attribute
        """

        if first_name_in is None:
            raise TypeError("%s.first_name cannot be None" %
                            self.__class__.__name__)

        if not isinstance(first_name_in, (str, unicode)):
            raise TypeError("%s.first_name should be instance of string or "
                            "unicode not %s" %
                            (self.__class__.__name__,
                             first_name_in.__class__.__name__))

        if first_name_in == "":
            raise ValueError("%s.first_name can not be an empty string" %
                             self.__class__.__name__)

        return first_name_in.strip().title()

    @validates("initials")
    def _validate_initials(self, key, initials_in):
        """validates the given initials
        """

        initials_in = str(initials_in)

        if initials_in == "":
            # derive the initials from the first and last name

            initials_in = re.sub("[^A-Z]+", "",
                                 self.first_name.title() + " " +\
                                 self.last_name.title()).lower()

        return initials_in

    @validates("last_login")
    def _validate_last_login(self, key, last_login_in):
        """validates the given last_login argument
        """

        if not isinstance(last_login_in, datetime.datetime) and\
           last_login_in is not None:
            raise TypeError("%s.last_login should be an instance of "
                            "datetime.datetime or None not %s" %
                            (self.__class__.__name__,
                             last_login_in.__class__.__name__))

        return last_login_in

    @validates("last_name")
    def _validate_last_name(self, key, last_name_in):
        """validates the given last_name attribute
        """

        if last_name_in is not None:
            if not isinstance(last_name_in, (str, unicode)):
                raise TypeError("%s.last_name should be instance of string "
                                "or unicode not %s" %
                                (self.__class__.__name__,
                                 last_name_in.__class__.__name__))
        else:
            last_name_in = ""

        return last_name_in.strip().title()

    def _format_name(self, name):
        """formats the given name
        """

        # be sure it is a string
        name = str(name)

        # strip white spaces from start and end
        name = name.strip()

        # remove all the spaces
        name = name.replace(" ", "")

        # make it lowercase
        name = name.lower()

        # remove any illegal characters
        name = re.sub("[^\\(a-zA-Z0-9)]+", "", name)

        # remove any number at the begining
        name = re.sub("^[0-9]+", "", name)

        return name

    @validates("password")
    def _validate_password(self, key, password_in):
        """validates the given password
        """

        if password_in is None:
            raise TypeError("%s.password cannot be None" %
                            self.__class__.__name__)
        
        if password_in == "":
            raise ValueError("raw_password can not be empty string")
        
        # mangle the password
        return base64.encodestring(password_in)
    
    def check_password(self, raw_password):
        """Checks the given raw_password.
        
        Checks the given raw_password with the current Users objects encrypted
        password.
        
        Checks the given raw password with the given encrypted password. Handles
        the encryption process behind the scene.
        """
        return self.password == base64.encodestring(str(raw_password))
    
    @validates("groups")
    def _validate_groups(self, key, group):
        """check the given group
        """
        
        if not isinstance(group, Group):
            raise TypeError(
                "any group in %s.groups should be an instance of"
                "stalker.models.auth.Group not %s" %
                (self.__class__.__name__, group.__class__.__name__)
            )

        return group

    @validates("projects_lead")
    def _validate_projects_lead(self, key, project):
        """validates the given projects_lead attribute
        """
        
        from stalker.models.project import Project
        
        if not isinstance(project, Project):
            raise TypeError(
                "any element in %s.projects_lead should be a"
                "stalker.models.project.Project instance not %s" %
                (self.__class__.__name__, project.__class__.__name__)
            )

        return project

    @validates("sequences_lead")
    def _validate_sequences_lead(self, key, sequence):
        """validates the given sequences_lead attribute
        """
        
        from stalker.models.sequence import Sequence
        
        if not isinstance(sequence, Sequence):
            raise TypeError(
                "any element in %s.sequences_lead should be an instance of "
                "stalker.models.sequence.Sequence not %s " %
                (self.__class__.__name__, sequence.__class__.__name__)
            )

        return sequence

    @validates("tasks")
    def _validate_tasks(self, key, task):
        """validates the given tasks attribute
        """
        
        from stalker.models.task import Task
        
        if not isinstance(task, Task):
            raise TypeError(
                "any element in %s.tasks should be an instance of "
                "stalker.models.task.Task not %s" %
                (self.__class__.__name__, task.__class__.__name__)
            )

        return task

    @property
    def projects(self):
        """The list of :class:`~stalker.models.project.Project`\ s those the current user assigned to.
        
        returns a list of :class:`~stalker.models.project.Project` objects.
        It is a read-only attribute. To assign a
        :class:`~stalker.models.auth.User` to a
        :class:`~stalker.models.project.Project`, you need to create a new
        :class:`~stalker.models.task.Task` with the
        :attr:`~stalker.models.task.Task.resources` is set to this
        :class:`~stalker.models.auth.User` and assign the
        :class:`~stalker.models.task.Task` to the
        :class:`~stalker.models.project.Project` by setting the
        :attr:`~stalker.models.task.Task.project` attribute of the
        :class:`~stalker.models.task.Task` to the
        :class:`~stalker.models.project.Project`.
        """

        #return self._projects
        projects = []
        for task in self.tasks:
            projects.append(task.task_of.project)

        return list(set(projects))

# USER_PERMISSIONGROUPS
User_Groups = Table(
    "User_Groups", Base.metadata,
    Column("uid", Integer, ForeignKey("Users.id"), primary_key=True),
    Column("gid", Integer, ForeignKey("Groups.id"),
           primary_key=True
    )
)

