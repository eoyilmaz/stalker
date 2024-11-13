# -*- coding: utf-8 -*-
"""Repository related functionality is situated here."""
import os
import platform
from typing import Any, Dict, Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, String, event
from sqlalchemy.orm import Mapped, mapped_column, validates

from stalker import defaults
from stalker.log import get_logger
from stalker.models.entity import Entity
from stalker.models.mixins import CodeMixin

if TYPE_CHECKING:  # pragma: no cover
    from sqlalchemy.orm import Mapper
    from sqlalchemy.engine import Connection

logger = get_logger(__name__)


class Repository(Entity, CodeMixin):
    r"""Manage fileserver/repository related data.

    A repository is a network share that all users have access to.

    A studio can create several repositories, for example, one for movie
    projects and one for commercial projects.

    A repository also defines the default paths for linux, windows and mac
    foreshores.

    The path separator in the repository is always forward slashes ("/").
    Setting a path that contains backward slashes ("\"), will be converted to
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

    Args:
        code (str): The code of the :class:`stalker.models.repository.Repository`.
            This attribute value is used by the :class:`stalker.models.studio.Studio`
            to generate environment variables that contains the path of this
            ``Repository`` (i.e. $REPOCP/path/to/asset.ma) so that instead of
            using absolute full paths one can use the ``repository_relative``
            path to generate a universal path that can be used across OSes and
            different installations of Stalker.
        linux_path (str): shows the linux path of the repository root, should be
            a string
        macos_path (str): shows the macOS path of the repository root, should be
            a string.
        windows_path (str): shows the windows path of the repository root, should
            be a string
    """

    #
    # TODO: Add OpenLDAP support.
    #
    # In an OpenLDAP Server + AutoFS setup Stalker can create new entries to
    # OpenLDAP server.
    #
    # The AutoFS can be installed to any linux system easily or it is already
    # installed. macOS has it already. I know nothing about Windows.
    #
    # AutoFS can be setup to listen for new mount points from an OpenLDAP
    # server. Thus it is heavily related with the users system, Stalker
    # cannot do anything about that. The IT should setup workstations.
    #
    # But Stalker can connect to the OpenLDAP server and create new entries.
    #

    __auto_name__ = False
    __tablename__ = "Repositories"
    __mapper_args__ = {"polymorphic_identity": "Repository"}
    repository_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Entities.id"),
        primary_key=True,
    )
    linux_path: Mapped[Optional[str]] = mapped_column(String(256))
    windows_path: Mapped[Optional[str]] = mapped_column(String(256))
    macos_path: Mapped[Optional[str]] = mapped_column(String(256))

    def __init__(
        self,
        code: str = "",
        linux_path: str = "",
        windows_path: str = "",
        macos_path: str = "",
        **kwargs: Dict[str, Any],
    ) -> None:
        kwargs["code"] = code
        super(Repository, self).__init__(**kwargs)
        CodeMixin.__init__(self, **kwargs)

        self.linux_path = linux_path
        self.windows_path = windows_path
        self.macos_path = macos_path

    @validates("linux_path")
    def _validate_linux_path(self, key: str, linux_path: str) -> str:
        """Validate the given Linux path.

        Args:
            key (str): The name of the validated column.
            linux_path (str): The Linux path to validated.

        Raises:
            TypeError: If the given Linux path is not a str.

        Returns:
            str: The validated Linux path.
        """
        if not isinstance(linux_path, str):
            raise TypeError(
                f"{self.__class__.__name__}.linux_path should be an instance of "
                f"string, not {linux_path.__class__.__name__}: '{linux_path}'"
            )

        linux_path = os.path.normpath(linux_path) + "/"

        linux_path = linux_path.replace("\\", "/")

        if self.code is not None and platform.system() == "Linux":
            # update the environment variable
            os.environ[defaults.repo_env_var_template.format(code=self.code)] = (
                linux_path
            )

        return linux_path

    @validates("macos_path")
    def _validate_macos_path(self, key: str, macos_path: str) -> str:
        """Validate the given macOS path.

        Args:
            key (str): The name of the validated column.
            macos_path (str): The macOS path to validate.

        Raises:
            TypeError: If the given macOS path is not a str.

        Returns:
            str: The validated macOS path.
        """
        if not isinstance(macos_path, str):
            raise TypeError(
                f"{self.__class__.__name__}.macos_path should be an instance of "
                f"string, not {macos_path.__class__.__name__}: '{macos_path}'"
            )

        macos_path = os.path.normpath(macos_path) + "/"
        macos_path = macos_path.replace("\\", "/")
        if self.code is not None and platform.system() == "Darwin":
            # update the environment variable
            rendered_env_var = defaults.repo_env_var_template.format(code=self.code)
            os.environ[rendered_env_var] = macos_path

        return macos_path

    @validates("windows_path")
    def _validate_windows_path(self, key: str, windows_path: str) -> str:
        """Validate the given Windows path.

        Args:
            key (str): The name of the validated column.
            windows_path (str): The Windows path to validate.

        Raises:
            TypeError: If the given Windows path is not a str.

        Returns:
            str: The validated Windows path.
        """
        if not isinstance(windows_path, str):
            raise TypeError(
                f"{self.__class__.__name__}.windows_path should be an instance of "
                f"string, not {windows_path.__class__.__name__}: '{windows_path}'"
            )

        windows_path = os.path.normpath(windows_path)
        windows_path = windows_path.replace("\\", "/")

        if not windows_path.endswith("/"):
            windows_path += "/"

        if self.code is not None and platform.system() == "Windows":
            # update the environment variable
            os.environ[defaults.repo_env_var_template.format(code=self.code)] = (
                windows_path
            )

        return windows_path

    @property
    def path(self) -> str:
        """Return the repository path for the current OS.

        Returns:
            str: The repository path for the current OS.
        """
        # return the proper value according to the current os
        platform_system = platform.system()

        if platform_system == "Linux":
            return self.linux_path
        elif platform_system == "Windows":
            return self.windows_path
        elif platform_system == "Darwin":
            return self.macos_path

    @path.setter
    def path(self, path: str) -> None:
        """Set the path for the current OS.

        Args:
            path (str): The path.
        """
        # return the proper value according to the current os
        platform_system = platform.system()

        if platform_system == "Linux":
            self.linux_path = path
        elif platform_system == "Windows":
            self.windows_path = path
        elif platform_system == "Darwin":
            self.macos_path = path

    def is_in_repo(self, path: str) -> bool:
        """Return True or False depending on the given is in this repo or not.

        Args:
            path: The path to be investigated.

        Returns:
            bool: Return True if the given path is in this repository.
        """
        path = path.replace("\\", "/")
        return (
            path.lower().startswith(self.windows_path.lower())
            or path.startswith(self.linux_path)
            or path.startswith(self.macos_path)
        )

    def _to_path(self, path: str, replace_with: str) -> str:
        """Return the path replacing the OS related part with the given str.

        Args:
            path (str): The input path.
            replace_with (str): replace_with path

        Raises:
            TypeError: When the given path is not a str.

        Returns:
            str: The converted path.
        """
        if not isinstance(path, str):
            raise TypeError(
                "path should be a string containing a file path, "
                f"not {path.__class__.__name__}: '{path}'"
            )

        if not isinstance(replace_with, str):
            raise TypeError(
                "replace_with should be a string containing a file path, "
                f"not {replace_with.__class__.__name__}: '{replace_with}'"
            )

        # expand all variables
        path = os.path.normpath(os.path.expandvars(os.path.expanduser(path))).replace(
            "\\", "/"
        )

        if path.startswith(self.windows_path):
            return path.replace(self.windows_path, replace_with)
        elif path.startswith(self.linux_path):
            return path.replace(self.linux_path, replace_with)
        elif path.startswith(self.macos_path):
            return path.replace(self.macos_path, replace_with)

        return path

    def to_linux_path(self, path: str) -> str:
        """Return the Linux version of the given path.

        Args:
            path (str): The path that needs to be converted to Linux path.

        Returns:
            str: The Linux path.
        """
        return self._to_path(path, self.linux_path)

    def to_windows_path(self, path: str) -> str:
        """Return the Windows version of the given path.

        Args:
            path (str): The path that needs to be converted to windows path.

        Returns:
            str: The Windows path.
        """
        return self._to_path(path, self.windows_path)

    def to_macos_path(self, path: str) -> str:
        """Return the macOS version of the given path.

        Args:
            path (str): The path that needs to be converted to macOS path.

        Returns:
            str: The macOS path.
        """
        return self._to_path(path, self.macos_path)

    def to_native_path(self, path: str) -> str:
        """Return the native version of the given path.

        Args:
            path (str): The path that needs to be converted to native path.

        Returns:
            str: The native path.
        """
        return self._to_path(path, self.path)

    def make_relative(self, path: str) -> str:
        """Make the given path relative to the repository root.

        Args:
            path (str): The path to be made relative.

        Returns:
            str: The relative path.
        """
        path = self.to_native_path(path)
        return os.path.relpath(path, self.path).replace("\\", "/")

    @classmethod
    def find_repo(cls, path: str) -> "Repository":
        """Return the repository from the given path.

        Args:
            path (str): Path in a repository.

        Returns:
            Repository:
        """
        logger.debug(f"Looking for a repo for path: {path}")
        # path could be using environment variables so expand them
        path = os.path.expandvars(path)
        logger.debug(f"path after expanding vars  : {path}")

        # first find the repository
        repos = Repository.query.all()
        found_repo = None
        for repo in repos:
            if (
                path.startswith(repo.path)
                or path.lower().startswith(repo.windows_path.lower())
                or path.startswith(repo.linux_path)
                or path.startswith(repo.macos_path)
            ):
                found_repo = repo
                break

        if found_repo is None:
            logger.debug(f"Couldn't find a repo for path: {path}")

        return found_repo

    @classmethod
    def to_os_independent_path(cls, path: str) -> str:
        """Replace the part of the given path with repository environment var.

         This makes the given path OS independent.

        Args:
            path (str): path to make OS independent.

        Returns:
            str: OS independent path.
        """
        # find the related repo
        repo = cls.find_repo(path)

        if repo:
            logger.debug("Found repo for path: {}".format(repo))
            return "${}/{}".format(repo.env_var, repo.make_relative(path))
        else:
            logger.debug("Can't find repo for path: {}".format(path))
            return path

    @property
    def env_var(self) -> str:
        """Return the env var of this repo.

        Returns:
            str: The env_var corresponding to this repo.
        """
        return defaults.repo_env_var_template.format(code=self.code)

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is equal to this one as an Entity, is a
                Repository instance and has the same linux_path, macos_path,
                windows_path.
        """
        return (
            super(Repository, self).__eq__(other)
            and isinstance(other, Repository)
            and self.linux_path == other.linux_path
            and self.macos_path == other.macos_path
            and self.windows_path == other.windows_path
        )

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Repository, self).__hash__()


@event.listens_for(Repository, "after_insert")
def receive_after_insert(
    mapper: "Mapper",
    connection: "Connection",
    repo: "Repository",
) -> None:
    """Listen for the 'after_insert' event and update environment variables.

    This is a mapper event to update the environment variables with the newly inserted
    Repository data.

    Args:
        mapper (sqlalchemy.orm.Mapper): The mapper object.
        connection (sqlalchemy.engine.Connection): The connection object.
        repo (Repository): The Repository instance that is just inserted to the DB.
    """
    logger.debug("auto creating env var for Repository: {}".format(repo.name))
    os.environ[defaults.repo_env_var_template.format(code=repo.code)] = repo.path
