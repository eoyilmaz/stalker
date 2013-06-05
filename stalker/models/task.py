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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import datetime
import logging

from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import (Table, Column, Integer, ForeignKey, Boolean, Enum,
                        DateTime, Float)
from sqlalchemy.orm import relationship, validates, synonym, reconstructor

from stalker import defaults
from stalker.models import check_circular_dependency
from stalker.models.entity import Entity
from stalker.models.auth import User
from stalker.models.mixins import ScheduleMixin, StatusMixin, ReferenceMixin
from stalker.db import DBSession
from stalker.db.declarative import Base
from stalker.exceptions import OverBookedError, CircularDependencyError
from stalker.log import logging_level

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


# schedule constraints
CONSTRAINT_NONE = 0
CONSTRAINT_START = 1
CONSTRAINT_END = 2
CONSTRAINT_BOTH = 3


class TimeLog(Entity, ScheduleMixin):
    """Holds information about the uninterrupted time spend on a specific
    :class:`~stalker.models.task.Task` by a specific
    :class:`~stalker.models.auth.User`.
    
    It is so important to note that the TimeLog reports the uninterrupted time
    that is spent for a Task. Thus it doesn't care about the working time
    attributes like daily working hours, weekly working days or anything else.
    Again it is the uninterrupted time which is spent for a task.
    
    Entering a time log for 2 days will book the resource for 48 hours not,
    2 * daily working hours.
    
    TimeLogs are created per resource. It means, you need to record all the 
    works separately for each resource. So there is only one resource in a 
    TimeLog instance.
    
    A :class:`~stalker.models.task.TimeLog` instance needs to be initialized
    with a :class:`~stalker.models.task.Task` and a
    :class:`~stalker.models.auth.User` instances.
    
    Adding overlapping time log for a :class:`~stalker.models.auth.User` will
    raise a :class:`~stalker.errors.OverBookedError`.
    
    TimeLog instances automatically extends the
    :attr:`~stalker.models.task.Task.schedule_timing` of the assigned Task if
    the :attr:`~stalker.models.task.Task.total_logged_seconds` is getting
    bigger than the :attr:`~stalker.models.task.Task.schedule_timing` after
    this TimeLog.
    
    :param task: The :class:`~stalker.models.task.Task` instance that this
      time log belongs to.
    
    :param resource: The :class:`~stalker.models.auth.User` instance that this
      time log is created for.
    """
    __auto_name__ = True
    __tablename__ = "TimeLogs"
    __mapper_args__ = {"polymorphic_identity": "TimeLog"}
    time_log_id = Column("id", Integer, ForeignKey("Entities.id"),
                         primary_key=True)
    task_id = Column(Integer, ForeignKey("Tasks.id"), nullable=False)
    task = relationship(
        "Task",
        primaryjoin="TimeLogs.c.task_id==Tasks.c.id",
        uselist=False,
        back_populates="time_logs",
        doc="""The :class:`~stalker.models.task.Task` instance that this 
        time log is created for"""
    )

    resource_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    resource = relationship(
        "User",
        primaryjoin="TimeLogs.c.resource_id==Users.c.id",
        uselist=False,
        back_populates="time_logs",
        doc="""The :class:`~stalker.models.auth.User` instance that this 
        time_log is created for"""
    )

    def __init__(
            self,
            task=None,
            resource=None,
            start=None,
            end=None,
            duration=None,
            **kwargs):
        super(TimeLog, self).__init__(**kwargs)
        kwargs['start'] = start
        kwargs['end'] = end
        kwargs['duration'] = duration
        ScheduleMixin.__init__(self, **kwargs)
        self.resource = resource
        self.task = task

    def _expand_task_schedule_timing(self, task):
        """Expands the task schedule timing if necessary
        
        :param task: The task that is going to be adjusted
        """
        # do the schedule_timing expansion here
        total_seconds = self.duration.days * 86400 + self.duration.seconds
        remaining_seconds = task.remaining_seconds
        from stalker import Studio

        studio = None
        try:
            with DBSession.no_autoflush:
                studio = Studio.query.first()
        except UnboundExecutionError:
            pass
        
        data_source = studio if studio else defaults
        conversion_ratio = 1
        if task.schedule_unit == 'min':
            conversion_ratio = 60
        elif task.schedule_unit == 'h':
            conversion_ratio = 3600
        elif task.schedule_unit == 'd':
            conversion_ratio = data_source.daily_working_hours * 3600
        elif task.schedule_unit == 'w':
            conversion_ratio = data_source.weekly_working_hours * 3600
        elif task.schedule_unit == 'm':
            conversion_ratio = data_source.weekly_working_hours * 4 * 3600
        elif task.schedule_unit == 'y':
            conversion_ratio = data_source.yearly_working_days * \
                               data_source.daily_working_hours * 3600
        logger.debug('remaining_seconds : %s' % remaining_seconds)
        logger.debug('total_seconds     : %s' % total_seconds)
        logger.debug('conversion_ratio  : %s' % conversion_ratio)
        if remaining_seconds < total_seconds:
            # expand it
            # first convert the task.schedule_timing to hours (by using studio
            # or defaults)
            # then add the needed seconds as hours

            # do it normally
            task.schedule_timing = float(task.schedule_timing) + \
                                   float(
                                       total_seconds - remaining_seconds) / conversion_ratio

    @validates("task")
    def _validate_task(self, key, task):
        """validates the given task value
        """
        if not isinstance(task, Task):
            raise TypeError("%s.task should be an instance of "
                            "stalker.models.task.Task not %s" %
                            (self.__class__.__name__,
                             task.__class__.__name__))
        
        # adjust task schedule
        self._expand_task_schedule_timing(task)
        
        return task

    @validates("resource")
    def _validate_resource(self, key, resource):
        """validates the given resource value
        """

        if resource is None:
            raise TypeError("%s.resource can not be None" %
                            self.__class__.__name__)

        if not isinstance(resource, User):
            raise TypeError("%s.resource should be a "
                            "stalker.models.auth.User instance not %s" %
                            (self.__class__.__name__,
                             resource.__class__.__name__))

        # check for overbooking
        logger.debug('resource.time_logs: %s' % resource.time_logs)
        for time_log in resource.time_logs:
            logger.debug('time_log       : %s' % time_log)
            logger.debug('time_log.start : %s' % time_log.start)
            logger.debug('time_log.end   : %s' % time_log.end)
            logger.debug('self.start     : %s' % self.start)
            logger.debug('self.end       : %s' % self.end)
            
            if time_log != self:
                if time_log.start == self.start or \
                                time_log.end == self.end or \
                                        time_log.start < self.end < time_log.end or \
                                        time_log.start < self.start < time_log.end:
                    raise OverBookedError(
                        "The resource %s is overly booked with %s and %s" %
                        (resource, self, time_log),
                    )
        return resource

# TODO: Consider contracting a Task with TimeLogs, what will happen when the task has logged in time
# TODO: Check, what happens when a task has TimeLogs and will have child task later on, will it be ok with TJ
# TODO: Create a TimeLog/Resource view where each resource is in one row and we have the days and hours in columns, you can temporarily store the resource report of TJ in db
# TODO: Task with no resource can not have booking (I think this is automatically done already!)



def update_task_dates(func):
    """decorator that updates the date after the function finishes its job
    """

    def wrap(*args, **kwargs):
        # call the function as usual
        rvalue = func(*args, **kwargs)
        # update the dates
        task_class = args[0]
        args[0]._validate_dates(task_class.start, task_class.end, None)
        return rvalue

        # return decorated function

    return wrap


class Task(Entity, StatusMixin, ScheduleMixin, ReferenceMixin):
    """Manages Task related data.
    
    **Introduction**
    
    Tasks are the unit of work that should be accomplished to complete a
    :class:`~stalker.models.project.Project`.
    
    Stalker tries to follow the concepts stated in TaskJuggler_.
    
    .. _TaskJuggler : http://www.taskjuggler.org/
    
    .. note::
       .. versionadded:: 0.2.0:
       Parent-child relation in Tasks

       Tasks can now have child Tasks. So you can create complex relations of
       Tasks to comply with your project needs.
    
    .. note::
       .. versionadded:: 0.2.0:
          References in Tasks
       
       Tasks can now have References.
    
    **Initialization**
    
    A Task needs to be created with a Project instance. It is also valid if no
    project is supplied but there should be a parent Task passed to the parent
    argument. And it is also possible to pass both project and the parent task.
    
    Because it will create an ambiguity, Stalker will raise a RuntimeWarning,
    if both project and task are given and the owner project of the given
    parent task is different then the supplied project instance. But again
    Stalker will warn the user but will continue to use the task as the parent
    and will correctly use the project of the given task as the project of the
    newly created task.
    
    The following codes are a couple of examples for creating Task instances::
      
      # with a project instance
      task1 = Task(name='Schedule', project=proj1)
      
      # with a parent task
      task2 = Task(name='Documentation', parent=task1)
      
      # or both
      task3 = Task(name='Test', project=proj1, parent=task1)
      
      # this will create a RuntimeWarning
      task4 = Task(name='Test', project=proj2, parent=task1) # task1 is not a
                                                             # task of proj2
      assert task4.project == proj1 # Stalker uses the task1.project for task4
      
      # this will also create a RuntimeError
      task3 = Task(name='Failure 2') # no project no parent, this is an orphan
                                     # task.
    
    Also initially Stalker will pin point the :attr:`.start` value and then
    will calculate proper :attr:`.end` and :attr:`.duration` values by using
    the :attr:`.schedule_timing` and :attr:`.schedule_unit` attributes. But
    these values (start, end and duration) are temporary values for an
    unscheduled task. The final date values will be calculated by TaskJuggler
    in the `auto scheduling` phase.
    
    **Auto Scheduling**
    
    Stalker uses TaskJuggler for task scheduling. After defining all the tasks,
    Stalker will convert them to a single tjp file along with the recorded
    :class:`~stalker.models.task.TimeLog`\ s and let TaskJuggler to solve the
    scheduling problem.
    
    During the auto scheduling (with TaskJuggler), the calculation of task
    duration, start and end dates are effected by the working hours setting of
    the :class:`~stalker.models.studio.Studio`, the effort that needs to spend
    for that task and the availability of the resources assigned to the task.
    
    A good practice for creating a project plan is to supply the parent/child
    and dependency relation between tasks and the effort and resource
    information per task and leave the start and end date calculation to
    TaskJuggler. It is also possible to use the ``length`` or ``duration``
    values (set :attr:`.schedule_model` to 'effort', 'length' or 'duration' to
    get the desired scheduling model).
    
    The default :attr:`.schedule_model` for Stalker tasks is 'effort`, the
    default :attr:`.schedule_unit` is ``hour`` and the default value of
    :attr:`.schedule_timing` is defined by the
    :attr:`stalker.config.Config.timing_resolution`. So for a
    config where the ``timing_resolution`` is set to 1 hour the schedule_timing
    is 1.
    
    To convert a Task instance to a TaskJuggler compatible string use the
    :attr:`.to_tjp`` attribute. It will try to create a good representation of
    the Task by using the resources, schedule_model, schedule_timing and
    schedule_constraint attributes.
    
    **Task/Task Relation**
    
    A Task is called a ``container task`` if it has at least one child Task.
    And it is called a ``leaf task`` if it doesn't have any children Tasks.
    Task which doesn't have a parent called ``root_task``.
    
    The resources in a container task is meaningless, cause the resources are
    defined by the child tasks (Dev Note: this can still be used to populate
    the resource information to the children tasks as in TaskJuggler).
    
    Although the values are not very important after TaskJuggler schedules a
    task, the :attr:`~.start` and :attr:`~.end` values for a container
    task is gathered from the child tasks. The start is equal to the earliest
    start value of the children tasks, and the end is equal to the latest end
    value of the children tasks. Of course, these values are going to be
    ignored by the TaskJuggler, but for interactive gantt charts these are good
    toy attributes to play with.
    
    Stalker will check if there will be a cycle if one wants to parent a Task
    to a child Task of its own or the dependency relation creates a cycle.
    
    In Gantt Charts the ``computed_start`` and ``computed_end`` attributes will
    be used if the task :attr:`.is_scheduled`.
    
    :param parent: The parent Task or Project of this Task. Every Task in
      Stalker should be related with a :class:`~stalker.models.project.Project`
      instance. So if no parent task is desired, at least a Project instance
      should be passed as the parent of the created Task or the Task will be an
      orphan task and Stalker will raise a RuntimeError.
    
    :param int priority: It is a number between 0 to 1000 which defines the
      priority of the :class:`~stalker.models.task.Task`. The higher the value
      the higher its priority. The default value is 500.
    
    :param resources: The :class:`~stalker.models.auth.User`\ s assigned to
      this :class:`~stalker.models.task.Task`. A
      :class:`~stalker.models.task.Task` without any resource can not be
      scheduled.
    
    :type resources: list of :class:`~stalker.User`
    
    :param int bid_timing: The initial bid for this Task. It can be used in
      measuring how accurate the initial guess was. It will be compared against
      the total amount of effort spend doing this task. Can be set to None,
      which will be set to the schedule_timing_day argument value if there is
      one or 0.
    
    :param str bid_unit: The unit of the bid value for this Task. Should be one
      of the 'min', 'h', 'd', 'w', 'm', 'y'.
        
    :param depends: A list of :class:`~stalker.models.task.Task`\ s that this
      :class:`~stalker.models.task.Task` is depending on. A Task can not depend
      to itself or any other Task which are already depending to this one in
      anyway or a CircularDependency error will be raised.
    
    :type depends: list of :class:`~stalker.models.task.Task`
    
    :param int schedule_timing: The value of the schedule timing.
    
    :param str schedule_unit: The unit value of the schedule timing. Should be
      one of 'min', 'h', 'd', 'w', 'm', 'y'.
    
    :param int schedule_constraint: The schedule constraint. It is the index
      of the schedule constraints value in
      :class:`stalker.config.Config.task_schedule_constraints`.
    
    :param bool milestone: A bool (True or False) value showing if this task is
      a milestone which doesn't need any resource and effort.
    """
    __auto_name__ = False
    __tablename__ = "Tasks"
    __mapper_args__ = {'polymorphic_identity': "Task"}
    task_id = Column("id", Integer, ForeignKey('Entities.id'),
                     primary_key=True)

    project_id = Column('project_id', Integer, ForeignKey('Projects.id'),
                        nullable=True)
    _project = relationship(
        'Project',
        primaryjoin='Tasks.c.project_id==Projects.c.id',
        back_populates='tasks',
        uselist=False,
        post_update=True,
    )

    parent_id = Column('parent_id', Integer, ForeignKey('Tasks.id'))
    parent = relationship(
        'Task',
        remote_side=[task_id],
        primaryjoin='Tasks.c.parent_id==Tasks.c.id',
        back_populates='children',
        post_update=True
    )

    children = relationship(
        'Task',
        primaryjoin='Tasks.c.parent_id==Tasks.c.id',
        back_populates='parent',
        post_update=True
    )

    tasks = synonym('children')

    is_milestone = Column(
        Boolean,
        doc="""Specifies if this Task is a milestone.
        
        Milestones doesn't need any duration, any effort and any resources. It
        is used to create meaningful dependencies between the critical stages
        of the project.
        """
    )

    # UPDATE THIS: is_complete should look to Task.status, but it is may be
    # faster to query in this way, judge later
    is_complete = Column(
        Boolean,
        doc="""A bool value showing if this task is completed or not.
        
        There is a good article_ about why not to use an attribute called
        ``percent_complete`` to measure how much the task is completed.
        
        .. _article: http://www.pmhut.com/how-percent-complete-is-that-task-again
        """
    )

    depends = relationship(
        "Task",
        secondary="Task_Dependencies",
        primaryjoin="Tasks.c.id==Task_Dependencies.c.task_id",
        secondaryjoin="Task_Dependencies.c.depends_to_task_id==Tasks.c.id",
        backref="dependent_of",
        doc="""A list of :class:`~stalker.models.task.Task`\ s that this one is depending on.
        
        A CircularDependencyError will be raised when the task dependency
        creates a circular dependency which means it is not allowed to create
        a dependency for this Task which is depending on another one which in
        some way depends to this one again.
        """
    )

    resources = relationship(
        "User",
        secondary="Task_Resources",
        primaryjoin="Tasks.c.id==Task_Resources.c.task_id",
        secondaryjoin="Task_Resources.c.resource_id==Users.c.id",
        #backref="tasks",
        back_populates="tasks",
        doc="""The list of :class:`~stalker.models.auth.User`\ s assigned to this Task.
        """
    )
    
    watchers = relationship(
        'User',
        secondary='Task_Watchers',
        primaryjoin='Tasks.c.id==Task_Watchers.c.task_id',
        secondaryjoin='Task_Watchers.c.watcher_id==Users.c.id',
        back_populates='watching',
        doc='''The list of :class:`~stalker.models.auth.User`\ s watching this Task.
        '''
    )

    priority = Column(Integer)

    time_logs = relationship(
        "TimeLog",
        primaryjoin="TimeLogs.c.task_id==Tasks.c.id",
        back_populates="task",
        doc="""A list of :class:`~stalker.models.task.TimeLog` instances showing who and when spent how much effort on this task.
        """
    )

    versions = relationship(
        "Version",
        primaryjoin="Versions.c.version_of_id==Tasks.c.id",
        back_populates="version_of",
        doc="""A list of :class:`~stalker.models.version.Version` instances showing the files created for this task.
        """
    )

    #_start = Column('start', DateTime)
    #_end = Column('end', DateTime)

    computed_start = Column(DateTime)
    computed_end = Column(DateTime)

    bid_timing = Column(
        Float, nullable=True, default=0,
        doc="""The value of the initial bid of this Task. It is an integer or
        a float.
        """
    )

    bid_unit = Column(
        Enum(*defaults.datetime_units, name='TaskBidUnit'),
        nullable=True,
        doc="""The unit of the initial bid of this Task. It is a string value.
        And should be one of 'min', 'h', 'd', 'w', 'm', 'y'.
        """
    )

    schedule_timing = Column(
        Float, nullable=True, default=0,
        doc="""It is the value of the schedule timing. It is a float value.
        """
    )

    schedule_unit = Column(
        Enum(*defaults.datetime_units, name='TaskScheduleUnit'),
        nullable=False, default='h',
        doc="""It is the unit of the schedule timing. It is a string value. And
        should be one of 'min', 'h', 'd', 'w', 'm', 'y'.
        """
    )

    schedule_model = Column(
        Enum(*defaults.task_schedule_models, name='TaskScheduleModels'),
        default=defaults.task_schedule_models[0], nullable=False
    )

    schedule_constraint = Column(Integer, default=0, nullable=False)

    def __init__(self,
                 project=None,
                 parent=None,
                 depends=None,
                 resources=None,
                 watchers=None,
                 start=None,
                 end=None,
                 duration=None,
                 schedule_timing=None,
                 schedule_unit='h',
                 schedule_model=None,
                 schedule_constraint=0,
                 bid_timing=None,
                 bid_unit=None,
                 is_milestone=False,
                 priority=defaults.task_priority,
                 **kwargs):

        # update kwargs with extras
        kwargs['start'] = start
        kwargs['end'] = end
        kwargs['duration'] = duration

        super(Task, self).__init__(**kwargs)

        # call the mixin __init__ methods
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)

        self.parent = parent
        self._project = project

        self.time_logs = []
        self.versions = []

        self.is_milestone = is_milestone
        self.is_complete = False

        if depends is None:
            depends = []

        self.depends = depends

        if self.is_milestone:
            resources = None

        if resources is None:
            resources = []
        self.resources = resources
        
        if watchers is None:
            watchers = []
        self.watchers = watchers
        
        self.schedule_constraint = schedule_constraint
        self.schedule_unit = schedule_unit
        self.schedule_timing = schedule_timing

        self.schedule_model = schedule_model

        if bid_timing is None:
            bid_timing = self.schedule_timing

        if bid_unit is None:
            bid_unit = self.schedule_unit

        self.bid_timing = bid_timing
        self.bid_unit = bid_unit
        self.priority = priority

    @reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        # TODO : fix this
        tmp = self.start # just read the start to update them
        self._reschedule(self.schedule_timing, self.schedule_unit)
        # call supers __init_on_load__
        super(Task, self).__init_on_load__()

    def __eq__(self, other):
        """the equality operator
        """
        return super(Task, self).__eq__(other) and isinstance(other, Task) \
        and self.parent == other.parent and self.depends == other.depends \
        and self.children == other.children
    

    @validates("time_logs")
    def _validate_time_logs(self, key, time_log):
        """validates the given time_logs value
        """
        if not isinstance(time_log, TimeLog):
            raise TypeError(
                "all the elements in the %s.time_logs should be an instances "
                "of stalker.models.task.TimeLog not %s instance" %
                (self.__class__.__name__, time_log.__class__.__name__))

        return time_log

    @validates("is_complete")
    def _validate_is_complete(self, key, complete_in):
        """validates the given complete value
        """
        return bool(complete_in)

    @validates("depends")
    def _validate_depends(self, key, depends):
        """validates the given depends value
        """
        if not isinstance(depends, Task):
            raise TypeError("all the elements in the depends should be an "
                            "instance of stalker.models.task.Task")

        # check for the circular dependency
        check_circular_dependency(depends, self, 'depends')
        check_circular_dependency(depends, self, 'children')

        # check for circular dependency toward the parent, non of the parents
        # should be depending to the given depends_to_task
        with DBSession.no_autoflush:
            parent = self.parent
            while parent:
                if parent in depends.depends:
                    raise CircularDependencyError(
                        'One of the parents of %s is '
                        'depending to %s' %
                        (self, depends))
                parent = parent.parent
        return depends

    @validates('schedule_timing')
    def _validate_schedule_timing(self, key, schedule_timing):
        """validates the given schedule_timing
        """
        if schedule_timing is None:
            schedule_timing = defaults.timing_resolution.seconds / 3600
            self.schedule_unit = 'h'

        if not isinstance(schedule_timing, (int, float)):
            raise TypeError(
                '%s.schedule_timing should be an integer or float number'
                'showing the value of the timing of this %s, not %s' % (
                    self.__class__.__name__, self.__class__.__name__,
                    schedule_timing.__class__.__name__)
            )

        # reschedule
        self._reschedule(schedule_timing, self.schedule_unit)

        return schedule_timing

    @validates('schedule_unit')
    def _validate_schedule_unit(self, key, schedule_unit):
        """validates the given schedule_unit
        """
        if schedule_unit is None:
            schedule_unit = 'h'

        if not isinstance(schedule_unit, (str, unicode)):
            raise TypeError(
                '%s.schedule_unit should be a string value one of %s showing '
                'the unit of the schedule timing of this %s, not %s' % (
                    self.__class__.__name__, defaults.datetime_units,
                    self.__class__.__name__, schedule_unit.__class__.__name__)
            )

        if schedule_unit not in defaults.datetime_units:
            raise ValueError(
                '%s.schedule_unit should be a string value one of %s showing '
                'the unit of the schedule timing of this %s, not %s' % (
                    self.__class__.__name__, defaults.datetime_units,
                    self.__class__.__name__, schedule_unit.__class__.__name__)
            )

        if self.schedule_timing:
            self._reschedule(self.schedule_timing, schedule_unit)

        return schedule_unit
    
    @validates('schedule_model')
    def _validate_schedule_model(self, key, schedule_model):
        """validates the given schedule_model value
        """

        if not schedule_model:
            schedule_model = defaults.task_schedule_models[0]
        
        
        error_message = '%s.schedule_model should be one of %s, not %s' % (
            self.__class__.__name__, defaults.task_schedule_models,
            schedule_model.__class__.__name__
        )
        
        if not isinstance(schedule_model, (str, unicode)):
            raise TypeError(error_message)
        
        if schedule_model not in defaults.task_schedule_models:
            raise ValueError(error_message)

        return schedule_model

    def _reschedule(self, schedule_timing, schedule_unit):
        """Updates the start and end date values by using the schedule_timing
        and schedule_unit values.

        :param schedule_timing: An integer or float value showing the value of
          the schedule timing.
        :type schedule_timing: int, float
        :param str schedule_unit: one of 'min', 'h', 'd', 'w', 'm', 'y'
        """
        # update end date value by using the start and calculated duration
        if self.is_leaf:
            unit = defaults.datetime_units_to_timedelta_kwargs.get(
                schedule_unit,
                None
            )
            if not unit: # we are in a pre flushing state do not do anything
                return

            kwargs = {
                unit['name']: schedule_timing * unit['multiplier']
            }
            calculated_duration = datetime.timedelta(**kwargs)
            if self.schedule_constraint == CONSTRAINT_NONE or \
                            self.schedule_constraint == CONSTRAINT_START:
                # get end
                self._validate_dates(self.start, None, calculated_duration)
            elif self.schedule_constraint == CONSTRAINT_END:
                # get start
                self._validate_dates(None, self.end, calculated_duration)
            elif self.schedule_constraint == CONSTRAINT_BOTH:
                # restore duration
                self._validate_dates(self.start, self.end, None)

    @validates("is_milestone")
    def _validate_is_milestone(self, key, is_milestone):
        """validates the given milestone value
        """
        if is_milestone:
            self.resources = []

        return bool(is_milestone)

    @validates('parent')
    def _validate_parent(self, key, parent):
        """validates the given parent value
        """
        if parent is not None:
            # if it is not a Task instance, go mad (cildir!!)
            if not isinstance(parent, Task):
                raise TypeError('%s.parent should be an instance of '
                                'stalker.models.task.Task, not '
                                'a %s' % (self.__class__.__name__,
                                          parent.__class__.__name__))

            # check for cycle
            check_circular_dependency(self, parent, 'children')
            check_circular_dependency(self, parent, 'depends')

        return parent

    @validates('_project')
    def _validates_project(self, key, project):
        """validates the given project instance
        """
        if project is None:
            # check if there is a parent defined
            if self.parent:
                # use its project as the project

                # to prevent prematurely flush the parent
                with DBSession.no_autoflush:
                    project = self.parent.project

            else:
                # no project, no task, go mad again!!!
                raise TypeError('%s.project should be an instance of '
                                'stalker.models.project.Project, not %s. Or '
                                'please supply a stalker.models.task.Task '
                                'with the parent argument, so Stalker can use '
                                'the project of the supplied parent task' %
                                (self.__class__.__name__,
                                 project.__class__.__name__))

        from stalker import Project

        if not isinstance(project, Project):
            # go mad again it is not a project instance
            raise TypeError('%s.project should be an instance of '
                            'stalker.models.project.Project, not %s' %
                            (self.__class__.__name__,
                             project.__class__.__name__))
        else:
            # check if there is a parent
            if self.parent:
                # check if given project is matching the parent.project
                with DBSession.no_autoflush:
                    if self.parent._project != project:
                        # don't go mad again, but warn the user that there is an
                        # ambiguity!!!
                        import warnings

                        message = 'The supplied parent and the project is not ' \
                                  'matching in %s, Stalker will use the parent ' \
                                  'project (%s) as the parent of this %s' % \
                                  (self,
                                   self.parent._project,
                                   self.__class__.__name__)

                        warnings.warn(message, RuntimeWarning)

                        # use the parent.project
                        project = self.parent._project
        return project

    @validates("priority")
    def _validate_priority(self, key, priority):
        """validates the given priority value
        """
        try:
            priority = int(priority)
        except (ValueError, TypeError):
            pass

        if not isinstance(priority, int):
            priority = defaults.task_priority

        if priority < 0:
            priority = 0
        elif priority > 1000:
            priority = 1000

        return priority

    @validates('children')
    def _validate_children(self, key, child):
        """validates the given child
        """
        # just empty the resources list
        # do it without a flush
        with DBSession.no_autoflush:
            self.resources = []

        return child

    @validates("resources")
    def _validate_resources(self, key, resource):
        """validates the given resources value
        """
        from stalker.models.auth import User

        if not isinstance(resource, User):
            raise TypeError("Task.resources should be a list of "
                            "stalker.models.auth.User instances not %s" %
                            resource.__class__.__name__)

            ## milestones do not need resources
            #if self.is_milestone:
            #resource = None

        return resource
    
    @validates("watchers")
    def _validate_watchers(self, key, watcher):
        """validates the given watcher value
        """
        from stalker.models.auth import User

        if not isinstance(watcher, User):
            raise TypeError("%s.watchers should be a list of "
                            "stalker.models.auth.User instances not %s" %
                            (self.__class__.__name__,
                             watcher.__class__.__name__))
        return watcher
    
    @validates("versions")
    def _validate_versions(self, key, version):
        """validates the given version value
        """
        from stalker.models.version import Version

        if not isinstance(version, Version):
            raise TypeError("Task.versions should only have "
                            "stalker.models.version.Version instances")

        return version

    @validates('bid_timing')
    def _validate_bid_timing(self, key, bid_timing):
        """validates the given bid_timing value
        """
        if bid_timing is not None:
            if not isinstance(bid_timing, (int, float)):
                raise TypeError(
                    '%s.bid_timing should be an integer or float showing the '
                    'value of the initial bid for this %s, not %s' %
                    (self.__class__.__name__, self.__class__.__name__,
                     bid_timing.__class__.__name__))
        return bid_timing

    @validates('bid_unit')
    def _validate_bid_unit(self, key, bid_unit):
        """validates the given bid_unit value
        """
        if bid_unit is None:
            bid_unit = 'h'

        if not isinstance(bid_unit, (str, unicode)):
            raise TypeError(
                '%s.bid_unit should be a string value one of %s showing '
                'the unit of the bid timing of this %s, not %s' % (
                    self.__class__.__name__, defaults.datetime_units,
                    self.__class__.__name__, bid_unit.__class__.__name__))

        if bid_unit not in defaults.datetime_units:
            raise ValueError(
                '%s.bid_unit should be a string value one of %s showing '
                'the unit of the bid timing of this %s, not %s' % (
                    self.__class__.__name__, defaults.datetime_units,
                    self.__class__.__name__, bid_unit.__class__.__name__))

        return bid_unit

    def _validate_start(self, start_in):
        """validates the given start value
        """
        if start_in is None:
            start_in = self.project.round_time(datetime.datetime.now())
        elif not isinstance(start_in, datetime.datetime):
            raise TypeError('%s.start should be an instance of '
                            'datetime.datetime, not %s' %
                            (self.__class__.__name__,
                             start_in.__class__.__name__))
        return start_in

    def _start_getter(self):
        """overridden start getter
        """
        # use children start
        if self.is_container:
            start = datetime.datetime.max
            for child in self.children:
                if child.start < start:
                    start = child.start
            self._validate_dates(start, self._end, self._duration)
        return self._start

    def _start_setter(self, start_in):
        """overridden start setter
        """
        # logger.debug('Task.start_setter       : %s' % start_in)
        # update the start only if this is not a container task
        if self.is_leaf:
            self._validate_dates(start_in, self._end, self._duration)

            # logger.debug('Task.start_setter afterV: %s' % self.start)

    def _end_getter(self):
        """overridden end getter
        """
        # TODO: do it only once not all the time they ask for it
        # use children end
        if self.is_container:
            end = datetime.datetime.min
            for child in self.children:
                if child.end > end:
                    end = child.end
            self._validate_dates(self._start, end, self._duration)
        return self._end

    def _end_setter(self, end_in):
        """overridden end setter
        """
        # update the end only if this is not a container task
        if self.is_leaf:
            self._validate_dates(self.start, end_in, self.duration)

    def _project_getter(self):
        return self._project

    project = synonym(
        '_project',
        descriptor=property(
            _project_getter
        ),
        doc="""The owner Project of this task.
        
        It is a read-only attribute. It is not possible to change the owner
        Project of a Task it is defined when the Task is created.
        """
    )

    @property
    def is_root(self):
        """Returns True if the Task has no parent
        """
        return not bool(self.parent)

    @property
    def is_container(self):
        """Returns True if the Task has children Tasks
        """
        return bool(len(self.children))

    @property
    def is_leaf(self):
        """Returns True if the Task has no children Tasks
        """
        return not bool(len(self.children))

    @property
    def parents(self):
        """Returns all of the parents of this Task starting from the root
        """
        parents = []
        task = self.parent
        while task:
            parents.append(task)
            task = task.parent
        parents.reverse()
        return parents

    @property
    def tjp_abs_id(self):
        """returns the calculated absolute id of this task
        """
        if self.parent:
            abs_id = self.parent.tjp_abs_id
        else:
            abs_id = self.project.tjp_id

        return abs_id + '.' + self.tjp_id

    @property
    def to_tjp(self):
        """TaskJuggler representation of this task
        """
        from jinja2 import Template

        temp = Template(defaults.tjp_task_template)
        return temp.render({'task': self})

    @property
    def level(self):
        """Returns the level of this task. It is a temporary property and will
        be useless when Stalker has its own implementation of a proper Gantt
        Chart. Write now it is used by the jQueryGantt.
        """
        i = 0
        current = self
        while current:
            i += 1
            current = current.parent
        return i

    @property
    def is_scheduled(self):
        """A predicate which returns True if this task has both a
        computed_start and computed_end values
        """
        return self.computed_start is not None and \
               self.computed_end is not None

    @property
    def total_logged_seconds(self):
        """The total effort spent for this Task. It is the sum of all the
        TimeLogs recorded for this task as seconds.

        :returns int: An integer showing the total seconds spent.
        """
        seconds = 0
        with DBSession.no_autoflush:
            for time_log in self.time_logs:
                seconds += time_log.total_seconds
        return seconds

    @property
    def schedule_seconds(self):
        """returns the total effort, length or duration in seconds, for
        completeness calculation
        """
        schedule_timing = self.schedule_timing
        schedule_model = self.schedule_model
        schedule_unit = self.schedule_unit
        from stalker import Studio

        try:
            with DBSession.no_autoflush:
                studio = Studio.query.first()
        except UnboundExecutionError:
            studio = None
        data_source = studio if studio else defaults

        if schedule_model == 'effort':
            if schedule_unit == 'min':
                return schedule_timing * 60

            elif schedule_unit == 'h':
                return schedule_timing * 3600

            elif schedule_unit == 'd':
                # we need to have a studio or defaults
                return schedule_timing * data_source.daily_working_hours * 3600

            elif schedule_unit == 'w':
                return schedule_timing * data_source.weekly_working_hours * 3600

            elif schedule_unit == 'm':
                return schedule_timing * 4 * data_source.weekly_working_hours * 3600

            elif schedule_unit == 'y':
                return schedule_timing * \
                       data_source.yearly_working_days * \
                       data_source.daily_working_hours * 3600

    @property
    def remaining_seconds(self):
        """returns the remaining amount of efforts, length or duration left
        in this Task as seconds.
        """
        # for effort based tasks use the time_logs
        return self.schedule_seconds - self.total_logged_seconds

# TASK_DEPENDENCIES
Task_Dependencies = Table(
    "Task_Dependencies", Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("depends_to_task_id", Integer, ForeignKey("Tasks.id"),
           primary_key=True)
)

# TASK_RESOURCES
Task_Resources = Table(
    "Task_Resources", Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("Users.id"), primary_key=True)
)

# TASK_WATCHERS
Task_Watchers = Table(
    "Task_Watchers", Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("watcher_id", Integer, ForeignKey("Users.id"), primary_key=True)
)


# TODO: subscribe to task: Users should be able to subscribe to any task they
#       want so they can be informed about the tickets as if they are a
#       resource for that task.
