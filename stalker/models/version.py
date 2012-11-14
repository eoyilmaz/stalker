# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import re
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, validates, synonym
from stalker.conf import defaults
from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.mixins import StatusMixin

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# TODO: Add parent_version attribute to hold a parent child relation between
# version to pin point the source of the given version.

class Version(Entity, StatusMixin):
    """The connection to the filesystem.
    
    A :class:`~stalker.models.version.Version` holds information about the
    every incarnation of the files in the
    :class:`~stalker.models.repository.Repository`.
    So if one creates a new version for a file or a sequences of file for a
    :class:`~stalker.models.task.Task` then the information is hold in the
    :class:`~stalker.models.version.Version` instance.
    
    The :attr:`~stalker.models.version.Version.version_number` attribute is
    read-only. Trying to change it will produce an AttributeError.
    
    :param str take_name: A short string holding the current take name. Can be
      any alphanumeric value (a-zA-Z0-9\_). The default is the string "Main".
      When skipped or given as None or an empty string then it will use the
      default value. It can not start with a number. It can not have white
      spaces.
    
    :param source_file: A :class:`~stalker.models.link.Link` instance, showing
      the source file of this version. It can be a Maya scene file
      (*.ma, *.mb), a Nuke file (*.nk) or anything that is opened with the
      application you have created this version.
    
    :type source_file: :class:`~stalker.models.link.Link`
    
    :param outputs: A list of :class:`~stalker.models.link.Link` instances,
      holding the outputs of the current version. It could be the rendered
      image sequences out of Maya or Nuke, or it can be a Targa file which is
      the output of a Photoshop file (*.psd), or anything that you can think
      as the output which is created using the
      :attr:`~stalker.models.version.Version.source_file`\ .
    
    :type outputs: list of :class:`~stalker.models.link.Link` instances
    
    :param version_of: A :class:`~stalker.models.task.Task` instance showing
      the owner of this Version.
    
    :type version_of: :class:`~stalker.models.task.Task`
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
    
    take_name = Column(String(256), default="MAIN")
    version_number = Column(Integer, default=1, nullable=False)
    
    source_file_id = Column(Integer, ForeignKey("Links.id"))
    source_file = relationship(
        "Link",
        primaryjoin="Versions.c.source_file_id==Links.c.id",
        uselist=False,
        doc="""This is the source file of this Version instance.
        
        It holds a :class:`~stalker.models.link.Link` instance which is showing
        a source file for this version. It is let say the scene file for Maya
        or a psd file for Photoshop etc.
        """
    )
    
    inputs = relationship(
        "Link",
        secondary="Version_Inputs",
        primaryjoin="Versions.c.id==Version_Inputs.c.version_id",
        secondaryjoin="Version_Inputs.c.link_id==Links.c.id",
        doc="""The inputs of the current version.
        
        It is a list of :class:`~stalker.models.link.Link` instances.
        """
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
                 take_name=defaults.DEFAULT_VERSION_TAKE_NAME,
                 #version_number=None,
                 source_file=None,
                 inputs=None,
                 outputs=None,
                 task=None,
                 **kwargs):
        # call supers __init__
        super(Version, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)
        
        self.take_name = take_name
        self.source_file = source_file
        self.version_of = version_of
        self.version_number = None
        if inputs is None:
            inputs = []
        
        if outputs is None:
            outputs = []
        
        self.inputs = inputs
        self.outputs = outputs
        
        # set published to False by default
        self.is_published = False
    
    @validates("source_file")
    def _validate_source_file(self, key, source_file):
        """validates the given source_file value
        """
        from stalker.models.link import Link
        
        if source_file is not None:
            if not isinstance(source_file, Link):
                raise TypeError("Version.source_file attribute should be a "
                                "stalker.models.link.Link instance, not %s"\
                                % source_file.__class__.__name__)
        
        return source_file

    def _format_take_name(self, take_name):
        """formats the given take_name value
        """
        # remove unnecessary characters
        take_name = re.sub(
            r"([^a-zA-Z0-9\s_\-]+)", r"", take_name
        ).strip().replace(" ", "")
        
        return re.sub(r"(.+?[^a-zA-Z]+)([a-zA-Z0-9\s_\-]+)", r"\2", take_name)

    @validates("take_name")
    def _validate_take_name(self, key, take_name):
        """validates the given take_name value
        """
        if take_name is None:
            raise TypeError("%s.take_name can not be None, please give a "
                            "proper string" % self.__class__.__name__)
        
        take_name = self._format_take_name(str(take_name))
        
        if take_name == "":
            raise ValueError("%s.take_name can not be an empty string" %
                             self.__class__.__name__)
        
        return take_name
    
    @property
    def max_version_number(self):
        """returns the maximum version number for this Version
        :return: int
        """
        from stalker.db.session import DBSession
        
        all_versions = DBSession.query(Version)\
            .filter(Version.version_of==self.version_of)\
            .filter(Version.take_name==self.take_name)\
            .order_by(Version.version_number.desc())\
            .all()
        
        if len(all_versions):
            version_with_max_version_number = all_versions[-1]
            
            # skip the current version if it is itself to prevent increasing
            # the version number unnecessarliy
            if version_with_max_version_number is not self:
                return version_with_max_version_number.version_number
            elif len(all_versions) > 1:
                return all_versions[-2].version_number
        
        return 0
    
    @validates("version_number")
    def _validate_version_number(self, key, version_number):
        """validates the given version_number value
        """
        max_version = self.max_version_number
        logger.debug('max_version_number: %s' % max_version)
        logger.debug('given version_number: %s' % version_number)
        if version_number is None or version_number <= max_version:

            version_number = max_version + 1
            logger.debug(
                'given Version.version_number is too low, max version_number '
                'in the database is %s, setting the current version_number to '
                '%s' % (max_version, version_number)
            )
        
        return version_number
    
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
    
    @validates("inputs")
    def _validate_inputs(self, key, input):
        """validates the given output
        """
        from stalker.models.link import Link
        
        if not isinstance(input, Link):
            raise TypeError("all elements in %s.inputs should be all "
                            "stalker.models.link.Link instances not %s" %
                            (self.__class__.__name__,
                             input.__class__.__name__)
            )

        return input
    
    @validates("outputs")
    def _validate_outputs(self, key, output):
        """validates the given output
        """
        from stalker.models.link import Link
        
        if not isinstance(output, Link):
            raise TypeError("all elements in %s.outputs should be all "
                            "stalker.models.link.Link instances not %s" %
                            (self.__class__.__name__,
                             output.__class__.__name__)
            )

        return output
    
#    @validates("tickets")
#    def _validate_tickets(self, key, ticket):
#        """validates the given ticket value
#        """
#        
#        from stalker.models.ticket import Ticket
#        
#        if not isinstance(ticket, Ticket):
#            raise TypeError("%s.tickets should be a list of "
#                            "stalker.models.ticket.Ticket instances not %s" %
#                            (self.__class__.__name__,
#                             ticket.__class__.__name__))
#        
#        return ticket

# VERSION INPUTS
Version_Inputs = Table(
    "Version_Inputs", Base.metadata,
    Column("version_id", Integer, ForeignKey("Versions.id"), primary_key=True),
    Column("link_id", Integer, ForeignKey("Links.id"), primary_key=True)
)

# VERSION_OUTPUTS
Version_Outputs = Table(
    "Version_Outputs", Base.metadata,
    Column("version_id", Integer, ForeignKey("Versions.id"), primary_key=True),
    Column("link_id", Integer, ForeignKey("Links.id"), primary_key=True)
)
