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

import os
import logging

from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import validates

from stalker.models.entity import Entity
from stalker.log import logging_level

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Link(Entity):
    """Holds data about external links.

    Links are all about giving some external information to the current entity
    (external to the database, so it can be something on the
    :class:`.Repository` or in the Web or anywhere that the server can reach).
    The type of the link (general, file, folder, web page, image, image
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
      It is the path part of the full_path

    Filename
      It is the filename part of the full_path, also includes the extension,
      so changing the filename also changes the extension part.

    Extension
      It is the extension part of the full_path. It also includes the extension
      separator ('.' for most of the file systems).

    :param full_path: The full path to the link, it can be a path to a folder
      or a file in the file system, or a web page. For file sequences use
      "%h%p%t %R" format, for more information see `PySeq Documentation`_.
      It can be set to empty string (or None which will be converted to an
      empty string automatically).

    .. _PySeq: http://packages.python.org/pyseq/
    .. _PySeq Documentation: http://packages.python.org/pyseq/

    """
    __auto_name__ = True
    __tablename__ = "Links"
    __mapper_args__ = {"polymorphic_identity": "Link"}

    link_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    original_filename = Column(String(256))  # this is a limit for most
                                             # filesystems
    full_path = Column(
        Text,
        doc="""The full path of the url to the link."""
    )

    def __init__(self, full_path='', original_filename='', **kwargs):
        super(Link, self).__init__(**kwargs)
        self.full_path = full_path
        self.original_filename = original_filename

    @validates('full_path')
    def _validate_full_path(self, key, full_path):
        """validates the given full_path value
        """
        if full_path is None:
            full_path = ''

        from stalker import __string_types__
        if not isinstance(full_path, __string_types__):
            raise TypeError(
                "%s.full_path should be an instance of string not %s" %
                (self.__class__.__name__, full_path.__class__.__name__)
            )

        return self._format_path(full_path)

    @validates('original_filename')
    def _validate_original_filename(self, key, original_filename):
        """validates the given original_filename value
        """
        filename_from_path = os.path.basename(self.full_path)
        if original_filename is None:
            original_filename = filename_from_path

        if original_filename == '':
            original_filename = filename_from_path

        from stalker import __string_types__
        if not isinstance(original_filename, __string_types__):
            raise TypeError(
                '%s.original_filename should be an instance of str and not '
                '%s' % (
                    self.__class__.__name__,
                    original_filename.__class__.__name__
                )
            )

        return original_filename

    @staticmethod
    def _format_path(path):
        """formats the path to internal format, which is Linux forward slashes
        for path separation
        """
        from stalker import __string_types__
        if not isinstance(path, __string_types__):
            path = path.encode('utf-8')

        return path.replace("\\", "/")

    @property
    def path(self):
        """the path property
        """
        return os.path.split(self.full_path)[0]

    @path.setter
    def path(self, path):
        """setter for the path

        :param str path: the new path
        """
        if path is None:
            raise TypeError(
                '%s.path can not be set to None' % self.__class__.__name__
            )

        from stalker import __string_types__
        if not isinstance(path, __string_types__):
            raise TypeError(
                '%s.path should be an instance of str, not %s' %
                (self.__class__.__name__, path.__class__.__name__)
            )

        if path == '':
            raise ValueError(
                '%s.path can not be an empty string' % self.__class__.__name__
            )

        self.full_path = self._format_path(
            os.path.join(path, self.filename)
        )

    @property
    def filename(self):
        """the filename property
        """
        return os.path.split(self.full_path)[1]

    @filename.setter
    def filename(self, filename):
        """filename setter

        :param str filename: the new filename
        """
        if filename is None:
            filename = ''

        from stalker import __string_types__
        if not isinstance(filename, __string_types__):
            raise TypeError(
                '%s.filename should be an instance of str, not %s' %
                (self.__class__.__name__, filename.__class__.__name__)
            )

        self.full_path = self._format_path(
            os.path.join(self.path, filename)
        )

    @property
    def extension(self):
        """the extension property
        """
        return os.path.splitext(self.full_path)[1]

    @extension.setter
    def extension(self, extension):
        """extension setter

        :param extension: the new extension
        """
        if extension is None:
            extension = ''

        from stalker import __string_types__
        if not isinstance(extension, __string_types__):
            raise TypeError(
                '%s.extension should be an instance of str, not %s' % (
                    self.__class__.__name__,
                    extension.__class__.__name__
                )
            )

        if extension != '':
            if not extension.startswith(os.path.extsep):
                extension = os.path.extsep + extension

        self.filename = os.path.splitext(self.filename)[0] + extension

    def __eq__(self, other):
        """the equality operator
        """
        return super(Link, self).__eq__(other) and \
            isinstance(other, Link) and \
            self.full_path == other.full_path and \
            self.type == other.type

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Link, self).__hash__()
