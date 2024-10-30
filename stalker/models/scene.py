# -*- coding: utf-8 -*-
"""Scene related classes and functions are situated here."""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, validates

from stalker.log import get_logger
from stalker.models.entity import Entity
from stalker.models.mixins import CodeMixin, ProjectMixin

logger = get_logger(__name__)


class Scene(Entity, ProjectMixin, CodeMixin):
    """Stores data about Scenes.

    Scenes are grouping the Shots according to their view to the world, that is
    shots taking place in the same set configuration can be grouped together by
    using Scenes.

    You can not replace :class:`.Sequence` s with Scenes, because Scene
    instances doesn't have some key features that :class:`.Sequence` s have.

    A Scene needs to be tied to a :class:`.Project`
    instance, so it is not possible to create a Scene without a one.
    """

    __auto_name__ = False
    __tablename__ = "Scenes"
    __mapper_args__ = {"polymorphic_identity": "Scene"}
    scene_id = Column("id", Integer, ForeignKey("Entities.id"), primary_key=True)

    shots = relationship(
        "Shot",
        secondary="Shot_Scenes",
        back_populates="scenes",
        doc="""The :class:`.Shot` s that is related with this Scene.

        It is a list of :class:`.Shot` instances.
        """,
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
        """Validate the given shot value.

        Args:
            key (str): The name of the validated column.
            shot (Shot): The shot instance.

        Raises:
            TypeError: If the shot is not a Shot instance.

        Returns:
            Shot: Return the validated Shot instance.
        """
        from stalker.models.shot import Shot

        if not isinstance(shot, Shot):
            raise TypeError(
                f"{self.__class__.__name__}.shots needs to be all "
                f"stalker.models.shot.Shot instances, not {shot.__class__.__name__}"
            )
        return shot

    def __eq__(self, other):
        """Check the equality with the other object.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is equal to this object.
        """
        return isinstance(other, Scene) and super(Scene, self).__eq__(other)

    def __hash__(self):
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Scene, self).__hash__()
