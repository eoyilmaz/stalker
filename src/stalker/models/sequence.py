# -*- coding: utf-8 -*-
"""Sequence related function and classes are situated here."""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, validates

from stalker.log import get_logger
from stalker.models.mixins import CodeMixin, ReferenceMixin
from stalker.models.task import Task

logger = get_logger(__name__)


class Sequence(Task, CodeMixin):
    """Stores data about Sequences.

    Sequences are a way of grouping the Shots according to their temporal
    position to each other.

    **Initialization**

    .. warning::

       .. deprecated:: 0.2.0

       Sequences do not have a lead anymore. Use the :class:`.Task.responsible`
       attribute of the super (:class:`.Task`).
    """

    __auto_name__ = False
    __tablename__ = "Sequences"
    __mapper_args__ = {"polymorphic_identity": "Sequence"}
    sequence_id = Column("id", Integer, ForeignKey("Tasks.id"), primary_key=True)

    shots = relationship(
        "Shot",
        secondary="Shot_Sequences",
        back_populates="sequences",
        doc="""The :class:`.Shot` s assigned to this Sequence.

        It is a list of :class:`.Shot` instances.
        """,
    )

    def __init__(self, **kwargs):
        super(Sequence, self).__init__(**kwargs)

        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        CodeMixin.__init__(self, **kwargs)
        self.shots = []

    @validates("shots")
    def _validate_shots(self, key, shot):
        """Validate the given shot value.

        Args:
            key (str): The name of the validated column.
            shot (Shot): The Shot instance to validate.

        Raises:
            TypeError: If the given shot is not a Shot instance.

        Returns:
            Shot: The validated shot value.
        """
        from stalker.models.shot import Shot

        if not isinstance(shot, Shot):
            raise TypeError(
                f"{self.__class__.__name__}.shots should be all "
                "stalker.models.shot.Shot instances, "
                f"not {shot.__class__.__name__}: '{shot}'"
            )
        return shot

    def __eq__(self, other):
        """Check the equality.

        Args:
            other (object): The other object.

        Returns:
            bool: True if the other object is a Sequence instance and has the same
                attributes.
        """
        return isinstance(other, Sequence) and super(Sequence, self).__eq__(other)

    def __hash__(self):
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Sequence, self).__hash__()