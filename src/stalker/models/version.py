# -*- coding: utf-8 -*-
"""Version related functions and classes are situated here."""

import os
import re
from typing import Generator, List, Union

import jinja2

from six import string_types

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.exc import OperationalError, UnboundExecutionError
from sqlalchemy.orm import relationship, validates

from stalker.db.declarative import Base
from stalker.db.session import DBSession
from stalker.log import get_logger
from stalker.models.link import Link
from stalker.models.mixins import DAGMixin
from stalker.models.task import Task
from stalker.utils import walk_hierarchy


logger = get_logger(__name__)


class Version(Link, DAGMixin):
    """Holds information about the created versions (files) for a class:`.Task`.

    A :class:`.Version` holds information about the
    created files related to a class:`.Task`. So if one
    creates a new version for a file or a sequences of file for a
    :class:`.Task` then the information is hold in the
    :class:`.Version` instance.

    .. versionadded: 0.2.13

       After Stalker 0.2.13 the :attr:`.path` become an absolute path which is
       not anymore merged with the project repository in anyway.

    .. warning:

       For projects those are created prior to Stalker version 0.2.13 and that
       has a :class:`.Structure` with :class:`.FilenameTemplate` that doesn't
       include the repository info, it is suggested to update the related
       ``FilenameTemplate`` s to include a the repository info manually.

       Example:
         pre 0.2.13 setup:

         FilenameTemplate with path attribute is set to:

           {{project.code}}/{%- for parent_task in parent_tasks -%}{{parent_task.nice_name}}/{%- endfor -%}

         Update to:

           {{project.repository.path}}/{{project.code}}/{%- for parent_task in parent_tasks -%}{{parent_task.nice_name}}/{%- endfor -%}

         Or, lets have a setup with environment variables:

           $REPO{{project.repository.id}}/{{project.code}}/{%- for parent_task in parent_tasks -%}{{parent_task.nice_name}}/{%- endfor -%}

    Args:
        take_name (str): A short string holding the current take name. Takes in Stalker
            are used solely for grouping individual versions together. Versions with the
            same ``take_name`` (of the same Task) are numbered together. It can be any
            alphanumeric value (a-zA-Z0-9_). The default is the string "Main". When
            skipped it will use the default value. It can not start with a number. It
            can not have white spaces.
        inputs (List[Link]): A list o :class:`.Link` instances, holding the inputs of
            the current version. It could be a texture for a Maya file or an image
            sequence for Nuke, or anything those you can think as the input for the
            current Version.
        outputs (List[Link]): A list of :class:`.Link` instances, holding the outputs of
            the current version. It could be the rendered image sequences out of Maya or
            Nuke, or it can be a Targa file which is the output of a Photoshop file, or
            anything that you can think as the output which is created out of this
            Version.
        task (Task): A :class:`.Task` instance showing the owner of this Version.
        parent (Version): A :class:`.Version` instance which is the parent of this
            Version. It is mainly used to see which Version is derived from which in the
            Version history of a :class:`.Task`.
    """  # noqa: B950

    from stalker import defaults

    __auto_name__ = True
    __tablename__ = "Versions"
    __mapper_args__ = {"polymorphic_identity": "Version"}

    __dag_cascade__ = "save-update, merge"

    version_id = Column("id", Integer, ForeignKey("Links.id"), primary_key=True)

    __id_column__ = "version_id"

    task_id = Column(Integer, ForeignKey("Tasks.id"), nullable=False)
    task = relationship(
        "Task",
        primaryjoin="Versions.c.task_id==Tasks.c.id",
        doc="""The :class:`.Task` instance that this Version is created for.
        """,
        uselist=False,
        back_populates="versions",
    )

    take_name = Column(
        String(256),
        default=defaults.version_take_name,
        doc="""Takes in Versions are used solely for grouping individual
        versions together.""",
    )

    version_number = Column(
        Integer,
        default=1,
        nullable=False,
        doc="""The :attr:`.version_number` attribute is read-only.
        Trying to change it will produce an AttributeError.
        """,
    )

    inputs = relationship(
        "Link",
        secondary="Version_Inputs",
        primaryjoin="Versions.c.id==Version_Inputs.c.version_id",
        secondaryjoin="Version_Inputs.c.link_id==Links.c.id",
        doc="""The inputs of the current version.

        It is a list of :class:`.Link` instances.
        """,
    )

    outputs = relationship(
        "Link",
        secondary="Version_Outputs",
        primaryjoin="Versions.c.id==Version_Outputs.c.version_id",
        secondaryjoin="Version_Outputs.c.link_id==Links.c.id",
        doc="""The outputs of the current version.

        It is a list of :class:`.Link` instances.
        """,
    )

    is_published = Column(Boolean, default=False)

    created_with = Column(String(256))

    def __init__(
        self,
        task=None,
        take_name=defaults.version_take_name,
        inputs=None,
        outputs=None,
        parent=None,
        full_path=None,
        created_with=None,
        **kwargs,
    ):
        # call supers __init__
        kwargs["full_path"] = full_path
        super(Version, self).__init__(**kwargs)

        DAGMixin.__init__(self, parent=parent)

        self.take_name = take_name
        self.task = task
        self.version_number = None
        if inputs is None:
            inputs = []

        if outputs is None:
            outputs = []

        self.inputs = inputs
        self.outputs = outputs

        self.is_published = False

        self.created_with = created_with

    def __repr__(self) -> str:
        """Return the str representation of the Version.

        Returns:
            str: The string representation of this Version instance.
        """
        return (
            "<{project_code}_{nice_name}_v{version_number:03d} ({entity_type})>".format(
                project_code=self.task.project.code,
                nice_name=self.nice_name,
                version_number=self.version_number,
                entity_type=self.entity_type,
            )
        )

    @classmethod
    def _format_take_name(cls, take_name: str) -> str:
        """Format the given take_name value.

        Args:
            take_name (str): The take name value to be formatted.

        Returns:
            str: The formatted take name value.
        """
        # remove unnecessary characters
        take_name = re.sub(r"([^a-zA-Z0-9\s_\-@]+)", r"", take_name).strip()

        # replace empty spaces with underscores
        take_name = re.sub(r"[\s]+", "_", take_name)

        # replace multiple underscores with only one
        # take_name = re.sub(r'([_]+)', r'_', take_name)

        # remove any non allowed characters from the start
        take_name = re.sub(r"^[^a-zA-Z0-9]+", r"", take_name)

        return take_name

    @validates("take_name")
    def _validate_take_name(self, key: str, take_name: str) -> str:
        """Validate the given take_name value.

        Args:
            key (str): The name of the validated column.
            take_name (str): The take name value to be validated.

        Raises:
            TypeError: If the take name value is not a string.
            ValueError: If the take name value is an empty string.

        Returns:
            str: The validated take name value.
        """
        if not isinstance(take_name, string_types):
            raise TypeError(
                "{}.take_name should be a string, not {}: '{}'".format(
                    self.__class__.__name__, take_name.__class__.__name__, take_name
                )
            )

        take_name = self._format_take_name(take_name)

        if take_name == "":
            raise ValueError(
                f"{self.__class__.__name__}.take_name can not be an empty string"
            )

        return take_name

    @property
    def latest_version(self) -> "Version":
        """Return the Version instance with the highest version number in this series.

        Returns:
            Version: The :class:`.Version` instance with the highest version number in
                this version series.
        """
        try:
            with DBSession.no_autoflush:
                last_version = (
                    Version.query.filter(Version.task == self.task)
                    .filter(Version.take_name == self.take_name)
                    .order_by(Version.version_number.desc())
                    .first()
                )
        except (UnboundExecutionError, OperationalError):
            all_versions = sorted(
                self.task.versions,
                key=lambda x: x.version_number if x.version_number else -1,
            )
            if all_versions:
                last_version = all_versions[-1]
                if last_version != self:
                    return last_version
                else:
                    return 0
            else:
                last_version = None
        return last_version

    @property
    def max_version_number(self) -> int:
        """Return the maximum version number for this Version.

        Returns:
            int: The maximum version number for this Version.
        """
        latest_version = self.latest_version

        if latest_version:
            return latest_version.version_number

        return 0

    @validates("version_number")
    def _validate_version_number(self, key: str, version_number: int) -> int:
        """Validate the given version_number value.

        Args:
            key (str): The name of the validated column.
            version_number (int): The version number to be validated.

        Returns:
            int: The validated version number.
        """
        # get the latest version
        latest_version = self.latest_version

        max_version_number = 0
        if latest_version:
            max_version_number = latest_version.version_number

        logger.debug(f"max_version_number: {max_version_number}")
        logger.debug(f"given version_number: {version_number}")

        if version_number is None or version_number <= max_version_number:
            if latest_version == self:
                version_number = latest_version.version_number
                logger.debug(
                    "the version is the latest version in database, the "
                    f"number will not be changed from {version_number}"
                )
            else:
                version_number = max_version_number + 1
                logger.debug(
                    "given Version.version_number is too low,"
                    f"max version_number in the database is {max_version_number}, "
                    f"setting the current version_number to {version_number}"
                )

        return version_number

    @validates("task")
    def _validate_task(self, key, task) -> Task:
        """Validate the given task value.

        Args:
            key (str): The name of the validated column.
            task (Task): The task value to be validated.

        Raises:
            TypeError: If the task value is not a :class:`.Task` instance.

        Returns:
            Task: The validated :class:`.Task` instance.
        """
        if task is None:
            raise TypeError("{}.task can not be None".format(self.__class__.__name__))

        if not isinstance(task, Task):
            raise TypeError(
                "{}.task should be a stalker.models.task.Task instance, "
                "not {}: '{}'".format(
                    self.__class__.__name__, task.__class__.__name__, task
                )
            )

        return task

    @validates("inputs")
    def _validate_inputs(self, key, input_):
        """Validate the given input value.

        Args:
            key (str): The name of the validated column.
            input_ (Link): The input value to be validated.

        Raises:
            TypeError: If the input is not a :class:`.Link` instance.

        Returns:
            Link: The validated input value.
        """
        if not isinstance(input_, Link):
            raise TypeError(
                "All elements in {}.inputs should be all "
                "stalker.models.link.Link instances, not {}: '{}'".format(
                    self.__class__.__name__, input_.__class__.__name__, input_
                )
            )

        return input_

    @validates("outputs")
    def _validate_outputs(self, key, output) -> Link:
        """Validate the given output value.

        Args:
            key (str): The name of the validated column.
            output (Link): The output value to be validated.

        Raises:
            TypeError: If the output is not a :class:`.Link` instance.

        Returns:
            Link: The validated output value.
        """
        if not isinstance(output, Link):
            raise TypeError(
                "All elements in {}.outputs should be all "
                "stalker.models.link.Link instances, not {}: '{}'".format(
                    self.__class__.__name__, output.__class__.__name__, output
                )
            )

        return output

    def _template_variables(self) -> dict:
        """Return the variables used in rendering the filename template.

        Returns:
            dict: The template variables.
        """
        from stalker import Shot

        sequences = []
        scenes = []
        if isinstance(self.task, Shot):
            sequences = self.task.sequences
            scenes = self.task.scenes

        # get the parent tasks
        task = self.task
        parent_tasks = task.parents
        parent_tasks.append(task)

        return {
            "project": self.task.project,
            "sequences": sequences,
            "scenes": scenes,
            "sequence": self.task,
            "shot": self.task,
            "asset": self.task,
            "task": self.task,
            "parent_tasks": parent_tasks,
            "version": self,
            "type": self.type,
            "extension": self.extension,
        }

    def update_paths(self) -> None:
        """Update the path variables.

        Raises:
            RuntimeError: If no Version related FilenameTemplate is found in the related
                Project.structure.
        """
        kwargs = self._template_variables()

        # get a suitable FilenameTemplate
        structure = self.task.project.structure

        vers_template = None
        if structure:
            for template in structure.templates:
                if template.target_entity_type == self.task.entity_type:
                    vers_template = template
                    break

        if not vers_template:
            raise RuntimeError(
                "There are no suitable FilenameTemplate "
                "(target_entity_type == '{entity_type}') defined in the Structure of "
                "the related Project instance, please create a new "
                "stalker.models.template.FilenameTemplate instance with its "
                "'target_entity_type' attribute is set to '{entity_type}' and assign "
                "it to the `templates` attribute of the structure of the "
                "project".format(entity_type=self.task.entity_type)
            )

        temp_filename = jinja2.Template(vers_template.filename).render(**kwargs)
        if not isinstance(temp_filename, string_types):
            temp_filename = temp_filename.encode("utf-8")

        temp_path = jinja2.Template(vers_template.path).render(**kwargs)
        if not isinstance(temp_path, string_types):
            temp_path = temp_path.encode("utf-8")

        self.filename = temp_filename
        self.path = temp_path

    @property
    def absolute_full_path(self) -> str:
        """Return the absolute full path of this version.

        This absolute full path includes the repository path of the related project.

        Returns:
            str: The absolute full path of this Version instance.
        """
        return os.path.normpath(os.path.expandvars(self.full_path)).replace("\\", "/")

    @property
    def absolute_path(self) -> str:
        """Return the absolute path.

        Returns:
            str: The absolute path.
        """
        return os.path.normpath(os.path.expandvars(self.path)).replace("\\", "/")

    def is_latest_published_version(self) -> bool:
        """Return True if this is the latest published Version False otherwise.

        Returns:
            bool: True if this is the latest published Version, False otherwise.
        """
        if not self.is_published:
            return False

        return self == self.latest_published_version

    @property
    def latest_published_version(self) -> "Version":
        """Return the last published version.

        Returns:
            Version: The last published Version instance.
        """
        return (
            Version.query.filter_by(task=self.task)
            .filter_by(take_name=self.take_name)
            .filter_by(is_published=True)
            .order_by(Version.version_number.desc())
            .first()
        )

    @validates("created_with")
    def _validate_created_with(
        self, key: str, created_with: Union[None, str]
    ) -> Union[None, str]:
        """Validate the given created_with value.

        Args:
            key (str): The name of the validated column.
            created_with (str): The name of the DCC used to create this Version
                instance.

        Raises:
            TypeError: If the given created_with attribute is not None and not a string.

        Returns:
            Union[None, str]: The validated created with value.
        """
        if created_with is not None and not isinstance(created_with, string_types):
            raise TypeError(
                "{}.created_with should be an instance of str, not {}: '{}'".format(
                    self.__class__.__name__,
                    created_with.__class__.__name__,
                    created_with,
                )
            )
        return created_with

    def __eq__(self, other):
        """Check the equality.

        Args:
            other (object): The other object.

        Returns:
            bool: True if the other object is equal to this one as an Entity, is a
                Version instance, has the same task, same take_name and same
                version_number.
        """
        return (
            super(Version, self).__eq__(other)
            and isinstance(other, Version)
            and self.task == other.task
            and self.take_name == other.take_name
            and self.version_number == other.version_number
        )

    def __hash__(self):
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Version, self).__hash__()

    @property
    def naming_parents(self) -> List[Task]:
        """Return a list of parents starting from the nearest Asset, Shot or Sequence.

        Returns:
            List[Task]: List of naming parents.
        """
        # find a Asset, Shot or Sequence, and store it as the significant
        # parent, and name the task starting from that entity
        all_parents = self.task.parents
        all_parents.append(self.task)
        naming_parents = []
        if all_parents:
            significant_parent = all_parents[0]

            for parent in reversed(all_parents):
                if parent.entity_type in ["Asset", "Shot", "Sequence"]:
                    significant_parent = parent
                    break

            # now start from that parent towards the task
            past_significant_parent = False
            naming_parents = []
            for parent in all_parents:
                if parent is significant_parent:
                    past_significant_parent = True
                if past_significant_parent:
                    naming_parents.append(parent)
        return naming_parents

    @property
    def nice_name(self) -> str:
        """Override the nice name method for Version class.

        Returns:
            str: The nice name.
        """
        naming_parents = self.naming_parents
        return self._format_nice_name(
            "{}_{}".format(
                "_".join(map(lambda x: x.nice_name, naming_parents)), self.take_name
            )
        )

    def walk_inputs(self, method: int = 0) -> Generator[None, "Version", None]:
        """Walk the inputs of this version instance.

        Args:
            method (int): The walk method, 0=Depth First, 1=Breadth First.

        Yields:
            Version: Yield the Version instances.
        """
        for v in walk_hierarchy(self, "inputs", method=method):
            yield v


# VERSION INPUTS
Version_Inputs = Table(
    "Version_Inputs",
    Base.metadata,
    Column("version_id", Integer, ForeignKey("Versions.id"), primary_key=True),
    Column(
        "link_id",
        Integer,
        ForeignKey("Links.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)

# VERSION_OUTPUTS
Version_Outputs = Table(
    "Version_Outputs",
    Base.metadata,
    Column("version_id", Integer, ForeignKey("Versions.id"), primary_key=True),
    Column("link_id", Integer, ForeignKey("Links.id"), primary_key=True),
)