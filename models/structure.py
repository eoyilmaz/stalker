#-*- coding: utf-8 -*-



from stalker.models import entity






########################################################################
class Structure(entity.Entity):
    """A structure object is the place to hold data about how the physical
    files are arranged in the fileserver or in Stalker terms repository.
    
    A structure has this parameters:
    :param folder_template: it is a string holding several lines of text
      showing the folder structure of the project. Whenever a project is
      created, a lot of folders are created by looking at this folder
      structure.
      
      The template string can have Jinja2 directives. These variables are
      given to the template engine:
      
        * *project*: holds the current :class:`~stalker.models.project` object
          using this structure, so you can use {{project.code}} or
          {{project.sequences}} kind of variables in the Jinja2 template
    
    :param asset_templates: holds :class:`~stalker.models.template.Template`
      objects with an :class:`~stalker.models.typeEntity.AssetType` connected
      to its `type` attribute, which can
      help specifying templates based on the related
      :class:`~stalker.models.typeEntity.AssetType` object.
    
    :param reference_templates: holds
      :class:`~stalker.models.template.Template` objects, which can help
      specifying templates based on the given
      :class:`~stalker.models.typeEntity.LinkType` object
    
    This templates are used in creation of Project folder structure and also
    while interacting with the assets and references in the current project.
    You can create one project structure for `Commmercials` and another project
    structure for Movies and another one for Print jobs etc. and can reuse them
    while creating a new project.
    """
    
    
    
    pass

