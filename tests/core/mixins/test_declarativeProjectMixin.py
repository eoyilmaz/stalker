#-*- coding: utf-8 -*-

import unittest

from stalker.core.models import (SimpleEntity, Project, Type, Status,
                                 StatusList, Repository, ProjectMixin)
from sqlalchemy import Column, Integer, ForeignKey



# create a new mixed in SimpleEntity
class DeclProjMixA(SimpleEntity, ProjectMixin):
    
    __tablename__ = "ProjMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclProjMixA"}
    a_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(DeclProjMixA, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)



class DeclProjMixB(SimpleEntity, ProjectMixin):
    
    __tablename__ = "ProjMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclProjMixB"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(DeclProjMixB, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)






########################################################################
class ProjectMixinTester(unittest.TestCase):
    """tests ProjectMixin
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        self.test_stat1 = Status(name="On Hold", code="OH")
        self.test_stat2 = Status(name="Work In Progress", code="WIP")
        self.test_stat3 = Status(name="Approved", code="APP")
        
        self.test_a_statusList = StatusList(
            name="A Statuses",
            statuses=[self.test_stat1, self.test_stat3],
            target_entity_type=DeclProjMixA,
        )
        
        self.test_b_statusList = StatusList(
            name="B Statuses",
            statuses=[self.test_stat2, self.test_stat3],
            target_entity_type=DeclProjMixB
        )
        
        self.test_project_statusList = StatusList(
            name="Project Statuses",
            statuses=[self.test_stat2, self.test_stat3],
            target_entity_type=Project
        )
        
        self.test_project_type = Type(
            name="Test Project",
            target_entity_type=Project,
        )
        
        self.test_repository = Repository(
            name="Test Repo",
        )
        
        self.test_project = Project(
            name="Test Project",
            type=self.test_project_type,
            status_list = self.test_project_statusList,
            repository=self.test_repository,
        )
        
        self.kwargs = {
            "name": "ozgur",
            "status_list": self.test_a_statusList,
            "project": self.test_project,
        }
        
        self.test_a_obj = DeclProjMixA(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_project_attribute_is_working_properly(self):
        """testing if the project attribute is working properly
        """
        
        self.assertEqual(self.test_a_obj.project, self.test_project)
    
    
    
    