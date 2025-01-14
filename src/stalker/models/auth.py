# -*- coding: utf-8 -*-
"""Authentication related classes and functions situated here."""
import base64
import copy
import json
import os
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

import pytz

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship, synonym, validates
from sqlalchemy.schema import UniqueConstraint

from stalker import defaults, log
from stalker.db.declarative import Base
from stalker.db.types import GenericDateTime
from stalker.models.entity import Entity, SimpleEntity
from stalker.models.mixins import ACLMixin
from stalker.models.status import Status
from stalker.utils import datetime_to_millis, millis_to_datetime

if TYPE_CHECKING:  # pragma: no cover
    from stalker.models.client import Client, ClientUser
    from stalker.models.department import Department, DepartmentUser
    from stalker.models.project import Project, ProjectUser
    from stalker.models.task import Task, TimeLog
    from stalker.models.ticket import Ticket
    from stalker.models.studio import Vacation

logger = log.get_logger(__name__)

LOGIN = "login"
LOGOUT = "logout"


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

    Example: Let say that you want to create a Permission specifying a Group of
    Users are allowed to create Projects::

    .. code-block:: Python

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

    Args:
        access (str): An Enum value which can have the one of the values of
            ``Allow`` or ``Deny``.
        action (str): An Enum value from the list ['Create', 'Read', 'Update',
            'Delete', 'List']. Cannot be None. The list can be changed from
            stalker.config.Config.default_actions.

        class_name (str): The name of the class that this action is applied
            to. Cannot be None or an empty string.
    """

    __tablename__ = "Permissions"
    __table_args__ = (
        UniqueConstraint("access", "action", "class_name"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    _access: Mapped[Optional[str]] = mapped_column(
        "access", Enum("Allow", "Deny", name="AccessNames")
    )
    _action: Mapped[Optional[str]] = mapped_column(
        "action", Enum(*defaults.actions, name="AuthenticationActions")
    )
    _class_name: Mapped[Optional[str]] = mapped_column("class_name", String(32))

    def __init__(self, access: str, action: str, class_name: str) -> None:
        super(Permission, self).__init__()
        self._access = self._validate_access(access)
        self._action = self._validate_action(action)
        self._class_name = self._validate_class_name(class_name)

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return hash(self.access + self.action + self.class_name)

    def _validate_access(self, access: str) -> str:
        """Validate the given access value.

        Args:
            access (str): The access value to be validated.

        Raises:
            TypeError: If the given access value is not a str.
            ValueError: If the access is not a one of ["Access", "Deny"].

        Returns:
            str: The access value.
        """
        if not isinstance(access, str):
            raise TypeError(
                f"{self.__class__.__name__}.access should be an instance of str, "
                f"not {access.__class__.__name__}: '{access}'"
            )

        if access not in ["Allow", "Deny"]:
            raise ValueError(
                f'{self.__class__.__name__}.access should be "Allow" or "Deny" '
                f"not {access}"
            )

        return access

    def _access_getter(self) -> str:
        """Return the _access value.

        Returns:
            str: Returns the access value.
        """
        return self._access

    access: Mapped[Optional[str]] = synonym(
        "_access", descriptor=property(_access_getter)
    )

    def _validate_class_name(self, class_name: str) -> str:
        """Validate the given class_name value.

        Args:
            class_name (str): The class name.

        Raises:
            TypeError: If the class_name is not a str.

        Returns:
            str: The validated class_name.
        """
        if not isinstance(class_name, str):
            raise TypeError(
                f"{self.__class__.__name__}.class_name should be an instance of str, "
                f"not {class_name.__class__.__name__}: '{class_name}'"
            )

        return class_name

    def _class_name_getter(self) -> str:
        """Return the _class_name attribute value.

        Returns:
            str: The class name.
        """
        return self._class_name

    class_name: Mapped[str] = synonym(
        "_class_name", descriptor=property(_class_name_getter)
    )

    def _validate_action(self, action: str) -> str:
        """Validate the given action value.

        Args:
            action (str): The action value.

        Raises:
            TypeError: If the action is not a str value.
            ValueError: If the given action is not in the "defaults.actions" list.

        Returns:
            str: The validated action value.
        """
        if not isinstance(action, str):
            raise TypeError(
                f"{self.__class__.__name__}.action should be an instance of str, "
                f"not {action.__class__.__name__}: '{action}'"
            )

        if action not in defaults.actions:
            raise ValueError(
                f"{self.__class__.__name__}.action should be one of the values of "
                f"{defaults.actions} not '{action}'"
            )

        return action

    def _action_getter(self) -> str:
        """Return the _action value.

        Returns:
            str: Returns the action value.
        """
        return self._action

    action: Mapped[Optional[str]] = synonym(
        "_action", descriptor=property(_action_getter)
    )

    def __eq__(self, other: Any) -> bool:
        """Check if the other Permission is equal to this one.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is a Permission instance and has the same
                access, action and class_name attributes.
        """
        return (
            isinstance(other, Permission)
            and other.access == self.access
            and other.action == self.action
            and other.class_name == self.class_name
        )


class Group(Entity, ACLMixin):
    """Creates groups for users to be used in authorization system.

    A Group instance is nothing more than a list of :class:`.User` s created
    to be able to assign permissions in a group level.

    The Group class, as with the :class:`.User` class, is mixed with the
    :class:`.ACLMixin` which adds ability to hold :class:`.Permission`
    instances and serve ACLs to Pyramid.

    Args:
        name (str): The name of this group.
        users list: A list of :class:`.User` instances holding the desired
            users in this group.
    """

    __auto_name__ = False
    __tablename__ = "Groups"
    __mapper_args__ = {"polymorphic_identity": "Group"}

    gid: Mapped[int] = mapped_column("id", ForeignKey("Entities.id"), primary_key=True)

    users: Mapped[Optional[List["User"]]] = relationship(
        "User",
        secondary="Group_Users",
        back_populates="groups",
        doc="""Users in this group.

        Accepts:class:`.User` instance.
        """,
    )

    def __init__(self, name="", users=None, permissions=None, **kwargs) -> None:
        if users is None:
            users = []

        if permissions is None:
            permissions = []

        kwargs.update({"name": name})
        super(Group, self).__init__(**kwargs)

        self.users = users
        self.permissions = permissions

    @validates("users")
    def _validate_users(self, key: str, user: "User") -> "User":
        """Validate the given user value.

        Args:
            key (str): The name of the validated column.
            user (User): The :class:`.User` instance.

        Raises:
            TypeError: If the given user is not a :class:`.User` instance.

        Returns:
            User: The validated :class:`.User` instance.
        """
        if not isinstance(user, User):
            raise TypeError(
                f"{self.__class__.__name__}.users should only contain "
                "instances of stalker.models.auth.User, "
                f"not {user.__class__.__name__}: '{user}'"
            )

        return user

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
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

    Args:
        rate: For future usage a rate attribute is added to the User to record
            the daily cost of this user as a resource. It should be either 0 or
            a positive integer or float value. Default is 0.
        efficiency : The efficiency is a multiplier for a user as a resource to
            a task and defines how much of the time spent for that particular
            task is counted as an actual effort. The default value is 1.0,
            lowest possible value is 0.0 and there is no upper limit.

            The efficiency of a resource can be used for three purposes. First
            you can use it as a crude way to model a team. A team of 5 people
            should have an efficiency of 5.0. Keep in mind that you cannot track
            the members of the team individually if you use this feature. They
            always act as a group.

            Another use is to model performance variations between your resources.
            Again, this is a fairly crude mechanism and should be used with care.
            A resource that isn't every good at some task might be pretty good
            at another. This can't be taken into account as the resource efficiency
            can only set globally for all tasks.

            One another and interesting use is to model the availability of passive
            resources like a meeting room or a workstation or something that needs
            to be free for a task to take place but does not contribute to a task
            as an active resource.

            All resources that do not contribute effort to the task, that is a
            passive resource, should have an efficiency of 0.0. Again a typical
            example would be a conference room. It's necessary for a meeting,
            but it does not contribute any work.
        email (str): holds the e-mail of the user, should be in [part1]@[part2]
            format.
        login (str): This is the login name of the user, it should be all lower
            case. Giving a string that has uppercase letters, it will be converted
            to lower case. It cannot be an empty string or None and it cannot
            contain any white space inside.
        departments (List[Department]): It is the departments that the user is
            a part of. It should be a list of Department objects. One user can
            be listed in multiple departments.
        password (str): it is the password of the user, can contain any character.
            Stalker doesn't store the raw passwords of the users. To check a stored
            password with a raw password use :meth:`.check_password` and to set
            the password you can use the :attr:`.password` property directly.
        groups (List[Group]): It is a list of :class:`.Group` instances that this
            user belongs to.
        tasks (List[Task]): it is a list of Task objects which holds the tasks
            that this user has been assigned to.
        last_login (datetime): it is a datetime object holds the last login
            date of the user (not implemented yet).
    """

    __auto_name__ = False
    __tablename__ = "Users"
    __mapper_args__ = {"polymorphic_identity": "User"}

    user_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )

    departments = association_proxy(
        "department_role", "department", creator=lambda d: create_department_user(d)
    )

    department_role: Mapped[Optional[List["DepartmentUser"]]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        primaryjoin="Users.c.id==Department_Users.c.uid",
        doc="""A list of :class:`.Department` s that
        this user is a part of""",
    )

    companies = association_proxy(
        "company_role", "client", creator=lambda n: create_client_user(n)
    )

    company_role: Mapped[Optional[List["ClientUser"]]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        primaryjoin="Users.c.id==Client_Users.c.uid",
        doc="""A list of :class:`.Client` s that this user is a part of.""",
    )

    email: Mapped[str] = mapped_column(
        String(256),
        unique=True,
        nullable=False,
        doc="email of the user, accepts string",
    )

    password: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        doc="""The password of the user.

        It is scrambled before it is stored.
        """,
    )

    login: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        doc="""The login name of the user.

        Cannot be empty.
        """,
    )

    authentication_logs: Mapped[Optional[List["AuthenticationLog"]]] = relationship(
        primaryjoin="AuthenticationLogs.c.uid==Users.c.id",
        back_populates="user",
        cascade="all, delete-orphan",
        doc="""A list of :class:`.AuthenticationLog` instances which holds the
        login/logout info for this :class:`.User`.
        """,
    )

    groups: Mapped[Optional[List["Group"]]] = relationship(
        secondary="Group_Users",
        back_populates="users",
        doc="""Permission groups that this users is a member of.

        Accepts :class:`.Group` object.
        """,
    )

    projects = association_proxy(
        "project_role", "project", creator=lambda p: create_project_user(p)
    )

    project_role: Mapped[Optional[List["ProjectUser"]]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        primaryjoin="Users.c.id==Project_Users.c.user_id",
    )

    tasks: Mapped[Optional[List["Task"]]] = relationship(
        secondary="Task_Resources",
        back_populates="resources",
        doc=""":class:`.Task` s assigned to this user.

        It is a list of :class:`.Task` instances.
        """,
    )

    watching: Mapped[Optional[List["Task"]]] = relationship(
        secondary="Task_Watchers",
        back_populates="watchers",
        doc=""":class:`.Tasks` s that this user is
        assigned as a watcher.

        It is a list of :class:`.Task` instances.
        """,
    )

    responsible_of: Mapped[Optional[List["Task"]]] = relationship(
        secondary="Task_Responsible",
        primaryjoin="Users.c.id==Task_Responsible.c.responsible_id",
        secondaryjoin="Task_Responsible.c.task_id==Tasks.c.id",
        back_populates="_responsible",
        doc="""A list of :class:`.Task` instances that this user is responsible
        of.""",
    )

    time_logs: Mapped[Optional[List["TimeLog"]]] = relationship(
        primaryjoin="TimeLogs.c.resource_id==Users.c.id",
        back_populates="resource",
        cascade="all, delete-orphan",
        doc="""A list of :class:`.TimeLog` instances which
        holds the time logs created for this :class:`.User`.
        """,
    )

    vacations: Mapped[Optional[List["Vacation"]]] = relationship(
        primaryjoin="Vacations.c.user_id==Users.c.id",
        back_populates="user",
        cascade="all, delete-orphan",
        doc="""A list of :class:`.Vacation` instances
        which holds the vacations created for this :class:`.User`
        """,
    )

    efficiency: Mapped[Optional[float]] = mapped_column(default=1.0)

    rate: Mapped[Optional[float]] = mapped_column(default=0.0)

    def __init__(
        self,
        name: Optional[str] = None,
        login: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        departments: Optional["Department"] = None,
        companies: Optional["Client"] = None,
        groups: Optional["Group"] = None,
        efficiency: float = 1.0,
        rate: float = 0.0,
        **kwargs: Optional[Dict[str, Any]],
    ) -> None:
        kwargs["name"] = name

        super(User, self).__init__(**kwargs)

        self.login = login

        if departments is None:
            departments = []

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

    def __repr__(self) -> str:
        """Return the representation of the current User.

        Returns:
            str: The str representation of this User.
        """
        return f"<{self.name} ('{self.login}') (User)>"

    def __eq__(self, other: Any) -> bool:
        """Check if the other User is equal to this one.

        Args:
            other (Any): The other user instance.

        Returns:
            bool: If the other object is equal to this one, meaning that it is a User
                instance, has the same name, login and email values then returns True.
        """
        return (
            super(User, self).__eq__(other)
            and isinstance(other, User)
            and self.email == other.email
            and self.login == other.login
            and self.name == other.name
        )

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(User, self).__hash__()

    @validates("login")
    def _validate_login(self, key: str, login: str) -> str:
        """Validate and format the given login value.

        Args:
            key (str): The name of the validated column.
            login (str): The login to be validated.

        Raises:
            TypeError: If the login is not a str.
            ValueError: If the login is an empty string after formatting.

        Returns:
            str: The validated and formatted login value.
        """
        if login is None:
            raise TypeError(f"{self.__class__.__name__}.login cannot be None")

        login = self._format_login(login)

        # raise a ValueError if the login is an empty string after formatting
        if login == "":
            raise ValueError(
                f"{self.__class__.__name__}.login cannot be an empty string"
            )

        logger.debug(f"name out: {login}")

        return login

    @validates("email")
    def _validate_email(self, key: str, email: str) -> str:
        """Validate the given email value.

        Args:
            key (str): The name of the validated column.
            email (str): The email to be validated.

        Raises:
            TypeError: If the given email is not a str.

        Returns:
            str: The validated email value.
        """
        # check if email is an instance of string
        if not isinstance(email, str):
            raise TypeError(
                f"{self.__class__.__name__}.email should be an instance of str, not "
                f"{email.__class__.__name__}: '{email}'"
            )
        return self._validate_email_format(email)

    def _validate_email_format(self, email: str) -> str:
        """Validate the email format.

        Args:
            email (str): The email value to be validated.

        Raises:
            ValueError: If the email doesn't have a "@" sign in it, or it has more than
                one "@" sign in it, or after formatting the account name part or the
                domain name part becomes an empty string.

        Returns:
            str: The validated email value.
        """
        # split the mail from @ sign
        splits = email.split("@")
        len_splits = len(splits)

        # there should be one and only one @ sign
        if len_splits > 2:
            raise ValueError(
                f"check the formatting of {self.__class__.__name__}.email, "
                "there are more than one @ sign"
            )

        if len_splits < 2:
            raise ValueError(
                f"check the formatting of {self.__class__.__name__}.email, "
                "there is no @ sign"
            )

        if splits[0] == "":
            raise ValueError(
                f"check the formatting of {self.__class__.__name__}.email, "
                "the name part is missing"
            )

        if splits[1] == "":
            raise ValueError(
                f"check the formatting {self.__class__.__name__}.email, "
                "the domain part is missing"
            )

        return email

    @classmethod
    def _format_login(cls, login: str) -> str:
        """Format the given login value.

        Args:
            login (str): The login value.

        Returns:
            str: The formatted login value.
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
    def _validate_password(self, key: str, password: str) -> str:
        """Validate the given password value.

        Note:
            This function was updated to support both Python 2.7 and 3.5+. It will now
            explicitly convert the base64 bytes object into a string object.

        Args:
            key (str): The name of the validated column.
            password (str): The password value.

        Raises:
            TypeError: If the given password is None.
            ValueError: If the given password is an empty string.

        Returns:
            str: The mangled password.
        """
        if password is None:
            raise TypeError(f"{self.__class__.__name__}.password cannot be None")

        if password == "":
            raise ValueError(
                f"{self.__class__.__name__}.password cannot be an empty string"
            )

        # mangle the password
        mangled_password_bytes = base64.b64encode(password.encode("utf-8"))
        mangled_password_str = str(mangled_password_bytes.decode("utf-8"))
        return mangled_password_str

    def check_password(self, raw_password: str) -> bool:
        """Check the given raw_password.

        Check the given raw_password with the current User object's mangled password.
        Handles the encryption process behind the scene.

        Note:
            This function was updated to support both Python 2.7 and 3.5+.
            It will now compare the string (str) versions of the given
            raw_password and the current Users object encrypted password.

        Args:
            raw_password (str): The raw password.

        Returns:
            bool: If the given raw password matches the password stored in the db.
        """
        mangled_password_str = str(self.password)
        raw_password_bytes = base64.b64encode(bytes(raw_password.encode("utf-8")))
        raw_password_encrypted_str = str(raw_password_bytes.decode("utf-8"))
        return mangled_password_str == raw_password_encrypted_str

    @validates("groups")
    def _validate_groups(self, key: str, group: Group) -> Group:
        """Validate the given group value.

        Args:
            key (str): The name of the validated column.
            group (Group): The :class:`.Group` instance to be validated.

        Raises:
            TypeError: If the given group arg value is not a :class:`.Group` instance.

        Returns:
            Group: The validated :class:`.Group` instance.
        """
        if not isinstance(group, Group):
            raise TypeError(
                f"Any group in {self.__class__.__name__}.groups should be an instance "
                "of stalker.models.auth.Group, "
                f"not {group.__class__.__name__}: '{group}'"
            )

        return group

    @validates("tasks")
    def _validate_tasks(self, key: str, task: "Task") -> "Task":
        """Validate the given tasks attribute.

        Args:
            key (str): The name of the validated column.
            task (stalker.models.task.Task): The :class:`stalker.models.task.Task`
                instance to be validated.

        Raises:
            TypeError: If the given task arg value is not a
                :class:`stalker.models.task.Task` instance.

        Returns:
            Task: The validated :class:`stalker.models.task.Task` instance.
        """
        from stalker.models.task import Task

        if not isinstance(task, Task):
            raise TypeError(
                f"Any element in {self.__class__.__name__}.tasks should be an instance "
                f"of stalker.models.task.Task, not {task.__class__.__name__}: '{task}'"
            )
        return task

    @validates("watching")
    def _validate_watching(self, key: str, task: "Task") -> "Task":
        """Validate the given watching attribute.

        Args:
            key (str): The name of the validated column.
            task (stalker.models.task.Task): The :class:`stalker.models.task.Task`
                instance that the user will watch.

        Raises:
            TypeError: If the given task arg value is not a
                :class:`stalker.models.task.Task` instance.

        Returns:
            Task: The validated :class:`stalker.models.task.Task` instance.
        """
        from stalker.models.task import Task

        if not isinstance(task, Task):
            raise TypeError(
                f"Any element in {self.__class__.__name__}.watching should be an "
                "instance of stalker.models.task.Task, "
                f"not {task.__class__.__name__}: '{task}'"
            )
        return task

    @validates("vacations")
    def _validate_vacations(self, key: str, vacation: "Vacation") -> "Vacation":
        """Validate the given vacation value.

        Args:
            key (str): The name of the validated column.
            vacation (stalker.models.studio.Vacation): The
                :class:`stalker.models.studio.Vacation` instance.

        Raises:
            TypeError: If the given vacation argument value is not a
                :class:`stalker.models.vacation.Vacation` instance.

        Returns:
            Vacation: The validated vacation value.
        """
        from stalker.models.studio import Vacation

        if not isinstance(vacation, Vacation):
            raise TypeError(
                f"All of the elements in {self.__class__.__name__}.vacations should be "
                "a stalker.models.studio.Vacation instance, "
                f"not {vacation.__class__.__name__}: '{vacation}'"
            )
        return vacation

    @validates("efficiency")
    def _validate_efficiency(
        self, key: str, efficiency: Union[None, int, float]
    ) -> float:
        """Validate the given efficiency value.

        Args:
            key (str): The name of the validated column.
            efficiency (Union[None, int, float]): The efficiency of this User instance.
                This shows how efficient the user works. It is a number between 0-1. If
                None given, a default value of 1.0 will be used.

        Raises:
            TypeError: If the given efficiency is not one of [None, int, float].
            ValueError: If the given efficiency is a negative value.

        Returns:
            float: The validated efficiency value.
        """
        if efficiency is None:
            efficiency = 1.0

        if not isinstance(efficiency, (int, float)):
            raise TypeError(
                f"{self.__class__.__name__}.efficiency should be a float number "
                "greater or equal to 0.0, "
                f"not {efficiency.__class__.__name__}: '{efficiency}'"
            )

        if efficiency < 0:
            raise ValueError(
                f"{self.__class__.__name__}.efficiency should be a float number "
                f"greater or equal to 0.0, not {efficiency}"
            )

        return float(efficiency)

    @validates("rate")
    def _validate_rate(self, key: str, rate: Union[int, float]) -> float:
        """Validate the given rate value.

        Args:
            key (str): The name of the validated column.
            rate (Union[int, float]): An int or float value representing the User hourly
                rate.

        Raises:
            TypeError: If the given rate is not an int or float.
            ValueError: If the given rate is a negative number.

        Returns:
            float: The validated rate value.
        """
        if rate is None:
            rate = 0.0

        if not isinstance(rate, (int, float)):
            raise TypeError(
                f"{self.__class__.__name__}.rate should be a float number greater or "
                f"equal to 0.0, not {rate.__class__.__name__}: '{rate}'"
            )

        if rate < 0:
            raise ValueError(
                f"{self.__class__.__name__}.rate should be a float number greater or "
                f"equal to 0.0, not {rate}"
            )

        return float(rate)

    @property
    def tickets(self) -> List["Ticket"]:
        """Return the list of :class:`.Ticket` s that this user has.

        Returns:
            List[Ticket]: The list of :class:`.Ticket` instances which this user is the
                owner of.
        """
        # do it with sqlalchemy
        from stalker.models.ticket import Ticket

        return Ticket.query.filter(Ticket.owner == self).all()

    @property
    def open_tickets(self) -> List["Ticket"]:
        """Return the list of open :class:`.Ticket` s that this user has.

        Returns:
             List[Ticket]: A list of :class:`.Ticket` instances which are not closed and
                this user is assigned as the owner.
        """
        from stalker import Ticket

        return (
            Ticket.query.join(Status, Ticket.status)
            .filter(Ticket.owner == self)
            .filter(Status.code != "CLS")
            .all()
        )

    @property
    def to_tjp(self) -> str:
        """Return a TaskJuggler compatible str representation of this User instance.

        Returns:
            str: The TaskJuggler compatible representation of this User instance.
        """
        tab = "    "
        indent = tab
        tjp = f'resource {self.tjp_id} "{self.tjp_id}" {{'
        tjp += f"\n{indent}efficiency {self.efficiency}"
        for vacation in self.vacations:
            tjp += "\n"
            tjp += "\n".join(f"{indent}{line}" for line in vacation.to_tjp.split("\n"))
        tjp += "\n}"
        return tjp


class LocalSession(object):
    """A simple temporary session object which simple stores session data.

    This class will later be removed, it is here because we need a login window
    for the Qt user interfaces.

    On initialize it will load the SessionData from the users .strc folder
    """

    def __init__(self) -> None:
        self.logged_in_user_id = None
        self.valid_to = None
        self.session_data = None
        self.load()

    def load(self) -> None:
        """Load the data from the saved local session."""
        try:
            with open(LocalSession.session_file_full_path(), "r") as s:
                # try:
                json_object = json.load(s)
                valid_to = millis_to_datetime(json_object.get("valid_to"))
                if valid_to > datetime.now(pytz.utc):
                    # fill __dict__ with the loaded one
                    self.valid_to = valid_to
                    self.logged_in_user_id = json_object.get("logged_in_user_id")
        except IOError:
            pass

    @property
    def logged_in_user(self) -> "User":
        """Return the logged-in user.

        Returns:
            User: The logged-in user.
        """
        return User.query.filter_by(id=self.logged_in_user_id).first()

    def store_user(self, user: "User") -> None:
        """Store the given user instance.

        Args:
            user (User): The :class:`.User` instance.
        """
        if user:
            self.logged_in_user_id = user.id

    def save(self) -> None:
        """Remember the data in user local file system."""
        self.valid_to = datetime.now(pytz.utc) + timedelta(days=10)
        # serialize self
        dumped_data = json.dumps(
            {
                "valid_to": datetime_to_millis(self.valid_to),
                "logged_in_user_id": self.logged_in_user_id,
            },
        )
        logger.debug(f"dumped session data : {dumped_data}")
        self._write_data(dumped_data)

    def delete(self) -> None:
        """Remove the cache file."""
        try:
            os.remove(self.session_file_full_path())
        except OSError:
            pass

    @classmethod
    def session_file_full_path(cls) -> str:
        """Return the session file full path.

        Returns:
            str: The session file full path.
        """
        return os.path.normpath(
            os.path.join(
                defaults.local_storage_path, defaults.local_session_data_file_name
            )
        )

    def _write_data(self, data: str) -> None:
        """Write the given data to the local session file.

        Args:
            data (str): The data to be written (generally serialized LocalSession class
                itself)
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
            with open(file_full_path, "w") as data_file:
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
    __tablename__ = "Roles"
    __mapper_args__ = {"polymorphic_identity": "Role"}

    role_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )

    def __init__(self, **kwargs) -> None:
        super(Role, self).__init__(**kwargs)


def create_department_user(department: "Department") -> "DepartmentUser":
    """Create DepartmentUser instance on association proxy.

    Args:
        department (stalker.models.department.Department): The
            :class:`stalker.models.department.Department` instance.

    Returns:
        stalker.models.department.DepartmentUser: The
            :class:`stalker.models.department.DepartmentUser` instance.
    """
    from stalker.models.department import DepartmentUser

    return DepartmentUser(department=department)


def create_client_user(client: "Client") -> "ClientUser":
    """Create ClientUser instance on association proxy.

    Args:
        client (stalker.models.client.Client): The
            :class:`stalker.models.project.Project` instance.

    Returns:
        stalker.models.client.ClientUser: The
            :class:`stalker.models.client.ClientUser` instance.
    """
    from stalker.models.client import ClientUser

    return ClientUser(client=client)


def create_project_user(project: "Project") -> "ProjectUser":
    """Create ProjectUser instance on association proxy.

    Args:
        project (stalker.models.project.Project): The
            :class:`stalker.models.project.Project` instance.

    Returns:
        stalker.models.project.ProjectUser: The
            :class:`stalker.models.project.ProjectUser` instance.
    """
    from stalker.models.project import ProjectUser

    return ProjectUser(project=project)


# Group_Users
Group_Users = Table(
    "Group_Users",
    Base.metadata,
    Column("uid", Integer, ForeignKey("Users.id"), primary_key=True),
    Column("gid", Integer, ForeignKey("Groups.id"), primary_key=True),
)


class AuthenticationLog(SimpleEntity):
    """Keeps track of login/logout dates and the action (login or logout)."""

    __auto_name__ = True
    __tablename__ = "AuthenticationLogs"
    __mapper_args__ = {"polymorphic_identity": "AuthenticationLog"}

    log_id: Mapped[int] = mapped_column(
        "id", ForeignKey("SimpleEntities.id"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column("uid", Integer, ForeignKey("Users.id"))
    user: Mapped[User] = relationship(
        primaryjoin="AuthenticationLogs.c.uid==Users.c.id",
        uselist=False,
        back_populates="authentication_logs",
        doc="The :class:`.User` instance that this AuthenticationLog is created for",
    )
    action: Mapped[str] = mapped_column(Enum(LOGIN, LOGOUT, name="ActionNames"))
    date: Mapped[datetime] = mapped_column(GenericDateTime)

    def __init__(self, user=None, date=None, action=LOGIN, **kwargs) -> None:
        super(AuthenticationLog, self).__init__(**kwargs)
        self.user = user
        self.date = date
        self.action = action

    def __lt__(self, other: "AuthenticationLog") -> bool:
        """Make this object order-able.

        Args:
            other (.AuthenticationLog): The other :class:`.AuthenticationLog`
                instance.

        Returns:
            Tuple(str, str): The str key to be used for ordering.
        """
        return self.date < other.date

    @validates("user")
    def __validate_user__(self, key: str, user: "User") -> "User":
        """Validate the given user argument value.

        Args:
            key (str): The name of the validated column.
            user (User): The :class:`.User` instance to be validated.

        Raises:
            TypeError: If the given user args is not a :class:`.User` instance.

        Returns:
            .User: The validated :class:`.User` instance.
        """
        if not isinstance(user, User):
            raise TypeError(
                f"{self.__class__.__name__}.user should be a User instance, "
                f"not {user.__class__.__name__}: '{user}'"
            )

        return user

    @validates("action")
    def __validate_action__(self, key: str, action: str) -> str:
        """Validate the given action argument value.

        Args:
            key (str): The name of the validated column.
            action (str): One of LOGIN or LOGOUT enum values.

        Raises:
            ValueError: If the given value is not one of LOGIN or LOGOUT.

        Returns:
            str: The validated action value.
        """
        if action is None:
            action = copy.copy(LOGIN)

        if action not in [LOGIN, LOGOUT]:
            raise ValueError(
                f'{self.__class__.__name__}.action should be one of "login" or '
                f'"logout", not "{action}"'
            )

        return action

    @validates("date")
    def __validate_date__(self, key: str, date: datetime) -> datetime:
        """Validate the given date value.

        Args:
            key (str): The name of the validated column.
            date (datetime): The datetime instance.

        Raises:
            TypeError: If the given date is not a datetime instance.

        Returns:
            datetime: Returns the validated datetime instance.
        """
        if date is None:
            date = datetime.now(pytz.utc)

        if not isinstance(date, datetime):
            raise TypeError(
                f"{self.__class__.__name__}.date should be a datetime.datetime "
                f"instance, not {date.__class__.__name__}: '{date}'"
            )

        return date
