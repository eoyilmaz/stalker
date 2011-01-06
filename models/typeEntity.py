#-*- coding: utf-8 -*-



from stalker.models import entity, pipelineStep






########################################################################
class TypeEntity(entity.Entity):
    """TypeEntity is the entry point for types.
    
    It is created to group the `Type` objects, so any other classes accepting a
    ``TypeEntity`` object can have one of the derived classes, this is done in
    that way mainly to ease the of creation of only one
    :class:`~stalker.models.template.Template` class and let the others to use
    this one Template class.
    
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
            raise ValueError('steps should be an instance of list')
        
        # raise a Value error if not all of the elements are pipelineStep
        # objects
        if not all([ isinstance(obj, pipelineStep.PipelineStep)
                 for obj in steps_in]):
            raise ValueError('all of the elements of the given list should be \
            instance of stalker.pipelineStep.PipelineStep class')
        
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
    """The type of :class:`~stalker.models.link.Link` is hold in LinkType
    objects.
    
    LinkType objects hold the type of the link and it is generaly
    used by :class:`~stalker.models.project.Project` to sort things out. See
    :class:`~stalker.models.project.Project` object documentation for details.
    """
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(LinkType, self).__init__(**kwargs)






########################################################################
class ProjectType(TypeEntity):
    """Helps to create different type of
    :class:`~stalker.models.project.Project` objects.
    
    Can be used to create different type projects like Commercial, Movie, Still
    etc.
    """
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(ProjectType, self).__init__(**kwargs)


