#-*- coding: utf-8 -*-



from stalker.models import entity






########################################################################
class Reference(entity.Entity):
    """Holds data about external references.
    
    References are all about to give some external information to the current
    entity (external to the database, so it can be something on the
    :class:`~stalker.models.repository.Repository` or in the Web). The
    reference type is defined by the
    :class:`~stalker.models.typeEntity.ReferenceType` object and it can be
    anything like *General*, *File*, *Folder*, *Web*, *Image*, *Movie*, *Text*
    etc. (you can also use multiple :class:`~stalker.models.tag.Tag` objects to
    adding more information, and filtering back). Again it is defined by the
    needs of the studio.
    
    The references should be used to give external references (as the name
    suggests), it is not a good place to connect
    :class:`~stalker.models.asset.Asset` related source files (namely
    :class:`~stalker.models.version.Version` objects) to files in the
    repository.
    
    The :class:`~stalker.models.project.Project` object also manages the
    reference by moving them to the projects reference folder (a folder which
    is defined by the :class:`~stalker.models.template.ReferenceTemplate`
    objects see :class:`~stalker.models.project.Project` for more details).
    
    :param url: The URL to the reference, it can be an url to a file in the
      file system, or a web page, for file sequences use '#' in place of the
      numerator (`Nuke`_ style). Setting URL to None or an empty string is not
      accepted and causes a ValueError to be raised.
    
    :param type: The type of the reference. It should be an instance of
      :class:`~stalker.models.typeEntity.ReferenceType`, the type can not be
      None or anything other than a
      :class:`~stalker.models.typeEntity.ReferenceType` object.
    
    .. _Nuke: http://www.thefoundry.co.uk
    """
    
    #----------------------------------------------------------------------
    def __init__(self):
        pass









