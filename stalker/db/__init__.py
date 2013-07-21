# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
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
"""Database module of Stalker.

Whenever stalker.db or something under it imported, the
:func:`stalker.db.setup` becomes available to let one setup the database.
"""

import logging

from sqlalchemy import engine_from_config
from sqlalchemy.exc import IntegrityError

from stalker import defaults
from stalker.db.declarative import Base
from stalker.db.session import DBSession
from stalker.log import logging_level

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


def setup(settings=None):
    """Utility function that helps to connect the system to the given database.

    if the database is None then the it setups using the default database in
    the settings file.

    :param settings: This is a dictionary which has keys prefixed with
        "sqlalchemy" and shows the settings. The most important one is the
        engine. The default is None, and in this case it uses the settings from
        stalker.config.Config.database_engine_settings

    :param callback: A callback function which is called after database is
        initialized. It is a good place to register your own classes.
   """

    if settings is None:
        settings = defaults.database_engine_settings
        logger.debug('no settings given, using the default: %s' % settings)

    logger.debug("settings: %s" % settings)
    # create engine
    engine = engine_from_config(settings, 'sqlalchemy.')

    logger.debug('engine: %s' % engine)

    # create the Session class
    DBSession.remove()
    DBSession.configure(
        bind=engine,
        extension=None
    )

    # create the database
    logger.debug("creating the tables")
    Base.metadata.create_all(engine)


def init():
    """fills the database with default values
    """
    logger.debug("initializing database")

    # register all Actions available for all SOM classes
    class_names = [
        'Asset', 'TimeLog', 'Department', 'Entity', 'FilenameTemplate',
        'Group', 'ImageFormat', 'Link', 'Message', 'Note', 'Permission',
        'Project', 'Repository', 'Scene', 'Sequence', 'Shot', 'SimpleEntity',
        'Status', 'StatusList', 'Structure', 'Studio', 'Tag', 'Task', 'Ticket',
        'TicketLog', 'Type', 'User', 'Vacation', 'Version']

    for class_name in class_names:
        _temp = __import__(
            'stalker',
            globals(),
            locals(),
            [class_name],
            -1
        )
        class_ = eval("_temp." + class_name)
        register(class_)

    # create the admin if needed
    if defaults.auto_create_admin:
        __create_admin__()

    # create Ticket statuses
    __create_ticket_statuses()

    logger.debug('finished initializing the database')


def __create_admin__():
    """creates the admin
    """
    from stalker.models.auth import User
    from stalker.models.department import Department

    # check if there is already an admin in the database
    admin = User.query.filter_by(name=defaults.admin_name).first()
    if admin:
        #there should be an admin user do nothing
        logger.debug("there is an admin already")
        return

    logger.debug("creating the default administrator user")

    # create the admin department
    admin_department = Department.query.filter_by(
        name=defaults.admin_department_name
    ).first()

    if not admin_department:
        admin_department = Department(name=defaults.admin_department_name)
        DBSession.add(admin_department)
        # create the admins group

    from stalker.models.auth import Group

    admins_group = Group.query \
        .filter_by(name=defaults.admin_group_name) \
        .first()

    if not admins_group:
        admins_group = Group(name=defaults.admin_group_name)
        DBSession.add(admins_group)

    # # create the admin user
    # admin = User.query \
    #     .filter_by(name=defaults.admin_name) \
    #     .first()

    # if not admin:
    admin = User(
        name=defaults.admin_name,
        login=defaults.admin_login,
        password=defaults.admin_password,
        email=defaults.admin_email,
        departments=[admin_department],
        groups=[admins_group]
    )

    admin.created_by = admin
    admin.updated_by = admin

    # update the department as created and updated by admin user
    admin_department.created_by = admin
    admin_department.updated_by = admin

    admins_group.created_by = admin
    admins_group.updated_by = admin

    DBSession.add(admin)
    DBSession.commit()


def __create_ticket_statuses():
    """creates the default ticket statuses
    """
    from stalker import User

    admin = User.query.filter(User.login == defaults.admin_name).first()

    # create statuses for Tickets
    from stalker import Status, StatusList

    logger.debug("Creating Ticket Statuses")

    # Update: check before adding
    ticket_names = map(str.title, defaults.ticket_status_order)
    ticket_statuses = Status.query.filter(Status.name.in_(ticket_names)).all()
    if not ticket_statuses:
        logger.debug('No Ticket Statuses found, creating new!')
        ticket_statuses = [
            Status(
                name=status_name.title(),
                code=status_name.upper(),
                created_by=admin,
                updated_by=admin
            ) for status_name in defaults.ticket_status_order
        ]
    else:
        logger.debug('Ticket Statuses are already created')

    ticket_status_list = StatusList.query\
        .filter(StatusList._target_entity_type=='Ticket')\
        .first()

    if not ticket_status_list:
        logger.debug('No Ticket Status List found, creating new!')
        ticket_status_list = StatusList(
            name='Ticket Statuses',
            target_entity_type='Ticket',
            statuses=ticket_statuses,
            created_by=admin,
            updated_by=admin
        )
        DBSession.add(ticket_status_list)
        try:
            DBSession.commit()
        except IntegrityError:
            DBSession.rollback()
        else:
            logger.debug("Created Ticket Statuses successfully")
            DBSession.flush()
    else:
        logger.debug("Ticket Status List already created")

    # Again I hate doing this in this way
    from stalker import Type

    types = Type.query \
        .filter_by(target_entity_type="Ticket") \
        .all()
    t_names = [t.name for t in types]

    # create Ticket Types
    logger.debug("Creating Ticket Types")
    if 'Defect' not in t_names:
        ticket_type_1 = Type(
            name='Defect',
            code='Defect',
            target_entity_type='Ticket',
            created_by=admin,
            updated_by=admin
        )
        DBSession.add(ticket_type_1)

    if 'Enhancement' not in t_names:
        ticket_type_2 = Type(
            name='Enhancement',
            code='Enhancement',
            target_entity_type='Ticket',
            created_by=admin,
            updated_by=admin
        )
        DBSession.add(ticket_type_2)
    try:
        DBSession.commit()
    except IntegrityError:
        DBSession.rollback()
        logger.debug("Ticket Types are already in the database!")
    else:
        # DBSession.flush()
        logger.debug("Ticket Types are created successfully")


def register(class_):
    """Registers the given class to the database.

    It is mainly used to create the :class:`~stalker.models.auth.Action`\ s
    needed for the :class:`~stalker.models.auth.User`\ s and
    :class:`~stalker.models.auth.Group`\ s to be able to interact with the
    given class. Whatever class you have created needs to be registered.

    Example, lets say that you have a data class which is specific to your
    studio and it is not present in Stalker Object Model (SOM), so you need to
    extend SOM with a new data type. Here is a simple Data class inherited from
    the :class:`~stalker.models.entity.SimpleEntity` class (which is the
    simplest class you should inherit your classes from or use more complex
    classes down to the hierarchy)::

      from sqlalchemy import Column, Integer, ForeignKey
      from stalker.models.entity import SimpleEntity

      class MyDataClass(SimpleEntity):
        '''This is an example class holding a studio specific data which is not
        present in SOM.
        '''

        __tablename__ = 'MyData'
        __mapper_arguments__ = {'polymorphic_identity': 'MyData'}

        my_data_id = Column('id', Integer, ForeignKey('SimpleEntities.c.id'),
                            primary_key=True)

    Now because Stalker is using Pyramid authorization mechanism it needs to be
    able to have an :class:`~stalker.models.auth.Permission` about your new
    class, so you can assign this :class;`~stalker.models.auth.Permission` to
    your :class:`~stalker.models.auth.User`\ s or
    :class:`~stalker.models.auth.Group`\ s. So you ned to register your new
    class with stalker.db.register like shown below::

      from stalker import db
      db.register(MyDataClass)

    This will create the necessary Actions in the 'Actions' table on your
    database, then you can create :class:`~stalker.models.auth.Permission`\ s
    and assign these to your :class:`~stalker.models.auth.User`\ s and
    :class:`~stalker.models.auth.Group`\ s so they are Allowed or Denied to do
    the specified Action.

    :param class_: The class itself that needs to be registered.
    """
    from stalker.models.auth import Permission

    # create the Permissions
    permissions_db = Permission.query.all()

    if not isinstance(class_, type):
        raise TypeError('To register a class please supply the class itself ')

    # register the class name to entity_types table
    from stalker import EntityType, StatusMixin, ScheduleMixin, ReferenceMixin

    class_name = class_.__name__

    if not EntityType.query.filter_by(name=class_name).first():
        new_entity_type = EntityType(class_name)
        # update attributes
        if issubclass(class_, StatusMixin):
            new_entity_type.statusable = True
        if issubclass(class_, ScheduleMixin):
            new_entity_type.schedulable = True
        if issubclass(class_, ReferenceMixin):
            new_entity_type.accepts_references = True

        DBSession.add(new_entity_type)

    for action in defaults.actions:
        for access in ['Allow', 'Deny']:
            permission_obj = Permission(access, action, class_name)
            if permission_obj not in permissions_db:
                DBSession.add(permission_obj)

    try:
        DBSession.commit()
    except IntegrityError:
        DBSession.rollback()
    # else:
    #     DBSession.flush()
