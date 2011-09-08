#-*- coding: utf-8 -*-

import unittest

from stalker.core.models import SimpleEntity, Status, StatusList, StatusMixin
from sqlalchemy import (
    Table,
    Column,
    Boolean,
    Integer,
    Float,
    String,
    ForeignKey,
)

# create a new mixed in SimpleEntity
class DeclStatMixA(SimpleEntity, StatusMixin):
    
    __tablename__ = "DeclStatMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclStatMixA"}
    a_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(DeclStatMixA, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)






class DeclStatMixB(SimpleEntity, StatusMixin):
    
    __tablename__ = "DeclStatMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclStatMixB"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(B, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)






########################################################################
class StatusMixinTester(unittest.TestCase):
    """tests StatusMixin
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
            target_entity_type="DeclStatMixA",
        )
        
        self.test_b_statusList = StatusList(
            name="B Statuses",
            statuses=[self.test_stat2, self.test_stat3],
            target_entity_type="DeclStatMixB"
        )
        
        self.kwargs = {
            "name": "ozgur",
            "status_list": self.test_a_statusList
        }
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_argument_not_set(self):
        """testing if a TypeError will be raised when the status_list argument
        is not set
        """
        self.kwargs.pop("status_list")
        self.assertRaises(TypeError, DeclStatMixA, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_argument_is_not_correct(self):
        """testing if a TypeError will be raised when the given StatusList
        instance with the status_list argument is not suitable for this class
        """
        self.kwargs["status_list"] = self.test_b_statusList
        self.assertRaises(TypeError, DeclStatMixA, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_status_list_working_properly(self):
        """testing if the status_list attribute is working properly
        """
        
        new_a_ins = DeclStatMixA(
            name="Ozgur",
            status_list=self.test_a_statusList
        )
        
        self.assertIn(self.test_stat1, new_a_ins.status_list)
        self.assertNotIn(self.test_stat2, new_a_ins.status_list)
        self.assertIn(self.test_stat3, new_a_ins.status_list)
    
    
    