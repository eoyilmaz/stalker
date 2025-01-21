# -*- coding: utf-8 -*-
"""Mixins are situated here."""

import datetime
from typing import (
    Any,
    Dict,
    Generator,
    List,
    Optional,
    TYPE_CHECKING,
    Tuple,
    Type,
    Union,
)
from typing_extensions import Self

import pytz

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    Interval,
    String,
    Table,
)
from sqlalchemy.exc import OperationalError, UnboundExecutionError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (
    Mapped,
    backref,
    mapped_column,
    relationship,
    synonym,
    validates,
)

from stalker import defaults
from stalker.db.declarative import Base
from stalker.db.session import DBSession
from stalker.db.types import GenericDateTime
from stalker.log import get_logger
from stalker.models.enum import (
    ScheduleConstraint,
    ScheduleConstraintDecorator,
    ScheduleModel,
    ScheduleModelDecorator,
    TimeUnit,
    TimeUnitDecorator,
    TraversalDirection,
)
from stalker.utils import check_circular_dependency, make_plural, walk_hierarchy


if TYPE_CHECKING:  # pragma: no cover
    from stalker.models.auth import Permission
    from stalker.models.project import Project
    from stalker.models.status import Status, StatusList
    from stalker.models.file import File
    from stalker.models.studio import WorkingHours


logger = get_logger(__name__)


def create_secondary_table(
    primary_cls_name: str,
    secondary_cls_name: str,
    primary_cls_table_name: str,
    secondary_cls_table_name: str,
    secondary_table_name: Optional[str] = None,
) -> Table:
    """Create any secondary table.

    Args:
        primary_cls_name (str): The primary class name.
        secondary_cls_name (str): The secondary class name.
        primary_cls_table_name (str): The primary class table name.
        secondary_cls_table_name (str): The secondary class table name.
        secondary_table_name (Union[None, str]): Optional secondary table name.

    Raises:
        TypeError: If primary_cls_name is not a str.
        TypeError: If secondary_cls_name is not a str.
        TypeError: If primary_cls_table_name is not a str.
        TypeError: If secondary_cls_table_name is not a str.
        TypeError: If secondary_table_name is not a str.
        ValueError: If primary_cls_name is an empty str.
        ValueError: If secondary_cls_name is an empty str.
        ValueError: If primary_cls_table_name is an empty str.
        ValueError: If secondary_cls_table_name is an empty str.
        ValueError: If secondary_table_name is an empty str.

    Returns:
        Table: The secondary table.
    """
    # validate data
    # primary_cls_name
    if not isinstance(primary_cls_name, str):
        raise TypeError(
            "primary_cls_name should be a str containing the primary class name, "
            f"not {primary_cls_name.__class__.__name__}: '{primary_cls_name}'"
        )

    if primary_cls_name == "":
        raise ValueError(
            "primary_cls_name should be a str containing the primary class name, "
            f"not: '{primary_cls_name}'"
        )

    # secondary_cls_name
    if not isinstance(secondary_cls_name, str):
        raise TypeError(
            "secondary_cls_name should be a str containing the secondary class name, "
            f"not {secondary_cls_name.__class__.__name__}: '{secondary_cls_name}'"
        )

    if secondary_cls_name == "":
        raise ValueError(
            "secondary_cls_name should be a str containing the secondary class name, "
            f"not: '{secondary_cls_name}'"
        )

    # primary_cls_table_name
    if not isinstance(primary_cls_table_name, str):
        raise TypeError(
            "primary_cls_table_name should be a str containing the primary class "
            f"table name, not {primary_cls_table_name.__class__.__name__}: "
            f"'{primary_cls_table_name}'"
        )

    if primary_cls_table_name == "":
        raise ValueError(
            "primary_cls_table_name should be a str containing the primary class "
            f"table name, not: '{primary_cls_table_name}'"
        )

    # secondary_cls_table_name
    if not isinstance(secondary_cls_table_name, str):
        raise TypeError(
            "secondary_cls_table_name should be a str containing the secondary class "
            f"table name, not {secondary_cls_table_name.__class__.__name__}: "
            f"'{secondary_cls_table_name}'"
        )

    if secondary_cls_table_name == "":
        raise ValueError(
            "secondary_cls_table_name should be a str containing the secondary class "
            f"table name, not: '{secondary_cls_table_name}'"
        )

    # secondary_table_name
    if secondary_table_name is not None and not isinstance(secondary_table_name, str):
        raise TypeError(
            "secondary_table_name should be a str containing the secondary table "
            "name, or it can be None or an empty string to let Stalker to auto "
            f"generate one, not {secondary_table_name.__class__.__name__}: "
            f"'{secondary_table_name}'"
        )

    plural_secondary_cls_name = make_plural(secondary_cls_name)

    # use the given class_name and the class_table
    if not secondary_table_name:
        secondary_table_name = f"{primary_cls_name}_{plural_secondary_cls_name}"

    # check if the table is already defined
    if secondary_table_name not in Base.metadata:
        secondary_table = Table(
            secondary_table_name,
            Base.metadata,
            Column(
                f"{primary_cls_name.lower()}_id",
                Integer,
                ForeignKey(f"{primary_cls_table_name}.id"),
                primary_key=True,
            ),
            Column(
                f"{secondary_cls_name.lower()}_id",
                Integer,
                ForeignKey(f"{secondary_cls_table_name}.id"),
                primary_key=True,
            ),
        )
    else:
        secondary_table = Base.metadata.tables[secondary_table_name]

    return secondary_table


class TargetEntityTypeMixin(object):
    """Adds target_entity_type attribute to mixed in class.

    Args:
        target_entity_type (Union[str, type]): The target entity type which this class
            is designed for. Should be a class or a class name.

        For example::

            from stalker import SimpleEntity, TargetEntityTypeMixin, Project

            class A(SimpleEntity, TargetEntityTypeMixin):
                __tablename__ = "As"
                __mapper_args__ = {"polymorphic_identity": "A"}

                def __init__(self, **kwargs):
                    super(A, self).__init__(**kwargs)
                    TargetEntityTypeMixin.__init__(self, **kwargs)

            a_obj = A(target_entity_type=Project)

        The ``a_obj`` will only be accepted by :class:`.Project` instances. You cannot
        assign it to any other class which accepts a :class:`.Type` instance.

        To control the mixed-in class behavior add these class variables to the
        mixed in class:

            __nullable_target__ : controls if the target_entity_type can be
                nullable or not. Default is False.

            __unique_target__ : controls if the target_entity_type should be unique, so
                there is only one object for one type. Default is False.
    """

    __nullable_target__ = False
    __unique_target__ = False

    @declared_attr
    def _target_entity_type(cls) -> Mapped[str]:
        """Create the _target_entity_type attribute as a declared attribute.

        Returns:
            Column: The Column related to the _target_entity_type attribute.
        """
        return mapped_column(
            "target_entity_type",
            String(128),
            nullable=cls.__nullable_target__,
            unique=cls.__unique_target__,
        )

    def __init__(self, target_entity_type: Optional[str] = None, **kwargs) -> None:
        self._target_entity_type = self._validate_target_entity_type(target_entity_type)

    def _validate_target_entity_type(self, target_entity_type: Union[str, Type]) -> str:
        """Validate the given target_entity_type value.

        Args:
            target_entity_type (Union[str, type]): The target_entity_type that this
                entity is valid for.

        Raises:
            TypeError: If the given target_entity_type value is None.
            ValueError: If the given target_entity_type value is an empty str.

        Returns:
            str: The validated target_entity_type value.
        """
        # it cannot be None
        if target_entity_type is None:
            raise TypeError(
                f"{self.__class__.__name__}.target_entity_type cannot be None"
            )

        # check if it is a class
        if isinstance(target_entity_type, type):
            target_entity_type = target_entity_type.__name__

        if target_entity_type == "":
            raise ValueError(
                f"{self.__class__.__name__}.target_entity_type cannot be empty"
            )

        return target_entity_type

    def _target_entity_type_getter(self) -> str:
        """Return the _target_entity_type attribute value.

        Returns:
            str: The _target_entity_type attribute value.
        """
        return self._target_entity_type

    @declared_attr
    def target_entity_type(cls) -> Mapped[str]:
        """Create the target_entity_type attribute as a declared attribute.

        Returns:
            SynonymProperty: The target_entity_type property.
        """
        return synonym(
            "_target_entity_type",
            descriptor=property(
                fget=cls._target_entity_type_getter,
                doc="""The entity type which this object is valid for.

                Usually it is set to the TargetClass directly.
                """,
            ),
        )


class StatusMixin(object):
    """Makes the mixed in object statusable.

    This mixin adds status and status_list attributes to the mixed in class.
    Any object that needs a status and a corresponding status list can include
    this mixin.

    When mixed with a class which don't have an __init__ method, the mixin
    supplies one, and in this case the parameters below must be defined.

    Args:
        status_list (StatusList): this attribute holds a status list object, which
            shows the possible statuses that this entity could be in. This attribute
            cannot be empty or None. Giving a StatusList object, the
            StatusList.target_entity_type should match the current class.

            .. versionadded:: 0.1.2.a4

                The status_list argument now can be skipped or can be None if there
                is an active database connection and there is a suitable
                :class:`.StatusList` instance in the database whom
                :attr:`.StatusList.target_entity_type` attribute is set to the
                current mixed-in class name.

        status (Status): It is a :class:`.Status` instance which shows the current
            status of the statusable object. Integer values are also accepted,
            which shows the index of the desired status in the ``status_list``
            attribute of the current statusable object. If a :class:`.Status`
            instance is supplied, it should also be present in the ``status_list``
            attribute. If set to None then the first :class:`.Status` instance
            in the ``status_list`` will be used.

            .. versionadded:: 0.2.0

                Status attribute as Status instance:

                It is now possible to set the status of the instance by a
                :class:`.Status` instance directly. And the :attr:`.StatusMixin.status`
                will return a proper :class:`.Status` instance.
    """

    def __init__(
        self,
        status: Union[None, "Status"] = None,
        status_list: Union[None, "StatusList"] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        self.status_list = status_list
        self.status = status

    @declared_attr
    def status_id(cls) -> Mapped[int]:
        """Create the status_id attribute as a declared attribute.

        Returns:
            Column: The Column related to the status_id attribute.
        """
        return mapped_column(
            "status_id",
            ForeignKey("Statuses.id"),
            nullable=False,
            # This is set to nullable=True but it is impossible to set the
            # status to None by using this Declarative approach.
            #
            # This is done in that way cause SQLAlchemy was flushing the data
            # (AutoFlush) preliminarily while checking if the given Status was
            # in the related StatusList, and it was complaining about the
            # status cannot be null
        )

    @declared_attr
    def status(cls) -> Mapped["Status"]:
        """Create the status attribute as a declared attribute.

        Returns:
            relationship: The relationship object related to the status attribute.
        """
        return relationship(
            "Status",
            primaryjoin=f"{cls.__name__}.status_id==Status.status_id",
            doc="""The current status of the object.

            It is a :class:`.Status` instance which
            is one of the Statuses stored in the ``status_list`` attribute
            of this object.
            """,
        )

    @declared_attr
    def status_list_id(cls) -> Mapped[int]:
        """Create the status_list_id attribute as a declared attribute.

        Returns:
            Column: The Column related to the status_list_id attribute.
        """
        return mapped_column(
            "status_list_id", ForeignKey("StatusLists.id"), nullable=False
        )

    @declared_attr
    def status_list(cls) -> Mapped["StatusList"]:
        """Create the status_list attribute as a declared attribute.

        Returns:
            relationship: The relationship object related to the status_list attribute.
        """
        return relationship(
            "StatusList",
            primaryjoin=f"{cls.__name__}.status_list_id==StatusList.status_list_id",
        )

    @validates("status_list")
    def _validate_status_list(
        self, key: str, status_list: Union[None, "StatusList"]
    ) -> "StatusList":
        """Validate the given status_list value.

        Args:
            key (str): The name of the validated column.
            status_list (Union[None, StatusList]): The status_list value to be
                validated.

        Raises:
            TypeError: If the given status_list value is not a StatusList instance.

        Returns:
            StatusList: The validated status_list value.
        """
        from stalker.models.status import StatusList

        super_names = [mro.__name__ for mro in self.__class__.__mro__]

        if status_list is None:
            # check if there is a db setup and try to get the appropriate
            # StatusList from the database

            # disable autoflush to prevent premature class initialization
            with DBSession.no_autoflush:
                try:
                    # try to get a StatusList with the target_entity_type is
                    # matching the class name
                    status_list = StatusList.query.filter(
                        StatusList.target_entity_type.in_(super_names)
                    ).first()
                except (UnboundExecutionError, OperationalError):
                    # it is not mapped just skip it
                    pass

        # if it is still None
        if status_list is None:
            # there is no db so raise an error because there is no way
            # to get an appropriate StatusList
            raise TypeError(
                f"{self.__class__.__name__} instances cannot be initialized without a "
                "stalker.models.status.StatusList instance, please pass a "
                "suitable StatusList "
                f"(StatusList.target_entity_type={self.__class__.__name__}) with the "
                "'status_list' argument"
            )
        else:
            # it is not an instance of status_list
            if not isinstance(status_list, StatusList):
                raise TypeError(
                    f"{self.__class__.__name__}.status_list should be an instance of "
                    "stalker.models.status.StatusList, "
                    f"not {status_list.__class__.__name__}: '{status_list}'"
                )

            # check if the entity_type matches to the
            # StatusList.target_entity_type
            if status_list.target_entity_type not in super_names:
                raise TypeError(
                    "The given StatusLists' target_entity_type is "
                    f"{status_list.target_entity_type}, "
                    "whereas the entity_type of this object is "
                    f"{self.__class__.__name__}"
                )

        return status_list

    @validates("status")
    def _validate_status(self, key: str, status: "Status") -> "Status":
        """Validate the given status value.

        Args:
            key (str): The name of the validated column.
            status (Status): The status value to be validated.

        Raises:
            TypeError: If the given status value is not a Status instance or an int.
            ValueError: If the status is a negative int value or the given int value
                is equal or bigger than the length of the `StatusList.statuses` or if
                the given Status instance is not in the `StatusList.statuses` list.

        Returns:
            Status: The validated status value.
        """
        from stalker.models.status import Status

        # it is set to None
        if status is None:
            with DBSession.no_autoflush:
                status = self.status_list.statuses[0]

        # it is not an instance of status or int
        if not isinstance(status, (Status, int)):
            raise TypeError(
                f"{self.__class__.__name__}.status must be an instance of "
                "stalker.models.status.Status or an integer showing the index of the "
                f"Status object in the {self.__class__.__name__}.status_list, "
                f"not {status.__class__.__name__}: '{status}'"
            )

        if isinstance(status, int):
            # if it is not in the correct range:
            if status < 0:
                raise ValueError(
                    f"{self.__class__.__name__}.status must be a non-negative integer"
                )

            if status >= len(self.status_list.statuses):
                raise ValueError(
                    f"{self.__class__.__name__}.status cannot be bigger than the "
                    "length of the status_list"
                )
                # get the status instance out of the status_list instance
            status = self.status_list[status]

        # check if the given status is in the status_list
        if status not in self.status_list:
            raise ValueError(
                f"The given Status instance for {self.__class__.__name__}.status is "
                f"not in the {self.__class__.__name__}.status_list, please supply a "
                "status from that list."
            )

        return status


class DateRangeMixin(object):
    """Adds date range info to the mixed in class.

    Adds date range information like ``start``, ``end`` and ``duration``. These
    attributes will be used in TaskJuggler. Because ``effort`` is only
    meaningful if there are some ``resources`` this attribute has been left
    special for :class:`.Task` class. The ``length`` has not been implemented
    because of its rare use.

    The preceding order for the attributes is as follows::

      start > end > duration

    So if all of the parameters are given only the ``start`` and the ``end``
    will be used and the ``duration`` will be calculated accordingly. In any
    other conditions the missing parameter will be calculated from the
    following table:

    +-------+-----+----------+----------------------------------------+
    | start | end | duration | DEFAULTS                               |
    +=======+=====+==========+========================================+
    |       |     |          | start = datetime.datetime.now(pytz.utc)|
    |       |     |          |                                        |
    |       |     |          | duration = datetime.timedelta(days=10) |
    |       |     |          |                                        |
    |       |     |          | end = start + duration                 |
    +-------+-----+----------+----------------------------------------+
    |   X   |     |          | duration = datetime.timedelta(days=10) |
    |       |     |          |                                        |
    |       |     |          | end = start + duration                 |
    +-------+-----+----------+----------------------------------------+
    |   X   |  X  |          | duration = end - start                 |
    +-------+-----+----------+----------------------------------------+
    |   X   |     |    X     | end = start + duration                 |
    +-------+-----+----------+----------------------------------------+
    |   X   |  X  |    X     | duration = end - start                 |
    +-------+-----+----------+----------------------------------------+
    |       |  X  |    X     | start = end - duration                 |
    +-------+-----+----------+----------------------------------------+
    |       |  X  |          | duration = datetime.timedelta(days=10) |
    |       |     |          |                                        |
    |       |     |          | start = end - duration                 |
    +-------+-----+----------+----------------------------------------+
    |       |     |    X     | start = datetime.datetime.now(pytz.utc)|
    |       |     |          |                                        |
    |       |     |          | end = start + duration                 |
    +-------+-----+----------+----------------------------------------+

    Only the ``start``, ``end`` will be stored. The ``duration`` attribute is
    the direct difference of the the ``start`` and ``end`` attributes, so there
    is no need to store it. But if will be used in calculation of the start and
    end values.

    The start and end attributes have a ``computed`` companion. Which are the
    return values from TaskJuggler. so for ``start`` there is the
    ``computed_start`` and for ``end`` there is the ``computed_end``
    attributes.

    The date attributes can be managed with timezones. Follow the Python idioms
    shown in the `documentation of datetime`_

    .. _documentation of datetime: https://docs.python.org/library/datetime.html

    Args:
        start (datetime.datetime): the start date of the entity, should be a
            datetime.datetime instance, the start is the pin point for the date
            calculation. In any condition if the start is available then the value
            will be preserved. If start passes the end the end is also changed
            to a date to keep the timedelta between dates. The default value is
            datetime.datetime.now(pytz.utc)

        end (datetime.datetime): the end of the entity, should be a datetime.datetime
            instance, when the start is changed to a date passing the end, then
            the end is also changed to a later date so the timedelta between the
            dates is kept.

        duration (datetime.timedelta): The duration of the entity. It is a
            :class:`datetime.timedelta` instance. The default value is read from
            he :class:`.Config` class. See the table above for the initialization
            rules.
    """

    def __init__(
        self,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        duration: Optional[datetime.timedelta] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        self._start, self._end, self._duration = self._validate_dates(
            start, end, duration
        )

    @declared_attr
    def _end(cls) -> Mapped[Optional[datetime.datetime]]:
        return mapped_column("end", GenericDateTime)

    def _end_getter(self) -> datetime.datetime:
        """Return the date that the entity should be delivered.

        The end can be set to a datetime.timedelta and in this case it will be
        calculated as an offset from the start and converted to datetime.datetime again.
        Setting the start to a date passing the end will also set the end, so the
        timedelta between them is preserved, default value is 10 days.

        Returns:
            datetime.datetime: The end datetime.
        """
        with DBSession.no_autoflush:
            return self._end

    def _end_setter(self, end: datetime.datetime) -> None:
        """Set the end attribute value.

        Args:
            end (datetime.datetime): The end datetime value.
        """
        self._start, self._end, self._duration = self._validate_dates(
            self.start, end, self.duration
        )

    @declared_attr
    def end(cls) -> Mapped[Optional[datetime.datetime]]:
        """Create the end attribute as a declared attribute.

        Returns:
            SynonymProperty: The end property.
        """
        return synonym("_end", descriptor=property(cls._end_getter, cls._end_setter))

    @declared_attr
    def _start(cls) -> Mapped[Optional[datetime.datetime]]:
        """Create the start attribute as a declared attribute.

        Returns:
            Column: The Column related to the start attribute.
        """
        return mapped_column("start", GenericDateTime)

    def _start_getter(self) -> datetime.datetime:
        """Return the date that this entity should start.

        Also effects the :attr:`.DateRangeMixin.end` attribute value in certain
        conditions, if the :attr:`.DateRangeMixin.start` is set to a time passing the
        :attr:`.DateRangeMixin.end` it will also offset the :attr:`.DateRangeMixin.end`
        to keep the :attr:`.DateRangeMixin.duration` value fixed.
        :attr:`.DateRangeMixin.start` should be an instance of class:`datetime.datetime`
        and the default value is :func:`datetime.datetime.now(pytz.utc)`.

        Returns:
            datetime.datetime: The start datetime value.
        """
        with DBSession.no_autoflush:
            return self._start

    def _start_setter(self, start: datetime.datetime) -> None:
        """Set the start attribute.

        Args:
            start (datetime.datetime): The start date and time.
        """
        self._start, self._end, self._duration = self._validate_dates(
            start, self.end, self.duration
        )

    @declared_attr
    def start(cls) -> Mapped[Optional[datetime.datetime]]:
        """Create the start attribute as a declared attribute.

        Returns:
            SynonymProperty: The start property.
        """
        return synonym(
            "_start",
            descriptor=property(
                cls._start_getter,
                cls._start_setter,
            ),
        )

    @declared_attr
    def _duration(cls) -> Mapped[Optional[datetime.timedelta]]:
        """Create the duration attribute as a declared attribute.

        Returns:
            Column: The Column related to the duration attribute.
        """
        return mapped_column("duration", Interval)

    def _duration_getter(self) -> datetime.timedelta:
        """Return the duration value.

        Returns:
            datetime.timedelta: The duration value.
        """
        with DBSession.no_autoflush:
            return self._duration

    def _duration_setter(self, duration: datetime.timedelta) -> None:
        """Set the duration value.

        Args:
            duration (datetime.timedelta): The duration value.
        """
        if duration is not None:
            if isinstance(duration, datetime.timedelta):
                # set the end to None
                # to make it recalculated
                self._start, self._end, self._duration = self._validate_dates(
                    self.start, None, duration
                )
            else:
                # use the end
                self._start, self._end, self._duration = self._validate_dates(
                    self.start, self.end, duration
                )
        else:
            self._start, self._end, self._duration = self._validate_dates(
                self.start, self.end, duration
            )

    @declared_attr
    def duration(self) -> Mapped[Optional[datetime.timedelta]]:
        """Return the duration attr as a synonym.

        Returns:
            SynonymProperty: The duration property.
        """
        return synonym(
            "_duration",
            descriptor=property(
                self._duration_getter,
                self._duration_setter,
                doc="""Duration of the entity.

                It is a datetime.timedelta instance. Showing the difference of
                the :attr:`.start` and the :attr:`.end`. If edited it changes
                the :attr:`.end` attribute value.""",
            ),
        )

    def _validate_dates(
        self,
        start: datetime.datetime,
        end: datetime.datetime,
        duration: datetime.timedelta,
    ) -> Tuple[datetime.datetime, datetime.datetime, datetime.timedelta]:  # noqa: C901
        """Update the date values.

        Args:
            start (datetime.datetime): The start datetime value.
            end (datetime.datetime): The end datetime value.
            duration (datetime.timedelta): The duration value.

        Returns:
            Tuple(datetime.datetime, datetime.datetime, datetime.timedelta): The
                validated and calculated start, end dates and duration value.
        """
        # logger.debug(f"start    : {start}")
        # logger.debug(f"end      : {end}")
        # logger.debug(f"duration : {duration}")
        if not isinstance(start, datetime.datetime):
            start = None

        if not isinstance(end, datetime.datetime):
            end = None

        if not isinstance(duration, datetime.timedelta):
            duration = None

        # check start
        if start is None:
            # try to calculate the start from end and duration
            if end is None:
                # set the defaults
                start = datetime.datetime.now(pytz.utc)

                if duration is None:
                    # set the defaults
                    duration = defaults.timing_resolution

                end = start + duration
            else:
                if duration is None:
                    duration = defaults.timing_resolution

                # try:
                start = end - duration
                # except OverflowError: # end is datetime.datetime.min
                #     start = end

        # check end
        if end is None:
            if duration is None:
                duration = defaults.timing_resolution

            end = start + duration

        if end < start:
            # check duration
            if duration is None or duration < datetime.timedelta(1):
                duration = datetime.timedelta(1)

            # try:
            end = start + duration
            # except OverflowError: # start is datetime.datetime.max
            #     end = start

        # round the dates to the timing_resolution
        rounded_start = self.round_time(start)
        rounded_end = self.round_time(end)
        rounded_duration = rounded_end - rounded_start

        if rounded_duration < defaults.timing_resolution:
            rounded_duration = defaults.timing_resolution
            rounded_end = rounded_start + rounded_duration

        return rounded_start, rounded_end, rounded_duration

    @declared_attr
    def computed_start(cls) -> Mapped[Optional[datetime.datetime]]:
        """Create the computed_start attribute as a declared attribute.

        Returns:
            Column: The Column related to the computed_start attribute.
        """
        return mapped_column("computed_start", GenericDateTime)

    @declared_attr
    def computed_end(cls) -> Mapped[Optional[datetime.datetime]]:
        """Create the computed_end attribute as a declared attribute.

        Returns:
            Column: The Column related to the computed_end attribute.
        """
        return mapped_column("computed_end", GenericDateTime)

    @property
    def computed_duration(self) -> datetime.timedelta:
        """Calculate the computed duration.

        The computed_duration is calculated as the difference of computed_start and
        computed_end if there are computed_start and computed_end otherwise returns
        None.

        Returns:
            Union[None, datetime.timedelta]: None if one of computed_start or
                computed_end value is None else the difference as datetime.timedelta
                instance.
        """
        return (
            self.computed_end - self.computed_start
            if self.computed_end and self.computed_start
            else None
        )

    @classmethod
    def round_time(cls, dt: datetime.datetime) -> datetime.datetime:
        """Round the given datetime object to the defaults.timing_resolution.

        Use the  :class:`stalker.defaults.timing_resolution` as the closest number of
        seconds to round to.

        Based on Thierry Husson's answer in `Stackoverflow`_

        _`Stackoverflow` : https://stackoverflow.com/a/10854034/1431079

        Args:
            dt (datetime.datetime): The datetime object, defaults to now.

        Returns:
            datetime.datetime: The rounded datetime.datetime instance.
        """
        # to be compatible with python 2.6 use the following instead of
        # total_seconds()
        timing_resolution = defaults.timing_resolution
        trs = timing_resolution.days * 86400 + timing_resolution.seconds

        # convert to seconds
        epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)

        diff = dt - epoch
        diff_in_seconds = diff.days * 86400 + diff.seconds
        return epoch + datetime.timedelta(
            seconds=(diff_in_seconds + trs * 0.5) // trs * trs
        )

    @property
    def total_seconds(self) -> float:
        """Return the duration as seconds.

        Returns:
            float: The calculated total seconds value.
        """
        return self.duration.days * 86400 + self.duration.seconds

    @property
    def computed_total_seconds(self) -> float:
        """Return the computed_total_seconds as seconds.

        Returns:
            float: The computed_total_seconds value.
        """
        return self.computed_duration.days * 86400 + self.computed_duration.seconds


class ProjectMixin(object):
    """Allows connecting a :class:`.Project` to the mixed in object.

    This also forces a ``all, delete-orphan`` cascade, so when a :class:``.Project``
    instance is deleted then all the class instances that are inherited from
    ``ProjectMixin`` will also be deleted. Meaning that, a class which also derives from
    ``ProjectMixin`` will not be able to exists without a project (``delete-orphan``
    case).

    Args:
        project (Project): A :class:`.Project` instance holding the project which this
            object is related to. It cannot be None, or anything other than a
            :class:`.Project` instance.
    """

    #    # add this lines for Sphinx
    #    __tablename__ = "ProjectMixins"

    @declared_attr
    def project_id(cls) -> Mapped[Optional[int]]:
        """Create the project_id attribute as a declared attribute.

        Returns:
            Column: The Column related to the project_id attribute.
        """
        return mapped_column(
            "project_id",
            Integer,
            ForeignKey("Projects.id"),
            # cannot use nullable cause a Project object needs
            # insert itself as the project and it needs post_update
            # thus nullable should be True
        )

    @declared_attr
    def project(cls) -> Mapped[Optional["Project"]]:
        """Create the project attribute as a declared attribute.

        Returns:
            relationship: The relationship object related to the project attribute.
        """
        backref_table_name = cls.__tablename__.lower()
        doc = """The :class:`.Project` instance that this object belongs to."""

        return relationship(
            "Project",
            primaryjoin=f"{cls.__tablename__}.c.project_id==Projects.c.id",
            post_update=True,  # for project itself
            uselist=False,
            backref=backref(backref_table_name, cascade="all, delete-orphan"),
            doc=doc,
        )

    def __init__(
        self, project: Optional["Project"] = None, **kwargs: Dict[str, Any]
    ) -> None:
        self.project = project

    @validates("project")
    def _validate_project(self, key: str, project: "Project") -> "Project":
        """Validate the given project value.

        Args:
            key (str): The name of the validated column.
            project (Project): The project value to be validated.

        Raises:
            TypeError: If the project is None or not a Project instance.

        Returns:
            Project: The validated project value.
        """
        from stalker.models.project import Project

        if project is None:
            raise TypeError(
                f"{self.__class__.__name__}.project cannot be None it must be an "
                "instance of stalker.models.project.Project"
            )

        if not isinstance(project, Project):
            raise TypeError(
                f"{self.__class__.__name__}.project should be an instance of "
                "stalker.models.project.Project instance, "
                f"not {project.__class__.__name__}: '{project}'"
            )
        return project


class ReferenceMixin(object):
    """Adds reference capabilities to the mixed in class.

    References are :class:`stalker.models.file.File` instances or anything
    derived from it, which adds information to the attached objects. The aim of
    the References are generally to give more info to direct the evolution of
    the object.

    Args:
        references (File): A list of :class:`.File` instances.
    """

    # add this lines for Sphinx
    #    __tablename__ = "ReferenceMixins"

    def __init__(
        self, references: Optional[List["File"]] = None, **kwargs: Dict[str, Any]
    ) -> None:
        if references is None:
            references = []

        self.references = references

    @declared_attr
    def references(cls) -> Mapped[Optional[List["File"]]]:
        """Create the references attribute as a declared attribute.

        Returns:
            relationship: The relationship object related to the references attribute.
        """
        primary_cls_name = f"{cls.__name__}"
        secondary_cls_name = "Reference"
        primary_cls_table_name = f"{cls.__tablename__}"
        secondary_cls_table_name = "Files"
        secondary_table_name = f"{cls.__name__}_References"

        # get secondary table
        secondary_table = create_secondary_table(
            primary_cls_name=primary_cls_name,
            secondary_cls_name=secondary_cls_name,
            primary_cls_table_name=primary_cls_table_name,
            secondary_cls_table_name=secondary_cls_table_name,
            secondary_table_name=secondary_table_name,
        )
        # return the relationship
        return relationship(
            secondary=secondary_table,
            primaryjoin=f"{primary_cls_table_name}.c.id=={secondary_table_name}.c.{primary_cls_name.lower()}_id",
            secondaryjoin=f"{secondary_table_name}.c.{secondary_cls_name.lower()}_id=={secondary_cls_table_name}.c.id",
            doc="""A list of :class:`.File` instances given as a reference for
            this entity.
            """,
        )

    @validates("references")
    def _validate_references(self, key: str, reference: "File") -> "File":
        """Validate the given reference.

        Args:
            key (str): The name of the validated column.
            reference (File): The reference value to be validated.

        Raises:
            TypeError: If the reference is not a File instance.

        Returns:
            File: The validated reference value.
        """
        from stalker.models.file import File

        # all items should be instance of stalker.models.entity.Entity
        if not isinstance(reference, File):
            raise TypeError(
                f"{self.__class__.__name__}.references should only contain "
                "instances of stalker.models.file.File, "
                f"not {reference.__class__.__name__}: '{reference}'"
            )
        return reference


class ACLMixin(object):
    """A Mixin for adding ACLs to mixed in class.

    Access control lists or ACLs are used to determine if the given resource has the
    permission to access the given data. It is based on Pyramids Authorization system
    but organized to fit in Stalker style.

    The ACLMixin adds an attribute called ``permissions`` and a property called
    ``__acl__`` to be able to pass the permission data to Pyramid framework.
    """

    @declared_attr
    def permissions(cls) -> Mapped[List["Permission"]]:
        """Create the permissions attribute as a declared attribute.

        Returns:
            relationship: The relationship object related to the permissions attribute.
        """
        # get the secondary table
        secondary_table = create_secondary_table(
            cls.__name__, "Permission", cls.__tablename__, "Permissions"
        )
        return relationship("Permission", secondary=secondary_table)

    @validates("permissions")
    def _validate_permissions(self, key: str, permission: "Permission") -> "Permission":
        """Validate the given permission value.

        Args:
            key (str): The name of the validated column.
            permission (Permission): The permission value to be validated.

        Raises:
            TypeError: If the given permission value is not a Permission instance.

        Returns:
            Permission: The validated permission value.
        """
        from stalker.models.auth import Permission

        if not isinstance(permission, Permission):
            raise TypeError(
                f"{self.__class__.__name__}.permissions should be all instances of "
                "stalker.models.auth.Permission, "
                f"not {permission.__class__.__name__}: '{permission}'"
            )

        return permission

    @property
    def __acl__(self) -> List[Tuple[str, str, str]]:
        """Return Pyramid friendly ACL list.

        The ACL list is composed by the:

          * Permission.access (Ex: 'Allow' or 'Deny')
          * The Mixed in class name and the object name (Ex: 'User:eoyilmaz')
          * The Action and the target class name (Ex: 'Create_Asset')

        Thus, a list of tuple is returned as follows::

          __acl__ = [
              ('Allow', 'User:eoyilmaz', 'Create_Asset'),
          ]

        For the last example user eoyilmaz can grant access to views requiring
        'Add_Project' permission.

        Returns:
            List[Tuple[str, str, str]]: A list of tuples containing the ACL .
        """
        return [
            (
                perm.access,
                f"{self.__class__.__name__}:{self.name}",
                f"{perm.action}_{perm.class_name}",
            )
            for perm in self.permissions
        ]


class CodeMixin(object):
    """Adds code info to the mixed in class.

    .. versionadded:: 0.2.0

      The code attribute of the SimpleEntity is now introduced as a separate
      mixin. To let it be used by the classes it is really needed.

    The CodeMixin just adds a new field called ``code``. It is a very simple attribute
    and is used for simplifying long names (like Project.name etc.).

    Contrary to previous implementations the code attribute is not formatted in any way,
    so care needs to be taken if the code attribute is going to be used in filesystem as
    file and directory names.

    Args:
        code (str): The code attribute is a string, cannot be empty or cannot be None.
    """

    def __init__(
        self,
        code: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        logger.debug(f"code: {code}")
        self.code = code

    @declared_attr
    def code(cls) -> Mapped[str]:
        """Create the code attribute as a declared attribute.

        Returns:
            Column: The Column related to the code attribute.
        """
        return mapped_column(
            "code",
            String(256),
            nullable=False,
            doc="""The code name of this object.

                It accepts strings. Cannot be None.""",
        )

    @validates("code")
    def _validate_code(self, key: str, code: str) -> str:
        """Validate the given code attribute.

        Args:
            key (str): The name of the validated column.
            code (str): The code value to be validated.

        Raises:
            TypeError: If the given code is not a str.
            ValueError: If the given code value is an empty str.

        Returns:
            str: The validated code value.
        """
        logger.debug(f"validating code value of: {code}")
        if code is None:
            raise TypeError(f"{self.__class__.__name__}.code cannot be None")

        if not isinstance(code, str):
            raise TypeError(
                f"{self.__class__.__name__}.code should be a string, "
                f"not {code.__class__.__name__}: '{code}'"
            )

        if code == "":
            raise ValueError(
                f"{self.__class__.__name__}.code cannot be an empty string"
            )

        return code


class WorkingHoursMixin(object):
    """Set working hours for the mixed in class.

    Generally is meaningful for users, departments and studio.

    Args:
        working_hours (WorkingHours): A :class:`.WorkingHours` instance showing the
            working hours settings.
    """

    def __init__(
        self, working_hours: Optional["WorkingHours"] = None, **kwargs: Dict[str, Any]
    ) -> None:
        self.working_hours = working_hours

    @declared_attr
    def working_hours_id(cls) -> Mapped[Optional[int]]:
        """Create the working_hours_id attribute as a declared attribute.

        Returns:
            Column: The Column related to the working_hours_id attribute.
        """
        return mapped_column("working_hours_id", Integer, ForeignKey("WorkingHours.id"))

    @declared_attr
    def working_hours(cls) -> Mapped[Optional["WorkingHours"]]:
        """Create the working_hours attribute as a declared attribute.

        Returns:
            relationship: The relationship object related to the working_hours
                attribute.
        """
        return relationship(
            "WorkingHours",
            primaryjoin=f"{cls.__name__}.working_hours_id==WorkingHours.working_hours_id",
        )

    @validates("working_hours")
    def _validate_working_hours(
        self, key, wh: Union[None, "WorkingHours"]
    ) -> "WorkingHours":
        """Validate the given working hours value.

        Args:
            key (str): The name of the validated column.
            wh (WorkingHours): The working hours value to be validated.

        Raises:
            TypeError: If the working hours is not None and not a WorkingHours instance.

        Returns:
            WorkingHours: The validated WorkingHours value.
        """
        from stalker.models.studio import WorkingHours

        if wh is None:
            wh = WorkingHours()  # without any argument this will use the
            # default.working_hours settings
        elif not isinstance(wh, WorkingHours):
            raise TypeError(
                f"{self.__class__.__name__}.working_hours should be a "
                "stalker.models.studio.WorkingHours instance, "
                f"not {wh.__class__.__name__}: '{wh}'"
            )

        return wh


class ScheduleMixin(object):
    """Add schedule info to the mixed in class.

    Add attributes like schedule_timing, schedule_unit and schedule_model
    attributes to the mixed in class.

    Use the ``__default_schedule_attr_name__`` attribute to customize the
    column names.
    """

    # some default values that can be overridden in Mixed in classes
    __default_schedule_attr_name__ = "schedule"
    __default_schedule_timing__ = defaults.timing_resolution.seconds / 60
    __default_schedule_unit__ = TimeUnit.Hour
    __default_schedule_model__ = ScheduleModel.Effort

    def __init__(
        self,
        schedule_timing: Optional[float] = None,
        schedule_unit: TimeUnit = TimeUnit.Hour,
        schedule_model: Optional[ScheduleModel] = ScheduleModel.Effort,
        schedule_constraint: ScheduleConstraint = ScheduleConstraint.NONE,
        **kwargs: Dict[str, Any],
    ) -> None:
        self.schedule_constraint = schedule_constraint
        self.schedule_model = schedule_model
        self.schedule_timing = schedule_timing
        self.schedule_unit = schedule_unit

    @declared_attr
    def schedule_timing(cls) -> Mapped[Optional[float]]:
        """Create the schedule_timing attribute as a declared attribute.

        Returns:
            Column: The Column related to the schedule_timing attribute.
        """
        return mapped_column(
            f"{cls.__default_schedule_attr_name__}_timing",
            Float,
            nullable=True,
            default=0,
            doc="""It is the value of the {attr} timing. It is a float value.

            The timing value can either be as Work Time or Calendar Time
            defined by the {attr}_model attribute. So when the {attr}_model
            is `duration` then the value of this attribute is in Calendar Time,
            and if the {attr}_model is either `length` or `effort` then the
            value is considered as Work Time.
            """.format(
                attr=cls.__default_schedule_attr_name__
            ),
        )

    @declared_attr
    def schedule_unit(cls) -> Mapped[Optional[TimeUnit]]:
        """Create the schedule_unit attribute as a declared attribute.

        Returns:
            Column: The Column related to the schedule_unit attribute.
        """
        return mapped_column(
            f"{cls.__default_schedule_attr_name__}_unit",
            TimeUnitDecorator(),
            nullable=True,
            default=TimeUnit.Hour,
            doc=f"It is the unit of the {cls.__default_schedule_attr_name__} "
            "timing. It is a TimeUnit enum value.",
        )

    @declared_attr
    def schedule_model(cls) -> Mapped[ScheduleModel]:
        """Create the schedule_model attribute as a declared attribute.

        Returns:
            Column: The Column related to the schedule_model attribute.
        """
        return mapped_column(
            f"{cls.__default_schedule_attr_name__}_model",
            ScheduleModelDecorator(),
            default=ScheduleModel.Effort,
            nullable=False,
            doc="""Defines the schedule model which is used by **TaskJuggler**
            while scheduling this Projects. It is handled as a ScheduleModel
            enum value which has three possible values; **effort**,
            **duration**, **length**. :attr:`.ScheduleModel.Effort` is the
            default value. Each value causes this task to be scheduled in
            different ways:

            ======== ==========================================================
            effort   If the :attr:`.schedule_model` attribute is set to
                     **"effort"** then the start and end date values are
                     calculated so that a resource should spent this much of
                     work time to complete a Task. For example, a task with
                     :attr:`.schedule_timing` of 4 days, needs 4 working days.
                     So it can take 4 working days to complete the Task, but it
                     doesn't mean that the task duration will be 4 days. If the
                     resource works overtime then the task will be finished
                     before 4 days or if the resource will not be available
                     (due to a vacation or task coinciding to a weekend day)
                     then the task duration can be much more bigger than
                     required effort.

            duration The duration of the task will exactly be equal to
                     :attr:`.schedule_timing` regardless of the resource
                     availability. So the difference between :attr:`.start`
                     and :attr:`.end` attribute values are equal to
                     :attr:`.schedule_timing`. Essentially making the task
                     duration in calendar days instead of working days.

            length   In this model the duration of the task will exactly be
                     equal to the given length value in working days regardless
                     of the resource availability. So a task with the
                     :attr:`.schedule_timing` is set to 4 days will be
                     completed in 4 working days. But again it will not be
                     always 4 calendar days due to the weekends or non working
                     days.
            ======== ==========================================================
            """,
        )

    @declared_attr
    def schedule_constraint(cls) -> Mapped[ScheduleConstraint]:
        """Create the schedule_constraint attribute as a declared attribute.

        Returns:
            Column: The Column related to the schedule_constraint attribute.
        """
        return mapped_column(
            f"{cls.__default_schedule_attr_name__}_constraint",
            ScheduleConstraintDecorator(),
            default=0,
            nullable=False,
            doc="""A ScheduleConstraint value showing the constraint schema
            for this task.

            Possible values are:

             ===== ===============
               0   Constrain None
               1   Constrain Start
               2   Constrain End
               3   Constrain Both
             ===== ===============

            This value is going to be used to constrain the start and end date
            values of this task. So if you want to pin the start of a task to a
            certain date. Set its :attr:`.schedule_constraint` value to
            :attr:`.ScheduleConstraint.Start`. When the task is scheduled by
            **TaskJuggler** the start date will be pinned to the :attr:`start`
            attribute of this task.

            And if both of the date values (start and end) wanted to be pinned
            to certain dates (making the task effectively a ``duration`` task)
            set the desired :attr:`start` and :attr:`end` and then set the
            :attr:`schedule_constraint` to :att:`.ScheduleConstraint.Both`.
            """,
        )

    @validates("schedule_constraint")
    def _validate_schedule_constraint(
        self,
        key: str,
        schedule_constraint: Union[None, int, str],
    ) -> ScheduleConstraint:
        """Validate the given schedule_constraint value.

        Args:
            key (str): The name of the validated column.
            schedule_constraint (Union[None, int, str]): The value to be
                validated.

        Returns:
            ScheduleConstraint: The validated schedule_constraint value.
        """
        if schedule_constraint is None:
            schedule_constraint = ScheduleConstraint.NONE

        schedule_constraint = ScheduleConstraint.to_constraint(schedule_constraint)

        return schedule_constraint

    @validates("schedule_model")
    def _validate_schedule_model(
        self, key: str, schedule_model: Union[None, str, ScheduleModel]
    ) -> ScheduleModel:
        """Validate the given schedule_model value.

        Args:
            key (str): The name of the validated column.
            schedule_model (Union[None, str]): The schedule_model value to be
                validated.

        Returns:
            ScheduleModel: The validated schedule_model value.
        """
        if schedule_model is None:
            schedule_model = self.__default_schedule_model__
        else:
            schedule_model = ScheduleModel.to_model(schedule_model)

        return schedule_model

    @validates("schedule_unit")
    def _validate_schedule_unit(
        self, key: str, schedule_unit: Union[None, str, TimeUnit]
    ) -> TimeUnit:
        """Validate the given schedule_unit.

        Args:
            key (str): The name of the validated column.
            schedule_unit (Union[None, str, TimeUnit]): The schedule_unit value
                to be validated.

        Returns:
            TimeUnit: The validated schedule_unit value.
        """
        if schedule_unit is None:
            schedule_unit = self.__default_schedule_unit__

        schedule_unit = TimeUnit.to_unit(schedule_unit)

        return schedule_unit

    @validates("schedule_timing")
    def _validate_schedule_timing(
        self,
        key: str,
        schedule_timing: Union[None, int, float],
    ) -> float:
        """Validate the given schedule_timing.

        Args:
            key (str): The name of the validated column.
            schedule_timing (Union[None, int, float]): The schedule_timing
                value to be validated.

        Raises:
            TypeError: If the given schedule_timing is not an int or float.

        Returns:
            float: The validated schedule_timing value.
        """
        if schedule_timing is None:
            schedule_timing = self.__default_schedule_timing__
            self.schedule_unit = self.__default_schedule_unit__

        if not isinstance(schedule_timing, (int, float)):
            raise TypeError(
                "{cls}.{attr}_timing should be an integer or float "
                "number showing the value of the {attr} timing of this "
                "{cls}, not {timing_class}: '{timing}'".format(
                    cls=self.__class__.__name__,
                    attr=self.__default_schedule_attr_name__,
                    timing_class=schedule_timing.__class__.__name__,
                    timing=schedule_timing,
                )
            )

        return schedule_timing

    @classmethod
    def least_meaningful_time_unit(
        cls, seconds: int, as_work_time: bool = True
    ) -> Tuple[int, TimeUnit]:
        """Return the least meaningful time unit that corresponds to the given seconds.

        So if:

          as_work_time == True
              seconds % (1 year work time as seconds) == 0 --> 'y' else:
              seconds % (1 month work time as seconds) == 0 --> 'm' else:
              seconds % (1 week work time as seconds) == 0 --> 'w' else:
              seconds % (1 day work time as seconds) == 0 --> 'd' else:
              seconds % (1 hour work time as seconds) == 0 --> 'h' else:
              seconds % (1 minute work time as seconds) == 0 --> 'min' else:
              raise RuntimeError
          as_work_time == False
              seconds % (1 years as seconds) == 0 --> 'y' else:
              seconds % (1 month as seconds) == 0 --> 'm' else:
              seconds % (1 week as seconds) == 0 --> 'w' else:
              seconds % (1 day as seconds) == 0 --> 'd' else:
              seconds % (1 hour as seconds) == 0 --> 'h' else:
              seconds % (1 minutes as seconds) == 0 --> 'min' else:
              raise RuntimeError

        Args:
            seconds (int): An integer showing the total seconds to be
                converted.
            as_work_time (bool): Should the input be considered as work time or
                calendar time.

        Returns:
            int, TimeUnit: Returns one integer and a TimeUnit enum value,
                showing the timing value and the unit.
        """
        minutes = 60
        hour = 3600
        day = 86400
        week = 604800
        month = 2419200
        year = 31536000

        day_wt = defaults.daily_working_hours * 3600
        week_wt = defaults.weekly_working_days * day_wt
        month_wt = 4 * week_wt
        year_wt = int(defaults.yearly_working_days) * day_wt

        if as_work_time:
            logger.debug("calculating in work time")
            if seconds % year_wt == 0:  # noqa: S001
                return seconds // year_wt, TimeUnit.Year
            elif seconds % month_wt == 0:  # noqa: S001
                return seconds // month_wt, TimeUnit.Month
            elif seconds % week_wt == 0:  # noqa: S001
                return seconds // week_wt, TimeUnit.Week
            elif seconds % day_wt == 0:  # noqa: S001
                return seconds // day_wt, TimeUnit.Day
        else:
            logger.debug("calculating in calendar time")  # noqa: S001
            if seconds % year == 0:  # noqa: S001
                return seconds // year, TimeUnit.Year
            elif seconds % month == 0:  # noqa: S001
                return seconds // month, TimeUnit.Month
            elif seconds % week == 0:  # noqa: S001
                return seconds // week, TimeUnit.Week
            elif seconds % day == 0:  # noqa: S001
                return seconds // day, TimeUnit.Day

        # in either case
        if seconds % hour == 0:  # noqa: S001
            return seconds // hour, TimeUnit.Hour

        # at this point we understand that it has a residual of less then one
        # minute so return in minutes
        return seconds // minutes, TimeUnit.Minute

    @classmethod
    def to_seconds(
        cls,
        timing: float,
        unit: Union[None, str, TimeUnit],
        model: Union[str, ScheduleModel],
    ) -> Union[None, float]:
        """Convert the schedule values to seconds.

        Depending on to the schedule_model the value will differ. So if the
        schedule_model is 'effort' or 'length' then the schedule_time and schedule_unit
        values are interpreted as work time, if the schedule_model is 'duration' then
        the schedule_time and schedule_unit values are considered as calendar time.

        Args:
            timing (float): The timing value.
            unit (Union[None, str, TimeUnit]): The unit value, a TimeUnit enum
                value or one of ['min', 'h', 'd', 'w', 'm', 'y', 'Minute',
                'Hour', 'Day', 'Week', 'Month', 'Year'].
            model (str): The schedule model, preferably a ScheduleModel enum
                value or one of 'effort', 'length' or 'duration'.

        Returns:
            Union[None, float]: The converted seconds value.
        """
        if not unit:
            return None

        unit = TimeUnit.to_unit(unit)

        lut = {
            TimeUnit.Minute: 60,
            TimeUnit.Hour: 3600,
            TimeUnit.Day: 86400,
            TimeUnit.Week: 604800,
            TimeUnit.Month: 2419200,
            TimeUnit.Year: 31536000,
        }

        if model in [ScheduleModel.Effort, ScheduleModel.Length]:
            day_wt = defaults.daily_working_hours * 3600
            week_wt = defaults.weekly_working_days * day_wt
            month_wt = 4 * week_wt
            year_wt = int(defaults.yearly_working_days) * day_wt

            lut = {
                TimeUnit.Minute: 60,
                TimeUnit.Hour: 3600,
                TimeUnit.Day: day_wt,
                TimeUnit.Week: week_wt,
                TimeUnit.Month: month_wt,
                TimeUnit.Year: year_wt,
            }

        return timing * lut[unit]

    @classmethod
    def to_unit(
        cls,
        seconds: int,
        unit: Union[None, str, TimeUnit],
        model: Union[str, ScheduleModel],
    ) -> float:
        """Convert the ``seconds`` value to the given ``unit``.

        Depending on to the ``schedule_model`` the value will differ. So if the
        ``schedule_model`` is 'effort' or 'length' then the ``seconds`` and
        ``schedule_unit`` values are interpreted as work time, if the
        ``schedule_model`` is :attr:`ScheduleModel.Duration` then the
        ``seconds`` and ``schedule_unit`` values are considered as calendar
        time.

        Args:
            seconds (int): The seconds to convert.
            unit (Union[None, str, TimeUnit]): The unit value, a TimeUnit enum
                value one of ['min', 'h', 'd', 'w', 'm', 'y', 'Minute', 'Hour',
                'Day', 'Week', 'Month', 'Year'] or a TimeUnit enum value.
            model (Union[str, ScheduleModel]): The schedule model, either a
                ScheduleModel enum value or one of 'effort', 'length' or
                'duration'.

        Returns:
            float: The seconds converted to the given unit considering the
                given model.
        """
        if unit is None:
            return None

        unit = TimeUnit.to_unit(unit)
        model = ScheduleModel.to_model(model)

        lut = {
            TimeUnit.Minute: 60,
            TimeUnit.Hour: 3600,
            TimeUnit.Day: 86400,
            TimeUnit.Week: 604800,
            TimeUnit.Month: 2419200,
            TimeUnit.Year: 31536000,
        }

        if model in [ScheduleModel.Effort, ScheduleModel.Length]:
            day_wt = defaults.daily_working_hours * 3600
            week_wt = defaults.weekly_working_days * day_wt
            month_wt = 4 * week_wt
            year_wt = int(defaults.yearly_working_days) * day_wt

            lut = {
                TimeUnit.Minute: 60,
                TimeUnit.Hour: 3600,
                TimeUnit.Day: day_wt,
                TimeUnit.Week: week_wt,
                TimeUnit.Month: month_wt,
                TimeUnit.Year: year_wt,
            }

        return seconds / lut[unit]

    @property
    def schedule_seconds(self) -> float:
        """Return the schedule values as seconds.

        Depending on to the schedule_model the value will differ. So if the
        schedule_model is 'effort' or 'length' then the schedule_time and schedule_unit
        values are interpreted as work time, if the schedule_model is 'duration' then
        the schedule_time and schedule_unit values are considered as calendar time.

        Returns:
            float: The schedule_seconds as seconds.
        """
        return self.to_seconds(
            self.schedule_timing, self.schedule_unit, self.schedule_model
        )


class DAGMixin(object):
    """DAG mixin adds attributes required for parent/child relationship.

    Create a parent/child or a directed acyclic graph (DAG) relation on the mixed in
    class by introducing two new attributes called parent and children.

    Please set the ``__id_column__`` attribute to the id column of the mixed in
    class to be able to use this mixin::

    .. code-block: python

        class MixedInClass(SomeBaseClass, DAGMixin):

            id : Mapped[int] = mapped_column('id', primary_key=True)
            __id_column__ = id

    Use the :attr:``.__dag_cascade__`` to control the cascade behavior.
    """

    __dag_cascade__ = "all, delete"

    @declared_attr
    def parent_id(cls) -> Mapped[Optional[int]]:
        """Create the parent_id attribute as a declared attribute.

        Returns:
            Column: The Column related to the parent_id attribute.
        """
        return mapped_column(
            "parent_id", Integer, ForeignKey(f"{cls.__tablename__}.id")
        )

    @declared_attr
    def parent(cls) -> Mapped[Self]:
        """Create the parent attribute as a declared attribute.

        Returns:
            relationship: The relationship object related to the parent attribute.
        """
        return relationship(
            cls.__name__,
            remote_side=[getattr(cls, cls.__id_column__)],
            primaryjoin="{ct}.c.parent_id=={ct}.c.id".format(ct=cls.__tablename__),
            back_populates="children",
            post_update=True,
            doc="""A :class:`{c}` instance which is the parent of this {c}.
            In Stalker it is possible to create a hierarchy of {c}.
            """.format(
                c=cls.__name__
            ),
        )

    @declared_attr
    def children(cls) -> Mapped[List[Self]]:
        """Create the children attribute as a declared attribute.

        Returns:
            relationship: The relationship object related to the parent attribute.
        """
        return relationship(
            cls.__name__,
            primaryjoin="{ct}.c.id=={ct}.c.parent_id".format(ct=cls.__tablename__),
            back_populates="parent",
            post_update=True,
            cascade=cls.__dag_cascade__,
            doc="""Other :class:`Budget` instances which are the children of this
            one. This attribute along with the :attr:`.parent` attribute is used in
            creating a DAG hierarchy of tasks.
            """,
        )

    def __init__(self, parent: Optional[Self] = None, **kwargs: Dict[str, Any]) -> None:
        self.parent = parent

    @validates("parent")
    def _validate_parent(
        self, key: str, parent: Union[None, Self]
    ) -> Union[None, Self]:
        """Validate the given parent value.

        Args:
            key (str): The name of the validated column.
            parent (object): The parent object to be validated.

        Raises:
            TypeError: If the parent is not None and not deriving from the same class
                with this instance.

        Returns:
            Union[None, Self]: The validated parent value.
        """
        if parent is None:
            return parent

        if not isinstance(parent, self.__class__):
            raise TypeError(
                "{cls}.parent should be an instance of {cls} class or "
                "derivative, not {parent_cls}: '{parent}'".format(
                    cls=self.__class__.__name__,
                    parent_cls=parent.__class__.__name__,
                    parent=parent,
                )
            )
        check_circular_dependency(self, parent, "children")

        return parent

    @validates("children")
    def _validate_children(self, key: str, child: Self) -> Self:
        """Validate the given child.

        Args:
            key (str): The name of the validated column.
            child (Self): The child value to be validated.

        Raises:
            TypeError: If any of the child objects are not deriving from the same class
                as this one.

        Returns:
            Self: The validated child instance.
        """
        if not isinstance(child, self.__class__):
            raise TypeError(
                "{cls}.children should only contain instances of {cls} "
                "(or derivative), not {child_cls}: '{child}'".format(
                    cls=self.__class__.__name__,
                    child_cls=child.__class__.__name__,
                    child=child,
                )
            )

        return child

    @property
    def is_root(self) -> bool:
        """Return True if the Task has no parent.

        Returns:
            bool: True if the Task has no parent.
        """
        return not bool(self.parent)

    @property
    def is_container(self) -> bool:
        """Return True if the Task has children Tasks.

        Returns:
            bool: True if the Task has children Tasks.
        """
        with DBSession.no_autoflush:
            return bool(len(self.children))

    @property
    def is_leaf(self) -> bool:
        """Return True if the Task has no children Tasks.

        Returns:
            bool: True if the Task has no children Tasks.
        """
        return not self.is_container

    @property
    def parents(self) -> List[Self]:
        """Return all of the parents of this mixed in class starting from the root.

        Returns:
            List[Self]: List of tasks showing the parent of this Task.
        """
        parents = []
        entity = self.parent
        # TODO: make this a generator
        while entity:
            parents.append(entity)
            entity = entity.parent
        parents.reverse()
        return parents

    def walk_hierarchy(
        self,
        method: Union[int, str, TraversalDirection] = TraversalDirection.DepthFirst,
    ) -> Generator[None, Self, None]:
        """Walk the hierarchy of this task.

        Args:
            method (Union[int, str, TraversalDirection]): The walk method
                defined by the :class:`.TraversalDirection` enum value. The
                default is :attr:`.TraversalDirection.DepthFirst`.

        Yields:
            Task: The child Task.
        """
        for c in walk_hierarchy(self, "children", method=method):
            yield c


class AmountMixin(object):
    """Adds ``amount`` attribute to the mixed in class.

    Args:
        amount (Union[int, float]): The amount value.
    """

    def __init__(self, amount: Union[int, float] = 0, **kwargs: Dict[str, Any]) -> None:
        self.amount = amount

    @declared_attr
    def amount(cls) -> Mapped[Optional[float]]:
        """Create the amount attribute as a declared attribute.

        Returns:
            Column: The Column related to the amount attribute.
        """
        return mapped_column(Float, default=0.0)

    @validates("amount")
    def _validate_amount(self, key: str, amount: Union[int, float]) -> float:
        """Validate the given amount value.

        Args:
            key (str): The name of the validated column.
            amount (Union[int, float]): The amount value to be validated.

        Raises:
            TypeError: If the given amount value is not a int or float.

        Returns:
            float: The validated amount value.
        """
        if amount is None:
            amount = 0.0

        if not isinstance(amount, (int, float)):
            raise TypeError(
                f"{self.__class__.__name__}.amount should be a number, "
                f"not {amount.__class__.__name__}: '{amount}'"
            )

        return float(amount)


class UnitMixin(object):
    """Adds ``unit`` attribute to the mixed in class.

    Args:
        unit (str): The unit of this mixed in class.
    """

    def __init__(self, unit: str = "", **kwargs: Dict[str, Any]) -> None:
        self.unit = unit

    @declared_attr
    def unit(cls) -> Mapped[Optional[str]]:
        """Create the unit attribute as a declared attribute.

        Returns:
            Column: The Column related to the unit attribute.
        """
        return mapped_column(String(64))

    @validates("unit")
    def _validate_unit(self, key: str, unit: Union[None, str]) -> str:
        """Validate the given unit value.

        Args:
            key (str): The name of the validated column.
            unit (str): The unit value to be validated.

        Raises:
            TypeError: If the given unit is not a str.

        Returns:
            str: The validated unit value.
        """
        if unit is None:
            unit = ""

        if not isinstance(unit, str):
            raise TypeError(
                f"{self.__class__.__name__}.unit should be a string, "
                f"not {unit.__class__.__name__}: '{unit}'"
            )

        return unit
