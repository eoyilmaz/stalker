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

from stalker.models.entity import SimpleEntity


class Revision(SimpleEntity):
    """Holds information about :class:`~stalker.models.task.Task` revisions.

    One may wanted to track all the dirty nasty about a revisions requested
    for a particular task. Stalker supplies
    :class:`~stalker.models.log.Revision` class for that purpose. It is
    possible to hold revision information like the revision description, who
    has given the revision and how much extra time has given for that revision
    etc. by using a Revision instance. The :attr:`.revision_of` is a link to
    the revised :class:`~stalker.models.task.Task`.

    :param task: A :class:`~stalker.models.task.Task` instance that this
      revision is related to.

    :type task: :class:`~stalker.models.task.Task`

    :param schedule_timing: Holds the timing value of this revision. It is a
      float value.

    :param schedule_unit: Holds the timing unit of this revision.

    :param schedule_model: As in tasks, it hold the 
    """

    __auto_name__ = True

    pass
