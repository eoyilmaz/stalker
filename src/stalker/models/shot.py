# -*- coding: utf-8 -*-
"""Shot related functions and classes are situated here."""

from typing import Any, Dict, Optional, TYPE_CHECKING, Union

from sqlalchemy import Float, ForeignKey
from sqlalchemy.exc import OperationalError, UnboundExecutionError
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    reconstructor,
    relationship,
    synonym,
    validates,
)

from stalker.db.session import DBSession
from stalker.log import get_logger
from stalker.models.format import ImageFormat
from stalker.models.mixins import CodeMixin, ReferenceMixin, StatusMixin
from stalker.models.task import Task

if TYPE_CHECKING:  # pragma: no cover
    from stalker.models.project import Project
    from stalker.models.scene import Scene
    from stalker.models.sequence import Sequence

logger = get_logger(__name__)


class Shot(Task, CodeMixin):
    """Manages Shot related data.

    A shot is a continuous, unbroken sequence of images that makes up a single
    part of a film. Shots are organized into :class:`.Sequence` s and
    :class:`.Scene` s :class:`.Sequence` s group shots together based on time,
    such as montage or flashback. :class:`.Scene` s group shots together based
    on location and narrative, marking where and when a specific story event
    occurs.

    .. warning::

       .. deprecated:: 0.1.2

       Because most of the shots in different projects may going to have
       the same name, which is a kind of a code like SH001, SH012A etc., and
       in Stalker you cannot have two entities with the same name if their
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

       .. versionadded:: 1.0.0

       Shot instances can only be connected to a single Sequence instance via
       the `Shot.sequence` attribute. Previously, Shots could have multiple
       Sequences, the initial purpose of that was to allow the very very rare
       case of having the same shot appear in two different sequences which
       proved itself being very useless and making things unnecessarily
       complicated. So, it has been removed and Shots can only be connected to
       a single Sequence (Shot <-> Scene relation will follow this in later
       versions/commits).

    .. note::

       .. versionadded:: 1.0.0

       Shot and Scene relation is now many-to-one, meaning a Shot can only be
       connected to a single Scene instance through the `Shot.scene` attribute.

    Two shots with the same :attr:`.code` cannot be assigned to the same
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

    .. note::

       .. versionadded:: 0.2.17.2

       Per shot FPS values. It is now possible to change the shot fps by
       setting its :attr:`.fps` attribute. The default values is same with the
       :class:`.Project` .

    Args:
        project (Project): This is the :class:`.Project` instance that this
            shot belongs to. A Shot cannot be created without a Project
            instance.

        sequence (Sequence): This is a :class:`.Sequence` that this shot is
            assigned to. A Shot can be created without having a Sequence
            instance.

        cut_in (int): The in frame number that this shot starts. The default
            value is 1. When the ``cut_in`` is bigger then ``cut_out``, the
            :attr:`.cut_out` attribute is set to :attr:`.cut_in` + 1.

        cut_duration (int): The duration of this shot in frames. It should be
            zero or a positive integer value (natural number?) or . The default
            value is None.

        cut_out (int): The out frame number that this shot ends. If it is given
            as a value lower then the ``cut_in`` parameter, then the
            :attr:`.cut_out` will be recalculated from the existent
            :attr:`.cut_in` :attr:`.cut_duration` attributes. Can be skipped.
            The default value is None.

        image_format (ImageFormat): The image format of this shot. This is an
            optional variable to differentiate the image format per shot. The
            default value is the same with the Project that this Shot belongs
            to.

        fps (float): The FPS of this shot. Default value is the same with the
            :class:`.Project` .
    """

    __auto_name__ = True
    __tablename__ = "Shots"
    __mapper_args__ = {"polymorphic_identity": "Shot"}

    shot_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Tasks.id"),
        primary_key=True,
    )

    sequence_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Sequences.id"))

    sequence: Mapped[Optional["Sequence"]] = relationship(
        primaryjoin="Shots.c.sequence_id==Sequences.c.id",
        back_populates="shots",
    )

    scene_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Scenes.id"))

    scene: Mapped[Optional["Scene"]] = relationship(
        primaryjoin="Shots.c.scene_id==Scenes.c.id",
        back_populates="shots",
    )

    image_format_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("ImageFormats.id")
    )
    _image_format: Mapped[Optional[ImageFormat]] = relationship(
        "ImageFormat",
        primaryjoin="Shots.c.image_format_id==ImageFormats.c.id",
        doc="""The :class:`.ImageFormat` of this shot.

        This value defines the output image format of this shot, should be an
        instance of :class:`.ImageFormat`.
        """,
    )

    # the cut_duration attribute is not going to be stored in the database,
    # only the cut_in and cut_out will be enough to calculate the cut_duration
    cut_in: Mapped[Optional[int]] = mapped_column(
        doc="The start frame of this shot. It is the start frame of the "
        "playback range in the application (Maya, Nuke etc.).",
        default=1,
    )
    cut_out: Mapped[Optional[int]] = mapped_column(
        doc="The end frame of this shot. It is the end frame of the "
        "playback range in the application (Maya, Nuke etc.).",
        default=1,
    )

    source_in: Mapped[Optional[int]] = mapped_column(
        doc="The start frame of the used range, should be in between"
        ":attr:`.cut_in` and :attr:`.cut_out`",
    )
    source_out: Mapped[Optional[int]] = mapped_column(
        doc="The end frame of the used range, should be in between"
        ":attr:`.cut_in and :attr:`.cut_out`",
    )
    record_in: Mapped[Optional[int]] = mapped_column(
        doc="The start frame in the Editors timeline specifying the start "
        "frame general placement of this shot.",
    )

    _fps: Mapped[Optional[float]] = mapped_column(
        "fps",
        Float(precision=3),
        doc="""The fps of the project.

        It is a float value, any other types will be converted to float. The
        default value is equal to :attr:`stalker.models.project..Project.fps`.
        """,
    )

    def __init__(
        self,
        code: Optional[str] = None,
        project: Optional["Project"] = None,
        sequence: Optional["Sequence"] = None,
        scene: Optional["Scene"] = None,
        cut_in: Optional[int] = None,
        cut_out: Optional[int] = None,
        source_in: Optional[int] = None,
        source_out: Optional[int] = None,
        record_in: Optional[int] = None,
        image_format: Optional[ImageFormat] = None,
        fps: Optional[float] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        kwargs["project"] = project
        kwargs["code"] = code

        self._updating_cut_in_cut_out = False

        super(Shot, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        CodeMixin.__init__(self, **kwargs)

        self.sequence = sequence
        self.scene = scene
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

        self.fps = fps

    @reconstructor
    def __init_on_load__(self) -> None:
        """Initialize on DB load."""
        super(Shot, self).__init_on_load__()
        self._updating_cut_in_cut_out = False

    def __repr__(self) -> str:
        """Return the string representation of this Shot instance.

        Returns:
            str: The string representation of this Shot instance.
        """
        return f"<{self.entity_type} ({self.name}, {self.code})>"

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is a Shot instance and has the same code and
                project.
        """
        return (
            isinstance(other, Shot)
            and self.code == other.code
            and self.project == other.project
        )

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Shot, self).__hash__()

    @classmethod
    def _check_code_availability(cls, code: str, project: "Project") -> bool:
        """Check if the given code is available in the given project.

        Args:
            code (str): The code to check the availability of.
            project (Project): The stalker.models.project.Project instance that this
                shot is a part of.

        Raises:
            TypeError: If the code is not a str.

        Returns:
            bool: True if the given code is available, False otherwise.
        """
        if not project or not code:
            return True

        if not isinstance(code, str):
            raise TypeError(
                "code should be a string containing a shot code, "
                f"not {code.__class__.__name__}: '{code}'"
            )

        from stalker import Project

        if not isinstance(project, Project):
            raise TypeError(
                "project should be a Project instance, "
                f"not {project.__class__.__name__}: '{project}'"
            )

        try:
            logger.debug("Try checking Shot.code with SQL expression.")
            with DBSession.no_autoflush:
                return (
                    Shot.query.filter(Shot.project == project)
                    .filter(Shot.code == code)
                    .first()
                    is None
                )
        except (UnboundExecutionError, OperationalError):
            # Fallback to Python
            logger.debug("SQL expression failed, falling back to Python!")
            for t in project.tasks:
                if isinstance(t, Shot) and t.code == code:
                    return False
        return True

    def _fps_getter(self) -> float:
        """Return the fps value either from the Project or from the _fps attribute.

        Returns:
            float: The fps attribute value.
        """
        if self._fps is None:
            return self.project.fps
        else:
            return self._fps

    def _fps_setter(self, fps: float) -> None:
        """Set the fps value.

        Args:
            fps (float): The fps value to set the fps attribute to.
        """
        self._fps = self._validate_fps(fps)

    fps: Mapped[Optional[float]] = synonym(
        "_fps",
        descriptor=property(_fps_getter, _fps_setter),
        doc="The fps of this shot.",
    )

    def _validate_fps(self, fps: Union[int, float]) -> float:
        """Validate the given fps value.

        Args:
            fps (Union[int, float]): Either an integer or float value to used as the
                fps.

        Raises:
            TypeError: If the given `fps` value is not an integer or float.
            ValueError: If the `fps` value is smaller or equal to 0.

        Returns:
            float: The validated fps value.
        """
        if fps is None:
            # fps = self.project.fps
            return None

        if not isinstance(fps, (int, float)):
            raise TypeError(
                "{}.fps should be a positive float or int, not {}: '{}'".format(
                    self.__class__.__name__, fps.__class__.__name__, fps
                )
            )

        fps = float(fps)
        if fps <= 0:
            raise ValueError(
                "{}.fps should be a positive float or int, not {}".format(
                    self.__class__.__name__, fps
                )
            )
        return float(fps)

    @validates("cut_in")
    def _validate_cut_in(self, key: str, cut_in: int) -> int:
        """Validate the cut_in value.

        Args:
            key (str): The name of the validated column.
            cut_in (int): The `cut_in` value to be validated.

        Raises:
            TypeError: If the given `cut_in` value is not an integer.

        Returns:
            int: The validated `cut_in` value.
        """
        if not isinstance(cut_in, int):
            raise TypeError(
                f"{self.__class__.__name__}.cut_in should be an int, "
                f"not {cut_in.__class__.__name__}: '{cut_in}'"
            )

        if self.cut_out is not None and not self._updating_cut_in_cut_out:
            if cut_in > self.cut_out:
                # lock the attribute update
                self._updating_cut_in_cut_out = True
                self.cut_out = cut_in
                self._updating_cut_in_cut_out = False

        return cut_in

    @validates("cut_out")
    def _validate_cut_out(self, key: str, cut_out: int) -> int:
        """Validate the cut_out value.

        Args:
            key (str): The name of the validated column.
            cut_out (int): The `cut_out` value to be validated.

        Raises:
            TypeError: If the `cut_out` value is not an integer.

        Returns:
            int: The validated `cut_out` value.
        """
        if not isinstance(cut_out, int):
            raise TypeError(
                f"{self.__class__.__name__}.cut_out should be an int, "
                f"not {cut_out.__class__.__name__}: '{cut_out}'"
            )

        if (
            self.cut_in is not None
            and not self._updating_cut_in_cut_out
            and cut_out < self.cut_in
        ):
            # lock the attribute update
            self._updating_cut_in_cut_out = True
            self.cut_in = cut_out
            self._updating_cut_in_cut_out = False

        return cut_out

    @validates("source_in")
    def _validate_source_in(self, key: str, source_in: int) -> int:
        """Validate the source_in value.

        Args:
            key (str): The name of the validated column.
            source_in (int): The `source_in` value to be validated.

        Raises:
            TypeError: If the `source_in` value is not an int.
            ValueError: If the given `source_in` value is smaller than the `cut_in`
                attribute value.
            ValueError: If the given `source_in` value is larger than the `cut_out`
                attribute value.
            ValueError: If a `source_out` is given before and the `source_in` value is
                larger than the `source_out` attribute value.

        Returns:
            int: The validated `source_in` value.
        """
        if not isinstance(source_in, int):
            raise TypeError(
                f"{self.__class__.__name__}.source_in should be an int, "
                f"not {source_in.__class__.__name__}: '{source_in}'"
            )

        if source_in < self.cut_in:
            raise ValueError(
                "{cls}.source_in cannot be smaller than "
                "{cls}.cut_in, cut_in: {cut_in} where as "
                "source_in: {source_in}".format(
                    cls=self.__class__.__name__,
                    cut_in=self.cut_in,
                    source_in=source_in,
                )
            )

        if source_in > self.cut_out:
            raise ValueError(
                "{cls}.source_in cannot be bigger than "
                "{cls}.cut_out, cut_out: {cut_out} where as "
                "source_in: {source_in}".format(
                    cls=self.__class__.__name__,
                    cut_out=self.cut_out,
                    source_in=source_in,
                )
            )

        if self.source_out and source_in > self.source_out:
            raise ValueError(
                "{cls}.source_in cannot be bigger than "
                "{cls}.source_out, source_in: {source_in} where "
                "as source_out: {source_out}".format(
                    cls=self.__class__.__name__,
                    source_out=self.source_out,
                    source_in=source_in,
                )
            )

        return source_in

    @validates("source_out")
    def _validate_source_out(self, key: str, source_out: int) -> int:
        """Validate the source_out value.

        Args:
            key (str): The name of the validated column.
            source_out (int): The source_out value to be validated.

        Raises:
            TypeError: If the source_out is not an integer.
            ValueError: If the source_out is smaller than the cut_in attribute value.
            ValueError: If the source_out is larger than the cut_out attribute value.
            ValueError: If the source_in is not None and source_out is smaller than the
                source_in value.

        Returns:
            int: The validated source_out value.
        """
        if not isinstance(source_out, int):
            raise TypeError(
                f"{self.__class__.__name__}.source_out should be an int, "
                f"not {source_out.__class__.__name__}: '{source_out}'"
            )

        if source_out < self.cut_in:
            raise ValueError(
                "{cls}.source_out cannot be smaller than "
                "{cls}.cut_in, cut_in: {cut_in} where as "
                "source_out: {source_out}".format(
                    cls=self.__class__.__name__,
                    cut_in=self.cut_in,
                    source_out=source_out,
                )
            )

        if source_out > self.cut_out:
            raise ValueError(
                "{cls}.source_out cannot be bigger than "
                "{cls}.cut_out, cut_out: {cut_out} where as "
                "source_out: {source_out}".format(
                    cls=self.__class__.__name__,
                    cut_out=self.cut_out,
                    source_out=source_out,
                )
            )

        if self.source_in and source_out < self.source_in:
            raise ValueError(
                "{cls}.source_out cannot be smaller than "
                "{cls}.source_in, source_in: {source_in} where "
                "as source_out: {source_out}".format(
                    cls=self.__class__.__name__,
                    source_in=self.source_in,
                    source_out=source_out,
                )
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
    def cut_duration(self) -> int:
        """Return the cut_duration property value.

        Returns:
            int: The cut_duration property value.
        """
        return self.cut_out - self.cut_in + 1

    @cut_duration.setter
    def cut_duration(self, cut_duration: int) -> None:
        """Set the cut_duration attribute.

        Args:
            cut_duration (int): The cut_duration value to be validated.

        Raises:
            TypeError: If the given cut_duration value is not an integer.
            ValueError: If the given cut_duration value is not a positive integer.
        """
        if not isinstance(cut_duration, int):
            raise TypeError(
                f"{self.__class__.__name__}.cut_duration should be a positive "
                "integer value, "
                f"not {cut_duration.__class__.__name__}: '{cut_duration}'"
            )

        if cut_duration < 1:
            raise ValueError(
                f"{self.__class__.__name__}.cut_duration cannot be set to "
                "zero or a negative value"
            )

        # always extend or contract the shot from end
        self.cut_out = self.cut_in + cut_duration - 1

    @validates("sequence")
    def _validate_sequence(self, key: str, sequence: "Sequence") -> "Sequence":
        """Validate the given sequence value.

        Args:
            key (str): The name of the validated column.
            sequence (Sequence): The sequence value to validate.

        Raises:
            TypeError: If the given sequence value is not a Sequence instance.

        Returns:
            Sequence: The validated Sequence instance.
        """
        from stalker.models.sequence import Sequence

        if sequence is not None and not isinstance(sequence, Sequence):
            raise TypeError(
                f"{self.__class__.__name__}.sequence should be a "
                "stalker.models.sequence.Sequence instance, "
                f"not {sequence.__class__.__name__}: '{sequence}'"
            )
        return sequence

    @validates("scene")
    def _validate_scene(self, key: str, scene: "Scene") -> "Scene":
        """Validate the given scene value.

        Args:
            key (str): The name of the validated column.
            scene (Scene): The scene value to validate.

        Raises:
            TypeError: If the given scene is not a Scene instance.

        Returns:
            Scene: The validated Scene instance.
        """
        from stalker.models.scene import Scene

        if scene is not None and not isinstance(scene, Scene):
            raise TypeError(
                f"{self.__class__.__name__}.scene should be a "
                "stalker.models.scene.Scene instance, "
                f"not {scene.__class__.__name__}: '{scene}'"
            )
        return scene

    def _image_format_getter(self) -> ImageFormat:
        """Return image_format value from the Project or from the _image_format attr.

        Returns:
            ImageFormat: The ImageFormat instance from image_format attribute or from
                the related Project's image_format attribute.
        """
        if self._image_format is None:
            return self.project.image_format
        else:
            return self._image_format

    def _image_format_setter(self, imf: ImageFormat) -> None:
        """Set the image_format value.

        Args:
            imf (ImageFormat): The ImageFormat instance to set the image_format
                attribute value.
        """
        self._image_format = self._validate_image_format(imf)

    image_format: Mapped[Optional[ImageFormat]] = synonym(
        "_image_format",
        descriptor=property(_image_format_getter, _image_format_setter),
        doc="The image_format of this shot. Set it to None to re-sync with "
        "Project.image_format.",
    )

    def _validate_image_format(
        self, imf: Union[None, ImageFormat]
    ) -> Union[None, ImageFormat]:
        """Validate the given imf value.

        Args:
            imf (ImageFormat): The ImageFormat instance to validate.

        Raises:
            TypeError: If the given imf value is not an ImageFormat instance.

        Returns:
            ImageFormat: The validated ImageFormat instance.
        """
        if imf is None:
            # do not set it to anything it will automatically use the project
            # image format
            return None

        if not isinstance(imf, ImageFormat):
            raise TypeError(
                f"{self.__class__.__name__}.image_format should be an instance of "
                "stalker.models.format.ImageFormat, "
                f"not {imf.__class__.__name__}: '{imf}'"
            )

        return imf

    @validates("code")
    def _validate_code(self, key: str, code: str) -> str:
        """Validate the given code value.

        Args:
            key (str): The name of the validated column.
            code (str): The code to validate.

        Raises:
            ValueError: If the code is not available.

        Returns:
            str: The validated code value.
        """
        code = super(Shot, self)._validate_code(key, code)

        # check code uniqueness
        if code != self.code and not self._check_code_availability(code, self.project):
            raise ValueError(f"There is a Shot with the same code: {code}")

        return code
