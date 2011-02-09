#-*- coding: utf-8 -*-



from stalker.core.models import entity, types






########################################################################
class Link(entity.Entity):
    """Holds data about external links.
    
    Links are all about to give some external information to the current entity
    (external to the database, so it can be something on the
    :class:`~stalker.core.models.repository.Repository` or in the Web). The
    link type is defined by the
    :class:`~stalker.core.models.types.LinkType` object and it can be
    anything like *General*, *File*, *Folder*, *WebPage*, *Image*,
    *ImageSequence*, *Movie*, *Text* etc. (you can also use multiple
    :class:`~stalker.core.models.tag.Tag` objects to adding more information,
    and filtering back). Again it is defined by the needs of the studio.
    
    :param path: The Path to the link, it can be a path to a file in the file
      system, or a web page.  Setting path to None or an empty string is not
      accepted and causes a ValueError to be raised.
    
    :param filename: The file name part of the link url, for file sequences use
      "#" in place of the numerator (`Nuke`_ style). Setting filename to None
      or an empty string is not accepted and causes a ValueError to be raised.
    
    :param type\_: The type of the link. It should be an instance of
      :class:`~stalker.core.models.types.LinkType`, the type can not be
      None or anything other than a
      :class:`~stalker.core.models.types.LinkType` object. Specifies the link
      type, can be an LinkType with name Image, Movie/Video, Sound etc.
    
    .. _Nuke: http://www.thefoundry.co.uk
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, path="", filename="", type=None, **kwargs):
        super(Link, self).__init__(**kwargs)
        
        self._path = self._validate_path(path)
        self._filename = self._validate_filename(filename)
        self._type = self._validate_type(type)
    
    
    
    #----------------------------------------------------------------------
    def _validate_path(self, path_in):
        """validates the given path
        """
        
        if path_in is None:
            raise ValueError("path can not be None")
        
        if not isinstance(path_in, (str, unicode)):
            raise ValueError("path should be an instance of string or unicode")
        
        if path_in=="":
            raise ValueError("path can not be an empty string")
        
        return self._format_path(path_in)
    
    
    
    #----------------------------------------------------------------------
    def _format_path(self, path_in):
        """formats the path to internal format, which is Linux forward slashes
        for path seperation
        """
        
        return path_in.replace("\\", "/")
    
    
    
    #----------------------------------------------------------------------
    def _validate_filename(self, filename_in):
        """validates the given filename
        """
        
        if filename_in is None:
            raise ValueError("filename can not be None")
        
        if not isinstance(filename_in, (str, unicode)):
            raise ValueError("filename should be an instance of string or "
                             "unicode")
        
        if filename_in=="":
            raise ValueError("filename can not be an empty string")
        
        return filename_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_type(self, type_in):
        """validates the given type
        """
        
        if type_in is None:
            raise ValueError("type can not be None, set it to a "
                             "stalker.core.models.types.LinkType object")
        
        if not isinstance(type_in, types.LinkType):
            raise ValueError("type should be an instance of "
                             "stalker.core.models.types.LinkType object")
        
        return type_in
    
    
    
    #----------------------------------------------------------------------
    def path():
        def fget(self):
            return self._path
        
        def fset(self, path_in):
            self._path = self._validate_path(path_in)
        
        doc="""the path part of the url to the link, it can not be None or an
        empty string, it should be a string or unicode"""
        
        return locals()
    
    path = property(**path())
    
    
    
    #----------------------------------------------------------------------
    def filename():
        def fget(self):
            return self._filename
        
        def fset(self, filename_in):
            self._filename = self._validate_filename(filename_in)
        
        doc="""the filename part of the url to the link, it can not be None or
        an empty string, it should be a string or unicode"""
        
        return locals()
    
    filename = property(**filename())
    
    
    
    #----------------------------------------------------------------------
    def type():
        def fget(self):
            return self._type
        
        def fset(self, type_in):
            self._type = self._validate_type(type_in)
        
        doc="""the type of the link, it should be a
        :class:`~stalker.core.models.types.LinkType` object and it can not be
        None"""
        
        return locals()
    
    type = property(**type())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Link, self).__eq__(other) and \
               isinstance(other, Link) and \
               self.path == other.path and \
               self.filename == other.filename and \
               self.type == other.type
    
    
    