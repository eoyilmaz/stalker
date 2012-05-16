# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates
from stalker import User
from stalker.models.entity import TaskableEntity
from stalker.models.mixins import StatusMixin, ScheduleMixin, ReferenceMixin

class Sequence(TaskableEntity, ReferenceMixin, StatusMixin, ScheduleMixin):
    """Stores data about Sequences.
    
    Sequences are holders of the :class:`~stalker.models.shot.Shot` objects.
    They organize the conceptual data with another level of complexity.
    
    The Sequence class updates the
    :attr:`~stalker.models.project.Project.sequence` attribute in the
    :class:`~stalker.models.project.Project` class when the Sequence is
    initialized.
    
    :param lead: The lead of this Sequence. The default value is None.
    
    :type lead: :class:`~stalker.User`
    """

    #    __project_backref_attrname__ = "sequences_ossuruk"
    __project_doc__ = """The :class:`~stalker.models.project.Project` instance that this Sequence belongs to.
    
    A :class:`~stalker.models.sequence.Sequence` can not be created without a
    :class:`~stalker.models.project.Project` instance.
    """

    __tablename__ = "Sequences"
    __mapper_args__ = {"polymorphic_identity": "Sequence"}
    sequence_id = Column("id", Integer, ForeignKey("TaskableEntities.id"),
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
        primaryjoin="Shots.c.sequence_id==Sequences.c.id",
        back_populates="_sequence",
        doc="""The :class:`~stalker.models.shot.Shot`\ s assigned to this Sequence.
        
        It is a list of :class:`~stalker.models.shot.Shot` instances.
        """
    )

    def __init__(self,
                 lead=None,
                 **kwargs
    ):
        super(Sequence, self).__init__(**kwargs)

        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        #TaskMixin.__init__(self, **kwargs)

        #self._lead = self._validate_lead(lead)
        self.lead = lead
        self.shots = []

        ## update the Project._sequences attribute
        #if not self in self.project.sequences:
        #self._project._sequences.append(self)

    @validates("lead")
    def _validate_lead(self, key, lead):
        """validates the given lead_in value
        """

        if lead is not None:
            if not isinstance(lead, User):
                raise TypeError("lead should be instance of "
                                "stalker.models.user.User")

        return lead

    @validates("shots")
    def _validate_shots(self, key, shot):
        """validates the given shot value
        """
        
        from stalker.models.shot import Shot
        
        if not isinstance(shot, Shot):
            raise TypeError("every item in the shots list should be an "
                            "instance of stalker.models.shot.Shot")

        return shot

    def __eq__(self, other):
        """the equality operator
        """

        return super(Sequence, self).__eq__(other) and\
               isinstance(other, Sequence)
