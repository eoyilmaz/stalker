#-*- coding: utf-8 -*-



from stalker.models import entity







########################################################################
class PipelineStep(entity.SimpleEntity):
    """A PipelineStep object represents the general pipeline steps which are
    used around the studio. A couple of examples are:
    
      * Design
      * Model
      * Rig
      * Fur
      * Shading
      * Previs
      * Match Move
      * Animation
      etc.
    
    :param code: the code of the pipelinestep, it should be all upper case
      letters and try to keep simple, like MDL for Model and MM for MatchMove
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self):
        pass
        
    
    