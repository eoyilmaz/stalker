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
from stalker.models.mixins import ScheduleMixin

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Revision(SimpleEntity, ScheduleMixin):
    """Holds information about :class:`~stalker.models.task.Task` revisions.

    One may wanted to track all the nasty information about a revisions
    requested for a particular task. Stalker supplies
    :class:`~stalker.models.log.Revision` class for that purpose. It is
    possible to hold revision information like the revision description, who
    has given the revision and how much extra time has given for that revision
    etc. by using a Revision instance. The :attr:`.task` is a link to the
    revised :class:`~stalker.models.task.Task`.

    Creating a revision will automatically cap the schedule timing value of the
    related task to the total logged time logs for that task and then extend
    the timing values according to the revision schedule values.

    :param task: A :class:`~stalker.models.task.Task` instance that this
      revision is related to. It can not be skipped.

    :type task: :class:`~stalker.models.task.Task`

    :param schedule_timing: Holds the timing value of this revision. It is a
      float value.

    :param schedule_unit: Holds the timing unit of this revision.

    :param schedule_model: It holds the schedule model of this revision.
    """

    __auto_name__ = True
    __tablename__ = 'Revisions'
    __mapper_args__ = {"polymorphic_identity": "Revision"}
    revision_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                         primary_key=True)

    task_id = Column(
        Integer, ForeignKey("Tasks.id"), nullable=False,
        doc="""The id of the related task."""
    )

    _task = relationship(
        "Task",
        primaryjoin="Revisions.c.task_id==Tasks.c.id",
        uselist=False,
        back_populates="_revisions",
        doc="""The :class:`~stalker.models.task.Task` instance that this
        revision is created for"""
    )

    def __init__(self,
                 task=None,
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

        self._task = task

    @validates('_task')
    def _validate_task(self, key, task):
        """validates the given task value
        """
        from stalker.models.task import Task
        if not isinstance(task, Task):
            raise TypeError(
                '%s.task should be an instance of '
                'stalker.models.task.Task, not %s' % (
                    self.__class__.__name__, task.__class__.__name__
                ))

        # is it a leaf task
        if not task.is_leaf:
            raise ValueError(
                'It is only possible to give revisions to leaf tasks, and %s '
                'is not a leaf task.' % task
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

    @property
    def task(self):
        """the getter for the _task attribute
        """
        return self._task
