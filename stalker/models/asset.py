# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from sqlalchemy import Column, Integer, ForeignKey
from stalker.models.task import Task
from stalker.models.mixins import ReferenceMixin, CodeMixin

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Asset(Task, CodeMixin):
    """The Asset class is the whole idea behind Stalker.

    *Assets* are containers of :class:`~stalker.models.task.Task`\ s. And
    :class:`~stalker.models.task.Task`\ s are the smallest meaningful part that
    should be accomplished to complete the
    :class:`~stalker.models.project.Project`.

    An example could be given as follows; you can create an asset for one of
    the characters in your project. Than you can divide this character asset in
    to :class:`~stalker.models.task.Task`\ s. These
    :class:`~stalker.models.task.Task`\ s can be defined by the type of the
    :class:`~stalker.models.asset.Asset`, which is a
    :class:`~stalker.models.type.Type` object created specifically for
    :class:`~stalker.models.asset.Asset` (ie. has its
    :attr:`~stalker.models.type.Type.target_entity_type` set to "Asset"),

    An :class:`~stalker.models.asset.Asset` instance should be initialized with
    a :class:`~stalker.models.project.Project` instance (as the other classes
    which are mixed with the :class:`~stalker.models.mixins.TaskMixin`). And
    when a :class:`~stalker.models.project.Project` instance is given then the
    asset will append itself to the
    :attr:`~stalker.models.project.Project.assets` list.

    ..versionadded: 0.2.0:
        No more Asset to Shot connection:

        Assets now are not directly related to Shots. Instead a
        :class:`~stalker.models.Version` will reference the Asset and then it
        is easy to track which shots are referencing this Asset by querying
        with a join of Shot Versions referencing this Asset.
    """
    __auto_name__ = False
    __strictly_typed__ = True
    __tablename__ = "Assets"
    __mapper_args__ = {"polymorphic_identity": "Asset"}

    asset_id = Column("id", Integer, ForeignKey("Tasks.id"),
                      primary_key=True)

    def __init__(self, code, **kwargs):
        kwargs['code'] = code

        super(Asset, self).__init__(**kwargs)
        CodeMixin.__init__(self, **kwargs)
        ReferenceMixin.__init__(self, **kwargs)

    def __eq__(self, other):
        """the equality operator
        """
        return super(Asset, self).__eq__(other) and \
               isinstance(other, Asset) and self.type == other.type
