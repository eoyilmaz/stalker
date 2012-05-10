# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import re
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, validates
from stalker.conf import defaults
from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.mixins import StatusMixin

class Version(Entity, StatusMixin):
    """The connection to the filesystem.
    
    A :class:`~stalker.models.version.Version` holds information about the
    every incarnation of the files in the
    :class:`~stalker.models.repository.Repository`.
    So if one creates a new version for a file or a sequences of file for a
    :class:`~stalker.models.task.Task` then the information is hold in the
    :class:`~stalker.models.version.Version` instance.
    
    The :attr:`~stalker.models.version.Version.version` attribute is read-only.
    Trying to change it will produce an AttributeError.
    
    :param str take: A short string holding the current take name. Can be
      any alphanumeric value (a-zA-Z0-9\_). The default is the string "Main".
      When skipped or given as None or an empty string then it will use the
      default value. It can not start with a number. It can not have white
      spaces.
    
    :param int version: An integer value showing the current version number.
      The default is "1". If skipped or given as zero or as a negative value a
      ValueError will be raised.
    
    :param source: A :class:`~stalker.models.link.Link` instance, showing
      the source file of this version. It can be a Maya scene file
      (*.ma, *.mb), a Nuke file (*.nk) or anything that is opened with the
      application you have created this version.
    
    :type source: :class:`~stalker.models.link.Link`
    
    :param outputs: A list of :class:`~stalker.models.link.Link` instances,
      holding the outputs of the current version. It could be the rendered
      image sequences out of Maya or Nuke, or it can be a Targa file which is
      the output of a Photoshop file (*.psd), or anything that you can think as
      the output which is created using the
      :attr:`~stalker.models.version.Version.source_file`\ .
    
    :type outputs: list of :class:`~stalker.models.link.Link` instances
    
    :param version_of: A :class:`~stalker.models.task.Task` instance showing
      the owner of this Version.
    
    :type version_of: :class:`~stalker.models.task.Task`
    
    .. TODO::
      Think about using Tickets instead of review notes for reporting desired
      changes.
    
    """

    __tablename__ = "Versions"
    __mapper_args__ = {"polymorphic_identity": "Version"}

    version_id = Column("id", Integer, ForeignKey("Entities.id"),
                        primary_key=True)
    version_of_id = Column(Integer, ForeignKey("Tasks.id"), nullable=False)
    version_of = relationship(
        "Task",
        primaryjoin="Versions.c.version_of_id==Tasks.c.id",
        doc="""The :class:`~stalker.models.task.Task` instance that this Version is created for.
        """,
        uselist=False,
        back_populates="versions",
        )

    take = Column(String(256), default="MAIN")
    version = Column(Integer)

    source_id = Column(Integer, ForeignKey("Links.id"))
    source = relationship(
        "Link",
        primaryjoin="Versions.c.source_id==Links.c.id",
        uselist=False
    )

    outputs = relationship(
        "Link",
        secondary="Version_Outputs",
        primaryjoin="Versions.c.id==Version_Outputs.c.version_id",
        secondaryjoin="Version_Outputs.c.link_id==Links.c.id",
        doc="""The outputs of the current version.
        
        It is a list of :class:`~stalker.models.link.Link` instances.
        """
    )

    is_published = Column(Boolean, default=False)

    def __init__(self,
                 version_of=None,
                 take=defaults.DEFAULT_VERSION_TAKE_NAME,
                 version=None,
                 source=None,
                 outputs=None,
                 task=None,
                 **kwargs):
        # call supers __init__
        super(Version, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)

        self.take = take
        self.source = source
        self.version = version
        self.version_of = version_of

        if outputs is None:
            outputs = []

        self.outputs = outputs

        # set published to False by default
        self.published = False

    @validates("source")
    def _validate_source(self, key, source):
        """validates the given source value
        """
        
        from stalker.models.link import Link

        if source is not None:
            if not isinstance(source, Link):
                raise TypeError("Version.source attribute should be a "
                                "stalker.models.link.Link instance, not %s"\
                                % source.__class__.__name__)

        return source

    def _format_take(self, take):
        """formats the given take value
        """

        # remove unnecessary characters
        take = re.sub("([^a-zA-Z0-9\s_\-]+)", r"", take).strip().replace(" ",
                                                                         "")

        return re.sub(r"(.+?[^a-zA-Z]+)([a-zA-Z0-9\s_\-]+)", r"\2", take)

    @validates("take")
    def _validate_take(self, key, take):
        """validates the given take value
        """

        if take is None:
            raise TypeError("%s.take can not be None, please give a "
                            "proper string" % self.__class__.__name__)

        take = self._format_take(str(take))

        if take == "":
            raise ValueError("%s.take can not be an empty string" %
                             self.__class__.__name__)

        return take

    @validates("version")
    def _validate_version(self, key, version):
        """validates the given version value
        """

        if version is None:
            raise TypeError("%s.version should be an int" %
                            self.__class__.__name__)

        if version <= 0:
            raise ValueError("%s.version can not be zero or a negative "
                             "number" % self.__class__.__name__)

        return version

    @validates("version_of")
    def _validate_version_of(self, key, version_of):
        """validates the given version_of value
        """
        
        if version_of is None:
            raise TypeError("%s.version_of can not be None" %
                            self.__class__.__name__)
        
        from stalker.models.task import Task
        
        if not isinstance(version_of, Task):
            raise TypeError("%s.version_of should be a "
                            "stalker.models.task.Task instance not %s" %
                            (self.__class__.__name__,
                             version_of.__class__.__name__))

        return version_of
    
    @validates("outputs")
    def _validate_outputs(self, key, output):
        """validates the given output
        """
        
        from stalker.models.link import Link
        
        if not isinstance(output, Link):
            raise TypeError("all elements in %s.outputs should be all "
                            "stalker.models.link.Link instances not %s" %
                self.__class__.__name__, output.__class__.__name__
            )

        return output

# VERSION_OUTPUTS
Version_Outputs = Table(
    "Version_Outputs", Base.metadata,
    Column("version_id", Integer, ForeignKey("Versions.id"), primary_key=True),
    Column("link_id", Integer, ForeignKey("Links.id"), primary_key=True)
)
