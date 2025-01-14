# -*- coding: utf-8 -*-
"""Structure related functions and classes are situated here."""
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import Column, ForeignKey, Integer, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from stalker.db.declarative import Base
from stalker.log import get_logger
from stalker.models.entity import Entity
from stalker.models.template import FilenameTemplate

logger = get_logger(__name__)


class Structure(Entity):
    """Defines folder structures for :class:`.Projects`.

    Structures are generally owned by :class:`.Project` objects. Whenever a
    :class:`.Project` is physically created, project folders are created by
    looking at :attr:`.Structure.custom_template` of the :class:`.Structure`,
    the :class:`.Project` object is generally given to the :class:`.Structure`.
    So it is possible to use a variable like "{{project}}" or derived variables
    like::

      {% for seq in project.sequences %}
          {{do something here}}

    Every line of this rendered template will represent a folder and Stalker
    will create these folders on the attached :class:`.Repository`.

    Args:
        templates (List[FilenameTemplate]): A list of :class:`.FilenameTemplate`
            instances which defines a specific template for the given
            :attr:`.FilenameTemplate.target_entity_type` values.

        custom_template (str): A string containing several lines of folder
            names. The folders are relative to the :class:`.Project` root. It
            can also contain a Jinja2 Template code. Which will be rendered to
            show the list of folders to be created with the project. The Jinja2
            Template is going to have the {{project}} variable. The important
            point to be careful about is to list all the custom folders of the
            project in a new line in this string. For example a
            :class:`.Structure` for a :class:`.Project` can have the following
            :attr:`.Structure.custom_template`::

            .. code-block:: Jinja

                ASSETS
                {% for asset in project.assets %}
                    {% set asset_root = 'ASSETS/' + asset.code %}
                    {{asset_root}}

                    {% for task in asset.tasks %}
                        {% set task_root = asset_root + '/' + task.code %}
                        {{task_root}}

                SEQUENCES
                {% for seq in project.sequences %}}
                    {% set seq_root = 'SEQUENCES/' + {{seq.code}} %}
                    {{seq_root}}/Edit
                    {{seq_root}}/Edit/Export
                    {{seq_root}}/Storyboard

                    {% for shot in seq.shots %}
                        {% set shot_root = seq_root + '/SHOTS/' + shot.code %}
                        {{shot_root}}

                        {% for task in shot.tasks %}
                            {% set task_root = shot_root + '/' + task.code %}
                            {{task_root}}

            The above example has gone far beyond deep than it is needed, where
            it started to define paths for :class:`.Asset` s. Even it is
            possible to create a :class:`.Project` structure like that, in
            general it is unnecessary. Because the above folders are going to
            be created but they are probably going to be empty for a while,
            because the :class:`.Asset` s are not created yet (or in fact no
            :class:`.Version` instances are created for the :class:`.Task` s).
            Anyway, it is much suitable and desired to create this details by
            using :class:`.FilenameTemplate` objects. Which are specific to
            certain :attr:`.FilenameTemplate.target_entity_type` s. And by
            using the :attr:`.Structure.custom_template` attribute, Stalker
            cannot place any source or output file of a :class:`.Version` in
            the :class:`.Repository` where as it can by using
            :class:`.FilenameTemplate` s.

            But for certain types of :class:`.Task` s it is may be good to
            previously create the folder structure just because in certain
            environments (programs) it is not possible to run a Python code
            that will place the file in to the Repository like in Photoshop.

            The ``custom_template`` parameter can be None or an empty string if
            it is not needed.

            A :class:`.Structure` cannot be created without a ``type``
            (__strictly_typed__ = True). By giving a ``type`` to the
            :class:`.Structure`, you can create one structure for
            **Commercials** and another project structure for **Movies** and
            another one for **Print** projects etc. and can reuse them with new
            :class:`.Project` s.
    """

    # __strictly_typed__ = True
    __auto_name__ = False
    __tablename__ = "Structures"
    __mapper_args__ = {"polymorphic_identity": "Structure"}

    structure_id: Mapped[int] = mapped_column(
        "id",
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    templates: Mapped[Optional[List[FilenameTemplate]]] = relationship(
        secondary="Structure_FilenameTemplates"
    )

    custom_template: Mapped[Optional[str]] = mapped_column("custom_template", Text)

    def __init__(
        self,
        templates: Optional[List[FilenameTemplate]] = None,
        custom_template: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        super(Structure, self).__init__(**kwargs)

        if templates is None:
            templates = []

        self.templates = templates
        self.custom_template = custom_template

    def __eq__(self, other: Any) -> bool:
        """Check the equality.

        Args:
            other (Any): The other object.

        Returns:
            bool: True if the other object is a Structure instance and has the same
                templates, custom_template.
        """
        return (
            super(Structure, self).__eq__(other)
            and isinstance(other, Structure)
            and self.templates == other.templates
            and self.custom_template == other.custom_template
        )

    def __hash__(self) -> int:
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Structure, self).__hash__()

    @validates("custom_template")
    def _validate_custom_template(
        self, key: str, custom_template: Union[None, str]
    ) -> str:
        """Validate the given custom_template value.

        Args:
            key (str): The name of the validated column.
            custom_template (Union[None, str]): The custom template value to be
                validated.

        Raises:
            TypeError: If the given custom_template value is not a str.

        Returns:
            str: The validated `custom_template` value.
        """
        if custom_template is None:
            custom_template = ""

        if not isinstance(custom_template, str):
            raise TypeError(
                "{}.custom_template should be a string, not {}: '{}'".format(
                    self.__class__.__name__,
                    custom_template.__class__.__name__,
                    custom_template,
                )
            )
        return custom_template

    @validates("templates")
    def _validate_templates(
        self, key: str, template: FilenameTemplate
    ) -> FilenameTemplate:
        """Validate the given template value.

        Args:
            key (str): The name of the validated column.
            template (FilenameTemplate): The validated template value.

        Raises:
            TypeError: If the given template value is not a FilenameTemplate
                instance.

        Returns:
            FilenameTemplate: Return the validated template value.
        """
        if not isinstance(template, FilenameTemplate):
            raise TypeError(
                f"{self.__class__.__name__}.templates should only contain "
                "instances of stalker.models.template.FilenameTemplate, "
                f"not {template.__class__.__name__}: '{template}'"
            )

        return template


# Structure_FilenameTemplates Table
Structure_FilenameTemplates = Table(
    "Structure_FilenameTemplates",
    Base.metadata,
    Column("structure_id", Integer, ForeignKey("Structures.id"), primary_key=True),
    Column(
        "filenametemplate_id",
        Integer,
        ForeignKey("FilenameTemplates.id"),
        primary_key=True,
    ),
)
