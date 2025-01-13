# -*- coding: utf-8 -*-
"""FilenameTemplate related functions and classes are situated here."""
from typing import Any, Dict, Optional, Union

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, validates

from stalker.log import get_logger
from stalker.models.entity import Entity
from stalker.models.mixins import TargetEntityTypeMixin

logger = get_logger(__name__)


class FilenameTemplate(Entity, TargetEntityTypeMixin):
    """Holds templates for filename and path conventions.

    FilenameTemplate objects help to specify where to place a :class:`.Version`
    related file.

    Although, it is mainly used by Stalker to define :class:`.Version` related
    file paths and file names to place them in to proper places inside a
    :class:`.Project`'s :attr:`.Project.structure`, the idea behind is open to
    endless possibilities.

    Here is an example::

        p1 = Project(name="Test Project") # shortened for this example

        # shortened for this example
        s1 = Structure(name="Commercial Project Structure")

        # this is going to be used by Stalker to decide the :stalker:`.File`
        # :stalker:`.File.filename` and :stalker:`.File.path` (which is the way
        # Stalker links external files to Version instances)
        f1 = FilenameTemplate(
            name="Asset Version Template",
            target_entity_type="Asset",
            path='$REPO{{project.repository.id}}/{{project.code}}/{%- for parent_task in parent_tasks -%}{{parent_task.nice_name}}/{%- endfor -%}",
            filename="{{version.nice_name}}_v{{"%03d"|format(version.version_number)}}"
        )

        s1.templates.append(f1)
        p1.structure = s1

        # now because we have defined a FilenameTemplate for Assets,
        # Stalker is now able to produce a path and a filename for any Version
        # related to an asset in this project.

    Args:
        target_entity_type (str): The class name that this FilenameTemplate is designed
            for. You can also pass the class itself. So both of the examples below can
            work::

                new_filename_template1 = FilenameTemplate(target_entity_type="Asset")
                new_filename_template2 = FilenameTemplate(target_entity_type=Asset)

            A TypeError will be raised when it is skipped or it is None and a
            ValueError will be raised when it is given as and empty string.

        path (str): A `Jinja2`_ template code which specifies the path of the given
            item. It is relative to the repository root. A typical example  could be::

            '$REPO{{project.repository.id}}/{{project.code}}/{%- for parent_task in parent_tasks -%}{{parent_task.nice_name}}/{%- endfor -%}'

        filename (str): A `Jinja2`_ template code which specifies the file name of the
            given item. It is relative to the :attr:`.FilenameTemplate.path`. A typical
            example could be::

            '{{version.nice_name}}_v{{"%03d"|format(version.version_number)}}'

            Could be set to an empty string or None, the default value is None. It can
            be None, or an empty string, or it can be skipped.

    .. _Jinja2: http://jinja.pocoo.org/docs/
    """  # noqa: B950

    __auto_name__ = False
    __strictly_typed__ = False
    __tablename__ = "FilenameTemplates"
    __mapper_args__ = {"polymorphic_identity": "FilenameTemplate"}
    filenameTemplate_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )

    path: Mapped[Optional[str]] = mapped_column(
        Text, doc="""The template code for the path of this FilenameTemplate."""
    )

    filename: Mapped[Optional[str]] = mapped_column(
        Text, doc="""The template code for the file part of the FilenameTemplate."""
    )

    def __init__(
        self,
        target_entity_type: Optional[str] = None,
        path: Optional[str] = None,
        filename: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        super(FilenameTemplate, self).__init__(**kwargs)
        TargetEntityTypeMixin.__init__(self, target_entity_type, **kwargs)
        self.path = path
        self.filename = filename

    @validates("path")
    def _validate_path(self, key: str, path: Union[None, str]) -> str:
        """Validate the given path value.

        Args:
            key (str): The name of the validated column.
            path (Union[None, str]): The path value to be validated.

        Raises:
            TypeError: If the given path value is not None and not a string.

        Returns:
            str: The validated path value.
        """
        # check if it is None
        if path is None:
            path = ""

        if not isinstance(path, str):
            raise TypeError(
                "{}.path attribute should be string, not {}: '{}'".format(
                    self.__class__.__name__, path.__class__.__name__, path
                )
            )

        return path

    @validates("filename")
    def _validate_filename(self, key: str, filename: Union[None, str]) -> str:
        """Validate the given filename value.

        Args:
            key (str): The name of the validated column.
            filename (Union[None, str]): The filename value to be validated.

        Raises:
            TypeError: If the given filename value is not None and not a string.

        Returns:
            str: The validated filename value.
        """
        # check if it is None
        if filename is None:
            filename = ""

        if not isinstance(filename, str):
            raise TypeError(
                "{}.filename attribute should be string, not {}: '{}'".format(
                    self.__class__.__name__, filename.__class__.__name__, filename
                )
            )

        return filename

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is a FilenameTemplate instance and has the
                same target_entity_type, path and filename.
        """
        return (
            super(FilenameTemplate, self).__eq__(other)
            and isinstance(other, FilenameTemplate)
            and self.target_entity_type == other.target_entity_type
            and self.path == other.path
            and self.filename == other.filename
        )

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(FilenameTemplate, self).__hash__()
