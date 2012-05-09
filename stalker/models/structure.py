# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, validates
from stalker.db.declarative import Base
from stalker.models.entity import Entity

class Structure(Entity):
    """Holds data about how the physical files are arranged in the :class:`~stalker.core.models.Repository`.
    
    Structures are generally owned by :class:`~stalker.core.models.Project`
    objects. Whenever a :class:`~stalker.core.models.Project` is physicaly
    created, project folders are created by looking at
    :attr:`~stalker.core.models.Structure.custom_template` of the
    :class:`~stalker.core.models.Structure`, the
    :class:`~stalker.core.models.Project` object is generally given to the
    :class:`~stalker.core.models.Structure`. So it is possible to use a
    variable like "{{project}}" or derived variables like::
      
      {% for seq in project.sequences %}
          {{do something here}}
    
    :param templates: A list of
      :class:`~stalker.core.models.FilenameTemplate`\ s which
      defines a specific template for the given
      :attr:`~stalker.core.models.FilenameTemplate.target_entity_type`\ s.
    
    :type templates: list of :class:`~stalker.core.models.FilenameTemplate`\ s
    
    :param str custom_template: A string containing several lines of folder
      names. The folders are relative to the
      :class:`~stalker.core.models.Project` root. It can also contain a Jinja2
      Template code. Which will be rendered to show the list of folders to be
      created with the project. The Jinja2 Template is going to have the
      {{project}} variable. The important point to be careful about is to list
      all the custom folders of the project in a new line in this string. For
      example a :class:`~stalker.core.models.Structure` for a
      :class:`~stalker.core.models.Project` can have the following
      :attr:`~stalker.core.models.Structure.custom_template`::
        
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
            {{seq_root}}/Edit/AnimaticStoryboard
            {{seq_root}}/Edit/Export
            {{seq_root}}/Storyboard
            
            {% for shot in seq.shots %}
                {% set shot_root = seq_root + '/SHOTS/' + shot.code %}
                {{shot_root}}
                
                {% for task in shot.tasks %}
                    {% set task_root = shot_root + '/' + task.code %}
                    {{task_root}}
      
      The above example has gone far beyond deep than it is needed, where it
      started to define paths for :class:`~stalker.core.models.Asset`\ s. Even
      it is possible to create a :class:`~stalker.core.models.Project`
      structure like that, in general it is unnecessary. Because the above
      folders are going to be created but they are probably going to be empty
      for a while, because the :class:`~stalker.core.models.Asset`\ s are not
      created yet (or in fact no :class:`~stalker.core.models.Version`\ s are
      created for the :class:`~stalker.core.models.Task`\ s). Anyway, it is
      much suitable and desired to create this details by using
      :class:`~stalker.core.models.FilenameTemplate` objects. Which are
      specific to certain
      :attr:`~stalker.core.FilenameTemplate.target_entity_type`\ s. And by
      using the :attr:`~stalker.core.models.Structure.custom_template`
      attribute, Stalker can not place any source or output file of a
      :class:`~stalker.core.models.Version` in the
      :class:`~stalker.core.models.Repository` where as it can by using
      :class:`~stalker.core.models.FilenameTemplate`\ s.
      
      But for certain types of :class:`~stalker.core.models.Task`\ s it is may
      be good to previously create the folder structure just because in certain
      environments (programs) it is not possible to run a Python code that will
      place the file in to the Repository like in Photoshop.
      
      The ``custom_template`` parameter can be None or an empty string if it is
      not needed. Be careful not to pass a variable other than a string or
      unicode because it will use the string representation of the given
      variable.
    
    A :class:`~stalker.core.models.Structure` can not be created without a
    ``type`` (__strictly_typed__ = True). By giving a ``type`` to the
    :class:`~stalker.core.models.Structure`, you can create one structure for
    **Commercials** and another project structure for **Movies** and another
    one for **Print** projects etc. and can reuse them with new
    :class:`~stalker.core.models.Project`\ s.
    """



    #__strictly_typed__ = True

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

    custom_template = Column("custom_template", String)

    def __init__(self, templates=None, custom_template=None, **kwargs):
        super(Structure, self).__init__(**kwargs)

        if templates is None:
            templates = []

        self.templates = templates
        self.custom_template = custom_template

    def __eq__(self, other):
        """the equality operator
        """

        return super(Structure, self).__eq__(other) and\
               isinstance(other, Structure) and\
               self.templates == other.templates and\
               self.custom_template == other.custom_template

    @validates("custom_template")
    def _validate_custom_template(self, key, custom_template_in):
        """validates the given custom_template value
        """

        return custom_template_in

    @validates("templates")
    def _validate_templates(self, key, template_in):
        """validates the given template value
        """
        
        from stalker.models.templates import FilenameTemplate
        
        if not isinstance(template_in, FilenameTemplate):
            raise TypeError("all the elements in the %s.templates should be a "
                            "list of stalker.core.models.FilenameTemplate "
                            "instances not %s" %
                            (self.__class__.__name__,
                             template_in.__class__.__name__))

        return template_in

# STRUCTURE_FILENAMETEMPLATES
Structure_FilenameTemplates = Table(
    "Structure_FilenameTemplates", Base.metadata,
    Column("structure_id", Integer, ForeignKey("Structures.id"),
           primary_key=True),
    Column("filenametemplate_id", Integer, ForeignKey("FilenameTemplates.id"),
           primary_key=True)
)

