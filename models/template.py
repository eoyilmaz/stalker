#-*- coding: utf-8 -*-



from stalker.models import entity






########################################################################
class Template(entity.Entity):
    """This is the template model. It holds templates for various tasks. The
    only attribute it has is the `template_code` attiribute
    
    :param template_code: holds the template code suitable to the template
      engine selected in the settings, the default template rendering engine is
      Jinja2, so the code is should be a jinja2 template if you want to use the
      defaults. It should be a string or unicode value, and cannot be empty
    
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






########################################################################
class PipelineTemplate(Template):
    """PipelineTemplate objects help to specify where to place a file related
    to a pipelineStep object.
    
    When a user wants put a :ref:~stalker.models.version.Version of his file to
    server then Stalker decides where to put this file in the server by looking
    at the related :ref:~stalker.models.assetType and
    :ref:~stalker.models.pipelineStep.PipelineStep object of this version an
    then by using the given template code it evaluates the path and the file
    names of the current version
    
    :param asset_type: holds one asset type object
    
    examples::
    
        from stalker import db
        from stalker.models import (
            asset,
            pipelineTemplate,
            status,
            task,
            version,
        )
        db.setup()
        session = db.meta.session
        newCharacterTemplate = pipelineTemplate.PipelineTemplate(
            name='Character Template',
            description='This is the template that shows where to save a \
character asset',
            path_code='{{project.code}}/ASSETS/{{assetType.name}}s/\
{{asset.code}}/{{pipelineStep.name}}',
            file_code='{{asset.code}}_{{take.name}}_{{pipelineStep.name}}_\
{{version.version_number}}.{{version.file.extension}}'
        )
    
    Lets create a new character asset::
    
        from stalker import db
        
        charStatList = session.query(status.StatusList).filter_by(\
name='Character Status List').first()
        charAssetType = session.query(assetType.AssetType).filter_by(\
name='Character').first()
        newAsset = asset.Asset(
            name='Olum',
            description='This is the final boss which is going to be seen in the\
end of the movie. It should give the feeling of the death.'
            statusList=charStatList,
            status=0,
            type=charAssetType)
    
    Create a task for the asset
    
    >>> newTask = task.Task(
        name='Model',
        description'='The modeling task of the asset')
    
    Create a new version for the task
    
    >>> newVersion=version.Version(
            name='a version',
            description='a description',
            version=1,
            revision=0,
        )
    
    Attach it to the task
    
    >>> newTask.versions.append(newVersion)
    
    Assign the new asset to a project from the database
    
    >>> session.query(project.Project).filter_by(code='PRENUYK').first().\
assets.append(newAsset)
    
    Save them to the database
    
    >>> session.add(newCharacterTemplate, newAsset, newTask, newVersion)
    >>> session.commit()
    
    Now render the template with the given entity, in our case it is the
    version:
    
    >>> newTemplate.render(newVersion)
    ('PRENUYK/ASSETS/Characters/Olum/Design/','Olum_MAIN_DESIGN_v001')
    
    """
    
    pass
        
        
    
    