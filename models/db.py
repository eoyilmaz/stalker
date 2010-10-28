#-*- coding: utf-8 -*-



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
