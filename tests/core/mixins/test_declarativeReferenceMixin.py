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

# create a new mixed in SimpleEntity

class A(SimpleEntity, ReferenceMixin):
    
    __tablename__ = "As"
    __mapper_args__ = {"polymorphic_identity": "A"}
    a_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)
    pass


class B(SimpleEntity, ReferenceMixin):
    
    __tablename__ = "Bs"
    __mapper_args__ = {"polymorphic_identity": "B"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                  primary_key=True)
    pass

a_ins = A(name="ozgur")
b_ins = B(name="bozgur")

new_link1 = Link(name="test link 1", path="none")
new_link2 = Link(name="test link 2", path="no path")

a_ins.references.append(new_link1)
b_ins.references.append(new_link2)

assert new_link1 in a_ins.references
assert new_link2 in b_ins.references


