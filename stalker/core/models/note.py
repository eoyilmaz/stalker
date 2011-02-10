#-*- coding: utf-8 -*-



from stalker.core.models import entity





########################################################################
class Note(entity.SimpleEntity):
    """To leave notes about the connected node
    
    To leave notes in Stalker use the Note class
    
    :param content: the content of the note
    
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, content="", **kwargs):
        super(Note, self).__init__(**kwargs)
        
        self._content = self._validate_content(content)
    
    
    
    #----------------------------------------------------------------------
    def _validate_content(self, content_in):
        """validates the given content
        """
        
        
        
        if content_in is not None and \
           not isinstance(content_in, (str, unicode)):
            raise ValueError("content should be an instance of string or "
                             "unicode")
        
        return content_in
    
    
    
    #----------------------------------------------------------------------
    def content():
        def fget(self):
            return self._content
        
        def fset(self, content_in):
            self._content = self._validate_content(content_in)
        
        doc = """content is a string representing the content of this Note,
        can be given as an empty string or can be even None, but anything other
        than None or string or unicode will raise a ValueError"""
        
        return locals()
    
    content = property(**content())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Note, self).__eq__(other) and \
               isinstance(other, Note) and \
               self.content == other.content
    
    
    
    
    