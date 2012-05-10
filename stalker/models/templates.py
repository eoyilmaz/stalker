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
    
    :param str path_code: A `Jinja2`_ template code which specifies the path of
      the given item. It is relative to the project root. A typical example
      could be::
        
        asset_path_code = "ASSETS/{{asset.code}}/{{task.code}}/"
    
    :param str file_code: A `Jinja2`_ template code which specifies the file
      name of the given item. It is relative to the
      :attr:`~stalker.models.templates.FilenameTemplate.path_code`. A typical
      example could be::
        
        asset_file_code = "{{asset.code}}_{{version.take}}_{{task.code}}_"\\
                          "{{version.version}}_{{user.initials}}"
      
      Could be set to an empty string or None, the default value is None.
    
    :param str output_path_code: A Jinja2 template code specifying where to
      place the outputs of the applied
      :attr:`~stalker.models.templates.FilenameTemplate.target_entity_type`. If
      it is empty and the
      :attr:`~stalker.models.templates.FilenameTemplate.output_is_relative` is
      True, then the outputs will naturally be in the same place with the
      :attr:`~stalker.models.templates.FilenameTemplate.path_code`. If the
      :attr:`~stalker.models.templates.FilenameTemplate.output_is_relative` is
      False then
      :attr:`~stalker.models.templates.FilenameTemplate.output_path_code` will
      be the same code with
      :attr:`~stalker.models.templates.FilenameTemplate.path_code`.
      
      It can be None, or an empty string, or it can be skipped.
    
    :param str output_file_code: A Jinja2 template code specifying what will be
      the file name of the output. If it is skipped or given as None or as an
      empty string, it will be the same with the
      :attr:`~stalker.models.templates.FilenameTemplate.file_code`.
      
      It can be skipped, or can be set to None or an empty string. The default
      value is None, and this will set the
      :attr:`~stalker.models.templates.FilenameTemplate.output_file_code` to
      the same value with
      :attr:`~stalker.models.templates.FilenameTemplate.file_code`.
    
    :param bool output_is_relative: A bool value specifying if the
      :attr:`~stalker.models.templates.FilenameTemplate.output_path_code` is
      relative to the
      :attr:`~stalker.models.templates.FilenameTemplate.path_code`. The default
      value is True. Can be skipped, any other than a bool value will be
      evaluated to a bool value.
    
    Examples:
    
    A template for asset versions can be used like this::
      
      from stalker import Type, FilenameTemplate, TaskTemplate
      
      # create a couple of variables
      path_code = "ASSETS/{{asset_type.name}}/{{task_type.code}}"
      
      file_code =
      "{{asset.name}}_{{take.name}}_{{asset_type.name}}_v{{version.version_number}}"
      
      output_path_code = "OUTPUT"
      output_file_code = file_code
      
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
          description="this is the template which explains how to place \
Character assets",
          target_entity_type="Asset",
          path_code=path_code,
          file_code=file_code,
          output_path_code=output_path_code,
          output_file_code=output_file_code,
          output_is_relative=True,
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
    
      |- M:\\\PROJECTS  --> {{repository.path}}
       |- PRENSESIN_UYKUSU  --> {{project.code}}
        |- ASSETS  --> "ASSETS"
         |- Character  --> {{asset_type.name}}
          |- Olum  --> {{asset.name}}
           |- MODEL  --> {{task_type.code}}
            |- Olum_MAIN_MODEL_v001.ma --> {{asset.name}}_\
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
    
    path_code = Column(
        String,
        doc="""The templating code for the path of this FilenameTemplate."""
    )

    file_code = Column(
        String,
        doc="""The templating code for the file part of the FilenameTemplate."""
    )
    
    # TODO: Remove the 'output is relative' attribute
    
    output_path_code = Column(
        String,
        doc="""The output_path_code of this FilenameTemplate object.
        
        Should be a unicode string. None and empty string is also accepted, but
        in this case the value is copied from the
        :attr:`~stalker.models.templates.FilenameTemplate.path_code` if also
        the
        :attr:`~stalker.models.templates.FilenameTemplate.output_is_relative`
        is False. If
        :attr:`~stalker.models.templates.FilenameTemplate.output_is_relative`
        is True then it will left as an empty string.
        """
    )

    output_file_code = Column(
        String,
        doc="""The output_file_code of this FilenameTemplate object.
        
        Should be a unicode string. None and empty string is also accepted, but
        in this case the value is copied from the
        :attr:`~stalker.models.templates.FilenameTemplate.file_code` if also
        the
        :attr:`~stalker.models.templates.FilenameTemplate.output_is_relative`
        is False. If
        :attr:`~stalker.models.templates.FilenameTemplate.output_is_relative`
        is True then it will left as an empty string.
        """
    )

    output_is_relative = Column(
        Boolean,
        doc="""Specifies if the output should be calculated relative to the path attribute.
        """
    )

    def __init__(self,
#                 target_entity_type=None,
                 path_code=None,
                 file_code=None,
                 output_path_code=None,
                 output_file_code=None,
                 output_is_relative=True,
                 **kwargs):
        super(FilenameTemplate, self).__init__(**kwargs)
        TargetEntityTypeMixin.__init__(self, **kwargs)
#        self._target_entity_type =\
#        self._validate_target_entity_type(target_entity_type)
        self.path_code = path_code
        self.file_code = file_code
        self.output_is_relative = output_is_relative
        self.output_path_code = output_path_code
        self.output_file_code = output_file_code

    @validates("path_code")
    def _validate_path_code(self, key, path_code_in):
        """validates the given path_code attribute for several conditions
        """

        # check if it is None
        if path_code_in is None:
            path_code_in = u""

        path_code_in = unicode(path_code_in)

        return path_code_in

    @validates("file_code")
    def _validate_file_code(self, key, file_code_in):
        """validates the given file_code attribute for several conditions
        """

        # check if it is None
        if file_code_in is None:
            file_code_in = u""

        # convert it to unicode
        file_code_in = unicode(file_code_in)

        return file_code_in

    @validates("output_path_code")
    def _validate_output_path_code(self, key, output_path_code_in):
        """validates the given output_path_code value
        """

        if output_path_code_in == None or output_path_code_in == "":
            if self.output_is_relative:
                output_path_code_in = ""
            else:
                output_path_code_in = self.path_code

        return output_path_code_in

    @validates("output_file_code")
    def _validate_output_file_code(self, key, output_file_code_in):
        """validates the given output_file_code value
        """

        if output_file_code_in == None or output_file_code_in == "":
            if self.output_is_relative:
                output_file_code_in = ""
            else:
                output_file_code_in = self.file_code

        return output_file_code_in

    @validates("output_is_relative")
    def _validate_output_is_relative(self, key, output_is_relative_in):
        """validates the given output_is_relative value
        """

        return bool(output_is_relative_in)

#    def _validate_target_entity_type(self, target_entity_type_in):
#        """validates the given target_entity_type attribute for several
#        conditions
#        """
#
#        # check if it is None
#        if target_entity_type_in is None:
#            raise TypeError("target_entity_type can not be None")
#
#        if isinstance(target_entity_type_in, type):
#            target_entity_type_in = target_entity_type_in.__name__
#
#        return target_entity_type_in

#    @synonym_for("_target_entity_type")
#    @property
#    def target_entity_type(self):
#        """The target entity type this FilenameTemplate object should work on.
#        
#        Should be a string value or the class itself
#        """
#
#        return self._target_entity_type

    def __eq__(self, other):
        """checks the equality of the given object to this one
        """

        return super(FilenameTemplate, self).__eq__(other) and\
               isinstance(other, FilenameTemplate) and\
               self.target_entity_type == other.target_entity_type and\
               self.path_code == other.path_code and\
               self.file_code == other.file_code and\
               self.output_path_code == other.output_path_code and\
               self.output_file_code == other.output_file_code
