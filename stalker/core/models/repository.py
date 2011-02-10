#-*- coding: utf-8 -*-



import platform
from stalker.core.models import entity






########################################################################
class Repository(entity.Entity):
    """Repository is a class to hold repository server data. A repository is a
    network share that all users have access to.
    
    A studio can create several repositories, for example, one for movie
    projects and one for commercial projects.
    
    A repository also defines the default paths for linux, windows and mac
    fileshares.
    
    :param linux_path: shows the linux path of the repository root, should be a
      string
    
    :param osx_path: shows the mac osx path of the repository root, should be a
      string
    
    :param windows_path: shows the windows path of the repository root, should
      be a string
    
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, linux_path="", windows_path="", osx_path="", **kwargs):
        super(Repository, self).__init__(**kwargs)
        
        self._linux_path = self._validate_linux_path(linux_path)
        self._windows_path = self._validate_windows_path(windows_path)
        self._osx_path = self._validate_osx_path(osx_path)
    
    
    
    #----------------------------------------------------------------------
    def _validate_linux_path(self, linux_path_in):
        """validates the given linux path
        """
        
        if not isinstance(linux_path_in, (str, unicode)):
            raise ValueError("linux_path should be an instance of string or "
                             "unicode")
        
        return linux_path_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_osx_path(self, osx_path_in):
        """validates the given osx path
        """
        
        if not isinstance(osx_path_in, (str, unicode)):
            raise ValueError("osx_path should be an instance of string or "
                             "unicode")
        
        return osx_path_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_windows_path(self, windows_path_in):
        """validates the given windows path
        """
        
        if not isinstance(windows_path_in, (str, unicode)):
            raise ValueError("windows_path should be an instance of string or "
                             "unicode")
        
        return windows_path_in
    
    
    
    #----------------------------------------------------------------------
    def linux_path():
        
        def fget(self):
            return self._linux_path
        
        def fset(self, linux_path_in):
            self._linux_path = self._validate_linux_path(linux_path_in)
        
        doc = """property that helps to set and get linux_path values"""
        
        return locals()
    
    linux_path = property(**linux_path())
    
    
    
    #----------------------------------------------------------------------
    def osx_path():
        
        def fget(self):
            return self._osx_path
        
        def fset(self, osx_path_in):
            self._osx_path = self._validate_osx_path(osx_path_in)
        
        doc = """property that helps to set and get osx_path values"""
        
        return locals()
    
    osx_path = property(**osx_path())
    
    
    
    #----------------------------------------------------------------------
    def windows_path():
        
        def fget(self):
            return self._windows_path
        
        def fset(self, windows_path_in):
            self._windows_path = self._validate_windows_path(windows_path_in)
        
        doc = """property that helps to set and get windows_path values"""
        
        return locals()
    
    windows_path = property(**windows_path())
    
    
    
    #----------------------------------------------------------------------
    def path():
        
        def fget(self):
            
            # return the proper value according to the current os
            platform_system = platform.system()
            
            if platform_system == "Linux":
                return self.linux_path
            elif platform_system == "Windows":
                return self.windows_path
            elif platform_system == "Darwin":
                return self.osx_path
        
        doc = """property that helps to get path for the current os"""
        
        return locals()
    
    path = property(**path())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Repository, self).__eq__(other) and \
               isinstance(other, Repository) and \
               self.linux_path == other.linux_path and \
               self.osx_path == other.osx_path and \
               self.windows_path == other.windows_path
        
    
    
    