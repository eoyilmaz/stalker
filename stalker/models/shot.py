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

from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, validates, reconstructor

from stalker import ImageFormat
from stalker.db.declarative import Base
from stalker.models.task import Task
from stalker.models.mixins import (StatusMixin, ReferenceMixin, CodeMixin)

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Shot(Task, CodeMixin):
    """Manages Shot related data.

    .. warning::

       .. deprecated:: 0.1.2

       Because most of the shots in different projects may going to have
       the same name, which is a kind of a code like SH001, SH012A etc., and
       in Stalker you can not have two entities with the same name if their
       types are also matching, to guarantee all the shots are going to have
       different names the :attr:`.name` attribute of the Shot instances are
       automatically set to a randomly generated **uuid4** sequence.

    .. note::

       .. versionadded:: 0.1.2

       The name of the shot can be freely set without worrying about clashing
       names.

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
       :class:`.Scene` instances which is another grouping attribute like
       ``sequences``. Where Sequences are grouping the Shots according to their
       temporal position to each other, Scenes are grouping the Shots according
       to their view to the world, that is shots taking place in the same set
       configuration can be grouped together by using Scenes.

    Two shots with the same :attr:`.code` can not be assigned to the same
    :class:`.Sequence`.


    .. note::

       .. versionadded:: 0.2.10

       Simplified the implementation of :attr:`.cut_in`, :attr:`.cut_out` and
       :attr:`.cut_duration` attributes. The :attr:`.cut_duration` is always
       the difference between :attr:`.cut_in` and :attr:`.cut_out` and its
       value is only be calculated when it is requested. This greatly
       simplifies the implementation of :attr:`.cut_in` and :attr:`.cut_out`
       attributes.

    The :attr:`.cut_out` and :attr:`.cut_duration` attributes effects each
    other. Setting the :attr:`.cut_out` will change the :attr:`.cut_duration`
    and setting the :attr:`.cut_duration` will change the :attr:`.cut_out`
    value. The default value of the :attr:`.cut_duration` attribute is
    calculated from the :attr:`.cut_in` and :attr:`.cut_out` attributes. If
    both :attr:`.cut_out` and :attr:`.cut_duration` arguments are set to None,
    the :attr:`.cut_duration` defaults to 1 and :attr:`.cut_out` will be set to
    :attr:`.cut_in` + :attr:`.cut_duration`. So the priority of the attributes
    are as follows:

      :attr:`.cut_in` >
      :attr:`.cut_out` >
      :attr:`.cut_duration`

    .. note::

       .. versionadded:: 0.2.4

       :attr:`.handles_at_start` and :attr:`.handles_at_end` attributes.

    :param project: This is the :class:`.Project` instance that this shot
      belongs to. A Shot can not be created without a Project instance.

    :type project: :class:`.Project`

    :param sequences: This is a list of :class:`.Sequence`\ s that this shot is
      assigned to. A Shot can be created without having a Sequence instance.

    :type sequences: list of :class:`.Sequence`

    :param int cut_in: The in frame number that this shot starts. The default
      value is 1. When the ``cut_in`` is bigger then ``cut_out``, the
      :attr:`.cut_out` attribute is set to :attr:`.cut_in` + 1.

    :param int cut_duration: The duration of this shot in frames. It should
      be zero or a positive integer value (natural number?) or . The default
      value is None.

    :param int cut_out: The out frame number that this shot ends. If it is
      given as a value lower then the ``cut_in`` parameter, then the
      :attr:`.cut_out` will be recalculated from the existent :attr:`.cut_in`
      :attr:`.cut_duration` attributes. Can be skipped. The default value is
      None.

    :param image_format: The image format of this shot. This is an optional
      variable to differentiate the image format per shot. The default value is
      the same with the Project that this Shot belongs to.

    :type image_format: :class:`.ImageFormat`
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
        doc="""The :class:`.ImageFormat` of this shot.

        This value defines the output image format of this shot, should be an
        instance of :class:`.ImageFormat`.
        """
    )

    # the cut_duration attribute is not going to be stored in the database,
    # only the cut_in and cut_out will be enough to calculate the cut_duration
    cut_in = Column(
        Integer,
        doc="The start frame of this shot. It is the start frame of the "
            "playback range in the application (Maya, Nuke etc.).",
        default=1
    )
    cut_out = Column(
        Integer,
        doc="The end frame of this shot. It is the end frame of the "
            "playback range in the application (Maya, Nuke etc.).",
        default=1
    )

    source_in = Column(
        Integer,
        doc="The start frame of the used range, should be in between"
            ":attr:`.cut_in` and :attr:`.cut_out`"
    )
    source_out = Column(
        Integer,
        doc="The end frame of the used range, should be in between"
            ":attr:`.cut_in and :attr:`.cut_out`"
    )
    record_in = Column(
        Integer,
        doc="The start frame in the Editors timeline specifying the start "
            "frame general placement of this shot."
    )
    #record_out = Column(Integer)

    def __init__(self,
                 code=None,
                 project=None,
                 sequences=None,
                 scenes=None,
                 cut_in=None,
                 cut_out=None,
                 source_in=None,
                 source_out=None,
                 record_in=None,
                 image_format=None,
                 **kwargs):

        # initialize TaskableMixin
        kwargs['project'] = project
        kwargs['code'] = code

        self._updating_cut_in_cut_out = False

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

        if cut_in is None:
            if cut_out is not None:
                cut_in = cut_out

        if cut_out is None:
            if cut_in is not None:
                cut_out = cut_in

        # if both are None set them to default values
        if cut_in is None and cut_out is None:
            cut_in = 1
            cut_out = 1

        self.cut_in = cut_in
        self.cut_out = cut_out

        if source_in is None:
            source_in = self.cut_in

        if source_out is None:
            source_out = self.cut_out

        self.source_in = source_in
        self.source_out = source_out
        self.record_in = record_in

    @reconstructor
    def __init_on_load__(self):
        """initialize on DB load
        """
        super(Shot, self).__init_on_load__()
        self._updating_cut_in_cut_out = False

    def __repr__(self):
        """the representation of the Shot
        """
        return "<%s (%s, %s)>" % (self.entity_type, self.name, self.code)

    def __eq__(self, other):
        """equality operator
        """
        return isinstance(other, Shot) and self.code == other.code and \
            self.project == other.project

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Shot, self).__hash__()

    @classmethod
    def _check_code_availability(cls, code, project):
        """checks if the given code is available in the given project

        :param code: the code string
        :param project: the stalker.models.project.Project instance that this
          shot is a part of
        :return: bool
        """
        if project and code:
            from stalker import db
            with db.DBSession.no_autoflush:
                return Shot.query\
                           .filter(Shot.project == project)\
                           .filter(Shot.code == code)\
                           .first() is None
        return True

    @validates('cut_in')
    def _validate_cut_in(self, key, cut_in):
        """validates the cut_in value
        """
        if not isinstance(cut_in, int):
            raise TypeError(
                '%(class)s.cut_in should be an int, not %(cut_in_class)s' % {
                    'class': self.__class__.__name__,
                    'cut_in_class': cut_in.__class__.__name__
                }
            )

        if self.cut_out is not None and not self._updating_cut_in_cut_out:
            if cut_in > self.cut_out:
                # lock the attribute update
                self._updating_cut_in_cut_out = True
                self.cut_out = cut_in
                self._updating_cut_in_cut_out = False

        return cut_in

    @validates('cut_out')
    def _validate_cut_out(self, key, cut_out):
        """validates the cut_out value
        """
        if not isinstance(cut_out, int):
            raise TypeError(
                '%(class)s.cut_out should be an int, not %(cut_out_class)s' % {
                    'class': self.__class__.__name__,
                    'cut_out_class': cut_out.__class__.__name__
                }
            )

        if self.cut_in is not None and not self._updating_cut_in_cut_out:
            if cut_out < self.cut_in:
                # lock the attribute update
                self._updating_cut_in_cut_out = True
                self.cut_in = cut_out
                self._updating_cut_in_cut_out = False

        return cut_out

    @validates('source_in')
    def _validate_source_in(self, key, source_in):
        """validates the source_in value
        """
        if not isinstance(source_in, int):
            raise TypeError(
                '%(class)s.source_in should be an int, not '
                '%(source_in_class)s' % {
                    'class': self.__class__.__name__,
                    'source_in_class': source_in.__class__.__name__
                }
            )

        if source_in < self.cut_in:
            raise ValueError(
                '%(class)s.source_in can not be smaller than '
                '%(class)s.cut_in, cut_in: %(cut_in)s where as '
                'source_in: %(source_in)s' % {
                    'class': self.__class__.__name__,
                    'cut_in': self.cut_in,
                    'source_in': source_in
                }
            )

        if source_in > self.cut_out:
            raise ValueError(
                '%(class)s.source_in can not be bigger than '
                '%(class)s.cut_out, cut_out: %(cut_out)s where as '
                'source_in: %(source_in)s' % {
                    'class': self.__class__.__name__,
                    'cut_out': self.cut_out,
                    'source_in': source_in
                }
            )

        if self.source_out:
            if source_in > self.source_out:
                raise ValueError(
                    '%(class)s.source_in can not be bigger than '
                    '%(class)s.source_out, source_in: %(source_in)s where '
                    'as source_out: %(source_out)s' % {
                        'class': self.__class__.__name__,
                        'source_out': self.source_out,
                        'source_in': source_in
                    }
                )

        return source_in

    @validates('source_out')
    def _validate_source_out(self, key, source_out):
        """validates the source_out value
        """
        if not isinstance(source_out, int):
            raise TypeError(
                '%(class)s.source_out should be an int, not '
                '%(source_out_class)s' % {
                    'class': self.__class__.__name__,
                    'source_out_class': source_out.__class__.__name__
                }
            )

        if source_out < self.cut_in:
            raise ValueError(
                '%(class)s.source_out can not be smaller than '
                '%(class)s.cut_in, cut_in: %(cut_in)s where as '
                'source_out: %(source_out)s' % {
                    'class': self.__class__.__name__,
                    'cut_in': self.cut_in,
                    'source_out': source_out
                }
            )

        if source_out > self.cut_out:
            raise ValueError(
                '%(class)s.source_out can not be bigger than '
                '%(class)s.cut_out, cut_out: %(cut_out)s where as '
                'source_out: %(source_out)s' % {
                    'class': self.__class__.__name__,
                    'cut_out': self.cut_out,
                    'source_out': source_out
                }
            )

        if self.source_in:
            if source_out < self.source_in:
                raise ValueError(
                    '%(class)s.source_out can not be smaller than '
                    '%(class)s.source_in, source_in: %(source_in)s where '
                    'as source_out: %(source_out)s' % {
                        'class': self.__class__.__name__,
                        'source_in': self.source_in,
                        'source_out': source_out
                    }
                )

        return source_out

    # @validates('record_in')
    # def _validate_record_in(self, key, record_in):
    #     """validates the given record_in value
    #     """
    #     # we don't really care about the record in value right now.
    #     # it can be set to anything
    #     return record_in

    @property
    def cut_duration(self):
        """getter for the cut_duration property
        """
        return self.cut_out - self.cut_in + 1

    @cut_duration.setter
    def cut_duration(self, cut_duration):
        """setter for the cut_duration property
        """
        if not isinstance(cut_duration, int):
            raise TypeError(
                '%(class)s.cut_duration should be a positive integer value, '
                'not %(cut_duration_class)s' % {
                    'class': self.__class__.__name__,
                    'cut_duration_class': cut_duration.__class__.__name__
                }
            )

        if cut_duration < 1:
            raise ValueError(
                '%(class)s.cut_duration can not be set to zero or a negative '
                'value' % {
                    'class': self.__class__.__name__
                }
            )

        # always extend or contract the shot from end
        self.cut_out = self.cut_in + cut_duration - 1

    @validates('sequences')
    def _validate_sequence(self, key, sequence):
        """validates the given sequence value
        """
        from stalker.models.sequence import Sequence

        if not isinstance(sequence, Sequence):
            raise TypeError(
                "%s.sequences should all be stalker.models.sequence.Sequence "
                "instances, not %s" %
                (self.__class__.__name__, sequence.__class__.__name__)
            )
        return sequence

    @validates('scenes')
    def _validate_scenes(self, key, scene):
        """validates the given scene value
        """
        from stalker.models.scene import Scene

        if not isinstance(scene, Scene):
            raise TypeError(
                "%s.scenes should all be stalker.models.scene.Scene "
                "instances, not %s" %
                (self.__class__.__name__, scene.__class__.__name__)
            )
        return scene

    @validates('image_format')
    def _validate_image_format(self, key, imf):
        """validates the given imf value
        """
        if imf is None:
            # use the projects image format
            from stalker import db
            with db.DBSession.no_autoflush:
                imf = self.project.image_format

        if imf is not None:
            if not isinstance(imf, ImageFormat):
                raise TypeError(
                    '%s.image_format should be an instance of '
                    'stalker.models.format.ImageFormat, not %s' %
                    (self.__class__.__name__, imf.__class__.__name__)
                )

        return imf

    @validates('code')
    def _validate_code(self, key, code):
        """validates the given code attribute
        """
        code = super(Shot, self)._validate_code(key, code)

        # check code uniqueness
        if code != self.code:
            if not self._check_code_availability(code, self.project):
                raise ValueError(
                    'There is a Shot with the same code: %s' % code
                )

        return code


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
