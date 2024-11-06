# -*- coding: utf-8 -*-
"""Project related classes and functions are situated here."""

from jinja2 import Template

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship, validates

from stalker import defaults
from stalker.db.declarative import Base
from stalker.log import get_logger
from stalker.models.entity import Entity
from stalker.models.mixins import CodeMixin, DateRangeMixin, ReferenceMixin, StatusMixin

logger = get_logger(__name__)


class ProjectRepository(Base):
    """The association object for Project to Repository instances."""

    __tablename__ = "Project_Repositories"

    project_id = Column(Integer, ForeignKey("Projects.id"), primary_key=True)

    project = relationship(
        "Project",
        back_populates="repositories_proxy",
        primaryjoin="Project.project_id==ProjectRepository.project_id",
    )

    repository_id = Column(Integer, ForeignKey("Repositories.id"), primary_key=True)

    repository = relationship(
        "Repository",
        primaryjoin="ProjectRepository.repository_id==Repository.repository_id",
    )

    position = Column(Integer)

    def __init__(self, project=None, repository=None, position=None):
        self.project = project
        self.repository = repository
        self.position = position

    @validates("project")
    def _validate_project(self, key, project):
        """Validate the given project value.

        Args:
            key (str): The name of the validated column.
            project (Project): The project value to be validated.

        Returns:
            project: The validated project value.
        """
        return project

    @validates("repository")
    def _validate_repository(self, key, repository):
        """Validate the given repository value.

        Args:
            key (str): The name of the validated column.
            repository (Repository): The repository to be validated.

        Raises:
            TypeError: If the repository is not a Repository instance.

        Returns:
            Repository: The repository value.
        """
        if repository is not None:
            from stalker.models.repository import Repository

            if not isinstance(repository, Repository):
                raise TypeError(
                    f"{self.__class__.__name__}.repositories should be a list of "
                    "stalker.models.repository.Repository instances or "
                    f"derivatives, not {repository.__class__.__name__}: '{repository}'"
                )

        return repository


class Project(Entity, ReferenceMixin, StatusMixin, DateRangeMixin, CodeMixin):
    """All the information about a Project in Stalker is hold in this class.

    Project is one of the main classes that will direct the others. A project
    in Stalker is a gathering point.

    It is mixed with :class:`.ReferenceMixin`, :class:`.StatusMixin`,
    :class:`.DateRangeMixin` and :class:`.CodeMixin` to give reference, status,
    schedule and code attribute. Please read the individual documentation of
    each of the mixins.

    **Project Users**

    The :attr:`.Project.users` attribute lists the users in this project. UIs
    like task creation for example will only list these users as available
    resources for this project.

    **TaskJuggler Integration**

    Stalker uses TaskJuggler for scheduling the project tasks. The
    :attr:`.Project.to_tjp` attribute generates a tjp compliant string which
    includes the project definition, the tasks of the project, the resources in
    the project including the vacation definitions and all the time logs
    recorded for the project.

    For custom attributes or directives that needs to be passed to TaskJuggler
    you can use the :attr:`.Project.custom_tjp` attribute which will be
    attached to the generated tjp file (inside the "project" directive).

    To manage all the studio projects at once (schedule them at once please use
    :class:`.Studio`).

    **Repositories**

    .. versionadded:: 0.2.13
       Multiple Repositories per Project

       Starting with v0.2.13 Project instances can have multiple Repositories,
       which allows the project files to be placed in more than one repository
       according to the need of the studio pipeline. One great advantage of
       having multiple repositories is to be able to place Published versions
       in to another repository which is placed on to a faster server.

       Also, the :attr:`.repositories` attribute is not a read-only attribute
       anymore.

    **Clients**

    .. versionadded:: 0.2.15
       Multiple Clients per Project

       It is now possible to attach multiple :class:`.Client` instances to one
       :class:`.Project` allowing to hold complex Projects to Client relations
       by using the :attr:`.ProjectClient.role` attribute of the
       :class:`.ProjectClient` class.

    **Deleting a Project**

    Deleting a :class:`.Project` instance will cascade the delete operation to
    all the :class:`.Task` s related to that particular Project and it will
    cascade the delete operation to :class:`.TimeLog` s, :class:`.Version` s,
    :class:`.Link` s and :class:`.Review` s etc.. So one can delete a
    :class:`.Project` instance without worrying about the non-project related
    data like :class:`.User` s or :class:`.Department` s to be deleted.

    Args:
        clients (List[Client]): The clients which the project is affiliated with.
            Default value is an empty list.

        image_format (ImageFormat): The output image format of the project. Default
            value is None.

        fps (float): The FPS of the project, it should be a integer or float number, or
            a string literal which can be correctly converted to a float. Default value
            is 25.0.

        type (Type): The type of the project. Default value is None.

        structure (Structure): The structure of the project. Default value is None.

        repositories (List[Repository]): A list of :class:`.Repository` instances that
            the project files are going to be stored in. You cannot create a project
            without specifying the repositories argument and passing a
            :class:`.Repository` to it. Default value is None which raises a TypeError.

        is_stereoscopic (bool): a bool value, showing if the project is going to be a
            stereo 3D project, anything given as the argument will be converted to True
            or False. Default value is False.

        users (List[User]): A list of :class:`.User` s holding the users in this
            project. This will create a reduced or grouped list of studio workers and
            will make it easier to define the resources for a Task related to this
            project. The default value is an empty list.
    """

    __auto_name__ = False
    __tablename__ = "Projects"
    project_id = Column("id", Integer, ForeignKey("Entities.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "Project",
        "inherit_condition": project_id == Entity.entity_id,
    }

    # TODO: Remove this attribute, because we have the statuses to control if a project
    #       is active or not.
    active = Column(Boolean, default=True)

    clients = association_proxy(
        "client_role", "client", creator=lambda n: ProjectClient(client=n)
    )

    client_role = relationship(
        "ProjectClient",
        back_populates="project",
        cascade="all, delete-orphan",
        cascade_backrefs=False,
        primaryjoin="Projects.c.id==Project_Clients.c.project_id",
    )

    tasks = relationship(
        "Task",
        primaryjoin="Tasks.c.project_id==Projects.c.id",
        uselist=True,
        cascade="all, delete-orphan",
    )

    users = association_proxy(
        "user_role", "user", creator=lambda n: ProjectUser(user=n)
    )

    user_role = relationship(
        "ProjectUser",
        back_populates="project",
        cascade="all, delete-orphan",
        cascade_backrefs=False,
        primaryjoin="Projects.c.id==Project_Users.c.project_id",
    )

    repositories_proxy = relationship(
        "ProjectRepository",
        back_populates="project",
        cascade="all, delete-orphan",
        cascade_backrefs=False,
        order_by="ProjectRepository.position",
        primaryjoin="Projects.c.id==Project_Repositories.c.project_id",
        collection_class=ordering_list("position"),
        doc="""The :class:`.Repository` that this project files should reside.

        Should be a list of :class:`.Repository` instances.
        """,
    )

    repositories = association_proxy(
        "repositories_proxy",
        "repository",
        creator=lambda n: ProjectRepository(repository=n),
    )

    structure_id = Column(Integer, ForeignKey("Structures.id"))
    structure = relationship(
        "Structure",
        primaryjoin="Project.structure_id==Structure.structure_id",
        doc="""The structure of the project. Should be an instance of
        :class:`.Structure` class""",
    )

    image_format_id = Column(Integer, ForeignKey("ImageFormats.id"))
    image_format = relationship(
        "ImageFormat",
        primaryjoin="Projects.c.image_format_id==ImageFormats.c.id",
        doc="""The :class:`.ImageFormat` of this project.

        This value defines the output image format of the project, should be an
        instance of :class:`.ImageFormat`.
        """,
    )

    fps = Column(
        Float(precision=3),
        doc="""The fps of the project.

        It is a float value, any other types will be converted to float. The
        default value is 25.0.
        """,
    )

    is_stereoscopic = Column(
        Boolean, doc="""True if the project is a stereoscopic project"""
    )

    tickets = relationship(
        "Ticket",
        primaryjoin="Tickets.c.project_id==Projects.c.id",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __init__(
        self,
        name=None,
        code=None,
        clients=None,
        repositories=None,
        structure=None,
        image_format=None,
        fps=25.0,
        is_stereoscopic=False,
        users=None,
        **kwargs,
    ):
        # a projects project should be self
        # initialize the project argument to self
        kwargs["project"] = self
        kwargs["name"] = name

        super(Project, self).__init__(**kwargs)
        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        DateRangeMixin.__init__(self, **kwargs)

        self.code = code

        if users is None:
            users = []
        self.users = users

        if repositories is None:
            repositories = []
        self.repositories = repositories

        self.structure = structure

        if clients is None:
            clients = []
        self.clients = clients

        self._sequences = []
        self._assets = []

        self.image_format = image_format
        self.fps = fps
        self.is_stereoscopic = bool(is_stereoscopic)

        self.active = True

    def __eq__(self, other):
        """Check the equality.

        Args:
            other (object): The other object.

        Returns:
            bool: True if the other object is a Project and equal as an Entity.
        """
        return super(Project, self).__eq__(other) and isinstance(other, Project)

    def __hash__(self):
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Project, self).__hash__()

    @validates("fps")
    def _validate_fps(self, key, fps):
        """Validate the given fps value.

        Args:
            key (str): The name of the validated column.
            fps (Union[int, float]): The fps value to be validated.

        Raises:
            TypeError: If the fps value is not an int or float.
            ValueError: If the fps is 0 or a negative number.

        Returns:
            float: The validated fps value.
        """
        if not isinstance(fps, (int, float)):
            raise TypeError(
                f"{self.__class__.__name__}.fps should be a positive float or int, "
                f"not {fps.__class__.__name__}: '{fps}'"
            )

        fps = float(fps)
        if fps <= 0:
            raise ValueError(
                f"{self.__class__.__name__}.fps should be a positive float or int, "
                f"not {fps}"
            )
        return float(fps)

    @validates("image_format")
    def _validate_image_format(self, key, image_format):
        """Validate the given image format.

        Args:
            key (str): The name of the validated column.
            image_format (ImageFormat): The image_format value to be validated.

        Raises:
            TypeError: If the given image format is not a ImageFormat instance.

        Returns:
            ImageFormat: The validated image_format value.
        """
        from stalker.models.format import ImageFormat

        if image_format is not None and not isinstance(image_format, ImageFormat):
            raise TypeError(
                f"{self.__class__.__name__}.image_format should be an instance of "
                "stalker.models.format.ImageFormat, "
                f"not {image_format.__class__.__name__}: '{image_format}'"
            )
        return image_format

    @validates("structure")
    def _validate_structure(self, key, structure):
        """Validate the given structure value.

        Args:
            key (str): The name of the validated column.
            structure (Structure): The structure to be validated.

        Raises:
            TypeError: If the given structure is not a Structure instance.

        Returns:
            Structure: The validated Structure value.
        """
        from stalker.models.structure import Structure

        if structure is not None:
            if not isinstance(structure, Structure):
                raise TypeError(
                    "{}.structure should be an instance of "
                    "stalker.models.structure.Structure, not {}: '{}'".format(
                        self.__class__.__name__, structure.__class__.__name__, structure
                    )
                )
        return structure

    @validates("is_stereoscopic")
    def _validate_is_stereoscopic(self, key, is_stereoscopic):
        """Validate the is_stereoscopic value.

        Args:
            key (str): The name of the validated column.
            is_stereoscopic (bool): The is_stereoscopic value to be validated.

        Returns:
            bool: The bool representation of the is_stereoscopic value.
        """
        return bool(is_stereoscopic)

    @property
    def root_tasks(self):
        """Return a list of Tasks which have no parents.

        Returns:
            List[Task]: The list of root :class:`Task`s in this project.
        """
        from stalker import Task
        from stalker.db.session import DBSession

        # TODO: add a fallback method
        with DBSession.no_autoflush:
            return (
                Task.query.filter(Task.project == self)
                .filter(Task.parent == None)  # noqa: E711
                .all()
            )

    @property
    def assets(self):
        """Return the assets in this project.

        Returns:
            List[Asset]: The list of :class:`Asset`s in this project.
        """
        from stalker.models.asset import Asset
        from stalker.db.session import DBSession

        # TODO: add a fallback method
        with DBSession.no_autoflush:
            return Asset.query.filter(Asset.project == self).all()

    @property
    def sequences(self):
        """Return the sequences in this project.

        Returns:
            List[Sequence]: List of :class:`Sequence`s in this project.
        """
        # sequences are tasks, use self.tasks
        from stalker.models.sequence import Sequence

        return Sequence.query.filter(Sequence.project == self).all()

    @property
    def shots(self):
        """Return the shots in this project.

        Returns:
            List[Shot]: List of :class:`Shot`s in this project.
        """
        # shots are tasks, use self.tasks
        from stalker.models.shot import Shot

        return Shot.query.filter(Shot.project == self).all()

    @property
    def to_tjp(self):
        """Return the TaskJuggler compatible representation of this project.

        Returns:
            str: The TaskJuggler compatible representation of this project.
        """
        temp = Template(
            defaults.tjp_project_template, trim_blocks=True, lstrip_blocks=True
        )
        return temp.render({"project": self})

    @property
    def is_active(self):
        """Return True if this project is active, False otherwise.

        This is a predicate for `Project.active` attribute.

        Returns:
            bool: True if the project is active, False otherwise.
        """
        return self.active

    @property
    def total_logged_seconds(self):
        """Return the total TimeLog seconds recorded in child tasks.

        Returns:
            int: The total amount of logged seconds in the child tasks.
        """
        total_logged_seconds = 0
        for task in self.root_tasks:
            total_logged_seconds += task.total_logged_seconds
        logger.debug(f"project.total_logged_seconds: {total_logged_seconds}")
        return total_logged_seconds

    @property
    def schedule_seconds(self):
        """Return the total amount of schedule timing of the child tasks in seconds.

        Returns:
            int: The total amount of schedule timing of the child tasks in seconds.
        """
        schedule_seconds = 0
        for task in self.root_tasks:
            schedule_seconds += task.schedule_seconds
        logger.debug(f"project.schedule_seconds: {schedule_seconds}")
        return schedule_seconds

    @property
    def percent_complete(self):
        """Return the percent_complete value.

        The percent_complete value is based on the total_logged_seconds and
        schedule_seconds of the root tasks.

        Returns:
            float: The percent_complete value.
        """
        total_logged_seconds = self.total_logged_seconds
        schedule_seconds = self.schedule_seconds
        if schedule_seconds > 0:
            return total_logged_seconds / schedule_seconds * 100
        else:
            return 0

    @property
    def open_tickets(self):
        """Return the list of open :class:`.Ticket` s in this project.

        Returns:
             List[Ticket]: A list of :class:`.Ticket` instances which has a status of
                `Open` and created in this project.
        """
        from stalker import Ticket, Status

        return (
            Ticket.query.join(Status, Ticket.status)
            .filter(Ticket.project == self)
            .filter(Status.code != "CLS")
            .all()
        )

    @property
    def repository(self):
        """Return the first repository in the `project.repositories` or None.

        Compatibility attribute for pre v0.2.13 systems.

        Returns:
            Union[None, Repository]: The Repository instance if there are any or None.
        """
        if self.repositories:
            return self.repositories[0]
        else:
            return None


class ProjectUser(Base):
    """The association object used in User-to-Project relation."""

    __tablename__ = "Project_Users"

    user_id = Column("user_id", Integer, ForeignKey("Users.id"), primary_key=True)

    user = relationship(
        "User",
        back_populates="project_role",
        cascade_backrefs=False,
        primaryjoin="ProjectUser.user_id==User.user_id",
    )

    project_id = Column(
        "project_id", Integer, ForeignKey("Projects.id"), primary_key=True
    )

    project = relationship(
        "Project",
        back_populates="user_role",
        cascade_backrefs=False,
        primaryjoin="ProjectUser.project_id==Project.project_id",
    )

    role_id = Column("rid", Integer, ForeignKey("Roles.id"), nullable=True)

    role = relationship(
        "Role", cascade_backrefs=False, primaryjoin="ProjectUser.role_id==Role.role_id"
    )

    rate = Column(Float, default=0.0)

    def __init__(self, project=None, user=None, role=None):
        self.user = user
        self.project = project
        self.role = role
        if self.user:
            # don't need to validate rate
            # as it is already validated on the User side
            self.rate = user.rate

    @validates("user")
    def _validate_user(self, key, user):
        """Validate the given user value.

        Args:
            key (str): The name of the validated column.
            user (User): The user value to be validated.

        Raises:
            TypeError: If the given user is not a User instance.

        Returns:
            User: The validated user value.
        """
        if user is not None:
            from stalker.models.auth import User

            if not isinstance(user, User):
                raise TypeError(
                    f"{self.__class__.__name__}.user should be a "
                    "stalker.models.auth.User instance, "
                    f"not {user.__class__.__name__}: '{user}'"
                )

            # also update rate attribute
            from stalker.db.session import DBSession

            with DBSession.no_autoflush:
                self.rate = user.rate

        return user

    @validates("project")
    def _validate_project(self, key, project):
        """Validate the given project value.

        Args:
            key (str): The name of the validated column.
            project (Project): The project value to be validated.

        Raises:
            TypeError: If the project is not a Project instance.

        Returns:
            Project: The validated project value.
        """
        if project is not None:
            # check if it is instance of Project object
            if not isinstance(project, Project):
                raise TypeError(
                    f"{self.__class__.__name__}.project should be a "
                    "stalker.models.project.Project instance, "
                    f"not {project.__class__.__name__}: '{project}'"
                )
        return project

    @validates("role")
    def _validate_role(self, key, role):
        """Validate the given role instance.

        Args:
            key (str): The name of the validated column.
            role (Role): The role value to be validated.

        Raises:
            TypeError: If the given role is not a Role instance.

        Returns:
            Role: The validated role value.
        """
        if role is not None:
            from stalker import Role

            if not isinstance(role, Role):
                raise TypeError(
                    f"{self.__class__.__name__}.role should be a "
                    "stalker.models.auth.Role instance, "
                    f"not {role.__class__.__name__}: '{role}'"
                )
        return role


class ProjectClient(Base):
    """The association object used in Client-to-Project relation.

    Args:
        project (Project): The project.
        client (Client): The client.
        role (Role): The client role in this project.
    """

    __tablename__ = "Project_Clients"

    client_id = Column("client_id", Integer, ForeignKey("Clients.id"), primary_key=True)

    client = relationship(
        "Client",
        back_populates="project_role",
        cascade_backrefs=False,
        primaryjoin="Project_Clients.c.client_id==Clients.c.id",
    )

    project_id = Column(
        "project_id", Integer, ForeignKey("Projects.id"), primary_key=True
    )

    project = relationship(
        "Project",
        back_populates="client_role",
        cascade_backrefs=False,
        primaryjoin="ProjectClient.project_id==Project.project_id",
    )

    role_id = Column("rid", Integer, ForeignKey("Roles.id"), nullable=True)

    role = relationship(
        "Role",
        cascade_backrefs=False,
        primaryjoin="ProjectClient.role_id==Role.role_id",
    )

    def __init__(self, project=None, client=None, role=None):
        self.client = client
        self.project = project
        self.role = role

    @validates("client")
    def _validate_client(self, key, client):
        """Validate the given client value.

        Args:
            key (str): The name of the validated column.
            client (Client): The client value to be validated.

        Raises:
            TypeError: If the given client arg value is not a Client instance.

        Returns:
            Client: The validated client value.
        """
        if client is not None:
            from stalker.models.client import Client

            if not isinstance(client, Client):
                raise TypeError(
                    f"{self.__class__.__name__}.client should be an instance of "
                    "stalker.models.auth.Client, "
                    f"not {client.__class__.__name__}: '{client}'"
                )
        return client

    @validates("project")
    def _validate_project(self, key, project):
        """Validate the given project value.

        Args:
            key (str): The name of the validated column.
            project (Project): The project value to be validated.

        Raises:
            TypeError: If the given project value is not a Project instance.

        Returns:
            Project: The validated project value.
        """
        if project is not None:
            # check if it is instance of Project object
            if not isinstance(project, Project):
                raise TypeError(
                    f"{self.__class__.__name__}.project should be a "
                    "stalker.models.project.Project instance, "
                    f"not {project.__class__.__name__}: '{project}'"
                )
        return project

    @validates("role")
    def _validate_role(self, key, role):
        """Validate the given role instance.

        Args:
            key (str): The name of the validated column.
            role (Role): The role value to be validated.

        Raises:
            TypeError: If the given role value is not a Role instance.

        Returns:
            Role: The validated role value.
        """
        if role is not None:
            from stalker import Role

            if not isinstance(role, Role):
                raise TypeError(
                    f"{self.__class__.__name__}.role should be a "
                    "stalker.models.auth.Role instance, "
                    f"not {role.__class__.__name__}: '{role}'"
                )
        return role


def create_project_client(project):
    """Create ProjectClient instance on association proxy.

    Args:
        project (Project): The :class:`.Project` instance to be used to create the
            :class:`.ProjectClient` instance.

    Returns:
        ProjectClient: The :class:`.ProjectClient` instance.
    """
    return ProjectClient(project=project)
