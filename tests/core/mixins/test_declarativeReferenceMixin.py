#-*- coding: utf-8 -*-


import unittest

from stalker.core.declarativeModels import SimpleEntity, Link
from stalker.core.declarativeMixins import ReferenceMixin
from sqlalchemy import (
    Table,
    Column,
    Boolean,
    Integer,
    Float,
    String,
    ForeignKey,
    #Date,
    DateTime,
    UniqueConstraint
)






########################################################################
class A(SimpleEntity, ReferenceMixin):
    """A test class for ReferenceMixin
    """
    
    __tablename__ = "As"
    __mapper_args__ = {"polymorphic_identity": "A"}
    a_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(A, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)





########################################################################
class B(SimpleEntity, ReferenceMixin):
    """A test class for ReferenceMixin
    """
    
    __tablename__ = "Bs"
    __mapper_args__ = {"polymorphic_identity": "B"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(B, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)





########################################################################
class ReferenceMixinTester(unittest.TestCase):
    """Tests ReferenceMixin
    """
    
    
    
    #----------------------------------------------------------------------
    def test_ReferenceMixin_setup(self):
        """
        """
        a_ins = A(name="ozgur")
        b_ins = B(name="bozgur")
        
        new_link1 = Link(name="test link 1", path="none")
        new_link2 = Link(name="test link 2", path="no path")
        
        a_ins.references.append(new_link1)
        b_ins.references.append(new_link2)
        
        self.assertIn(new_link1, a_ins.references)
        self.assertIn(new_link2, b_ins.references)



