#-*- coding: utf-8 -*-



from stalker.models import entity






########################################################################
class Link(entity.TaggedEntity):
    """A link is the type of class that holds information about outer
    resources, like web links, files, file sequences and folders. It is the
    main door of Stalker to the file system and the internet. It is aimed to
    be used as direct links to files but it is not the correct place to hold
    information about Asset and file connections. It is the duty of Version
    objects to hold information about the Asset and file connections.
    
    Use this class for just reference a file or link to an entity.
    """
    
    
    
    pass

