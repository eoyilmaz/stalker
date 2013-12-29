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

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates

from stalker.models.entity import SimpleEntity
from stalker.models.mixins import ScheduleMixin, StatusMixin

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Review(SimpleEntity, ScheduleMixin, StatusMixin):
    """Holds information about :class:`.Task` reviews.

    This class represents a very important part of the review workflow. For
    more information about the workflow please read the documentation about the
    `Stalker Task Review Workflow`_.

    .. _`Stalker Task Review Workflow`: task_review_workflow_top_level

    According to the workflow, Review instances holds information about what
    have the responsible of the task requested about the task when the resource
    asks a review from him/her/them.

    Each Review instance with the same :attr:`.revision_number` for a
    :class:`.Task` represents a set of reviews.

    .. :
      Creating a review will automatically cap the schedule timing value of the
      related task to the total logged time logs for that task and then extend
      the timing values according to the review schedule values.

    :param task: A :class:`.Task` instance that this review is related to. It
      can not be skipped.

    :type task: :class:`Task`

    :param int revision_number: This number represents the revision set id
      that this Review instance belongs to.

    :param reviewer: One of the responsible of the related Task. There will be
      only one Review instances with the same revision_number for every
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

    def __init__(self,
                 task=None,
                 reviewer=None,
                 schedule_timing=1.0,
                 schedule_unit='h',
                 schedule_model=None,
                 schedule_constraint=0,
                 **kwargs):
        SimpleEntity.__init__(self, **kwargs)
        kwargs['schedule_timing'] = schedule_timing
        kwargs['schedule_unit'] = schedule_unit
        kwargs['schedule_model'] = schedule_model
        kwargs['schedule_constraint'] = schedule_constraint

        ScheduleMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)

        self.task = task
        self.reviewer = reviewer

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

        # adjust the timing
        seconds = task.total_logged_seconds + self.schedule_seconds
        logger.debug('seconds: %s' % seconds)

        # convert the schedule_unit to the most meaningful one
        schedule_timing, schedule_unit = \
            self.least_meaningful_time_unit(seconds)

        # first set the unit to prevent task instance to reschedule itself
        # incorrectly
        task.schedule_unit = schedule_unit
        task.schedule_timing = schedule_timing

        return task
