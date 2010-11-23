#-*- coding: utf-8 -*-



from stalker.models import entity, pipelineStep




########################################################################
class AssetType(entity.SimpleEntity):
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
    