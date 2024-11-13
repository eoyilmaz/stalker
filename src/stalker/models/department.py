# -*- coding: utf-8 -*-
"""Department related classes and functions are situated here."""

from typing import Any, Dict, List, Optional, Union

from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from stalker.db.declarative import Base
from stalker.log import get_logger
from stalker.models.auth import Role, User
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

    Args:
        users (List[User]): it can be an empty list, so one department can be
            created without any member in it. But this parameter should be a list
            of User objects.
    """

    __auto_name__ = False
    __tablename__ = "Departments"
    __mapper_args__ = {"polymorphic_identity": "Department"}
    department_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )

    users = association_proxy(
        "user_role", "user", creator=lambda u: DepartmentUser(user=u)
    )

    user_role: Mapped[Optional[List["DepartmentUser"]]] = relationship(
        back_populates="department",
        cascade="all, delete-orphan",
        primaryjoin="Departments.c.id==Department_Users.c.did",
        doc="""List of users representing the members of this department.""",
    )

    def __init__(
        self, users: Optional[List[User]] = None, **kwargs: Optional[Dict[str, Any]]
    ) -> None:
        super(Department, self).__init__(**kwargs)

        if users is None:
            users = []

        self.users = users

    def __eq__(self, other: Any) -> bool:
        """Check if the other is equal to this one.

        Args:
            other (Any): The other Department instance.

        Returns:
            bool: True if the other object is also a Department and all the attributes
                are equal.
        """
        return super(Department, self).__eq__(other) and isinstance(other, Department)

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Department, self).__hash__()

    @validates("user_role")
    def _validate_user_role(
        self, key: str, user_role: "DepartmentUser"
    ) -> "DepartmentUser":
        """Validate the given user_role value.

        Args:
            key (str): The name of the validated column.
            user_role (DepartmentUser): The user_role value to be validated.

        Returns:
            DepartmentUser: The validated user_role value.
        """
        return user_role

    @property
    def to_tjp(self) -> str:
        """Output a TaskJuggler compatible representation.

        Returns:
            str: The TaskJuggler compatible representation.
        """
        tab = "    "
        indent = tab
        tjp = f'resource {self.tjp_id} "{self.tjp_id}" {{'
        for resource in self.users:
            tjp += "\n"
            tjp += "\n".join(f"{indent}{line}" for line in resource.to_tjp.split("\n"))
        tjp += "\n}"
        return tjp


# DEPARTMENTS_USERS
class DepartmentUser(Base):
    """The association object used in Department-to-User relation."""

    __tablename__ = "Department_Users"

    user_id: Mapped[int] = mapped_column(
        "uid", ForeignKey("Users.id"), primary_key=True
    )
    user: Mapped["User"] = relationship(
        back_populates="department_role",
        primaryjoin="DepartmentUser.user_id==User.user_id",
        uselist=False,
    )
    department_id: Mapped[int] = mapped_column(
        "did", ForeignKey("Departments.id"), primary_key=True
    )
    department: Mapped[Department] = relationship(
        back_populates="user_role",
        primaryjoin="DepartmentUser.department_id==Department.department_id",
        uselist=False,
    )
    role_id: Mapped[Optional[int]] = mapped_column("rid", ForeignKey("Roles.id"))
    role: Mapped[Role] = relationship(
        primaryjoin="DepartmentUser.role_id==Role.role_id"
    )

    def __init__(self, department=None, user=None, role=None):
        self.department = department
        self.user = user
        self.role = role

    @validates("department")
    def _validate_department(
        self, key: str, department: Union[None, Department]
    ) -> Union[None, Department]:
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
                    f"{self.__class__.__name__}.department should be a "
                    "stalker.models.department.Department instance, "
                    f"not {department.__class__.__name__}: '{department}'"
                )
        return department

    @validates("user")
    def _validate_user(
        self, key: str, user: Union[None, "User"]
    ) -> Union[None, "User"]:
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
                    f"{self.__class__.__name__}.user should be a "
                    "stalker.models.auth.User instance, "
                    f"not {user.__class__.__name__}: '{user}'"
                )
        return user

    @validates("role")
    def _validate_role(self, key: str, role: Union[None, Role]) -> Union[None, Role]:
        """Validate the given role instance.

        Args:
            key (str): The name of the validated column.
            role (Union[None, Role]): The role value to be validated.

        Raises:
            TypeError: If the given role value is not a
                :class:`stalker.models.auth.Role` instance.

        Returns:
            Union[None, Role]: The validated role value.
        """
        if role is not None:
            if not isinstance(role, Role):
                raise TypeError(
                    f"{self.__class__.__name__}.role should be a "
                    "stalker.models.auth.Role instance, "
                    f"not {role.__class__.__name__}: '{role}'"
                )
        return role
