# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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

import copy
import logging
import time
import datetime
from math import ceil

from sqlalchemy import (Column, Integer, ForeignKey, Interval, Boolean,
                        DateTime, PickleType)
from sqlalchemy.orm import validates, relationship, synonym, reconstructor

from stalker import db, defaults, log
from stalker.models.entity import SimpleEntity, Entity
from stalker.models.mixins import DateRangeMixin, WorkingHoursMixin
from stalker.models.schedulers import SchedulerBase

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


class Studio(Entity, DateRangeMixin, WorkingHoursMixin):
    """Manage all the studio information at once.

    With Stalker you can manage all you Studio data by using this class. Studio
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

    :param int daily_working_hours: An integer specifying the daily working
      hours for the studio. It is another critical value attribute which
      TaskJuggler uses mainly converting working day values to working hours
      (1d = 10h kind of thing).

    :param now: The now attribute overrides the TaskJugglers ``now`` attribute
      allowing the user to schedule the projects as if the scheduling is done
      on that date. The default value is the rounded value of
      datetime.datetime.now().

    :type now: datetime.datetime

    :param timing_resolution: The timing_resolution of the datetime.datetime
      object in datetime.timedelta. Uses ``timing_resolution`` settings in the
      :class:`stalker.config.Config` class which defaults to 1 hour. Setting
      the timing_resolution to less then 5 minutes is not suggested because it
      is a limit for TaskJuggler.

    :type timing_resolution: datetime.timedelta

    """
    __auto_name__ = False
    __tablename__ = 'Studios'
    __mapper_args__ = {'polymorphic_identity': 'Studio'}

    studio_id = Column(
        'id',
        Integer,
        ForeignKey('Entities.id'),
        primary_key=True,
    )

    _timing_resolution = Column("timing_resolution", Interval)

    is_scheduling = Column(Boolean, default=False)
    is_scheduling_by_id = Column(
        Integer,
        ForeignKey('Users.id'),
        doc='The id of the user who is scheduling the Studio projects right '
            'now'
    )
    is_scheduling_by = relationship(
        'User',
        primaryjoin='Studios.c.is_scheduling_by_id==Users.c.id',
        doc='The User who is scheduling the Studio projects right now'
    )
    scheduling_started_at = Column(
        DateTime,
        doc='Stores when the current scheduling is started at, it is a good '
            'measure for measuring if the last schedule is not correctly '
            'finished'
    )
    last_scheduled_at = Column(
        DateTime,
        doc='Stores the last schedule date'
    )
    last_scheduled_by_id = Column(
        Integer,
        ForeignKey('Users.id'),
        doc='The id of the user who has last scheduled the Studio projects'
    )
    last_scheduled_by = relationship(
        'User',
        primaryjoin='Studios.c.last_scheduled_by_id==Users.c.id',
        doc='The User who has last scheduled the Studio projects'
    )
    last_schedule_message = Column(
        PickleType,
        doc='Holds the last schedule message, generally coming generated by '
        'TaskJuggler'
    )

    def __init__(self,
                 daily_working_hours=None,
                 now=None,
                 timing_resolution=None,
                 **kwargs):
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
    def daily_working_hours(self):
        """a shortcut for Studio.working_hours.daily_working_hours
        """
        return self.working_hours.daily_working_hours

    @daily_working_hours.setter
    def daily_working_hours(self, dwh):
        """a shortcut for Studio.working_hours.daily_working_hours
        """
        self.working_hours.daily_working_hours = dwh

    def update_defaults(self):
        """updates the default values with the studio
        """
        # TODO: add update_defaults() to attribute edit/update methods,
        #       so we will always have an up to date info about the working
        #       hours.

        logger.debug('updating defaults with Studio instance')
        from stalker import defaults
        try:
            if self.daily_working_hours:
                defaults.daily_working_hours = self.daily_working_hours
                logger.debug(
                    'updated defaults.daily_working_hours: %s' %
                    defaults.daily_working_hours
                )
            else:
                logger.debug('can not update defaults.daily_working_hours')
        except AttributeError:
            # The Studio and WorkingHours classes has changed from
            # v0.2.3 to v0.2.5 and with this change it is simply
            # no possible to initialize the db if we insist to update the
            # defaults for daily_working_hours, because there is no
            # WorkingHours._daily_working_hours in versions before than
            # v0.2.5, so just skip it for at least the studio instance
            # in the database has been updated.
            logger.debug(
                'Can not update defaults.daily_working_hours, WorkingHours '
                'version mismatch'
            )

        if self.weekly_working_days:
            defaults.weekly_working_days = self.weekly_working_days
            logger.debug(
                'updated defaults.weekly_working_days: %s' %
                defaults.weekly_working_days
            )
        else:
            logger.debug('can not update defaults.weekly_working_days')

        if self.weekly_working_hours:
            defaults.weekly_working_hours = self.weekly_working_hours
            logger.debug(
                'updated defaults.weekly_working_hours: %s' %
                defaults.weekly_working_hours
            )
        else:
            logger.debug('can not update defaults.weekly_working_hours')

        if self.yearly_working_days:
            defaults.yearly_working_days = self.yearly_working_days
            logger.debug(
                'updated defaults.yearly_working_days: %s' %
                defaults.yearly_working_days
            )
        else:
            logger.debug('can not update defaults.yearly_working_days')

        if self.timing_resolution:
            defaults.timing_resolution = self.timing_resolution
            logger.debug(
                'updated defaults.timing_resolution: %s' %
                defaults.timing_resolution
            )
        else:
            logger.debug('can not update defaults.timing_resolution')

        logger.debug("""done updating defaults:
        daily_working_hours  : %(daily_working_hours)s
        weekly_working_days  : %(weekly_working_days)s
        weekly_working_hours : %(weekly_working_hours)s
        yearly_working_days  : %(yearly_working_days)s
        timing_resolution    : %(timing_resolution)s
        """ % {
            'daily_working_hours': defaults.daily_working_hours,
            'weekly_working_days': defaults.weekly_working_days,
            'weekly_working_hours': defaults.weekly_working_hours,
            'yearly_working_days': defaults.yearly_working_days,
            'timing_resolution': defaults.timing_resolution,
        })

    @reconstructor
    def __init_on_load__(self):
        """update defaults on load
        """
        self.update_defaults()

    def _validate_now(self, now_in):
        """validates the given now_in value
        """
        if now_in is None:
            now_in = datetime.datetime.now()

        if not isinstance(now_in, datetime.datetime):
            raise TypeError(
                '%s.now attribute should be an instance of datetime.datetime, '
                'not %s' %
                (self.__class__.__name__, now_in.__class__.__name__)
            )

        return self.round_time(now_in)

    @property
    def now(self):
        """now getter
        """
        try:
            if self._now is None:
                self._now = self.round_time(datetime.datetime.now())
        except AttributeError:
            setattr(self, '_now', self.round_time(datetime.datetime.now()))
        return self._now

    @now.setter
    def now(self, now_in):
        """now setter
        """
        self._now = self._validate_now(now_in)

    def _validate_scheduler(self, scheduler_in):
        """validates the given scheduler_in value
        """
        if scheduler_in is not None:
            if not isinstance(scheduler_in, SchedulerBase):
                raise TypeError(
                    '%s.scheduler should be an instance of '
                    'stalker.models.scheduler.SchedulerBase, not %s' %
                    (self.__class__.__name__, scheduler_in.__class__.__name__)
                )
        return scheduler_in

    @property
    def scheduler(self):
        """scheduler getter
        """
        return self._scheduler

    @scheduler.setter
    def scheduler(self, scheduler_in):
        """the scheduler setter
        """
        self._scheduler = self._validate_scheduler(scheduler_in)

    @property
    def to_tjp(self):
        """converts the studio to a tjp representation
        """
        from jinja2 import Template

        temp = Template(
            defaults.tjp_studio_template,
            trim_blocks=True,
            lstrip_blocks=True
        )
        start = time.time()
        rendered_template = temp.render({
            'studio': self,
            'datetime': datetime,
            'now': self.round_time(self.now).strftime('%Y-%m-%d-%H:%M')
        })
        end = time.time()
        logger.debug('render studio to tjp took: %s seconds' % (end - start))
        return rendered_template

    @property
    def projects(self):
        """returns all the projects in the studio
        """
        from stalker import Project
        return Project.query.all()

    @property
    def active_projects(self):
        """returns all the active projects in the studio
        """
        from stalker import Project
        return Project.query.filter_by(active=True).all()

    @property
    def inactive_projects(self):
        """return all the inactive projects in the studio
        """
        from stalker import Project
        return Project.query.filter_by(active=False).all()

    @property
    def departments(self):
        """returns all the departments in the studio
        """
        from stalker import Department
        return Department.query.all()

    @property
    def users(self):
        """returns all the users in the studio
        """
        from stalker import User
        return User.query.all()

    @property
    def vacations(self):
        """returns all Vacations which doesn't have a User defined
        """
        return Vacation.query.filter(Vacation.user==None).all()

    def schedule(self, scheduled_by=None):
        """Schedules all the active projects in the studio. Needs a Scheduler,
        so before calling it set a scheduler by using the :attr:`.scheduler`
        attribute.

        :param scheduled_by: A User instance who is doing the scheduling.
        """
        # check the scheduler first
        if self.scheduler is None or \
                not isinstance(self.scheduler, SchedulerBase):
            raise RuntimeError(
                'There is no scheduler for this %(class)s, please assign a '
                'scheduler to the %(class)s.scheduler attribute, before '
                'calling %(class)s.schedule()' %
                {
                    'class': self.__class__.__name__
                }
            )

        with db.DBSession.no_autoflush:
            self.scheduling_started_at = datetime.datetime.now()

            # run the scheduler
            self.scheduler.studio = self
        start = time.time()

        # commit before scheduling
        #DBSession.commit()

        result = None
        try:
            result = self.scheduler.schedule()
        finally:
            # in any case set is_scheduling to False
            with db.DBSession.no_autoflush:
                self.is_scheduling = False
                self.is_scheduling_by = None

                # also store the result
                # if result:
                self.last_schedule_message = result

                # And the date the schedule is completed
                # TODO: convert to UTC time
                self.last_scheduled_at = datetime.datetime.now()

                # and who has done the scheduling
                if scheduled_by:
                    logger.debug(
                        'setting last_scheduled_by to : %s' % scheduled_by
                    )
                    self.last_scheduled_by = scheduled_by

        end = time.time()
        logger.debug('scheduling took %s seconds' % (end - start))
        return result

    @property
    def weekly_working_hours(self):
        """returns the WorkingHours.weekly_working_hours
        """
        return self.working_hours.weekly_working_hours

    @property
    def weekly_working_days(self):
        """returns the WorkingHours.weekly_working_hours
        """
        return self.working_hours.weekly_working_days

    @property
    def yearly_working_days(self):
        """returns the yearly working days
        """
        return self.working_hours.yearly_working_days

    def to_unit(self, from_timing, from_unit, to_unit, working_hours=True):
        """converts the given timing and unit to the desired unit
        if working_hours=True then the given timing is considered as working
        hours
        """
        raise NotImplementedError('this is not implemented yet')

    def _timing_resolution_getter(self):
        """returns the timing_resolution
        """
        return self._timing_resolution

    def _timing_resolution_setter(self, res_in):
        """sets the timing_resolution
        """
        self._timing_resolution = self._validate_timing_resolution(res_in)
        logger.debug('self._timing_resolution: %s' % self._timing_resolution)
        # update date values
        if self.start and self.end and self.duration:
            self._start, self._end, self._duration = \
                self._validate_dates(
                    self.round_time(self.start),
                    self.round_time(self.end),
                    None
                )

    timing_resolution = synonym(
        '_timing_resolution',
        descriptor=property(
            _timing_resolution_getter,
            _timing_resolution_setter,
            doc="""The timing_resolution of this object.

            Can be set to any value that is representable with
            datetime.timedelta. The default value is 1 hour. Whenever it is
            changed the start, end and duration values will be updated.
            """
        )
    )

    def _validate_timing_resolution(self, timing_resolution):
        """validates the given timing_resolution value
        """
        if timing_resolution is None:
            timing_resolution = defaults.timing_resolution

        if not isinstance(timing_resolution, datetime.timedelta):
            raise TypeError(
                '%s.timing_resolution should be an instance of '
                'datetime.timedelta not, %s' %
                (self.__class__.__name__, timing_resolution.__class__.__name__)
            )

        return timing_resolution


class WorkingHours(object):
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

    :param working_hours: The dictionary that shows the working hours. The keys
      of the dictionary should be one of ['mon', 'tue', 'wed', 'thu', 'fri',
      'sat', 'sun']. And the values should be a list of two integers like
      [[int, int], [int, int], ...] format, showing the minutes after midnight.
      For missing days the default value will be used. If skipped the default
      value is going to be used.
    """

    def __init__(self,
                 working_hours=None,
                 daily_working_hours=None,
                 **kwargs):
        if working_hours is None:
            working_hours = defaults.working_hours
        self._wh = None
        self.working_hours = self._validate_working_hours(working_hours)
        self._daily_working_hours = None
        self.daily_working_hours = daily_working_hours

    def __eq__(self, other):
        """overridden equality operator
        """
        return isinstance(other, WorkingHours) and \
            other.working_hours == self.working_hours

    def __hash__(self):
        """the overridden __hash__ method
        """
        return hash(self.working_hours)

    def __getitem__(self, item):
        from stalker import __string_types__
        if isinstance(item, int):
            return self._wh[defaults.day_order[item]]
        elif isinstance(item, __string_types__):
            return self._wh[item]

    def __setitem__(self, key, value):
        self._validate_wh_value(value)
        from stalker import __string_types__
        if isinstance(key, int):
            self._wh[defaults.day_order[key]] = value
        elif isinstance(key, __string_types__):
            # check if key is in
            if key not in defaults.day_order:
                raise KeyError(
                    '%s accepts only %s as key, not %s' %
                    (self.__class__.__name__, defaults.day_order, key)
                )
            self._wh[key] = value

    def _validate_working_hours(self, wh_in):
        """validates the given working hours
        """
        if not isinstance(wh_in, dict):
            raise TypeError(
                '%s.working_hours should be a dictionary, not %s' %
                (self.__class__.__name__, wh_in.__class__.__name__)
            )

        for key in wh_in.keys():
            if not isinstance(wh_in[key], list):
                raise TypeError(
                    '%s.working_hours should be a dictionary with keys "mon, '
                    'tue, wed, thu, fri, sat, sun" and the values should a '
                    'list of lists of two integers like [[540, 720], [800, '
                    '1080]], not %s' %
                    (self.__class__.__name__, wh_in[key].__class__.__name__)
                )

            # validate item values
            self._validate_wh_value(wh_in[key])

        # update the default values with the supplied working_hour dictionary
        # copy the defaults
        wh_def = copy.copy(defaults.working_hours)
        # update them
        wh_def.update(wh_in)

        return wh_def

    @property
    def working_hours(self):
        """the getter of _wh
        """
        return self._wh

    @working_hours.setter
    def working_hours(self, wh_in):
        """the setter of _wh
        """
        self._wh = self._validate_working_hours(wh_in)

    def is_working_hour(self, check_for_date):
        """checks if the given datetime is in working hours

        :param datetime.datetime check_for_date: The time to check if it is a
          working hour
        """
        weekday_nr = check_for_date.weekday()
        hour = check_for_date.hour
        minute = check_for_date.minute

        time_from_midnight = hour * 60 + minute

        # check if the hour is inside the working hour ranges
        logger.debug('checking for: %s' % time_from_midnight)
        logger.debug('self[weekday_nr]: %s' % self[weekday_nr])
        for working_hour_groups in self[weekday_nr]:
            start = working_hour_groups[0]
            end = working_hour_groups[1]
            logger.debug('start       : %s' % start)
            logger.debug('end         : %s' % end)
            if start <= time_from_midnight < end:
                return True

        return False

    def _validate_wh_value(self, value):
        """validates the working hour value
        """
        err = '%s.working_hours value should be a list of lists of two ' \
              'integers between and the range of integers should be 0-1440, ' \
              'not %s'

        if not isinstance(value, list):
            raise TypeError(err % (self.__class__.__name__,
                                   value.__class__.__name__))

        for i in value:
            if not isinstance(i, list):
                raise TypeError(err % (self.__class__.__name__,
                                       i.__class__.__name__))

            # check list length
            if len(i) != 2:
                raise RuntimeError(err % (self.__class__.__name__, value))

            # check type
            if not isinstance(i[0], int) or not isinstance(i[1], int):
                raise TypeError(err % (self.__class__.__name__, value))

            # check range
            if i[0] < 0 or i[0] > 1440 or i[1] < 0 or i[1] > 1440:
                raise ValueError(err % (self.__class__.__name__, value))

        return value

    @property
    def to_tjp(self):
        """returns TaskJuggler representation of this object
        """
        # render the template
        from jinja2 import Template

        template = Template(defaults.tjp_working_hours_template)
        return template.render({'workinghours': self})

    @property
    def weekly_working_hours(self):
        """returns the total working hours in a week
        """
        weekly_working_hours = 0
        for i in range(0, 7):
            for start, end in self[i]:
                weekly_working_hours += (end - start)
        return weekly_working_hours / 60.0

    @property
    def weekly_working_days(self):
        """returns the weekly working days by looking at the working hours
        settings
        """
        wwd = 0
        for i in range(0, 7):
            if len(self[i]):
                wwd += 1
        return wwd

    @property
    def yearly_working_days(self):
        """returns the total working days in a year
        """
        return int(ceil(self.weekly_working_days * 52.1428))

    def _validate_daily_working_hours(self, dwh):
        """validates the given daily working hours value
        """
        if dwh is None:
            dwh = defaults.daily_working_hours

        if not isinstance(dwh, int):
            raise TypeError(
                '%s.daily_working_hours should be an integer, not %s' %
                (self.__class__.__name__, dwh.__class__.__name__)
            )

        if dwh <= 0 or dwh > 24:
            raise ValueError(
                '%s.daily_working_hours should be a positive integer value '
                'greater than 0 and smaller than or equal to 24'
            )
        return dwh

    @property
    def daily_working_hours(self):
        """getter for daily_working_hours attribute
        """
        return self._daily_working_hours

    @daily_working_hours.setter
    def daily_working_hours(self, dwh):
        """setter for daily_working_hours attribute
        """
        self._daily_working_hours = self._validate_daily_working_hours(dwh)

    def split_in_to_working_hours(self, start, end):
        """splits the given start and end datetime objects in to working hours
        """
        raise NotImplementedError()


class Vacation(SimpleEntity, DateRangeMixin):
    """Vacation is the way to manage the User vacations.

    :param user: The user of this vacation. Should be an instance of
      :class:`.User` if skipped or given as None the
      Vacation is considered as a Studio vacation and applies to all Users.

    :param start: The start datetime of the vacation. Is is an
      datetime.datetime instance. When skipped it will be set to the rounded
      value of.

    :param end: The end datetime of the vacation. It is an datetime.datetime
      instance.
    """
    __auto_name__ = True
    __tablename__ = 'Vacations'
    __mapper_args__ = {'polymorphic_identity': 'Vacation'}

    __strictly_typed__ = False

    vacation_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                         primary_key=True)

    user_id = Column('user_id', Integer, ForeignKey('Users.id'),
                     nullable=True)

    user = relationship(
        'User',
        primaryjoin='Vacations.c.user_id==Users.c.id',
        back_populates='vacations',
        doc="""The User of this Vacation.

        Accepts :class:`.User` instance.
        """
    )

    def __init__(self, user=None, start=None, end=None, **kwargs):
        kwargs['start'] = start
        kwargs['end'] = end
        super(Vacation, self).__init__(**kwargs)
        DateRangeMixin.__init__(self, **kwargs)
        self.user = user

    @validates('user')
    def _validate_user(self, key, user):
        """validates the given user instance
        """
        if user is not None:
            from stalker import User
            if not isinstance(user, User):
                raise TypeError(
                    '%s.user should be an instance of '
                    'stalker.models.auth.User, not %s' %
                    (self.__class__.__name__, user.__class__.__name__)
                )
        return user

    @property
    def to_tjp(self):
        """overridden to_tjp method
        """
        from jinja2 import Template

        template = Template(defaults.tjp_vacation_template)
        return template.render({'vacation': self})
