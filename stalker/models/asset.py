# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import reconstructor
from stalker.models.entity import TaskableEntity
from stalker.models.mixins import StatusMixin, ReferenceMixin

__author__ = 'eoyilmaz'

class Asset(TaskableEntity, ReferenceMixin, StatusMixin):
    """The Asset class is the whole idea behind Stalker.
    
    *Assets* are containers of :class:`~stalker.core.models.Task`\ s. And
    :class:`~stalker.core.models.Task`\ s are the smallest meaningful part that
    should be accomplished to complete the
    :class:`~stalker.core.models.Project`.
    
    An example could be given as follows; you can create an asset for one of
    the characters in your project. Than you can divide this character asset in
    to :class:`~stalker.core.models.Task`\ s. These
    :class:`~stalker.core.models.Task`\ s can be defined by the type of the
    :class:`~stalker.core.models.Asset`, which is a
    :class:`~stalker.core.models.Type` object created specifically for
    :class:`~stalker.core.models.Asset` (ie. has its
    :attr:`~stalker.core.models.Type.target_entity_type` set to "Asset"),
    
    An :class:`~stalker.core.models.Asset` instance should be initialized with
    a :class:`~stalker.core.models.Project` instance (as the other classes
    which are mixed with the :class:`~stalekr.core.mixins.TaskMixin`). And when
    a :class:`~stalker.core.models.Project` instance is given then the asset
    will append itself to the :attr:`~stalker.core.models.Project.assets` list.
    
    ..versionadded: 0.2.0:
        No more Asset to Shot connection:
        
        Assets now are not directly related to Shots. Instead a
        :class:`~stalker.models.Version` will reference the Asset and then it
        is easy to track which shots are referencing this Asset by querying
        with a join of Shot Versions referencing this Asset.
    """

    __strictly_typed__ = True
    __tablename__ = "Assets"
    __mapper_args__ = {"polymorphic_identity": "Asset"}

    asset_id = Column("id", Integer, ForeignKey("TaskableEntities.id"),
                      primary_key=True)

    #@declared_attr
    #def project(self):
    #return relationship(
    #"Project",
    #primaryjoin="Assets.c.project_id==Projects.c.id",
    #back_populates="assets",
    #uselist=False,
    #doc="""The :class:`~stalker.core.models.Project` instance that this Asset belongs to.

    #A :class:`~stalker.core.models.Asset` can not be created without a
    #:class:`~stalker.core.models.Project` instance.
    #"""
    #)



    #project_id = Column(Integer, ForeignKey("Projects.id"), nullable=False)
    #project = relationship(
    #"Project",
    #primaryjoin="Assets.c.project_id==Projects.c.id",
    #back_populates="assets",
    #uselist=False,
    #doc="""The :class:`~stalker.core.models.Project` instance that this Asset belongs to.

    #A :class:`~stalker.core.models.Asset` can not be created without a
    #:class:`~stalker.core.models.Project` instance.
    #"""
    #)

    def __init__(self, **kwargs):
        super(Asset, self).__init__(**kwargs)

        # call the mixin init methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        #TaskMixin.__init__(self, **kwargs)

        #self._shots = []
        #if shots is None:
        #    shots = []
        #self.shots = shots

        ## append it self to the given projects assets attribute
        #if not self in self.project._assets:
        #self.project._assets.append(self)

    @reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        #self._shots = None

        # call supers __init_on_load__
        super(Asset, self).__init_on_load__()

#    @validates("shots")
#    def _validate_shots(self, key, shot):
#        """validates the given shots_in value
#        """
#
#        if not isinstance(shot, Shot):
#            raise TypeError("shots should be set to a list of "
#                            "stalker.core.models.Shot objects")
#
#        return shot

    def __eq__(self, other):
        """the equality operator
        """

        return super(Asset, self).__eq__(other) and\
               isinstance(other, Asset) and self.type == other.type
