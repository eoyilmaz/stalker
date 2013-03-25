# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of oyProjectManager and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
""" store the declarative_base in this module
"""

from sqlalchemy.ext.declarative import declarative_base
from stalker.db.session import DBSession

class ORMClass(object):
    query = DBSession.query_property()

Base = declarative_base(cls=ORMClass)
