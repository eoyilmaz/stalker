# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
import os
import pickle
import re
import base64
import datetime

from sqlalchemy import (Table, Column, Integer, ForeignKey, String, DateTime,
                        Enum)
from sqlalchemy.orm import relationship, synonym, reconstructor, validates
from sqlalchemy.schema import UniqueConstraint

from stalker import defaults
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
            return map(lambda x: 'Group:' + x.name, groups)

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

        # start with default ACLs

        ACLs = [
            ('Allow', 'Group:' + defaults.admin_department_name,
             all_permissions),
            ('Allow', 'User:' + defaults.admin_name, all_permissions)
        ]

        # get all users and their ACLs
        all_users = User.query.all()
        for user in all_users:
            ACLs.extend(user.__acl__)

        # get all groups and their ACLs
        all_groups = Group.query.all()
        for group in all_groups:
            ACLs.extend(group.__acl__)

        return ACLs

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

    :param str action: An Enum value from the list ['Create', 'Read', 'Update',
      'Delete', 'List']. Can not be None. The list can be changed from
      stalker.config.Config.default_actions.

    :param str class_name: The name of the class that this action is applied
      to. Can not be None or an empty string.

    Example: Let say that you want to create a Permission specifying a Group of
    Users are allowed to create Projects::

      from stalker import db
      from stalker.db.session import DBSession
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
      project_permissions = Permission.query\
          .filter(Actions.access='Allow')\
          .filter(Actions.action='Create')\
          .filter(Actions.class_name='Project')\
          .first()

      # now we have the permission specifying the allowance of creating a
      # Project

      # to make group1 users able to create a Project we simply add this
      # Permission to the groups permission attribute
      group1.permissions.append(permission)

      # and persist this information in the database
      DBSession.add(group)
      DBSession.commit()
    """
    __tablename__ = 'Permissions'
    __table_args__ = (
        UniqueConstraint('access', 'action', 'class_name'),
        {"extend_existing": True}
    )

    id = Column(Integer, primary_key=True)
    _access = Column('access', Enum('Allow', 'Deny', name='AccessNames'))
    _action = Column('action',
                     Enum(*defaults.actions, name='ActionNames'))
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

    class_name = synonym('_class_name',
                         descriptor=property(_class_name_getter))

    def _validate_action(self, action):
        """validates the given action value
        """

        if not isinstance(action, (str, unicode)):
            raise TypeError('Permission.action should be an instance of str '
                            'or unicode not %s' % action.__class__.__name__)

        if action not in defaults.actions:
            raise ValueError('Permission.action should be one of the values '
                             'of %s not %s' %
                             (defaults.actions, action))

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

    A Group instance is nothing more than a list of :class:`.User`\ s created
    to be able to assign permissions in a group level.

    The Group class, as with the :class:`.User` class, is mixed with the
    :class:`~stalker.models.mixins.ACLMixin` which adds ability to hold
    :class:`~stalker.models.mixin.Permission` instances and serve ACLs to
    Pyramid.
    """

    # TODO: Update Group class documentation
    __auto_name__ = False
    __tablename__ = 'Groups'
    __mapper_args__ = {'polymorphic_identity': 'Group'}

    gid = Column("id", Integer, ForeignKey("Entities.id"),
                 primary_key=True)

    users = relationship(
        "User",
        secondary="User_Groups",
        back_populates="groups",
        doc="""Users in this group.

        Accepts:class:`.User` instance.
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

    * The :attr:`.code` attribute is derived from the :attr:`.nice_name` as it
      is in a :class:`~stalker.models.entity.SimpleEntity`, but the
      :attr:`.nice_name` is derived from the :attr:`.login` instead of the
      :attr:`.name` attribute, so the :attr:`.code` of a :class:`.User` and a
      :class:`~stalker.models.entity.SimpleEntity` will be different then each
      other. The formatting of the :attr:`.code` attribute is as follows:

      * no underscore character is allowed, so while in the
        :class:`~stalker.models.entity.SimpleEntity` class the code could have
        underscores, in :class:`.User` class it is not
        allowed.
      * all the letters in the code will be converted to lower case.

      Other than these two new rules all the previous formatting rules from the
      :class:`~stalker.models.entity.SimpleEntity` are valid.

    .. note::
       .. versionadded 0.2.0: Task Watchers

       New to version 0.2.0 users can be assigned to a
       :class:`~stalker.models.task.Task` as a **Watcher**. Which can be used
       to inform the users in watchers list about the updates of certain Tasks.

    .. note::
       .. versionadded 0.2.0: Vacations

       It is now possible to define Vacations per user.

    .. note::
        .. deprecated 0.2.0: User.sequences_lead

        User.sequences_lead attribute has been deprecated. Use
        :attr:`.responsible_of` to query all the
        :class:`~stalker.models.task.Task`\ s and derivatives.

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
      password with a raw password use :meth:`.check_password` and to set the
      password you can use the :attr:`.password` property directly.

    :type password: str, unicode

    :param groups: It is a list of :class:`.Group` instances that this user
      belongs to.

    :type groups: list of :class:`.Group`

    :param tasks: it is a list of Task objects which holds the tasks that this
      user has been assigned to

    :type tasks: list of :class:`~stalker.models.task.Task`\ s

    :param projects_lead: it is a list of Project objects that this user
      is the leader of, it is for back referencing purposes.

    :type projects_lead: list of :class:`~stalker.models.project.Project`\ s

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
        doc="""email of the user, accepts strings or unicode"""
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
        'Group',
        secondary='User_Groups',
        back_populates='users',
        doc="""Permission groups that this users is a member of.

        Accepts :class:`.Group` object.
        """
    )

    projects = relationship(
        'Project',
        secondary='Project_Users',
        back_populates='users'
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

    tasks = relationship(
        "Task",
        secondary="Task_Resources",
        back_populates="resources",
        doc=""":class:`~stalker.models.task.Task`\ s assigned to this user.

        It is a list of :class:`~stalker.models.task.Task` instances.
        """
    )

    watching = relationship(
        'Task',
        secondary='Task_Watchers',
        back_populates='watchers',
        doc=''':class:`~stalker.models.task.Tasks`\ s that this user is
        assigned as a watcher.

        It is a list of :class:`~stalker.models.task.Task` instances.
        '''
    )

    responsible_of = relationship(
        'Task',
        primaryjoin='Users.c.id==Tasks.c.responsible_id',
        back_populates='_responsible',
        uselist=True,
        doc='''A list of :class:`~stalker.models.task.Task` instances that this user is responsible of.
        '''
    )

    time_logs = relationship(
        "TimeLog",
        primaryjoin="TimeLogs.c.resource_id==Users.c.id",
        back_populates="resource",
        cascade='all, delete-orphan',
        doc="""A list of :class:`~stalker.models.task.TimeLog` instances which
        holds the time logs created for this :class:`.User`.
        """
    )

    vacations = relationship(
        'Vacation',
        primaryjoin='Vacations.c.user_id==Users.c.id',
        back_populates='user',
        cascade='all, delete-orphan',
        doc="""A list of :class:`~stalker.models.studio.Vacation` instances
        which holds the vacations created for this :class:`.User`
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
            tasks=None,
            watching=None,
            # TODO: Watchlist should be a list of lists `WatchLists` so one can create task lists (playlists) for different tasks
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

        if projects_lead is None:
            projects_lead = []
        self.projects_lead = projects_lead

        if tasks is None:
            tasks = []

        self.tasks = tasks

        if watching is None:
            watching = []

        self.last_login = last_login

    # @reconstructor
    # def __init_on_load__(self):
    #     """initialized the instance variables when the instance created with
    #     SQLAlchemy
    #     """
    #     # call the Entity __init_on_load__
    #     super(User, self).__init_on_load__()

    def __repr__(self):
        """return the representation of the current User
        """
        return "<User (%s ('%s'))>" % (self.name, self.login)

    def __eq__(self, other):
        """the equality operator
        """
        return super(User, self).__eq__(other) and \
               isinstance(other, User) and \
               self.email == other.email and \
               self.login == other.login and \
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

    @validates("last_login")
    def _validate_last_login(self, key, last_login_in):
        """validates the given last_login argument
        """
        if not isinstance(last_login_in, datetime.datetime) and \
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

        Checks the given raw password with the given encrypted password.
        Handles the encryption process behind the scene.
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

    @validates("watching")
    def _validate_watching(self, key, task):
        """validates the given watching attribute
        """
        from stalker.models.task import Task

        if not isinstance(task, Task):
            raise TypeError(
                "any element in %s.watching should be an instance of "
                "stalker.models.task.Task not %s" %
                (self.__class__.__name__, task.__class__.__name__)
            )
        return task

    @validates('projects')
    def _validate_projects(self, key, project):
        """validates the given project instance
        """
        from stalker import Project

        if not isinstance(project, Project):
            raise TypeError('%s.projects should a list of '
                            'stalker.models.project.Project instances, not '
                            '%s' % (self.__class__.__name__,
                                    project.__class__.__name__))
        return project

    @validates('vacations')
    def _validate_vacations(self, key, vacation):
        """validates the given vacation value
        """
        from stalker.models.studio import Vacation

        if not isinstance(vacation, Vacation):
            raise TypeError("Every member of %s.vacations should be an "
                            "instance of stalker.models.studio.Vacation, "
                            "not %s" %
                            (self.__class__.__name__,
                             vacation.__class__.__name__))

        return vacation

    @property
    def tickets(self):
        """The list of :class:`~stalker.models.ticket.Ticket`\ s that this user has.

        returns a list of :class:`~stalker.models.ticket.Ticket` instances
        which are derived from the :class:`~stalker.models.task.Task`\ s that
        this user is assigned to
        (Stalker checks the related :class:`~stalker.models.version.Version`
        instances and then the `~stalker.models.ticket.Ticket` instances
        assigned to the Versions.).
        """
        # do it with sqlalchemy
        from stalker import Ticket

        return Ticket.query \
            .filter(Ticket.owner == self) \
            .all()

    @property
    def open_tickets(self):
        """The list of open :class:`~stalker.models.ticket.Ticket`\ s that this user has.

        returns a list of :class:`~stalker.models.ticket.Ticket` instances
        which has a status of `Open` and are derived from the
        :class:`~stalker.models.task.Task`\ s that this user is assigned to
        (Stalker checks the related :class:`~stalker.models.version.Version`
        instances and then the `~stalker.models.ticket.Ticket` instances
        assigned to the Version and has a status of `Open`.).
        """
        # do it with sqlalchemy
        from stalker import Ticket, Status

        return Ticket.query \
            .filter(Ticket.owner == self) \
            .join(Ticket.status) \
            .filter(Status.code != 'CLOSED') \
            .all()

    @property
    def to_tjp(self):
        """outputs a TaskJuggler formatted string
        """
        from jinja2 import Template

        temp = Template(defaults.tjp_user_template)
        return temp.render({'user': self})


class LocalSession(object):
    """A simple temporary session object which simple stores session data.

    This class will later be removed, it is here because we need a login window
    for the Qt user interfaces.

    On initialize it will load the SessionData from the users .strc folder
    """

    def __init__(self):
        self.logged_in_user_id = None
        self.valid_to = None
        self.session_data = None
        self.load()

    def load(self):
        """loads the data from the saved local session
        """
        try:
            with open(LocalSession.session_file_full_path(), 'r') as s:
                # try:
                unpickled_object = pickle.load(s)
                if unpickled_object.valid_to > datetime.datetime.now():
                    # fill __dict__ with the loaded one
                    self.__dict__ = unpickled_object.__dict__
        except IOError:
            pass

    @property
    def logged_in_user(self):
        """returns the logged in user
        """
        return User.query.filter_by(id=self.logged_in_user_id).first()

    def store_user(self, user):
        """stores the given user instance

        :param user: The user instance. 
        """
        if user:
            self.logged_in_user_id = user.id

    def save(self):
        """remembers the data in user local file system
        """
        self.valid_to = datetime.datetime.now() + datetime.timedelta(10)
        # serialize self
        dumped_data = pickle.dumps(self)
        logger.debug('dumped session data : %s' % dumped_data)
        self._write_data(dumped_data)

    def delete(self):
        """removes the cache file
        """
        try:
            os.remove(self.session_file_full_path())
        except OSError:
            pass

    @classmethod
    def session_file_full_path(cls):
        """
        :return str: the session file full path
        """
        return os.path.normpath(os.path.join(
            defaults.local_storage_path,
            defaults.local_session_data_file_name
        ))

    def _write_data(self, data):
        """Writes the given data to the local session file

        :param data: the data to be written (generally serialized LocalSession
          class itself)
        """
        file_full_path = self.session_file_full_path()

        # create the path first
        file_path = os.path.dirname(file_full_path)
        try:
            os.makedirs(file_path)
        except OSError:
            # dir exists
            pass
        finally:
            with open(file_full_path, 'w') as data_file:
                data_file.writelines(data)


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
