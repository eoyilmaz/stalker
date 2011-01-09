#-*- coding: utf-8 -*-



from stalker.core.models import entity, pipelineStep






########################################################################
class TypeEntity(entity.Entity):
    """TypeEntity is the entry point for types.
    
    It is created to group the `Type` objects, so any other classes accepting a
    ``TypeEntity`` object can have one of the derived classes, this is done in
    that way mainly to ease the of creation of only one
    :class:`~stalker.core.models.typeEntity.TypeTemplate` class and let the
    others to use this one TypeTemplate class.
    
    It doesn't add any new parameters to it's super.
    """
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(TypeEntity, self).__init__(**kwargs)






########################################################################
class AssetType(TypeEntity):
    """The AssetType class holds the information about the asset type.
    
    One asset type object has information about the pipeline steps that this
    type of asset needs.
    
    So for example one can create a "Chracter" asset type and then link
    "Design", "Modeling", "Rig", "Shading" pipeline steps to this asset type
    object. And then have a "Environment" asset type and then just link
    "Design", "Modeling", "Shading" pipeline steps to it.
    
    :param steps: This is a list of PipelineStep objects.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, steps=[], **kwargs):
        super(AssetType, self).__init__(**kwargs)
        
        self._steps = self._check_steps(steps)
    
    
    
    #----------------------------------------------------------------------
    def _check_steps(self, steps_in):
        """checks the given steps list
        """
        
        # raise a Value error if it is not a list
        if not isinstance(steps_in, list):
            raise ValueError("steps should be an instance of list")
        
        # raise a Value error if not all of the elements are pipelineStep
        # objects
        if not all([ isinstance(obj, pipelineStep.PipelineStep)
                 for obj in steps_in]):
            raise ValueError("all of the elements of the given list should be \
            instance of stalker.pipelineStep.PipelineStep class")
        
        return steps_in
    
    
    
    #----------------------------------------------------------------------
    def steps():
        
        def fget(self):
            return self._steps
        
        def fset(self, steps_in):
            self._steps = self._check_steps(steps_in)
        
        doc = """this is the property that lets you set and get steps attribute
        """
        
        return locals()
    
    steps = property(**steps())






########################################################################
class LinkType(TypeEntity):
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






########################################################################
class ProjectType(TypeEntity):
    """Helps to create different type of
    :class:`~stalker.core.models.project.Project` objects.
    
    Can be used to create different type projects like Commercial, Movie, Still
    etc.
    """
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(ProjectType, self).__init__(**kwargs)







########################################################################
class TypeTemplate(entity.Entity):
    """The TypeTemplate model holds templates for Types.
    
    TypeTemplate objects help to specify where to place a file related to
    :class:`~stalker.core.models.typeEntity.TypeEntity` objects and its derived
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
    
    :param type: A :class:`~stalker.core.models.typeEntity.TypeEntity` object
      or any other class which is derived from Type.
    
    Examples:
    
    A template for asset versions can have this parameters::
    
      from stalker import db
      from satlker.db import auth
      from stalker.core.models import typeEntity, pipelineStep
      
      # setup the default database
      db.setup()
      
      # store the query method for ease of use
      session = db.meta.session
      query = db.meta.session.query
      
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
      typeObj = typeEntity.AssetType(
          name="Character",
          description="this is the character asset type",
          created_by=admin,
          steps=[modelingStep]
      )
      
      # now create our TypeTemplate
      char_template = typeEntity.TypeTemplate(
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
    the above template should render something like below for Windows:
    
    |- M:\\\PROJECTS  --> {{repository.path}}
       |- PRENSESIN_UYKUSU  --> {{project.code}}
          |- ASSETS  --> "ASSETS"
            |- Character  --> {{asset_type.name}}
               |- Olum  --> {{asset.name}}
                  |- MODEL  --> {{pipeline_step.code}}
                     |- Olum_MAIN_MODEL_v001.ma  --> {{asset.name}}_\
{{take.name}}_{{asset_type.name}}_v{{version.version_number}}
    
    And one of the good side is you can create a version from Linux, Windows or
    OSX all the paths will be correctly handled by Stalker.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, template_code, **kwargs):
        super(Template, self).__init__(**kwargs)
        
        self._template_code = self._check_template_code(template_code)
    
    
    
    #----------------------------------------------------------------------
    def _check_template_code(self, template_code_in):
        """checks the given template_code attribute for several conditions
        """
        
        # check if it is None
        if template_code_in is None:
            raise(ValueError("template_code could not be None"))
        
        # check if it is an empty string
        if template_code_in == "":
            raise(ValueError("template_code could not be an empty string"))
        
        # check if it is an instance of string or unicode
        if not isinstance(template_code_in, (str, unicode)):
            raise(ValueError("template_code should be an instance of string \
            or unicode"))
        
        return template_code_in
    
    
    
    #----------------------------------------------------------------------
    def template_code():
        
        def fget(self):
            return self._template_code
        
        def fset(self, template_code_in):
            self._template_code = self._check_template_code(template_code_in)
        
        doc = """this is the property that helps you assign values to
        template_code attribute"""
        
        return locals()
    
    template_code = property(**template_code())





