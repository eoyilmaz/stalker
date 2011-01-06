#-*- coding: utf-8 -*-



from stalker.core.models import entity






########################################################################
class Structure(entity.Entity):
    """A structure object is the place to hold data about how the physical
    files are arranged in the
    :class:`~stalker.core.models.repository.Repository`.
    
    A structure has these parameters:
    :param folder_template: it is a string holding several lines of text
      showing the folder structure of the project. Whenever a project is
      created, folders are created by looking at this folder template.
      
      The template string can have Jinja2 directives. These variables are
      given to the template engine:
      
        * *project*: holds the current :class:`~stalker.core.models.project`
          object using this structure, so you can use {{project.code}} or
          {{project.sequences}} kind of variables in the Jinja2 template
    
    :param asset_templates: holds
      :class:`~stalker.core.models.template.Template` objects with an
      :class:`~stalker.core.models.typeEntity.AssetType` connected to its
      `type` attribute, which can help specifying templates based on the
      related :class:`~stalker.core.models.typeEntity.AssetType` object.
    
    :param reference_templates: holds
      :class:`~stalker.core.models.template.Template` objects, which can help
      specifying templates based on the given
      :class:`~stalker.core.models.typeEntity.LinkType` object
    
    This templates are used in creation of Project folder structure and also
    while interacting with the assets and references in the current
    :class:`~stalker.core.models.project.Project`. You can create one project
    structure for `Commmercials` and another project structure for `Movies` and
    another one for `Print` projects etc. and can reuse them with new projects.
    """
    
    
    
    pass

