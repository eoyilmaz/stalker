#-*- coding: utf-8 -*-



from stalker.models import entity






########################################################################
class Link(entity.Entity):
    """Holds data about external links.
    
    Links are all about to give some external information to the current entity
    (external to the database, so it can be something on the
    :class:`~stalker.models.repository.Repository` or in the Web). The link
    type is defined by the :class:`~stalker.models.typeEntity.LinkType` object
    and it can be anything like *General*, *File*, *Folder*, *Web*, *Image*,
    *ImageSequence*, *Movie*, *Text* etc. (you can also use multiple
    :class:`~stalker.models.tag.Tag` objects to adding more information, and
    filtering back). Again it is defined by the needs of the studio.
    
    :param url: The URL to the link, it can be an url to a file in the
      file system, or a web page, for file sequences use '#' in place of the
      numerator (`Nuke`_ style). Setting URL to None or an empty string is not
      accepted and causes a ValueError to be raised.
    
    :param type: The type of the link. It should be an instance of
      :class:`~stalker.models.typeEntity.LinkType`, the type can not be
      None or anything other than a
      :class:`~stalker.models.typeEntity.LinkType` object.
    
    .. _Nuke: http://www.thefoundry.co.uk
    """
    
    #----------------------------------------------------------------------
    def __init__(self):
        pass









