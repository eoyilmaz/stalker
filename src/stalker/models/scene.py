# -*- coding: utf-8 -*-
"""Scene related classes and functions are situated here."""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from stalker.log import get_logger
from stalker.models.mixins import CodeMixin
from stalker.models.task import Task

if TYPE_CHECKING:  # pragma: no cover
    from stalker.models.shot import Shot

logger = get_logger(__name__)


class Scene(Task, CodeMixin):
    """Stores data about Scenes.

    Scenes are grouping the Shots according to their view to the world, that is
    shots taking place in the same set configuration can be grouped together by
    using Scenes.

    You cannot replace :class:`.Sequence` s with Scenes, because Scene
    instances doesn't have some key features that :class:`.Sequence` s have.

    A Scene needs to be tied to a :class:`.Project`
    instance, so it is not possible to create a Scene without a one.
    """

    __auto_name__ = False
    __tablename__ = "Scenes"
    __mapper_args__ = {"polymorphic_identity": "Scene"}
    scene_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Tasks.id"),
        primary_key=True,
    )

    shots: Mapped[Optional[List["Shot"]]] = relationship(
        primaryjoin="Shots.c.scene_id==Scenes.c.id",
        back_populates="scene",
        doc="""The :class:`.Shot` s that is related with this Scene.

        It is a list of :class:`.Shot` instances.
        """,
    )

    def __init__(self, shots: Optional[List["Shot"]] = None, **kwargs: Dict[str, Any]):
        super(Scene, self).__init__(**kwargs)

        # call the mixin __init__ methods
        CodeMixin.__init__(self, **kwargs)

        if shots is None:
            shots = []

        self.shots = shots

    @validates("shots")
    def _validate_shots(self, key: str, shot: "Shot") -> "Shot":
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
                f"{self.__class__.__name__}.shots should only contain "
                "instances of stalker.models.shot.Shot, "
                f"not {shot.__class__.__name__}: '{shot}'"
            )
        return shot

    def __eq__(self, other: Any) -> bool:
        """Check the equality with the other object.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is equal to this object.
        """
        return isinstance(other, Scene) and super(Scene, self).__eq__(other)

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Scene, self).__hash__()
