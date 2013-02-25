# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, synonym, reconstructor
from stalker.models.entity import TaskableEntity
from stalker.models.mixins import (StatusMixin, ReferenceMixin, CodeMixin)

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Shot(TaskableEntity, ReferenceMixin, StatusMixin, CodeMixin):
    """Manages Shot related data.

    .. deprecated:: 0.1.2

       Because most of the shots in different projects are going to have the
       same name, which is a kind of a code like SH001, SH012A etc., and in
       Stalker you can not have two entities with the same name if their types
       are also matching, to guarantee all the shots are going to have
       different names the :attr:`~stalker.models.shot.Shot.name` attribute of
       the Shot instances are automatically set to a randomly generated
       **uuid4** sequence.

    .. versionadded:: 0.1.2

       The name of the shot can be freely set without worrying about clashing
       names.

    .. versionadded:: 0.2.0

       Shot instances now have their own image format. So you can set up
       different resolutions per shot.

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

    :param sequence: The :class:`~stalker.models.sequence.Sequence` that this
      shot belongs to. A shot can only be created with a
      :class:`~stalker.models.sequence.Sequence` instance, so it can not be
      None. The shot itself will be added to the
      :attr:`~stalker.models.sequence.Sequence.shots` list of the given
      sequence. Also the ``project`` of the
      :class:`~stalker.models.sequence.Sequence` will be used to set the
      ``project`` of the current Shot.

    :type sequence: :class:`~stalker.models.sequence.Sequence`

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
    """
    __auto_name__ = True
    __tablename__ = "Shots"
    __mapper_args__ = {"polymorphic_identity": "Shot"}

    shot_id = Column("id", Integer, ForeignKey("TaskableEntities.id"),
                     primary_key=True)
    sequence_id = Column(Integer, ForeignKey("Sequences.id"))
    _sequence = relationship(
        "Sequence",
        primaryjoin="Shots.c.sequence_id==Sequences.c.id",
        back_populates="shots"
    )

    # the cut_duration attribute is not going to be stored in the database,
    # only the cut_in and cut_out will be enough to calculate the cut_duration
    _cut_in = Column(Integer)
    _cut_out = Column(Integer)

    def __init__(self,
                 code=None,
                 sequence=None,
                 cut_in=1,
                 cut_out=None,
                 cut_duration=None,
                 #assets=None,
                 **kwargs):
        sequence = self._validate_sequence(sequence)

        # initialize TaskableMixin
        kwargs['project'] = sequence.project
        kwargs['code'] = code
        #kwargs['name'] = code

        super(Shot, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        CodeMixin.__init__(self, **kwargs)

        self.sequence = self._validate_sequence(sequence)

        self._cut_in = cut_in
        self._cut_duration = cut_duration
        self._cut_out = cut_out

        self._update_cut_info(cut_in, cut_duration, cut_out)

    @reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        self._cut_duration = None
        self._update_cut_info(self._cut_in, self._cut_duration, self._cut_out)

        # call supers __init_on_load__
        super(Shot, self).__init_on_load__()

    def __repr__(self):
        """the representation of the Shot
        """
        return "<%s (%s, %s)>" % (self.entity_type, self.name, self.code)

    def __eq__(self, other):
        """equality operator
        """
        # __eq__ always returns false but to be safe the code will be added
        # here

        return isinstance(other, Shot) and self.code == other.code and \
            self.sequence == other.sequence

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

    def _validate_sequence(self, sequence):
        """validates the given sequence_in value
        """
        from stalker.models.sequence import Sequence

        if not isinstance(sequence, Sequence):
            raise TypeError("the sequence should be an instance of "
                            "stalker.models.sequence.Sequence instance")

        for shot in sequence.shots:
            if self.code == shot.code:
                raise ValueError("the given sequence already has a shot with "
                                 "a code %s" % self.code)

        return sequence

    def _sequence_getter(self):
        """The getter for the sequence attribute.
        """
        return self._sequence

    def _sequence_setter(self, sequence):
        """the setter for the sequence attribute.
        """
        self._sequence = self._validate_sequence(sequence)

    sequence = synonym(
        "_sequence",
        descriptor=property(_sequence_getter, _sequence_setter),
        doc="""The :class:`~stalker.models.sequence.Sequence` instance that
            this :class:`~stalker.models.shot.Shot` instance belongs to."""
    )

    def _cut_duration_getter(self):
        return self._cut_duration

    def _cut_duration_setter(self, cut_duration_in):
        self._update_cut_info(self._cut_in, cut_duration_in, self._cut_out)

    cut_duration = synonym(
        "_cut_duration",
        descriptor=property(_cut_duration_getter, _cut_duration_setter),
        doc="""The duration of this shot in frames.

        It should be a positive integer value. If updated also updates the
        :attr:`~stalker.models.shot.Shot.cut_duration` attribute. The default
        value is 100."""
    )

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
