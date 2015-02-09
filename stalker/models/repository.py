# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import os
import platform
from sqlalchemy import event, Column, Integer, ForeignKey, String
from sqlalchemy.orm import validates
from stalker import defaults
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

    #
    # TODO: Add OpenLDAP support.
    #
    # In an OpenLDAP Server + AutoFS setup Stalker can create new entries to
    # OpenLDAP server.
    #
    # The AutoFS can be installed to any linux system easily or it is already
    # installed. OSX has it already. I know nothing about Windows.
    #
    # AutoFS can be setup to listen for new mount points from an OpendLDAP
    # server. Thus it is heavily related with the users system, Stalker
    # can not do anything about that. The IT should setup workstations.
    #
    # But Stalker can connect to the OpenLDAP server and create new entries.
    #

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
    def _validate_linux_path(self, key, linux_path):
        """validates the given linux path
        """
        from stalker import __string_types__
        if not isinstance(linux_path, __string_types__):
            raise TypeError(
                "%s.linux_path should be an instance of string not %s" %
                (self.__class__.__name__, linux_path.__class__.__name__)
            )

        linux_path = os.path.normpath(linux_path) + '/'

        linux_path = linux_path.replace("\\", "/")

        if self.id is not None and platform.system() == "Linux":
            # update the environment variable
            os.environ[defaults.repo_env_var_template % {'id': self.id}] = \
                linux_path

        return linux_path

    @validates("osx_path")
    def _validate_osx_path(self, key, osx_path):
        """validates the given osx path
        """
        from stalker import __string_types__
        if not isinstance(osx_path, __string_types__):
            raise TypeError(
                "%s.osx_path should be an instance of string not %s" %
                (self.__class__.__name__, osx_path.__class__.__name__)
            )

        osx_path = os.path.normpath(osx_path) + '/'

        osx_path = osx_path.replace("\\", "/")

        if self.id is not None and platform.system() == "Darwin":
            # update the environment variable
            os.environ[defaults.repo_env_var_template % {'id': self.id}] = \
                osx_path

        return osx_path


    @validates("windows_path")
    def _validate_windows_path(self, key, windows_path):
        """validates the given windows path
        """
        from stalker import __string_types__
        if not isinstance(windows_path, __string_types__):
            raise TypeError(
                "%s.windows_path should be an instance of string not %s" %
                (self.__class__.__name__, windows_path.__class__.__name__)
            )

        windows_path = os.path.normpath(windows_path) + '/'

        windows_path = windows_path.replace("\\", "/")

        if self.id is not None and platform.system() == "Windows":
            # update the environment variable
            os.environ[defaults.repo_env_var_template % {'id': self.id}] = \
                windows_path

        return windows_path

    @property
    def path(self):
        """Returns the path for the current os
        """
        # return the proper value according to the current os
        platform_system = platform.system()

        if platform_system == "Linux":
            return self.linux_path
        elif platform_system == "Windows":
            return self.windows_path
        elif platform_system == "Darwin":
            return self.osx_path

    @path.setter
    def path(self, path):
        """Sets the path for the current os
        """
        # return the proper value according to the current os
        platform_system = platform.system()

        if platform_system == "Linux":
            self.linux_path = path
        elif platform_system == "Windows":
            self.windows_path = path
        elif platform_system == "Darwin":
            self.osx_path = path

    def is_in_repo(self, path):
        """Returns True or False depending of the given is in this repo or not

        :param path: The path to be investigated
        :return:
        """
        path = path.replace('\\', '/')
        return path.startswith(self.windows_path) or \
            path.startswith(self.linux_path) or \
            path.startswith(self.osx_path)

    def _to_path(self, path, replace_with):
        """Helper function fot to_*_path functions

        :param path: the input path
        :param replace_with: replace_with path
        :return:
        """
        if path is None:
            raise TypeError('path can not be None')

        from stalker import __string_types__
        if not isinstance(path, __string_types__):
            raise TypeError('path should be a string')

        # expand all variables
        path = os.path.normpath(
            os.path.expandvars(
                os.path.expanduser(path)
            )
        ).replace('\\', '/')

        if path.startswith(self.windows_path):
            return path.replace(self.windows_path, replace_with)
        elif path.startswith(self.linux_path):
            return path.replace(self.linux_path, replace_with)
        elif path.startswith(self.osx_path):
            return path.replace(self.osx_path, replace_with)

        return path

    def to_linux_path(self, path):
        """Returns the linux version of the given path

        :param path: The path that needs to be converted to linux path.
        :return:
        """
        return self._to_path(path, self.linux_path)

    def to_windows_path(self, path):
        """Returns the windows version of the given path

        :param path: The path that needs to be converted to windows path.
        :return:
        """
        return self._to_path(path, self.windows_path)

    def to_osx_path(self, path):
        """Returns the osx version of the given path

        :param path: The path that needs to be converted to osx path.
        :return:
        """
        return self._to_path(path, self.osx_path)

    def to_native_path(self, path):
        """Returns the native version of the given path

        :param path: The path that needs to be converted to native path.
        :return:
        """
        return self._to_path(path, self.path)

    def make_relative(self, path):
        """makes the given path relative to the repository root

        :param path: The path to be made relative
        :return: str
        """
        path = self.to_native_path(path)
        return os.path.relpath(path, self.path).replace('\\', '/')

    @classmethod
    def find_repo(cls, path):
        """returns the repository from the given path

        :param str path: path in a repository
        :return: stalker.models.repository.Repository
        """
        # path could be using environment variables so expand them
        path = os.path.expandvars(path)

        # first find the repository
        repos = Repository.query.all()
        found_repo = None
        for repo in repos:
            if path.startswith(repo.path) \
               or path.startswith(repo.windows_path) \
               or path.startswith(repo.linux_path) \
               or path.startswith(repo.osx_path):
                found_repo = repo
                break
        return found_repo

    @classmethod
    def to_os_independent_path(cls, path):
        """Replaces the part of the given path with repository environment
        variable which makes the given path OS independent.

        :param path: path to make OS independent
        :return:
        """
        # find the related repo
        repo = cls.find_repo(path)

        if repo:
            return '$%s/%s' % (repo.env_var, repo.make_relative(path))
        else:
            return path

    @property
    def env_var(self):
        """returns the env var of this repo
        """
        return defaults.repo_env_var_template % {'id': self.id}

    def __eq__(self, other):
        """the equality operator
        """
        return super(Repository, self).__eq__(other) and \
            isinstance(other, Repository) and \
            self.linux_path == other.linux_path and \
            self.osx_path == other.osx_path and \
            self.windows_path == other.windows_path

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Repository, self).__hash__()


@event.listens_for(Repository, 'after_insert')
def receive_after_insert(mapper, connection, repo):
    """listen for the 'after_insert' event
    """
    logger.debug('auto creating env var for Repository with id: %s' % repo.id)
    os.environ[defaults.repo_env_var_template % {'id': repo.id}] = repo.path


#@event.listens_for
