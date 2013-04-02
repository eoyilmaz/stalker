# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import validates
from stalker.models.entity import Entity
from stalker.models.mixins import TargetEntityTypeMixin

from stalker.log import logging_level
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

class FilenameTemplate(Entity, TargetEntityTypeMixin):
    """Holds templates for filename conventions.
    
    FilenameTemplate objects help to specify where to place a file related to
    its :attr:`~stalker.models.template.FilenameTemplate.target_entity_type`
    and :attr:`~stalker.models.template.FilenameTemplate.type`.
    
    Because the ``type`` attribute is used to define the correct
    FilenameTemplate in a :class:`~stalker.models.structure.Structure`, the
    FilenameTemplate class is `strictly typed`. This means you can not define
    a FilenameTemplate instance without assigning a
    :class:`~stalker.models.type.Type` instance to it.
    
    For now there are two possible values for the type attribute:
      
      * A :class:`~stalker.models.type.Type` with the ``name`` attribute is set
        to "Version". This type of FilenameTemplates are used to specify where
        to place :class:`~staler.models.version.Version` source files.
        
      * A :class:`~stalker.models.type.Type` with the ``name`` attribute is set
        to "Reference". This type of FilenameTemplates are used to specify
        where to place reference files in to the Project structure.
    
    Here is a nice example to how to create a FilenameTemplate for Asset
    Versions and References::
      
      # first get the Types
      vers_type = Type.query\
                  .filter_by(target_entity_type="FilenameTemplate")\
                  .filter_by(type="Version")\
                  .first()
      
      ref_type = Type.query\
                 .filter_by(target_entity_type="FilenameTemplate")\
                 .filter_by(type="Reference")\
                 .first()
      
      # lets create a FilenameTemplate for placing Asset Version files.
      f_ver = FilenameTemplate(
          target_entity_type="Asset",
          type=vers_type,
          path="Assets/{{asset.type.code}}/{{asset.code}}/{{task.type.code}}",
          filename="{{asset.code}}_{{version.take_name}}_{{task.type.code}}_v{{'%03d'|version.version_number}}{{link.extension}}"
          custom_path="{{version.path}}/Outputs/{{version.take_name}}"
      )
      
      # and now define a FilenameTemplate for placing Asset Reference files.
      # no need to have a custom_path here...
      f_ref = FilenameTemplate(
          target_entity_type="Asset",
          type=ref_type,
          path="Assets/{{asset.type.code}}/{{asset.code}}/References",
          filename="{{link.type.code}}/{{link.id}}{{link.extension}}"
      )
    
    The first very important usage of FilenameTemplates is to place
    :class:`~stalker.models.version.Version` related files to proper places
    inside a :class:`~stalker.models.project.Project`'s
    :attr:`~stalker.models.project.Project.structure`.
    
    The :attr:`~stalker.models.template.FilenameTemplate.type` attribute of
    the FilenameTemplate class (which is derived from
    :class:`stalker.models.entity.SimpleEntity` is used to determine which
    template is going to be used in a :class:`~stalker.models.project.Project`.
    
    Let say we have a :class:`~stalker.models.project.Project` and in its
    :attr:`~stalker.models.project.Project.structure` attribute a
    :class:`~stalker.models.structure.Structure` is attached where::
        
        p1 = Project(name="Test Project")
        s1 = Structure(name="Commercial Project Structure")
        
        t1 = Type(
            name="Version",
            target_entity_type="FilenameTemplate"
        )
        
        # this is going to be used by Stalker to decide the
        # :stalker:`~stalker.models.link.Link`
        # :stalker:`~stalker.models.link.Link.filename` and
        # :stalker:`~stalker.models.link.Link.path` (which is the way Stalker
        # links external files to Version instances)
        f1 = FilenameTemplate(
            name="Asset Version",
            target_entity_type="Asset",
            type=t1,
            path_code="{{project.code}}/Assets/{{asset.type.name}}/{{task.type.name}}",
            filename_code="{{taskable.code}}_{{version.take}}_{{task.type.name}}_v{{'%03d'|version.version_number}}{{link.extension}}",
            custom_path="use if needed for outputs from the version (renders, exports, etc)"
        )
        
        # now because we have defined a FilenameTemplate for Asset Versions,
        # Stalker is now able to produce a path and a filename for you.
        
        
    
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
      :attr:`~stalker.models.template.FilenameTemplate.path`. A typical
      example could be::
        
        asset_filename = "{{asset.code}}_{{version.take}}_{{task.code}}_v"{{'%03d'|format(version.version)}}{{version.extension}}"
      
      Could be set to an empty string or None, the default value is None.
      
      It can be None, or an empty string, or it can be skipped.
    
    Examples:
    
    A template for asset versions can be used like this::
      
      from stalker import Type, FilenameTemplate, TaskTemplate
       
      # create a couple of variables
      path = "{{project.code}}/Assets/{{asset.code}}/{{task.type.name}}"
      
      filename = "{{asset.name}}_{{take.name}}_{{asset_type.name}}_v{{version.version_number}}"
      
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
            |- Olum_MAIN_MODEL_v001.ma --> {{asset.name}}_{{take.name}}_{{asset_type.name}}_v{{version.version_number}}
    
    And one of the best side is you can create a version from Linux, Windows or
    OSX all the paths will be correctly handled by Stalker.
    
    .. _Jinja2: http://jinja.pocoo.org/docs/
    """
    __auto_name__ = False
    __strictly_typed__ = True
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
        
        if not isinstance(path_in, (str, unicode)):
            raise TypeError("%s.path attribute should be string or unicode "
                            "not %s" % (self.__class__.__name__,
                                        path_in.__class__.__name__))
        
        return path_in
    
    @validates("filename")
    def _validate_filename(self, key, filename_in):
        """validates the given filename attribute for several conditions
        """
        # check if it is None
        if filename_in is None:
            filename_in = ""
        
        if not isinstance(filename_in, (str, unicode)):
            raise TypeError("%s.filename attribute should be string or "
                            "unicode not %s" % (self.__class__.__name__,
                                                filename_in.__class__.__name__))
        
        return filename_in
    
    def __eq__(self, other):
        """checks the equality of the given object to this one
        """
        return super(FilenameTemplate, self).__eq__(other) and\
               isinstance(other, FilenameTemplate) and\
               self.target_entity_type == other.target_entity_type and\
               self.path == other.path and\
               self.filename == other.filename
