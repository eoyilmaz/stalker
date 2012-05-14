# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import validates
from stalker.models.entity import Entity
from stalker.models.mixins import TargetEntityTypeMixin

class FilenameTemplate(Entity, TargetEntityTypeMixin):
    """Holds templates for filename conventions.
    
    FilenameTemplate objects help to specify where to place a file related to
    its :attr:`~stalker.models.templates.FilenameTemplate.target_entity_type`.
    
    The first very important usage of FilenameTemplates is to place asset file
    :class:`~stalker.models.version.Version`'s to proper places inside a
    :class:`~stalker.models.project.Project`'s
    :class:`~stalker.models.structure.Structure`.
    
    Secondly, it can be used in the process of injecting files in to the
    repository. By creating templates for :class:`~stalker.models.link.Link`.
    
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
        :attr:`~stalker.models.templates.FilenameTemplate.path`. A typical
        example could be::
        
            asset_filename = "{{asset.code}}_{{version.take}}_{{task.code}}_"\\
                             "{{version.version}}_{{user.initials}}"
      
        Could be set to an empty string or None, the default value is None.
    
    :param str output_path: A Jinja2 template code specifying where to
        place the outputs of the applied
        :attr:`~stalker.models.templates.FilenameTemplate.target_entity_type`.
     
        It can be None, or an empty string, or it can be skipped.
    
    Examples:
    
    A template for asset versions can be used like this::
        
        from stalker import Type, FilenameTemplate, TaskTemplate
         
        # create a couple of variables
        path = "{{project.code}}/Assets/{{asset_type.name}}/{{task_type.code}}"
        
        filename = "{{asset.name}}_{{take.name}}_{{asset_type.name}}_v{{version.version_number}}"
        
        output_path = "{{version.path}}/Outputs"
        
        # create a type for modeling task
        modeling = Type(
            name="Modeling",
            code="MODEL",
            description="The modeling step of the asset",
            target_entity_type=Task
        )
        
        # create a "Character" Type for Asset classes
        character = Type(
            name="Character",
            description="this is the character asset type",
            target_entity_type=Asset
        )
        
        # now create our FilenameTemplate
        char_template = FilenameTemplate(
            name="Character",
            description="this is the template which explains how to place Character assets",
            target_entity_type="Asset",
            path=path,
            filename=filename,
            output_path=output_path,
        )
        
        # assign this type template to the structure of the project with id=101
        myProject = query(Project).filter_by(id=101).first()
      
        # append the type template to the structures' templates
        myProject.structure.templates.append(char_template)
      
        # commit everything to the database
        session.commit()
    
    Now with the code above, whenever a new
    :class:`~stalker.models.version.Version` created for a **Character**
    asset, Stalker will automatically place the related file to a certain
    folder and with a certain file name defined by the template. For example
    the above template should render something like below for Windows::
    
      |- M:/PROJECTS  --> {{repository.path}}
       |- PRENSESIN_UYKUSU  --> {{project.code}}
        |- ASSETS  --> "ASSETS"
         |- Character  --> {{asset_type.name}}
          |- Olum  --> {{asset.name}}
           |- MODEL  --> {{task_type.code}}
            |- Olum_MAIN_MODEL_v001.ma --> {{asset.name}}_/
{{take.name}}_{{asset_type.name}}_v{{version.version_number}}
    
    And one of the best side is you can create a version from Linux, Windows or
    OSX all the paths will be correctly handled by Stalker.
    
    .. _Jinja2: http://jinja.pocoo.org/docs/
    """

    __tablename__ = "FilenameTemplates"
    __mapper_args__ = {"polymorphic_identity": "FilenameTemplate"}
    filenameTemplate_id = Column("id", Integer, ForeignKey("Entities.id"),
                                 primary_key=True)
#    _target_entity_type = Column("target_entity_type", String)
    
    path = Column(
        String,
        doc="""The template code for the path of this FilenameTemplate."""
    )

    filename = Column(
        String,
        doc="""The template code for the file part of the FilenameTemplate."""
    )
    
    output_path = Column(
        String,
        doc="""The output_path of this FilenameTemplate object.
        
        Should be a unicode string. None and empty string is also accepted.
        """
    )
    
    def __init__(self,
                 target_entity_type=None,
                 path=None,
                 filename=None,
                 output_path=None,
                 **kwargs):
        super(FilenameTemplate, self).__init__(**kwargs)
        TargetEntityTypeMixin.__init__(self, target_entity_type, **kwargs)
        self.path = path
        self.filename = filename
        self.output_path = output_path
    
    @validates("path")
    def _validate_path(self, key, path_in):
        """validates the given path attribute for several conditions
        """
        # check if it is None
        if path_in is None:
            path_in = u""

        path_in = unicode(path_in)

        return path_in
    
    @validates("filename")
    def _validate_filename(self, key, filename_in):
        """validates the given filename attribute for several conditions
        """
        # check if it is None
        if filename_in is None:
            filename_in = u""
        
        # convert it to unicode
        filename_in = unicode(filename_in)
        
        return filename_in
    
    @validates("output_path")
    def _validate_output_path(self, key, output_path_in):
        """validates the given output_path value
        """
        if output_path_in is None:
            output_path_in = ""
        
        return output_path_in
    
    def __eq__(self, other):
        """checks the equality of the given object to this one
        """
        return super(FilenameTemplate, self).__eq__(other) and\
               isinstance(other, FilenameTemplate) and\
               self.target_entity_type == other.target_entity_type and\
               self.path == other.path and\
               self.filename == other.filename and\
               self.output_path == other.output_path
