# -*- coding: utf-8 -*-
"""Review related classes and functions are situated here."""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, synonym, validates

from stalker.db.declarative import Base
from stalker.db.session import DBSession
from stalker.log import get_logger
from stalker.models.entity import Entity, SimpleEntity
from stalker.models.link import Link
from stalker.models.mixins import ProjectMixin, ScheduleMixin, StatusMixin
from stalker.models.status import Status
from stalker.utils import walk_hierarchy

logger = get_logger(__name__)


class Review(SimpleEntity, ScheduleMixin, StatusMixin):
    """Manages the Task Review Workflow.

    This class represents a very important part of the review workflow. For
    more information about the workflow please read the documentation about the
    `Stalker Task Review Workflow`_.

    .. _`Stalker Task Review Workflow`: task_review_workflow_top_level

    According to the workflow, Review instances holds information about what
    have the responsible of the task requested about the task when the resource
    requested a review from the responsible.

    Each Review instance with the same :attr:`.review_number` for a
    :class:`.Task` represents a set of reviews.

    Creating a review will automatically cap the schedule timing value of the
    related task to the total logged time logs for that task and then extend
    the timing values according to the review schedule values.

    :param task: A :class:`.Task` instance that this review is related to. It
      can not be skipped.

    :type task: :class:`Task`

    :param int review_number: This number represents the revision set id
      that this Review instance belongs to.

    :param reviewer: One of the responsible of the related Task. There will be
      only one Review instances with the same review_number for every
      responsible of the same Task.

    :type reviewer: :class:`.User`

    :param schedule_timing: Holds the timing value of this review. It is a
      float value. Only useful if it is a review which ends up requesting a
      revision.

    :param schedule_unit: Holds the timing unit of this review. Only useful if
      it is a review which ends up requesting a revision.

    :param schedule_model: It holds the schedule model of this review. Only
      useful if it is a review which ends up requesting a revision.
    """

    __auto_name__ = True
    __tablename__ = "Reviews"
    __table_args__ = {"extend_existing": True}

    __mapper_args__ = {"polymorphic_identity": "Review"}

    review_id = Column("id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True)

    task_id = Column(
        Integer,
        ForeignKey("Tasks.id"),
        nullable=False,
        doc="The id of the related task.",
    )

    task = relationship(
        "Task",
        primaryjoin="Reviews.c.task_id==Tasks.c.id",
        uselist=False,
        back_populates="reviews",
        doc="The :class:`.Task` instance that this Review is created for",
    )

    reviewer_id = Column(
        Integer,
        ForeignKey("Users.id"),
        nullable=False,
        doc="The User which does the review, also on of the responsible of "
        "the related Task",
    )

    reviewer = relationship("User", primaryjoin="Reviews.c.reviewer_id==Users.c.id")

    _review_number = Column("review_number", Integer, default=1)

    def __init__(self, task=None, reviewer=None, description="", **kwargs):

        kwargs["description"] = description
        SimpleEntity.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)

        self.task = task
        self.reviewer = reviewer

        # set the status to NEW
        with DBSession.no_autoflush:
            new = Status.query.filter_by(code="NEW").first()
        self.status = new

        # set the review_number
        self._review_number = self.task.review_number + 1

    @validates("task")
    def _validate_task(self, key, task):
        """Validate the given task value.

        Args:
            key (str): The name of the validated column.
            task (Task): The task value to be validated.

        Raises:
            TypeError: If the given task value is not a Task instance.
            ValueError: If the given task is not a leaf task.

        Returns:
            Task: The validated Task instance.
        """
        if task is not None:
            from stalker.models.task import Task

            if not isinstance(task, Task):
                raise TypeError(
                    f"{self.__class__.__name__}.task should be an instance of "
                    f"stalker.models.task.Task, not {task.__class__.__name__}: '{task}'"
                )

            # is it a leaf task
            if not task.is_leaf:
                raise ValueError(
                    "It is only possible to create a review for a leaf tasks, "
                    f"and {task} is not a leaf task."
                )

            # set the review_number of this review instance
            self._review_number = task.review_number + 1

        return task

    @validates("reviewer")
    def _validate_reviewer(self, key, reviewer):
        """Validate the given reviewer value.

        Args:
            key (str): The name of the validated column.
            reviewer (User): The reviewer value to validate.

        Raises:
            TypeError: If the given reviewer is not a User instance.

        Returns:
            User: The validated reviewer value.
        """
        from stalker.models.auth import User

        if not isinstance(reviewer, User):
            raise TypeError(
                f"{self.__class__.__name__}.reviewer should be set to a "
                "stalker.models.auth.User instance, "
                f"not {reviewer.__class__.__name__}: '{reviewer}'"
            )
        return reviewer

    def _review_number_getter(self):
        """Return the review number value.

        Returns:
            int: The review_number value.
        """
        return self._review_number

    review_number = synonym(
        "_review_number",
        descriptor=property(_review_number_getter),
        doc="returns the _review_number attribute value",
    )

    @property
    def review_set(self):
        """Return all the reviews in the same review set with this one.

        Returns:
            List[Review]: The Review instances in the same review set with this one.
        """
        logger.debug(
            f"finding revisions with the same review_number of: {self.review_number}"
        )
        with DBSession.no_autoflush:
            logger.debug("using raw Python to get review set")
            reviews = []
            rev_num = self.review_number
            for review in self.task.reviews:
                if review.review_number == rev_num:
                    reviews.append(review)

        return reviews

    def is_finalized(self):
        """Check if all reviews in the same set with this one are finalized.

        Returns:
            bool: True if all the reviews in the same review set with this one are
                finalized, False otherwise.
        """
        return all([review.status.code != "NEW" for review in self.review_set])

    def request_revision(self, schedule_timing=1, schedule_unit="h", description=""):
        """Finalize the review by requesting a revision.

        Args:
            schedule_timing (float): The schedule timing value for this Review instance.
            schedule_unit (str): The schedule unit value for this Review instance.
            description (str): The description for this Review instance.
        """
        # set self timing values
        self.schedule_timing = schedule_timing
        self.schedule_unit = schedule_unit
        self.description = description

        # set self status to RREV
        with DBSession.no_autoflush:
            rrev = Status.query.filter_by(code="RREV").first()

            # set self status to RREV
            self.status = rrev

        # call finalize_review_set
        self.finalize_review_set()

    def approve(self):
        """Finalize the review by approving the task."""
        # set self status to APP
        with DBSession.no_autoflush:
            app = Status.query.filter_by(code="APP").first()
            self.status = app

        # call finalize review_set
        self.finalize_review_set()

    def finalize_review_set(self):
        """Finalize the current review set Review decisions."""
        with DBSession.no_autoflush:
            hrev = Status.query.filter_by(code="HREV").first()
            cmpl = Status.query.filter_by(code="CMPL").first()

        # check if all the reviews are finalized
        if self.is_finalized():
            logger.debug("all reviews are finalized")

            # check if there are any RREV reviews
            revise_task = False

            # now we can extend the timing of the task
            total_seconds = self.task.total_logged_seconds
            for review in self.review_set:
                if review.status.code == "RREV":
                    total_seconds += review.schedule_seconds
                    revise_task = True

            timing, unit = self.least_meaningful_time_unit(total_seconds)
            self.task._review_number += 1
            if revise_task:
                # revise the task timing if the task needs more time
                if total_seconds > self.task.schedule_seconds:
                    logger.debug(f"total_seconds including reviews: {total_seconds}")

                    self.task.schedule_timing = timing
                    self.task.schedule_unit = unit
                self.task.status = hrev
            else:
                # approve the task
                self.task.status = cmpl

                # also clamp the schedule timing
                self.task.schedule_timing = timing
                self.task.schedule_unit = unit

            # update task parent statuses
            self.task.update_parent_statuses()

            from stalker import TaskDependency

            # update dependent task statuses

            for dependency in walk_hierarchy(self.task, "dependent_of", method=1):
                logger.debug(f"current TaskDependency object: {dependency}")
                dependency.update_status_with_dependent_statuses()
                if dependency.status.code in ["HREV", "PREV", "DREV", "OH", "STOP"]:
                    # for tasks that are still be able to continue to work,
                    # change the dependency_target to "onstart" to allow
                    # the two of the tasks to work together and still let the
                    # TJ to be able to schedule the tasks correctly
                    with DBSession.no_autoflush:
                        tdeps = (
                            TaskDependency.query.filter_by(depends_to=dependency).all()
                        )
                    for tdep in tdeps:
                        tdep.dependency_target = "onstart"

                # also update the status of parents of dependencies
                dependency.update_parent_statuses()

        else:
            logger.debug("not all reviews are finalized yet!")


class Daily(Entity, StatusMixin, ProjectMixin):
    """Manages data related to **Dailies**.

    Dailies are sessions where outputs of a group of tasks are reviewed all
    together by the resources and responsible of those tasks.

    The main purpose of a ``Daily`` is to gather a group of :class:`.Link`
    instances and introduce a simple way of presenting them as a group.

    :class:`.Note` s created during a Daily session can be directly stored
    both in the :class:`.Link` and the :class:`.Daily` instances and a *join*
    will reveal which :class:`.Note` is created in which :class:`.Daily`.
    """

    __auto_name__ = False
    __tablename__ = "Dailies"
    __mapper_args__ = {"polymorphic_identity": "Daily"}

    daily_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    links = association_proxy(
        "link_relations", "link", creator=lambda n: DailyLink(link=n)
    )

    link_relations = relationship(
        "DailyLink",
        back_populates="daily",
        cascade="all, delete-orphan",
        primaryjoin="Dailies.c.id==Daily_Links.c.daily_id",
    )

    def __init__(self, links=None, **kwargs):
        super(Daily, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)
        ProjectMixin.__init__(self, **kwargs)

        if links is None:
            links = []

        self.links = links

    @property
    def versions(self):
        """Return the Version instances related to this Daily.

        Returns:
             List[Task]: A list of :class:`.Version` instances that this Daily is
                related to (through the outputs of the versions).
        """
        from stalker import Version

        return (
            Version.query.join(Version.outputs)
            .join(DailyLink)
            .join(Daily)
            .filter(Daily.id == self.id)
            .all()
        )

    @property
    def tasks(self):
        """Return the Task's related this Daily instance.

        Returns:
             List[Task]: A list of :class:`.Task` instances that this Daily is
                related to (through the outputs of the versions)
        """
        from stalker import Task, Version

        return (
            Task.query.join(Task.versions)
            .join(Version.outputs)
            .join(DailyLink)
            .join(Daily)
            .filter(Daily.id == self.id)
            .all()
        )


class DailyLink(Base):
    """The association object used in Daily-to-Link relation."""

    __tablename__ = "Daily_Links"

    daily_id = Column(Integer, ForeignKey("Dailies.id"), primary_key=True)
    daily = relationship(
        Daily,
        back_populates="link_relations",
        primaryjoin="DailyLink.daily_id==Daily.daily_id",
    )

    link_id = Column(Integer, ForeignKey("Links.id"), primary_key=True)
    link = relationship(
        Link,
        primaryjoin="DailyLink.link_id==Link.link_id",
        doc="""stalker.models.link.Link instances related to the Daily
        instance.

        Attach the same :class:`.Link` s that are linked as an output to a
        certain :class:`.Version` s instance to this attribute.

        This attribute is an **association_proxy** so and the real attribute
        that the data is related to is the :attr:`.link_relations` attribute.

        You can use the :attr:`.link_relations` attribute to change the
        ``rank`` attribute of the :class:`.DailyLink` instance (which is the
        returned data), thus change the order of the ``Links``.

        This is done in that way to be able to store the order of the links in
        this Daily instance.
        """,
    )

    # may used for sorting
    rank = Column(Integer, default=0)

    def __init__(self, daily=None, link=None, rank=0):
        super(DailyLink, self).__init__()

        self.daily = daily
        self.link = link
        self.rank = rank

    @validates("link")
    def _validate_link(self, key, link):
        """Validate the given link instance.

        Args:
            key (str): The name of the validated column.
            link (Link): The like value to be validated.

        Raises:
            TypeError: When the given like value is not a Link instance.

        Returns:
            Like: The validated Link instance.
        """
        from stalker import Link

        if link is not None and not isinstance(link, Link):
            raise TypeError(
                f"{self.__class__.__name__}.link should be an instance of "
                "stalker.models.link.Link instance, "
                f"not {link.__class__.__name__}: '{link}'"
            )

        return link

    @validates("daily")
    def _validate_daily(self, key, daily):
        """Validate the given daily instance.

        Args:
            key (str): The name of the validated column.
            daily (Daily): The daily value to be validated.

        Raises:
            TypeError: If the given daily value is not a Daily instance.

        Returns:
            Daily: The validated daily instance.
        """
        if daily is not None:
            if not isinstance(daily, Daily):
                raise TypeError(
                    f"{self.__class__.__name__}.daily should be an instance of "
                    "stalker.models.review.Daily instance, "
                    f"not {daily.__class__.__name__}: '{daily}'"
                )

        return daily
