# -*- coding: utf-8 -*-
"""Review related classes and functions are situated here."""

from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship, synonym, validates

from stalker.db.declarative import Base
from stalker.db.session import DBSession
from stalker.log import get_logger
from stalker.models.entity import Entity, SimpleEntity
from stalker.models.enum import DependencyTarget, TimeUnit, TraversalDirection
from stalker.models.file import File
from stalker.models.mixins import (
    ProjectMixin,
    ScheduleMixin,
    StatusMixin,
)
from stalker.models.status import Status
from stalker.utils import walk_hierarchy

if TYPE_CHECKING:  # pragma: no cover
    from stalker.models.auth import User
    from stalker.models.task import Task
    from stalker.models.version import Version

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

    .. version-added:: 1.0.0

      Review -> Version relation

      Versions can now be attached to reviews.

    Review instances, alongside the :class:`.Task` can also optionally hold a
    :class:`.Version` instance. This allows the information of which
    :class:`.Version` instance has been reviewed as a part of the review
    process to be much cleaner, and when the Review history is investigated,
    it will be much easier to identify which :class:`.Version` the review was
    about.

    Args:
        task (Task): A :class:`.Task` instance that this review is related to.
            It can be skipped if a :class:`.Version` instance has been given.

        version (Version): A :class:`.Version` instance that this review
            instance is related to. The :class:`.Version` and the
            :class:`.Task` should be related, a ``ValueError`` will be raised
            if they are not.

        review_number (int): This number represents the revision set id that
            this Review instance belongs to.

        reviewer (User): One of the responsible of the related Task. There will
            be only one Review instances with the same review_number for every
            responsible of the same Task.

        schedule_timing (int): Holds the timing value of this review. It is a
            float value. Only useful if it is a review which ends up requesting
            a revision.

        schedule_unit (Union[str, TimeUnit]): Holds the timing unit of this
            review. Only useful if it is a review which ends up requesting a
            revision.

        schedule_model (str): It holds the schedule model of this review. Only
            useful if it is a review which ends up requesting a revision.
    """

    __auto_name__ = True
    __tablename__ = "Reviews"
    __table_args__ = {"extend_existing": True}

    __mapper_args__ = {"polymorphic_identity": "Review"}

    review_id: Mapped[int] = mapped_column(
        "id", ForeignKey("SimpleEntities.id"), primary_key=True
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("Tasks.id"),
        nullable=False,
        doc="The id of the related task.",
    )

    task: Mapped["Task"] = relationship(
        primaryjoin="Reviews.c.task_id==Tasks.c.id",
        uselist=False,
        back_populates="reviews",
        doc="The :class:`.Task` instance that this Review is created for",
    )

    version_id: Mapped[Optional[int]] = mapped_column(
        "version_id", ForeignKey("Versions.id")
    )

    version: Mapped[Optional["Version"]] = relationship(
        primaryjoin="Reviews.c.version_id==Versions.c.id",
        uselist=False,
        back_populates="reviews",
    )

    reviewer_id: Mapped[int] = mapped_column(
        ForeignKey("Users.id"),
        nullable=False,
        doc="The User which does the review, also on of the responsible of "
        "the related Task",
    )

    reviewer: Mapped["User"] = relationship(
        primaryjoin="Reviews.c.reviewer_id==Users.c.id"
    )

    _review_number: Mapped[Optional[int]] = mapped_column("review_number", default=1)

    def __init__(
        self,
        task: Optional["Task"] = None,
        version: Optional["Version"] = None,
        reviewer: Optional["User"] = None,
        description: str = "",
        **kwargs: Dict[str, Any],
    ) -> None:
        kwargs["description"] = description
        SimpleEntity.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)

        self.task = task
        self.version = version
        self.reviewer = reviewer

        # set the status to NEW
        with DBSession.no_autoflush:
            new = Status.query.filter_by(code="NEW").first()
        self.status = new

        # set the review_number
        self._review_number = self.task.review_number + 1

    @validates("task")
    def _validate_task(
        self, key: str, task: Union[None, "Task"]
    ) -> Union[None, "Task"]:
        """Validate the given task value.

        Args:
            key (str): The name of the validated column.
            task (Union[None, Task]): The task value to be validated.

        Raises:
            TypeError: If the given task value is not a Task instance.
            ValueError: If the given task is not a leaf task.

        Returns:
            Union[None, Task]: The validated Task instance.
        """
        if task is None:
            return task

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

    @validates("version")
    def _validate_version(
        self, key: str, version: Union[None, "Version"]
    ) -> Union[None, "Version"]:
        """Validate the given version value.

        Args:
            key (str): The name of the validated column.
            version (Union[None, Version]): The version value to be validated.

        Raises:
            TypeError: If version is not a Version instance.
            ValueError: If the version.task and the self.task is not matching.

        Returns:
            Union[None, Version]: The validated version value.
        """
        if version is None:
            return version

        from stalker.models.version import Version

        if not isinstance(version, Version):
            raise TypeError(
                f"{self.__class__.__name__}.version should be a Version "
                f"instance, not {version.__class__.__name__}: '{version}'"
            )

        if self.task is not None:
            if version.task != self.task:
                raise ValueError(
                    f"{self.__class__.__name__}.version should be a Version "
                    f"instance related to this Task: {version}"
                )
        else:
            self.task = version.task

        return version

    @validates("reviewer")
    def _validate_reviewer(self, key: str, reviewer: "User") -> "User":
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

    def _review_number_getter(self) -> int:
        """Return the review number value.

        Returns:
            int: The review_number value.
        """
        return self._review_number

    review_number: Mapped[Optional[int]] = synonym(
        "_review_number",
        descriptor=property(_review_number_getter),
        doc="returns the _review_number attribute value",
    )

    @property
    def review_set(self) -> List["Review"]:
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

    def is_finalized(self) -> bool:
        """Check if all reviews in the same set with this one are finalized.

        Returns:
            bool: True if all the reviews in the same review set with this one are
                finalized, False otherwise.
        """
        return all([review.status.code != "NEW" for review in self.review_set])

    def request_revision(
        self,
        schedule_timing: Union[float, int] = 1,
        schedule_unit: Union[str, TimeUnit] = TimeUnit.Hour,
        description: str = "",
    ) -> None:
        """Finalize the review by requesting a revision.

        Args:
            schedule_timing (Union[float, int]): The schedule timing value for
                this Review instance.
            schedule_unit (Union[str, TimeUnit]): The schedule unit value for
                this Review instance.
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

    def finalize_review_set(self) -> None:
        """Finalize the current review set Review decisions."""
        with DBSession.no_autoflush:
            hrev = Status.query.filter_by(code="HREV").first()
            cmpl = Status.query.filter_by(code="CMPL").first()

        # check if all the reviews are finalized
        if not self.is_finalized():
            logger.debug("not all reviews are finalized yet!")
            return

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
        for dependency in walk_hierarchy(
            self.task, "dependent_of", method=TraversalDirection.BreadthFirst
        ):
            logger.debug(f"current TaskDependency object: {dependency}")
            dependency.update_status_with_dependent_statuses()
            if dependency.status.code in ["HREV", "PREV", "DREV", "OH", "STOP"]:
                # for tasks that are still be able to continue to work,
                # change the dependency_target to DependencyTarget.OnStart
                # to allow the two of the tasks to work together and still let
                # the TJ to be able to schedule the tasks correctly
                with DBSession.no_autoflush:
                    task_dependencies = TaskDependency.query.filter_by(
                        depends_on=dependency
                    ).all()
                for task_dependency in task_dependencies:
                    task_dependency.dependency_target = DependencyTarget.OnStart

            # also update the status of parents of dependencies
            dependency.update_parent_statuses()


class Daily(Entity, StatusMixin, ProjectMixin):
    """Manages data related to **Dailies**.

    Dailies are sessions where outputs of a group of tasks are reviewed all
    together by the resources and responsible of those tasks.

    The main purpose of a ``Daily`` is to gather a group of :class:`.File`
    instances and introduce a simple way of presenting them as a group.

    :class:`.Note` s created during a Daily session can be directly stored
    both in the :class:`.File` and the :class:`.Daily` instances and a *join*
    will reveal which :class:`.Note` is created in which :class:`.Daily`.
    """

    __auto_name__ = False
    __tablename__ = "Dailies"
    __mapper_args__ = {"polymorphic_identity": "Daily"}

    daily_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    files: Mapped[Optional[List[File]]] = association_proxy(
        "file_relations", "file", creator=lambda n: DailyFile(file=n)
    )

    file_relations: Mapped[Optional[List["DailyFile"]]] = relationship(
        back_populates="daily",
        cascade="all, delete-orphan",
        primaryjoin="Dailies.c.id==Daily_Files.c.daily_id",
    )

    def __init__(
        self,
        files: Optional[List[File]] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        super(Daily, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)
        ProjectMixin.__init__(self, **kwargs)

        if files is None:
            files = []

        self.files = files

    @property
    def versions(self) -> List["Version"]:
        """Return the Version instances related to this Daily.

        Returns:
            List[Task]: A list of :class:`.Version` instances that this Daily
                is related to (through the files attribute of the versions).
        """
        from stalker.models.version import Version

        return (
            Version.query.join(Version.files)
            .join(DailyFile)
            .join(Daily)
            .filter(Daily.id == self.id)
            .all()
        )

    @property
    def tasks(self) -> List["Task"]:
        """Return the Task's related this Daily instance.

        Returns:
            List[Task]: A list of :class:`.Task` instances that this Daily is
                related to (through the files attribute of the versions).
        """
        from stalker.models.version import Version
        from stalker.models.task import Task

        return (
            Task.query.join(Task.versions)
            .join(Version.files)
            .join(DailyFile)
            .join(Daily)
            .filter(Daily.id == self.id)
            .all()
        )


class DailyFile(Base):
    """The association object used in Daily-to-File relation."""

    __tablename__ = "Daily_Files"

    daily_id: Mapped[int] = mapped_column(
        ForeignKey("Dailies.id"),
        primary_key=True,
    )
    daily: Mapped[Daily] = relationship(
        back_populates="file_relations",
        primaryjoin="DailyFile.daily_id==Daily.daily_id",
    )

    file_id: Mapped[int] = mapped_column(
        ForeignKey("Files.id"),
        primary_key=True,
    )
    file: Mapped[File] = relationship(
        primaryjoin="DailyFile.file_id==File.file_id",
        doc="""stalker.models.file.File instances related to the Daily instance.

        Attach the same :class:`.File` instances that are linked as an output
        to a certain :class:`.Version` s instance to this attribute.

        This attribute is an **association_proxy** so and the real attribute
        that the data is related to is the :attr:`.file_relations` attribute.

        You can use the :attr:`.file_relations` attribute to change the
        ``rank`` attribute of the :class:`.DailyFile` instance (which is the
        returned data), thus change the order of the ``Files``.

        This is done in that way to be able to store the order of the files in
        this Daily instance.
        """,
    )

    # may used for sorting
    rank: Mapped[Optional[int]] = mapped_column(default=0)

    def __init__(
        self, daily: Optional[Daily] = None, file: Optional[File] = None, rank: int = 0
    ) -> None:
        super(DailyFile, self).__init__()

        self.daily = daily
        self.file = file
        self.rank = rank

    @validates("file")
    def _validate_file(self, key: str, file: Union[None, File]) -> Union[None, File]:
        """Validate the given file instance.

        Args:
            key (str): The name of the validated column.
            file (Union[None, File]): The like value to be validated.

        Raises:
            TypeError: When the given like value is not a File instance.

        Returns:
            Union[None, File]: The validated File instance.
        """
        from stalker import File

        if file is not None and not isinstance(file, File):
            raise TypeError(
                f"{self.__class__.__name__}.file should be an instance of "
                "stalker.models.file.File instance, "
                f"not {file.__class__.__name__}: '{file}'"
            )

        return file

    @validates("daily")
    def _validate_daily(
        self, key: str, daily: Union[None, Daily]
    ) -> Union[None, Daily]:
        """Validate the given daily instance.

        Args:
            key (str): The name of the validated column.
            daily (Union[None, Daily]): The daily value to be validated.

        Raises:
            TypeError: If the given daily value is not a Daily instance.

        Returns:
            Union[None, Daily]: The validated daily instance.
        """
        if daily is not None:
            if not isinstance(daily, Daily):
                raise TypeError(
                    f"{self.__class__.__name__}.daily should be an instance of "
                    "stalker.models.review.Daily instance, "
                    f"not {daily.__class__.__name__}: '{daily}'"
                )

        return daily
