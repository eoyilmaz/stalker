# -*- coding: utf-8 -*-
"""Studio, WorkingHours and Vacation related functions and classes are situated here."""

import copy
import datetime
import time
from math import ceil
from typing import Any, Dict, List, Optional, Union

import pytz

from sqlalchemy import ForeignKey, Interval, Text
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    reconstructor,
    relationship,
    synonym,
    validates,
)

from stalker import defaults, log
from stalker.db.session import DBSession
from stalker.db.types import GenericDateTime, GenericJSON
from stalker.models.auth import User
from stalker.models.department import Department
from stalker.models.entity import Entity, SimpleEntity
from stalker.models.mixins import DateRangeMixin, WorkingHoursMixin
from stalker.models.project import Project
from stalker.models.schedulers import SchedulerBase
from stalker.models.status import Status


logger = log.get_logger(__name__)


class Studio(Entity, DateRangeMixin, WorkingHoursMixin):
    """Manage all the studio information at once.

    With Stalker, you can manage all you Studio data by using this class. Studio
    knows all the projects, all the departments, all the users and every thing
    about the studio. But the most important part of the Studio is that it can
    schedule all the Projects by using TaskJuggler.

    Studio class is kind of the database itself::

      studio = Studio()

      # simple data
      studio.projects
      studio.active_projects
      studio.inactive_projects
      studio.departments
      studio.users

      # project management
      studio.to_tjp          # a tjp representation of the studio with all
                             # its projects, departments and resources etc.

      studio.schedule() # schedules all the active projects at once

    **Working Hours**

    In Stalker, Studio class also manages the working hours of the studio.
    Allowing project tasks to be scheduled to be scheduled in those hours.

    **Vacations**

    Studio wide vacations are managed by the Studio class.

    **Scheduling**

    .. versionadded: 0.2.5
       Schedule Info Attributes

    There are a couple of attributes those become pretty interesting when used
    together with the Studio instance while using the scheduling part of the
    Studio. Please refer to the attribute documentation for each attribute:

      :attr:`.is_scheduling`
      :attr:`.last_scheduled_at`
      :attr:`.last_scheduled_by`
      :attr:`.last_schedule_message`

    Args:
        daily_working_hours (int): An integer specifying the daily working
            hours for the studio. It is another critical value attribute which
            TaskJuggler uses mainly converting working day values to working hours
            (1d = 10h kind of thing).
        now (datetime.datetime): The now attribute overrides the TaskJugglers ``now``
            attribute allowing the user to schedule the projects as if the scheduling is
            done on that date. The default value is the rounded value of
            datetime.datetime.now(pytz.utc).
        timing_resolution (datetime.timedelta): The timing_resolution of the
            datetime.datetime object in datetime.timedelta. Uses ``timing_resolution``
            settings in the :class:`stalker.config.Config` class which defaults to 1
            hour. Setting the timing_resolution to less then 5 minutes is not suggested
            because it is a limit for TaskJuggler.
    """

    __auto_name__ = False
    __tablename__ = "Studios"
    __mapper_args__ = {"polymorphic_identity": "Studio"}

    studio_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    _timing_resolution: Mapped[Optional[datetime.timedelta]] = mapped_column(
        "timing_resolution", Interval
    )

    is_scheduling: Mapped[Optional[bool]] = mapped_column(default=False)
    is_scheduling_by_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("Users.id"),
        doc="The id of the user who is scheduling the Studio projects right " "now",
    )
    is_scheduling_by: Mapped[Optional[User]] = relationship(
        primaryjoin="Studios.c.is_scheduling_by_id==Users.c.id",
        doc="The User who is scheduling the Studio projects right now",
    )
    scheduling_started_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        GenericDateTime,
        doc="Stores when the current scheduling is started at, it is a good "
        "measure for measuring if the last schedule is not correctly "
        "finished",
    )
    last_scheduled_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        GenericDateTime, doc="Stores the last schedule date"
    )
    last_scheduled_by_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("Users.id"),
        doc="The id of the user who has last scheduled the Studio projects",
    )
    last_scheduled_by: Mapped[Optional[User]] = relationship(
        primaryjoin="Studios.c.last_scheduled_by_id==Users.c.id",
        doc="The User who has last scheduled the Studio projects",
    )
    last_schedule_message: Mapped[Optional[str]] = mapped_column(
        Text,
        doc="Holds the last schedule message, generally coming generated by "
        "TaskJuggler",
    )

    def __init__(
        self,
        daily_working_hours: Optional[int] = None,
        now: Optional[datetime.datetime] = None,
        timing_resolution: Optional[datetime.timedelta] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        super(Studio, self).__init__(**kwargs)
        DateRangeMixin.__init__(self, **kwargs)
        WorkingHoursMixin.__init__(self, **kwargs)
        self.timing_resolution = timing_resolution
        self.daily_working_hours = daily_working_hours
        self._now = None
        self.now = self._validate_now(now)
        self._scheduler = None

        # update defaults
        self.update_defaults()

    @property
    def daily_working_hours(self) -> int:
        """Return the Studio.working_hours.daily_working_hours.

        Returns:
            int: The daily working hours of this Studio.
        """
        return self.working_hours.daily_working_hours

    @daily_working_hours.setter
    def daily_working_hours(self, daily_working_hours: int) -> None:
        """Set the Studio.working_hours.daily_working_hours.

        Args:
            daily_working_hours (int): The daily working hours in this studio.
        """
        self.working_hours.daily_working_hours = daily_working_hours

    def update_defaults(self) -> None:
        """Update the default values with the studio."""
        # TODO: add update_defaults() to attribute edit/update methods,
        #       so we will always have an up to date info about the working
        #       hours.

        logger.debug("updating defaults with Studio instance")
        logger.debug("defaults: {}".format(defaults))
        logger.debug("id(defaults): {}".format(id(defaults)))

        defaults["daily_working_hours"] = self.daily_working_hours
        logger.debug(
            "updated defaults.daily_working_hours: {}".format(
                defaults.daily_working_hours
            )
        )

        defaults["weekly_working_days"] = self.weekly_working_days
        logger.debug(
            f"updated defaults.weekly_working_days: {defaults.weekly_working_days}"
        )

        defaults["weekly_working_hours"] = self.weekly_working_hours
        logger.debug(
            "updated defaults.weekly_working_hours: {}".format(
                defaults.weekly_working_hours
            )
        )

        defaults["yearly_working_days"] = self.yearly_working_days
        logger.debug(
            f"updated defaults.yearly_working_days: {defaults.yearly_working_days}"
        )

        defaults["timing_resolution"] = self.timing_resolution
        logger.debug(
            f"updated defaults.timing_resolution: {defaults.timing_resolution}"
        )

        logger.debug(
            """done updating defaults:
        daily_working_hours  : {daily_working_hours}
        weekly_working_days  : {weekly_working_days}
        weekly_working_hours : {weekly_working_hours}
        yearly_working_days  : {yearly_working_days}
        timing_resolution    : {timing_resolution}
        """.format(
                daily_working_hours=defaults.daily_working_hours,
                weekly_working_days=defaults.weekly_working_days,
                weekly_working_hours=defaults.weekly_working_hours,
                yearly_working_days=defaults.yearly_working_days,
                timing_resolution=defaults.timing_resolution,
            )
        )

    @reconstructor
    def __init_on_load__(self) -> None:
        """Update defaults on load."""
        self.update_defaults()

    def _validate_now(self, now: datetime.datetime) -> datetime.datetime:
        """Validate the given now value.

        Args:
            now (Union[None, datetime.datetime]): Either None in which the current
                date and time will be used or a datetime.datetime instance.

        Raises:
            TypeError: If the now value is not None and not a datetime.datetime
                instance.

        Returns:
            datetime.datetime: The validated datetime.datetime value.
        """
        if now is None:
            now = datetime.datetime.now(pytz.utc)

        if not isinstance(now, datetime.datetime):
            raise TypeError(
                "{}.now attribute should be an instance of datetime.datetime, "
                "not {}: '{}'".format(
                    self.__class__.__name__, now.__class__.__name__, now
                )
            )

        return self.round_time(now)

    @property
    def now(self) -> datetime.datetime:
        """Return the currently stored now value.

        Returns:
            datetime.datetime: Return the currently stored now value if there is any,
                return the current date and time otherwise.
        """
        if self._now is None:
            self._now = self.round_time(datetime.datetime.now(pytz.utc))
        return self._now

    @now.setter
    def now(self, now: datetime.datetime) -> None:
        """Set the current date and time.

        Args:
            now (datetime.datetime): The datetime.datetime instance showing the current
                date and time, useful for project management purposes before
                scheduling.
        """
        self._now = self._validate_now(now)

    def _validate_scheduler(
        self, scheduler: Union[None, SchedulerBase]
    ) -> Union[None, SchedulerBase]:
        """Validate the given scheduler value.

        Args:
            scheduler (Union[None, SchedulerBase]): The scheduler to be used to schedule
                the projects in this Studio instance. Can be set to None to disable the
                scheduling abilities.

        Raises:
            TypeError: If the given scheduler value is not None and is not a
                SchedulerBase instance.

        Returns:
            Union[None, SchedulerBase]: The validated scheduler value.
        """
        if scheduler is not None and not isinstance(scheduler, SchedulerBase):
            raise TypeError(
                "{}.scheduler should be an instance of "
                "stalker.models.scheduler.SchedulerBase, not {}: '{}'".format(
                    self.__class__.__name__, scheduler.__class__.__name__, scheduler
                )
            )
        return scheduler

    @property
    def scheduler(self) -> Union[None, SchedulerBase]:
        """Return the scheduler.

        Returns:
            Union[None, SchedulerBase]: The scheduler of this Studio.
        """
        return self._scheduler

    @scheduler.setter
    def scheduler(self, scheduler: Union[None, SchedulerBase]):
        """Set the scheduler.

        Args:
            scheduler (Union[None, SchedulerBase]): The SchedulerBase derivative as
                the scheduler.
        """
        self._scheduler = self._validate_scheduler(scheduler)

    @property
    def to_tjp(self) -> str:
        """Convert the studio to a tjp representation.

        Returns:
            str: The TaskJuggler representation of this Studio.
        """
        start = time.time()

        tab = "    "
        indent = tab
        now = self.round_time(self.now).astimezone(pytz.utc).strftime("%Y-%m-%d-%H:%M")
        tjp = (
            f'project {self.tjp_id} "{self.tjp_id}" '
            f"{self.start.date()} - {self.end.date()} {{"
        )
        timing_resolution = (
            self.timing_resolution.days * 86400 + self.timing_resolution.seconds // 60
        )
        tjp += f"\n{indent}timingresolution {timing_resolution}min"
        tjp += f"\n{indent}now {now}"
        tjp += f"\n{indent}dailyworkinghours {self.daily_working_hours}"
        tjp += f"\n{indent}weekstartsmonday"

        # working hours
        tjp += "\n"
        tjp += "\n".join(
            f"{indent}{line}" for line in self.working_hours.to_tjp.split("\n")
        )

        tjp += f'\n{indent}timeformat "%Y-%m-%d"'
        tjp += f'\n{indent}scenario plan "Plan"'
        tjp += f"\n{indent}trackingscenario plan"
        tjp += "\n}"

        end = time.time()
        logger.debug("render studio to tjp took: {:0.3f} seconds".format(end - start))
        return tjp

    @property
    def projects(self) -> List[Project]:
        """Returns all the projects in the studio.

        Returns:
            List[Project]: List of all the Project instances in this Studio.
        """
        return Project.query.all()

    @property
    def active_projects(self) -> List[Project]:
        """Return all the active projects in the studio.

        Returns:
            List[Project]: List of active Project instances in this studio.
        """
        with DBSession.no_autoflush:
            wip = Status.query.filter_by(code="WIP").first()
        return Project.query.filter(Project.status == wip).all()

    @property
    def inactive_projects(self) -> List[Project]:
        """Return all the inactive projects in the studio.

        Returns:
            List[Project]: List of inactive Project instances in this studio.
        """
        with DBSession.no_autoflush:
            wip = Status.query.filter_by(code="WIP").first()
        return Project.query.filter(Project.status != wip).all()

    @property
    def departments(self) -> List[Department]:
        """Return all the departments in the studio.

        Returns:
            List[Department]: The list of Department instances in this Studio.
        """
        return Department.query.all()

    @property
    def users(self) -> List[User]:
        """Return all the users in the studio.

        Returns:
            List[User]: List of User instances in the studio.
        """
        return User.query.all()

    @property
    def vacations(self) -> List["Vacation"]:
        """Return all Vacations which doesn't have a User defined.

        Returns:
            List[Vacation]: List of Vacation instances.
        """
        return Vacation.query.filter(Vacation.user == None).all()  # noqa: E711

    def schedule(self, scheduled_by: Optional[User] = None) -> str:
        """Schedule all the active projects in the studio.

        Needs a Scheduler, so before calling it set a scheduler by using the
        :attr:`.scheduler` attribute.

        Args:
            scheduled_by (stalker.models.auth.User): A User instance who is doing the
                scheduling.

        Raises:
            RuntimeError: If the `self.scheduler` is None or it is not a `SchedulerBase`
                instance.

        Returns:
            str: The result of the scheduling process.
        """
        # check the scheduler first
        if self.scheduler is None or not isinstance(self.scheduler, SchedulerBase):
            raise RuntimeError(
                "There is no scheduler for this {cls}, please assign a scheduler to "
                "the {cls}.scheduler attribute, before calling {cls}.schedule()".format(
                    cls=self.__class__.__name__
                )
            )

        with DBSession.no_autoflush:
            self.scheduling_started_at = datetime.datetime.now(pytz.utc)

            # run the scheduler
            self.scheduler.studio = self
        start = time.time()

        # commit before scheduling
        # DBSession.commit()

        result = None
        try:
            result = self.scheduler.schedule()
        finally:
            # in any case set is_scheduling to False
            with DBSession.no_autoflush:
                self.is_scheduling = False
                self.is_scheduling_by = None

                # also store the result
                # if result:
                self.last_schedule_message = result

                # And the date the schedule is completed
                self.last_scheduled_at = datetime.datetime.now(pytz.utc)

                # and who has done the scheduling
                if scheduled_by:
                    logger.debug(f"setting last_scheduled_by to : {scheduled_by}")
                    self.last_scheduled_by = scheduled_by

        end = time.time()
        logger.debug("scheduling took {:0.3f} seconds".format(end - start))
        return result

    @property
    def weekly_working_hours(self) -> int:
        """Return the WorkingHours.weekly_working_hours value.

        Returns:
            int: The weekly working hours value stored in the working hours
                configuration of this Studio instance.
        """
        return self.working_hours.weekly_working_hours

    @property
    def weekly_working_days(self) -> int:
        """Return the WorkingHours.weekly_working_hours value.

        Returns:
            int: The weekly working days value stored in the working hours
                configuration of this Studio instance.
        """
        return self.working_hours.weekly_working_days

    @property
    def yearly_working_days(self) -> int:
        """Return the WorkingHours.yearly_working_days value.

        Returns:
            int: The yearly working days in the working hours configuration of this
                Studio instance.
        """
        return self.working_hours.yearly_working_days

    def to_unit(
        self,
        from_timing: int,
        from_unit: str,
        to_unit: str,
        working_hours: bool = True,
    ) -> int:
        """Convert the given timing and unit to the desired unit.

        If working_hours=True then the given timing is considered as working hours.

        Args:
            from_timing (int): The timing value.
            from_unit (str): The timing unit.
            to_unit (str): The other timing unit to convert the given timing unit to.
            working_hours (bool): True to consider the given from timing as a working
                hour. Default is True.

        Raises:
            NotImplementedError: Unless it is implemented.
        """
        raise NotImplementedError("this is not implemented yet")

    def _timing_resolution_getter(self) -> datetime.timedelta:
        """Return the timing_resolution value.

        Returns:
            datetime.timedelta: The timing resolution stored in this Studio instance.
        """
        return self._timing_resolution

    def _timing_resolution_setter(self, timing_resolution: datetime.timedelta) -> None:
        """Set the timing_resolution.

        Args:
            timing_resolution (datetime.timedelta): The `timing_resolution` instance to
                validate.
        """
        self._timing_resolution = self._validate_timing_resolution(timing_resolution)
        logger.debug(f"self._timing_resolution: {self._timing_resolution}")
        # update date values
        if self.start and self.end and self.duration:
            self._start, self._end, self._duration = self._validate_dates(
                self.round_time(self.start), self.round_time(self.end), None
            )

    timing_resolution: Mapped[Optional[datetime.timedelta]] = synonym(
        "_timing_resolution",
        descriptor=property(
            _timing_resolution_getter,
            _timing_resolution_setter,
            doc="""The timing_resolution of this object.

            Can be set to any value that is representable with
            datetime.timedelta. The default value is 1 hour. Whenever it is
            changed the start, end and duration values will be updated.
            """,
        ),
    )

    def _validate_timing_resolution(
        self, timing_resolution: datetime.timedelta
    ) -> datetime.timedelta:
        """Validate the given timing_resolution value.

        Args:
            timing_resolution (datetime.timedelta): The timing resolution value as a
                `datetime.timedelta` instance.

        Raises:
            TypeError: If the given `timing_resolution` is not a `datetime.timedelta`
                instance.

        Returns:
            datetime.timedelta: The validated timing resolution instance.
        """
        if timing_resolution is None:
            timing_resolution = defaults.timing_resolution

        if not isinstance(timing_resolution, datetime.timedelta):
            raise TypeError(
                "{}.timing_resolution should be an instance of "
                "datetime.timedelta, not {}: '{}'".format(
                    self.__class__.__name__,
                    timing_resolution.__class__.__name__,
                    timing_resolution,
                )
            )

        return timing_resolution


class WorkingHours(Entity):
    """A helper class to manage Studio working hours.

    Working hours is a data class to store the weekly working hours pattern of
    the studio.

    The data stored as a dictionary with the short day names are used as the
    key and the value is a list of two integers showing the working hours
    interval as the minutes after midnight. This is done in that way to ease
    the data transfer to TaskJuggler. The default value is defined in
    :class:`stalker.config.Config` ::

      wh = WorkingHours()
      wh.working_hours = {
          'mon': [[540, 720], [820, 1080]], # 9:00 - 12:00, 13:00 - 18:00
          'tue': [[540, 720], [820, 1080]], # 9:00 - 12:00, 13:00 - 18:00
          'wed': [[540, 720], [820, 1080]], # 9:00 - 12:00, 13:00 - 18:00
          'thu': [[540, 720], [820, 1080]], # 9:00 - 12:00, 13:00 - 18:00
          'fri': [[540, 720], [820, 1080]], # 9:00 - 12:00, 13:00 - 18:00
          'sat': [], # saturday off
          'sun': [], # sunday off
      }

    The default value is 9:00 - 18:00 from Monday to Friday and Saturday and
    Sunday are off.

    The working hours can be updated by the user supplied dictionary. If the
    user supplied dictionary doesn't have all the days then the default values
    will be used for those days.

    It is possible to use day index and day short names as a key value to reach
    the data::

      from stalker import config
      defaults = config.Config()

      wh = WorkingHours()

      # this is same by doing wh.working_hours['sun']
      assert wh['sun'] == defaults.working_hours['sun']

      # you can reach the data using the weekday number as index
      assert wh[0] == defaults.working_hours['mon']

      # working hours of sunday if defaults are used or any other day defined
      # by the stalker.config.Config.day_order
      assert wh[0] == defaults.working_hours[defaults.day_order[0]]

    Args:
        working_hours (Union[None, dict]): The dictionary that shows the
            working hours. The keys of the dictionary should be one of ['mon',
            'tue', 'wed', 'thu', 'fri', 'sat', 'sun']. And the values should be
            a list of two integers like [[int, int], [int, int], ...] format,
            showing the minutes after midnight. For missing days the default
            value will be used. If skipped the default value is going to be
            used.
        daily_working_hours (Union[None, int]): The daily working hours value.
            If given None the default value will be used.
    """

    __auto_name__ = True
    __tablename__ = "WorkingHours"
    __mapper_args__ = {"polymorphic_identity": "WorkingHours"}

    working_hours_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )

    working_hours: Mapped[Optional[Dict[str, List]]] = mapped_column(GenericJSON)
    daily_working_hours: Mapped[Optional[int]] = mapped_column(
        default=defaults.daily_working_hours
    )

    def __init__(
        self,
        working_hours: Optional[Dict[str, List]] = None,
        daily_working_hours=None,
        **kwargs: Dict[str, Any],
    ) -> None:
        super(WorkingHours, self).__init__(**kwargs)
        if working_hours is None:
            working_hours = defaults.working_hours
        self.working_hours = working_hours
        self.daily_working_hours = daily_working_hours

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is a WorkingHours instance and has
                the same working_hours.
        """
        return (
            isinstance(other, WorkingHours)
            and other.working_hours == self.working_hours
        )

    def __getitem__(self, index: Union[int, str]) -> Optional[List]:
        """Return the item at the given index.

        Args:
            index (Union[int, str]): Either an integer representing the weekday starting
                from Monday:0 or a string value of a shorthand day name one of
                ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].

        Returns:
            List[int, int]: The daily working hour arranged in a list where the first
                item is the minute from the midnight of the start of the working hour
                and the second item is the minute from the midnight of the end of the
                daily working hour. As in [540, 1080] represents 9am to 6pm.
        """
        if isinstance(index, int):
            return self.working_hours[defaults.day_order[index]]
        elif isinstance(index, str):
            return self.working_hours[index]

    def __setitem__(self, key: Union[int, str], value: List[List]) -> None:
        """Set the item value at the given index.

        Args:
            key (Union[int, str]): The index to set the value of or the day name.
            value (List[List[int, int]]): The working hours data arranged in a list of
                lists of two integers.

        Raises:
            KeyError: If the given key value is not one of the day names.
        """
        self._validate_working_hours_value(value)
        if isinstance(key, int):
            self.working_hours[defaults.day_order[key]] = value
        elif isinstance(key, str):
            # check if key is in
            if key not in defaults.day_order:
                raise KeyError(
                    "{} accepts only {} as key, not '{}'".format(
                        self.__class__.__name__, defaults.day_order, key
                    )
                )
            self.working_hours[key] = value

    @validates("working_hours")
    def _validate_working_hours(self, key: str, working_hours: Dict[str, List]) -> dict:
        """Validate the given working hours value.

        Args:
            key (str): The name of the validated column.
            working_hours (dict): The working hours value to be validated.

        Raises:
            TypeError: If the given working hours is not a dictionary.
            TypeError: If the values in the working hours dictionary are not lists.

        Returns:
            dict: The validated working hours dictionary.
        """
        if not isinstance(working_hours, dict):
            raise TypeError(
                "{}.working_hours should be a dictionary, not {}: '{}'".format(
                    self.__class__.__name__,
                    working_hours.__class__.__name__,
                    working_hours,
                )
            )

        for day in working_hours:
            if not isinstance(working_hours[day], list):
                raise TypeError(
                    '{}.working_hours should be a dictionary with keys "mon, '
                    'tue, wed, thu, fri, sat, sun" and the values should a '
                    "list of lists of two integers like [[540, 720], [800, "
                    "1080]], not {}: '{}'".format(
                        self.__class__.__name__,
                        working_hours[day].__class__.__name__,
                        working_hours[day],
                    )
                )

            # validate item values
            self._validate_working_hours_value(working_hours[day])

        # update the default values with the supplied working_hour dictionary
        # copy the defaults
        wh_def = copy.copy(defaults.working_hours)
        # update them
        wh_def.update(working_hours)

        return wh_def

    def is_working_hour(self, check_for_date: datetime.datetime) -> bool:
        """Check if the given datetime is in working hours.

        Args:
            check_for_date (datetime.datetime): The time value to check if it
                is a working hour.

        Returns:
            bool: True if the given datetime coincides to a working hour, False
                otherwise.
        """
        weekday_nr = check_for_date.weekday()
        hour = check_for_date.hour
        minute = check_for_date.minute

        time_from_midnight = hour * 60 + minute

        # check if the hour is inside the working hour ranges
        logger.debug(f"checking for: {time_from_midnight}")
        logger.debug(f"self[weekday_nr]: {self[weekday_nr]}")
        for working_hour_groups in self[weekday_nr]:
            start = working_hour_groups[0]
            end = working_hour_groups[1]
            logger.debug(f"start       : {start}")
            logger.debug(f"end         : {end}")
            if start <= time_from_midnight < end:
                return True

        return False

    def _validate_working_hours_value(self, value: List) -> List:
        """Validate the working hour value.

        The given value should follow the following format:

        .. code-block:: python

            working_hours = [
                [540, 1080],  # Working hour in minutes for Monday
                [540, 1080],  # Working hour in minutes for Tuesday
                [540, 1080],  # Working hour in minutes for Wednesday
                [540, 1080],  # Working hour in minutes for Thursday
                [540, 1080],  # Working hour in minutes for Friday
                [0, 0],  # Working hour in minutes for Saturday
                [0, 0],  # Working hour in minutes for Sunday
            ]

        Args:
            value (List): The validated working hour value.

        Raises:
            TypeError: If the given value is not a list.
            TypeError: If the immediate items in the list is not a list.
            TypeError: If the length of the items in the given list is not 2.
            TypeError: If the items in the lists inside the list are not integers.
            ValueError: If the integer values in the secondary lists are smaller than 0
                or larger than 1440 (which is 24 * 60).

        Returns:
            List[List[int, int]]
        """
        err = (
            "{}.working_hours value should be a list of lists of two "
            "integers and the range of integers should be between 0-1440, "
            "not {}: '{}'".format(
                self.__class__.__name__, value.__class__.__name__, value
            )
        )

        if not isinstance(value, list):
            raise TypeError(err)

        for i in value:
            if not isinstance(i, list):
                raise TypeError(err)

            # check list length
            if len(i) != 2:
                raise ValueError(err)

            # check type
            for j in range(2):
                if not isinstance(i[j], int):
                    raise TypeError(err)

                # check range
                if i[j] < 0 or i[j] > 1440:
                    raise ValueError(err)

        return value

    @property
    def to_tjp(self) -> str:
        """Return TaskJuggler representation of this object.

        Returns:
            str: The TaskJuggler representation.
        """
        tjp = ""
        for i, day in enumerate(["mon", "tue", "wed", "thu", "fri", "sat", "sun"]):
            if i != 0:
                tjp += "\n"
            tjp += f"workinghours {day} "
            if self[day]:
                for i, part in enumerate(self[day]):
                    start_hour, end_hour = part
                    if i != 0:
                        tjp += ", "
                    tjp += (
                        f"{start_hour // 60:02d}:{start_hour % 60:02d} - "
                        f"{end_hour // 60:02d}:{end_hour % 60:02d}"
                    )
            else:
                tjp += "off"
        return tjp

    @property
    def weekly_working_hours(self) -> int:
        """Return the total working hours in a week.

        Returns:
            int: The calculated weekly working hours.
        """
        weekly_working_hours = 0
        for i in range(0, 7):
            for start, end in self[i]:
                weekly_working_hours += end - start
        return weekly_working_hours / 60.0

    @property
    def weekly_working_days(self) -> int:
        """Return the weekly working days by looking at the working hours settings.

        Returns:
            int: The weekly working days value.
        """
        wwd = 0
        for i in range(0, 7):
            if len(self[i]):
                wwd += 1
        return wwd

    @property
    def yearly_working_days(self) -> int:
        """Return the total working days in a year.

        Returns:
            int: The calculated yearly_working_days value.
        """
        return int(ceil(self.weekly_working_days * 52.1428))

    @validates("daily_working_hours")
    def _validate_daily_working_hours(self, key: str, daily_working_hours: int) -> int:
        """Validate the given daily working hours value.

        Args:
            key (str): The name of the validated column.
            daily_working_hours (int): The daily working hours to be validated.

        Raises:
            TypeError: If the `daily_working_hours` value is not an integer.
            ValueError: If the `daily_working_hours` is smaller thane 0 or
                bigger than 24.

        Returns:
            int: The validated daily working hours value.
        """
        if daily_working_hours is None:
            daily_working_hours = defaults.daily_working_hours

        if not isinstance(daily_working_hours, int):
            raise TypeError(
                "{}.daily_working_hours should be an integer, not {}: '{}'".format(
                    self.__class__.__name__,
                    daily_working_hours.__class__.__name__,
                    daily_working_hours,
                )
            )

        if daily_working_hours <= 0 or daily_working_hours > 24:
            raise ValueError(
                f"{self.__class__.__name__}.daily_working_hours should be a positive "
                "integer value greater than 0 and smaller than or equal to 24"
            )
        return daily_working_hours

    def split_in_to_working_hours(
        self, start: datetime.datetime, end: datetime.datetime
    ) -> List[datetime.datetime]:
        """Split the given start and end datetime objects in to working hours.

        Args:
            start (datetime.datetime): The start date and time.
            end (datetime.datetime): The end date and time.

        Raises:
            NotImplementedError: Unless this is implemented.
        """
        raise NotImplementedError()


class Vacation(SimpleEntity, DateRangeMixin):
    """Vacation is the way to manage the User vacations.

    Args:
        user (User): The user of this vacation. Should be an instance of
            :class:`.User` if skipped or given as None the Vacation is considered
            as a Studio vacation and applies to all Users.

        start (datetime.datetime): The start datetime of the vacation. Is is an
            datetime.datetime instance. When skipped it will be set to the rounded
            value of.

        end (datetime.datetime): The end datetime of the vacation. It is an
            datetime.datetime instance.
    """

    __auto_name__ = True
    __tablename__ = "Vacations"
    __mapper_args__ = {"polymorphic_identity": "Vacation"}

    __strictly_typed__ = False

    vacation_id: Mapped[int] = mapped_column(
        "id", ForeignKey("SimpleEntities.id"), primary_key=True
    )

    user_id: Mapped[Optional[int]] = mapped_column("user_id", ForeignKey("Users.id"))

    user: Mapped[User] = relationship(
        primaryjoin="Vacations.c.user_id==Users.c.id",
        back_populates="vacations",
        doc="""The User of this Vacation.

        Accepts :class:`.User` instance.
        """,
    )

    def __init__(
        self,
        user: Optional[User] = None,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        kwargs["start"] = start
        kwargs["end"] = end
        super(Vacation, self).__init__(**kwargs)
        DateRangeMixin.__init__(self, **kwargs)
        self.user = user

    @validates("user")
    def _validate_user(self, key: str, user: User) -> User:
        """Validate the given user instance.

        Args:
            key (str): The name of the validated column.
            user (User): The user value to be validated.

        Raises:
            TypeError: If the user value is not None and not a
                :class:`stalker.models.auth.User` instance.

        Returns:
            User: The validated user value.
        """
        if user is not None and not isinstance(user, User):
            raise TypeError(
                "{}.user should be an instance of stalker.models.auth.User, "
                "not {}: '{}'".format(
                    self.__class__.__name__, user.__class__.__name__, user
                )
            )
        return user

    @property
    def to_tjp(self) -> str:
        """Override the to_tjp method.

        Returns:
            str: The rendered tjp template.
        """
        tjp = "vacation "
        tjp += f"{self.start.astimezone(pytz.utc).strftime('%Y-%m-%d-%H:%M:%S')} - "
        tjp += f"{self.end.astimezone(pytz.utc).strftime('%Y-%m-%d-%H:%M:%S')}"
        return tjp
