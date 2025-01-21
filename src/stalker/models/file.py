# -*- coding: utf-8 -*-
"""File related classes and utility functions are situated here."""

import os
from typing import Any, Dict, Generator, List, Optional, Union

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, validates

from stalker.log import get_logger
from stalker.models.entity import Entity
from stalker.models.enum import TraversalDirection
from stalker.models.mixins import ReferenceMixin
from stalker.utils import walk_hierarchy


logger = get_logger(__name__)


class File(Entity, ReferenceMixin):
    """Holds data about files or file sequences.

    Files are all about giving some external information to the current entity
    (external to the database, so it can be something on the
    :class:`.Repository` or in the Web or anywhere that the server can reach).
    The type of the file (general, file, folder, web page, image, image
    sequence, video, movie, sound, text etc.) can be defined by a
    :class:`.Type` instance (you can also use multiple :class:`.Tag` instances
    to add more information, and to filter them back). Again it is defined by
    the needs of the studio.

    For sequences of files the file name should be in "%h%p%t %R" format in
    PySeq_ formatting rules.

    There are three secondary attributes (properties to be more precise)
    ``path``, ``filename`` and ``extension``. These attributes are derived from
    the :attr:`.full_path` attribute and they modify it.

    Path
        It is the path part of the full_path.

    Filename
        It is the filename part of the full_path, also includes the extension,
        so changing the filename also changes the extension part.

    Extension
        It is the extension part of the full_path. It also includes the
        extension separator ('.' for most of the file systems).

    .. versionadded:: 1.1.0

       Inputs or references can now be tracked per File instance through the
       :attr:`.File.references` attribute. So, that all the references can be
       tracked per individual file instance.

    Args:
        full_path (str): The full path to the File, it can be a path to a
            folder or a file in the file system, or a web page. For file
            sequences use "%h%p%t %R" format, for more information see
            `PySeq Documentation`_. It can be set to empty string (or None
            which will be converted to an empty string automatically).

    .. _PySeq: http://packages.python.org/pyseq/
    .. _PySeq Documentation: http://packages.python.org/pyseq/
    """

    __auto_name__ = True
    __tablename__ = "Files"
    __mapper_args__ = {"polymorphic_identity": "File"}

    file_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    # this is a limit for most
    original_filename: Mapped[Optional[str]] = mapped_column(String(256))
    # file systems
    full_path: Mapped[Optional[str]] = mapped_column(
        Text, doc="The full path of the url to the file."
    )

    created_with: Mapped[Optional[str]] = mapped_column(String(256))

    def __init__(
        self,
        full_path: Optional[str] = "",
        original_filename: Optional[str] = "",
        references: Optional[List["File"]] = None,
        created_with: Optional[str] = None,
        **kwargs: Optional[Dict[str, Any]],
    ) -> None:
        super(File, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, references=references)
        self.full_path = full_path
        self.original_filename = original_filename
        self.created_with = created_with

    @validates("full_path")
    def _validate_full_path(self, key: str, full_path: Union[None, str]) -> str:
        """Validate the given full_path value.

        Args:
            key (str): The name of the validated column.
            full_path (str): The full_path value to be validated.

        Raises:
            TypeError: If the given full_path is not a str.

        Returns:
            str: The validated full_path value.
        """
        if full_path is None:
            full_path = ""

        if not isinstance(full_path, str):
            raise TypeError(
                f"{self.__class__.__name__}.full_path should be a str, "
                f"not {full_path.__class__.__name__}: '{full_path}'"
            )

        return self._format_path(full_path)

    @validates("created_with")
    def _validate_created_with(
        self, key: str, created_with: Union[None, str]
    ) -> Union[None, str]:
        """Validate the given created_with value.

        Args:
            key (str): The name of the validated column.
            created_with (str): The name of the application used to create this
                File.

        Raises:
            TypeError: If the given created_with attribute is not None and not
                a string.

        Returns:
            Union[None, str]: The validated created with value.
        """
        if created_with is not None and not isinstance(created_with, str):
            raise TypeError(
                "{}.created_with should be an instance of str, not {}: '{}'".format(
                    self.__class__.__name__,
                    created_with.__class__.__name__,
                    created_with,
                )
            )
        return created_with

    @validates("original_filename")
    def _validate_original_filename(
        self, key: str, original_filename: Union[None, str]
    ) -> str:
        """Validate the given original_filename value.

        Args:
            key (str): The name of the validated column.
            original_filename (str): The original filename value to be validated.

        Raises:
            TypeError: If the given original_filename value is not a str.

        Returns:
            str: The validated original_filename value.
        """
        filename_from_path = os.path.basename(self.full_path)
        if original_filename is None:
            original_filename = filename_from_path

        if original_filename == "":
            original_filename = filename_from_path

        if not isinstance(original_filename, str):
            raise TypeError(
                f"{self.__class__.__name__}.original_filename should be a str, "
                f"not {original_filename.__class__.__name__}: '{original_filename}'"
            )

        return original_filename

    @staticmethod
    def _format_path(path: Union[bytes, str]) -> str:
        """Format the path to internal format.

        The path is using the Linux forward slashes for path separation.

        Args:
            path (Union[bytes, str]): The path value to be formatted.

        Returns:
            str: The formatted path value.
        """
        if isinstance(path, bytes):
            path = path.decode("utf-8")

        return path.replace("\\", "/")

    @property
    def path(self) -> str:
        """Return the path part of the full_path.

        Returns:
            str: The path part of the full_path value.
        """
        return os.path.split(self.full_path)[0]

    @path.setter
    def path(self, path: str) -> None:
        """Set the path part of the full_path attribute.

        Args:
            path (str): The new path value.

        Raises:
            TypeError: If the given path value is not a str.
            ValueError: If the given path is an empty str.
        """
        if path is None:
            raise TypeError(f"{self.__class__.__name__}.path cannot be set to None")

        if not isinstance(path, str):
            raise TypeError(
                f"{self.__class__.__name__}.path should be a str, "
                f"not {path.__class__.__name__}: '{path}'"
            )

        if path == "":
            raise ValueError(
                f"{self.__class__.__name__}.path cannot be an empty string"
            )

        self.full_path = self._format_path(os.path.join(path, self.filename))

    @property
    def filename(self) -> str:
        """Return the filename part of the full_path attribute.

        Returns:
            str: The filename part of the full_path attribute.
        """
        return os.path.split(self.full_path)[1]

    @filename.setter
    def filename(self, filename: Union[None, str]) -> None:
        """Set the filename part of the full_path attr.

        Args:
            filename (Union[None, str]): The new filename.

        Raises:
            TypeError: If the given filename is not a str.
        """
        if filename is None:
            filename = ""

        if not isinstance(filename, str):
            raise TypeError(
                f"{self.__class__.__name__}.filename should be a str, "
                f"not {filename.__class__.__name__}: '{filename}'"
            )

        self.full_path = self._format_path(os.path.join(self.path, filename))

    @property
    def extension(self) -> str:
        """Return the extension value.

        Returns:
            str: The extension extracted from the full_path value.
        """
        return os.path.splitext(self.full_path)[1]

    @extension.setter
    def extension(self, extension: Union[None, str]) -> None:
        """Set the extension value.

        Args:
            extension (Union[None, str]): The new extension value.

        Raises:
            TypeError: If the given extension value is not a str.
        """
        if extension is None:
            extension = ""

        if not isinstance(extension, str):
            raise TypeError(
                f"{self.__class__.__name__}.extension should be a str, "
                f"not {extension.__class__.__name__}: '{extension}'"
            )

        if extension != "":
            if not extension.startswith(os.path.extsep):
                extension = os.path.extsep + extension

        self.filename = os.path.splitext(self.filename)[0] + extension

    def walk_references(
        self,
        method: Union[int, str, TraversalDirection] = TraversalDirection.DepthFirst,
    ) -> Generator[None, "File", None]:
        """Walk the references of this file.

        Args:
            method (Union[int, str, TraversalDirection]): The walk method
                defined by the :class:`.TraversalDirection` enum.

        Yields:
            File: Yield the File instances.
        """
        for v in walk_hierarchy(self, "references", method=method):
            yield v

    def __eq__(self, other: Any) -> bool:
        """Check if the other is equal to this File.

        Args:
            other (Any): The other object to be checked for equality.

        Returns:
            bool: If the other object is a File instance and has the same
                full_path and type value.
        """
        return (
            super(File, self).__eq__(other)
            and isinstance(other, File)
            and self.full_path == other.full_path
            and self.type == other.type
        )

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(File, self).__hash__()
