#-*- coding: utf-8 -*-



from stalker.models import entity






########################################################################
class Template(entity.Entity):
    """The template model holds templates for Types.
    
    Template objects help to specify where to place a file related to
    :class:`~stalker.models.typeEntity.TypeEntity` objects and its derived
    classes.
    
    The first very important usage of Templates is to place asset
    :class:`~stalker.models.version.Version`'s to proper places inside a
    :class:`~stalker.models.project.Project`'s
    :class:`~stalker.models.structure.Structure`.
    
    :param path_code: The Jinja2 template code which specifies the path of the
      given item.
    
    :param file_code: The Jinja2 template code which specifies the file name of
      the given item
    
    :param type: A :class:`~stalker.models.typeEntity.TypeEntity` object or any
      other class which is derived from Type.
    
    Examples:
    
    A template for asset versions can have this parameters::
    
      from stalker import db
      from satlker.db import auth
      from stalker.models import typeEntity, template, pipelineStep
      
      # setup the default database
      db.setup()
      
      # store the query method for ease of use
      session = db.meta.session
      query = db.meta.session.query
      
      # login to the system as admin
      admin = auth.login('admin', 'admin')
      
      # create a couple of variables
      path_code = "{{repository.path}}/{{project.code}}/ASSETS/\
{{asset_type.name}}/{{pipeline_step.code}}"
      
      file_code = "{{asset.name}}_{{take.name}}_{{asset_type.name}}_\
v{{version.version_number}}"
      
      # create a pipeline step object
      modelingStep = pipelineStep.PipelineStep(
          name='Modeling',
          code='MODEL',
          description='The modeling step of the asset',
          created_by=admin
      )
      
      # create a 'Character' AssetType with only one step
      typeObj = typeEntity.AssetType(
          name='Character',
          description='this is the character asset type',
          created_by=admin,
          steps=[modelingStep]
      )
      
      # now create our template
      char_template = template.Template(
          name='Character',
          description='this is the template which explains how to place \
Character assets',
          path_code=path_code,
          file_code=file_code,
          type=typeObj,
      )
      
      # assign this template to the structure of the project with id=101
      myProject = query(project.Project).filter_by(id=101).first()
      
      # append the template to the structures asset templates
      myProject.structure.asset_templates.append(char_template)
      
      session.commit()
    
    Now with the code above, whenever a new
    :class:`~stalker.models.version.Version` created for a **Character** asset,
    Stalker will automatically place the related file to a certain folder and
    with a certain file name defined by the template. For example the above
    template should render something like below for Windows:
    
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
            raise(ValueError('template_code could not be None'))
        
        # check if it is an empty string
        if template_code_in == "":
            raise(ValueError('template_code could not be an empty string'))
        
        # check if it is an instance of string or unicode
        if not isinstance(template_code_in, (str, unicode)):
            raise(ValueError('template_code should be an instance of string \
            or unicode'))
        
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

