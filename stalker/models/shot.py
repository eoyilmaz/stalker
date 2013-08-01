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

from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, synonym, reconstructor, validates

from stalker import ImageFormat
from stalker.db import Base
from stalker.models.task import Task
from stalker.models.mixins import (StatusMixin, ReferenceMixin, CodeMixin)

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


# TODO: Add handles_at_start and handles_at_end attributes
class Shot(Task, CodeMixin):
    """Manages Shot related data.

    .. warning::

       .. deprecated:: 0.1.2

       Because most of the shots in different projects are going to have
       the same name, which is a kind of a code like SH001, SH012A etc., and
       in Stalker you can not have two entities with the same name if their
       types are also matching, to guarantee all the shots are going to have
       different names the :attr:`~stalker.models.shot.Shot.name` attribute
       of the Shot instances are automatically set to a randomly generated
       **uuid4** sequence.

    .. note::

       .. versionadded:: 0.1.2

       The name of the shot can be freely set without worrying about
       clashing names.

    .. note::

       .. versionadded:: 0.2.0

       Shot instances now can have their own image format. So you can set up
       different resolutions per shot.

    .. note::

       .. versionadded:: 0.2.0

       Shot instances can now be created with a Project instance only, without
       needing a Sequence instance. Sequences are now a kind of a grouping
       attribute for the Shots. And Shots can have more than one Sequence.

    .. note::

       .. versionadded:: 0.2.0

       Shots now have a new attribute called ``scenes``, holding
       :class:`~stalker.models.scene.Scene` instances which is another grouping
       attribute like ``sequences``. Where Sequences are grouping the Shots
       according to their temporal position to each other, Scenes are grouping
       the Shots according to their view to the world, that is shots taking
       place in the same set configuration can be grouped together by using
       Scenes.

    Two shots with the same :attr:`~stalker.models.shot.Shot.code` can not be
    assigned to the same :class:`~stalker.models.sequence.Sequence`.

    The :attr:`~stalker.models.shot.Shot.cut_out` and
    :attr:`~stalker.models.shot.Shot.cut_duration` attributes effects each
    other. Setting the :attr:`~stalker.models.shot.Shot.cut_out` will change
    the :attr:`~stalker.models.shot.Shot.cut_duration` and setting the
    :attr:`~stalker.models.shot.Shot.cut_duration` will change the
    :attr:`~stalker.models.shot.Shot.cut_out` value. The default value of the
    :attr:`~stalker.models.shot.Shot.cut_out` attribute is calculated from the
    :attr:`~stalker.models.shot.Shot.cut_in` and
    :attr:`~stalker.models.shot.Shot.cut_duration` attributes. If both
    :attr:`~stalker.models.shot.Shot.cut_out` and
    :attr:`~stalker.models.shot.Shot.cut_duration` arguments are set to None,
    the :attr:`~stalker.models.shot.Shot.cut_duration` defaults to 100 and
    :attr:`~stalker.models.shot.Shot.cut_out` will be set to
    :attr:`~stalker.models.shot.Shot.cut_in` +
    :attr:`~stalker.models.shot.Shot.cut_duration`. So the priority of the
    attributes are as follows:

      :attr:`~stalker.models.shot.Shot.cut_in` >
      :attr:`~stalker.models.shot.Shot.cut_duration` >
      :attr:`~stalker.models.shot.Shot.cut_out`

    For still images (which can be also managed by shots) the
    :attr:`~stalker.models.shot.Shot.cut_in` and
    :attr:`~stalker.models.shot.Shot.cut_out` can be set to the same value
    so the :attr:`~stalker.models.shot.Shot.cut_duration` can be set to zero.

    Because Shot is getting its relation to a
    :class:`~stalker.models.project.Project` from the
    passed :class:`~stalker.models.sequence.Sequence`, you can skip the
    ``project`` argument, and if you not the value of the ``project`` argument
    is not going to be used.

    :param project: This is the :class:`~stalker.models.project.Project`
      instance that this shot belongs to. A Shot can not be created without a
      Project instance.

    :type project: :class:`~stalker.models.project.Project`

    :param sequences: This is a list of
      :class:`~stalker.models.sequence.Sequence`\ s that this shot is assigned
      to. A Shot can be created without having a Sequence instance.

    :type sequences: list of :class:`~stalker.models.sequence.Sequence`

    :param integer cut_in: The in frame number that this shot starts. The
      default value is 1. When the ``cut_in`` is bigger then
      ``cut_out``, the :attr:`~stalker.models.shot.Shot.cut_out` attribute is
      set to :attr:`~stalker.models.shot.Shot.cut_in` + 1.

    :param integer cut_duration: The duration of this shot in frames. It should
      be zero or a positive integer value (natural number?) or . The default
      value is None.

    :param integer cut_out: The out frame number that this shot ends. If it is
      given as a value lower then the ``cut_in`` parameter, then the
      :attr:`~stalker.models.shot.Shot.cut_out` will be set to the same value
      with :attr:`~stalker.models.shot.Shot.cut_in` and the
      :attr:`~stalker.models.shot.Shot.cut_duration` attribute will be set to
      1. Can be skipped. The default value is None.

    :param image_format: The image format of this shot. This is an optional
      variable to differentiate the image format per shot. The default value is
      the same with the Project that this Shot belongs to.

    :type image_format: :class:`~stalker.models.format.ImageFormat`
    """
    __auto_name__ = True
    __tablename__ = 'Shots'
    __mapper_args__ = {'polymorphic_identity': 'Shot'}

    shot_id = Column('id', Integer, ForeignKey('Tasks.id'),
                     primary_key=True)

    sequences = relationship(
        'Sequence',
        secondary='Shot_Sequences',
        primaryjoin='Shots.c.id==Shot_Sequences.c.shot_id',
        secondaryjoin='Shot_Sequences.c.sequence_id==Sequences.c.id',
        back_populates='shots'
    )

    scenes = relationship(
        'Scene',
        secondary='Shot_Scenes',
        primaryjoin='Shots.c.id==Shot_Scenes.c.shot_id',
        secondaryjoin='Shot_Scenes.c.scene_id==Scenes.c.id',
        back_populates='shots'
    )

    image_format_id = Column(Integer, ForeignKey("ImageFormats.id"))
    image_format = relationship(
        "ImageFormat",
        primaryjoin="Shots.c.image_format_id==ImageFormats.c.id",
        doc="""The :class:`~stalker.models.format.ImageFormat` of this shot.

        This value defines the output image format of this shot, should be an
        instance of :class:`~stalker.models.format.ImageFormat`.
        """
    )

    # the cut_duration attribute is not going to be stored in the database,
    # only the cut_in and cut_out will be enough to calculate the cut_duration
    _cut_in = Column(Integer)
    _cut_out = Column(Integer)

    def __init__(self,
                 code=None,
                 project=None,
                 sequences=None,
                 scenes=None,
                 cut_in=1,
                 cut_out=None,
                 cut_duration=None,
                 image_format=None,
                 **kwargs):

        # initialize TaskableMixin
        kwargs['project'] = project
        kwargs['code'] = code

        # check for the code and project before ProjectMixin
        self._check_code_availability(code, project)

        super(Shot, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        CodeMixin.__init__(self, **kwargs)

        if sequences is None:
            sequences = []
        self.sequences = sequences

        if scenes is None:
            scenes = []
        self.scenes = scenes

        self.image_format = image_format

        self._cut_in = cut_in
        self._cut_duration = cut_duration
        self._cut_out = cut_out

        self._update_cut_info(cut_in, cut_duration, cut_out)

    def __repr__(self):
        """the representation of the Shot
        """
        return "<%s (%s, %s)>" % (self.entity_type, self.name, self.code)

    def __eq__(self, other):
        """equality operator
        """
        return isinstance(other, Shot) and self.code == other.code and \
               self.project == other.project

    def _check_code_availability(self, code, project):
        """checks if the given code is available in the given project

        :param code: the code string
        :param project: the stalker.models.project.Project instance that this
          shot is a part of
        :return: bool
        """
        if project and code:
            # the shots are task instances, use project.tasks
            for task in project.tasks:
                if isinstance(task, Shot):
                    shot = task
                    if shot.code == code:
                        raise ValueError("The given project already has a "
                                         "Shot with a code of %s" % self.code)
        return True

    def _update_cut_info(self, cut_in, cut_duration, cut_out):
        """updates the cut_in, cut_duration and cut_out attributes
        """
        # validate all the values
        self._cut_in = self._validate_cut_in(cut_in)
        self._cut_duration = self._validate_cut_duration(cut_duration)
        self._cut_out = self._validate_cut_out(cut_out)

        if self._cut_in is None:
            self._cut_in = 1

        if self._cut_out is not None:
            if self._cut_in > self._cut_out:
                # just update cut_duration
                self._cut_duration = 1
                #else:
                #self._cut_o

        if self._cut_duration is None or self._cut_duration <= 0:
            self._cut_duration = 1

        self._cut_out = self._cut_in + self._cut_duration - 1

    def _validate_cut_duration(self, cut_duration_in):
        """validates the given cut_duration value
        """
        if cut_duration_in is not None and \
                not isinstance(cut_duration_in, int):
            raise TypeError("cut_duration should be an instance of int")

        return cut_duration_in

    def _validate_cut_in(self, cut_in_in):
        """validates the given cut_in_in value
        """
        if cut_in_in is not None:
            if not isinstance(cut_in_in, int):
                raise TypeError("cut_in should be an instance of int")

        return cut_in_in

    def _validate_cut_out(self, cut_out_in):
        """validates the given cut_out_in value
        """
        if cut_out_in is not None:
            if not isinstance(cut_out_in, int):
                raise TypeError("cut_out should be an instance of int")

        return cut_out_in

    @validates('sequences')
    def _validate_sequence(self, key, sequence):
        """validates the given sequence value
        """
        from stalker.models.sequence import Sequence

        if not isinstance(sequence, Sequence):
            raise TypeError("%s.sequences should all be "
                            "stalker.models.sequence.Sequence instances, not "
                            "%s" % (self.__class__.__name__,
                                    sequence.__class__.__name__))
        return sequence

    @validates('scenes')
    def _validate_scenes(self, key, scene):
        """validates the given scene value
        """
        from stalker.models.scene import Scene

        if not isinstance(scene, Scene):
            raise TypeError("%s.scenes should all be "
                            "stalker.models.scene.Scene instances, not "
                            "%s" % (self.__class__.__name__,
                                    scene.__class__.__name__))
        return scene

    @validates('image_format')
    def _validate_image_format(self, key, imf):
        """validates the given imf value
        """
        if imf is None:
            # use the projects image format
            imf = self.project.image_format

        if imf is not None:
            if not isinstance(imf, ImageFormat):
                raise TypeError('%s.image_format should be an instance of '
                                'stalker.models.format.ImageFormat, not %s' %
                                (self.__class__.__name__, imf.__class__.__name__))

        return imf

    @property
    def cut_duration(self):
        try:
            if self._cut_duration is None:
                self._update_cut_info(self._cutin, None, self._cut_out)
        except AttributeError:
            setattr(self, '_cut_duration', None)
            self._update_cut_info(self._cut_in, None, self._cut_out)
        return self._cut_duration

    @cut_duration.setter
    def cut_duration(self, cut_duration_in):
        self._update_cut_info(self._cut_in, cut_duration_in, self._cut_out)

    def _cut_in_getter(self):
        return self._cut_in

    def _cut_in_setter(self, cut_in_in):
        self._update_cut_info(cut_in_in, self._cut_duration, self._cut_out)

    cut_in = synonym(
        "_cut_in",
        descriptor=property(_cut_in_getter, _cut_in_setter),
        doc="""The in frame number that this shot starts.

        The default value is 1. When the cut_in is bigger then
        :attr:`~stalker.models.shot.Shot.cut_out`, the
        :attr:`~stalker.models.shot.Shot.cut_out` value is update to
        :attr:`~stalker.models.shot.Shot.cut_in` + 1."""
    )

    def _cut_out_getter(self):
        if self._cut_out is None:
            self._update_cut_info(self._cut_in, self._cut_duration, None)
        return self._cut_out

    def _cut_out_setter(self, cut_out_in):
        self._update_cut_info(self._cut_in, self._cut_duration, cut_out_in)

    cut_out = synonym(
        "_cut_out",
        descriptor=property(_cut_out_getter, _cut_out_setter),
        doc="""The out frame number that this shot ends.

        When the :attr:`~stalker.models.shot.Shot.cut_out` is set to a value
        lower than :attr:`~stalker.models.shot.Shot.cut_in`,
        :attr:`~stalker.models.shot.Shot.cut_out` will be updated to
        :attr:`~stalker.models.shot.Shot.cut_in` + 1. The default value is
        :attr:`~stalker.models.shot.Shot.cut_in` +
        :attr:`~stalker.models.shot.Shot.cut_duration`."""
    )


Shot_Sequences = Table(
    'Shot_Sequences', Base.metadata,
    Column('shot_id', Integer, ForeignKey('Shots.id'), primary_key=True),
    Column('sequence_id', Integer, ForeignKey('Sequences.id'),
           primary_key=True)
)

Shot_Scenes = Table(
    'Shot_Scenes', Base.metadata,
    Column('shot_id', Integer, ForeignKey('Shots.id'), primary_key=True),
    Column('scene_id', Integer, ForeignKey('Scenes.id'), primary_key=True)
)

