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

import copy
import logging
import datetime
import time

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import validates, relationship

from stalker import defaults, log
from stalker.models.entity import SimpleEntity, Entity
from stalker.models.mixins import ScheduleMixin, WorkingHoursMixin
from stalker.models.schedulers import SchedulerBase

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


class Studio(Entity, ScheduleMixin, WorkingHoursMixin):
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

    You can define

    :param int daily_working_hours: An integer specifying the daily working
      hours for the studio. It is another critical value attribute which
      TaskJuggler uses mainly converting working day values to working hours
      (1d = 10h kind of thing).

    :param now: The now attribute overrides the TaskJugglers ``now`` attribute
      allowing the user to schedule the projects as if the scheduling is done
      on that date. The default value is the rounded value of
      datetime.datetime.now().

    :type now: datetime.datetime
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

    daily_working_hours = Column(Integer, default=8)

    def __init__(self,
                 daily_working_hours=None,
                 now=None,
                 **kwargs):
        super(Studio, self).__init__(**kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        WorkingHoursMixin.__init__(self, **kwargs)
        # TODO: daily_working_hours should be in WorkingHours not in Studio
        self.daily_working_hours = daily_working_hours
        self._now = None
        self.now = self._validate_now(now)
        self._scheduler = None

    # @reconstructor
    # def __init_on_load__(self):
    #     self._now = None
    #     super(Studio, self).__init_on_load__()

    @validates('daily_working_hours')
    def _validate_daily_working_hours(self, key, dwh):
        """validates the given daily working hours value
        """
        if dwh is None:
            dwh = defaults.daily_working_hours
        else:
            if not isinstance(dwh, int):
                raise TypeError('%s.daily_working_hours should be an integer, '
                                'not %s' %
                                (self.__class__.__name__,
                                 dwh.__class__.__name__))
        return dwh

    def _validate_now(self, now_in):
        """validates the given now_in value
        """
        if now_in is None:
            now_in = datetime.datetime.now()

        if not isinstance(now_in, datetime.datetime):
            raise TypeError('%s.now attribute should be an instance of '
                            'datetime.datetime, not %s' %
                            (self.__class__.__name__,
                             now_in.__class__.__name__))

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
                raise TypeError('%s.scheduler should be an instance of '
                                'stalker.models.scheduler.SchedulerBase, not '
                                '%s' % (self.__class__.__name__,
                                        scheduler_in.__class__.__name__))
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

        temp = Template(defaults.tjp_studio_template)
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

        return Project.query.filter(Project.active == True).all()

    @property
    def inactive_projects(self):
        """return all the inactive projects in the studio
        """
        from stalker import Project

        return Project.query.filter(Project.active == False).all()

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

    def schedule(self):
        """Schedules all the active projects in the studio. Needs a Scheduler,
        so before calling it set a scheduler by using the :attr:`.scheduler`
        attribute.
        """
        # check the scheduler first
        if self.scheduler is None or \
                not isinstance(self.scheduler, SchedulerBase):
            raise RuntimeError('There is no scheduler for this %s, please '
                               'assign a scheduler to the %s.scheduler '
                               'attribute, before calling %s.schedule()' %
                               (self.__class__.__name__,
                                self.__class__.__name__,
                                self.__class__.__name__))

        # run the scheduler
        self.scheduler.studio = self
        start = time.time()
        result = self.scheduler.schedule()
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

    def __init__(self, working_hours=None, **kwargs):
        if working_hours is None:
            working_hours = defaults.working_hours
        self._wh = None
        self.working_hours = self._validate_working_hours(working_hours)

    def __eq__(self, other):
        """equality test
        """
        return isinstance(other, WorkingHours) and \
               other.working_hours == self.working_hours

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._wh[defaults.day_order[item]]
        elif isinstance(item, str):
            return self._wh[item]

    def __setitem__(self, key, value):
        self._validate_wh_value(value)
        if isinstance(key, int):
            self._wh[defaults.day_order[key]] = value
        elif isinstance(key, str):
            # check if key is in
            if key not in defaults.day_order:
                raise KeyError('%s accepts only %s as key, not %s' %
                               (self.__class__.__name__, defaults.day_order,
                                key))
            self._wh[key] = value

    def _validate_working_hours(self, wh_in):
        """validates the given working hours
        """
        if not isinstance(wh_in, dict):
            raise TypeError('%s.working_hours should be a dictionary, not %s' %
                            (self.__class__.__name__,
                             wh_in.__class__.__name__))

        for key in wh_in.keys():
            if not isinstance(wh_in[key], list):
                raise TypeError('%s.working_hours should be a dictionary with '
                                'keys "mon, tue, wed, thu, fri, sat, sun" '
                                'and the values should a list of lists of '
                                'two integers like [[540, 720], [800, 1080]], '
                                'not %s' % (self.__class__.__name__,
                                            wh_in[key].__class__.__name__))

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
        return self.weekly_working_days * 52.1428


class Vacation(SimpleEntity, ScheduleMixin):
    """Vacation is the way to manage the User vacations.

    :param user: The user of this vacation. Should be an instance of
      :class:`~stalker.models.auth.User` if skipped or given as None the
      Vacation is considered as a Studio vacation and applies to all Users.

    :param start: The start datetime of the vacation. Is is an
      datetime.datetime instance. When skipped it will be set to the rounded
      value of 

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

        Accepts:class:`~stalker.models.auth.User` instance.
        """
    )

    def __init__(self, user=None, start=None, end=None, **kwargs):
        kwargs['start'] = start
        kwargs['end'] = end
        super(Vacation, self).__init__(**kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        self.user = user

    @validates('user')
    def _validate_user(self, key, user):
        """validates the given user instance
        """
        if user is not None:
            from stalker import User
            if not isinstance(user, User):
                raise TypeError('%s.user should be an instance of '
                                'stalker.models.auth.User, not %s' %
                                (self.__class__.__name__, user.__class__.__name__))
        return user

    @property
    def to_tjp(self):
        """overridden to_tjp method
        """
        from jinja2 import Template

        template = Template(defaults.tjp_vacation_template)
        return template.render({'vacation': self})
