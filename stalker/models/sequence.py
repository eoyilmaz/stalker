# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates
from stalker import User
from stalker.models.task import Task
from stalker.models.mixins import (ReferenceMixin, CodeMixin)

from stalker.log import logging_level
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

class Sequence(Task, ReferenceMixin, CodeMixin):
    """Stores data about Sequences.
    
    Sequences are a way of grouping the Shots according to their temporal
    position to each other.
    
    Initialization
    --------------
    
    A Sequence instance needs to be initialized with a
    :class:`~stalker.models.project.Project` instance.
    
    :param lead: The lead of this Sequence. The default value is None.
    
    :type lead: :class:`~stalker.User`
    """
    
    __project_doc__ = """The :class:`~stalker.models.project.Project` instance that this Sequence belongs to.
    
    A :class:`~stalker.models.sequence.Sequence` can not be created without a
    :class:`~stalker.models.project.Project` instance.
    """
    __auto_name__ = False
    __tablename__ = "Sequences"
    __mapper_args__ = {"polymorphic_identity": "Sequence"}
    sequence_id = Column("id", Integer, ForeignKey("Tasks.id"),
                         primary_key=True)

    lead_id = Column(Integer, ForeignKey("Users.id"))
    lead = relationship(
        "User",
        primaryjoin="Sequences.c.lead_id==Users.c.id",
        back_populates="sequences_lead",
        uselist=False,
        doc="""The lead of this sequence.
        
        A :class:`~stalker.models.user.User` instance which is assigned as the
        lead of this :class:`~stalker.models.sequence.Sequence`.
        """
    )

    shots = relationship(
        "Shot",
        secondary='Shot_Sequences',
        back_populates="sequences",
        doc="""The :class:`~stalker.models.shot.Shot`\ s assigned to this Sequence.
        
        It is a list of :class:`~stalker.models.shot.Shot` instances.
        """
    )

    def __init__(self, lead=None, **kwargs):
        super(Sequence, self).__init__(**kwargs)
        
        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        #StatusMixin.__init__(self, **kwargs)
        #ScheduleMixin.__init__(self, **kwargs)
        CodeMixin.__init__(self, **kwargs)
        
        self.lead = lead
        self.shots = []

    @validates("lead")
    def _validate_lead(self, key, lead):
        """validates the given lead_in value
        """
        if lead is not None:
            if not isinstance(lead, User):
                raise TypeError("%s.lead should be instance of "
                                "stalker.models.user.User, not %s" % 
                                (self.__class__.__name__,
                                 lead.__class__.__name__))
        return lead

    @validates("shots")
    def _validate_shots(self, key, shot):
        """validates the given shot value
        """
        from stalker.models.shot import Shot
        if not isinstance(shot, Shot):
            raise TypeError('%s.shots should be all '
                            'stalker.models.shot.Shot instances, not %s')
        return shot

    def __eq__(self, other):
        """the equality operator
        """
        return isinstance(other, Sequence) and \
               super(Sequence, self).__eq__(other)
