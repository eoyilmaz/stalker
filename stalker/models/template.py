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

from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import validates
from stalker.models.entity import Entity
from stalker.models.mixins import TargetEntityTypeMixin

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


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

        # this is going to be used by Stalker to decide the :stalker:`.Link`
        # :stalker:`.Link.filename` and :stalker:`.Link.path` (which is the way
        # Stalker links external files to Version instances)
        f1 = FilenameTemplate(
            name="Asset Version Template",
            target_entity_type="Asset",
            target_entity_type="Asset",
            path="{{project.code}}/Assets/{{asset.type.code}}/{{asset.code}}/{{task.type.code}}",
            filename="{{asset.code}}_{{version.take_name}}_{{task.type.code}}_v{{'%03d'|version.version_number}}{{link.extension}}"
        )

        s1.templates.append(f1)
        p1.structure = s1

        # now because we have defined a FilenameTemplate for Assets,
        # Stalker is now able to produce a path and a filename for any Version
        # related to this asset.

    :param str target_entity_type: The class name that this FilenameTemplate
      is designed for. You can also pass the class itself. So both of the
      examples below can work::

        new_filename_template1 = FilenameTemplate(target_entity_type="Asset")
        new_filename_template2 = FilenameTemplate(target_entity_type=Asset)

      A TypeError will be raised when it is skipped or it is None and a
      ValueError will be raised when it is given as and empty string.

    :param str path: A `Jinja2`_ template code which specifies the path of the
      given item. It is relative to the repository root. A typical example
      could be::

        asset_path = "{{project.code}}/ASSETS/{{asset.code}}/{{task.code}}/"

    :param str filename: A `Jinja2`_ template code which specifies the file
      name of the given item. It is relative to the
      :attr:`.FilenameTemplate.path`. A typical example could be::

        asset_filename = "{{asset.code}}_{{version.take}}_{{task.code}}_v"{{'%03d'|format(version.version)}}{{version.extension}}"

      Could be set to an empty string or None, the default value is None.

      It can be None, or an empty string, or it can be skipped.

    .. _Jinja2: http://jinja.pocoo.org/docs/
    """
    __auto_name__ = False
    __strictly_typed__ = False
    __tablename__ = "FilenameTemplates"
    __mapper_args__ = {"polymorphic_identity": "FilenameTemplate"}
    filenameTemplate_id = Column("id", Integer, ForeignKey("Entities.id"),
                                 primary_key=True)

    path = Column(
        Text,
        doc="""The template code for the path of this FilenameTemplate."""
    )

    filename = Column(
        Text,
        doc="""The template code for the file part of the FilenameTemplate."""
    )

    def __init__(self,
                 target_entity_type=None,
                 path=None,
                 filename=None,
                 **kwargs):
        super(FilenameTemplate, self).__init__(**kwargs)
        TargetEntityTypeMixin.__init__(self, target_entity_type, **kwargs)
        self.path = path
        self.filename = filename

    @validates("path")
    def _validate_path(self, key, path_in):
        """validates the given path attribute for several conditions
        """
        # check if it is None
        if path_in is None:
            path_in = ""

        from stalker import __string_types__
        if not isinstance(path_in, __string_types__):
            raise TypeError(
                "%s.path attribute should be string not %s" %
                (self.__class__.__name__, path_in.__class__.__name__)
            )

        return path_in

    @validates("filename")
    def _validate_filename(self, key, filename_in):
        """validates the given filename attribute for several conditions
        """
        # check if it is None
        if filename_in is None:
            filename_in = ""

        from stalker import __string_types__
        if not isinstance(filename_in, __string_types__):
            raise TypeError(
                "%s.filename attribute should be string not %s" %
                (self.__class__.__name__, filename_in.__class__.__name__)
            )

        return filename_in

    def __eq__(self, other):
        """checks the equality of the given object to this one
        """
        return super(FilenameTemplate, self).__eq__(other) and \
            isinstance(other, FilenameTemplate) and \
            self.target_entity_type == other.target_entity_type and \
            self.path == other.path and \
            self.filename == other.filename

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(FilenameTemplate, self).__hash__()
