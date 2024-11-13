# -*- coding: utf-8 -*-
"""Status and StatusList related functions and classes are situated here."""
from typing import Any, Dict, List, Optional, Type, Union

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from stalker.db.declarative import Base
from stalker.db.session import DBSession
from stalker.log import get_logger
from stalker.models.entity import Entity
from stalker.models.mixins import CodeMixin, TargetEntityTypeMixin

logger = get_logger(__name__)


class Status(Entity, CodeMixin):
    """Defines object statutes.

    No extra parameters, use the *code* attribute to give a short name for the
    status.

    A Status object can be compared with a string value and it will return if
    the lower case name or lower case code of the status matches the lower case
    form of the given string::

    .. code-block:: Python

        >>> from stalker import Status
        >>> a_status = Status(name="On Hold", code="OH")
        >>> a_status == "on hold"
        True
        >>> a_status != "complete"
        True
        >>> a_status == "oh"
        True
        >>> a_status == "another status"
        False

    Args:
        name (str): The name long name of this Status.
        code (str): The code of this Status, its generally the short version of
            the name attribute.
    """

    __auto_name__ = False
    __tablename__ = "Statuses"
    __mapper_args__ = {"polymorphic_identity": "Status"}
    status_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    def __init__(
        self,
        name: Optional[str] = None,
        code: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        kwargs["name"] = name
        kwargs["code"] = code

        super(Status, self).__init__(**kwargs)
        self.code = code

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is a Status instance and has the same
                attributes.
        """
        if isinstance(other, str):
            return (
                self.name.lower() == other.lower() or self.code.lower() == other.lower()
            )
        else:
            return super(Status, self).__eq__(other) and isinstance(other, Status)

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Status, self).__hash__()


class StatusList(Entity, TargetEntityTypeMixin):
    """Type specific list of :class:`.Status` instances.

    Holds multiple :class:`.Status` instances to be used as a choice list for several
    other classes.

    A StatusList can only be assigned to only one entity type. So a
    :class:`.Project` can only have one suitable StatusList object which is
    designed for :class:`.Project` entities.

    The list of statuses in StatusList can be accessed by using a list like
    indexing and it also supports string indexes only for getting the item,
    you cannot set an item with string indices:

    .. code-block:: Python

        >>> from stalker import Status, StatusList
        >>> status1 = Status(name="Complete", code="CMPLT")
        >>> status2 = Status(name="Work in Progress", code="WIP")
        >>> status3 = Status(name="Pending Review", code="PRev")
        >>> a_status_list = StatusList(name="Asset Status List",
                                    statuses=[status1, status2, status3],
                                    target_entity_type="Asset")
        >>> a_status_list[0]
        <Status (Complete, CMPLT)>
        >>> a_status_list["complete"]
        <Status (Complete, CMPLT)>
        >>> a_status_list["WIP"]
        <Status (Work in Progress, WIP)>

    Args:
        statuses (List[Status]): This is a list of :class:`.Status` instances,
            so you can prepare different StatusLists for different kind of
            entities using the same pool of :class:`.Status` instances.

        target_entity_type (str): use this parameter to specify the target entity
            type that this StatusList is designed for. It accepts classes or names
            of classes.

        For example:

        .. code-block:: Python

            from stalker import Status, StatusList, Project

            status_list = [
                Status(name="Waiting To Start", code="WTS"),
                Status(name="On Hold", code="OH"),
                Status(name="In Progress", code="WIP"),
                Status(name="Waiting Review", code="WREV"),
                Status(name="Approved", code="APP"),
                Status(name="Completed", code="CMPLT"),
            ]

            project_status_list = StatusList(
                name="Project Status List",
                statuses=status_list,
                target_entity_type="Project"
            )

            # or
            project_status_list = StatusList(
                name="Project Status List",
                statuses=status_list,
                target_entity_type=Project
            )

        now with the code above you cannot assign the ``project_status_list``
        object to any other class than a ``Project`` object.

        The StatusList instance can be empty, means it may not have anything in
        its :attr:`.StatusList.statuses`. But it is useless. The validation for
        empty statuses list is left to the SOM user.
    """

    __auto_name__ = True
    __tablename__ = "StatusLists"
    __mapper_args__ = {"polymorphic_identity": "StatusList"}

    __unique_target__ = True

    status_list_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    statuses: Mapped[Optional[List[Status]]] = relationship(
        secondary="StatusList_Statuses",
        doc="List of :class:`.Status` objects, showing the possible statuses",
    )

    def __init__(
        self,
        statuses: Optional[List[Status]] = None,
        target_entity_type: Optional[Union[Type, str]] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        super(StatusList, self).__init__(**kwargs)
        TargetEntityTypeMixin.__init__(self, target_entity_type, **kwargs)

        if statuses is None:
            statuses = []
        self.statuses = statuses

    @validates("statuses")
    def _validate_statuses(self, key: str, status: Status) -> Status:
        """Validate the given status value.

        Args:
            key (str): The name of the validated column.
            status (Status): The status value to be validated.

        Raises:
            TypeError: If the status value is not a Status instance.

        Returns:
            Status: The validated status value.
        """
        if not isinstance(status, Status):
            raise TypeError(
                f"All of the elements in {self.__class__.__name__}.statuses must be an "
                "instance of stalker.models.status.Status, "
                f"not {status.__class__.__name__}: '{status}'"
            )
        return status

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is a StatusList instance and has the same
                statuses, target_entity_type.
        """
        return (
            super(StatusList, self).__eq__(other)
            and isinstance(other, StatusList)
            and self.statuses == other.statuses
            and self.target_entity_type == other.target_entity_type
        )

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(StatusList, self).__hash__()

    def __getitem__(self, key: int) -> Status:
        """Return the Status at the given key.

        Args:
            key (int): The index to return the value of.

        Returns:
            Status: The Status instance at the given index.
        """
        return_item = None
        with DBSession.no_autoflush:
            if isinstance(key, str):
                for item in self.statuses:
                    if item == key:
                        return_item = item
                        break
            else:
                return_item = self.statuses[key]

        return return_item

    def __setitem__(self, key: int, value: Status) -> None:
        """Set the value at the given index.

        Args:
            key (int): The index to set the item value to.
            value (Status): The Status instance to set at the given index.
        """
        self.statuses[key] = value

    def __delitem__(self, key: int) -> None:
        """Delete the item with the given key.

        Args:
            key (int): Remove the Status at the given index.
        """
        del self.statuses[key]

    def __len__(self) -> int:
        """Return the  number of Statuses in this StatusList.

        Returns:
            int: The number of Statuses in this StatusList.
        """
        return len(self.statuses)


# StatusList_Statuses Table
StatusList_Statuses = Table(
    "StatusList_Statuses",
    Base.metadata,
    Column("status_list_id", Integer, ForeignKey("StatusLists.id"), primary_key=True),
    Column("status_id", Integer, ForeignKey("Statuses.id"), primary_key=True),
)
