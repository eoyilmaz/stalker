# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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
from sqlalchemy.orm import relationship, validates

from stalker.models.entity import Entity
from stalker.models.mixins import CodeMixin, ProjectMixin

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Scene(Entity, ProjectMixin, CodeMixin):
    """Stores data about Scenes.

    Scenes are grouping the Shots according to their view to the world, that is
    shots taking place in the same set configuration can be grouped together by
    using Scenes.

    You can not replace :class:`.Sequence`\ s with Scenes, because Scene
    instances doesn't have some key features that :class:`.Sequence`\ s have.

    A Scene needs to be tied to a :class:`.Project`
    instance, so it is not possible to create a Scene without a one.
    """
    __auto_name__ = False
    __tablename__ = "Scenes"
    __mapper_args__ = {"polymorphic_identity": "Scene"}
    scene_id = Column("id", Integer, ForeignKey("Entities.id"),
                      primary_key=True)

    shots = relationship(
        "Shot",
        secondary='Shot_Scenes',
        back_populates="scenes",
        doc="""The :class:`.Shot`\ s that is related with this Scene.

        It is a list of :class:`.Shot` instances.
        """
    )

    def __init__(self, shots=None, **kwargs):
        super(Scene, self).__init__(**kwargs)

        # call the mixin __init__ methods
        CodeMixin.__init__(self, **kwargs)
        ProjectMixin.__init__(self, **kwargs)

        if shots is None:
            shots = []

        self.shots = shots

    @validates("shots")
    def _validate_shots(self, key, shot):
        """validates the given shot value
        """
        from stalker.models.shot import Shot

        if not isinstance(shot, Shot):
            raise TypeError(
                '%s.shots needs to be all stalker.models.shot.Shot instances, '
                'not %s' %
                (self.__class__.__name__, shot.__class__.__name__)
            )
        return shot

    def __eq__(self, other):
        """the equality operator
        """
        return isinstance(other, Scene) and super(Scene, self).__eq__(other)

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Scene, self).__hash__()
