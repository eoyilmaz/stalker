#-*- coding: utf-8 -*-



from stalker.core.models import entity, types
from stalker.ext.validatedList import ValidatedList





########################################################################
class Structure(entity.Entity):
    """A structure object is the place to hold data about how the physical
    files are arranged in the
    :class:`~stalker.core.models.repository.Repository`.
    
    :param project_template: it is a string holding several lines of text
      showing the folder structure of the project. Whenever a project is
      created, folders are created by looking at this folder template.
      
      The template string can have Jinja2 directives. These variables are given
      to the template engine:
      
        * *project*: holds the current
          :class:`~stalker.core.models.project.Project`
          object using this structure, so you can use {{project.code}} or
          {{project.sequences}} kind of variables in the Jinja2 template
    
    :param asset_templates: holds
      :class:`~stalker.core.models.types.TypeTemplate` objects with an
      :class:`~stalker.core.models.types.AssetType` connected to its
      `type` attribute, which can help specifying templates based on the
      related :class:`~stalker.core.models.types.AssetType` object.
      
      Testing a second paragraph addition.
    
    :param reference_templates: holds
      :class:`~stalker.core.models.types.TypeTemplate` objects, which can
      help specifying templates based on the given
      :class:`~stalker.core.models.types.LinkType` object
    
    This templates are used in creation of Project folder structure and also
    while interacting with the assets and references in the current
    :class:`~stalker.core.models.project.Project`. You can create one project
    structure for `Commmercials` and another project structure for `Movies` and
    another one for `Print` projects etc. and can reuse them with new projects.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 project_template="",
                 asset_templates=[],
                 reference_templates=[], **kwargs):
        super(Structure, self).__init__(**kwargs)
        
        self._project_template = self._validate_project_template(project_template)
        self._asset_templates = self._validate_asset_templates(asset_templates)
        self._reference_templates = \
            self._validate_reference_templates(reference_templates)
    
    
    
    #----------------------------------------------------------------------
    def _validate_asset_templates(self, asset_templates_in):
        """validates the given asset_templates list
        """
        
        if not isinstance(asset_templates_in, list):
            raise ValueError("asset_templates should be a list object")
        
        for element in asset_templates_in:
            if not isinstance(element, types.TypeTemplate):
                raise ValueError(
                    "asset_templates should only contain instances of "
                    "stalker.core.models.types.TypeTemplate objects"
                )
        
        return ValidatedList(asset_templates_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_reference_templates(self, reference_templates_in):
        """validates the given reference_templates list
        """
        
        if not isinstance(reference_templates_in, list):
            raise ValueError("reference_templates should be a list object")
        
        for element in reference_templates_in:
            if not isinstance(element, types.TypeTemplate):
                raise ValueError(
                    "reference_templates should only contain instances of "
                    "stalker.core.models.types.TypeTemplate objects"
                )
        
        return ValidatedList(reference_templates_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_project_template(self, project_template_in):
        """validates the given project_template object
        """
        
        if not isinstance(project_template_in, (str, unicode)):
            raise ValueError(
                "project_template should be an instance of string or unicode"
            )
        
        return project_template_in
    
    
    
    #----------------------------------------------------------------------
    def asset_templates():
        
        def fget(self):
            return self._asset_templates
        
        def fset(self, asset_templates_in):
            self._asset_templates = \
                self._validate_asset_templates(asset_templates_in)
        
        doc = """A list of
        :class:`~stalker.core.models.types.TypeTemplate` objects which
        gives information about the :class:`~stalker.core.models.asset.Asset`
        :class:`~stalker.core.models.version.Version` file placements"""
        
        return locals()
    
    asset_templates = property(**asset_templates())
    
    
    
    #----------------------------------------------------------------------
    def reference_templates():
        
        def fget(self):
            return self._reference_templates
        
        def fset(self, reference_templates_in):
            self._reference_templates = \
                self._validate_reference_templates(reference_templates_in)
        
        doc = """A list of
        :class:`~stalker.core.models.types.TypeTemplate` objects which
        gives information about the placement of references to entities"""
        
        return locals()
    
    reference_templates = property(**reference_templates())
    
    
    
    #----------------------------------------------------------------------
    def project_template():
        
        def fget(self):
            return self._project_template
        
        def fset(self, project_template_in):
            self._project_template = \
                self._validate_project_template(project_template_in)
        
        doc= """A string which shows the folder structure of the current
        project. It can have Jinja2 directives. See the documentation of
        :class:`~stalker.core.models.structure.Structure` object for more
        information"""
        
        return locals()
    
    project_template = property(**project_template())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Structure, self).__eq__(other) and \
               isinstance(other, Structure) and \
               self.project_template == other.project_template and \
               self.reference_templates == other.reference_templates and \
               self.asset_templates == other.asset_templates
    
    
    