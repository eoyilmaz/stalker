# -*- coding: utf-8 -*-

import os
import platform
from sqlalchemy import event, Column, Integer, ForeignKey, String
from sqlalchemy.orm import validates
from stalker.models.entity import Entity
from stalker.models.mixins import CodeMixin

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Repository(Entity, CodeMixin):
    """Manages fileserver/repository related data.

    A repository is a network share that all users have access to.

    A studio can create several repositories, for example, one for movie
    projects and one for commercial projects.

    A repository also defines the default paths for linux, windows and mac
    foreshores.

    The path separator in the repository is always forward slashes ("/").
    Setting a path that contains backward slashes ("\\"), will be converted to
    a path with forward slashes.

    .. versionadded:: 0.2.24
       Code attribute

       Starting with v0.2.24 Repository instances have a new :attr:`.code`
       attribute whose value is used by the
       :class:`stalker.models.studio.Studio` to generate environment variables
       that contains the path of this
       :class:`stalker.models.repository.Repository` (i.e.
       $REPOCP/path/to/asset.ma ``CP`` here is the ``Repository.code``) so that
       instead of using absolute full paths one can use the
       :attr:`.make_relative`` path to generate a universal path that can be
       used across OSes and different installations of Stalker.

    :param code: The code of the :class:`stalker.models.repository.Repository`.
      This attribute value is used by the :class:`stalker.models.studio.Studio`
      to generate environment variables that contains the path of this
      ``Repository`` (i.e. $REPOCP/path/to/asset.ma) so that instead of using
      absolute full paths one can use the ``repository_relative`` path to
      generate a universal path that can be used across OSes and different
      installations of Stalker.

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
                 code="",
                 linux_path="",
                 windows_path="",
                 osx_path="",
                 **kwargs):
        kwargs['code'] = code
        super(Repository, self).__init__(**kwargs)
        CodeMixin.__init__(self, **kwargs)

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

        if self.code is not None and platform.system() == "Linux":
            # update the environment variable
            from stalker import defaults
            os.environ[
                defaults.repo_env_var_template % {'code': self.code}
            ] = linux_path

        if self.id is not None and platform.system() == "Linux":
            # update the environment variable
            from stalker import defaults
            os.environ[
                defaults.repo_env_var_template_old % {'id': self.id}
            ] = linux_path

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

        from stalker import defaults
        if self.code is not None and platform.system() == "Darwin":
            # update the environment variable
            os.environ[
                defaults.repo_env_var_template % {'code': self.code}
            ] = osx_path

        if self.id is not None and platform.system() == "Darwin":
            os.environ[
                defaults.repo_env_var_template_old % {'id': self.id}
            ] = osx_path

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

        windows_path = os.path.normpath(windows_path)
        windows_path = windows_path.replace("\\", "/")

        if not windows_path.endswith('/'):
            windows_path += '/'

        if self.code is not None and platform.system() == "Windows":
            # update the environment variable
            from stalker import defaults
            os.environ[
                defaults.repo_env_var_template % {'code': self.code}
            ] = windows_path

        if self.id is not None and platform.system() == "Windows":
            # update the environment variable
            from stalker import defaults
            os.environ[
                defaults.repo_env_var_template_old % {'id': self.id}
            ] = windows_path

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
        return path.lower().startswith(self.windows_path.lower()) or \
            path.startswith(self.linux_path) or \
            path.startswith(self.osx_path)

    def _to_path(self, path, replace_with):
        """Helper function fot to_*_path functions

        :param path: the input path
        :param replace_with: replace_with path
        :return:
        """
        if path is None:
            raise TypeError(
                '%s.path can not be None' % self.__class__.__name__
            )

        from stalker import __string_types__
        if not isinstance(path, __string_types__):
            raise TypeError(
                '%s.path should be a string, not %s' % (
                    self.__class__.__name__, path.__class__.__name__
                )
            )

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
               or path.lower().startswith(repo.windows_path.lower()) \
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
        from stalker import defaults
        return defaults.repo_env_var_template % {'code': self.code}

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
    logger.debug('auto creating env var for Repository: %s' % repo.name)
    from stalker import defaults
    os.environ[
        defaults.repo_env_var_template % {'code': repo.code}
    ] = repo.path
    os.environ[
        defaults.repo_env_var_template_old % {'id': repo.id}
    ] = repo.path
