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

from sqlalchemy import Table, Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, validates

from stalker.db.declarative import Base
from stalker.models.entity import Entity

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Structure(Entity):
    """Defines folder structures for :class:`.Projects`.

    Structures are generally owned by :class:`.Project` objects. Whenever a
    :class:`.Project` is physically created, project folders are created by
    looking at :attr:`.Structure.custom_template` of the :class:`.Structure`,
    the :class:`.Project` object is generally given to the :class:`.Structure`.
    So it is possible to use a variable like "{{project}}" or derived variables
    like::

      {% for seq in project.sequences %}
          {{do something here}}

    Every line of this rendered template will represent a folder and Stalker
    will create these folders on the attached :class:`.Repository`.

    :param templates: A list of :class:`.FilenameTemplate`\ s which defines a
      specific template for the given
      :attr:`.FilenameTemplate.target_entity_type`\ s.

    :type templates: list of :class:`.FilenameTemplate`\ s

    :param str custom_template: A string containing several lines of folder
      names. The folders are relative to the :class:`.Project` root. It can
      also contain a Jinja2 Template code. Which will be rendered to show the
      list of folders to be created with the project. The Jinja2 Template is
      going to have the {{project}} variable. The important point to be careful
      about is to list all the custom folders of the project in a new line in
      this string. For example a :class:`.Structure` for a :class:`.Project`
      can have the following :attr:`.Structure.custom_template`::

        ASSETS
        {% for asset in project.assets %}
            {% set asset_root = 'ASSETS/' + asset.code %}
            {{asset_root}}

            {% for task in asset.tasks %}
                {% set task_root = asset_root + '/' + task.code %}
                {{task_root}}

        SEQUENCES
        {% for seq in project.sequences %}}
            {% set seq_root = 'SEQUENCES/' + {{seq.code}} %}
            {{seq_root}}/Edit
            {{seq_root}}/Edit/Export
            {{seq_root}}/Storyboard

            {% for shot in seq.shots %}
                {% set shot_root = seq_root + '/SHOTS/' + shot.code %}
                {{shot_root}}

                {% for task in shot.tasks %}
                    {% set task_root = shot_root + '/' + task.code %}
                    {{task_root}}

      The above example has gone far beyond deep than it is needed, where it
      started to define paths for :class:`.Asset`\ s. Even it is possible to
      create a :class:`.Project` structure like that, in general it is
      unnecessary. Because the above folders are going to be created but they
      are probably going to be empty for a while, because the
      :class:`.Asset`\ s are not created yet (or in fact no
      :class:`.Version`\ s are created for the :class:`.Task`\ s). Anyway, it
      is much suitable and desired to create this details by using
      :class:`.FilenameTemplate` objects. Which are specific to certain
      :attr:`.FilenameTemplate.target_entity_type`\ s. And by using the
      :attr:`.Structure.custom_template` attribute, Stalker can not place any
      source or output file of a :class:`.Version` in the :class:`.Repository`
      where as it can by using :class:`.FilenameTemplate`\ s.

      But for certain types of :class:`.Task`\ s it is may be good to
      previously create the folder structure just because in certain
      environments (programs) it is not possible to run a Python code that will
      place the file in to the Repository like in Photoshop.

      The ``custom_template`` parameter can be None or an empty string if it is
      not needed.

    A :class:`.Structure` can not be created without a ``type``
    (__strictly_typed__ = True). By giving a ``type`` to the
    :class:`.Structure`, you can create one structure for **Commercials** and
    another project structure for **Movies** and another one for **Print**
    projects etc. and can reuse them with new :class:`.Project`\ s.
    """

    #__strictly_typed__ = True
    __auto_name__ = False
    __tablename__ = "Structures"
    __mapper_args__ = {"polymorphic_identity": "Structure"}

    structure_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    templates = relationship(
        "FilenameTemplate",
        secondary="Structure_FilenameTemplates"
    )

    custom_template = Column("custom_template", Text)

    def __init__(self, templates=None, custom_template=None, **kwargs):
        super(Structure, self).__init__(**kwargs)

        if templates is None:
            templates = []

        self.templates = templates
        self.custom_template = custom_template

    def __eq__(self, other):
        """the equality operator
        """
        return super(Structure, self).__eq__(other) and \
            isinstance(other, Structure) and \
            self.templates == other.templates and \
            self.custom_template == other.custom_template

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Structure, self).__hash__()

    @validates("custom_template")
    def _validate_custom_template(self, key, custom_template_in):
        """validates the given custom_template value
        """
        if custom_template_in is None:
            custom_template_in = ""

        from stalker import __string_types__
        if not isinstance(custom_template_in, __string_types__):
            raise TypeError(
                "%s.custom_template should be a string not %s" %
                (
                    self.__class__.__name__,
                    custom_template_in.__class__.__name__
                )
            )
        return custom_template_in

    @validates("templates")
    def _validate_templates(self, key, template_in):
        """validates the given template value
        """

        from stalker.models.template import FilenameTemplate

        if not isinstance(template_in, FilenameTemplate):
            raise TypeError(
                "All the elements in the %s.templates should be a list of "
                "stalker.models.template.FilenameTemplate instances not %s" %
                (self.__class__.__name__, template_in.__class__.__name__)
            )

        return template_in

# Structure_FilenameTemplates Table
Structure_FilenameTemplates = Table(
    "Structure_FilenameTemplates", Base.metadata,
    Column("structure_id", Integer, ForeignKey("Structures.id"),
           primary_key=True),
    Column("filenametemplate_id", Integer, ForeignKey("FilenameTemplates.id"),
           primary_key=True)
)
