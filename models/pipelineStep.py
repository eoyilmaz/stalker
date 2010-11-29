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
      letters and try to keep simple, like MDL for Model and MM for MatchMove,
      it cannot be empty
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, code="", **kwargs):
        
        super(PipelineStep, self).__init__(**kwargs)
        
        self._code=self._check_code(code)
    
    
    
    #----------------------------------------------------------------------
    def _check_code(self, code):
        """checks the given code value
        """
        
        # check if the code is empty
        if code=='':
            raise(ValueError('the code attribute can not be an empty string'))
        
        # check if the code is None
        if code is None:
            raise(ValueError('the code attribute can not be None'))
        
        # check if it is something other than a string
        if not isinstance(code, (str, unicode)):
            raise(ValueError('the code should be an instance of string or \
            unicode'))
        
        return code
    
    
    
    #----------------------------------------------------------------------
    def code():
        
        def fget(self):
            return self._code
        
        def fset(self, code_in):
            self._code = self._check_code(code_in)
        
        doc = """this is the property that helps getting values from or
        assigning vales to the code attribute
        """
        
        return locals()
    
    code = property(**code())