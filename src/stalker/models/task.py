# -*- coding: utf-8 -*-
"""Task related functions and classes are situated here."""
import copy
import datetime
import os
from typing import Any, Dict, Generator, List, Optional, TYPE_CHECKING, Union

from jinja2 import Template

import pytz

import sqlalchemy
from sqlalchemy import (
    CheckConstraint,
    Column,
    DDL,
    Enum,
    ForeignKey,
    Integer,
    Table,
    event,
    text,
)
from sqlalchemy.exc import (
    InternalError,
    InvalidRequestError,
    OperationalError,
    ProgrammingError,
    UnboundExecutionError,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    reconstructor,
    relationship,
    synonym,
    validates,
)
from sqlalchemy.orm.attributes import AttributeEvent

from stalker.db.declarative import Base
from stalker.db.session import DBSession
from stalker.exceptions import (
    CircularDependencyError,
    DependencyViolationError,
    OverBookedError,
    StatusError,
)
from stalker.log import get_logger
from stalker.models.auth import User
from stalker.models.budget import Good
from stalker.models.entity import Entity
from stalker.models.enum import (
    DependencyTarget,
    DependencyTargetDecorator,
    ScheduleConstraint,
    ScheduleModel,
    TimeUnit,
    TimeUnitDecorator,
    TraversalDirection,
)
from stalker.models.mixins import (
    DAGMixin,
    DateRangeMixin,
    ReferenceMixin,
    ScheduleMixin,
    StatusMixin,
)
from stalker.models.review import Review
from stalker.models.status import Status
from stalker.models.ticket import Ticket
from stalker.utils import check_circular_dependency, walk_hierarchy

if TYPE_CHECKING:  # pragma: no cover
    from stalker.models.project import Project
    from stalker.models.version import Version

logger = get_logger(__name__)


BINARY_STATUS_VALUES = {
    "WFD": 0b100000000,
    "RTS": 0b010000000,
    "WIP": 0b001000000,
    "PREV": 0b000100000,
    "HREV": 0b000010000,
    "DREV": 0b000001000,
    "OH": 0b000000100,
    "STOP": 0b000000010,
    "CMPL": 0b000000001,
}
"""
  +--------- WFD
  |+-------- RTS
  ||+------- WIP
  |||+------ PREV
  ||||+----- HREV
  |||||+---- DREV
  ||||||+--- OH
  |||||||+-- STOP
  ||||||||+- CMPL
  |||||||||
0b000000000
"""  # noqa: SC100


CHILDREN_TO_PARENT_STATUSES_MAP = {
    0b000000000: 0,
    0b000000001: 3,
    0b000000010: 3,
    0b000000011: 3,
    0b010000000: 1,
    0b010000010: 1,
    0b100000000: 0,
    0b100000010: 0,
    0b110000000: 1,
    0b110000010: 1,
}
"""Although the  dictionary seems cryptic, it shows the final status index in
parent_statuses_map[] list.

So by using the cumulative statuses of children we got an index from the following
table, and use the found element (integer) as the index for the parent_statuses_map[]
list, and we find the desired status.

We are doing it in this way for a couple of reasons:

  1. We shouldn't hold the statuses in the following list,
  2. We are using a sparse dictionary which is more efficient than storing
     all the data in a single list.
"""


class TimeLog(Entity, DateRangeMixin):
    """Time entry for the time spent on a :class:`.Task` by a specific :class:`.User`.

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

    Args:
        task (Task): The :class:`.Task` instance that this time log belongs to.
        resource (User): The :class:`.User` instance that this time log is created
            for.
    """

    __auto_name__ = True
    __tablename__ = "TimeLogs"
    __mapper_args__ = {"polymorphic_identity": "TimeLog"}

    __table_args__ = (
        CheckConstraint('"end" > start'),  # this will be ignored in SQLite3
    )

    time_log_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Entities.id"),
        primary_key=True,
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey("Tasks.id"),
        nullable=False,
        doc="""The id of the related task.""",
    )
    task: Mapped["Task"] = relationship(
        primaryjoin="TimeLogs.c.task_id==Tasks.c.id",
        uselist=False,
        back_populates="time_logs",
        doc="""The :class:`.Task` instance that this time log is created for""",
    )

    resource_id: Mapped[int] = mapped_column(
        ForeignKey("Users.id"),
        nullable=False,
    )
    resource: Mapped[User] = relationship(
        primaryjoin="TimeLogs.c.resource_id==Users.c.id",
        uselist=False,
        back_populates="time_logs",
        doc="""The :class:`.User` instance that this time_log is created for""",
    )

    def __init__(
        self,
        task: Optional["Task"] = None,
        resource: Optional[User] = None,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        duration: Optional[datetime.timedelta] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        super(TimeLog, self).__init__(**kwargs)
        kwargs["start"] = start
        kwargs["end"] = end
        kwargs["duration"] = duration
        DateRangeMixin.__init__(self, **kwargs)
        self.task = task
        self.resource = resource

    @validates("task")
    def _validate_task(self, key: str, task: "Task") -> "Task":
        """Validate the given task value.

        Args:
            key (str): The name of the validated column.
            task (Task): The Task instance to be validated.

        Raises:
            TypeError: If the given task is not a Task instance.
            ValueError: If this is a container task.
            StatusError: If the Task.status is one of [WDF, OH, STOP, CMPL] where it is
                not allowed to entry any further TimeLog information.
            DependencyViolationError: If this TimeLog overlaps with one of the
                dependencies start and end time, essentially forcing this Task to start
                or end before its dependencies start or end.

        Returns:
            Task: The validated task value.
        """
        if not isinstance(task, Task):
            raise TypeError(
                "{}.task should be an instance of stalker.models.task.Task, "
                "not {}: '{}'".format(
                    self.__class__.__name__, task.__class__.__name__, task
                )
            )

        if task.is_container:
            raise ValueError(
                f"{task.name} (id: {task.id}) is a container task, and it is not "
                "allowed to create TimeLogs for a container task"
            )

        # check status
        logger.debug("checking task status!")
        with DBSession.no_autoflush:
            task_status_list = task.status_list
            WFD = task_status_list["WFD"]
            RTS = task_status_list["RTS"]
            WIP = task_status_list["WIP"]
            # PREV = task_status_list["PREV"]
            HREV = task_status_list["HREV"]
            # DREV = task_status_list["DREV"]
            OH = task_status_list["OH"]
            STOP = task_status_list["STOP"]
            CMPL = task_status_list["CMPL"]

            if task.status in [WFD, OH, STOP, CMPL]:
                raise StatusError(
                    f"{task.name} is a {task.status.code} task, and it is not allowed "
                    f"to create TimeLogs for a {task.status.code} task, please supply "
                    "a RTS, WIP, HREV or DREV task!"
                )
            elif task.status in [RTS, HREV]:
                # update task status
                logger.debug("updating task status to WIP!")
                task.status = WIP

            # check dependent tasks
            logger.debug("checking dependent task statuses")
            for task_dependencies in task.task_depends_on:
                dep_task = task_dependencies.depends_on
                dependency_target = task_dependencies.dependency_target
                raise_violation_error = False
                violation_date = None

                if dependency_target == DependencyTarget.OnEnd:
                    # time log cannot start before the end date of this task
                    if self.start < dep_task.end:
                        raise_violation_error = True
                        violation_date = dep_task.end
                elif dependency_target == DependencyTarget.OnStart:
                    if self.start < dep_task.start:
                        raise_violation_error = True
                        violation_date = dep_task.start

                if raise_violation_error:
                    raise DependencyViolationError(
                        "It is not possible to create a TimeLog before "
                        f"{violation_date}, which violates the dependency relation of "
                        f'"{task.name}" to "{dep_task.name}"'
                    )

        # this may need to be in an external event, it needs to trigger a flush
        # to correctly function
        task.update_parent_statuses()

        return task

    @validates("resource")
    def _validate_resource(self, key: str, resource: User) -> User:
        """Validate the given resource value.

        Args:
            key (str): The name of the validated column.
            resource (User): The User instance as the resource of this TimeLog.

        raises:
            TypeError: If the resource is None or is not a User instance.
            OverBookedError: If the resource has already a clashing TimeLog.

        Returns:
            User: The validated User instance.
        """
        if resource is None:
            raise TypeError(f"{self.__class__.__name__}.resource cannot be None")

        if not isinstance(resource, User):
            raise TypeError(
                "{}.resource should be a stalker.models.auth.User instance, "
                "not {}: '{}'".format(
                    self.__class__.__name__, resource.__class__.__name__, resource
                )
            )

        # check for overbooking
        clashing_time_log_data = None
        with DBSession.no_autoflush:
            try:
                from sqlalchemy import or_, and_

                clashing_time_log_data = (
                    DBSession.query(TimeLog.start, TimeLog.end)
                    .filter(TimeLog.id != self.id)
                    .filter(TimeLog.resource_id == resource.id)
                    .filter(
                        or_(
                            and_(TimeLog.start <= self.start, self.start < TimeLog.end),
                            and_(TimeLog.start < self.end, self.end <= TimeLog.end),
                        )
                    )
                    .first()
                )

            except (UnboundExecutionError, OperationalError):
                # fallback to Python
                for time_log in resource.time_logs:
                    if time_log == self:
                        continue

                    if (
                        time_log.start == self.start
                        or time_log.end == self.end
                        or time_log.start < self.end < time_log.end
                        or time_log.start < self.start < time_log.end
                    ):
                        clashing_time_log_data = [time_log.start, time_log.end]
                        break

            if clashing_time_log_data:
                import tzlocal

                local_tz = tzlocal.get_localzone()
                raise OverBookedError(
                    "The resource has another TimeLog between {} and {}".format(
                        clashing_time_log_data[0].astimezone(local_tz),
                        clashing_time_log_data[1].astimezone(local_tz),
                    )
                )

        return resource

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is a TimeLog instance and has the same task,
                resource, start, end and name.
        """
        return (
            isinstance(other, TimeLog)
            and self.task is other.task
            and self.resource is other.resource
            and self.start == other.start
            and self.end == other.end
            and self.name == other.name
        )


# TODO: Consider contracting a Task with TimeLogs, what will happen when the
#       task has logged in time
# TODO: Check, what happens when a task has TimeLogs and will have child task
#       later on, will it be ok with TJ


class Task(
    Entity, StatusMixin, DateRangeMixin, ReferenceMixin, ScheduleMixin, DAGMixin
):
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

    The default :attr:`.schedule_model` for Stalker tasks is
    `ScheduleModel.Effort`, the default :attr:`TimeUnit.Hour` and the default
    value of :attr:`.schedule_timing` is defined by the
    :attr:`stalker.config.Config.timing_resolution`. So for a config where the
    ``timing_resolution`` is set to 1 hour the schedule_timing is 1.

    It is also possible to use :attr:`.ScheduleModel.Length`` or
    :attr:`.ScheduleModel.duration` values for
    :attr:`.schedule_model` (set it to :attr:`ScheduleModel.Effort`,
    :attr:`.ScheduleModel.Length` or :attr:`.ScheduleModel.Duration` to get the
    desired scheduling model).

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
      time slot where no resources were available.

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
       tasks proportional to the elapsed time from the :attr:`.start` attr
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
      |                  | not have a TimeLog or a review request cannot be  |
      |                  | made for it.                                       |
      +------------------+----------------------------------------------------+
      | Ready To Start   | A task is set to RTS when there are no             |
      | (RTS)            | dependencies or all of its dependencies are        |
      |                  | completed, so there is nothing preventing it to be |
      |                  | started. An RTS Task can have new TimeLogs. A      |
      |                  | review cannot be requested at this stage cause no |
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
      |                  | status WIP. A PREV task cannot have new TimeLogs  |
      |                  | nor a new request can be made because it is in     |
      |                  | already in review.                                 |
      +------------------+----------------------------------------------------+
      | Has Revision     | A task is set to HREV when one of its Reviews      |
      | (HREV)           | completed by requesting a review by using the      |
      |                  | :meth:`.Review.request_review` method. A HREV Task |
      |                  | can have new TimeLogs, and it will be converted to |
      |                  | a WIP or DREV depending on its dependency task     |
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
      |                  | :meth:`.Task.resume` method and depending on its   |
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
       means that you cannot change the :attr:`.computed_start` anymore), it
       is only allowed to change the dependencies of a WFD and RTS tasks.

    .. warning::
       **Resuming a STOP Task**

       Resuming a STOP Task will be treated as if a revision has been made to
       that task, and all the statuses of the tasks depending on this
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
          :attr:`.absolute_path` . The value of these attributes are the
          rendered version of the related :class:`.FilenameTemplate` which
          has its target_entity_type attribute set to "Task" (or "Asset",
          "Shot" or "Sequence" or anything matching to the derived class name,
          so it can be used in :class:`.Asset`, :class:`.Shot` and
          :class:`.Sequences` or anything that is derived from Task class) in
          the :class:`.Project` that this task belongs to. This property has
          been added to make it easier to write custom template codes for
          Project :class:`.Structure` s.

          The :attr:`.path` attribute is a repository relative path, where as
          the :attr:`.absolute_path` is the full path and includes the OS
          dependent repository path.

    .. versionadded: 0.2.13

       Task to :class:`.Good` relation. It is now possible to define the
       related Good to this task, to be able to filter tasks that are related
       to the same :class:`.Good`.

       Its main purpose of existence is to be able to generate
       :class:`.BudgetEntry` instances from the tasks that are related to the
       same :class:`.Good` and because the Goods are defining the cost and MSRP
       of different things, it is possible to create BudgetEntries and thus
       :class;`.Budget` s with this information.

    Args:
        project (Project): A Task which doesn't have a parent (a root task)
            should be created with a :class:`.Project` instance. If it is
            skipped an no :attr:`.parent` is given then Stalker will raise a
            RuntimeError. If both the ``project`` and the :attr:`.parent`
            argument contains data and the project of the Task instance given
            with parent argument is different than the Project instance given
            with the ``project`` argument then a RuntimeWarning will be raised
            and the project of the parent task will be used.
        parent (Task): The parent Task or Project of this Task. Every Task in
            Stalker should be related with a :class:`.Project` instance. So if
            no parent task is desired, at least a Project instance should be
            passed as the parent of the created Task or the Task will be an
            orphan task and Stalker will raise a RuntimeError.
        depends_on (List[Task]): A list of :class:`.Task` s that this
            :class:`.Task` is depending on. A Task cannot depend on itself or
            any other Task which are already depending on this one in anyway or
            a CircularDependency error will be raised.
        resources (List[User]): The :class:`.User` s assigned to this
            :class:`.Task`. A :class:`.Task` without any resource cannot be
            scheduled.
        responsible (List[User]): A list of :class:`.User` instances that is
            responsible of this task.
        watchers (List[User]): A list of :class:`.User` those are added this
            Task instance to their watch list.
        start (datetime.datetime): The start date and time of this task
            instance. It is only used if the :attr:`.schedule_constraint`
            attribute is set to :attr:`.ScheduleConstraint.Start` or
            :attr:`.ScheduleConstraint.Both`. The default value is
            `datetime.datetime.now(pytz.utc)`.
        end (datetime.datetime): The end date and time of this task instance.
            It is only used if the :attr:`.schedule_constraint` attribute is
            set to :attr:`.CONSTRAIN_END` or :attr:`.CONSTRAIN_BOTH`. The
            default value is `datetime.datetime.now(pytz.utc)`.
        schedule_timing (int): The value of the schedule timing.
        schedule_unit (str): The unit value of the schedule timing. Should be
            one of 'min', 'h', 'd', 'w', 'm', 'y'.
        schedule_constraint (ScheduleConstraint): The
            :class:`.ScheduleConstraint` value. The default is
            `ScheduleConstraint.NONE`.
        bid_timing (int): The initial bid for this Task. It can be used in
            measuring how accurate the initial guess was. It will be compared
            against the total amount of effort spend doing this task. Can be
            set to None, which will be set to the schedule_timing_day argument
            value if there is one or 0.
        bid_unit (str): The unit of the bid value for this Task. Should be one
            of the 'min', 'h', 'd', 'w', 'm', 'y'.
        is_milestone (bool): A bool (True or False) value showing if this task
            is a milestone which doesn't need any resource and effort.
        priority (int): It is a number between 0 to 1000 which defines the
            priority of the :class:`.Task`. The higher the value the higher its
            priority. The default value is 500. Mainly used by TaskJuggler.

            Higher priority tasks will be scheduled to an early date or at
            least will tried to be scheduled to an early date then a lower
            priority task (a task that is using the same resources).

            In complex projects, a task with a lower priority task may steal
            resources from a higher priority task, this is due to the internals
            of TaskJuggler, it tries to increase the resource utilization by
            letting the lower priority task to be completed earlier than the
            higher priority task. This is done in that way if the lower
            priority task is dependent of more important tasks (tasks in
            critical path or tasks with critical resources). Read TaskJuggler
            documentation for more information on how TaskJuggler schedules
            tasks.
        allocation_strategy (str): Defines the allocation strategy for
            resources of a task with alternative resources. Should be one of
            ['minallocated', 'maxloaded', 'minloaded', 'order', 'random'] and
            the default value is 'minallocated'. For more information read the
            :class:`.Task` class documentation.
        persistent_allocation (bool): Specifies that once a resource is picked
            from the list of alternatives this resource is used for the whole
            task. The default value is True. For more information read the
            :class:`.Task` class documentation.
        good (stalker.models.budget.Good): It is possible to attach a good to
            this Task to be able to filter and group them later on.
    """

    from stalker import defaults

    __auto_name__ = False
    __tablename__ = "Tasks"
    __mapper_args__ = {"polymorphic_identity": "Task"}
    task_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Entities.id"),
        primary_key=True,
        doc="""The ``primary_key`` attribute for the ``Tasks`` table used by
        SQLAlchemy to map this Task in relationships.
        """,
    )
    __id_column__ = "task_id"

    project_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("Projects.id"),
        doc="""The id of the owner :class:`.Project` of this Task. This
        attribute is mainly used by **SQLAlchemy** to map a :class:`.Project`
        instance to a Task.
        """,
    )
    _project: Mapped[Optional["Project"]] = relationship(
        primaryjoin="Tasks.c.project_id==Projects.c.id",
        back_populates="tasks",
        uselist=False,
        post_update=True,
    )

    tasks: Mapped[Optional[List["Task"]]] = synonym(
        "children",
        doc="""A synonym for the :attr:`.children` attribute used by the
        descendants of the :class:`Task` class (currently :class:`.Asset`,
        :class:`.Shot` and :class:`.Sequence` classes).
        """,
    )

    is_milestone: Mapped[Optional[bool]] = mapped_column(
        doc="""Specifies if this Task is a milestone.

        Milestones doesn't need any duration, any effort and any resources. It
        is used to create meaningful dependencies between the critical stages
        of the project.
        """,
    )

    depends_on = association_proxy(
        "task_depends_on", "depends_on", creator=lambda n: TaskDependency(depends_on=n)
    )

    dependent_of = association_proxy(
        "task_dependent_of", "task", creator=lambda n: TaskDependency(task=n)
    )

    task_depends_on: Mapped[Optional[List["TaskDependency"]]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
        primaryjoin="Tasks.c.id==Task_Dependencies.c.task_id",
        doc="""A list of :class:`.Task` s that this one is depending on.

        A CircularDependencyError will be raised when the task dependency
        creates a circular dependency which means it is not allowed to create
        a dependency for this Task which is depending on another one which in
        some way depends on this one again.""",
    )

    task_dependent_of: Mapped[Optional[List["TaskDependency"]]] = relationship(
        back_populates="depends_on",
        cascade="all, delete-orphan",
        primaryjoin="Tasks.c.id==Task_Dependencies.c.depends_on_id",
        doc="""A list of :class:`.Task` s that this one is being depended by.

        A CircularDependencyError will be raised when the task dependency
        creates a circular dependency which means it is not allowed to create
        a dependency for this Task which is depending on another one which in
        some way depends on this one again.
        """,
    )

    resources: Mapped[Optional[List[User]]] = relationship(
        secondary="Task_Resources",
        primaryjoin="Tasks.c.id==Task_Resources.c.task_id",
        secondaryjoin="Task_Resources.c.resource_id==Users.c.id",
        back_populates="tasks",
        doc="The list of :class:`.User` s assigned to this Task.",
    )

    alternative_resources: Mapped[Optional[List[User]]] = relationship(
        secondary="Task_Alternative_Resources",
        primaryjoin="Tasks.c.id==Task_Alternative_Resources.c.task_id",
        secondaryjoin="Task_Alternative_Resources.c.resource_id==Users.c.id",
        backref="alternative_resource_in_tasks",
        doc="The list of :class:`.User` s assigned to this Task as an "
        "alternative resource.",
    )

    allocation_strategy: Mapped[str] = mapped_column(
        Enum(*defaults.allocation_strategy, name="ResourceAllocationStrategy"),
        default=defaults.allocation_strategy[0],
        doc="Please read :class:`.Task` class documentation for details.",
    )

    persistent_allocation: Mapped[bool] = mapped_column(
        default=True,
        doc="Please read :class:`.Task` class documentation for details.",
    )

    watchers: Mapped[Optional[List[User]]] = relationship(
        secondary="Task_Watchers",
        primaryjoin="Tasks.c.id==Task_Watchers.c.task_id",
        secondaryjoin="Task_Watchers.c.watcher_id==Users.c.id",
        back_populates="watching",
        doc="The list of :class:`.User` s watching this Task.",
    )

    _responsible: Mapped[Optional[List[User]]] = relationship(
        secondary="Task_Responsible",
        primaryjoin="Tasks.c.id==Task_Responsible.c.task_id",
        secondaryjoin="Task_Responsible.c.responsible_id==Users.c.id",
        back_populates="responsible_of",
        doc="The list of :class:`.User` s responsible from this Task.",
    )

    priority: Mapped[Optional[int]] = mapped_column(
        doc="""An integer number between 0 and 1000 used by TaskJuggler to
        determine the priority of this Task. The default value is 500.""",
        default=500,
    )

    time_logs: Mapped[Optional[List[TimeLog]]] = relationship(
        primaryjoin="TimeLogs.c.task_id==Tasks.c.id",
        back_populates="task",
        cascade="all, delete-orphan",
        doc="""A list of :class:`.TimeLog` instances showing who and when has
        spent how much effort on this task.""",
    )

    versions: Mapped[Optional[List["Version"]]] = relationship(
        primaryjoin="Versions.c.task_id==Tasks.c.id",
        back_populates="task",
        cascade="all, delete-orphan",
        doc="""A list of :class:`.Version` instances showing the files created
        for this task.
        """,
    )

    _computed_resources: Mapped[Optional[List[User]]] = relationship(
        secondary="Task_Computed_Resources",
        primaryjoin="Tasks.c.id==Task_Computed_Resources.c.task_id",
        secondaryjoin="Task_Computed_Resources.c.resource_id==Users.c.id",
        backref="computed_resource_in_tasks",
        doc="A list of :class:`.User` s computed by TaskJuggler. It is the "
        "result of scheduling.",
    )

    bid_timing: Mapped[Optional[float]] = mapped_column(
        default=0,
        doc="""The value of the initial bid of this Task. It is an integer or
        a float.
        """,
    )

    bid_unit: Mapped[Optional[TimeUnit]] = mapped_column(
        TimeUnitDecorator,
        doc="""The unit of the initial bid of this Task. It is a string value.
        And should be one of 'min', 'h', 'd', 'w', 'm', 'y'.
        """,
    )

    _schedule_seconds: Mapped[Optional[int]] = mapped_column(
        "schedule_seconds",
        Integer,
        nullable=True,
        doc="cache column for schedule_seconds",
    )

    _total_logged_seconds: Mapped[Optional[int]] = mapped_column(
        "total_logged_seconds",
        doc="cache column for total_logged_seconds",
    )

    reviews: Mapped[Optional[List[Review]]] = relationship(
        primaryjoin="Reviews.c.task_id==Tasks.c.id",
        back_populates="task",
        cascade="all, delete-orphan",
        doc="""A list of :class:`.Review` holding the details about the reviews
        created for this task.""",
    )

    _review_number: Mapped[Optional[int]] = mapped_column("review_number", default=0)

    good_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Goods.id"))

    good: Mapped[Optional[Good]] = relationship(
        primaryjoin="Tasks.c.good_id==Goods.c.id",
        uselist=False,
        post_update=True,
    )

    # TODO: Add ``unmanaged`` attribute for Asset management only tasks.
    #
    # Some tasks are created for asset management purposes only and doesn't
    # need TimeLogs to be entered. Create an attribute called ``unmanaged`` and
    # and set it to False by default, and if its True don't include it in the
    # TaskJuggler project. And do not track its status.

    def __init__(
        self,
        project: Optional["Project"] = None,
        parent: Optional["Task"] = None,
        depends_on: Optional[List["Task"]] = None,
        resources: Optional[List[User]] = None,
        alternative_resources: Optional[List[User]] = None,
        responsible: Optional[List[User]] = None,
        watchers: Optional[List[User]] = None,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        schedule_timing: float = 1.0,
        schedule_unit: TimeUnit = TimeUnit.Hour,
        schedule_model: Optional[ScheduleModel] = None,
        schedule_constraint: Optional[ScheduleConstraint] = ScheduleConstraint.NONE,
        bid_timing: Optional[Union[int, float]] = None,
        bid_unit: Optional[TimeUnit] = None,
        is_milestone: bool = False,
        priority: int = defaults.task_priority,
        allocation_strategy: str = defaults.allocation_strategy[0],
        persistent_allocation: bool = True,
        good: Optional[Good] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        # temp attribute for remove event
        self._previously_removed_dependent_tasks = []

        # update kwargs with extras
        kwargs["start"] = start
        kwargs["end"] = end

        kwargs["schedule_timing"] = schedule_timing
        kwargs["schedule_unit"] = schedule_unit
        kwargs["schedule_model"] = schedule_model
        kwargs["schedule_constraint"] = schedule_constraint

        super(Task, self).__init__(**kwargs)

        # call the mixin __init__ methods
        StatusMixin.__init__(self, **kwargs)
        DateRangeMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)

        kwargs["parent"] = parent
        DAGMixin.__init__(self, **kwargs)

        self._review_number = 0

        # self.parent = parent
        self._project = project

        self.time_logs = []
        self.versions = []

        self.is_milestone = is_milestone

        # update the status
        with DBSession.no_autoflush:
            self.status = self.status_list["WFD"]

        if depends_on is None:
            depends_on = []

        self.depends_on = depends_on

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
    def __init_on_load__(self) -> None:
        """Update defaults on load."""
        # temp attribute for remove event
        self._previously_removed_dependent_tasks = []

    def __eq__(self, other: Any) -> None:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is a Task instance and has the same project,
                parent, depends_on, start and end value and resources.
        """
        return (
            super(Task, self).__eq__(other)
            and isinstance(other, Task)
            and self.project == other.project
            and self.parent == other.parent
            and self.depends_on == other.depends_on
            and self.start == other.start
            and self.end == other.end
            and self.resources == other.resources
        )

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Task, self).__hash__()

    @validates("time_logs")
    def _validate_time_logs(self, key: str, time_log: TimeLog) -> TimeLog:
        """Validate the given time_log value.

        Args:
            key (str): The name of the validated column.
            time_log (TimeLog): A TimeLog instance to validate.

        Raises:
            TypeError: If the given time_log value is not a :class:`.TimeLog` instance.

        Returns:
            TimeLog: The validated TimeLog instance.
        """
        if not isinstance(time_log, TimeLog):
            raise TypeError(
                "{}.time_logs should only contain instances of "
                "stalker.models.task.TimeLog, not {}: '{}'".format(
                    self.__class__.__name__, time_log.__class__.__name__, time_log
                )
            )

        # TODO: convert this to an event
        # update parents total_logged_second attribute
        with DBSession.no_autoflush:
            if self.parent:
                self.parent.total_logged_seconds += time_log.total_seconds

        return time_log

    @validates("reviews")
    def _validate_reviews(self, key: str, review: Review) -> Review:
        """Validate the given review value.

        Args:
            key (str): The name of the validated column.
            review (Review): The validated review value.

        Raises:
            TypeError: If the review is not a :class:`stalker.models.review.Review`
                instance.

        Returns:
            Review: The validated review instance.
        """
        if not isinstance(review, Review):
            raise TypeError(
                "{}.reviews should only contain instances of "
                "stalker.models.review.Review, not {}: '{}'".format(
                    self.__class__.__name__, review.__class__.__name__, review
                )
            )
        return review

    @validates("task_depends_on")
    def _validate_task_depends_on(self, key: str, task_depends_on: "Task") -> "Task":
        """Validate the given task_depends_on value.

        Args:
            key (str): The name of the validated column.
            task_depends_on (Task): The Task instance that this Task is depending on.

        Raises:
            TypeError: If the `task_depends_on.depends_on` is not a Task instance.
            StatusError: If the status of the current task is one of WIP, PREV, HREV,
                OH, STOP or CMPL as this means the Task has been started to be worked on
                and it is not allowed to change the dependency chain of an already
                started task.
            StatusError: If the current task is a container and its status is CMPL.
            CircularDependencyError: If the given task is in circular relation with this
                Task instance.

        Returns:
            Task: The validated task_depends_on value.
        """
        if not isinstance(task_depends_on, TaskDependency):
            raise TypeError(
                "{}.task_depends_on should only contain instances of "
                "TaskDependency, not {}: '{}'".format(
                    self.__class__.__name__,
                    task_depends_on.__class__.__name__,
                    task_depends_on,
                )
            )

        depends_on = task_depends_on.depends_on
        if not depends_on:
            # the relation is still not setup yet
            # trust to the TaskDependency class for checking the
            # depends_on attribute
            return task_depends_on

        # check the status of the current task
        with DBSession.no_autoflush:
            wfd = self.status_list["WFD"]
            rts = self.status_list["RTS"]
            wip = self.status_list["WIP"]
            prev = self.status_list["PREV"]
            hrev = self.status_list["HREV"]
            drev = self.status_list["DREV"]
            oh = self.status_list["OH"]
            stop = self.status_list["STOP"]
            cmpl = self.status_list["CMPL"]

            if self.status in [wip, prev, hrev, drev, oh, stop, cmpl]:
                raise StatusError(
                    f"This is a {self.status.code} task and it is not allowed to "
                    f"change the dependencies of a {self.status.code} task"
                )

        # check for the circular dependency
        with DBSession.no_autoflush:
            check_circular_dependency(depends_on, self, "depends_on")
            check_circular_dependency(depends_on, self, "children")

        # check for circular dependency toward the parent, non of the parents
        # should be depending on the given depends_on_task
        with DBSession.no_autoflush:
            parent = self.parent
            while parent:
                if parent in depends_on.depends_on:
                    raise CircularDependencyError(
                        f"One of the parents of {self} is depending on {depends_on}"
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
                if depends_on.status in [wfd, rts, wip, oh, prev, hrev, drev, oh]:
                    do_update_status = True

            if do_update_status:
                self.status = wfd

        return task_depends_on

    @validates("schedule_timing")
    def _validate_schedule_timing(
        self, key: str, schedule_timing: Union[int, float]
    ) -> Union[int, float]:
        """Validate the given schedule_timing value.

        Args:
            key (str): The name of the validated column.
            schedule_timing (Union[int, float]): The schedule_timing value to be
                validated.

        Returns:
            float: The validated schedule_timing value.
        """
        schedule_timing = ScheduleMixin._validate_schedule_timing(
            self, key, schedule_timing
        )

        # reschedule
        self._reschedule(schedule_timing, self.schedule_unit)

        return schedule_timing

    @validates("schedule_unit")
    def _validate_schedule_unit(
        self, key: str, schedule_unit: Union[str, TimeUnit]
    ) -> TimeUnit:
        """Validate the given schedule_unit value.

        Args:
            key (str): The name of the validated column.
            schedule_unit (Union[str, TimeUnit]): The schedule_unit value to be
                validated.

        Returns:
            TimeUnit: The validated schedule_unit value.
        """
        schedule_unit = ScheduleMixin._validate_schedule_unit(self, key, schedule_unit)

        if self.schedule_timing:
            self._reschedule(self.schedule_timing, schedule_unit)

        return schedule_unit

    def _reschedule(
        self, schedule_timing: Union[int, float], schedule_unit: Union[str, TimeUnit]
    ) -> None:
        """Update the start and end date with schedule_timing and schedule_unit values.

        Args:
            schedule_timing (Union[int, float]): An integer or float value showing the
                value of the schedule timing.
            schedule_unit (Union[str, TimeUnit]): One of 'min', 'h', 'd',
                'w', 'm', 'y' or a TimeUnit enum value.
        """
        # update end date value by using the start and calculated duration
        if not self.is_leaf:
            return

        from stalker import defaults

        schedule_unit_value = None
        if schedule_unit is not None:
            schedule_unit = TimeUnit.to_unit(schedule_unit)
            schedule_unit_value = schedule_unit.value

        unit = defaults.datetime_units_to_timedelta_kwargs.get(schedule_unit_value)
        if not unit:  # we are in a pre flushing state do not do anything
            return

        kwargs = {unit["name"]: schedule_timing * unit["multiplier"]}
        calculated_duration = datetime.timedelta(**kwargs)
        if (
            self.schedule_constraint == ScheduleConstraint.NONE
            or self.schedule_constraint == ScheduleConstraint.Start
        ):
            # get end
            self._start, self._end, self._duration = self._validate_dates(
                self.start, None, calculated_duration
            )
        elif self.schedule_constraint == ScheduleConstraint.End:
            # get start
            self._start, self._end, self._duration = self._validate_dates(
                None, self.end, calculated_duration
            )
        elif self.schedule_constraint == ScheduleConstraint.Both:
            # restore duration
            self._start, self._end, self._duration = self._validate_dates(
                self.start, self.end, None
            )

        # also update cached _schedule_seconds value
        self._schedule_seconds = self.schedule_seconds

    @validates("is_milestone")
    def _validate_is_milestone(self, key: str, is_milestone: Union[None, bool]) -> bool:
        """Validate the given is_milestone value.

        Args:
            key (str): The name of the validated column.
            is_milestone (Union[None, bool]): The value to validated.

        Raises:
            TypeError: If the is_milestone value is not None and not a bool value.

        Returns:
            bool: The validated value.
        """
        if is_milestone is None:
            is_milestone = False

        if not isinstance(is_milestone, bool):
            raise TypeError(
                "{}.is_milestone should be a bool value (True or False), "
                "not {}: '{}'".format(
                    self.__class__.__name__,
                    is_milestone.__class__.__name__,
                    is_milestone,
                )
            )

        if is_milestone:
            self.resources = []

        return bool(is_milestone)

    @validates("parent")
    def _validate_parent(self, key: str, parent: "Task") -> "Task":
        """Validate the given parent value.

        Args:
            key (str): The name of the validated column.
            parent (Task): The parent value to be validated.

        Raises:
            TypeError: If the parent value is not None and not a :class:`.Task`
                instance.

        Returns:
            Task: The validated parent value.
        """
        if parent is not None:
            if not isinstance(parent, Task):
                raise TypeError(
                    "{}.parent should be an instance of "
                    "stalker.models.task.Task, not {}: '{}'".format(
                        self.__class__.__name__, parent.__class__.__name__, parent
                    )
                )

            # check for cycle
            check_circular_dependency(self, parent, "children")
            check_circular_dependency(self, parent, "depends_on")

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

    @validates("_project")
    def _validate_project(self, key: str, project: "Project") -> "Project":
        """Validate the given project value.

        Args:
            key (str): The name of the validated column.
            project (stalker.models.project.Project): The project value to validate.

        Raises:
            TypeError: If the project is None and a
                :class:`stalker.models.project.Project` cannot be found through the
                parents of this current task.
            TypeError: If the project is not a :class:`stalker.models.project.Project`
                instance.

        Returns:
            stalker.models.project.Project: The validated
                :class:`stalker.models.project.Project` instance.
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
                raise TypeError(
                    "{}.project should be an instance of "
                    "stalker.models.project.Project, not {}: '{}'.\n\nOr please supply "
                    "a stalker.models.task.Task with the parent argument, so "
                    "Stalker can use the project of the supplied parent task".format(
                        self.__class__.__name__, project.__class__.__name__, project
                    )
                )

        from stalker.models.project import Project

        if not isinstance(project, Project):
            # go mad again it is not a project instance
            raise TypeError(
                "{}.project should be an instance of stalker.models.project.Project, "
                "not {}: '{}'".format(
                    self.__class__.__name__, project.__class__.__name__, project
                )
            )

        # check if there is a parent
        if not self.parent:
            return project

        # check if given project is matching the parent.project
        with DBSession.no_autoflush:
            if self.parent.project != project:
                # don't go mad again, but warn the user that there is
                # an ambiguity!!!
                import warnings

                message = (
                    "The supplied parent and the project is not matching in "
                    "{}, Stalker will use the parent's project ({}) as the "
                    "parent of this {}".format(
                        self, self.parent.project, self.__class__.__name__
                    )
                )

                warnings.warn(message, RuntimeWarning, stacklevel=2)

                # use the parent.project
                project = self.parent.project

        return project

    @validates("priority")
    def _validate_priority(self, key: str, priority: Union[int, float]) -> int:
        """Validate the given priority value.

        Args:
            key (str): The name of the validated column.
            priority (int): The priority value to be validated. It should be a float or
                integer value between 0 and 1000, any other value will be clamped to
                this range.

        Raises:
            TypeError: If the given priority value is not an integer or float.

        Returns:
            int: The validated priority value.
        """
        if priority is None:
            from stalker import defaults

            priority = defaults.task_priority

        if not isinstance(priority, (int, float)):
            raise TypeError(
                "{}.priority should be an integer value between 0 and 1000, "
                "not {}: '{}'".format(
                    self.__class__.__name__, priority.__class__.__name__, priority
                )
            )

        if priority < 0:
            priority = 0
        elif priority > 1000:
            priority = 1000

        return int(priority)

    @validates("children")
    def _validate_children(self, key: str, child: "Task") -> "Task":
        """Validate the given child value.

        Args:
            key (str): The name of the validated column.
            child (Task): The child Task to be validated.

        Returns:
            Task: The validated child Task instance.
        """
        # just empty the resources list
        # do it without a flush
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
                self._start = datetime.datetime.max.replace(tzinfo=pytz.utc)
                self._end = datetime.datetime.min.replace(tzinfo=pytz.utc)

            # extend start and end dates
            self._expand_dates(self, child.start, child.end)

        return child

    @validates("resources")
    def _validate_resources(self, key: str, resource: User) -> User:
        """Validate the given resources value.

        Args:
            key (str): The name of the validated column.
            resource (User): The value to validate.

        Raises:
            TypeError: If the given resource value is not a
                :class:`stalker.models.auth.User` instance.

        Returns:
            User: The validated :class:`stalker.models.auth.User` instance.
        """
        if not isinstance(resource, User):
            raise TypeError(
                "{}.resources should only contain instances of "
                "stalker.models.auth.User, not {}: '{}'".format(
                    self.__class__.__name__,
                    resource.__class__.__name__,
                    resource,
                )
            )
        return resource

    @validates("alternative_resources")
    def _validate_alternative_resources(self, key: str, resource: User) -> User:
        """Validate the given resource value.

        Args:
            key (str): The name of the validated column.
            resource (User): The value to validate.

        Raises:
            TypeError: If the given resource value is not a
                :class:`stalker.models.auth.User` instance.

        Returns:
            User: The validated User instance.
        """
        if not isinstance(resource, User):
            raise TypeError(
                "{}.alternative_resources should only contain instances of "
                "stalker.models.auth.User, not {}: '{}'".format(
                    self.__class__.__name__,
                    resource.__class__.__name__,
                    resource,
                )
            )
        return resource

    @validates("_computed_resources")
    def _validate_computed_resources(self, key: str, resource: User) -> User:
        """Validate the computed resources value.

        Args:
            key (str): The name of the validated column.
            resource (User): The value to validate.

        Raises:
            TypeError: If the given resource value is not a
                :class:`stalker.models.auth.User` instance.

        Returns:
            User: The validated User instance.
        """
        if not isinstance(resource, User):
            raise TypeError(
                "{}.computed_resources should only contain instances of "
                "stalker.models.auth.User, not {}: '{}'".format(
                    self.__class__.__name__, resource.__class__.__name__, resource
                )
            )
        return resource

    def _computed_resources_getter(self):
        """Return the _computed_resources attribute value.

        Returns:
            User: The computed_user attribute value if there are any else the
                same content of the resources attribute.
        """
        if not self.is_scheduled:
            self._computed_resources = self.resources
        return self._computed_resources

    def _computed_resources_setter(self, resources: List[User]) -> None:
        """Set the _computed_resources attribute value.

        Args:
            resources (List[User]): List of User instances to set the computed
                resources too.
        """
        self._computed_resources = resources

    computed_resources: Mapped[Optional[List["User"]]] = synonym(
        "_computed_resources",
        descriptor=property(_computed_resources_getter, _computed_resources_setter),
    )

    @validates("allocation_strategy")
    def _validate_allocation_strategy(self, key: str, strategy: str) -> str:
        """Validate the given allocation_strategy value.

        Args:
            key (str): The name of the validated column.
            strategy (str): The allocation strategy value to validate.

        Raises:
            TypeError: If the given allocation strategy value is not a string.
            ValueError: If the given allocation strategy value is not one of
                [ "minallocated", "maxloaded", "minloaded", "order", "random"].

        Returns:
            str: The validated allocation strategy value.
        """
        from stalker import defaults

        if strategy is None:
            strategy = defaults.allocation_strategy[0]

        if not isinstance(strategy, str):
            raise TypeError(
                "{}.allocation_strategy should be one of {}, not {}: '{}'".format(
                    self.__class__.__name__,
                    defaults.allocation_strategy,
                    strategy.__class__.__name__,
                    strategy,
                )
            )

        if strategy not in defaults.allocation_strategy:
            raise ValueError(
                "{}.allocation_strategy should be one of {}, not '{}'".format(
                    self.__class__.__name__,
                    defaults.allocation_strategy,
                    strategy,
                )
            )

        return strategy

    @validates("persistent_allocation")
    def _validate_persistent_allocation(
        self, key: str, persistent_allocation: bool
    ) -> bool:
        """Validate the given persistent_allocation value.

        Args:
            key (str): The name of the validate column.
            persistent_allocation (bool): The persistent allocation value to be
                validated.

        Returns:
            bool: The validated persistent allocation value.
        """
        if persistent_allocation is None:
            from stalker import defaults

            persistent_allocation = defaults.persistent_allocation

        return bool(persistent_allocation)

    @validates("watchers")
    def _validate_watchers(self, key: str, watcher: User) -> User:
        """Validate the given watcher value.

        Args:
            key (str): The name of the validated column.
            watcher (User): The watcher value to be validated.

        Raises:
            TypeError: If the watcher is not a :class:`stalker.models.auth.User`
                instance.

        Returns:
            User: The validated :class:`stalker.models.auth.User` instance.
        """
        if not isinstance(watcher, User):
            raise TypeError(
                "{}.watchers should only contain instances of "
                "stalker.models.auth.User, not {}: '{}'".format(
                    self.__class__.__name__,
                    watcher.__class__.__name__,
                    watcher,
                )
            )
        return watcher

    @validates("versions")
    def _validate_versions(self, key: str, version: "Version"):
        """Validate the given version value.

        Args:
            key (str): The name of the validated column.
            version (stalker.models.version.Version): The version value to be
                validated.

        Raises:
            TypeError: If the version is not an Version instance.

        Returns:
            stalker.models.version.Version: The validated
                :class:`stalker.models.version.Version` value.
        """
        from stalker.models.version import Version

        if not isinstance(version, Version):
            raise TypeError(
                "{}.versions should only contain instances of "
                "stalker.models.version.Version, and not {}: '{}'".format(
                    self.__class__.__name__,
                    version.__class__.__name__,
                    version,
                )
            )

        return version

    @validates("bid_timing")
    def _validate_bid_timing(
        self, key: str, bid_timing: Union[None, int, float]
    ) -> Union[None, int, float]:
        """Validate the given bid_timing value.

        Args:
            key (str): The name of the validated column.
            bid_timing (Union[int, float]): The bid_timing value to be validated.

        Raises:
            TypeError: If the bid_timing is not None and not an integer or float.

        Returns:
            Union[int, float]: The validated bid_timing value.
        """
        if bid_timing is not None:
            if not isinstance(bid_timing, (int, float)):
                raise TypeError(
                    "{}.bid_timing should be an integer or float showing the value of "
                    "the initial bid for this {}, not {}: '{}'".format(
                        self.__class__.__name__,
                        self.__class__.__name__,
                        bid_timing.__class__.__name__,
                        bid_timing,
                    )
                )
        return bid_timing

    @validates("bid_unit")
    def _validate_bid_unit(self, key: str, bid_unit: Union[str, TimeUnit]) -> str:
        """Validate the given bid_unit value.

        Args:
            key (str): The name of the validated column.
            bid_unit (Union[str, TimeUnit]): The timing unit of the bid
                value, should be a TimeUnit enum value or one of ["min", "h",
                "d", "w", "m", "y", "Minute", "Hour", "Day", "Week", "Month",
                "Year"].

        Returns:
            str: The validated bid_unit value.
        """
        if bid_unit is None:
            bid_unit = TimeUnit.Hour

        bid_unit = TimeUnit.to_unit(bid_unit)

        return bid_unit

    @classmethod
    def _expand_dates(
        cls, task: "Task", start: datetime.datetime, end: datetime.datetime
    ) -> None:
        """Extend the given tasks date values with the given start and end values.

        Args:
            task (Task): The Task instance.
            start (datetime.datetime): The start datetime.datetime instance.
            end (datetime.datetime): The end datetime.datetime instance.
        """
        # update parents start and end date
        if task:
            if task.start > start:
                task.start = start
            if task.end < end:
                task.end = end

    # TODO: Why these methods are not in the DateRangeMixin class.
    @validates("computed_start")
    def _validate_computed_start(
        self, key: str, computed_start: datetime.datetime
    ) -> datetime.datetime:
        """Validate the given computed_start value.

        Args:
            key (str): The name of the validated column.
            computed_start (datetime.datetime): The computed start as a
                datetime.datetime instance.

        Returns:
            datetime.datetime: The validated computed start value.
        """
        self.start = computed_start
        return computed_start

    @validates("computed_end")
    def _validate_computed_end(
        self, key: str, computed_end: datetime.datetime
    ) -> datetime.datetime:
        """Validate the given computed_end value.

        Args:
            key (str): The name of the validated column.
            computed_end (datetime.datetime): The computed start as a
                datetime.datetime instance.

        Returns:
            datetime.datetime: The validated computed end value.
        """
        self.end = computed_end
        return computed_end

    def _start_getter(self) -> datetime.datetime:
        """Return the start value.

        Returns:
            datetime.datetime: The start date and time value.
        """
        return self._start

    def _start_setter(self, start: datetime.datetime) -> None:
        """Set the start value.

        Args:
            start (datetime.datetime): The start date and time value to be validated.
        """
        self._start, self._end, self._duration = self._validate_dates(
            start, self._end, self._duration
        )
        self._expand_dates(self.parent, self.start, self.end)

    def _end_getter(self) -> datetime.datetime:
        """Return the end value.

        Returns:
            datetime.datetime: The end date and time value.
        """
        return self._end

    def _end_setter(self, end: datetime.datetime) -> None:
        """Set the end value.

        Args:
            end (datetime.datetime): The end date and time value to be validated.
        """
        # update the end only if this is not a container task
        self._start, self._end, self._duration = self._validate_dates(
            self.start, end, self.duration
        )
        self._expand_dates(self.parent, self.start, self.end)

    def _project_getter(self) -> "Project":
        """Return the project value.

        Returns:
            stalker.models.project.Project: The :class:`stalker.models.project.Project`
                instance.
        """
        return self._project

    project: Mapped[Optional["Project"]] = synonym(
        "_project",
        descriptor=property(_project_getter),
        doc="""The owner Project of this task.

        It is a read-only attribute. It is not possible to change the owner
        Project of a Task it is defined when the Task is created.
        """,
    )

    @property
    def tjp_abs_id(self) -> str:
        """Return the calculated absolute id of this task.

        Returns:
            str: The calculated absolute id of this task.
        """
        abs_id = self.parent.tjp_abs_id if self.parent else self.project.tjp_id
        return f"{abs_id}.{self.tjp_id}"

    @property
    def to_tjp(self) -> str:
        """Return the TaskJuggler representation of this task.

        Returns:
            str: The TaskJuggler representation of this task.
        """
        tab = "    "
        indent = tab * len(self.parents)
        has_inner_data = False
        tjp = f'{indent}task {self.tjp_id} "{self.tjp_id}" {{'
        if self.priority != 500:
            has_inner_data = True
            tjp += f"\n{indent}{tab}priority {self.priority}"
        if self.task_depends_on:
            has_inner_data = True
            tjp += f"\n{indent}{tab}depends "
            for i, depends_on in enumerate(self.task_depends_on):
                if i != 0:
                    tjp += ", "
                tjp += depends_on.to_tjp
        if self.is_container:
            has_inner_data = True
            for child_task in self.children:
                tjp += "\n"
                tjp += child_task.to_tjp
        if self.resources:
            has_inner_data = True
            if self.schedule_constraint:
                if self.schedule_constraint in [1, 3]:
                    tjp += f"\n{indent}{tab}start {self.start.astimezone(pytz.utc).strftime('%Y-%m-%d-%H:%M')}"  # noqa: B950
                if self.schedule_constraint in [2, 3]:
                    tjp += f"\n{indent}{tab}end {self.end.astimezone(pytz.utc).strftime('%Y-%m-%d-%H:%M')}"  # noqa: B950
            tjp += f"\n{indent}{tab}{self.schedule_model} {self.schedule_timing}{self.schedule_unit}"  # noqa: B950
            tjp += f"\n{indent}{tab}allocate "
            for i, resource in enumerate(sorted(self.resources, key=lambda x: x.id)):
                if i != 0:
                    tjp += ", "
                tjp += resource.tjp_id
                if not self.alternative_resources:
                    continue
                tjp += f" {{\n{indent}{tab}{tab}alternative\n{indent}{tab}{tab}"
                for i, alt_res in enumerate(
                    sorted(self.alternative_resources, key=lambda x: x.id)
                ):
                    if i != 0:
                        tjp += ", "
                    tjp += alt_res.tjp_id
                tjp += f" select {self.allocation_strategy}"
                if self.persistent_allocation:
                    tjp += f"\n{indent}{tab}{tab}persistent"
                tjp += f"\n{indent}{tab}}}"
        for time_log in self.time_logs:
            has_inner_data = True
            tjp += (
                f"\n{indent}{tab}booking "
                f"{time_log.resource.tjp_id} "
                f"{time_log.start.astimezone(pytz.utc).strftime('%Y-%m-%d-%H:%M:%S')} "
                f"- "
                f"{time_log.end.astimezone(pytz.utc).strftime('%Y-%m-%d-%H:%M:%S')} "
                "{ overtime 2 }"
            )
        tjp += f"\n{indent}}}" if has_inner_data else "}"
        return tjp

    @property
    def level(self) -> int:
        """Returns the hierarchical level of this task.

        It is a temporary property and will be useless when Stalker has its own
        implementation of a proper Gantt Chart. Right now it is used by the jQueryGantt.

        Returns:
            int: The hierarchical level of this task.
        """
        i = 0
        current_task = self
        while current_task:
            i += 1
            current_task = current_task.parent
        return i

    @property
    def is_scheduled(self) -> bool:
        """Return if this task has both a computed_start and computed_end values.

        Returns:
            bool: Return True if this task has both a computed_start and computed_end
                values.
        """
        return self.computed_start is not None and self.computed_end is not None

    def _total_logged_seconds_getter(self) -> int:
        """Return the total effort spent for this Task.

        It is the sum of all the TimeLogs recorded for this task as seconds.

        Returns:
            int: An integer showing the total seconds spent.
        """
        with DBSession.no_autoflush:
            if not self.is_leaf:
                if self._total_logged_seconds is None:
                    self.update_schedule_info()
                return self._total_logged_seconds

            if self.schedule_model == ScheduleModel.Effort:
                logger.debug("effort based task detected!")
                try:
                    sql = """
                    select
                        extract(epoch from sum("TimeLogs".end - "TimeLogs".start))::int
                    from "TimeLogs"
                    where "TimeLogs".task_id = :task_id
                    """
                    connection = DBSession.connection()
                    result = connection.execute(
                        text(sql), {"task_id": self.id}
                    ).fetchone()
                    return result[0] if result[0] else 0
                except (UnboundExecutionError, OperationalError, ProgrammingError):
                    # no database connection
                    # fallback to Python
                    logger.debug("No session found! Falling back to Python")
                    seconds = 0
                    for time_log in self.time_logs:
                        seconds += time_log.total_seconds
                    return seconds
            else:
                now = datetime.datetime.now(pytz.utc)
                if self.schedule_model == ScheduleModel.Duration:
                    # directly return the difference between
                    # min(now - start, end - start)
                    logger.debug(
                        "duration based task detected!, "
                        "calculating schedule_info from duration of the task"
                    )
                    daily_working_hours = 86400.0
                elif self.schedule_model == ScheduleModel.Length:
                    # directly return the difference between
                    # min(now - start, end - start)
                    # but use working days
                    logger.debug(
                        "length based task detected!, "
                        "calculating schedule_info from duration of the task"
                    )
                    from stalker import defaults

                    daily_working_hours = defaults.daily_working_hours

                if self.end <= now:
                    seconds = (
                        self.duration.days * daily_working_hours + self.duration.seconds
                    )
                elif self.start >= now:
                    seconds = 0
                else:
                    past = now - self.start
                    past_as_seconds = past.days * daily_working_hours + past.seconds
                    logger.debug(f"past_as_seconds: {past_as_seconds}")
                    seconds = past_as_seconds
                return seconds

    def _total_logged_seconds_setter(self, seconds: int) -> None:
        """Set the total_logged_seconds value.

        This is mainly used for container tasks, to cache the child logged_seconds

        Args:
            seconds (int): An integer value for the seconds.
        """
        # only set for container tasks
        if self.is_container:
            # update parent
            old_value = 0
            if self._total_logged_seconds:
                old_value = self._total_logged_seconds
            self._total_logged_seconds = seconds
            if self.parent:
                self.parent.total_logged_seconds = (
                    self.parent.total_logged_seconds - old_value + seconds
                )

    total_logged_seconds: Mapped[Optional[int]] = synonym(
        "_total_logged_seconds",
        descriptor=property(_total_logged_seconds_getter, _total_logged_seconds_setter),
    )

    def _schedule_seconds_getter(self) -> int:
        """Return the total effort, length or duration in seconds.

        This is used for calculating the percent_complete value.

        Returns:
            int: The total effort, length or duration in seconds.
        """
        # for container tasks use the children schedule_seconds attribute
        if self.is_container:
            if self._schedule_seconds is None or self._schedule_seconds < 0:
                self.update_schedule_info()
            return self._schedule_seconds
        else:
            return self.to_seconds(
                self.schedule_timing, self.schedule_unit, self.schedule_model
            )

    def _schedule_seconds_setter(self, seconds: int) -> None:
        """Set the schedule_seconds of this task.

        Mainly used for container tasks.

        Args:
            seconds (int): An integer value of schedule_seconds for this task.
        """
        # do it only for container tasks
        if self.is_container:
            # also update the parents
            with DBSession.no_autoflush:
                if self.parent:
                    current_value = 0
                    if self._schedule_seconds:
                        current_value = self._schedule_seconds
                    self.parent.schedule_seconds = (
                        self.parent.schedule_seconds - current_value + seconds
                    )
                self._schedule_seconds = seconds

    schedule_seconds: Mapped[Optional[int]] = synonym(
        "_schedule_seconds",
        descriptor=property(_schedule_seconds_getter, _schedule_seconds_setter),
    )

    def update_schedule_info(self) -> None:
        """Update the total_logged_seconds and schedule_seconds attributes.

        This updates the total_logged_seconds and schedule_seconds attributes by using
        the children info and triggers an update on every children.
        """
        if self.is_container:
            total_logged_seconds = 0
            schedule_seconds = 0
            logger.debug(f"updating schedule info for: {self.name}")
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
                    schedule_seconds += (
                        child.schedule_seconds if child.schedule_seconds else 0
                    )
                    total_logged_seconds += (
                        child.total_logged_seconds if child.total_logged_seconds else 0
                    )

            self._schedule_seconds = schedule_seconds
            self._total_logged_seconds = total_logged_seconds
        else:
            self._schedule_seconds = self.schedule_seconds
            self._total_logged_seconds = self.total_logged_seconds

    @property
    def percent_complete(self) -> float:
        """Calculate and return the percent_complete value.

        The percent_complete value is based on the total_logged_seconds and
        schedule_seconds of the task.

        Container tasks will use info from their children.

        Returns:
            float: The percent complete value between 0 and 1.
        """
        if self.is_container and (
            self._total_logged_seconds is None or self._schedule_seconds is None
        ):
            self.update_schedule_info()

        return self.total_logged_seconds / float(self.schedule_seconds) * 100.0

    @property
    def remaining_seconds(self) -> int:
        """Return the remaining amount of effort, length or duration left as seconds.

        Returns:
            int: The remaining amount of effort, length or duration in seconds.
        """
        # for effort based tasks use the time_logs
        return self.schedule_seconds - self.total_logged_seconds

    def _responsible_getter(self) -> List[User]:
        """Return the current responsible of this task.

        Returns:
            List[User]: The list of :class:`stalker.models.auth.User` instances that are
                the responsible of this task. If no stored value is found the same list
                of Users from the parents will be returned.
        """
        if not self._responsible:
            # traverse parents
            for parent in reversed(self.parents):
                if parent.responsible:
                    self._responsible = copy.copy(parent.responsible)
                    break

        # so parents do not have a responsible
        return self._responsible

    def _responsible_setter(self, responsible: List[User]) -> None:
        """Set the responsible attribute.

        Args:
            responsible (List[User]): A list of :class:`.User` instances to be the
                responsible of this Task.
        """
        self._responsible = responsible

    @validates("_responsible")
    def _validate_responsible(self, key, responsible: User) -> User:
        """Validate the given responsible value (each responsible).

        Args:
            key (str): The name of the validated column.
            responsible (User): A :class:`stalker.models.auth.User` instance to be
                validated.

        Raises:
            TypeError: If the given responsible value is not a User instance.

        Returns:
            User: The validated :class:`stalker.models.auth.User` instance.
        """
        if not isinstance(responsible, User):
            raise TypeError(
                "{}.responsible should only contain instances of "
                "stalker.models.auth.User, not {}: '{}'".format(
                    self.__class__.__name__,
                    responsible.__class__.__name__,
                    responsible,
                )
            )
        return responsible

    responsible: Mapped[Optional[List[User]]] = synonym(
        "_responsible",
        descriptor=property(
            _responsible_getter,
            _responsible_setter,
            doc="""The responsible of this task.

            This attribute will return the responsible of this task which is a
            list of :class:`.User` instances. If there is no responsible set
            for this task, then it will try to find a responsible in its
            parents.
            """,
        ),
    )

    @property
    def tickets(self) -> List[Ticket]:
        """Return the tickets referencing this Task in their links attribute.

        Returns:
            List[Ticket]: List of :class:`stalker.models.ticket.Ticket` instances that
                are referencing this Task in their links attribute.
        """
        return Ticket.query.filter(Ticket.links.contains(self)).all()

    @property
    def open_tickets(self) -> List[Ticket]:
        """Return the open tickets referencing this task in their links attribute.

        Returns:
            List[Ticket]: List of open :class:`stalker.models.ticket.Ticket` instances
                that are referencing this Task in their links attribute.
        """
        status_closed = Status.query.filter(Status.name == "Closed").first()
        return (
            Ticket.query.filter(Ticket.links.contains(self))
            .filter(Ticket.status != status_closed)
            .all()
        )

    def walk_dependencies(
        self,
        method: Union[int, str, TraversalDirection] = TraversalDirection.BreadthFirst,
    ) -> Generator[None, "Task", None]:
        """Walk the dependencies of this task.

        Args:
            method (Union[int, str, TraversalDirection]): The walk method
                defined by the :class:`.TraversalDirection` enum value. Default
                is :attr:`.TraversalDirection.BreadthFirst`.

        Yields:
            Task: Yields Task instances.
        """
        for t in walk_hierarchy(self, "depends_on", method=method):
            yield t

    @validates("good")
    def _validate_good(self, key: str, good: Good) -> Good:
        """Validate the given good value.

        Args:
            key (str): The name of the validated column.
            good (Good): The validated good value.

        Raises:
            TypeError: If the given good is not None and not a Good instance.

        Returns:
            Good: The validated good value.
        """
        if good is not None and not isinstance(good, Good):
            raise TypeError(
                "{}.good should be a stalker.models.budget.Good instance, "
                "not {}: '{}'".format(
                    self.__class__.__name__, good.__class__.__name__, good
                )
            )
        return good

    # =============
    # ** ACTIONS **
    # =============
    def create_time_log(
        self, resource: User, start: datetime.datetime, end: datetime.datetime
    ) -> TimeLog:
        """Create a TimeLog with the given information.

        This will ease creating TimeLog instances for task.

        Args:
            resource (User): The :class:`stalker.models.auth.User` instance as
                the resource for the TimeLog.
            start (datetime.datetime): The start date and time.
            end (datetime.datetime): The end date and time.

        Returns:
            TimeLog: The created TimeLog instance.
        """
        # all the status checks are now part of TimeLog._validate_task
        # create a TimeLog
        return TimeLog(task=self, resource=resource, start=start, end=end)
        # also updating parent statuses are done in TimeLog._validate_task

    def request_review(self, version: Optional["Version"] = None) -> List[Review]:
        """Create and return Review instances for each of the responsible of this task.

        Also set the task status to PREV.

        .. versionadded:: 0.2.0
           Request review will not cap the timing of this task anymore.

        Only applicable to leaf tasks.

        Args:
            version (Optional[Version]): An optional :class:`.Version` instance
                can also be passed. The :class:`.Version` should be related to
                this :class:`.Task`.

        Raises:
            StatusError: If the current task status is not WIP a StatusError
                will be raised as the task has either not been started on being
                worked yet, it is already on review, a dependency might be
                under review or this is stopped, hold or completed.

        Returns:
            List[Review]: The list of :class:`stalker.models.review.Review`
                instances created.
        """
        # check task status
        with DBSession.no_autoflush:
            wip = self.status_list["WIP"]
            prev = self.status_list["PREV"]

        if self.status != wip:
            raise StatusError(
                "{task} (id:{id}) is a {status} task, and it is not suitable for "
                "requesting a review, please supply a WIP task instead.".format(
                    task=self.name, id=self.id, status=self.status.code
                )
            )

        # create Review instances for each Responsible of this task
        reviews = []
        for responsible in self.responsible:
            reviews.append(Review(task=self, version=version, reviewer=responsible))

        # update the status to PREV
        self.status = prev

        # no need to update parent or dependent task statuses
        return reviews

    def request_revision(
        self,
        reviewer: Optional[User] = None,
        description: str = "",
        schedule_timing: int = 1,
        schedule_unit: Union[str, TimeUnit] = TimeUnit.Hour,
    ) -> Review:
        """Request revision.

        Applicable to PREV or CMPL leaf tasks. This method will expand the
        schedule timings of the task according to the supplied arguments.

        When request_revision is called on a PREV task, the other NEW Review
        instances (those created when request_review on a WIP task is called
        and still waiting a review) will be deleted.

        This method at the end will return a new Review instance with correct
        attributes (reviewer, description, schedule_timing, schedule_unit and
        review_number attributes).

        Args:
            reviewer (User): This is the user that requested the revision. They
                don't need to be the responsible, anybody that has a Permission
                to create a Review instance can request a revision.
            description (str): The description of the requested revision.
            schedule_timing (int): The timing value of the requested revision.
                The task will be extended this much of duration. Works along
                with the ``schedule_unit`` parameter. The default value is 1.
            schedule_unit (Union[str, TimeUnit]): The timing unit value of the
                requested revision. The task will be extended this much of
                duration. Works along with the ``schedule_timing`` parameter.
                The default value is `TimeUnit.Hour`.

        Raises:
            StatusError: If the status of the current task is not PREV or CMPL.

        Returns:
            Review: The newly created :class:`stalker.models.review.Review`
                instance.
        """
        # check status
        with DBSession.no_autoflush:
            prev = self.status_list["PREV"]
            cmpl = self.status_list["CMPL"]

        if self.status not in [prev, cmpl]:
            raise StatusError(
                "{task} (id: {id}) is a {status} task, and it is not suitable "
                "for requesting a revision, please supply a PREV or CMPL "
                "task".format(task=self.name, id=self.id, status=self.status.code)
            )

        # *********************************************************************
        # TODO: I don't like this part, find another way to delete them
        #       directly
        # find other NEW Reviews and delete them
        reviews_to_be_deleted = []
        for r in self.reviews:
            if r.status.code == "NEW":
                reviews_to_be_deleted.append(r)

        for r in reviews_to_be_deleted:
            logger.debug(f"removing {r} from task.reviews")
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
        review = Review(reviewer=reviewer, task=self)
        # and call request_revision in the Review instance
        review.request_revision(
            schedule_timing=schedule_timing,
            schedule_unit=schedule_unit,
            description=description,
        )
        return review

    def hold(self) -> None:
        """Pause the execution of this task by setting its status to OH.

        Only applicable to RTS and WIP tasks, any task with other statuses will raise a
        StatusError. Also sets the priority to 0.

        Raises:
            StatusError: If the status of the task is not RTS or WIP.
        """
        # check if status is WIP
        with DBSession.no_autoflush:
            wip = self.status_list["WIP"]
            drev = self.status_list["DREV"]
            oh = self.status_list["OH"]

        if self.status not in [wip, drev, oh]:
            raise StatusError(
                "{task} (id:{id}) is a {status} task, only WIP or DREV tasks can be "
                "set to On Hold".format(
                    task=self.name, id=self.id, status=self.status.code
                )
            )
        # update the status to OH
        self.status = oh

        # set the priority to 0
        self.priority = 0

        # no need to update the status of dependencies nor parents

    def stop(self) -> None:
        """Stop this task.

        It is nearly equivalent to deleting this task. But this will at least preserve
        the TimeLogs entered for this task. It is only possible to stop WIP tasks.

        You can use :meth:`.resume` to resume the task.

        The only difference between :meth:`.hold` (other than setting the task to
        different statuses) is the schedule info, while the :meth:`.hold` method will
        preserve the schedule info, stop() will set the schedule info to the current
        effort.

        So if 2 days of effort has been entered for a 4 days task, when stopped the task
        effort will be capped to 2 days, thus TaskJuggler will not try to reserve any
        resource for this task anymore.

        Also, STOP tasks will be ignored in dependency relations.

        Raises:
            StatusError: If the task status is not WIP, DREV or STOP.
        """
        # check the status
        with DBSession.no_autoflush:
            wip = self.status_list["WIP"]
            drev = self.status_list["DREV"]
            stop = self.status_list["STOP"]

        if self.status not in [wip, drev, stop]:
            raise StatusError(
                "{task} (id:{id})is a {status} task and it is not possible to stop a "
                "{status} task.".format(
                    task=self.name, id=self.id, status=self.status.code
                )
            )

        # set the status
        self.status = stop

        # clamp schedule values
        self.schedule_timing, self.schedule_unit = self.least_meaningful_time_unit(
            self.total_logged_seconds
        )

        # update parent statuses
        self.update_parent_statuses()

        # update dependent task statuses
        for dependency in self.dependent_of:
            dependency.update_status_with_dependent_statuses()

    def resume(self) -> None:
        """Resume the execution of this task.

        Resume the task by setting its status to RTS or WIP depending on its time_logs
        attribute, so if it has TimeLogs then it will resume as WIP and if it doesn't
        then it will resume as RTS. Only applicable to Tasks with status OH.

        Raises:
            StatusError: If the task status is not OH or STOP.
        """
        # check status
        with DBSession.no_autoflush:
            wip = self.status_list["WIP"]
            oh = self.status_list["OH"]
            stop = self.status_list["STOP"]

        if self.status not in [oh, stop]:
            raise StatusError(
                "{task} (id:{id}) is a {status} task, and it is not suitable to be "
                "resumed, please supply an OH or STOP task".format(
                    task=self.name, id=self.id, status=self.status.code
                )
            )
        else:
            # set to WIP
            self.status = wip

        # now update the status with dependencies
        self.update_status_with_dependent_statuses()

        # and update parents statuses
        self.update_parent_statuses()

    def review_set(self, review_number: Union[None, int] = None) -> List[Review]:
        """Return the reviews with the given review_number.

        Args:
            review_number (Union[None, int]): The review number. If
                review_number is skipped it will return the latest set of
                reviews.

        Raises:
            TypeError: If the review_number is not None and not an integer.
            ValueError: If the review_number is less than 0.

        Returns:
            List[Review]: The reviews with the given review number or the
                latest set of :class:`stalker.models.review.Review` instances
                if the review number is is skipped or None.
        """
        review_set = []
        if review_number is None:
            if self.status.code == "PREV":
                review_number = self.review_number + 1
            else:
                review_number = self.review_number

        if not isinstance(review_number, int):
            raise TypeError(
                "review_number argument in {}.review_set should be a positive "
                "integer, not {}: '{}'".format(
                    self.__class__.__name__,
                    review_number.__class__.__name__,
                    review_number,
                )
            )

        if review_number < 1:
            raise ValueError(
                "review_number argument in {}.review_set should be a positive "
                "integer, not {}".format(self.__class__.__name__, review_number)
            )

        for review in self.reviews:
            if review.review_number == review_number:
                review_set.append(review)

        return review_set

    def update_status_with_dependent_statuses(
        self,
        removing: Optional["Task"] = None,
    ) -> None:  # noqa: C901
        """Update the status by looking at the dependent tasks.

        Args:
            removing (Task): The item that is being removed right now, used for
                the remove event to overcome the update issue.
        """
        if self.is_container:
            # do nothing, its status will be decided by its children
            return

        # in case there is no database
        # try to find the statuses from the status_list attribute
        with DBSession.no_autoflush:
            wfd = self.status_list["WFD"]
            rts = self.status_list["RTS"]
            wip = self.status_list["WIP"]
            hrev = self.status_list["HREV"]
            drev = self.status_list["DREV"]
            cmpl = self.status_list["CMPL"]

        if removing:
            self._previously_removed_dependent_tasks.append(removing)
        else:
            self._previously_removed_dependent_tasks = []

        # create a new list from depends_on and skip_list
        dependency_list = []
        for dependency in self.depends_on:
            if dependency not in self._previously_removed_dependent_tasks:
                dependency_list.append(dependency)

        logger.debug(f"self           : {self}")
        logger.debug(f"self.depends_on: {self.depends_on}")
        logger.debug(f"dependency_list: {dependency_list}")

        # if not self.depends_on:
        if not dependency_list:
            # doesn't have any dependency
            # convert its status from WFD to RTS if necessary
            if self.status == wfd:
                self.status = rts
            elif self.status in [wip, drev]:
                if len(self.time_logs):
                    self.status = wip
                else:
                    # doesn't have any TimeLogs return back to rts
                    self.status = rts
            return

        # Keep this part for future reference
        # if self.id:
        #     # use pure sql
        #     logger.debug('using pure SQL to query dependency statuses')
        #     sql_query = """
        #         select
        #             "Statuses".code
        #         from "Tasks"
        #             join "Task_Dependencies"
        #                 on "Tasks".id = "Task_Dependencies".task_id
        #             join "Tasks" as "Dependent_Tasks"
        #                 on "Task_Dependencies".depends_on_id = "Dependent_Tasks".id
        #             join "Statuses" on "Dependent_Tasks".status_id = "Statuses".id
        #         where "Tasks".id = {}
        #         group by "Statuses".code
        #     """.format(self.id)
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
        logger.debug("using pure Python to query dependency statuses")
        binary_status = 0
        dep_statuses = []
        # with DBSession.no_autoflush:
        logger.debug(
            "self.depends_on in update_status_with_dependent_statuses: "
            f"{self.depends_on}"
        )
        for dependency in dependency_list:
            # consider every status only once
            if dependency.status not in dep_statuses:
                dep_statuses.append(dependency.status)
                binary_status += BINARY_STATUS_VALUES[dependency.status.code]

        logger.debug(f"status of the task                   : {self.status.code}")
        logger.debug(f"binary status for dependency statuses: {binary_status}")

        work_alone = binary_status < 4
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

                    total_seconds = (
                        self.schedule_seconds + defaults.timing_resolution.seconds
                    )
                    timing, unit = self.least_meaningful_time_unit(total_seconds)
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

        logger.debug(f"setting status from {self.status} to {status}: ")
        self.status = status

        # also update parent statuses
        self.update_parent_statuses()

        # # also update dependent tasks
        # for dependency in dependency_list:
        #     dependency.update_status_with_dependent_statuses()

    def update_parent_statuses(self) -> None:
        """Update the parent statuses of this task if any."""
        # prevent query-invoked auto-flush
        with DBSession.no_autoflush:
            if self.parent:
                self.parent.update_status_with_children_statuses()

    def update_status_with_children_statuses(self) -> None:
        """Update the task status according to its children statuses."""
        logger.debug(f"setting statuses with child statuses for: {self.name}")

        if not self.is_container:
            # do nothing
            logger.debug("not a container returning!")
            return

        with DBSession.no_autoflush:
            wfd = self.status_list["WFD"]
            rts = self.status_list["RTS"]
            wip = self.status_list["WIP"]
            cmpl = self.status_list["CMPL"]

        parent_statuses_map = [wfd, rts, wip, cmpl]

        # use Python
        logger.debug("using pure Python to query children statuses")
        binary_status = 0
        children_statuses = []
        for child in self.children:
            # consider every status only once
            if child.status not in children_statuses:
                children_statuses.append(child.status)
                binary_status += BINARY_STATUS_VALUES[child.status.code]

        # any condition not listed above should return the status_index of "2=WIP"
        status_index = CHILDREN_TO_PARENT_STATUSES_MAP.get(binary_status, 2)
        status = parent_statuses_map[status_index]

        logger.debug(f"binary statuses value : {binary_status}")
        logger.debug(f"setting status to     : {status.code}")

        self.status = status

        # # update dependent task statuses
        # for dependent in self.dependent_of:
        #     dependent.update_status_with_dependent_statuses()

        # go to parents
        self.update_parent_statuses()

    def _review_number_getter(self) -> None:
        """Return the revision number value.

        Returns:
            int: The current revision number.
        """
        return self._review_number

    review_number: Mapped[Optional[int]] = synonym(
        "_review_number",
        descriptor=property(_review_number_getter),
        doc="returns the _review_number attribute value",
    )

    def _template_variables(self) -> dict:
        """Return variables used in rendering the filename template.

        Returns:
            dict: The template variables.
        """
        # TODO: add test for this template variables
        from stalker import Asset, Shot

        asset = None
        sequence = None
        scene = None
        shot = None
        if isinstance(self, Shot):
            shot = self
            sequence = self.sequence
            scene = self.scene
        elif isinstance(self, Asset):
            asset = self
        else:
            # Look for shots in parents
            for parent in self.parents:
                if isinstance(parent, Shot):
                    sequence = parent.sequence
                    scene = parent.scene
                    break
                elif isinstance(parent, Asset):
                    asset = parent
                    break

        # get the parent tasks
        task = self
        parent_tasks = task.parents
        parent_tasks.append(task)

        return {
            "project": self.project,
            "sequence": sequence,
            "scene": scene,
            "shot": shot,
            "asset": asset,
            "task": self,
            "parent_tasks": parent_tasks,
            "type": self.type,
        }

    @property
    def path(self) -> str:
        """Return the rendered file path of this Task.

        The path attribute will generate a path suitable for placing the files under it.
        It will use the :class:`.FilenameTemplate` class related to the
        :class:`.Project` :class:`.Structure` with the ``target_entity_type`` is set to
        the type of this instance.

        Raises:
            RuntimeError: If no :class:`stalker.models.template.FilenameTemplate`
                instance found in the :class:`stalker.models.structure.Structure` of the
                related :class:`stalker.models.project.Project`.

        Returns:
            str: The rendered file path of this Task.
        """
        # get a suitable FilenameTemplate
        structure = self.project.structure

        task_template = None
        if structure:
            for template in structure.templates:
                if template.target_entity_type == self.entity_type:
                    task_template = template
                    break

        if not task_template:
            raise RuntimeError(
                "There are no suitable FilenameTemplate "
                "(target_entity_type == '{entity_type}') defined in the "
                "Structure of the related Project instance, please create a "
                "new stalker.models.template.FilenameTemplate instance with "
                "its 'target_entity_type' attribute is set to '{entity_type}' "
                "and assign it to the `templates` attribute of the structure "
                "of the project".format(entity_type=self.entity_type)
            )

        return os.path.normpath(
            Template(task_template.path).render(
                **self._template_variables(),
                trim_blocks=True,
                lstrip_blocks=True,
            )
        ).replace("\\", "/")

    @property
    def absolute_path(self) -> str:
        """Return the absolute file path of this task.

        This is the absolute version of the :attr:`.Task.path` attribute and
        depends on the :class:`stalker.models.template.FilenameTemplate` found
        in the :class:`stalker.models.structure.Structure` instance of the
        related :class:`stalker.models.project.Project` instance.

        Returns:
            str: The rendered absolute file path of this task.
        """
        return os.path.normpath(os.path.expandvars(self.path)).replace("\\", "/")


class TaskDependency(Base, ScheduleMixin):
    """The association object used in Task-to-Task dependency relation."""

    from stalker import defaults

    __default_schedule_attr_name__ = "gap"  # used in docstring of ScheduleMixin
    __default_schedule_model__ = ScheduleModel.Length
    __default_schedule_timing__ = 0
    __default_schedule_unit__ = TimeUnit.Hour

    __tablename__ = "Task_Dependencies"

    # depends_on_id
    depends_on_id: Mapped[int] = mapped_column(
        ForeignKey("Tasks.id"),
        primary_key=True,
    )

    # depends_on
    depends_on: Mapped[Task] = relationship(
        back_populates="task_dependent_of",
        primaryjoin="Task.task_id==TaskDependency.depends_on_id",
    )

    # task_id
    task_id: Mapped[int] = mapped_column(ForeignKey("Tasks.id"), primary_key=True)

    # task
    task: Mapped[Task] = relationship(
        back_populates="task_depends_on",
        primaryjoin="Task.task_id==TaskDependency.task_id",
    )

    dependency_target: Mapped[DependencyTarget] = mapped_column(
        DependencyTargetDecorator(),
        nullable=False,
        doc="""The dependency target of the relation. The default value is
        "onend", which will create a dependency between two tasks so that the
        depending task will start after the task that it is depending on is
        finished.

        The dependency_target attribute is updated to
        :attr:`.DependencyTarget.OnStart` when a task has a revision and needs
        to work together with its depending tasks.
        """,
        default=DependencyTarget.OnStart,
    )

    gap_timing: Mapped[Optional[float]] = synonym(
        "schedule_timing",
        doc="""A positive float value showing the desired gap between the
        dependent and dependee tasks. The meaning of the gap value, either is
        it *work time* or *calendar time* is defined by the :attr:`.gap_model`
        attribute. So when the gap model is "duration" then the value of `gap`
        is in calendar time, if `gap` is "length" then it is considered as work
        time.
        """,
    )

    gap_unit: Mapped[Optional[str]] = synonym("schedule_unit")

    gap_model: Mapped[str] = synonym(
        "schedule_model",
        doc="""An enumeration value one of [:attr:`.ScheduleModel.Length`,
        :attr:`.ScheduleModel.Duration`]. The value of this attribute defines
        if the :attr:`.gap` value is in *Work Time* or *Calendar Time*. The
        default value is :attr:`.ScheduleModel.Length` so the gap value defines
        a time interval in work time.
        """,
    )

    def __init__(
        self,
        task: Optional["Task"] = None,
        depends_on: Optional["Task"] = None,
        dependency_target: Optional[str] = None,
        gap_timing: Optional[Union[float, int]] = 0,
        gap_unit: Optional[TimeUnit] = TimeUnit.Hour,
        gap_model: Optional[ScheduleModel] = ScheduleModel.Length,
    ) -> None:
        ScheduleMixin.__init__(
            self,
            schedule_timing=gap_timing,
            schedule_unit=gap_unit,
            schedule_model=gap_model,
        )

        self.task = task
        self.depends_on = depends_on
        self.dependency_target = dependency_target

    @validates("task")
    def _validate_task(self, key: str, task: Task) -> Task:
        """Validate the task value.

        Args:
            key (str): The name of the validated column.
            task (Task): The task value to be validated.

        Raises:
            TypeError: If the given task value is not None and not a
                :class:`stalker.models.task.Task` instance.

        Returns:
            Task: The validated task value.
        """
        # trust to the session for checking the task
        if task is not None and not isinstance(task, Task):
            raise TypeError(
                "{}.task should be and instance of stalker.models.task.Task, "
                "not {}: '{}'".format(
                    self.__class__.__name__, task.__class__.__name__, task
                )
            )
        return task

    @validates("depends_on")
    def _validate_depends_on(self, key: str, dependency: Task) -> Task:
        """Validate the task value.

        Args:
            key (str): The name of the validated column.
            dependency (Task): The depends_on value to be validated.

        Raises:
            TypeError: If the given depends_on value is not None and not a
                :class:`stalker.models.task.Task` instance.

        Returns:
            Task: The validated depends_on value.
        """
        # trust to the session for checking the depends_on attribute
        if dependency is not None and not isinstance(dependency, Task):
            raise TypeError(
                "{}.depends_on should be and instance of stalker.models.task.Task, "
                "not {}: '{}'".format(
                    self.__class__.__name__, dependency.__class__.__name__, dependency
                )
            )
        return dependency

    @validates("dependency_target")
    def _validate_dependency_target(
        self, key: str, dependency_target: Union[None, str, DependencyTarget]
    ) -> DependencyTarget:
        """Validate the given dependency_target value.

        Args:
            key (str): The name of the validated column.
            dependency_target (Union[None, str, DependencyTarget]): The
                dependency_target value to be validated.

        Returns:
            DependencyTarget: The validated dependency_target value.
        """
        from stalker import defaults

        if dependency_target is None:
            dependency_target = defaults.task_dependency_targets[0]

        dependency_target = DependencyTarget.to_target(dependency_target)

        return dependency_target

    @property
    def to_tjp(self) -> str:
        """Return the TaskJuggler representation of this TaskDependency.

        Returns:
            str: The TaskJuggler representation of this TaskDependency.
        """
        tjp = f"{self.depends_on.tjp_abs_id} {{{self.dependency_target}"
        if self.gap_timing:
            tjp += f" gap{self.gap_model} {self.gap_timing}{self.gap_unit}"
        tjp += "}"
        return tjp


# TASK_RESOURCES
Task_Resources = Table(
    "Task_Resources",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("Users.id"), primary_key=True),
)

# TASK_ALTERNATIVE_RESOURCES
Task_Alternative_Resources = Table(
    "Task_Alternative_Resources",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("Users.id"), primary_key=True),
)

# TASK_COMPUTED_RESOURCES
Task_Computed_Resources = Table(
    "Task_Computed_Resources",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("Users.id"), primary_key=True),
)

# TASK_WATCHERS
Task_Watchers = Table(
    "Task_Watchers",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("watcher_id", Integer, ForeignKey("Users.id"), primary_key=True),
)

# TASK_RESPONSIBLE
Task_Responsible = Table(
    "Task_Responsible",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("responsible_id", Integer, ForeignKey("Users.id"), primary_key=True),
)

# *****************************************************************************
# Register Events
# *****************************************************************************


# *****************************************************************************
# TimeLog updates the owner tasks parents total_logged_seconds attribute
# with new duration
@event.listens_for(TimeLog._start, "set")
def update_time_log_task_parents_for_start(
    timelog: TimeLog,
    new_start: datetime.datetime,
    old_start: datetime.datetime,
    initiator: AttributeEvent,
) -> None:
    """Update the parent task of the TimeLog.task if the new_start value is changed.

    Args:
        timelog (TimeLog): The TimeLog instance.
        new_start (datetime.datetime): The datetime.datetime instance showing the new
            value.
        old_start (datetime.datetime): The datetime.datetime instance showing the old
            value.
        initiator (AttributeEvent): Currently not used.
    """
    logger.debug(f"Received set event for new_start in target : {timelog}")
    if timelog.end and old_start and new_start:
        old_duration = timelog.end - old_start
        new_duration = timelog.end - new_start
        __update_total_logged_seconds__(timelog, new_duration, old_duration)


@event.listens_for(TimeLog._end, "set")
def update_time_log_task_parents_for_end(
    timelog: TimeLog,
    new_end: datetime.datetime,
    old_end: datetime.datetime,
    initiator: sqlalchemy.orm.attributes.AttributeEvent,
) -> None:
    """Update the parent task of the TimeLog.task if the new_end value is changed.

    Args:
        timelog (TimeLog): The TimeLog instance.
        new_end (datetime.datetime): The datetime.datetime instance showing the new
            value.
        old_end (datetime.datetime): The datetime.datetime instance showing the old
            value.
        initiator (sqlalchemy.orm.attributes.AttributeEvent): Currently not used.
    """
    logger.debug(f"Received set event for new_end in target: {timelog}")
    if (
        timelog.start
        and isinstance(old_end, datetime.datetime)
        and isinstance(new_end, datetime.datetime)
    ):
        old_duration = old_end - timelog.start
        new_duration = new_end - timelog.start
        __update_total_logged_seconds__(timelog, new_duration, old_duration)


def __update_total_logged_seconds__(
    time_log: TimeLog,
    new_duration: datetime.timedelta,
    old_duration: datetime.timedelta,
) -> None:
    """Update the given parent tasks total_logged_seconds attr with the new duration.

    Args:
        time_log (TimeLog): A :class:`.Task` instance which is the parent of the.
        new_duration (datetime.timedelta): The new duration value.
        old_duration (datetime.timedelta): The old duration value.
    """
    # if not time_log.task:
    #     logger.debug(f"TimeLog doesn't have a task yet: {time_log}")
    #     return

    logger.debug(f"TimeLog has a task: {time_log.task}")
    parent = time_log.task.parent
    if not parent:
        logger.debug("TimeLog.task doesn't have a parent!")
        return

    logger.debug(f"TImeLog.task has a parent: {parent}")

    logger.debug(f"old_duration: {old_duration}")
    logger.debug(f"new_duration: {new_duration}")

    old_total_seconds = old_duration.days * 86400 + old_duration.seconds
    new_total_seconds = new_duration.days * 86400 + new_duration.seconds

    parent.total_logged_seconds = (
        parent.total_logged_seconds - old_total_seconds + new_total_seconds
    )


# *****************************************************************************
# Task.schedule_timing updates Task.parent.schedule_seconds attribute
# *****************************************************************************
@event.listens_for(Task.schedule_timing, "set", propagate=True)
def update_parents_schedule_seconds_with_schedule_timing(
    task: Task,
    new_schedule_timing: int,
    old_schedule_timing: int,
    initiator: sqlalchemy.orm.attributes.AttributeEvent,
) -> None:
    """Update parent task's schedule_seconds attr if schedule_timing attr is updated.

    Args:
        task (Task): The base task.
        new_schedule_timing (int): An integer showing the schedule_timing of the task.
        old_schedule_timing (int): The old value of schedule_timing.
        initiator (sqlalchemy.orm.attribute.AttributeEvent): Currently not used.
    """
    logger.debug(f"Received set event for new_schedule_timing in target: {task}")
    # update parents schedule_seconds attribute
    if not task.parent:
        return

    old_schedule_seconds = task.to_seconds(
        old_schedule_timing, task.schedule_unit, task.schedule_model
    )
    new_schedule_seconds = task.to_seconds(
        new_schedule_timing, task.schedule_unit, task.schedule_model
    )
    # remove the old and add the new one
    task.parent.schedule_seconds = (
        task.parent.schedule_seconds - old_schedule_seconds + new_schedule_seconds
    )


# *****************************************************************************
# Task.schedule_unit updates Task.parent.schedule_seconds attribute
# *****************************************************************************
@event.listens_for(Task.schedule_unit, "set", propagate=True)
def update_parents_schedule_seconds_with_schedule_unit(
    task: Task,
    new_schedule_unit: str,
    old_schedule_unit: str,
    initiator: sqlalchemy.orm.attributes.AttributeEvent,
) -> None:
    """Update parent task's schedule_seconds attr if new_schedule_unit attr is updated.

    Args:
        task (Task): The base task that the schedule unit is updated of.
        new_schedule_unit (str): A string with a value of 'min', 'h', 'd', 'w', 'm' or
            'y' showing the timing unit.
        old_schedule_unit (str): The old value of new_schedule_unit.
        initiator (sqlalchemy.orm.attribute.AttributeEvent): Currently not used.
    """
    logger.debug(f"Received set event for new_schedule_unit in target: {task}")
    # update parents schedule_seconds attribute
    if not task.parent:
        return

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
    task.parent.schedule_seconds = (
        parent_schedule_seconds - old_schedule_seconds + new_schedule_seconds
    )


# *****************************************************************************
# Task.children removed
# *****************************************************************************
@event.listens_for(Task.children, "remove", propagate=True)
def update_task_date_values(
    task: Task, removed_child: Task, initiator: sqlalchemy.orm.attributes.AttributeEvent
) -> None:
    """Run when a child is removed from parent.

    Args:
        task (Task): The task that a child is removed from.
        removed_child (Task): The removed child.
        initiator (sqlalchemy.orm.attribute.AttributeEvent): Currently not used.
    """
    # update start and end date values of the task
    with DBSession.no_autoflush:
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
            task.start = datetime.datetime.now(pytz.utc)
            # this will also update end


# *****************************************************************************
# Task.depends_on set
# *****************************************************************************
@event.listens_for(Task.task_depends_on, "remove", propagate=True)
def removed_a_dependency(
    task: Task,
    task_dependency: TaskDependency,
    initiator: sqlalchemy.orm.attributes.AttributeEvent,
) -> None:
    """Update statuses when a task is removed from another tasks dependency list.

    Args:
        task (Task): The task that a dependent is being removed from.
        task_dependency (TaskDependency): The association object that has the
            relation.
        initiator (sqlalchemy.orm.attributes.AttributeEvent): Currently not used.
    """
    # update task status with dependencies
    task.update_status_with_dependent_statuses(removing=task_dependency.depends_on)


@event.listens_for(TimeLog.__table__, "after_create")
def add_exclude_constraint(
    table: sqlalchemy.sql.schema.Table,
    connection: sqlalchemy.engine.base.Connection,
    **kwargs,
) -> None:
    """Add the PostgreSQL specific ExcludeConstraint.

    Args:
        table (sqlalchemy.sql.schema.Table): The table that this event is triggered on.
        connection (sqlalchemy.engine.base.Connection): The connection instance.
        **kwargs (Any): Extra kwargs that are passed to the event.
    """
    if connection.engine.dialect.name != "postgresql":
        logger.debug("it is not a PostgreSQL database not creating Exclude Constraint")
        return

    logger.debug("add_exclude_constraint is Running!")
    # try to create the extension first
    create_extension = DDL("CREATE EXTENSION btree_gist;")
    try:
        logger.debug('running "btree_gist" extension creation!')
        connection.execute(create_extension)
        logger.debug('successfully created "btree_gist" extension!')
    except (ProgrammingError, InternalError) as e:
        logger.debug(f"add_exclude_constraint: {e}")

    # create the ts_to_box sql function
    ts_to_box = DDL(
        """CREATE FUNCTION ts_to_box(TIMESTAMPTZ, TIMESTAMPTZ)
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
"""
    )
    try:
        logger.debug("creating ts_to_box function!")
        connection.execute(ts_to_box)
        logger.debug("successfully created ts_to_box function")
    except (ProgrammingError, InternalError) as e:
        logger.debug(f"failed creating ts_to_box function!: {e}")

    # create exclude constraint
    exclude_constraint = DDL(
        """ALTER TABLE "TimeLogs" ADD CONSTRAINT
        overlapping_time_logs EXCLUDE USING GIST (
            resource_id WITH =,
            ts_to_box(start, "end") WITH &&
        )"""
    )
    try:
        logger.debug('running ExcludeConstraint for "TimeLogs" table creation!')
        connection.execute(exclude_constraint)
        logger.debug('successfully created ExcludeConstraint for "TimeLogs" table!')
    except (ProgrammingError, InternalError) as e:
        logger.debug(f"failed creating ExcludeConstraint for TimeLogs table!: {e}")
