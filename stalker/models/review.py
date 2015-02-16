# -*- coding: utf-8 -*-
# stalker_pyramid
# Copyright (C) 2013 Erkan Ozgur Yilmaz
#
# This file is part of stalker_pyramid.
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

import logging

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, validates, synonym

from stalker.db import Base
from stalker.db.session import DBSession
from stalker.log import logging_level
from stalker.models import walk_hierarchy
from stalker.models.entity import Entity, SimpleEntity
from stalker.models.link import Link
from stalker.models.status import Status
from stalker.models.mixins import ScheduleMixin, StatusMixin, ProjectMixin

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


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
    __tablename__ = 'Reviews'
    __table_args__ = (
        {"extend_existing": True}
    )

    __mapper_args__ = {"polymorphic_identity": "Review"}

    review_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                       primary_key=True)

    task_id = Column(
        Integer, ForeignKey("Tasks.id"), nullable=False,
        doc="The id of the related task."
    )

    task = relationship(
        "Task",
        primaryjoin="Reviews.c.task_id==Tasks.c.id",
        uselist=False,
        back_populates="reviews",
        doc="The :class:`.Task` instance that this Review is created for"
    )

    reviewer_id = Column(
        Integer, ForeignKey("Users.id"), nullable=False,
        doc="The User which does the review, also on of the responsible of "
            "the related Task"
    )

    reviewer = relationship(
        "User",
        primaryjoin='Reviews.c.reviewer_id==Users.c.id'
    )

    _review_number = Column("review_number", Integer, default=1)

    def __init__(self,
                 task=None,
                 reviewer=None,
                 description='',
                 **kwargs):

        kwargs['description'] = description
        SimpleEntity.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)

        self.task = task
        self.reviewer = reviewer

        # set the status to NEW
        with DBSession.no_autoflush:
            new = Status.query.filter_by(code='NEW').first()
        self.status = new

        # set the review_number
        self._review_number = self.task.review_number + 1

    @validates('task')
    def _validate_task(self, key, task):
        """validates the given task value
        """
        if task is not None:
            from stalker.models.task import Task

            if not isinstance(task, Task):
                raise TypeError(
                    '%s.task should be an instance of '
                    'stalker.models.task.Task, not %s' %
                    (self.__class__.__name__, task.__class__.__name__)
                )

            # is it a leaf task
            if not task.is_leaf:
                raise ValueError(
                    'It is only possible to create a review for a leaf tasks, '
                    'and %s is not a leaf task.' % task
                )

            # set the review_number of this review instance
            self._review_number = task.review_number + 1

        return task

    @validates('reviewer')
    def _validate_reviewer(self, key, reviewer):
        """validates the given reviewer value
        """
        from stalker.models.auth import User
        if not isinstance(reviewer, User):
            raise TypeError(
                '%s.reviewer should be set to a stalker.models.auth.User '
                'instance, not %s' % (self.__class__.__name__,
                                      reviewer.__class__.__name__))
        return reviewer

    def _review_number_getter(self):
        """returns the review_number value
        """
        return self._review_number

    review_number = synonym(
        '_review_number',
        descriptor=property(_review_number_getter),
        doc="returns the _review_number attribute value"
    )

    @property
    def review_set(self):
        """returns the Review instances in the same review set
        """
        logger.debug('finding revisions with the same review_number of: %s' %
                     self.review_number)
        with DBSession.no_autoflush:
            logger.debug('using raw Python to get review set')
            reviews = []
            rev_num = self.review_number
            for review in self.task.reviews:
                if review.review_number == rev_num:
                    reviews.append(review)

        return reviews

    def is_finalized(self):
        """A predicate method that checks if all reviews in the same set with
        this one is finalized
        """
        return all([review.status.code != 'NEW' for review in self.review_set])

    def request_revision(self, schedule_timing=1, schedule_unit='h',
                         description=''):
        """Finalizes the review by requesting a revision
        """
        # set self timing values
        self.schedule_timing = schedule_timing
        self.schedule_unit = schedule_unit
        self.description = description

        # set self status to RREV
        with DBSession.no_autoflush:
            rrev = Status.query.filter_by(code='RREV').first()

            # set self status to RREV
            self.status = rrev

        # call finalize_review_set
        self.finalize_review_set()

    def approve(self):
        """Finalizes the review by approving the task
        """
        # set self status to APP
        with DBSession.no_autoflush:
            app = Status.query.filter_by(code='APP').first()
            self.status = app

        # call finalize review_set
        self.finalize_review_set()

    def finalize_review_set(self):
        """finalizes the current review set Review decisions
        """
        with DBSession.no_autoflush:
            hrev = Status.query.filter_by(code='HREV').first()
            cmpl = Status.query.filter_by(code='CMPL').first()

        # check if all the reviews are finalized
        if self.is_finalized():
            logger.debug('all reviews are finalized')

            # check if there are any RREV reviews
            revise_task = False

            # now we can extend the timing of the task
            total_seconds = self.task.total_logged_seconds
            for review in self.review_set:
                if review.status.code == 'RREV':
                    total_seconds += review.schedule_seconds
                    revise_task = True

            timing, unit = self.least_meaningful_time_unit(total_seconds)
            self.task._review_number += 1
            if revise_task:
                # revise the task timing if the task needs more time
                if total_seconds > self.task.schedule_seconds:
                    logger.debug(
                        'total_seconds including reviews: %s' % total_seconds
                    )

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

            for dep in walk_hierarchy(self.task, 'dependent_of', method=1):
                logger.debug('current TaskDependency object: %s' % dep)
                dep.update_status_with_dependent_statuses()
                if dep.status.code in ['HREV', 'PREV', 'DREV', 'OH', 'STOP']:
                    # for tasks that are still be able to continue to work,
                    # change the dependency_target to "onstart" to allow
                    # the two of the tasks to work together and still let the
                    # TJ to be able to schedule the tasks correctly
                    tdeps = TaskDependency.query\
                        .filter_by(depends_to=dep).all()
                    for tdep in tdeps:
                        tdep.dependency_target = 'onstart'

                # also update the status of parents of dependencies
                dep.update_parent_statuses()

        else:
            logger.debug('not all reviews are finalized yet!')


class Daily(Entity, StatusMixin, ProjectMixin):
    """Manages data related to **Dailies**.

    Dailies are sessions where outputs of a group of tasks are reviewed all
    together by the resources and responsible of those tasks.

    The main purpose of a ``Daily`` is to gather a group of :class:`.Link`
    instances and introduce a simple way of presenting them as a group.

    :class:`.Note`\ s created during a Daily session can be directly stored
    both in the :class:`.Link` and the :class:`.Daily` instances and a *join*
    will reveal which :class:`.Note` is created in which :class:`.Daily`.
    """

    __auto_name__ = False
    __tablename__ = 'Dailies'
    __mapper_args__ = {"polymorphic_identity": "Daily"}

    daily_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    links = association_proxy(
        'link_relations',
        'link',
        creator=lambda n: DailyLink(link=n)
    )

    link_relations = relationship(
        'DailyLink',
        back_populates='daily',
        cascade='all, delete-orphan',
        primaryjoin='Dailies.c.id==Daily_Links.c.daily_id'
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
        """returns a list of :class:`.Version` instances that this Daily is
        related to (through the outputs of the versions)
        """
        from stalker import Version
        return Version.query\
            .join(Version.outputs)\
            .join(DailyLink)\
            .join(Daily)\
            .filter(Daily.id == self.id)\
            .all()

    @property
    def tasks(self):
        """returns a list of :class:`.Task` instances that this Daily is
        related to (through the outputs of the versions)
        """
        from stalker import Task, Version
        return Task.query\
            .join(Task.versions)\
            .join(Version.outputs)\
            .join(DailyLink)\
            .join(Daily)\
            .filter(Daily.id == self.id)\
            .all()


class DailyLink(Base):
    """The association object used in Daily-to-Link relation
    """

    __tablename__ = 'Daily_Links'

    daily_id = Column(Integer, ForeignKey('Dailies.id'), primary_key=True)
    daily = relationship(
        Daily,
        back_populates='link_relations',
        primaryjoin='DailyLink.daily_id==Daily.daily_id',
    )

    link_id = Column(Integer, ForeignKey('Links.id'), primary_key=True)
    link = relationship(
        Link,
        primaryjoin='DailyLink.link_id==Link.link_id',
        doc="""stalker.models.link.Link instances related to the Daily
        instance.

        Attach the same :class:`.Link`\ s that are linked as an output to a
        certain :class:`.Version`\ s instance to this attribute.

        This attribute is an **association_proxy** so and the real attribute
        that the data is related to is the :attr:`.link_relations` attribute.

        You can use the :attr:`.link_relations` attribute to change the
        ``rank`` attribute of the :class:`.DailyLink` instance (which is the
        returned data), thus change the order of the ``Links``.

        This is done in that way to be able to store the order of the links in
        this Daily instance.
        """
    )

    # may used for sorting
    rank = Column(Integer, default=0)

    def __init__(self, daily=None, link=None, rank=0):
        super(DailyLink, self).__init__()

        self.daily = daily
        self.link = link
        self.rank = rank

    @validates('link')
    def _validate_link(self, key, link):
        """validates the given link instance
        """
        from stalker import Link
        if link is not None:
            if not isinstance(link, Link):
                raise TypeError(
                    '%(class)s.link should be an instance of '
                    'stalker.models.link.Link instance, not %(link_class)s' % {
                        'class': self.__class__.__name__,
                        'link_class': link.__class__.__name__
                    }
                )

        return link

    @validates('daily')
    def _validate_daily(self, key, daily):
        """validates the given daily instance
        """
        if daily is not None:
            if not isinstance(daily, Daily):
                raise TypeError(
                    '%(class)s.daily should be an instance of '
                    'stalker.models.review.Daily instance, not '
                    '%(daily_class)s' % {
                        'class': self.__class__.__name__,
                        'daily_class': daily.__class__.__name__
                    }
                )

        return daily
