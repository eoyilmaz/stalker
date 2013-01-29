# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
import re
import base64
import datetime

from sqlalchemy import (Table, Column, Integer, ForeignKey, String, DateTime,
                        Enum)
from sqlalchemy.orm import relationship, synonym, reconstructor, validates
from sqlalchemy.schema import UniqueConstraint

from pyramid.security import Allow

from stalker.conf import defaults
from stalker.db.declarative import Base
from stalker.models.mixins import ACLMixin
from stalker.models.entity import Entity

from stalker.log import logging_level
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

def group_finder(login, request):
    """Returns the group of the given login. The login name will be in
    'User:{login}' format.
    
    :param login: The login of the user, both '{login}' and
      'User:{login}' format is accepted.
    
    :param request: The Request object
    
    :return: Will return the groups of the user in ['Group:{group_name}']
      format.
    """
    if ':' in login:
        login = login.split(':')[1]
    
    # return the group of the given User object
    user_obj = User.query.filter_by(login=login).first()
    
    if user_obj:
        # just return the groups names if there is any group
        groups = user_obj.groups
        if len(groups):
            return map(lambda x:'Group:' + x.name, groups)
    
    return []

class RootFactory(object):
    """The main purpose of having a root factory is to generate the objects
    used as the context by the request. But in our case it just used to
    determine the default ACLs.
    """
   
    @property
    def __acl__(self):
        # create the default acl and give admins all the permissions
        all_permissions = map(
            lambda x: x.action + '_' + x.class_name,
            Permission.query.all()
        )
        
        d = defaults
        
        return [
            (Allow, 'Group:' + d.ADMIN_DEPARTMENT_NAME, all_permissions),
            (Allow, 'User:' + d.ADMIN_NAME, all_permissions)
        ]
    
    def __init__(self, request):
        pass

class Permission(Base):
    """A class to hold permissions.
    
    Permissions in Stalker defines what one can do or do not. A Permission
    instance is composed by three attributes; access, action and class_name.
    
    Permissions for all the classes in SOM are generally created by Stalker
    when initializing the database.
    
    If you created any custom classes to extend SOM you are also responsible to
    create the Permissions for it by calling :meth:`stalker.db.register` and
    passing your class to it. See the :mod:`stalker.db` documentation for
    details.
    
    :param str access: An Enum value which can have the one of the values of
      ``Allow`` or ``Deny``.
    
    :param str action: An Enum value from the list: 'Add', 'View', 'Edit',
      'Delete'. Can not be None. The list can be changed from
      defaults.DEFAULT_ACTIONS.
    
    :param str class_name: The name of the class that this action is applied
      to. Can not be None or an empty string.
    
    Example: Let say that you want to create a Permission specifying a Group of
    Users are allowed to create Projects::
      
      import transaction
      from stalker import db
      from stalker.db.session import DBSession, transaction
      from stalker.models.auth import User, Group, Permission
      
      # first setup the db with the default database
      #
      # stalker.db.__init_db__ will create all the Actions possible with the
      # SOM classes automatically
      # 
      # What is left to you is to create the permissions
      setup.db()
      
      user1 = User(login='test_user1', password='1234')
      user2 = User(login='test_user2', password='1234')
      
      group1 = Group(name='users')
      group1.users = [user1, user2]
      
      # get the permissions for the Project class
      project_permissions = DBSession.query(Permission)\
          .filter(Actions.access='Allow')\
          .filter(Actions.class_name='Project')\
          .filter(Actions.action='Add')\
          .first()
      
      # now we have the permission specifying the allowance of creating a
      # Project
      
      # to make group1 users able to create a Project we simple add this
      # Permission to the groups permission attribute
      group1.permissions.append(permission)
      
      # and persist this information in the database
      DBSession.add(group)
      transaction.commit()
    
    
    """
    __tablename__ = 'Permissions'
    __table_args__  = (
        UniqueConstraint('access', 'action', 'class_name'),
        {"extend_existing":True}
    )
    
    id = Column(Integer, primary_key=True)
    _access = Column('access', Enum('Allow', 'Deny', name='AccessNames'))
    _action = Column('action',
                     Enum(*defaults.DEFAULT_ACTIONS,name='ActionNames'))
    _class_name = Column('class_name', String)
    
    def __init__(self, access, action, class_name):
        self._access = self._validate_access(access)
        self._action = self._validate_action(action)
        self._class_name = self._validate_class_name(class_name)
    
    def _validate_access(self, access):
        """validates the given access value
        """
        if not isinstance(access, (str, unicode)):
            raise TypeError('Permission.access should be an instance of str '
                            'or unicode not %s' % access.__class__.__name__)
        
        if access not in ['Allow', 'Deny']:
            raise ValueError('Permission.access should be "Allow" or "Deny"' 
                             'not %s' % access)
        
        return access
    
    def _access_getter(self):
        """returns the _access value
        """
        return self._access
    
    access = synonym('_access', descriptor=property(_access_getter))
    
    def _validate_class_name(self, class_name):
        """validates the given class_name value
        """
        if not isinstance(class_name, (str, unicode)):
            raise TypeError('Permission.class_name should be an instance of '
                            'str or unicode not %s' % 
                            class_name.__class__.__name__)
        
        return class_name
    
    def _class_name_getter(self):
        """returns the _class_name attribute value
        """
        return self._class_name
    
    class_name = synonym('_class_name', descriptor=property(_class_name_getter))
    
    def _validate_action(self, action):
        """validates the given action value
        """
        
        if not isinstance(action, (str, unicode)):
            raise TypeError('Permission.action should be an instance of str '
                            'or unicode not %s' % action.__class__.__name__)
        
        if action not in defaults.DEFAULT_ACTIONS:
            raise ValueError('Permission.action should be one of the values '
                             'of %s not %s' % 
                             (defaults.DEFAULT_ACTIONS, action))
        
        return action
    
    def _action_getter(self):
        """returns the _action value
        """
        return self._action
    
    action = synonym('_action', descriptor=property(_action_getter))
    
    def __eq__(self, other):
        """the equality of two Permissions
        """
        return isinstance(other, Permission) \
            and other.access == self.access \
            and other.action == self.action \
            and other.class_name == self.class_name
    
    def __ne__(self, other):
        """the inequality of two Permissions
        """
        return not self.__eq__(other)

class Group(Entity, ACLMixin):
    """Creates groups for users to be used in authorization system.
    
    A Group instance is nothing more than a list of
    :class:`~stalker.models.auth.User`\ s created to be able to assign
    permissions in a group level.
    
    The Group class, as with the :class:`~stalker.models.auth.User` class, is
    mixed with the :class:`~stalker.models.mixins.ACLMixin` which adds ability
    to hold :class:`~stalker.models.mixin.Permission` instances and serve ACLs
    to Pyramid.
    """
    
    # TODO: Update Group class documentation
    __auto_name__ = False
    __tablename__ = "Groups"
    __mapper_args__ = {"polymorphic_identity": "Group"}

    gid = Column("id", Integer, ForeignKey("Entities.id"),
                 primary_key=True)
    
    users = relationship(
        "User",
        secondary="User_Groups",
        back_populates="groups",
        doc="""Users in this group.
        
        Accepts:class:`~stalker.models.auth.User` instance.
        """
    )
    
    def __init__(self, name='', users=None, **kwargs):
        if users is None:
            users = []
        kwargs.update({'name': name})
        super(Group, self).__init__(**kwargs)
        
        self.users = users
    
    @validates('users')
    def _validate_users(self, key, user):
        """validates the given user instance
        """
        if not isinstance(user, User):
            raise TypeError(
                'Group.users attribute must all be stalker.models.auth.User '
                'instances not %s' % user.__class__.__name__
            )
        
        return user

class User(Entity, ACLMixin):
    """The user class is designed to hold data about a User in the system.
    
    There are a couple of points to take your attention to:
    
    * The :attr:`~stalker.models.auth.User.code` attribute is derived from
      the :attr:`~stalker.models.auth.User.nice_name` as it is in a
      :class:`~stalker.models.entity.SimpleEntity`, but the
      :attr:`~stalker.models.auth.User.nice_name` is derived from the
      :attr:`~stalker.models.auth.User.login` instead of the
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
      
      Other than these two new rules all the previous formatting rules from the
      :class:`~stalker.models.entity.SimpleEntity` are valid.
    
    :param email: holds the e-mail of the user, should be in [part1]@[part2]
      format
    
    :type email: str, unicode
    
    :param login: This is the login name of the user, it should be all lower
      case. Giving a string or unicode that has uppercase letters, it will be
      converted to lower case. It can not be an empty string or None and it can
      not contain any white space inside.
    
    :type login: str, unicode
    
    :param departments: It is the departments that the user is a part of. It
      should be a list of Department objects. One user can be listed in
      multiple departments.
    
    :type departments: list of :class:`~stalker.models.department.Department`\ s
    
    :param password: it is the password of the user, can contain any character.
      Stalker doesn't store the raw passwords of the users. To check a stored
      password with a raw password use
      :meth:`~stalker.models.auth.User.check_password` and to set the password
      you can use the :attr:`~stalker.models.auth.User.password` property
      directly.
    
    :type password: str, unicode
    
    :param groups: It is a list of :class:`~stalker.models.auth.Group`
      instances that this user belongs to.
    
    :type groups: list of :class:`~stalker.models.auth.Group`
    
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
    """
    __auto_name__ = False
    __tablename__ = "Users"
    __mapper_args__ = {"polymorphic_identity": "User"}

    user_id = Column("id", Integer, ForeignKey("Entities.id"),
                     primary_key=True)
    
    departments = relationship(
        "Department",
        secondary='User_Departments',
        back_populates="members",
        doc="""A list of :class:`~stalker.models.department.Department`\ s that
        this user is a part of""",
    )
    
    email = Column(
        String(256),
        unique=True,
        nullable=False,
        doc="""email of the user, accepts strings or unicodes"""
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
    
    login = Column(
        String(256),
        nullable=False,
        doc="""The login name of the user.
        
        Can not be empty.
        """
    )
    
    groups = relationship(
        "Group",
        secondary="User_Groups",
        back_populates="users",
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
        name=None,
        login=None,
        email=None,
        password=None,
        departments=None,
        groups=None,
        projects_lead=None,
        sequences_lead=None,
        tasks=None,
        last_login=None,
        **kwargs
    ):
        kwargs['name'] = name
        
        super(User, self).__init__(**kwargs)

        self.login = login
        
        if departments is None:
            departments = []
        self.departments = departments
        
        self.email = email
        
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
        return "<User (%s ('%s'))>" % (self.name, self.login)

    def __eq__(self, other):
        """the equality operator
        """
        return super(User, self).__eq__(other) and\
               isinstance(other, User) and\
               self.email == other.email and\
               self.login == other.login and\
               self.name == other.name

    def __ne__(self, other):
        """the inequality operator
        """
        return not self.__eq__(other)

    @validates("login")
    def _validate_login(self, key, login):
        """validates the given login value
        """
        if login is None:
            raise TypeError('%s.login can not be None' %
                            self.__class__.__name__)
        
        login = self._format_login(login)
        
        # raise a ValueError if the login is an empty string after formatting
        if login == '':
            raise ValueError('%s.login can not be an empty string' %
                             self.__class__.__name__)
        
        logger.debug("name out: %s" % login)
        
        return login
    
    @validates("departments")
    def _validate_department(self, key, department):
        """validates the given department value
        """
        
        from stalker.models.department import Department
        
        # check if it is instance of Department object
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

#    @validates("initials")
#    def _validate_initials(self, key, initials):
#        """validates the given initials
#        """
#        
#        if initials is None:
#            raise TypeError('%s.initials can not be None' %
#                             self.__class__.__name__)
#        
#        if not isinstance(initials, str):
#            raise TypeError('%s.initials should be a string not %s' %
#                            (self.__class__.__name__,
#                             initials.__class__.__name__))
#        
#        if initials == '':
#            raise ValueError('%s.initials can not be an empty string' %
#                             self.__class__.__name__)
#        
#        initials = initials.lower()
#        
#        return initials

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

    def _format_login(self, login):
        """formats the given login value
        """
        # be sure it is a string
        login = str(login)
        
        # strip white spaces from start and end
        login = login.strip()
        
        # remove all the spaces
        login = login.replace(" ", "")
        
        # make it lowercase
        login = login.lower()
        
        # remove any illegal characters
        login = re.sub("[^\\(a-zA-Z0-9)]+", "", login)
        
        # remove any number at the beginning
        login = re.sub("^[0-9]+", "", login)
        
        return login

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
        
        # TODO: do it with SQLAlchemy
        projects = []
        for task in self.tasks:
            projects.append(task.task_of.project)

        return list(set(projects))

# USER_PERMISSIONGROUPS
User_Groups = Table(
    "User_Groups", Base.metadata,
    Column("uid", Integer, ForeignKey("Users.id"), primary_key=True),
    Column("gid", Integer, ForeignKey("Groups.id"), primary_key=True)
)

# USER_DEPARTMENTS
User_Departments = Table(
    'User_Departments', Base.metadata,
    Column('uid', Integer, ForeignKey('Users.id'), primary_key=True),
    Column('did', Integer, ForeignKey('Departments.id'), primary_key=True)
)
