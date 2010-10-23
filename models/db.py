#-*- coding: utf-8 -*-
########################################################################
# 
# Copyright (C) 2010  Erkan Ozgur Yilmaz
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# 
########################################################################



# lets play with SQLAlchemy a little bit

from sqlalchemy import *
from datetime import datetime

metadata = MetaData('sqlite:///tutorial.sqlite')

user_table = Table(
    'tf_user', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_name', Unicode(16),
           unique=True, nullable=False),
    Column('password', Unicode(40), nullable=False),
    Column('display_name', Unicode(255), default=''),
    Column('created', DateTime, default=datetime.now)
    )

group_table = Table(
    'tf_group', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(16),
           unique=True, nullable=False)
    )

permission_table = Table(
    'tf_permission', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(16),
           unique=True, nullable=False)
    )

user_group_table = Table(
    'tf_user_group', metadata,
    Column('user_id', None, ForeignKey('tf_user.id'),
           primary_key=True),
    Column('group_id', None, ForeignKey('tf_group.id'),
           primary_key=True)
    )

group_permission_table = Table(
    'tf_group_permission', metadata,
    Column('permission_id', None, ForeignKey('tf_permission.id'),
           primary_key=True),
    Column('group_id', None, ForeignKey('tf_group.id'),
           primary_key=True)
    )

metadata.create_all()
