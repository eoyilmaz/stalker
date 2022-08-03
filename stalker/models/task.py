# -*- coding: utf-8 -*-

import datetime
import logging
import os

from sqlalchemy import (Table, Column, Integer, ForeignKey, Boolean, Enum,
                        Float, event, CheckConstraint)
from sqlalchemy.exc import UnboundExecutionError, OperationalError, InvalidRequestError, ProgrammingError
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, validates, synonym, reconstructor

from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.mixins import (DateRangeMixin, StatusMixin, ReferenceMixin,
                                   ScheduleMixin, DAGMixin)
from stalker.log import logging_level

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


# schedule constraints
CONSTRAIN_NONE = 0
CONSTRAIN_START = 1
CONSTRAIN_END = 2
CONSTRAIN_BOTH = 3


class TimeLog(Entity, DateRangeMixin):
    """Holds information about the uninterrupted time spent on a specific
    :class:`.Task` by a specific :class:`.User`.

    It is so important to note that the TimeLog reports the **uninterrupted**
    time interval that is spent for a Task. Thus it doesn't care about the
    working time attributes like daily working hours, weekly working days or
    anything else. Again it is the uninterrupted time which is spent for a
    task.

    Entering a time log for 2 days will book the resource for 48 hours and not,
    2 * daily working hours.

    TimeLogs are created per resource. It means, you need to record all the
    works separately for each resource. So there is only one resource in a
    TimeLog instance.

    A :class:`.TimeLog` instance needs to be initialized with a :class:`.Task`
    and a :class:`.User` instances.

    Adding overlapping time log for a :class:`.User` will raise a
    :class:`.OverBookedError`.

    .. ::
      TimeLog instances automatically extends the :attr:`.Task.schedule_timing`
      of the assigned Task if the :attr:`.Task.total_logged_seconds` is getting
      bigger than the :attr:`.Task.schedule_timing` after this TimeLog.

    :param task: The :class:`.Task` instance that this time log belongs to.

    :param resource: The :class:`.User` instance that this time log is created
      for.
    """
    __auto_name__ = True
    __tablename__ = "TimeLogs"
    __mapper_args__ = {"polymorphic_identity": "TimeLog"}

    __table_args__ = (
        CheckConstraint('"end" > start'),  # this will be ignored in SQLite3
    )

    time_log_id = Column("id", Integer, ForeignKey("Entities.id"),
                         primary_key=True)
    task_id = Column(
        Integer, ForeignKey("Tasks.id"), nullable=False,
        doc="""The id of the related task."""
    )
    task = relationship(
        "Task",
        primaryjoin="TimeLogs.c.task_id==Tasks.c.id",
        uselist=False,
        back_populates="time_logs",
        doc="""The :class:`.Task` instance that this time log is created for"""
    )

    resource_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    resource = relationship(
        "User",
        primaryjoin="TimeLogs.c.resource_id==Users.c.id",
        uselist=False,
        back_populates="time_logs",
        doc="""The :class:`.User` instance that this time_log is created for"""
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
        DateRangeMixin.__init__(self, **kwargs)
        self.task = task
        self.resource = resource

    @validates("task")
    def _validate_task(self, key, task):
        """validates the given task value
        """
        if not isinstance(task, Task):
            raise TypeError(
                "%s.task should be an instance of stalker.models.task.Task "
                "not %s" %
                (self.__class__.__name__, task.__class__.__name__)
            )

        if task.is_container:
            raise ValueError(
                '%(task)s (id: %(id)s) is a container task, and it is not '
                'allowed to create TimeLogs for a container task' % {
                    'task': task.name,
                    'id': task.id
                }
            )

        # check status
        logger.debug('checking task status!')
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            task_status_list = task.status_list
            WFD = task_status_list['WFD']
            RTS = task_status_list['RTS']
            WIP = task_status_list['WIP']
            PREV = task_status_list['PREV']
            HREV = task_status_list['HREV']
            DREV = task_status_list['DREV']
            OH = task_status_list['OH']
            STOP = task_status_list['STOP']
            CMPL = task_status_list['CMPL']
    
            if task.status in [WFD, OH, STOP, CMPL]:
                from stalker.exceptions import StatusError
                raise StatusError(
                    '%(task)s is a %(status)s task, and it is not allowed to '
                    'create TimeLogs for a %(status)s task, please supply a '
                    'RTS, WIP, HREV or DREV task!' % {
                        'task': task.name,
                        'status': task.status.code
                    }
                )
            elif task.status in [RTS, HREV]:
                # update task status
                logger.debug('updating task status to WIP!')
                task.status = WIP

            # check dependent tasks
            logger.debug('checking dependent task statuses')
            for task_dependencies in task.task_depends_to:
                dep_task = task_dependencies.depends_to
                dependency_target = task_dependencies.dependency_target
                raise_violation_error = False
                violation_date = None

                if dependency_target == 'onend':
                    # time log can not start before the end date of this task
                    if self.start < dep_task.end:
                        raise_violation_error = True
                        violation_date = dep_task.end
                elif dependency_target == 'onstart':
                    if self.start < dep_task.start:
                        raise_violation_error = True
                        violation_date = dep_task.start

                if raise_violation_error:
                    from stalker.exceptions import DependencyViolationError
                    raise DependencyViolationError(
                        'It is not possible to create a TimeLog before '
                        '%s, which violates the dependency relation of '
                        '"%s" to "%s"' % (
                            violation_date,
                            task.name,
                            dep_task.name,
                        )
                    )

        # this may need to be in an external event, it needs to trigger a flush
        # to correctly function
        task.update_parent_statuses()

        return task

    @validates("resource")
    def _validate_resource(self, key, resource):
        """validates the given resource value
        """
        if resource is None:
            raise TypeError(
                "%s.resource can not be None" % self.__class__.__name__
            )

        from stalker import User
        if not isinstance(resource, User):
            raise TypeError(
                "%s.resource should be a stalker.models.auth.User instance "
                "not %s" %
                (self.__class__.__name__, resource.__class__.__name__)
            )

        # check for overbooking
        clashing_time_log_data = None
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            try:
                from sqlalchemy import or_, and_
                clashing_time_log_data = \
                    DBSession.query(TimeLog.start, TimeLog.end)\
                        .filter(TimeLog.id != self.id)\
                        .filter(TimeLog.resource_id == resource.id)\
                        .filter(
                            or_(
                                and_(
                                    TimeLog.start <= self.start,
                                    self.start < TimeLog.end
                                ),
                                and_(
                                    TimeLog.start < self.end,
                                    self.end <= TimeLog.end
                                )
                            )
                        )\
                        .first()

            except (UnboundExecutionError, OperationalError) as e:
                # fallback to Python
                for time_log in resource.time_logs:
                    if time_log != self:
                        if time_log.start == self.start or \
                           time_log.end == self.end or \
                           time_log.start < self.end < time_log.end or \
                           time_log.start < self.start < time_log.end:
                            clashing_time_log_data = \
                                [time_log.start, time_log.end]

            if clashing_time_log_data:
                from stalker.exceptions import OverBookedError
                raise OverBookedError(
                    "The resource has another TimeLog between %s and %s" % (
                        clashing_time_log_data[0], clashing_time_log_data[1]
                    )
                )

        return resource

    def __eq__(self, other):
        """equality of TimeLog instances
        """
        return isinstance(other, TimeLog) and self.task is other.task and \
            self.resource is other.resource and self.start == other.start and \
            self.end == other.end and self.name == other.name

# TODO: Consider contracting a Task with TimeLogs, what will happen when the
#       task has logged in time
# TODO: Check, what happens when a task has TimeLogs and will have child task
#       later on, will it be ok with TJ


class Task(Entity, StatusMixin, DateRangeMixin, ReferenceMixin, ScheduleMixin, DAGMixin):
    """Manages Task related data.

    **Introduction**

    Tasks are the smallest unit of work that should be accomplished to complete
    a :class:`.Project`. Tasks define a certain amount of time needed to be
    spent for a purpose. They also define a complex hierarchy of relation.

    Stalker follows and enhances the concepts stated in TaskJuggler_.

    .. _TaskJuggler : http://www.taskjuggler.org/

    .. note::
       .. versionadded:: 0.2.0
          References in Tasks

       Tasks can now have References.

    **Initialization**

    Tasks are a part of a bigger Project, that's way a Task needs to be created
    with a :class:`.Project` instance. It is possible to create a task without
    a project, if it is created to be a child of another task. And it is also
    possible to pass both a project and a parent task.

    But because passing both a project and a parent task may create an
    ambiguity, Stalker will raise a RuntimeWarning, if both project and task
    are given and the owner project of the given parent task is different then
    the supplied project instance. But again Stalker will warn the user but
    will continue to use the task as the parent and will correctly use the
    project of the given task as the project of the newly created task.

    The following codes are a couple of examples for creating Task instances::

      # with a project instance
      >>> from stalker import Project
      >>> project1 = Project(name='Test Project 1')  # simplified
      >>> task1 = Task(name='Schedule', project=project1)

      # with a parent task
      >>> task2 = Task(name='Documentation', parent=task1)

      # or both
      >>> task3 = Task(name='Test', project=project1, parent=task1)

      # this will create a RuntimeWarning
      >>> project2 = Project(name='Test Project 2')
      >>> task4 = Task(name='Test', project=project2, parent=task1)
      # task1 is not a # task of proj2

      >>> assert task4.project == project1
      # Stalker uses the task1.project for task4

      # this will also create a RuntimeError
      >>> task3 = Task(name='Failure 2') # no project no parent, this is an
                                         # orphan task.

    Also initially Stalker will pin point the :attr:`.start` value and then
    will calculate proper :attr:`.end` and :attr:`.duration` values by using
    the :attr:`.schedule_timing` and :attr:`.schedule_unit` attributes. But
    these values (start, end and duration) are temporary values for an
    unscheduled task. The final date values will be calculated by TaskJuggler
    in the `auto scheduling` phase.

    **Auto Scheduling**

    Stalker uses TaskJuggler for task scheduling. After defining all the tasks,
    Stalker will convert them to a single tjp file along with the recorded
    :class:`.TimeLog` s :class:`.Vacation` s etc. and let TaskJuggler to
    solve the scheduling problem.

    During the auto scheduling (with TaskJuggler), the calculation of task
    duration, start and end dates are effected by the working hours setting of
    the :class:`.Studio`, the effort that needs to spend for that task and the
    availability of the resources assigned to the task.

    A good practice for creating a project plan is to supply the parent/child
    and dependency relation between tasks and the effort and resource
    information per task and leave the start and end date calculation to
    TaskJuggler.

    The default :attr:`.schedule_model` for Stalker tasks is 'effort`, the
    default :attr:`.schedule_unit` is ``hour`` and the default value of
    :attr:`.schedule_timing` is defined by the
    :attr:`stalker.config.Config.timing_resolution`. So for a config where the
    ``timing_resolution`` is set to 1 hour the schedule_timing is 1.

    It is also possible to use the ``length`` or ``duration`` values for
    :attr:`.schedule_model` (set it to 'effort', 'length' or 'duration' to get
    the desired scheduling model).

    To convert a Task instance to a TaskJuggler compatible string use the
    :attr:`.to_tjp`` attribute. It will try to create a good representation of
    the Task by using the resources, schedule_model, schedule_timing and
    schedule_constraint attributes.

    ** Alternative Resources**

    .. versionadded:: 0.2.5
       Alternative Resources

    Stalker now supports alternative resources per task. You can specify
    alternative resources by using the :attr:`.alternative_resources`
    attribute. The number of resources and the number of alternative resources
    are not related. So you can define only 1 resource and more than one
    alternative resources, or you can define 2 resources and only one
    alternative resource.

    .. warning::

       As opposed to TaskJuggler alternative resources are not per resource
       based. So Stalker will use the alternatives list for all of the
       resources in the resources list. Per resource alternative will be
       supported in future versions of Stalker.

    Stalker will pass the data to TaskJuggler and TJ will compute a list of
    resources that are assigned to the task in the report time frame and
    Stalker will store the resultant list of users in
    :attr:`.computed_resources` attribute.

    .. warning::

       When TaskJuggler computes the resources, the returned list may contain
       resources which are not in the :attr:`.resources` nor in
       :attr:`.alternative_resources` list anymore. Stalker will silently
       filter those resources and will only store resources (in
       :attr:`.computed_resources`) those are still available as a direct or
       alternative resource to that particular task.

    The selection strategy of the alternative resource is defined by the
    :attr:`.allocation_strategy` attribute. The `allocation_strategy`
    attribute value should be one of [minallocated, maxloaded, minloaded,
    order, random]. The following description is from TaskJuggler
    documentation:

      +--------------+--------------------------------------------------------+
      | minallocated | Pick the resource that has the smallest allocation     |
      |              | factor. The allocation factor is calculated from the   |
      |              | various allocations of the resource across the tasks.  |
      |              | This is the default setting.)                          |
      +--------------+--------------------------------------------------------+
      | maxloaded    | Pick the available resource that has been used the     |
      |              | most so far.                                           |
      +--------------+--------------------------------------------------------+
      | minloaded    | Pick the available resource that has been used the     |
      |              | least so far.                                          |
      +--------------+--------------------------------------------------------+
      | order        | Pick the first available resource from the list.       |
      +--------------+--------------------------------------------------------+
      | random       | Pick a random resource from the list.                  |
      +--------------+--------------------------------------------------------+

    As in TaskJuggler the default for :attr:`.allocation_strategy` attribute is
    "minallocated".

    Also the allocation of the resources are effected by the
    :attr:`.persistent_allocation` attribute. The persistent_allocation
    attribute refers to the ``persistent`` attribute in TJ. The documentation
    of ``persistent`` in TJ is as follows:

      Specifies that once a resource is picked from the list of alternatives
      this resource is used for the whole task. This is useful when several
      alternative resources have been specified. Normally the selected resource
      can change after each break. A break is an interval of at least one
      timeslot where no resources were available.

    :attr:`.persistent_allocation` attribute is True by default.

    For a not yet scheduled task the :attr:`.computed_resources` attribute will
    be the same as the :attr:`.resources` list. After the task is scheduled the
    content of the :attr:`.computed_resources` will purely come from TJ.

    Updating the resources list will not update the :attr:`.computed_resources`
    list if the task :attr:`.is_scheduled`.

    **Task to Task Relation**

    .. note::
       .. versionadded:: 0.2.0
       Task to Task Relation

    Tasks can have child Tasks. So you can create complex relations of Tasks to
    comply with your project needs.

    A Task is called a ``container task`` if it has at least one child Task.
    And it is called a ``leaf task`` if it doesn't have any children Tasks.
    Tasks which doesn't have a parent called ``root_task``.

    As opposed to TaskJuggler where the resource information is passed through
    parent to child, in Stalker the resources in a container task is
    meaningless, cause the resources are defined by the child tasks.

    .. note::

      Although, the ``tjp_task_template`` variable is not coded in that way in
      the default config, if you want to populate resource information through
      children tasks as it is in TaskJuggler, you can change the
      ``tjp_task_template`` variable with a local **config.py** file. See
      `configuring stalker`_

      .. _configuring stalker: ../configure.html

    Although the values are not very important after TaskJuggler schedules a
    task, the :attr:`~.start` and :attr:`~.end` values for a container
    task is gathered from the child tasks. The start is equal to the earliest
    start value of the children tasks, and the end is equal to the latest end
    value of the children tasks. Of course, these values are going to be
    ignored by TaskJuggler, but for interactive gantt charts these are good toy
    attributes to play with.

    Stalker will check if there will be a cycle if one wants to parent a Task
    to a child Task of its own or the dependency relation creates a cycle.

    In Gantt Charts the ``computed_start``, ``computed_end`` and
    ``computed_resources`` attributes will be used if the task
    :attr:`.is_scheduled`.

    **Task Responsible**

    .. note::
       .. versionadded:: 0.2.0
          Task Responsible

    .. note::
       .. versionadded:: 0.2.5
          Multiple Responsible Per Task

    Tasks have a **responsible** which is a list of :class:`.User` instances
    who are responsible of the assigned task and all the hierarchy under it.

    If a task doesn't have any responsible, it will start looking to its
    parent tasks and will return a copy of the responsible of its parent and it
    will be an empty list if non of its parents has a responsible.

    You can create complex responsibility chains for different branches of
    Tasks.

    **Percent Complete Calculation** .. versionadded:: 0.2.0

    Tasks can calculate how much it is completed based on the
    :attr:`.schedule_seconds` and :attr:`.total_logged_seconds` attributes.
    For a parent task, the calculation is based on the total
    :attr:`.schedule_seconds` and :attr:`.total_logged_seconds` attributes of
    their children.

    .. versionadded:: 0.2.14
       Because duration tasks do not need time logs there is no way to
       calculate the percent complete by using the time logs. And Percent
       Complete on a duration task is calculated directly from the
       :attr:`.start` and :attr:`.end` and ``datetime.datetime.now(pytz.utc)``.

    .. versionadded:: 0.2.26
       For parent tasks that have both effort based and duration based children
       tasks the percent complete is calculated as if the
       :attr:`.total_logged_seconds` is properly filled for duration based
       tasks proportinal to the elapsed time from the :attr:`.start` attr
       value.

    Even tough, the percent_complete attribute of a task is
    100% the task may not be considered as completed, because it may not be
    reviewed and approved by the responsible yet.

    **Task Review Workflow**

    .. versionadded:: 0.2.5
       Task Review Workflow

    Starting with Stalker v0.2.5 tasks are reviewed by their responsible users.
    The reviews done by responsible users will set the task status according to
    the supplied reviews. Please see the :class:`.Review` class documentation
    for more details.

    **Task Status Workflow**

    .. note::
       .. versionadded:: 0.2.5
          Task Status Workflow

    Task statuses now follow a workflow called "Task Status Workflow".

    The "Task Status Workflow" defines the different statuses that a Task will
    have along its normal life cycle. Container and leaf tasks will have
    different workflow using nearly the same set of statuses (container tasks
    have only 4 statuses where as leaf tasks have 9).

    The following diagram shows the status workflow for leaf tasks:

    .. image:: ../../../docs/source/_static/images/Task_Status_Workflow.png
          :width: 637 px
          :height: 611 px
          :align: center

    The workflow defines the following statuses at described situations:

      +-----------------------------------------------------------------------+
      | LEAF TASK STATUS WORKFLOW                                             |
      +------------------+----------------------------------------------------+
      | Status Name      | Description                                        |
      +------------------+----------------------------------------------------+
      | Waiting For      | If a task has uncompleted dependencies then it     |
      | Dependency (WFD) | will have its status to set to WFD. A WFD Task can |
      |                  | not have a TimeLog or a review request can not be  |
      |                  | made for it.                                       |
      +------------------+----------------------------------------------------+
      | Ready To Start   | A task is set to RTS when there are no             |
      | (RTS)            | dependencies or all of its dependencies are        |
      |                  | completed, so there is nothing preventing it to be |
      |                  | started. An RTS Task can have new TimeLogs. A      |
      |                  | review can not be requested at this stage cause no |
      |                  | work is done yet.                                  |
      +------------------+----------------------------------------------------+
      | Work In Progress | A task is set to WIP when a TimeLog has been       |
      | (WIP)            | created for that task. A WIP task can have new     |
      |                  | TimeLogs and a review can be requested for that    |
      |                  | task.                                              |
      +------------------+----------------------------------------------------+
      | Pending Review   | A task is set to PREV when a new set of Review     |
      | (PREV)           | instances created for it by using the              |
      |                  | :meth:`.Task.request_review` method. And it is     |
      |                  | possible to request a review only for a task with  |
      |                  | status WIP. A PREV task can not have new TimeLogs  |
      |                  | nor a new request can be made because it is in     |
      |                  | already in review.                                 |
      +------------------+----------------------------------------------------+
      | Has Revision     | A task is set to HREV when one of its Reviews      |
      | (HREV)           | completed by requesting a review by using the      |
      |                  | :meth:`.Review.request_review` method. A HREV Task |
      |                  | can have new TimeLogs, and it will be converted to |
      |                  | a WIP or DREV depending to its dependency task     |
      |                  | statuses.                                          |
      +------------------+----------------------------------------------------+
      | Dependency Has   | If the dependent task of a WIP, PREV, HREV, DREV   |
      | Revision (DREV)  | or CMPL task has a revision then the statuses of   |
      |                  | the tasks are set to DREV which means both of the  |
      |                  | dependee and the dependent tasks can work at the   |
      |                  | same time. For a DREV task a review request can    |
      |                  | not be made until it is set to WIP again by        |
      |                  | setting the depending task to CMPL again.          |
      +------------------+----------------------------------------------------+
      | On Hold (OH)     | A task is set to OH when the resource needs to     |
      |                  | work for another task, and the :meth:`Task.hold`   |
      |                  | is called. An OH Task can be resumed by calling    |
      |                  | :meth:`.Task.resume` method and depending to its   |
      |                  | :attr:`.Task.time_logs` attribute it will have its |
      |                  | status set to RTS or WIP.                          |
      +------------------+----------------------------------------------------+
      | Stopped (STOP)   | A task is set to STOP when no more work needs to   |
      |                  | done for that task and it will not be used         |
      |                  | anymore. Call :meth:`.Task.stop` method to do it   |
      |                  | properly. Only applicable to WIP tasks.            |
      |                  |                                                    |
      |                  | The schedule values of the task will be capped to  |
      |                  | current time spent on it, so Task Juggler will not |
      |                  | reserve any more resources for it.                 |
      |                  |                                                    |
      |                  | Also STOP tasks are treated as if they are dead.   |
      +------------------+----------------------------------------------------+
      | Completed (CMPL) | A task is set to CMPL when all of the Reviews are  |
      |                  | completed by approving the task. It is not         |
      |                  | possible to create any new TimeLogs and no new     |
      |                  | review can be requested for a CMPL Task.           |
      +------------------+----------------------------------------------------+

    Container "Task Status Workflow" defines a set of statuses where the
    container task status will only change according to its children task
    statuses:

      +-----------------------------------------------------------------------+
      |                    CONTAINER TASK STATUS WORKFLOW                     |
      +------------------+----------------------------------------------------+
      | Status Name      | Description                                        |
      +------------------+----------------------------------------------------+
      | Waiting For      | If all of the child tasks are in WFD status then   |
      | Dependency (WFD) | the container task is also WFD.                    |
      +------------------+----------------------------------------------------+
      | Ready To Start   | A container task is set to RTS when children tasks |
      | (RTS)            | have statuses of only WFD and RTS.                 |
      +------------------+----------------------------------------------------+
      | Work In Progress | A container task is set to WIP when one of its     |
      | (WIP)            | children tasks have any of the statuses of RTS,    |
      |                  | WIP, PREV, HREV, DREV or CMPL.                     |
      +------------------+----------------------------------------------------+
      | Completed (CMPL) | A container task is set to CMPL when all of its    |
      |                  | children tasks are CMPL.                           |
      +------------------+----------------------------------------------------+

    Even though, users are encouraged to use the actions (like
    :meth:`.Task.create_time_log`, :meth:`.Task.hold`, :meth:`.Task.stop`,
    :meth:`.Task.resume`, :meth:`.Task.request_revision`,
    :meth:`.Task.request_review`, :meth:`.Task.approve`) to update the task
    statuses , setting the :attr:`.Task.status` will also update the dependent
    tasks or will check the new status against dependencies or the current
    status of the task.

    Thus in some situations setting the :attr:`.Task.status` will not change
    the status of the task. For example, setting the task status to WFD when
    there are no dependencies will not update the task status to WFD,
    also updating a PREV task status to STOP or HOLD or RTS is not possible.
    And it is not possible to set a task to WIP if there are no TimeLogs
    entered for that task.

    So the task will strictly follow the Task Status Workflow diagram above.

    .. warning::
       **Dependency Relation in Task Status Workflow**

       Because the Task Status Workflow heavily effected by the dependent task
       statuses, and the main reason of having dependency relation is to let
       TaskJuggler to schedule the tasks correctly, and any task status other
       than WFD or RTS means that a TimeLog has been created for a task (which
       means that you can not change the :attr:`.computed_start` anymore), it
       is only allowed to change the dependencies of a WFD and RTS tasks.

    .. warning::
       **Resuming a STOP Task**

       Resuming a STOP Task will be treated as if a revision has been made to
       that task, and all the statuses of the tasks depending to this
       particular task will be updated accordingly.

    .. warning::
       **Initial Status of a Task**

       .. versionadded:: 0.2.5

       Because of the Task Status Workflow, supplying a status with the
       **status** argument may not set the status of the Task to the desired
       value. A Task starts with WFD status by default, and updated to RTS if
       it doesn't have any dependencies or all of the dependencies are STOP or
       CMPL.

    .. note::
       .. versionadded:: 0.2.5.2
          Task.path and Task.absolute_path properties

          Task instances now have two new properties called :attr:`.path` and
          :attr:`.absolute_path`\ . The value of these attributes are the
          rendered version of the related :class:`.FilenameTemplate` which
          has its target_entity_type attribute set to "Task" (or "Asset",
          "Shot" or "Sequence" or anything matching to the derived class name,
          so it can be used in :class:`.Asset`, :class:`.Shot` and
          :class:`.Sequences` or anything that is derived from Task class) in
          the :class:`.Project` that this task belongs to. This property has
          been added to make it easier to write custom template codes for
          Project :class:`.Structure` s.

          The :attr:`.path` attribute is a repository relative path, where as
          the :attr:`.absolute_path` is the full path and includs the OS
          dependent repository path.

    .. versionadded: 0.2.13

       Task to :class:`.Good` relation. It is now possible to define the
       related Good to this task, to be able to filter tasks that are related
       to the same :class:`.Good`.

       Its main purpose of existence is to be able to generate
       :class:`.BugdetEntry` instances from the tasks that are related to the
       same :class:`.Good` and because the Goods are defining the cost and MSRP
       of different things, it is possible to create BudgetEntries and thus
       :class;`.Budget` s with this information.

    **Arguments**

    :param project: A Task which doesn't have a parent (a root task) should be
      created with a :class:`.Project` instance. If it is skipped an no
      :attr:`.parent` is given then Stalker will raise a RuntimeError. If both
      the ``project`` and the :attr:`.parent` argument contains data and the
      project of the Task instance given with parent argument is different than
      the Project instance given with the ``project`` argument then a
      RuntimeWarning will be raised and the project of the parent task will be
      used.

    :type project: :class:`.Project`

    :param parent: The parent Task or Project of this Task. Every Task in
      Stalker should be related with a :class:`.Project` instance. So if no
      parent task is desired, at least a Project instance should be passed as
      the parent of the created Task or the Task will be an orphan task and
      Stalker will raise a RuntimeError.

    :type parent: :class:`.Task`

    :param depends: A list of :class:`.Task` s that this :class:`.Task` is
      depending on. A Task can not depend to itself or any other Task which are
      already depending to this one in anyway or a CircularDependency error
      will be raised.

    :type depends: [:class:`.Task`]

    :param resources: The :class:`.User` s assigned to this :class:`.Task`. A
      :class:`.Task` without any resource can not be scheduled.

    :type resources: [:class:`.User`]

    :param responsible: A list of :class:`.User` instances that is responsible
      of this task.

    :type responsible: [:class:`.User`]

    :param watchers: A list of :class:`.User` those are added this Task
      instance to their watchlist.

    :type watchers: [:class:`.User`]

    :param start: The start date and time of this task instance. It is only
      used if the :attr:`.schedule_constraint` attribute is set to
      :attr:`.CONSTRAIN_START` or :attr:`.CONSTRAIN_BOTH`. The default value
      is `datetime.datetime.now(pytz.utc)`.

    :type start: :class:`datetime.datetime`

    :param end: The end date and time of this task instance. It is only used if
      the :attr:`.schedule_constraint` attribute is set to
      :attr:`.CONSTRAIN_END` or :attr:`.CONSTRAIN_BOTH`. The default value is
      `datetime.datetime.now(pytz.utc)`.

    :type end: :class:`datetime.datetime`

    :param int schedule_timing: The value of the schedule timing.

    :param str schedule_unit: The unit value of the schedule timing. Should be
      one of 'min', 'h', 'd', 'w', 'm', 'y'.

    :param int schedule_constraint: The schedule constraint. It is the index
      of the schedule constraints value in
      :class:`stalker.config.Config.task_schedule_constraints`.

    :param int bid_timing: The initial bid for this Task. It can be used in
      measuring how accurate the initial guess was. It will be compared against
      the total amount of effort spend doing this task. Can be set to None,
      which will be set to the schedule_timing_day argument value if there is
      one or 0.

    :param str bid_unit: The unit of the bid value for this Task. Should be one
      of the 'min', 'h', 'd', 'w', 'm', 'y'.

    :param bool is_milestone: A bool (True or False) value showing if this task
      is a milestone which doesn't need any resource and effort.

    :param int priority: It is a number between 0 to 1000 which defines the
      priority of the :class:`.Task`. The higher the value the higher its
      priority. The default value is 500. Mainly used by TaskJuggler.

      Higher priority tasks will be scheduled to an early date or at least will
      tried to be scheduled to an early date then a lower priority task (a task
      that is using the same resources).

      In complex projects, a task with a lower priority task may steal
      resources from a higher priority task, this is due to the internals of
      TaskJuggler, it tries to increase the resource utilization by letting the
      lower priority task to be completed earlier than the higher priority
      task. This is done in that way if the lower priority task is dependent of
      more important tasks (tasks in critical path or tasks with critical
      resources). Read TaskJuggler documentation for more information on how
      TaskJuggler schedules tasks.

    :param allocation_strategy: Defines the allocation strategy for resources
      of a task with alternative resources. Should be one of ['minallocated',
      'maxloaded', 'minloaded', 'order', 'random'] and the default value is
      'minallocated'. For more information read the :class:`.Task` class
      documetation.

    :param persistent_allocation: Specifies that once a resource is picked from
      the list of alternatives this resource is used for the whole task. The
      default value is True. For more information read the :class:`.Task` class
      documentation.

    :param good: It is possible to attach a good to this Task to be able to
      filter and group them later on.

    """
    from stalker import defaults
    __auto_name__ = False
    __tablename__ = "Tasks"
    __mapper_args__ = {'polymorphic_identity': "Task"}
    task_id = Column(
        "id", Integer, ForeignKey('Entities.id'), primary_key=True,
        doc="""The ``primary_key`` attribute for the ``Tasks`` table used by
        SQLAlchemy to map this Task in relationships.
        """
    )
    __id_column__ = 'task_id'

    project_id = Column(
        'project_id', Integer, ForeignKey('Projects.id'),
        doc="""The id of the owner :class:`.Project` of this Task. This
        attribute is mainly used by **SQLAlchemy** to map a :class:`.Project`
        instance to a Task.
        """
    )
    _project = relationship(
        'Project',
        primaryjoin='Tasks.c.project_id==Projects.c.id',
        back_populates='tasks',
        uselist=False,
        post_update=True,
    )

    tasks = synonym(
        'children',
        doc="""A synonym for the :attr:`.children` attribute used by the
        descendants of the :class:`Task` class (currently :class:`.Asset`,
        :class:`.Shot` and :class:`.Sequence` classes).
        """
    )

    is_milestone = Column(
        Boolean,
        doc="""Specifies if this Task is a milestone.

        Milestones doesn't need any duration, any effort and any resources. It
        is used to create meaningful dependencies between the critical stages
        of the project.
        """
    )

    depends = association_proxy(
        'task_depends_to',
        'depends_to',
        creator=lambda n: TaskDependency(depends_to=n)
    )

    dependent_of = association_proxy(
        'task_dependent_of',
        'task',
        creator=lambda n: TaskDependency(task=n)
    )

    task_depends_to = relationship(
        'TaskDependency',
        back_populates='task',
        cascade="all, delete-orphan",
        primaryjoin='Tasks.c.id==Task_Dependencies.c.task_id',
        doc="""A list of :class:`.Task` s that this one is depending on.

        A CircularDependencyError will be raised when the task dependency
        creates a circular dependency which means it is not allowed to create
        a dependency for this Task which is depending on another one which in
        some way depends to this one again."""
    )

    task_dependent_of = relationship(
        'TaskDependency',
        back_populates='depends_to',
        cascade="all, delete-orphan",
        primaryjoin='Tasks.c.id==Task_Dependencies.c.depends_to_id',
        doc="""A list of :class:`.Task` s that this one is being depended by.

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
        back_populates="tasks",
        doc="The list of :class:`.User` s assigned to this Task."
    )

    alternative_resources = relationship(
        "User",
        secondary="Task_Alternative_Resources",
        primaryjoin="Tasks.c.id==Task_Alternative_Resources.c.task_id",
        secondaryjoin="Task_Alternative_Resources.c.resource_id==Users.c.id",
        backref="alternative_resource_in_tasks",
        doc="The list of :class:`.User` s assigned to this Task as an "
            "alternative resource."
    )

    allocation_strategy = Column(
        Enum(*defaults.allocation_strategy,
             name='ResourceAllocationStrategy'),
        default=defaults.allocation_strategy[0],
        nullable=False,
        doc="Please read :class:`.Task` class documentation for details."
    )

    persistent_allocation = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Please read :class:`.Task` class documentation for details."
    )

    watchers = relationship(
        'User',
        secondary='Task_Watchers',
        primaryjoin='Tasks.c.id==Task_Watchers.c.task_id',
        secondaryjoin='Task_Watchers.c.watcher_id==Users.c.id',
        back_populates='watching',
        doc="The list of :class:`.User` s watching this Task."
    )

    _responsible = relationship(
        'User',
        secondary='Task_Responsible',
        primaryjoin='Tasks.c.id==Task_Responsible.c.task_id',
        secondaryjoin='Task_Responsible.c.responsible_id==Users.c.id',
        back_populates='responsible_of',
        doc="The list of :class:`.User` s responsible from this Task."
    )

    priority = Column(
        Integer,
        doc="""An integer number between 0 and 1000 used by TaskJuggler to
        determine the priority of this Task. The default value is 500."""
    )

    time_logs = relationship(
        "TimeLog",
        primaryjoin="TimeLogs.c.task_id==Tasks.c.id",
        back_populates="task",
        cascade='all, delete-orphan',
        doc="""A list of :class:`.TimeLog` instances showing who and when has
        spent how much effort on this task."""
    )

    versions = relationship(
        "Version",
        primaryjoin="Versions.c.task_id==Tasks.c.id",
        back_populates="task",
        cascade='all, delete-orphan',
        doc="""A list of :class:`.Version` instances showing the files created
        for this task.
        """
    )

    _computed_resources = relationship(
        "User",
        secondary="Task_Computed_Resources",
        primaryjoin="Tasks.c.id==Task_Computed_Resources.c.task_id",
        secondaryjoin="Task_Computed_Resources.c.resource_id==Users.c.id",
        backref="computed_resource_in_tasks",
        doc="A list of :class:`.User` s computed by TaskJuggler. It is the "
            "result of scheduling."
    )

    bid_timing = Column(
        Float, nullable=True, default=0,
        doc="""The value of the initial bid of this Task. It is an integer or
        a float.
        """
    )

    bid_unit = Column(
        Enum(*defaults.datetime_units, name='TimeUnit'),
        nullable=True,
        doc="""The unit of the initial bid of this Task. It is a string value.
        And should be one of 'min', 'h', 'd', 'w', 'm', 'y'.
        """
    )

    _schedule_seconds = Column(
        "schedule_seconds",
        Integer, nullable=True,
        doc='cache column for schedule_seconds'
    )

    _total_logged_seconds = Column(
        "total_logged_seconds",
        Integer, nullable=True,
        doc='cache column for total_logged_seconds'
    )

    reviews = relationship(
        "Review",
        primaryjoin="Reviews.c.task_id==Tasks.c.id",
        back_populates="task",
        cascade='all, delete-orphan',
        doc="""A list of :class:`.Review` holding the details about the reviews
        created for this task."""
    )

    _review_number = Column("review_number", Integer, default=0)

    good_id = Column(Integer, ForeignKey('Goods.id'))

    good = relationship(
        'Good',
        primaryjoin='Tasks.c.good_id==Goods.c.id',
        uselist=False,
        post_update=True,
    )

    # TODO: Add ``unmanaged`` attribute for Asset management only tasks.
    #
    # Some tasks are created for asset management purposes only and doesn't
    # need TimeLogs to be entered. Create an attribute called ``unmanaged`` and
    # and set it to False by default, and if its True don't include it in the
    # TaskJuggler project. And do not track its status.

    def __init__(self,
                 project=None,
                 parent=None,
                 depends=None,
                 resources=None,
                 alternative_resources=None,
                 responsible=None,
                 watchers=None,
                 start=None,
                 end=None,
                 schedule_timing=1.0,
                 schedule_unit='h',
                 schedule_model=None,
                 schedule_constraint=0,
                 bid_timing=None,
                 bid_unit=None,
                 is_milestone=False,
                 priority=defaults.task_priority,
                 allocation_strategy=defaults.allocation_strategy[0],
                 persistent_allocation=True,
                 good=None,
                 **kwargs):
        # temp attribute for remove event
        self._previously_removed_dependent_tasks = []

        # update kwargs with extras
        kwargs['start'] = start
        kwargs['end'] = end

        kwargs['schedule_timing'] = schedule_timing
        kwargs['schedule_unit'] = schedule_unit
        kwargs['schedule_model'] = schedule_model
        kwargs['schedule_constraint'] = schedule_constraint

        super(Task, self).__init__(**kwargs)

        # call the mixin __init__ methods
        StatusMixin.__init__(self, **kwargs)
        DateRangeMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)

        kwargs['parent'] = parent
        DAGMixin.__init__(self, **kwargs)

        self._review_number = 0

        # self.parent = parent
        self._project = project

        self.time_logs = []
        self.versions = []

        self.is_milestone = is_milestone

        # update the status
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            self.status = self.status_list['WFD']

        if depends is None:
            depends = []

        self.depends = depends

        if self.is_milestone:
            resources = None

        if resources is None:
            resources = []
        self.resources = resources

        if alternative_resources is None:
            alternative_resources = []
        self.alternative_resources = alternative_resources

        # for newly created tasks set the computed_resources to resources
        self.computed_resources = self.resources

        if watchers is None:
            watchers = []
        self.watchers = watchers

        if bid_timing is None:
            bid_timing = self.schedule_timing

        if bid_unit is None:
            bid_unit = self.schedule_unit

        self.bid_timing = bid_timing
        self.bid_unit = bid_unit
        self.priority = priority
        if responsible is None:
            responsible = []
        self.responsible = responsible

        self.allocation_strategy = allocation_strategy
        self.persistent_allocation = persistent_allocation

        self.update_status_with_dependent_statuses()

        self.good = good

    @reconstructor
    def __init_on_load__(self):
        """update defaults on load
        """
        # temp attribute for remove event
        self._previously_removed_dependent_tasks = []

    def __eq__(self, other):
        """the equality operator
        """
        return super(Task, self).__eq__(other) and isinstance(other, Task) \
            and self.project == other.project and self.parent == other.parent \
            and self.depends == other.depends and self.start == other.start \
            and self.end == other.end and self.resources == other.resources

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Task, self).__hash__()

    @validates("time_logs")
    def _validate_time_logs(self, key, time_log):
        """validates the given time_logs value
        """
        if not isinstance(time_log, TimeLog):
            raise TypeError(
                "%s.time_logs should be all stalker.models.task.TimeLog "
                "instances, not %s" % (
                    self.__class__.__name__, time_log.__class__.__name__
                )
            )

        # TODO: convert this to an event
        # update parents total_logged_second attribute
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            if self.parent:
                self.parent.total_logged_seconds += time_log.total_seconds

        return time_log

    @validates("_reviews")
    def _validate_reviews(self, key, review):
        """validates the given review value
        """
        from stalker.models.review import Review
        if not isinstance(review, Review):
            raise TypeError(
                "%s.reviews should be all stalker.models.review.Review "
                "instances, not %s" % (
                    self.__class__.__name__,
                    review.__class__.__name__
                )
            )
        return review

    @validates("task_depends_to")
    def _validate_task_depends_to(self, key, task_depends_to):
        """validates the given task_depends_to value
        """
        depends = task_depends_to.depends_to
        if not depends:
            # the relation is still not setup yet
            # trust to the TaskDependency class for checking the
            # depends_to attribute
            return task_depends_to

        # check the status of the current task
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            wfd = self.status_list['WFD']
            rts = self.status_list['RTS']
            wip = self.status_list['WIP']
            prev = self.status_list['PREV']
            hrev = self.status_list['HREV']
            drev = self.status_list['DREV']
            oh = self.status_list['OH']
            stop = self.status_list['STOP']
            cmpl = self.status_list['CMPL']

            from stalker.exceptions import StatusError
            if self.status in [wip, prev, hrev, drev, oh, stop, cmpl]:
                raise StatusError(
                    'This is a %(status)s task and it is not allowed to '
                    'change the dependencies of a %(status)s task' % {
                        'status': self.status.code
                    }
                )

        if self.is_container:
            if self.status == cmpl:
                raise StatusError(
                    'This is a %(status)s container task and it is not '
                    'allowed to change the dependency in %(status)s container '
                    'tasks' % {'status': self.status.code}
                )

        if not isinstance(depends, Task):
            raise TypeError(
                "All the elements in the %s.depends should be an instance of "
                "stalker.models.task.Task, not %s" %
                (self.__class__.__name__, depends.__class__.__name__)
            )

        # check for the circular dependency
        from stalker.models import check_circular_dependency
        with DBSession.no_autoflush:
            check_circular_dependency(depends, self, 'depends')
            check_circular_dependency(depends, self, 'children')

        # check for circular dependency toward the parent, non of the parents
        # should be depending to the given depends_to_task
        with DBSession.no_autoflush:
            parent = self.parent
            while parent:
                if parent in depends.depends:
                    from stalker.exceptions import CircularDependencyError
                    raise CircularDependencyError(
                        'One of the parents of %s is depending to %s' %
                        (self, depends)
                    )
                parent = parent.parent

        # update status with the new dependency
        # update towards more constrained situation
        #
        # Do not update for example to RTS if the current dependent task is
        # CMPL or STOP, this will be done by the approve or stop action in the
        # dependent task it self

        if self.status == rts:
            with DBSession.no_autoflush:
                do_update_status = False
                if depends.status in [wfd, rts, wip, oh, prev, hrev, drev, oh]:
                    do_update_status = True

            if do_update_status:
                self.status = wfd

        return task_depends_to

    @validates('schedule_timing')
    def _validate_schedule_timing(self, key, schedule_timing):
        """validates the given schedule_timing
        """
        schedule_timing = \
            ScheduleMixin._validate_schedule_timing(self, key, schedule_timing)

        # reschedule
        self._reschedule(schedule_timing, self.schedule_unit)

        return schedule_timing

    @validates('schedule_unit')
    def _validate_schedule_unit(self, key, schedule_unit):
        """validates the given schedule_unit
        """
        schedule_unit = \
            ScheduleMixin._validate_schedule_unit(self, key, schedule_unit)

        if self.schedule_timing:
            self._reschedule(self.schedule_timing, schedule_unit)

        return schedule_unit

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
            from stalker import defaults
            unit = defaults.datetime_units_to_timedelta_kwargs.get(
                schedule_unit,
                None
            )
            if not unit:  # we are in a pre flushing state do not do anything
                return

            kwargs = {
                unit['name']: schedule_timing * unit['multiplier']
            }
            calculated_duration = datetime.timedelta(**kwargs)
            if self.schedule_constraint == CONSTRAIN_NONE or \
               self.schedule_constraint == CONSTRAIN_START:
                # get end
                self._start, self._end, self._duration = \
                    self._validate_dates(self.start, None, calculated_duration)
            elif self.schedule_constraint == CONSTRAIN_END:
                # get start
                self._start, self._end, self._duration = \
                    self._validate_dates(None, self.end, calculated_duration)
            elif self.schedule_constraint == CONSTRAIN_BOTH:
                # restore duration
                self._start, self._end, self._duration = \
                    self._validate_dates(self.start, self.end, None)

            # also update cached _schedule_seconds value
            self._schedule_seconds = self.schedule_seconds

    @validates("is_milestone")
    def _validate_is_milestone(self, key, is_milestone):
        """validates the given milestone value
        """
        if is_milestone is None:
            is_milestone = False

        if not isinstance(is_milestone, bool):
            raise TypeError(
                '%(class)s.is_milestone should be a bool value (True or '
                'False), not %(is_milestone_class)s' % {
                    'class': self.__class__.__name__,
                    'is_milestone_class': is_milestone.__class__.__name__
                }
            )

        if is_milestone:
            self.resources = []

        return bool(is_milestone)

    @validates('parent')
    def _validate_parent(self, key, parent):
        """validates the given parent value
        """
        if parent is not None:
            if not isinstance(parent, Task):
                raise TypeError(
                    '%s.parent should be an instance of '
                    'stalker.models.task.Task, not %s' %
                    (self.__class__.__name__, parent.__class__.__name__)
                )

            # check for cycle
            from stalker.models import check_circular_dependency
            check_circular_dependency(self, parent, 'children')
            check_circular_dependency(self, parent, 'depends')

        old_parent = self.parent
        new_parent = parent

        if old_parent:
            old_parent.schedule_seconds -= self.schedule_seconds
            old_parent.total_logged_seconds -= self.total_logged_seconds

        # update the new parent
        if new_parent:
            # if the new parent was a leaf task before this attachment
            # set schedule_seconds to 0
            if new_parent.is_leaf:
                new_parent.schedule_seconds = self.schedule_seconds
                new_parent.total_logged_seconds = self.total_logged_seconds
            else:
                new_parent.schedule_seconds += self.schedule_seconds
                new_parent.total_logged_seconds += self.total_logged_seconds

        return parent

    @validates('_project')
    def _validates_project(self, key, project):
        """validates the given project instance
        """
        from stalker.db.session import DBSession
        if project is None:
            # check if there is a parent defined
            if self.parent:
                # use its project as the project

                # to prevent prematurely flush the parent
                with DBSession.no_autoflush:
                    project = self.parent.project

            else:
                # no project, no task, go mad again!!!
                raise TypeError(
                    '%s.project should be an instance of '
                    'stalker.models.project.Project, not %s. Or please supply '
                    'a stalker.models.task.Task with the parent argument, so '
                    'Stalker can use the project of the supplied parent task' %
                    (self.__class__.__name__, project.__class__.__name__)
                )

        from stalker import Project

        if not isinstance(project, Project):
            # go mad again it is not a project instance
            raise TypeError(
                '%s.project should be an instance of '
                'stalker.models.project.Project, not %s' %
                (self.__class__.__name__, project.__class__.__name__)
            )
        else:
            # check if there is a parent
            if self.parent:
                # check if given project is matching the parent.project
                with DBSession.no_autoflush:
                    if self.parent.project != project:
                        # don't go mad again, but warn the user that there is
                        # an ambiguity!!!
                        import warnings

                        message = \
                            'The supplied parent and the project is not ' \
                            'matching in %s, Stalker will use the parents ' \
                            'project (%s) as the parent of this %s' % (
                                self,
                                self.parent.project,
                                self.__class__.__name__
                            )

                        warnings.warn(message, RuntimeWarning)

                        # use the parent.project
                        project = self.parent.project
        return project

    @validates("priority")
    def _validate_priority(self, key, priority):
        """validates the given priority value
        """
        if priority is None:
            from stalker import defaults
            priority = defaults.task_priority

        if not isinstance(priority, (int, float)):
            raise TypeError(
                '%(class)s.priority should be an integer value between 0 and '
                '1000, not %(priority_class)s' % {
                    'class': self.__class__.__name__,
                    'priority_class': priority.__class__.__name__
                }
            )

        if priority < 0:
            priority = 0
        elif priority > 1000:
            priority = 1000

        return int(priority)

    @validates('children')
    def _validate_children(self, key, child):
        """validates the given child
        """
        # just empty the resources list
        # do it without a flush
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            self.resources = []

            # if this is the first ever child we receive
            # set total_scheduled_seconds to child's total_logged_seconds
            # and set schedule_seconds to child's schedule_seconds
            if self.is_leaf:
                # remove info from parent
                old_schedule_seconds = self.schedule_seconds
                self._total_logged_seconds = child.total_logged_seconds
                self._schedule_seconds = child.schedule_seconds
                # got a parent ?
                if self.parent:
                    # update schedule_seconds
                    self.parent._schedule_seconds -= old_schedule_seconds
                    self.parent._schedule_seconds += child.schedule_seconds

                # it was a leaf but now a parent, so set the start to max and
                # end to min
                import pytz
                self._start = datetime.datetime.max.replace(tzinfo=pytz.utc)
                self._end = datetime.datetime.min.replace(tzinfo=pytz.utc)

            # extend start and end dates
            self._expand_dates(self, child.start, child.end)

        return child

    @validates("resources")
    def _validate_resources(self, key, resource):
        """validates the given resources value
        """
        from stalker.models.auth import User

        if not isinstance(resource, User):
            raise TypeError(
                "%(class)s.resources should be a list of "
                "stalker.models.auth.User instances, not %(resource_class)s" %
                {
                    'class': self.__class__.__name__,
                    'resource_class': resource.__class__.__name__
                }
            )
        return resource

    @validates("alternative_resources")
    def _validate_alternative_resources(self, key, alt_resource):
        """validates the given alt_resource value
        """
        from stalker.models.auth import User

        if not isinstance(alt_resource, User):
            raise TypeError(
                "%(class)s.resources should be a list of "
                "stalker.models.auth.User instances, not "
                "%(alt_resource_class)s" % {
                    'class': self.__class__.__name__,
                    'alt_resource_class': alt_resource.__class__.__name__
                }
            )
        return alt_resource

    @validates("_computed_resources")
    def _validate_computed_resources(self, key, resource):
        """validates the computed resources value
        """
        from stalker.models.auth import User

        if not isinstance(resource, User):
            raise TypeError(
                "%(class)s.computed_resources should be a list of "
                "stalker.models.auth.User instances, not %(resource_class)s" %
                {
                    'class': self.__class__.__name__,
                    'resource_class': resource.__class__.__name__
                }
            )
        return resource

    def _computed_resources_getter(self):
        """getter for the _computed_resources attribute
        """
        if not self.is_scheduled:
            self._computed_resources = self.resources
        return self._computed_resources

    def _computed_resources_setter(self, new_list):
        """setter for the _computed_resources attribute
        """
        self._computed_resources = new_list

    computed_resources = synonym(
        '_computed_resources',
        descriptor=property(
            _computed_resources_getter,
            _computed_resources_setter
        )
    )

    @validates("allocation_strategy")
    def _validate_allocation_strategy(self, key, strategy):
        """validates the given allocation_strategy value
        """
        from stalker import defaults
        if strategy is None:
            strategy = defaults.allocation_strategy[0]

        from stalker import __string_types__
        if not isinstance(strategy, __string_types__):
            raise TypeError(
                '%(class)s.allocation_strategy should be one of %(defaults)s, '
                'not %(strategy_class)s' % {
                    'class': self.__class__.__name__,
                    'defaults': defaults.allocation_strategy,
                    'strategy_class': strategy.__class__.__name__
                }
            )

        if strategy not in defaults.allocation_strategy:
            raise ValueError(
                '%(class)s.allocation_strategy should be one of %(defaults)s, '
                'not %(strategy)s' % {
                    'class': self.__class__.__name__,
                    'defaults': defaults.allocation_strategy,
                    'strategy': strategy
                }
            )

        return strategy

    @validates("persistent_allocation")
    def _validate_persistent_allocation(self, key, persistent_allocation):
        """validates the given persistent_allocation value
        """
        if persistent_allocation is None:
            from stalker import defaults
            persistent_allocation = defaults.persistent_allocation

        return bool(persistent_allocation)

    @validates("watchers")
    def _validate_watchers(self, key, watcher):
        """validates the given watcher value
        """
        from stalker.models.auth import User

        if not isinstance(watcher, User):
            raise TypeError(
                "%s.watchers should be a list of "
                "stalker.models.auth.User instances not %s" %
                (self.__class__.__name__, watcher.__class__.__name__)
            )
        return watcher

    @validates("versions")
    def _validate_versions(self, key, version):
        """validates the given version value
        """
        from stalker.models.version import Version

        if not isinstance(version, Version):
            raise TypeError(
                "%(class)s.versions should only have "
                "stalker.models.version.Version instances, and not %(class)s" %
                {'class': self.__class__.__name__}
            )

        return version

    @validates('bid_timing')
    def _validate_bid_timing(self, key, bid_timing):
        """validates the given bid_timing value
        """
        if bid_timing is not None:
            if not isinstance(bid_timing, (int, float)):
                raise TypeError(
                    '%(class)s.bid_timing should be an integer or float '
                    'showing the value of the initial bid for this %(class)s, '
                    'not %(bid)s' %
                    {
                        'class': self.__class__.__name__,
                        'bid': bid_timing.__class__.__name__
                    }
                )
        return bid_timing

    @validates('bid_unit')
    def _validate_bid_unit(self, key, bid_unit):
        """validates the given bid_unit value
        """
        if bid_unit is None:
            bid_unit = 'h'

        from stalker import __string_types__, defaults
        if not isinstance(bid_unit, __string_types__):
            raise TypeError(
                '%(class)s.bid_unit should be a string value one of %(units)s '
                'showing the unit of the bid timing of this %(class)s, not '
                '%(bid)s' % {
                    'class': self.__class__.__name__,
                    'units': defaults.datetime_units,
                    'bid': bid_unit.__class__.__name__
                }
            )

        if bid_unit not in defaults.datetime_units:
            raise ValueError(
                '%(class)s.bid_unit should be a string value one of %(units)s '
                'showing the unit of the bid timing of this %(class)s, not '
                '%(bid)s' % {
                    'class': self.__class__.__name__,
                    'units': defaults.datetime_units,
                    'bid': bid_unit.__class__.__name__
                }
            )

        return bid_unit

    @classmethod
    def _expand_dates(cls, task, start, end):
        """extends the given tasks date values with the given start and end
        values
        """
        # update parents start and end date
        if task:
            if task.start > start:
                task.start = start
            if task.end < end:
                task.end = end

    # TODO: Why these methods are not in the DateRangeMixin class.
    @validates('computed_start')
    def _validate_computed_start(self, key, computed_start):
        """validates the given computed_start value
        """
        self.start = computed_start
        return computed_start

    @validates('computed_end')
    def _validate_computed_end(self, key, computed_end):
        """validates the given computed_end value
        """
        self.end = computed_end
        return computed_end

    def _validate_start(self, start_in):
        """validates the given start value
        """
        if start_in is None:
            import pytz
            start_in = self.project.round_time(datetime.datetime.now(pytz.utc))
        elif not isinstance(start_in, datetime.datetime):
            raise TypeError(
                '%s.start should be an instance of datetime.datetime, not %s' %
                (self.__class__.__name__, start_in.__class__.__name__)
            )
        return start_in

    def _start_getter(self):
        """overridden start getter
        """
        return self._start

    def _start_setter(self, start_in):
        """overridden start setter
        """
        self._start, self._end, self._duration = \
            self._validate_dates(start_in, self._end, self._duration)
        self._expand_dates(self.parent, self.start, self.end)

    def _end_getter(self):
        """overridden end getter
        """
        return self._end

    def _end_setter(self, end_in):
        """overridden end setter
        """
        # update the end only if this is not a container task
        self._start, self._end, self._duration = \
            self._validate_dates(self.start, end_in, self.duration)
        self._expand_dates(self.parent, self.start, self.end)

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
    def tjp_abs_id(self):
        """returns the calculated absolute id of this task
        """
        if self.parent:
            abs_id = self.parent.tjp_abs_id
        else:
            abs_id = self.project.tjp_id

        return '%s.%s' % (abs_id, self.tjp_id)

    @property
    def to_tjp(self):
        """TaskJuggler representation of this task
        """
        from jinja2 import Template
        from stalker import defaults
        import pytz
        temp = Template(defaults.tjp_task_template, trim_blocks=True)
        return temp.render({
            'task': self,
            'utc': pytz.utc
        })

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

    def _total_logged_seconds_getter(self):
        """The total effort spent for this Task. It is the sum of all the
        TimeLogs recorded for this task as seconds.

        :returns int: An integer showing the total seconds spent.
        """
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            if self.is_leaf:
                if self.schedule_model in 'effort':
                    logger.debug("effort based task detected!")
                    try:
                        from sqlalchemy import text
                        sql = """
                        select
                            extract(epoch from sum("TimeLogs".end - "TimeLogs".start))::int
                        from "TimeLogs"
                        where "TimeLogs".task_id = :task_id
                        """
                        engine = DBSession.connection().engine
                        result = engine.execute(text(sql), task_id=self.id).fetchone()
                        return result[0] if result[0] else 0
                    except (UnboundExecutionError, OperationalError, ProgrammingError) as e:
                        # no database connection
                        # fallback to Python
                        logger.debug('No session found! Falling back to Python')
                        seconds = 0
                        for time_log in self.time_logs:
                            seconds += time_log.total_seconds
                        return seconds
                else:
                    import pytz
                    now = datetime.datetime.now(pytz.utc)

                    if self.schedule_model == 'duration':
                        # directly return the difference between min(now - start, end - start)
                        logger.debug('duration based task detected!, '
                                     'calculating schedule_info from duration of the task')
                        daily_working_hours = 86400.0
                    elif self.schedule_model == 'length':
                        # directly return the difference between min(now - start, end - start)
                        # but use working days
                        logger.debug('length based task detected!, '
                                     'calculating schedule_info from duration of the task')
                        from stalker import defaults
                        daily_working_hours = defaults.daily_working_hours

                    if self.end <= now:
                        seconds = self.duration.days * daily_working_hours + self.duration.seconds
                    elif self.start >= now:
                        seconds = 0
                    else:
                        past = now - self.start
                        past_as_seconds = past.days * daily_working_hours + past.seconds
                        logger.debug('past_as_seconds : %s' % past_as_seconds)
                        seconds = past_as_seconds
                    return seconds
            else:
                if self._total_logged_seconds is None:
                    self.update_schedule_info()
                return self._total_logged_seconds

    def _total_logged_seconds_setter(self, seconds):
        """Setter for total_logged_seconds. Mainly used for container tasks, to
        cache the child logged_seconds

        :param seconds: An integer value for the seconds
        """
        # only set for container tasks
        if self.is_container:
            # update parent
            old_value = 0
            if self._total_logged_seconds:
                old_value = self._total_logged_seconds
            self._total_logged_seconds = seconds
            if self.parent:
                self.parent.total_logged_seconds = \
                    self.parent.total_logged_seconds - old_value + seconds

    total_logged_seconds = synonym(
        '_total_logged_seconds',
        descriptor=property(
            _total_logged_seconds_getter,
            _total_logged_seconds_setter
        )
    )

    def _schedule_seconds_getter(self):
        """returns the total effort, length or duration in seconds, for
        completeness calculation
        """
        # for container tasks use the children schedule_seconds attribute
        if self.is_container:
            if self._schedule_seconds is None or self._schedule_seconds < 0:
                self.update_schedule_info()
            return self._schedule_seconds
        else:
            return self.to_seconds(
                self.schedule_timing,
                self.schedule_unit,
                self.schedule_model
            )

    def _schedule_seconds_setter(self, seconds):
        """Sets the schedule_seconds of this task. Mainly used for container
        tasks.

        :param seconds: An integer value of schedule_seconds for this task.
        :return:
        """
        # do it only for container tasks
        if self.is_container:
            # also update the parents
            from stalker.db.session import DBSession
            with DBSession.no_autoflush:
                if self.parent:
                    current_value = 0
                    if self._schedule_seconds:
                        current_value = self._schedule_seconds
                    self.parent.schedule_seconds = \
                        self.parent.schedule_seconds - current_value + seconds
                self._schedule_seconds = seconds

    schedule_seconds = synonym(
        '_schedule_seconds',
        descriptor=property(
            _schedule_seconds_getter,
            _schedule_seconds_setter
        )
    )

    def update_schedule_info(self):
        """updates the total_logged_seconds and schedule_seconds attributes by
        using the children info and triggers an update on every children
        """
        if self.is_container:
            total_logged_seconds = 0
            schedule_seconds = 0
            logger.debug('updating schedule info for : %s' % self.name)
            for child in self.children:
                # update children if they are a container task
                if child.is_container:
                    child.update_schedule_info()
                    if child.schedule_seconds:
                        schedule_seconds += child.schedule_seconds
                    if child.total_logged_seconds:
                        total_logged_seconds += child.total_logged_seconds
                else:
                    # DRY please!!!!
                    schedule_seconds += child.schedule_seconds if child.schedule_seconds else 0
                    total_logged_seconds += child.total_logged_seconds if child.total_logged_seconds else 0

            self._schedule_seconds = schedule_seconds
            self._total_logged_seconds = total_logged_seconds
        else:
            self._schedule_seconds = self.schedule_seconds
            self._total_logged_seconds = self.total_logged_seconds

    @property
    def percent_complete(self):
        """returns the percent_complete based on the total_logged_seconds and
        schedule_seconds of the task. Container tasks will use info from their
        children
        """
        if self.is_container:
            if self.total_logged_seconds is None or \
               self.schedule_seconds is None:
                self.update_schedule_info()

        return self.total_logged_seconds / float(self.schedule_seconds) * 100.0

    @property
    def remaining_seconds(self):
        """returns the remaining amount of efforts, length or duration left
        in this Task as seconds.
        """
        # for effort based tasks use the time_logs
        return self.schedule_seconds - self.total_logged_seconds

    def _responsible_getter(self):
        """returns the current responsible of this task
        """
        if not self._responsible:
            # traverse parents
            for parent in reversed(self.parents):
                if parent.responsible:
                    import copy
                    self._responsible = copy.copy(parent.responsible)

        # so parents do not have a responsible
        return self._responsible

    def _responsible_setter(self, responsible):
        """sets the responsible attribute

        :param responsible: A :class:`.User` instance
        """
        self._responsible = responsible

    @validates('_responsible')
    def _validate_responsible(self, key, responsible):
        """validates the given responsible value (each responsible)
        """
        from stalker.models.auth import User
        if not isinstance(responsible, User):
            raise TypeError(
                '%s.responsible should be a list of '
                'stalker.models.auth.User instances, not %s' %
                (self.__class__.__name__, responsible.__class__.__name__)
            )
        return responsible

    responsible = synonym(
        '_responsible',
        descriptor=property(
            _responsible_getter,
            _responsible_setter,
            doc="""The responsible of this task.

            This attribute will return the responsible of this task which is a
            list of :class:`.User` instances. If there is no responsible set
            for this task, then it will try to find a responsible in its
            parents.
            """
        )
    )

    @property
    def tickets(self):
        """returns the tickets referencing this task in their links attribute
        """
        from stalker import Ticket
        return Ticket.query.filter(Ticket.links.contains(self)).all()

    @property
    def open_tickets(self):
        """returns the open tickets referencing this task in their links
        attribute
        """
        from stalker import Ticket, Status
        status_closed = Status.query.filter(Status.name == 'Closed').first()
        return Ticket.query\
            .filter(Ticket.links.contains(self))\
            .filter(Ticket.status != status_closed).all()

    def walk_dependencies(self, method=1):
        """Walks the dependencies of this task

        :param method: The walk method, 0: Depth First, 1: Breadth First
        """
        from stalker.models import walk_hierarchy
        for t in walk_hierarchy(self, 'depends', method=method):
            yield t

    @validates('good')
    def _validate_good(self, key, good):
        """validates the given good value
        """
        from stalker import Good
        if good is not None and not isinstance(good, Good):
            raise TypeError(
                '%s.good should be a stalker.models.budget.Good instance, not '
                '%s' % (self.__class__.__name__, good.__class__.__name__)
            )
        return good

    # =============
    # ** ACTIONS **
    # =============
    def create_time_log(self, resource, start, end):
        """A helper method to create TimeLogs, this will ease creating TimeLog
        instances for task.
        """
        # all the status checks are now part of TimeLog._validate_task
        # create a TimeLog
        return TimeLog(task=self, resource=resource, start=start, end=end)
        # also updating parent statuses are done in TimeLog._validate_task

    def request_review(self):
        """Creates and returns Review instances for each of the responsible of
        this task and sets the task status to PREV.

        .. versionadded:: 0.2.0
          Request review will not cap the timing of this task anymore.

        Only applicable to leaf tasks.
        """
        # check task status
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            wip = self.status_list['WIP']
            prev = self.status_list['PREV']

        if self.status != wip:
            from stalker.exceptions import StatusError
            raise StatusError(
                '%(task)s (id:%(id)s) is a %(status)s task, and %(status)s '
                'tasks are not suitable for requesting a review, please '
                'supply a WIP task instead.' % {
                    'task': self.name,
                    'id': self.id,
                    'status': self.status.code
                }
            )

        # create Review instances for each Responsible of this task
        from stalker.models.review import Review
        reviews = []
        for responsible in self.responsible:
            reviews.append(
                Review(
                    task=self,
                    reviewer=responsible
                )
            )

        # update the status to PREV
        self.status = prev

        # no need to update parent or dependent task statuses
        return reviews

    def request_revision(self, reviewer=None, description='',
                         schedule_timing=1, schedule_unit='h'):
        """Requests revision.

        Applicable to PREV or CMPL leaf tasks. This method will expand the
        schedule timings of the task according to the supplied arguments.

        When request_revision is called on a PREV task, the other NEW Review
        instances (those created when request_review on a WIP task is called
        and still waiting a review) will be deleted.

        This method at the end will return a new Review instance with correct
        attributes (reviewer, description, schedule_timing, schedule_unit and
        review_number attributes).

        :param reviewer: This is the user that requested the revision. He/she
          doesn't need to be the responsible, anybody that has a Permission to
          create a Review instance can request a revision.

        :param str description: The description of the requested revision.

        :param int schedule_timing: The timing value of the requested revision.
          The task will be extended this much of duration. Works along with the
          ``schedule_unit`` parameter. The default value is 1.

        :param str schedule_unit: The timin unit value of the requested
          revision. The task will be extended this much of duration. Works
          along with the ``schedule_timing`` parameter. The default value is
          'h' for 'hour'.

        :type reviewer: class:`.User`
        """
        # check status
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            prev = self.status_list['PREV']
            cmpl = self.status_list['CMPL']

        if self.status not in [prev, cmpl]:
            from stalker.exceptions import StatusError
            raise StatusError(
                '%(task)s (id: %(id)s) is a %(status)s task, and it is not '
                'suitable for requesting a revision, please supply a PREV or '
                'CMPL task' % {
                    'task': self.name,
                    'id': self.id,
                    'status': self.status.code
                }
            )

        # *********************************************************************
        # TODO: I don't like this part, find another way to delete them
        #       directly
        # find other NEW Reviews and delete them
        reviews_to_be_deleted = []
        for r in self.reviews:
            if r.status.code == 'NEW':
                reviews_to_be_deleted.append(r)

        for r in reviews_to_be_deleted:
            logger.debug('removing %s from task.reviews' % r)
            self.reviews.remove(r)
            r.task = None
            try:
                DBSession.delete(r)
            except InvalidRequestError:
                # not persisted yet
                # do nothing
                pass
        # *********************************************************************

        # create a Review instance with the given data
        from stalker.models.review import Review
        review = Review(reviewer=reviewer, task=self)
        # and call request_revision in the Review instance
        review.request_revision(
            schedule_timing=schedule_timing,
            schedule_unit=schedule_unit,
            description=description
        )
        return review

    def hold(self):
        """Pauses the execution of this task by setting its status to OH. Only
        applicable to RTS and WIP tasks, any task with other statuses will
        raise a ValueError.
        """
        # check if status is WIP
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            wip = self.status_list['WIP']
            drev = self.status_list['DREV']
            oh = self.status_list['OH']

        if self.status not in [wip, drev, oh]:
            from stalker.exceptions import StatusError
            raise StatusError(
                '%(task)s (id:%(id)s) is a %(status)s task, only WIP or DREV '
                'tasks can be set to On Hold' % {
                    'task': self.name,
                    'id': self.id,
                    'status': self.status.code
                }
            )
        # update the status to OH
        self.status = oh

        # set the priority to 0
        self.priority = 0

        # no need to update the status of dependencies nor parents

    def stop(self):
        """Stops this task. It is nearly equivalent to deleting this task. But
        this will at least preserve the TimeLogs entered for this task. It is
        only possible to stop WIP tasks.

        You can use :meth:`.resume` to resume the task.

        The only difference between :meth:`.hold` (other than setting the task
        to different statuses) is the schedule info, while the :meth:`.hold`
        method will preserve the schedule info, stop() will set the schedule
        info to the current effort.

        So if 2 days of effort has been entered for a 4 days task, when stopped
        the task effort will be capped to 2 days, thus TaskJuggler will not try
        to reserve any resource for this task anymore.

        Also, STOP tasks will be ignored in dependency relations.
        """

        # check the status
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            wip = self.status_list['WIP']
            drev = self.status_list['DREV']
            stop = self.status_list['STOP']

        if self.status not in [wip, drev, stop]:
            from stalker.exceptions import StatusError
            raise StatusError(
                '%(task)s (id:%(id)s)is a %(status)s task and it is not '
                'possible to stop a %(status)s task.' % {
                    'task': self.name,
                    'id': self.id,
                    'status': self.status.code
                }
            )

        # set the status
        self.status = stop

        # clamp schedule values
        self.schedule_timing, self.schedule_unit = \
            self.least_meaningful_time_unit(self.total_logged_seconds)

        # update parent statuses
        self.update_parent_statuses()

        # update dependent task statuses
        for dep in self.dependent_of:
            dep.update_status_with_dependent_statuses()

    def resume(self):
        """Resumes the execution of this task by setting its status to RTS or
        WIP depending to its time_logs attribute, so if it has TimeLogs then it
        will resume as WIP and if it doesn't then it will resume as RTS. Only
        applicable to Tasks with status OH.
        """
        # check status
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            wip = self.status_list['WIP']
            oh = self.status_list['OH']
            stop = self.status_list['STOP']

        if self.status not in [oh, stop]:
            from stalker.exceptions import StatusError
            raise StatusError(
                '%(task)s (id:%(id)s) is a %(status)s task, and it is not '
                'suitable to be resumed, please supply an OH or STOP task' %
                {
                    'task': self.name,
                    'id': self.id,
                    'status': self.status.code
                }
            )
        else:
            # set to WIP
            self.status = wip

        # now update the status with dependencies
        self.update_status_with_dependent_statuses()

        # and update parents statuses
        self.update_parent_statuses()

    def review_set(self, review_number=None):
        """returns the reviews with the given review_number, if review_number
        is skipped it will return the latest set of reviews
        """

        review_set = []
        if review_number is None:
            if self.status.code == 'PREV':
                review_number = self.review_number + 1
            else:
                review_number = self.review_number

        if not isinstance(review_number, int):
            raise TypeError(
                'review_number argument in %(class)s.review_set should be a '
                'positive integer, not %(review_number_class)s' %
                {
                    'class': self.__class__.__name__,
                    'review_number_class': review_number.__class__.__name__
                }
            )

        if review_number < 1:
            raise TypeError(
                'review_number argument in %(class)s.review_set should be a '
                'positive integer, not %(review_number)s' %
                {
                    'class': self.__class__.__name__,
                    'review_number': review_number
                }
            )

        for review in self.reviews:
            if review.review_number == review_number:
                review_set.append(review)

        return review_set

    def update_status_with_dependent_statuses(self, removing=None):
        """updates the status by looking at the dependent tasks

        :param removing: The item that is been removing right now, used for the
          remove event to overcome the update issue.
        """
        if self.is_container:
            # do nothing, its status will be decided by its children
            return

        # in case there is no database
        # try to find the statuses from the status_list attribute
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            wfd = self.status_list['WFD']
            rts = self.status_list['RTS']
            wip = self.status_list['WIP']
            hrev = self.status_list['HREV']
            drev = self.status_list['DREV']
            cmpl = self.status_list['CMPL']

        if removing:
            self._previously_removed_dependent_tasks.append(removing)
        else:
            self._previously_removed_dependent_tasks = []

        # create a new list from depends and skip_list
        dep_list = []
        for dep in self.depends:
            if dep not in self._previously_removed_dependent_tasks:
                dep_list.append(dep)

        logger.debug('self.depends : %s' % self.depends)
        logger.debug('dep_list     : %s' % dep_list)

        # if not self.depends:
        if not dep_list:
            # doesn't have any dependency
            # convert its status from WFD to RTS if necessary
            if self.status == wfd:
                self.status = rts
            elif self.status in [wip, drev]:
                if len(self.time_logs):
                    self.status = wip
                else:
                    self.status = rts
            return

        #   +--------- WFD
        #   |+-------- RTS
        #   ||+------- WIP
        #   |||+------ PREV
        #   ||||+----- HREV
        #   |||||+---- DREV
        #   ||||||+--- OH
        #   |||||||+-- STOP
        #   ||||||||+- CMPL
        #   |||||||||
        # 0b000000000

        binary_status_codes = {
            'WFD':  256,
            'RTS':  128,
            'WIP':  64,
            'PREV': 32,
            'HREV': 16,
            'DREV': 8,
            'OH':   4,
            'STOP': 2,
            'CMPL': 1
        }

        # Keep this part for future reference
        # if self.id:
        #     # use pure sql
        #     logger.debug('using pure SQL to query dependency statuses')
        #     sql_query = """
        #         select
        #             "Statuses".code
        #         from "Tasks"
        #             join "Task_Dependencies" on "Tasks".id = "Task_Dependencies".task_id
        #             join "Tasks" as "Dependent_Tasks" on "Task_Dependencies".depends_to_id = "Dependent_Tasks".id
        #             join "Statuses" on "Dependent_Tasks".status_id = "Statuses".id
        #         where "Tasks".id = %s
        #         group by "Statuses".code
        #     """ % self.id
        #
        #     result = DBSession.connection().execute(sql_query)
        #
        #     # convert to a binary value
        #     binary_status = reduce(
        #         lambda x, y: x+y,
        #         map(lambda x: binary_status_codes[x[0]], result.fetchall()),
        #         0
        #     )
        #
        # else:
        # task is not committed yet, use Python version
        logger.debug('using pure Python to query dependency statuses')
        binary_status = 0
        dep_statuses = []
        # with DBSession.no_autoflush:
        logger.debug(
            'self.depends in update_status_with_dependent_statuses: %s' %
            self.depends
        )
        # for dep in self.depends:
        for dep in dep_list:
            # consider every status only once
            if dep.status not in dep_statuses:
                dep_statuses.append(dep.status)
                binary_status += binary_status_codes[dep.status.code]

        logger.debug('status of the task: %s' % self.status.code)
        logger.debug('binary status for dependency statuses: %s' %
                     binary_status)

        work_alone = False
        if binary_status < 4:
            work_alone = True

        status = self.status
        if work_alone:
            if self.status == wfd:
                status = rts
            elif self.status == drev:
                status = hrev
                # Expand task timing with the timing resolution if there is no
                # time left for this task
                if self.total_logged_seconds == self.schedule_seconds:
                    from stalker import defaults
                    total_seconds = \
                        self.schedule_seconds \
                        + defaults.timing_resolution.seconds
                    timing, unit = \
                        self.least_meaningful_time_unit(total_seconds)
                    self.schedule_timing = timing
                    self.schedule_unit = unit

        else:
            if self.status == rts:
                status = wfd
            elif self.status == wip:
                status = drev
            elif self.status == hrev:
                status = drev
            elif self.status == cmpl:
                status = drev

        logger.debug('setting status from %s to %s: ' % (self.status, status))
        self.status = status

        # also update parent statuses
        self.update_parent_statuses()

        # # also update dependent tasks
        # for dep in dep_list:
        #     dep.update_status_with_dependent_statuses()

    def update_parent_statuses(self):
        """updates the parent statuses of this task if any
        """
        # prevent query-invoked auto-flush
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            if self.parent:
                self.parent.update_status_with_children_statuses()

    def update_status_with_children_statuses(self):
        """updates the task status according to its children statuses
        """
        logger.debug(
            'setting statuses with child statuses for: %s' % self.name
        )

        if not self.is_container:
            # do nothing
            logger.debug('not a container returning!')
            return

        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            wfd = self.status_list['WFD']
            rts = self.status_list['RTS']
            wip = self.status_list['WIP']
            cmpl = self.status_list['CMPL']

        parent_statuses_lut = [wfd, rts, wip, cmpl]

        #   +--------- WFD
        #   |+-------- RTS
        #   ||+------- WIP
        #   |||+------ PREV
        #   ||||+----- HREV
        #   |||||+---- DREV
        #   ||||||+--- OH
        #   |||||||+-- STOP
        #   ||||||||+- CMPL
        #   |||||||||
        # 0b000000000

        binary_status_codes = {
            'WFD':  256,
            'RTS':  128,
            'WIP':  64,
            'PREV': 32,
            'HREV': 16,
            'DREV': 8,
            'OH':   4,
            'STOP': 2,
            'CMPL': 1
        }

        # use Python
        logger.debug('using pure Python to query children statuses')
        binary_status = 0
        children_statuses = []
        for child in self.children:
            # consider every status only once
            if child.status not in children_statuses:
                children_statuses.append(child.status)
                binary_status += binary_status_codes[child.status.code]

        #
        # I know that the following list seems cryptic but the it shows the
        # final status index in parent_statuses_lut[] list.
        #
        # So by using the cumulative statuses of children we got an index from
        # the following table, and use the found element (integer) as the index
        # for the parent_statuses_lut[] list, and we find the desired status
        #
        # We are doing it in this way for a couple of reasons:
        #
        #   1. We shouldn't hold the statuses in the following list,
        #   2. Using a dictionary is another alternative, where the keys are
        #      the cumulative binary status codes, but at the end the result of
        #      this cumulative thing is a number between 0-511 so no need to
        #      use a dictionary with integer keys
        #
        children_to_parent_statuses_lut = [
            0, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2
        ]

        status_index = children_to_parent_statuses_lut[binary_status]
        status = parent_statuses_lut[status_index]

        logger.debug('binary statuses value : %s' % binary_status)
        logger.debug('setting status to : %s' % status.code)

        self.status = status

        # # update dependent task statuses
        # for dep in self.dependent_of:
        #     dep.update_status_with_dependent_statuses()

        # go to parents
        self.update_parent_statuses()

    def _review_number_getter(self):
        """returns the revision number value
        """
        return self._review_number

    review_number = synonym(
        '_review_number',
        descriptor=property(_review_number_getter),
        doc="returns the _review_number attribute value"
    )

    def _template_variables(self):
        """variables used in rendering the filename template
        """
        # TODO: add test for this template variables
        from stalker import Shot

        sequences = []
        scenes = []
        if isinstance(self, Shot):
            sequences = self.sequences
            scenes = self.scenes

        # get the parent tasks
        task = self
        parent_tasks = task.parents
        parent_tasks.append(task)

        kwargs = {
            'project': self.project,
            'sequences': sequences,
            'sequence': self,
            'scenes': scenes,
            'shot': self,
            'asset': self,
            'task': self,
            'parent_tasks': parent_tasks,
            'type': self.type,
        }
        return kwargs

    @property
    def path(self):
        """The path attribute will generate a path suitable for placing the
        files under it. It will use the :class:`.FilenameTemplate` class
        related to the :class:`.Project` :class:`.Structure` with the
        ``target_entity_type`` is set to the type of this instance.
        """
        kwargs = self._template_variables()

        # get a suitable FilenameTemplate
        structure = self.project.structure

        from stalker import FilenameTemplate

        task_template = None
        if structure:
            for template in structure.templates:
                assert isinstance(template, FilenameTemplate)
                if template.target_entity_type == self.entity_type:
                    task_template = template
                    break

        if not task_template:
            raise RuntimeError(
                "There are no suitable FilenameTemplate "
                "(target_entity_type == '%(entity_type)s') defined in the "
                "Structure of the related Project instance, please create a "
                "new stalker.models.template.FilenameTemplate instance with "
                "its 'target_entity_type' attribute is set to "
                "'%(entity_type)s' and assign it to the `templates` attribute "
                "of the structure of the project" % {
                    'entity_type': self.entity_type
                }
            )

        import jinja2

        return os.path.normpath(
            jinja2.Template(task_template.path).render(**kwargs)
        ).replace('\\', '/')

    @property
    def absolute_path(self):
        """the absolute_path attribute
        """
        return os.path.normpath(
            os.path.expandvars(
                self.path
            )
        ).replace('\\', '/')


class TaskDependency(Base, ScheduleMixin):
    """The association object used in Task-to-Task dependency relation
    """

    from stalker import defaults
    __default_schedule_attr_name__ = 'gap'  # used in docstrings coming from
                                            # ScheduleMixin
    __default_schedule_models__ = defaults.task_dependency_gap_models
    __default_schedule_timing__ = 0
    __default_schedule_unit__ = 'h'

    __tablename__ = "Task_Dependencies"

    # depends_to_id
    depends_to_id = Column(
        Integer,
        ForeignKey("Tasks.id"),
        primary_key=True
    )

    # depends_to
    depends_to = relationship(
        Task,
        back_populates='task_dependent_of',
        primaryjoin='Task.task_id==TaskDependency.depends_to_id',
    )

    # task_id
    task_id = Column(
        Integer,
        ForeignKey("Tasks.id"),
        primary_key=True
    )

    # task
    task = relationship(
        Task,
        back_populates='task_depends_to',
        primaryjoin="Task.task_id==TaskDependency.task_id",
    )

    dependency_target = Column(
        Enum(*defaults.task_dependency_targets, name='TaskDependencyTarget'),
        nullable=False,
        doc="""The dependency target of the relation. The default value is
        "onend", which will create a dependency between two tasks so that the
        depending task will start after the task that it is depending to is
        finished.

        The dependency_target attribute is updated to "onstart" when a task has
        a revision and needs to work together with its depending tasks.
        """,
        default=defaults.task_dependency_targets[0]
    )

    gap_timing = synonym(
        'schedule_timing',
        doc="""A positive float value showing the desired gap between the
        dependent and dependee tasks. The meaning of the gap value, either is
        it *work time* or *calendar time* is defined by the :attr:`.gap_model`
        attribute. So when the gap model is "duration" then the value of `gap`
        is in calendar time, if `gap` is "length" then it is considered as work
        time.
        """
    )

    gap_unit = synonym('schedule_unit')

    gap_model = synonym(
        'schedule_model',
        doc="""An enumeration value one of ["length", "duration"]. The value of
        this attribute defines if the :attr:`.gap` value is in *Work Time* or
        *Calendar Time*. The default value is "length" so the gap value defines
        a time interval in work time.
        """
    )

    def __init__(self, task=None, depends_to=None, dependency_target=None,
                 gap_timing=0, gap_unit='h', gap_model='length'):

        ScheduleMixin.__init__(
            self, schedule_timing=gap_timing, schedule_unit=gap_unit,
            schedule_model=gap_model
        )

        self.task = task
        self.depends_to = depends_to
        self.dependency_target = dependency_target

    @validates("task")
    def _validate_task(self, key, task):
        """validates the task value
        """
        if task is not None:
            # trust to the session for checking the task
            if not isinstance(task, Task):
                raise TypeError(
                    '%s.task should be and instance of '
                    'stalker.models.task.Task, not %s' % (
                        self.__class__.__name__, task.__class__.__name__
                    )
                )
        return task

    @validates("depends_to")
    def _validate_depends_to(self, key, dep):
        """validates the task value
        """
        if dep is not None:
            # trust to the session for checking the depends_to attribute
            if not isinstance(dep, Task):
                raise TypeError(
                    '%s.depends_to can should be and instance of '
                    'stalker.models.task.Task, not %s' % (
                        self.__class__.__name__, dep.__class__.__name__
                    )
                )
        return dep

    @validates('dependency_target')
    def _validate_dependency_target(self, key, dep_target):
        """validates the given dep_target value
        """
        from stalker import defaults
        if dep_target is None:
            dep_target = defaults.task_dependency_targets[0]

        from stalker import __string_types__
        if not isinstance(dep_target, __string_types__):
            raise TypeError(
                '%s.dependency_target should be a string with a value one of '
                '%s, not %s' % (
                    self.__class__.__name__, defaults.task_dependency_targets,
                    dep_target.__class__.__name__
                )
            )

        if dep_target not in defaults.task_dependency_targets:
            raise ValueError(
                "%s.dependency_target should be one of %s, not '%s'" % (
                    self.__class__.__name__, defaults.task_dependency_targets,
                    dep_target
                )
            )

        return dep_target

    @property
    def to_tjp(self):
        """TaskJuggler representation of this TaskDependency
        """
        from jinja2 import Template

        template_variables = {
            'task': self.task,
            'depends_to': self.depends_to,
            'dependency_target': self.dependency_target,
            'gap_timing': self.gap_timing,
            'gap_unit': self.gap_unit,
            'gap_model': self.gap_model
        }

        from stalker import defaults
        temp = Template(
            defaults.tjp_task_dependency_template,
            trim_blocks=True
        )
        return temp.render(template_variables)


# TASK_RESOURCES
Task_Resources = Table(
    "Task_Resources", Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("Users.id"), primary_key=True)
)

# TASK_ALTERNATIVE_RESOURCES
Task_Alternative_Resources = Table(
    "Task_Alternative_Resources", Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("Users.id"), primary_key=True)
)

# TASK_COMPUTED_RESOURCES
Task_Computed_Resources = Table(
    "Task_Computed_Resources", Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("Users.id"), primary_key=True)
)

# TASK_WATCHERS
Task_Watchers = Table(
    "Task_Watchers", Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("watcher_id", Integer, ForeignKey("Users.id"), primary_key=True)
)

# TASK_RESPONSIBLE
Task_Responsible = Table(
    "Task_Responsible", Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("responsible_id", Integer, ForeignKey("Users.id"), primary_key=True)
)

# *****************************************************************************
# Register Events
# *****************************************************************************


# *****************************************************************************
# TimeLog updates the owner tasks parents total_logged_seconds attribute
# with new duration
@event.listens_for(TimeLog._start, 'set')
def update_time_log_task_parents_for_start(
        tlog, new_start, old_start, initiator):
    """Updates the parent task of the task related to the time_log when the
    new_start or end values are changed

    :param tlog: The TimeLog instance
    :param new_start: The datetime.datetime instance showing the new value
    :param old_start: The datetime.datetime instance showing the old value
    :param initiator: not used
    :return: None
    """
    logger.debug('Received set event for new_start in target : %s' % tlog)
    if tlog.end and old_start and new_start:
        old_duration = tlog.end - old_start
        new_duration = tlog.end - new_start
        __update_total_logged_seconds__(tlog, new_duration, old_duration)


@event.listens_for(TimeLog._end, 'set')
def update_time_log_task_parents_for_end(tlog, new_end, old_end, initiator):
    """Updates the parent task of the task related to the time_log when the
    start or new_end values are changed

    :param tlog: The TimeLog instance
    :param new_end: The datetime.datetime instance showing the new value
    :param old_end: The datetime.datetime instance showing the old value
    :param initiator: not used
    :return: None
    """
    logger.debug('Received set event for new_end in target : %s' % tlog)
    if tlog.start and isinstance(old_end, datetime.datetime) \
       and isinstance(new_end, datetime.datetime):
        old_duration = old_end - tlog.start
        new_duration = new_end - tlog.start
        __update_total_logged_seconds__(tlog, new_duration, old_duration)


def __update_total_logged_seconds__(tlog, new_duration, old_duration):
    """Updates the given parent tasks total_logged_seconds attribute with the
    new duration

    :param tlog: A :class:`.Task` instance which is the parent of the
    :param new_duration:
    :param old_duration:
    :return:
    """
    if tlog.task:
        logger.debug('TimeLog has a task: %s' % tlog.task)
        parent = tlog.task.parent
        if parent:
            logger.debug('TImeLog.task has a parent: %s' % parent)

            logger.debug('old_duration: %s' % old_duration)
            logger.debug('new_duration: %s' % new_duration)

            old_total_seconds = old_duration.days * 86400 + \
                old_duration.seconds
            new_total_seconds = new_duration.days * 86400 + \
                new_duration.seconds

            parent.total_logged_seconds = \
                parent.total_logged_seconds - old_total_seconds + \
                new_total_seconds
        else:
            logger.debug("TimeLog.task doesn't have a parent:")
    else:
        logger.debug("TimeLog doesn't have a task yet: %s" % tlog)


# *****************************************************************************
# Task.schedule_timing updates Task.parent.schedule_seconds attribute
# *****************************************************************************
@event.listens_for(Task.schedule_timing, 'set', propagate=True)
def update_parents_schedule_seconds_with_schedule_timing(
        task, new_schedule_timing, old_schedule_timing, initiator):
    """Updates the parent tasks schedule_seconds attribute when the
    schedule_timing attribute is updated on a task

    :param task: The base task
    :param new_schedule_timing: an integer showing the schedule_timing of the
      task
    :param old_schedule_timing: the old value of schedule_timing
    :param initiator: not used
    :return: None
    """
    # update parents schedule_seconds attribute
    if task.parent:
        old_schedule_seconds = task.to_seconds(
            old_schedule_timing, task.schedule_unit, task.schedule_model
        )
        new_schedule_seconds = task.to_seconds(
            new_schedule_timing, task.schedule_unit, task.schedule_model
        )
        # remove the old and add the new one
        task.parent.schedule_seconds = \
            task.parent.schedule_seconds - old_schedule_seconds + \
            new_schedule_seconds


# *****************************************************************************
# Task.schedule_unit updates Task.parent.schedule_seconds attribute
# *****************************************************************************
@event.listens_for(Task.schedule_unit, 'set', propagate=True)
def update_parents_schedule_seconds_with_schedule_unit(
        task, new_schedule_unit, old_schedule_unit, initiator):
    """Updates the parent tasks schedule_seconds attribute when the
    new_schedule_unit attribute is updated on a task

    :param task: The base task that the schedule unit is updated of
    :param new_schedule_unit: a string with a value of 'min', 'h', 'd', 'w',
      'm' or 'y' showing the timing unit.
    :param old_schedule_unit: the old value of new_schedule_unit
    :param initiator: not used
    :return: None
    """
    # update parents schedule_seconds attribute
    if task.parent:
        schedule_timing = 0
        if task.schedule_timing:
            schedule_timing = task.schedule_timing
        old_schedule_seconds = task.to_seconds(
            schedule_timing, old_schedule_unit, task.schedule_model
        )
        new_schedule_seconds = task.to_seconds(
            schedule_timing, new_schedule_unit, task.schedule_model
        )
        # remove the old and add the new one
        parent_schedule_seconds = 0
        if task.parent.schedule_seconds:
            parent_schedule_seconds = task.parent.schedule_seconds
        task.parent.schedule_seconds = \
            parent_schedule_seconds - old_schedule_seconds + \
            new_schedule_seconds


# *****************************************************************************
# Task.children removed
# *****************************************************************************
@event.listens_for(Task.children, 'remove', propagate=True)
def update_task_date_values(task, removed_child, initiator):
    """Runs when a child is removed from parent

    :param task: The task that a child is removed from
    :param removed_child: The removed child
    :param initiator: not used
    """
    # update start and end date values of the task
    from stalker.db.session import DBSession
    with DBSession.no_autoflush:
        import pytz
        start = datetime.datetime.max.replace(tzinfo=pytz.utc)
        end = datetime.datetime.min.replace(tzinfo=pytz.utc)
        for child in task.children:
            if child is not removed_child:
                if child.start < start:
                    start = child.start
                if child.end > end:
                    end = child.end

        max_date = datetime.datetime.max.replace(tzinfo=pytz.utc)
        min_date = datetime.datetime.min.replace(tzinfo=pytz.utc)
        if start != max_date and end != min_date:
            task.start = start
            task.end = end
        else:
            # no child left
            # set it to now
            import pytz
            task.start = datetime.datetime.now(pytz.utc)
            # this will also update end


# *****************************************************************************
# Task.depends set
# *****************************************************************************
@event.listens_for(Task.task_depends_to, 'remove', propagate=True)
def removed_a_dependency(task, task_dependent, initiator):
    """Runs when a task is removed from another tasks dependency list.

    :param task: The task that a dependent is being removed from.
    :param task_dependent: The association object that has the relation.
    :param initiator: not used
    """
    # update task status with dependencies
    task.update_status_with_dependent_statuses(
        removing=task_dependent.depends_to
    )


@event.listens_for(TimeLog.__table__, 'after_create')
def add_exclude_constraint(table, connection, **kwargs):
    """adds the PostgreSQL specific ExcludeConstraint
    """
    from sqlalchemy import DDL
    from sqlalchemy.exc import ProgrammingError, InternalError

    if connection.engine.dialect.name == 'postgresql':
        logger.debug('add_exclude_constraint is Running!')
        # try to create the extension first
        create_extension = DDL("CREATE EXTENSION btree_gist;")
        try:
            logger.debug('running "btree_gist" extension creation!')
            create_extension.execute(bind=connection)
            logger.debug('successfully created "btree_gist" extension!')
        except (ProgrammingError, InternalError) as e:
            logger.debug('add_exclude_constraint: %s' % e)

        # create the ts_to_box sql function
        ts_to_box = DDL("""CREATE FUNCTION ts_to_box(TIMESTAMPTZ, TIMESTAMPTZ)
RETURNS BOX
AS
$$
    SELECT  BOX(
      POINT(DATE_PART('epoch', $1), 0),
      POINT(DATE_PART('epoch', $2 - interval '1 minute'), 1)
    )
$$
LANGUAGE 'sql'
IMMUTABLE;
""")
        try:
            logger.debug(
                'creating ts_to_box function!'
            )
            ts_to_box.execute(bind=connection)
            logger.debug(
                'successfully created ts_to_box function'
            )
        except (ProgrammingError, InternalError) as e:
            logger.debug(
                'failed creating ts_to_box function!: %s' % e
            )

        # create exclude constraint
        exclude_constraint = \
            DDL("""ALTER TABLE "TimeLogs" ADD CONSTRAINT
                overlapping_time_logs EXCLUDE USING GIST (
                  resource_id WITH =,
                  ts_to_box(start, "end") WITH &&
                )"""
            )
        try:
            logger.debug(
                'running ExcludeConstraint for "TimeLogs" table creation!'
            )
            exclude_constraint.execute(bind=connection)
            logger.debug(
                'successfully created ExcludeConstraint for "TimeLogs" table!'
            )
        except (ProgrammingError, InternalError) as e:
            logger.debug(
                'failed creating ExcludeConstraint for TimeLogs table!: %s' % e
            )
    else:
        logger.debug(
            'it is not a PostgreSQL database not creating Exclude Constraint'
        )
