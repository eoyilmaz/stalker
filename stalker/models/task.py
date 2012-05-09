# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import datetime
import logging
from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, Interval
from sqlalchemy.orm import relationship, validates, synonym, reconstructor
from stalker.conf import defaults
from stalker.db.declarative import Base
from stalker.errors import OverBookedWarning, CircularDependencyError
from stalker.models.entity import Entity
from stalker.models.mixins import ScheduleMixin, StatusMixin

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class Booking(Entity, ScheduleMixin):
    """Holds information about the time spend on a specific
    :class:`~stalker.core.models.Task` by a specific
    :class:`~stalker.core.models.User`.
    
    Bookings are created per resource. It means, you need to record all the 
    works separately for each resource. So there is only one resource in a 
    Booking instance, thus :attr:`~stalker.core.models.Booking.duration`
    attribute is equal to the meaning of ``effort``.
    
    A :class:`~stalker.core.models.Booking` instance needs to be initialized
    with a :class:`~stalker.core.models.Task` and a
    :class:`~stalker.core.models.User` instances.
    
    Adding overlapping booking for a :class:`~stalker.core.models.User` will
    raise a :class:`~stalker.core.errors.OverBookedWarning`.
    
    :param task: The :class:`~stalker.core.models.Task` instance that this
      booking belongs to.
    
    :param resource: The :class:`~stalker.core.models.User` instance that this
      booking is created for.
    """

    __tablename__ = "Bookings"
    __mapper_args__ = {"polymorphic_identity": "Booking"}
    booking_id = Column("id", Integer, ForeignKey("Entities.id"),
                        primary_key=True)
    task_id = Column(Integer, ForeignKey("Tasks.id"), nullable=False)
    task = relationship(
        "Task",
        primaryjoin="Bookings.c.task_id==Tasks.c.id",
        uselist=False,
        back_populates="bookings",
        doc="""The :class:`~stalker.core.models.Task` instance that this 
        booking is created for"""
    )

    resource_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    resource = relationship(
        "User",
        primaryjoin="Bookings.c.resource_id==Users.c.id",
        uselist=False,
        back_populates="bookings",
        doc="""The :class:`~stalker.core.models.User` instance that this booking
        is created for"""
    )

    def __init__(self, task=None, resource=None, **kwargs):
        super(Booking, self).__init__(**kwargs)
        ScheduleMixin.__init__(self, **kwargs)

        self.task = task
        self.resource = resource

    @validates("task")
    def _validate_task(self, key, task):
        """validates the given task value
        """

        if not isinstance(task, Task):
            raise TypeError("%s.task should be an instance of "
                            "stalker.core.models.Task not %s" %
                            (self.__class__.__name__,
                             task.__class__.__name__))

        return task

    @validates("resource")
    def _validate_resource(self, key, resource):
        """validates the given resource value
        """
        
        from stalker.models.user import User

        if resource is None:
            raise TypeError("%s.resource can not be None" %
                            self.__class__.__name__)

        if not isinstance(resource, User):
            raise TypeError("%s.resource should be a "
                            "stalker.core.models.User instance not %s" %
                            (self.__class__.__name__,
                             resource.__class__.__name__))
        
        # check for overbooking
        for booking in resource.bookings:
            logger.debug('booking.start_date: %s' % booking.start_date)
            logger.debug('self.start_date: %s' % self.start_date)

            if booking.start_date == self.start_date or\
               booking.due_date == self.due_date or\
               (self.due_date > booking.start_date and\
                self.due_date < booking.due_date) or\
               (self.start_date > booking.start_date and\
                self.start_date < booking.due_date):
                raise OverBookedWarning(
                    "The resource %s is overly booked with %s and %s" %
                    (resource, self, booking)
                )

        return resource


class Task(Entity, StatusMixin, ScheduleMixin):
    """Manages Task related data.
    
    Tasks are the smallest meaningful part that should be accomplished to
    complete the a :class:`~stalker.core.models.Project`.
    
    In Stalker, currently these items supports Tasks:
    
      * :class:`~stalker.core.models.Project`
      * :class:`~stalker.core.models.Sequence`
      * :class:`~stalker.core.models.Asset`
      * :class:`~stalker.core.models.Shot`
      * :class:`~stalker.core.models.TaskableEntity` itself and any class 
        which derives from :class:`~stalker.core.models.TaskableEntity`.
    
    If you want to have your own class to be *taskable* derive it from the
    :class:`~stalker.core.models.TaskableEntity` to add the ability to 
    connect a :class:`~stalker.core.models.Task` to it.
    
    The Task class itself is mixed with
    :class:`~stalker.core.models.StatusMixin` and
    :class:`~stalker.core.models.ScheduleMixin`. To be able to give the
    :class:`~stalker.core.models.Task` a *Status* and a *start* and *end* time.
    
    :param int priority: It is a number between 0 to 1000 which defines the
      priority of the :class:`~stalker.core.models.Task`. The higher the value
      the higher its priority. The default value is 500.
    
    :param resources: The :class:`~stalker.core.models.User`\ s assigned to
      this :class:`~stalker.core.models.Task`. A
      :class:`~stalker.core.models.Task` without any resource can not be
      scheduled.
    
    :type resources: list of :class:`~stalker.core.models.User`
    
    :param effort: The total effort that needs to be spend to complete this
      :class:`~stalker.core.models.Task`. Can be used to create an initial bid
      of how long this task will take. The effort is equally divided to the
      assigned resources. So if the effort is 10 days and 2
      :attr:`~stalker.core.models.Task.resources` is assigned then the
      :attr:`~stalker.core.models.Task.duration` of the task is going to be 5
      days (if both of the resources are free to work). The default value is
      stalker.conf.defaults.DEFAULT_TASK_DURATION.
      
      The effort argument defines the
      :attr:`~stalker.core.models.Task.duration` of the task. Every resource is
      counted equally effective and the
      :attr:`~stalker.core.models.Task.duration` will be calculated by the
      simple formula:
      
      .. math::
         
         {duration} = \\frac{{effort}}{n_{resources}}
      
      And changing the :attr:`~stalker.core.models.Task.duration` will also
      effect the :attr:`~stalker.core.models.Task.effort` spend. The
      :attr:`~stalker.core.models.Task.effort` will be calculated with the
      formula:
      
      .. math::
         
         {effort} = {duration} \\times {n_{resources}}
    
    :type effort: datetime.timedelta
    
    :param depends: A list of :class:`~stalker.core.models.Task`\ s that this
      :class:`~stalker.core.models.Task` is depending on. A Task can not depend
      to itself or any other Task which are already depending to this one in
      anyway or a CircularDependency error will be raised.
    
    :type depends: list of :class:`~stalker.core.models.Task`
    
    :param bool milestone: A bool (True or False) value showing if this task is
      a milestone which doesn't need any resource and effort.
    
    :param task_of: A :class:`~stalker.core.models.TaskableEntity` instance
      which is the owner of this Task.
    
    :type task_of: :class:`~stalker.core.models.TaskableEntity`
    """
    #.. :param depends: A list of
    #:class:`~stalker.core.models.TaskDependencyRelation` objects. Holds
    #information about the list of other :class:`~stalker.core.models.Task`\ s
    #which the current one is dependent on.

    #.. giving information about the dependent tasks. The given list is iterated
    #and the :attr:`~stalker.core.models.Task.start_date` attribute is set to
    #the latest found :attr:`~stalker.core.models.Task.due_date` attribute of
    #the dependent :class:`~stalker.core.models.Task`\ s.

    #.. :type depends: list of :class:`~stalker.core.models.TaskDependencyRelation`


    #:param parent_task: Another :class:`~stalker.core.models.Task` which is the
    #parent of the current :class:`~stalker.core.models.Task`.

    #:class:`~stalker.core.models.Task`\ s can be grouped by using parent and
    #child relation.

    #:type parent_task: :class:`~stalker.core.models.Task`

    #:param sub_tasks: A list of other :class:`~stalker.core.models.Task`\ s
    #which are the child of the current one. A
    #:class:`~stalker.core.models.Task` with other child
    #:class:`~stalker.core.models.Task`\ s:

    #* can not have any resources
    #* can not have any effort set
    #* can not have any versions

    #The only reason of a :class:`~stalker.core.models.Task` to have other
    #:class:`~stalker.core.models.Task`\ s as child is to group them. So it
    #is meaningles to let a parent :class:`~stalker.core.models.Task` to have
    #any resource or any effort or any verions. The
    #:attr:`~stalker.core.models.Task.start_date`,
    #:attr:`~stalker.core.models.Task.due_date` and
    #:attr:`~stalker.core.models.Task.duration` attributes of a
    #:class:`~stalker.core.models.Task` with child classes will be based on
    #it childrens date attributes.

    #:type child_tasks: :class:`~stalker.core.models.Task`.

    #:param versions: A list of :class:`~stalker.core.models.Version` objects
    #showing the produced work on the repository. This is the relation between
    #database and the repository.

    #:type versions: list of :class:`~stalker.core.models.Version`
    #"""


    __tablename__ = "Tasks"
    __mapper_args__ = {"polymorphic_identity": "Task"}
    task_id = Column("id", Integer, ForeignKey("Entities.id"),
                     primary_key=True)

    is_milestone = Column(
        Boolean,
        doc="""Specifies if this Task is a milestone.
        
        Milestones doesn't need any duration, any effort and any resources. It
        is used to create meaningfull dependencies between the critical stages
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
        secondary="Task_Tasks",
        primaryjoin="Tasks.c.id==Task_Tasks.c.task_id",
        secondaryjoin="Task_Tasks.c.depends_to_task_id==Tasks.c.id",
        backref="dependent_of",
        doc="""A list of :class:`~stalker.core.models.Task`\ s that this one is depending on.
        
        A CircularDependencyError will be raised when the task dependency
        creates a circlar dependency which means it is not allowed to create
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
        doc="""The list of :class:`stalker.core.models.User`\ s instances assigned to this Task.
        """
    )

    _effort = Column(Interval)
    priority = Column(Integer)

    task_of_id = Column(Integer, ForeignKey("TaskableEntities.id"))

    task_of = relationship(
        "TaskableEntity",
        primaryjoin="Tasks.c.task_of_id==TaskableEntities.c.id",
        back_populates="tasks",
        doc="""An object that this Task is a part of.
        
        The assigned object should have an attribute called ``tasks``. Any
        object which is not inherited from
        :class:`~stalker.core.models.TaskableEntity` thus doesn't have a
        ``tasks`` attribute which is mapped to the Tasks.task_of attribute
        will raise an AttributeError.
        """
    )

    bookings = relationship(
        "Booking",
        primaryjoin="Bookings.c.task_id==Tasks.c.id",
        back_populates="task",
        doc="""A list of :class:`~stalker.core.models.Booking` instances showing who and when spent how much effort on this task.
        """
    )

    versions = relationship(
        "Version",
        primaryjoin="Versions.c.version_of_id==Tasks.c.id",
        back_populates="version_of",
        doc="""A list of :class:`~stalker.core.models.Version` instances showing the files created for this task.
        """
    )

    def __init__(self,
                 depends=None,
                 effort=None,
                 resources=None,
                 is_milestone=False,
                 priority=defaults.DEFAULT_TASK_PRIORITY,
                 task_of=None,
                 **kwargs):
        super(Task, self).__init__(**kwargs)

        # call the mixin __init__ methods
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)

        self.bookings = []
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
        self._effort = None
        self.effort = effort

        self.priority = priority

        self.task_of = task_of

    @reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        # UPDATE THIS
        self.bookings = []
        self.versions = []

        # call supers __init_on_load__
        super(Task, self).__init_on_load__()

    def __eq__(self, other):
        """the equality operator
        """

        return super(Task, self).__eq__(other) and isinstance(other, Task)

    @validates("bookings")
    def _validate_bookings(self, key, booking):
        """validates the given bookings value
        """

        if not isinstance(booking, Booking):
            raise TypeError(
                "all the elements in the %s.bookings should be an instances "
                "of stalker.core.models.Booking not %s instance" %
                (self.__class__.__name__, booking.__class__.__name__))

        return booking

    @validates("is_complete")
    def _validate_is_complete(self, key, complete_in):
        """validates the given complete value
        """
        return bool(complete_in)

    @validates("depends")
    def _validate_depends(self, key, depends):
        """validates the given depends value
        """

        #if depends_in is None:
        #depends_in = []

        #if not isinstance(depends_in, list):
        #raise TypeError("the depends attribute should be an list of"
        #"stalker.core.models.Task instances")


        if not isinstance(depends, Task):
            raise TypeError("all the elements in the depends should be an "
                            "instance of stalker.core.models.Task")

        # check for the circular dependency
        _check_circular_dependency(depends, self)

        return depends

    def _validate_effort(self, effort):
        """validates the given effort
        """

        if not isinstance(effort, datetime.timedelta):
            effort = None

        if effort is None:
            # take it from the duration and resources

            num_of_resources = len(self.resources)
            if num_of_resources == 0:
                num_of_resources = 1

            effort = self.duration * num_of_resources

        return effort

    def _effort_getter(self):
        """the getter for the effort property
        """
        return self._effort

    def _effort_setter(self, effort_in):
        """the setter for the effort property
        """
        self._effort = self._validate_effort(effort_in)

        # update the duration
        num_of_resources = len(self.resources)
        if num_of_resources == 0:
            num_of_resources = 1

        self.duration = self._effort / num_of_resources

    effort = synonym(
        "_effort",
        descriptor=property(
            fget=_effort_getter,
            fset=_effort_setter
        ),
        doc="""The total effort that needs to be spend to complete this Task.
        
        Can be used to create an initial bid of how long this task going to
        take. The effort is equally divided to the assigned resources. So if
        the effort is 10 days and 2 resources is assigned then the
        :attr:`~stalker.core.models.Task.duration` of the task is going to be 5
        days (if both of the resources are free to work). The default value is
        stalker.conf.defaults.DEFAULT_TASK_DURATION.
      
        The effort defines the :attr:`~stalker.core.models.Task.duration` of
        the task. Every resource is counted equally effective and the
        :attr:`~stalker.core.models.Task.duration` will be calculated by the
        simple formula:
        
        .. math::
           
           {duration} = \\frac{{effort}}{n_{resources}}
        
        And changing the :attr:`~stalker.core.models.Task.duration` will also
        effect the :attr:`~stalker.core.models.Task.effort` spend. The
        :attr:`~stalker.core.models.Task.effort` will be calculated with the
        formula:
           
        .. math::
           
           {effort} = {duration} \\times {n_{resources}}
        """
    )

    @validates("is_milestone")
    def _validate_is_milestone(self, key, is_milestone):
        """validates the given milestone value
        """

        if is_milestone:
            self.resources = []

        return bool(is_milestone)

    @validates("task_of")
    def _validate_task_of(self, key, task_of):
        """validates the given task_of value
        """

        # the object given withe the task_of argument should have an attribute
        # called "tasks"
        if task_of is None:
            raise TypeError("'task_of' can not be None, this will produce "
                            "Tasks without a parent, to remove a task from "
                            "a TaskableEntity, assign the task to another "
                            "TaskableEntity or delete it.")

        if not hasattr(task_of, "tasks"):
            raise AttributeError("the object given with 'task_of' should have "
                                 "an attribute called 'tasks'")

        return task_of

    @validates("priority")
    def _validate_priority(self, key, priority):
        """validates the given priority value
        """

        try:
            priority = int(priority)
        except (ValueError, TypeError):
            pass

        if not isinstance(priority, int):
            priority = defaults.DEFAULT_TASK_PRIORITY

        if priority < 0:
            priority = 0
        elif priority > 1000:
            priority = 1000

        return priority

    @validates("resources")
    def _validate_resources(self, key, resource):
        """validates the given resources value
        """
        
        from stalker.models.user import User

        if not isinstance(resource, User):
            raise TypeError("resources should be a list of "
                            "stalker.core.models.User instances")

            ## milestones do not need resources
            #if self.is_milestone:
            #resource = None

        return resource

    # TODO: UPDATE THIS

    @validates("versions")
    def _validate_versions(self, key, version):
        """validates the given version value
        """
        
        from stalker.models.version import Version
        
        if not isinstance(version, Version):
            raise TypeError("all the elements in the versions list should be "
                            "stalker.core.models.Version instances")

        return version

    def _duration_getter(self):
        return self._duration

    def _duration_setter(self, duration):
        # just call the fset method of the duration property in the super

        #------------------------------------------------------------
        # code copied and pasted from ScheduleMixin - Fix it later
        if duration is not None:
            if isinstance(duration, datetime.timedelta):
                # set the due_date to None
                # to make it recalculated
                self._validate_dates(self.start_date, None, duration)
            else:
                self._validate_dates(self.start_date, self.due_date, duration)
        else:
            self._validate_dates(self.start_date, self.due_date, duration)
            #------------------------------------------------------------


        # then update the effort
        num_of_resources = len(self.resources)
        if num_of_resources == 0:
            num_of_resources = 1

        new_effort_value = self.duration * num_of_resources

        # break recursion
        if self.effort != new_effort_value:
            self.effort = new_effort_value

            #return duration

    duration = synonym(
        "_duration",
        descriptor=property(
            _duration_getter,
            _duration_setter
        ),
        doc="""The overridden duration attribute.
        
        It is a datetime.timedelta instance. Showing the difference of the
        :attr:`~stalker.core.models.ScheduleMixin.start_date` and the
        :attr:`~stalker.core.models.ScheduleMixin.due_date`. If edited it
        changes the :attr:`~stalker.core.models.ScheduleMixin.due_date`
        attribute value.
        """
    )


def _check_circular_dependency(task, check_for_task):
    """checks the circular dependency in task if it has check_for_task in its
    depends list
    
    !!!!WARNING THERE IS NO TEST FOR THIS FUNCTION!!!!
    """

    for dependent_task in task.depends:
        if dependent_task is check_for_task:
            raise CircularDependencyError(
                "task %s and %s creates a circular dependency" %\
                (task, check_for_task)
            )
        else:
            _check_circular_dependency(dependent_task, check_for_task)


#class TaskDependencyRelation(object):
#"""Holds information about :class:`~stalker.core.models.Task` dependencies.

#(DEVELOPERS: It could be an association proxy for the Task class)

#A TaskDependencyRelation object basically defines which
#:class:`~stalker.core.models.Task` is dependedt
#to which other :class:`~stalker.core.models.Task` and what is the lag
#between the end of the dependent to the start of the dependee.

#A :class:`~stalker.core.models.Task` can not be set dependent to it self.
#So the the :attr:`~stalker.core.models.TaskDependencyRelation.depends` list
#can not contain the same value with
#:attr:`~stalker.core.models.TaskDependencyRelation.task`.

#:param task: The :class:`~stalker.core.models.Task` that is dependent to
#others.

#:type task: :class:`~stalker.core.models.Task`

#:param depends: A :class:`~stalker.core.models.Task`\ s that the
#:class:`~stalker.core.models.Task` which is held by the
#:attr:`~stakler.core.models.TaskDependencyRelation.task` attribute is
#dependening on. The :attr:`~stalker.core.models.Task.start_date` and the
#:attr:`~stalker.core.models.Task.due_date` attributes of the
#:class:`~stalker.core.models.Task` is updated if it is before the
#``due_date`` of the dependent :class:`~stalker.core.models.Task`.

#:type depends: :class:`~stalker.core.models.Task`

#:param lag: The lag between the end of the dependent task to the start of
#the dependee. It is an instance of timedelta and could be a negative
#value. The default is 0. So the end of the task is start of the other.
#"""

#
    #def __init__(self):
        #pass

# TASK_TASKS
Task_Tasks = Table(
    "Task_Tasks", Base.metadata,
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
