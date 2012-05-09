# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import validates
from stalker.models.entity import Entity

class Link(Entity):
    """Holds data about external links.
    
    Links are all about giving some external information to the current entity
    (external to the database, so it can be something on the
    :class:`~stalker.core.models.Repository` or in the Web). The type of the
    link (general, file, folder, web page, image, image sequence, video, 
    movie, sound, text etc.) can be defined by a
    :class:`~stalker.core.models.Type` instance (you can also use multiple
    :class:`~stalker.core.models.Tag` instances to add more information, and to
    filter them back). Again it is defined by the needs of the studio.
    
    For sequences of files the file name may contain "#" or multiple of them
    like "###" to define padding.
    
    :param path: The Path to the link, it can be a path to a folder or a file
      in the file system, or a web page. For file sequences use "#" in place of
      the numerator (`Nuke`_ style). Setting the path to None or an empty
      string is not accepted.
    
    .. _Nuke: http://www.thefoundry.co.uk
    """

    __tablename__ = "Links"
    __mapper_args__ = {"polymorphic_identity": "Link"}
    link_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
        )
    path = Column(
        String,
        doc="""The path of the url to the link.
        
        It can not be None or an empty string, it should be a string or
        unicode.
        """
    )

    def __init__(self, path="", **kwargs):
        super(Link, self).__init__(**kwargs)
        self.path = path

    @validates("path")
    def _validate_path(self, key, path):
        """validates the given path
        """

        if path is None:
            raise TypeError("%s.path can not be None" %
                            self.__class__.__name__)

        if not isinstance(path, (str, unicode)):
            raise TypeError("%s.path should be an instance of string or "
                            "unicode not %s" %
                            (self.__class__.__name__,
                             path.__class__.__name__))

        if path == "":
            raise ValueError("%s.path can not be an empty string" %
                             self.__class__.__name__)

        return self._format_path(path)

    def _format_path(self, path):
        """formats the path to internal format, which is Linux forward slashes
        for path separation
        """

        return path.replace("\\", "/")

    def __eq__(self, other):
        """the equality operator
        """

        return super(Link, self).__eq__(other) and\
               isinstance(other, Link) and\
               self.path == other.path and\
               self.type == other.type
