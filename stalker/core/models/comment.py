#-*- coding: utf-8 -*-



from stalker.core.models import entity





########################################################################
class Comment(entity.Entity):
    """User reviews and comments about other entities.
    
    :param body: the body of the comment, it is a string or unicode variable,
      it can be empty but it is then meaningles to have an empty comment.
      Anything other than a string or unicode will raise a ValueError.
    
    :param to: the relation variable, that holds the connection that this
      comment is related to. it should be an Entity object, any other will
      raise a ValueError
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, body="", to=None, **kwargs):
        super(Comment, self).__init__(**kwargs)
        
        self._body = self._validate_body(body)
        self._to = self._validate_to(to)
    
    
    
    #----------------------------------------------------------------------
    def _validate_body(self, body_in):
        """validates the given body variable
        """
        
        # the body could be empty
        # but it should be an instance of string or unicode
        
        if not isinstance(body_in, (str, unicode)):
            raise ValueError("the body attribute should be an instance of "
                              "string or unicode")
        
        return body_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_to(self, to_in):
        """validates the given to variable
        """
        
        
        # the to variable should be:
        # - not None
        # - an instance of entity.Entity object
        
        if to_in is None:
            raise ValueError("the to attribute could not be empty")
        
        if not isinstance(to_in, entity.Entity):
            raise ValueError("the to attibute should be an instance of "
                             "entity.Entity class")
        
        return to_in
    
    
    
    #----------------------------------------------------------------------
    def body():
        def fget(self):
            return self._body
        
        def fset(self, body_in):
            self._body = self._validate_body(body_in)
        
        doc = """this is the property that sets and returns the body attribute
        """
        
        return locals()
    
    body = property(**body())
    
    
    
    #----------------------------------------------------------------------
    def to():
        def fget(self):
            return self._to
        
        def fset(self, to_in):
            self._to = self._validate_to(to_in)
        
        doc = """this is the property that sets and returns the to attribute
        """
        
        return locals()
    
    to = property(**to())
    
    
    