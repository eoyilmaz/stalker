# -*- coding: utf-8 -*-

import sys
import os
import json
import re
import base64
import datetime
import pytz

from sqlalchemy import (Table, Column, Integer, ForeignKey, String, Enum,
                        Float)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, synonym, validates
from sqlalchemy.schema import UniqueConstraint

from stalker.db.declarative import Base
from stalker.db.types import GenericDateTime
from stalker.models.mixins import ACLMixin
from stalker.models.entity import Entity, SimpleEntity
from stalker.log import logging_level

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


LOGIN = 'login'
LOGOUT = 'logout'


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
      from stalker import db
      from stalker.models.auth import User, Group, Permission

      # first setup the db with the default database
      #
      # stalker.db.init() will create all the Actions possible with the
      # SOM classes automatically
      #
      # What is left to you is to create the permissions
      db.setup()

      user1 = User(
          name='Test User',
          login='test_user1',
          password='1234',
          email='testuser1@test.com'
      )
      user2 = User(
          name='Test User',
          login='test_user2',
          password='1234',
          email='testuser2@test.com'
      )

      group1 = Group(name='users')
      group1.users = [user1, user2]

      # get the permissions for the Project class
      project_permissions = Permission.query\
          .filter(Permission.access='Allow')\
          .filter(Permission.action='Create')\
          .filter(Permission.class_name='Project')\
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
    from stalker import defaults  # I know it is a weird place to import but we
                                  # need to do it in that way to limit the
                                  # import statement with a scope, because the
                                  # default can be updated
    __tablename__ = 'Permissions'
    __table_args__ = (
        UniqueConstraint('access', 'action', 'class_name'),
        {"extend_existing": True}
    )

    id = Column(Integer, primary_key=True)
    _access = Column('access', Enum('Allow', 'Deny', name='AccessNames'))
    _action = Column('action',
                     Enum(*defaults.actions, name='AuthenticationActions'))
    _class_name = Column('class_name', String(32))

    def __init__(self, access, action, class_name):
        self._access = self._validate_access(access)
        self._action = self._validate_action(action)
        self._class_name = self._validate_class_name(class_name)

    def __hash__(self):
        """returns the hash value for this instance
        """
        return hash(self.access + self.action + self.class_name)

    def _validate_access(self, access):
        """validates the given access value
        """
        from stalker import __string_types__
        if not isinstance(access, __string_types__):
            raise TypeError(
                '%s.access should be an instance of str not %s' % (
                    self.__class__.__name__,
                    access.__class__.__name__
                )
            )

        if access not in ['Allow', 'Deny']:
            raise ValueError(
                '%s.access should be "Allow" or "Deny" not %s' %
                (self.__class__.__name__, access)
            )

        return access

    def _access_getter(self):
        """returns the _access value
        """
        return self._access

    access = synonym('_access', descriptor=property(_access_getter))

    def _validate_class_name(self, class_name):
        """validates the given class_name value
        """
        from stalker import __string_types__
        if not isinstance(class_name, __string_types__):
            raise TypeError(
                '%s.class_name should be an instance of str not %s' %
                (self.__class__.__name__, class_name.__class__.__name__)
            )

        return class_name

    def _class_name_getter(self):
        """returns the _class_name attribute value
        """
        return self._class_name

    class_name = synonym(
        '_class_name',
        descriptor=property(_class_name_getter)
    )

    def _validate_action(self, action):
        """validates the given action value
        """
        from stalker import __string_types__
        if not isinstance(action, __string_types__):
            raise TypeError(
                '%s.action should be an instance of str not %s' %
                (self.__class__.__name__, action.__class__.__name__)
            )

        from stalker import defaults
        if action not in defaults.actions:
            raise ValueError(
                "%s.action should be one of the values of %s not '%s'" %
                (self.__class__.__name__, defaults.actions, action)
            )

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


class Group(Entity, ACLMixin):
    """Creates groups for users to be used in authorization system.

    A Group instance is nothing more than a list of :class:`.User` s created
    to be able to assign permissions in a group level.

    The Group class, as with the :class:`.User` class, is mixed with the
    :class:`.ACLMixin` which adds ability to hold :class:`.Permission`
    instances and serve ACLs to Pyramid.

    :param str name: The name of this group.
    :param list users: A list of :class:`.User` instances, holding the desired
      users in this group.
    """

    __auto_name__ = False
    __tablename__ = 'Groups'
    __mapper_args__ = {'polymorphic_identity': 'Group'}

    gid = Column("id", Integer, ForeignKey("Entities.id"),
                 primary_key=True)

    users = relationship(
        "User",
        secondary="Group_Users",
        back_populates="groups",
        doc="""Users in this group.

        Accepts:class:`.User` instance.
        """
    )

    def __init__(self, name='', users=None, permissions=None, **kwargs):
        if users is None:
            users = []

        if permissions is None:
            permissions = []

        kwargs.update({'name': name})
        super(Group, self).__init__(**kwargs)

        self.users = users
        self.permissions = permissions

    @validates('users')
    def _validate_users(self, key, user):
        """validates the given user instance
        """
        if not isinstance(user, User):
            raise TypeError(
                '%s.users attribute must all be stalker.models.auth.User '
                'instances not %s' %
                (self.__class__.__name__, user.__class__.__name__)
            )

        return user

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Group, self).__hash__()


class User(Entity, ACLMixin):
    """The user class is designed to hold data about a User in the system.

    .. note::
       .. versionadded 0.2.0: Task Watchers

       New to version 0.2.0 users can be assigned to a :class:`.Task` as a
       **Watcher**. Which can be used to inform the users in watchers list
       about the updates of certain Tasks.

    .. note::
       .. versionadded 0.2.0: Vacations

       It is now possible to define Vacations per user.

    .. note::
       .. versionadded 0.2.7: Resource Efficiency

    .. note::
       .. versionadded 0.2.11:

          Users not have a :attr:`.rate` attribute.

    :param rate:
       For future usage a rate attribute is added to the User to record the
       daily cost of this user as a resource. It should be either 0 or a
       positive integer or float value. Default is 0.

    :param efficiency:

      The efficiency is a multiplier for a user as a resource to a task and
      defines how much of the time spent for that particular task is counted as
      an actual effort. The default value is 1.0, lowest possible value is 0.0
      and there is no upper limit.

      The efficiency of a resource can be used for three purposes. First you
      can use it as a crude way to model a team. A team of 5 people should have
      an efficiency of 5.0. Keep in mind that you cannot track the members of
      the team individually if you use this feature. They always act as a
      group.

      Another use is to model performance variations between your resources.
      Again, this is a fairly crude mechanism and should be used with care. A
      resource that isn't every good at some task might be pretty good at
      another. This can't be taken into account as the resource efficiency can
      only set globally for all tasks.

      One another and interesting use is to model the availability of passive
      resources like a meeting room or a workstation or something that needs to
      be free for a task to take place but does not contribute to a task as an
      active resource.

      All resources that do not contribute effort to the task, that is a
      passive resource, should have an efficiency of 0.0. Again a typical
      example would be a conference room. It's necessary for a meeting, but it
      does not contribute any work.

    :param email: holds the e-mail of the user, should be in [part1]@[part2]
      format

    :type email: str

    :param login: This is the login name of the user, it should be all lower
      case. Giving a string that has uppercase letters, it will be converted to
      lower case. It can not be an empty string or None and it can not contain
      any white space inside.

    :type login: str

    :param departments: It is the departments that the user is a part of. It
      should be a list of Department objects. One user can be listed in
      multiple departments.

    :type departments: list of :class:`.Department` s

    :param password: it is the password of the user, can contain any character.
      Stalker doesn't store the raw passwords of the users. To check a stored
      password with a raw password use :meth:`.check_password` and to set the
      password you can use the :attr:`.password` property directly.

    :type password: str

    :param groups: It is a list of :class:`.Group` instances that this user
      belongs to.

    :type groups: list of :class:`.Group`

    :param tasks: it is a list of Task objects which holds the tasks that this
      user has been assigned to

    :type tasks: list of :class:`.Task` s

    :param last_login: it is a datetime.datetime object holds the last login
      date of the user (not implemented yet)

    :type last_login: datetime.datetime
    """
    __auto_name__ = False
    __tablename__ = "Users"
    __mapper_args__ = {"polymorphic_identity": "User"}

    user_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True
    )

    departments = association_proxy(
        'department_role',
        'department',
        creator=lambda d: create_department_user(d)
    )

    department_role = relationship(
        'DepartmentUser',
        back_populates='user',
        cascade='all, delete-orphan',
        primaryjoin='Users.c.id==Department_Users.c.uid',
        doc="""A list of :class:`.Department` s that
        this user is a part of"""
    )

    companies = association_proxy(
        'company_role',
        'client',
        creator=lambda n: create_client_user(n)
    )

    company_role = relationship(
        "ClientUser",
        back_populates="user",
        cascade='all, delete-orphan',
        primaryjoin="Users.c.id==Client_Users.c.uid",
        doc="""A list of :class:`.Client` s that this user is a part of."""
    )

    email = Column(
        String(256),
        unique=True,
        nullable=False,
        doc="email of the user, accepts string"
    )

    password = Column(
        String(256),
        nullable=False,
        doc="""The password of the user.

        It is scrambled before it is stored.
        """
    )

    login = Column(
        String(256),
        nullable=False,
        unique=True,
        doc="""The login name of the user.

        Can not be empty.
        """
    )

    authentication_logs = relationship(
        "AuthenticationLog",
        primaryjoin="AuthenticationLogs.c.uid==Users.c.id",
        back_populates="user",
        cascade='all, delete-orphan',
        doc="""A list of :class:`.AuthenticationLog` instances which holds the
        login/logout info for this :class:`.User`.
        """
    )

    groups = relationship(
        'Group',
        secondary='Group_Users',
        back_populates='users',
        doc="""Permission groups that this users is a member of.

        Accepts :class:`.Group` object.
        """
    )

    projects = association_proxy(
        'project_role',
        'project',
        creator=lambda p: create_project_user(p)
    )

    project_role = relationship(
        'ProjectUser',
        back_populates='user',
        cascade='all, delete-orphan',
        primaryjoin='Users.c.id==Project_Users.c.user_id'
    )

    tasks = relationship(
        "Task",
        secondary="Task_Resources",
        back_populates="resources",
        doc=""":class:`.Task` s assigned to this user.

        It is a list of :class:`.Task` instances.
        """
    )

    watching = relationship(
        'Task',
        secondary='Task_Watchers',
        back_populates='watchers',
        doc=''':class:`.Tasks` s that this user is
        assigned as a watcher.

        It is a list of :class:`.Task` instances.
        '''
    )

    responsible_of = relationship(
        'Task',
        secondary='Task_Responsible',
        primaryjoin='Users.c.id==Task_Responsible.c.responsible_id',
        secondaryjoin='Task_Responsible.c.task_id==Tasks.c.id',
        back_populates='_responsible',
        uselist=True,
        doc="""A list of :class:`.Task` instances that this user is responsible
        of."""
    )

    time_logs = relationship(
        "TimeLog",
        primaryjoin="TimeLogs.c.resource_id==Users.c.id",
        back_populates="resource",
        cascade='all, delete-orphan',
        doc="""A list of :class:`.TimeLog` instances which
        holds the time logs created for this :class:`.User`.
        """
    )

    vacations = relationship(
        'Vacation',
        primaryjoin='Vacations.c.user_id==Users.c.id',
        back_populates='user',
        cascade='all, delete-orphan',
        doc="""A list of :class:`.Vacation` instances
        which holds the vacations created for this :class:`.User`
        """
    )

    efficiency = Column(Float, default=1.0)

    rate = Column(Float, default=0.0)

    def __init__(
            self,
            name=None,
            login=None,
            email=None,
            password=None,
            departments=None,
            companies=None,
            groups=None,
            efficiency=1.0,
            rate=0.0,
            **kwargs):
        kwargs['name'] = name

        super(User, self).__init__(**kwargs)

        self.login = login

        if departments is None:
            departments = []

        # from stalker import DepartmentUser
        # for department in departments:
        #     self.department_role.append(
        #         DepartmentUser(user=self, department=department)
        #     )
        self.departments = departments

        if companies is None:
            companies = []
        self.companies = companies

        self.email = email

        # to be able to mangle the password do it like this
        self.password = password

        if groups is None:
            groups = []
        self.groups = groups

        self.tasks = []

        self.efficiency = efficiency
        self.rate = rate

    def __repr__(self):
        """return the representation of the current User
        """
        return "<%s ('%s') (User)>" % (self.name, self.login)

    def __eq__(self, other):
        """the equality operator
        """
        return super(User, self).__eq__(other) and \
            isinstance(other, User) and \
            self.email == other.email and \
            self.login == other.login and \
            self.name == other.name

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(User, self).__hash__()

    @validates("login")
    def _validate_login(self, key, login):
        """validates the given login value
        """
        if login is None:
            raise TypeError(
                '%s.login can not be None' % self.__class__.__name__
            )

        login = self._format_login(login)

        # raise a ValueError if the login is an empty string after formatting
        if login == '':
            raise ValueError(
                '%s.login can not be an empty string' %
                self.__class__.__name__
            )

        logger.debug("name out: %s" % login)

        return login

    @validates("email")
    def _validate_email(self, key, email_in):
        """validates the given email value
        """
        # check if email_in is an instance of string
        from stalker import __string_types__
        if not isinstance(email_in, __string_types__):
            raise TypeError(
                "%s.email should be an instance of str not %s" %
                (self.__class__.__name__, email_in.__class__.__name__)
            )
        return self._validate_email_format(email_in)

    def _validate_email_format(self, email_in):
        """formats the email
        """
        # split the mail from @ sign
        splits = email_in.split("@")
        len_splits = len(splits)

        # there should be one and only one @ sign
        if len_splits > 2:
            raise ValueError(
                "check the formatting of %s.email, there are more than one @ "
                "sign" % self.__class__.__name__
            )

        if len_splits < 2:
            raise ValueError(
                "check the formatting of %s.email, there is no @ sign" %
                self.__class__.__name__
            )

        if splits[0] == "":
            raise ValueError(
                "check the formatting of %s.email, the name part is missing" %
                self.__class__.__name__
            )

        if splits[1] == "":
            raise ValueError(
                "check the formatting %s.email, the domain part is missing" %
                self.__class__.__name__
            )

        return email_in

    @classmethod
    def _format_login(cls, login):
        """formats the given login value
        """
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

        Note:
            This function was updated to support both Python 2.7 and 3.5.
            It will now explicitly convert the base64 bytes object into
            a string object.
        """
        if password_in is None:
            raise TypeError(
                "%s.password cannot be None" % self.__class__.__name__
            )

        if password_in == "":
            raise ValueError(
                "%s.password can not be an empty string" %
                self.__class__.__name__
            )

        # mangle the password
        mangled_password_bytes = base64.b64encode(password_in.encode('utf-8'))

        if sys.version_info[0] == 2:
            mangled_password_str = str(mangled_password_bytes)
        else:
            # Assuming Python >= 3.5
            mangled_password_str = \
                str(mangled_password_bytes.decode('utf-8'))

        return mangled_password_str

    def check_password(self, raw_password):
        """Checks the given raw_password.

        Checks the given raw_password with the current User object's mangled
        password. Handles the encryption process behind the scene.

        Note:
            This function was updated to support both Python 2.7 and 3.5.
            It will now compare the string (str) versions of the given
            raw_password and the current Users object encrypted password.
        """
        mangled_password_str = str(self.password)
        raw_password_bytes = base64.b64encode(
            bytes(raw_password.encode('utf-8')))

        if sys.version_info[0] == 2:
            raw_password_encrypted_str = str(raw_password_bytes)
        else:
            # Assuming Python >= 3.5
            raw_password_encrypted_str = \
                str(raw_password_bytes.decode('utf-8'))

        return mangled_password_str == raw_password_encrypted_str

    @validates("groups")
    def _validate_groups(self, key, group):
        """check the given group
        """
        if not isinstance(group, Group):
            raise TypeError(
                "Any group in %s.groups should be an instance of "
                "stalker.models.auth.Group not %s" %
                (self.__class__.__name__, group.__class__.__name__)
            )

        return group

    @validates("tasks")
    def _validate_tasks(self, key, task):
        """validates the given tasks attribute
        """
        from stalker.models.task import Task

        if not isinstance(task, Task):
            raise TypeError(
                "Any element in %s.tasks should be an instance of "
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
                "Any element in %s.watching should be an instance of "
                "stalker.models.task.Task not %s" %
                (self.__class__.__name__, task.__class__.__name__)
            )
        return task

    @validates('vacations')
    def _validate_vacations(self, key, vacation):
        """validates the given vacation value
        """
        from stalker.models.studio import Vacation

        if not isinstance(vacation, Vacation):
            raise TypeError(
                "All of the elements in %s.vacations should be a "
                "stalker.models.studio.Vacation instance, not %s" %
                (self.__class__.__name__, vacation.__class__.__name__)
            )
        return vacation

    @validates('efficiency')
    def _validate_efficiency(self, key, efficiency):
        """validates the given efficiency value
        """
        if efficiency is None:
            efficiency = 1.0

        if not isinstance(efficiency, (int, float)):
            raise TypeError(
                '%(class)s.efficiency should be a float number greater or '
                'equal to 0.0, not %(efficiency_class)s' % {
                    'class': self.__class__.__name__,
                    'efficiency_class': efficiency.__class__.__name__
                }
            )

        if efficiency < 0:
            raise ValueError(
                '%(class)s.efficiency should be a float number greater or '
                'equal to 0.0, not %(efficiency)s' % {
                    'class': self.__class__.__name__,
                    'efficiency': efficiency
                }
            )

        return efficiency

    @validates('rate')
    def _validate_rate(self, key, rate):
        """validates the given rate value
        """
        if rate is None:
            rate = 0.0

        if not isinstance(rate, (int, float)):
            raise TypeError(
                '%(class)s.rate should be a float number greater or '
                'equal to 0.0, not %(rate_class)s' % {
                    'class': self.__class__.__name__,
                    'rate_class': rate.__class__.__name__
                }
            )

        if rate < 0:
            raise ValueError(
                '%(class)s.rate should be a float number greater or '
                'equal to 0.0, not %(rate)s' % {
                    'class': self.__class__.__name__,
                    'rate': rate
                }
            )

        return rate

    @property
    def tickets(self):
        """The list of :class:`.Ticket` s that this user has.

        returns a list of :class:`.Ticket` instances
        which this user is the owner of.
        """
        # do it with sqlalchemy
        from stalker import Ticket

        return Ticket.query \
            .filter(Ticket.owner == self) \
            .all()

    @property
    def open_tickets(self):
        """The list of open :class:`.Ticket` s that this user has.

        returns a list of :class:`.Ticket` instances which has a status of
        `Open` that this user is assigned as the owner.
        """
        from stalker import Ticket, Status
        return Ticket.query \
            .join(Status, Ticket.status) \
            .filter(Ticket.owner == self) \
            .filter(Status.code != 'CLS') \
            .all()

    @property
    def to_tjp(self):
        """outputs a TaskJuggler formatted string
        """
        from jinja2 import Template
        from stalker import defaults
        temp = Template(defaults.tjp_user_template, trim_blocks=True)
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

    @classmethod
    def default_json_serializer(cls, obj):
        """default serializer for json data
        """
        if isinstance(obj, datetime.datetime):
            return cls.datetime_to_millis(obj)
        elif isinstance(obj, User):
            return User.id
        elif isinstance(obj, int):
            return obj

    @classmethod
    def datetime_to_millis(cls, dt):
        """Default JSON serializer for datetime objects.

        code is based on the answer of Jay Taylor in
        http://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable-in-python

        :param dt: datetime.datetime instance
        """
        import calendar

        if isinstance(dt, datetime.datetime):
            if dt.utcoffset() is not None:
                dt = dt - dt.utcoffset()
        millis = int(
            calendar.timegm(dt.timetuple()) * 1000 +
            dt.microsecond / 1000
        )
        return millis

    @classmethod
    def millis_to_datetime(cls, millis):
        """
        :param int millis: an int value showing the millis from unix EPOCH
        :return:
        """
        epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
        return epoch + datetime.timedelta(milliseconds=millis)

    def load(self):
        """loads the data from the saved local session
        """
        try:
            with open(LocalSession.session_file_full_path(), 'r') as s:
                # try:
                json_object = json.load(s)
                valid_to = self.millis_to_datetime(json_object.get('valid_to'))
                if valid_to > datetime.datetime.now(pytz.utc):
                    # fill __dict__ with the loaded one
                    self.valid_to = valid_to
                    self.logged_in_user_id = \
                        json_object.get('logged_in_user_id')
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
        self.valid_to = datetime.datetime.now(pytz.utc) + \
                        datetime.timedelta(days=10)
        # serialize self
        dumped_data = json.dumps({
            'valid_to': self.valid_to,
            'logged_in_user_id': self.logged_in_user_id
        }, default=self.default_json_serializer)
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
        from stalker import defaults
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
                data_file.write(data)


class Role(Entity):
    """Defines a User role.

    .. versionadded 0.2.11: Roles

    When :class:`.User` s are assigned to a
    :class:`.Client`/:class:`.Department`, they also can be assigned to a role
    for that client/department.

    Also, because Users can be assigned to multiple clients/departments they
    can have different roles for each of this clients/departments.

    The duty of this class is to defined different roles that can be reused
    when required. So one can defined a **Lead** role and then assign a User to
    a department with its role is set to "lead". This essentially generalizes
    the previous implementation of now removed *Department.lead* attribute.
    """
    __auto_name__ = False
    __tablename__ = 'Roles'
    __mapper_args__ = {"polymorphic_identity": "Role"}

    role_id = Column(
        'id',
        Integer,
        ForeignKey('Entities.id'),
        primary_key=True
    )

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)


def create_department_user(department):
    """helper function to create DepartmentUser instance on association proxy
    """
    from stalker.models.department import DepartmentUser
    return DepartmentUser(department=department)


def create_client_user(client):
    """helper function to create ClientUser instance on association proxy
    """
    from stalker.models.client import ClientUser
    return ClientUser(client=client)


def create_project_user(project):
    """helper function to create ProjectUser instance on association proxy
    """
    from stalker.models.project import ProjectUser
    return ProjectUser(project=project)


# Group_Users
Group_Users = Table(
    "Group_Users", Base.metadata,
    Column("uid", Integer, ForeignKey("Users.id"), primary_key=True),
    Column("gid", Integer, ForeignKey("Groups.id"), primary_key=True)
)


class AuthenticationLog(SimpleEntity):
    """Keeps track of login/logout dates and the action (login or logout).
    """

    __auto_name__ = True
    __tablename__ = "AuthenticationLogs"
    __mapper_args__ = {"polymorphic_identity": "AuthenticationLog"}

    log_id = Column(
        'id',
        Integer,
        ForeignKey('SimpleEntities.id'),
        primary_key=True
    )

    user_id = Column(
        'uid',
        Integer,
        ForeignKey('Users.id'),
        nullable=False
    )

    user = relationship(
        'User',
        primaryjoin='AuthenticationLogs.c.uid==Users.c.id',
        uselist=False,
        back_populates='authentication_logs',
        doc="The :class:`.User` instance that this AuthenticationLog is "
        "created for"
    )

    action = Column(
        'action',
        Enum(LOGIN, LOGOUT, name='ActionNames'),
        nullable=False
    )

    date = Column(
        GenericDateTime,
        nullable=False
    )

    def __init__(self, user=None, date=None, action=LOGIN, **kwargs):
        super(AuthenticationLog, self).__init__(**kwargs)
        self.user = user
        self.date = date
        self.action = action

    def __lt__(self, other):
        """make this orderable
        """
        return (
            '%s %s %s' % (self.date, self.action, self.user.name),
            '%s %s %s' % (other.date, other.action, other.user.name)
        )

    @validates('user')
    def __validate_user__(self, key, user):
        """validates the given user argument value
        """
        if not isinstance(user, User):
            raise TypeError(
                '%s.user should be a User instance, not %s' % (
                    self.__class__.__name__,
                    user.__class__.__name__
                )
            )

        return user

    @validates('action')
    def __validate_action__(self, key, action):
        """validates the given action argument value
        """
        if action is None:
            import copy
            action = copy.copy(LOGIN)

        if action not in [LOGIN, LOGOUT]:
            raise ValueError(
                '%s.action should be one of "login" or "logout", not "%s"' % (
                    self.__class__.__name__,
                    action
                )
            )

        return action

    @validates('date')
    def __validate_date__(self, key, date):
        """validates the given date value
        """
        if date is None:
            date = datetime.datetime.now(pytz.utc)

        if not isinstance(date, datetime.datetime):
            raise TypeError(
                '%s.date should be a "datetime.datetime" instance, not %s' % (
                    self.__class__.__name__,
                    date.__class__.__name__
                )
            )

        return date
