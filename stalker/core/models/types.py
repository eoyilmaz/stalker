#-*- coding: utf-8 -*-



from stalker.core.models import entity, pipelineStep
from stalker.ext.validatedList import ValidatedList






########################################################################
class AssetType(entity.TypeEntity):
    """Holds the information about the asset types.
    
    One AssetType object has information about the pipeline steps that this
    type of asset has.
    
    So for example one can create a "Chracter" AssetType and then link
    "Design", "Modeling", "Rig", "Shading"
    :class:`~stalker.core.model.pipelineStep.PipelineStep`\ s to this AssetType
    object. And then have an "Environment" AssetType and then just link
    "Design", "Modeling", "Shading"
    :class:`~stalker.core.model.pipelineStep.PipelineStep`\ s to it.
    
    :param steps: This is a list of
      :class:`~stalker.core.model.pipelineStep.PipelineStep` objects.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, steps=[], **kwargs):
        super(AssetType, self).__init__(**kwargs)
        
        self._steps = self._validate_steps(steps)
    
    
    
    #----------------------------------------------------------------------
    def _validate_steps(self, steps_in):
        """validates the given steps list
        """
        
        # raise a Value error if it is not a list
        if not isinstance(steps_in, list):
            raise ValueError("steps should be an instance of list")
        
        # raise a Value error if not all of the elements are pipelineStep
        # objects
        if not all([ isinstance(obj, pipelineStep.PipelineStep)
                 for obj in steps_in]):
            raise ValueError(
                "all of the elements of the given list should be instance of "
                "stalker.pipelineStep.PipelineStep class"
            )
        
        return ValidatedList(steps_in)
    
    
    
    #----------------------------------------------------------------------
    def steps():
        
        def fget(self):
            return self._steps
        
        def fset(self, steps_in):
            self._steps = self._validate_steps(steps_in)
        
        doc = """this is the property that lets you set and get steps attribute
        """
        
        return locals()
    
    steps = property(**steps())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(AssetType, self).__eq__(other) and \
               isinstance(other, AssetType) and \
               self.steps == other.steps






########################################################################
class LinkType(entity.TypeEntity):
    """The type of :class:`~stalker.core.models.link.Link` is hold in LinkType
    objects.
    
    LinkType objects hold the type of the link and it is generaly
    used by :class:`~stalker.core.models.project.Project` to sort things out.
    See :class:`~stalker.core.models.project.Project` object documentation for
    details.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(LinkType, self).__init__(**kwargs)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(LinkType, self).__eq__(other) and \
               isinstance(other, LinkType)






########################################################################
class ProjectType(entity.TypeEntity):
    """Helps to create different type of :class:`~stalker.core.models.project.Project` objects.
    
    Can be used to create different type projects like Commercial, Movie, Still
    etc.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(ProjectType, self).__init__(**kwargs)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(ProjectType, self).__eq__(other) and \
               isinstance(other, ProjectType)
        







########################################################################
class TypeTemplate(entity.Entity):
    """The TypeTemplate model holds templates for Types.
    
    TypeTemplate objects help to specify where to place a file related to
    :class:`~stalker.core.models.entity.TypeEntity` objects and its derived
    classes.
    
    The first very important usage of TypeTemplates is to place asset
    :class:`~stalker.core.models.version.Version`'s to proper places inside a
    :class:`~stalker.core.models.project.Project`'s
    :class:`~stalker.core.models.structure.Structure`.
    
    :param path_code: The Jinja2 template code which specifies the path of the
      given item. It is relative to the project root which is in general
      {{repository.path}}/{{project.code}}/
    
    :param file_code: The Jinja2 template code which specifies the file name of
      the given item
    
    :param type\_: A :class:`~stalker.core.models.entity.TypeEntity` object
      or any other class which is derived from TypeEntity.
    
    Examples:
    
    A template for asset versions can have this parameters::
    
      from stalker import db
      from satlker.db import auth
      from stalker.core.models import types, pipelineStep
      
      # setup the default database
      db.setup()
      
      # store the query method for ease of use
      session = db.session
      query = db.session.query
      
      # login to the system as admin
      admin = auth.login("admin", "admin")
      
      # create a couple of variables
      path_code = "ASSETS/{{asset_type.name}}/{{pipeline_step.code}}"
      
      file_code = "{{asset.name}}_{{take.name}}_{{asset_type.name}}_\
v{{version.version_number}}"
      
      # create a pipeline step object
      modelingStep = pipelineStep.PipelineStep(
          name="Modeling",
          code="MODEL",
          description="The modeling step of the asset",
          created_by=admin
      )
      
      # create a "Character" AssetType with only one step
      typeObj = types.AssetType(
          name="Character",
          description="this is the character asset type",
          created_by=admin,
          steps=[modelingStep]
      )
      
      # now create our TypeTemplate
      char_template = types.TypeTemplate(
          name="Character",
          description="this is the template which explains how to place \
Character assets",
          path_code=path_code,
          file_code=file_code,
          type=typeObj,
      )
      
      # assign this type template to the structure of the project with id=101
      myProject = query(project.Project).filter_by(id=101).first()
      
      # append the type template to the structures' asset templates
      myProject.structure.asset_templates.append(char_template)
      
      session.commit()
    
    Now with the code above, whenever a new
    :class:`~stalker.core.models.version.Version` created for a **Character**
    asset, Stalker will automatically place the related file to a certain
    folder and with a certain file name defined by the template. For example
    the above template should render something like below for Windows::
    
      |- M:\\\PROJECTS  --> {{repository.path}}
       |- PRENSESIN_UYKUSU  --> {{project.code}}
        |- ASSETS  --> "ASSETS"
         |- Character  --> {{asset_type.name}}
          |- Olum  --> {{asset.name}}
           |- MODEL  --> {{pipeline_step.code}}
            |- Olum_MAIN_MODEL_v001.ma --> {{asset.name}}_\
{{take.name}}_{{asset_type.name}}_v{{version.version_number}}
    
    And one of the good side is you can create a version from Linux, Windows or
    OSX all the paths will be correctly handled by Stalker.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 path_code="",
                 file_code="",
                 type=None,
                 **kwargs):
        super(TypeTemplate, self).__init__(**kwargs)
        
        self._path_code = self._validate_path_code(path_code)
        self._file_code = self._validate_file_code(file_code)
        self._type = self._validate_type(type)
    
    
    
    #----------------------------------------------------------------------
    def _validate_path_code(self, path_code_in):
        """validates the given path_code attribute for several conditions
        """
        
        # check if it is None
        if path_code_in is None:
            raise ValueError("path_code could not be None")
        
        # check if it is an instance of string or unicode
        if not isinstance(path_code_in, (str, unicode)):
            raise ValueError("path_code should be an instance of string "
                             "or unicode")
        
        # check if it is an empty string
        if path_code_in == "":
            raise ValueError("path_code could not be an empty string")
        
        return path_code_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_file_code(self, file_code_in):
        """validates the given file_code attribute for several conditions
        """
        
        # check if it is None
        if file_code_in is None:
            raise ValueError("file_code could not be None")
        
        # check if it is an instance of string or unicode
        if not isinstance(file_code_in, (str, unicode)):
            raise ValueError("file_code should be an instance of string "
                             "or unicode")
        
        # check if it is an empty string
        if file_code_in == "":
            raise ValueError("file_code could not be an empty string")
        
        return file_code_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_type(self, type_in):
        """validates the given type attribute for several conditions
        """
        
        # check if it is None
        if type_in is None:
            raise ValueError("type could not be None")
        
        if not isinstance(type_in, entity.TypeEntity):
            raise ValueError("type should be an instance of "
                             "stalker.core.models.entity.TypeEntity")
        
        return type_in
    
    
    
    #----------------------------------------------------------------------
    def path_code():
        
        def fget(self):
            return self._path_code
        
        def fset(self, path_code_in):
            self._path_code = self._validate_path_code(path_code_in)
        
        doc = """this is the property that helps you assign values to
        path_code attribute"""
        
        return locals()
    
    path_code = property(**path_code())
    
    
    
    #----------------------------------------------------------------------
    def file_code():
        
        def fget(self):
            return self._file_code
        
        def fset(self, file_code_in):
            self._file_code = self._validate_file_code(file_code_in)
        
        doc = """this is the property that helps you assign values to
        file_code attribute"""
        
        return locals()
    
    file_code = property(**file_code())
    
    
    
    #----------------------------------------------------------------------
    def type():
        
        def fget(self):
            return self._type
        
        def fset(self, type_in):
            self._type = self._validate_type(type_in)
        
        doc = """the target type this template should work on, should be an
        instance of :class:`~stalker.core.models.entity.TypeEntity`"""
        
        return locals()
    
    type = property(**type())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """checks the equality of the given object to this one
        """
        #print "running the TypeTemplate.__eq__"
        
        #print super(TypeTemplate, self).__eq__(other)
        #print isinstance(other, TypeTemplate)
        #print self.path_code == other.path_code
        #print self.file_code == other.file_code
        #print self.type == other.type
        
        
        return super(TypeTemplate, self).__eq__(other) and \
               isinstance(other, TypeTemplate) and \
               self.path_code == other.path_code and \
               self.file_code == other.file_code and \
               self.type == other.type
    
    
    