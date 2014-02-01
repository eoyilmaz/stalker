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

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, validates, synonym

from stalker.db.session import DBSession
from stalker.models.status import Status
from stalker.models.entity import SimpleEntity
from stalker.models.mixins import ScheduleMixin, StatusMixin

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
        #UniqueConstraint('task_id', '_review_number', 'reviewer_id', name='uix_1'),
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

    _review_number = Column(Integer, default=1)

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
            NEW = Status.query.filter_by(code='NEW').first()
        self.status = NEW

        # set the review_number
        self._review_number = self.task.review_number + 1

    @validates('task')
    def _validate_task(self, key, task):
        """validates the given task value
        """
        from stalker.models.task import Task
        if not isinstance(task, Task):
            raise TypeError(
                '%s.task should be an instance of stalker.models.task.Task, '
                'not %s' %
                (self.__class__.__name__, task.__class__.__name__)
            )

        # is it a leaf task
        if not task.is_leaf:
            raise ValueError(
                'It is only possible to create a review for a leaf tasks, and '
                '%s is not a leaf task.' % task
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
                '%s.reviwer should be set to a stalker.models.auth.User '
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
        reviews = []
        logger.debug('finding revisions with the same review_number of: %s' %
                     self.review_number)
        with DBSession.no_autoflush:
            # if self in DBSession:
            #     logger.debug('using SQLAlchemy to get review set')
            #     reviews = Review.query\
            #         .filter_by(task=self.task)\
            #         .filter_by(review_number=self.review_number)\
            #         .all()
            # else:
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
            RREV = Status.query.filter_by(code='RREV').first()

            # set self status to RREV
            self.status = RREV

        # call finalize_review_set
        self.finalize_review_set()

    def approve(self):
        """Finalizes the review by approving the task
        """
        # set self status to APP
        with DBSession.no_autoflush:
            APP = Status.query.filter_by(code='APP').first()
            self.status = APP

        # call finalize review_set
        self.finalize_review_set()

    def finalize_review_set(self):
        """finalizes the current review set Review decisions
        """
        with DBSession.no_autoflush:
            HREV = Status.query.filter_by(code='HREV').first()
            CMPL = Status.query.filter_by(code='CMPL').first()

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

            self.task._review_number += 1
            if revise_task:
                # revise the task
                logger.debug('total_seconds including reviews: %s' %
                             total_seconds)
                timing, unit = self.least_meaningful_time_unit(total_seconds)

                self.task.schedule_timing = timing
                self.task.schedule_unit = unit
                self.task.status = HREV
            else:
                # approve the task
                self.task.status = CMPL
                # update task parent statuses

            self.task.update_parent_statuses()

            # update dependent task statuses
            for tdep in self.task.task_dependent_of:
                dep = tdep.task
                dep.update_status_with_dependent_statuses()
                if dep.status.code in ['HREV', 'PREV', 'DREV', 'OH', 'STOP']:
                    # for tasks that are still be able to continue to work,
                    # change the dependency_target to "onstart" to allow
                    # the two of the tasks to work together and still let the
                    # TJ to be able to schedule the tasks correctly
                    tdep.dependency_target = 'onstart'
                # also update the status of parents of dependencies
                dep.update_parent_statuses()

        else:
            logger.debug('not all reviews are finilized yet!')
