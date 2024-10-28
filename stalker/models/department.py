# -*- coding: utf-8 -*-
"""Department related classes and functions are situated here."""

from jinja2 import Template

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, validates

from stalker import defaults
from stalker.db.declarative import Base
from stalker.log import get_logger
from stalker.models.auth import User
from stalker.models.entity import Entity

logger = get_logger(__name__)


class Department(Entity):
    """The departments that forms the studio itself.

    The information that a Department object holds is like:

      * The members of the department
      * and all the other things those are inherited from the AuditEntity class

    Two Department object considered the same if they have the same name, the
    the users list is not important, a "Modeling" department
    should of course be the same with another department which has the name
    "Modeling" again.

    so creating a department object needs the following parameters:

    :param users: it can be an empty list, so one department can be created
      without any member in it. But this parameter should be a list of User
      objects.

    """

    __auto_name__ = False
    __tablename__ = "Departments"
    __mapper_args__ = {"polymorphic_identity": "Department"}
    department_id = Column("id", Integer, ForeignKey("Entities.id"), primary_key=True)

    users = association_proxy(
        "user_role", "user", creator=lambda u: DepartmentUser(user=u)
    )

    user_role = relationship(
        "DepartmentUser",
        back_populates="department",
        cascade="all, delete-orphan",
        primaryjoin="Departments.c.id==Department_Users.c.did",
        doc="""List of users representing the members of this department.""",
    )

    def __init__(self, users=None, **kwargs):
        super(Department, self).__init__(**kwargs)

        if users is None:
            users = []

        # for user in users:
        #     self.user_role.append(
        #         DepartmentUser(department=self, user=user)
        #     )
        self.users = users

    def __eq__(self, other):
        """Check if the other is equal to this one.

        Args:
            other (Department): The other Department instance.

        Returns:
            bool: True if the other object is also a Department and all the attributes
                are equal.
        """
        return super(Department, self).__eq__(other) and isinstance(other, Department)

    def __hash__(self):
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Department, self).__hash__()

    @validates("user_role")
    def _validate_user_role(self, key, user_role):
        """Validate the given user_role value.

        Args:
            key (str): The name of the validated column.
            user_role (DepartmentUser): The user_role value to be validated.

        Returns:
            DepartmentUser: The validated user_role value.
        """
        return user_role

    @property
    def to_tjp(self):
        """Output a TaskJuggler compatible representation.

        This uses the ``defaults.tjp_department_template``.

        Returns:
            str: The TaskJuggler compatible representation.
        """
        temp = Template(defaults.tjp_department_template, trim_blocks=True)
        return temp.render({"department": self})


# DEPARTMENTS_USERS
class DepartmentUser(Base):
    """The association object used in Department-to-User relation."""

    __tablename__ = "Department_Users"

    user_id = Column("uid", Integer, ForeignKey("Users.id"), primary_key=True)

    user = relationship(
        "User",
        back_populates="department_role",
        primaryjoin="DepartmentUser.user_id==User.user_id",
    )

    department_id = Column(
        "did", Integer, ForeignKey("Departments.id"), primary_key=True
    )

    department = relationship(
        "Department",
        back_populates="user_role",
        primaryjoin="DepartmentUser.department_id==Department.department_id",
    )

    role_id = Column("rid", Integer, ForeignKey("Roles.id"), nullable=True)

    role = relationship("Role", primaryjoin="DepartmentUser.role_id==Role.role_id")

    def __init__(self, department=None, user=None, role=None):
        self.department = department
        self.user = user
        self.role = role

    @validates("department")
    def _validate_department(self, key, department):
        """Validate the given department value.

        Args:
            key (str): The name of the validated column.
            department (Department): The department value to be validated.

        Raises:
            TypeError: If the given user value is not a :class:`.Department` instance.

        Returns:
            Department: The validated department value.
        """
        if department is not None:
            # check if it is instance of Department object
            if not isinstance(department, Department):
                raise TypeError(
                    "%s.department should be a "
                    "stalker.models.department.Department instance, not %s"
                    % (self.__class__.__name__, department.__class__.__name__)
                )
        return department

    @validates("user")
    def _validate_user(self, key, user):
        """Validate the given user value.

        Args:
            key (str): The name of the validated column.
            user (User): The user value to be validated.

        Raises:
            TypeError: If the given user value is not a
                :class:`stalker.models.auth.User` instance.

        Returns:
            User: The validated user value.
        """
        if user is not None:
            if not isinstance(user, User):
                raise TypeError(
                    "%s.user should be a stalker.models.auth.User instance, "
                    "not %s" % (self.__class__.__name__, user.__class__.__name__)
                )
        return user

    @validates("role")
    def _validate_role(self, key, role):
        """Validate the given role instance.

        Args:
            key (str): The name of the validated column.
            role (Role): The role value to be validated.

        Raises:
            TypeError: If the given role value is not a
                :class:`stalker.models.auth.Role` instance.

        Returns:
            Role: The validated role value.
        """
        if role is not None:
            from stalker import Role

            if not isinstance(role, Role):
                raise TypeError(
                    "%s.role should be a "
                    "stalker.models.auth.Role instance, not %s"
                    % (self.__class__.__name__, role.__class__.__name__)
                )
        return role
