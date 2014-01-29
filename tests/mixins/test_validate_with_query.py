# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import session, relationship
from sqlalchemy.orm.mapper import validates
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import ForeignKey, Column
from sqlalchemy.types import Integer

Base = declarative_base()

class Mixin(object):
    def __init__(self, b=None):
#        print "running __init__ on %s" % self.__class__.__name__
        self.b = b

    @declared_attr
    def b_id(cls):
        return Column(Integer, ForeignKey("Bs.id"))

    @declared_attr
    def b(cls):
        return relationship(
            "B",
            primaryjoin="%s.b_id==B.b_id" % cls.__name__
        )

    @validates("b")
    def _validate_bs(self, key, b):
        if b is None:
            if session is not None:
#                print "session is not None"
#                print "querying for a b"

                b = session.query(B).first()
#            if b is not None:
#                print "found a b"

        return b


class A(Base, Mixin):
    __tablename__ = "As"
    a_id = Column("id", Integer, primary_key=True)

    def __init__(self, b=None):
        Mixin.__init__(self, b)


class B(Base):
    __tablename__ = "Bs"
    b_id = Column("id", Integer, primary_key=True)


engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

b = B()
session.add(b)
session.commit()

#print session.query(B).first()

a = A()
assert a.b is b


