# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, validates
from stalker import User
from stalker.db.session import DBSession
from stalker.models.entity import TaskableEntity
from stalker.models.mixins import StatusMixin, ScheduleMixin, ReferenceMixin

class Project(TaskableEntity, ReferenceMixin, StatusMixin, ScheduleMixin):
    """All the information about a Project in Stalker is hold in this class.
    
    Project is one of the main classes that will direct the others. A project
    in Stalker is a gathering point.
    
    It is mixed with :class:`~stalker.models.mixins.ReferenceMixin`,
    :class:`~stalker.models.mixins.StatusMixin`,
    :class:`~stalker.models.mixins.ScheduleMixin` and
    :class:`~stalker.models.mixins.TaskMixin` to give reference, status,
    schedule and task abilities. Please read the individual documentation of
    each of the mixins.
    
    The :attr:`~stalker.models.project.Project.users` attributes content is
    gathered from all the :class:`~stalker.models.task.Task`\ s of the project
    itself and from the :class:`~stalker.models.task.Task`\ s of the
    :class:`~stalker.models.sequence.Sequence`\ s stored in the
    :attr:`~stalker.models.project.Project.sequences` attribute, the
    :class:`~stalker.models.shot.Shot`\ s stored in the
    :attr:`~stalker.models.sequence.Sequence.shots` attribute, the
    :class:`~stalker.models.asset.Asset`\ s stored in the
    :attr:`~stalker.models.project.Project.assets`. It is a read only
    attribute.
    
    :param lead: The lead of the project. Default value is None.
    
    :type lead: :class:`~stalker.User`
    
    :param image_format: The output image format of the project. Default
      value is None.
    
    :type image_format: :class:`~stalker.models.formats.ImageFormat`
    
    :param float fps: The FPS of the project, it should be a integer or float
      number, or a string literal which can be correctly converted to a float.
      Default value is 25.0.
    
    :param type: The type of the project. Default value is None.
    
    :type type: :class:`~stalker.models.type.Type`
    
    :param structure: The structure of the project. Default value is None
    
    :type structure: :class:`~stalker.models.structure.Structure`
    
    :param repository: The repository that the project files are going to be
      stored in. You can not create a project without specifying the
      repository argument and passing a
      :class:`~stalker.models.repository.Repository` to it. Default value is
      None which raises a TypeError.
    
    :type repository: :class:`~stalker.models.repository.Repository`.
    
    :param bool is_stereoscopic: a bool value, showing if the project is going
      to be a stereo 3D project, anything given as the argument will be
      converted to True or False. Default value is False.
    

    """
    
    
    # DELETED ARGUMENTS:
    #
    #:param float display_width: the width of the display that the output of the
    #  project is going to be displayed (very unnecessary if you are not using
    #  stereo 3D setup). Should be an int or float value, negative values
    #  converted to the positive values. Default value is 1.
    
    
    # ------------------------------------------------------------------------
    # NOTES:
    #
    # Because a Project instance is inherited from TaskableEntity and which is
    # mixed with the ProjectMixin it has a project attribute. In SOM, the
    # project instantly assigns itself to the project attribute (in __init__).
    # But this creates a weird position in database table and mapper
    # configuration where for the Project class the mapper should configure the
    # `project` attribute with the post_update flag is set to True, and this
    # implies the project_id coloumn to be Null for a while, at least
    # SQLAlchemy does an UPDATE to assign the Project itself to the project
    # attribute, thus the project_id column shouldn't be nullable for Project
    # class, but it is not neccessary for the others.
    # 
    # And because SOM is also checking if the project attribute is None or Null
    # for the created instance, I consider doing this safe.
    # ------------------------------------------------------------------------

    #__strictly_typed__ = True
    __tablename__ = "Projects"
    project_id_local = Column("id", Integer, ForeignKey("TaskableEntities.id"),
                              primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "Project",
                       "inherit_condition":
                           project_id_local == TaskableEntity.taskableEntity_id}


    lead_id = Column(Integer, ForeignKey("Users.id"))
    lead = relationship(
        "User",
        primaryjoin="Projects.c.lead_id==Users.c.id",
        back_populates="projects_lead",
        doc="""The lead of the project.
        
        Should be an instance of :class:`~stalker.models.auth.User`,
        also can set to None.
        """
    )

    repository_id = Column(Integer, ForeignKey("Repositories.id"))
    repository = relationship(
        "Repository",
        primaryjoin="Project.repository_id==Repository.repository_id",
        doc="""The :class:`~stalker.models.repository.Repository` that this
        project should reside.
        
        Should be an instance of
        :class:`~stalker.models.repository.Repository`\ . It
        is a read-only attribute. So it is not possible to change the
        repository of one project.
        """
    )

    structure_id = Column(Integer, ForeignKey("Structures.id"))
    structure = relationship(
        "Structure",
        primaryjoin="Project.structure_id==Structure.structure_id",
        doc="""The structure of the project. Should be an instance of
        :class:`~stalker.models.structure.Structure` class"""
    )

    image_format_id = Column(Integer, ForeignKey("ImageFormats.id"))
    image_format = relationship(
        "ImageFormat",
        primaryjoin="Projects.c.image_format_id==ImageFormats.c.id",
        doc="""The :class:`~stalker.models.formats.ImageFormat` of this
        project.
        
        This value defines the output image format of the project, should be an
        instance of :class:`~stalker.models.formats.ImageFormat`.
        """
    )

    fps = Column(
        Float(precision=3),
        doc="""The fps of the project.
        
        It is a float value, any other types will be converted to float. The
        default value is 25.0.
        """
    )
    is_stereoscopic = Column(
        Boolean,
        doc="""True if the project is a stereoscopic project"""
    )

    def __init__(self,
                 lead=None,
                 repository=None,
                 structure=None,
                 image_format=None,
                 fps=25.0,
                 is_stereoscopic=False,
                 #display_width=1.0,
                 **kwargs):
        # a projects project should be self
        # initialize the project argument to self
        kwargs["project"] = self

        super(Project, self).__init__(**kwargs)
        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)

        self.lead = lead
        self._users = []
        self.repository = repository
        self.structure = structure
        self._sequences = []
        self._assets = []

        self.image_format = image_format
        self.fps = fps
        self.is_stereoscopic = bool(is_stereoscopic)


    @validates("fps")
    def _validate_fps(self, key, fps):
        """validates the given fps_in value
        """
        return float(fps)

    @validates("image_format")
    def _validate_image_format(self, key, image_format):
        """validates the given image format
        """
        
        from stalker.models.formats import ImageFormat

        if image_format is not None and\
           not isinstance(image_format, ImageFormat):
            raise TypeError("the image_format should be an instance of "
                            "stalker.models.formats.ImageFormat")

        return image_format

    @validates("lead")
    def _validate_lead(self, key, lead):
        """validates the given lead_in value
        """

        if lead is not None:
            if not isinstance(lead, User):
                raise TypeError("lead must be an instance of "
                                "stalker.models.auth.User")

        return lead

    @validates("repository")
    def _validate_repository(self, key, repository):
        """validates the given repository_in value
        """
        
        from stalker.models.repository import Repository

        if not isinstance(repository, Repository):
            raise TypeError("The stalker.models.project.Project instance "
                            "should be created with a "
                            "stalker.models.repository.Repository instance "
                            "passed through the 'repository' argument, the "
                            "current value is '%s'" % repository)

        return repository

    @validates("structure")
    def _validate_structure(self, key, structure_in):
        """validates the given structure_in value
        """
        from stalker.models.structure import Structure
        
        if structure_in is not None:
            if not isinstance(structure_in, Structure):
                raise TypeError("structure should be an instance of "
                                "stalker.models.structure.Structure")

        return structure_in

    @validates("is_stereoscopic")
    def _validate_is_stereoscopic(self, key, is_stereoscopic_in):
        return bool(is_stereoscopic_in)


    @property
    def users(self):
        """returns the users related to this project
        """
        
        from stalker.models.auth import User
        from stalker.models.task import Task
        
        if DBSession is not None:
            return DBSession.query(User).\
            join(User.tasks).\
            join(Task.task_of).\
            join(TaskableEntity.project).\
            filter(Project.name == self.name).all()
        else:
            RuntimeWarning("There is no database setup, the users can not "
                           "be queried from this state, please use "
                           "stalker.db.setup() to setup a database")
            return []

    @property
    def assets(self):
        """returns the assets related to this project
        """

        # use joins over the session.query
        from stalker.models.asset import Asset
        
        if DBSession is not None:
            return DBSession.query(Asset).\
            join(Asset.project).\
            filter(Project.name == self.name).all()
        else:
            RuntimeWarning("There is no database setup, the users can not "
                           "be queried from this state, please use "
                           "stalker.db.setup() to setup a database")
            return []

    @property
    def sequences(self):
        """returns the sequences related to this project
        """

        # use joins over the session.query
        from stalker.models.sequence import Sequence

        if DBSession is not None:
            return DBSession.query(Sequence).\
            join(Sequence.project).\
            filter(Project.name == self.name).all()
        else:
            RuntimeWarning("There is no database setup, the sequences can not "
                           "be queried from this state, please use "
                           "stalker.db.setup() to setup a database")
            return []

    def __eq__(self, other):
        """the equality operator
        """

        return super(Project, self).__eq__(other) and\
               isinstance(other, Project)
