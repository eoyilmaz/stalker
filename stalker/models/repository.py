# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
# 
# This file is part of Stalker.
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import os
import platform
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import validates
from stalker.models.entity import Entity

from stalker.log import logging_level
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

class Repository(Entity):
    """Manages fileserver/repository related data.
    
    A repository is a network share that all users have access to.
    
    A studio can create several repositories, for example, one for movie
    projects and one for commercial projects.
    
    A repository also defines the default paths for linux, windows and mac
    foreshores.
    
    The path separator in the repository is always forward slashes ("/").
    Setting a path that contains backward slashes ("\\"), will be converted to
    a path with forward slashes.
    
    :param linux_path: shows the linux path of the repository root, should be a
      string
    
    :param osx_path: shows the mac osx path of the repository root, should be a
      string
    
    :param windows_path: shows the windows path of the repository root, should
      be a string
    """

    # TODO: Add OpenLDAP support, or at least learn how those stuff works.

    __auto_name__ = False
    __tablename__ = 'Repositories'
    __mapper_args__ = {'polymorphic_identity': 'Repository'}
    repository_id = Column(
        'id',
        Integer,
        ForeignKey('Entities.id'),
        primary_key=True,
    )
    linux_path = Column(String(256))
    windows_path = Column(String(256))
    osx_path = Column(String(256))

    def __init__(self,
                 linux_path="",
                 windows_path="",
                 osx_path="",
                 **kwargs):
        super(Repository, self).__init__(**kwargs)

        self.linux_path = linux_path
        self.windows_path = windows_path
        self.osx_path = osx_path

    @validates("linux_path")
    def _validate_linux_path(self, key, linux_path_in):
        """validates the given linux path
        """
        if not isinstance(linux_path_in, (str, unicode)):
            raise TypeError("%s.linux_path should be an instance of string "
                            "or unicode not %s" %
                            (self.__class__.__name__,
                             linux_path_in.__class__.__name__))
        
        linux_path_in = os.path.normpath(linux_path_in) + '/'
        
        return linux_path_in.replace("\\", "/")

    @validates("osx_path")
    def _validate_osx_path(self, key, osx_path_in):
        """validates the given osx path
        """
        if not isinstance(osx_path_in, (str, unicode)):
            raise TypeError("%s.osx_path should be an instance of string or "
                            "unicode not %s" %
                            (self.__class__.__name__,
                             osx_path_in.__class__.__name__))
        
        osx_path_in = os.path.normpath(osx_path_in) + '/'

        return osx_path_in.replace("\\", "/")

    @validates("windows_path")
    def _validate_windows_path(self, key, windows_path_in):
        """validates the given windows path
        """
        if not isinstance(windows_path_in, (str, unicode)):
            raise TypeError("%s.windows_path should be an instance of string "
                            "or unicode not %s" %
                            (self.__class__.__name__,
                             windows_path_in.__class__.__name__))
        
        windows_path_in = os.path.normpath(windows_path_in) + '/'
        
        return windows_path_in.replace("\\", "/")
    
    @property
    def path(self):
        """The path for the current os"""
        # return the proper value according to the current os
        platform_system = platform.system()

        if platform_system == "Linux":
            return self.linux_path
        elif platform_system == "Windows":
            return self.windows_path
        elif platform_system == "Darwin":
            return self.osx_path

    def __eq__(self, other):
        """the equality operator
        """
        return super(Repository, self).__eq__(other) and\
               isinstance(other, Repository) and\
               self.linux_path == other.linux_path and\
               self.osx_path == other.osx_path and\
               self.windows_path == other.windows_path
