# -*- coding: utf-8 -*-
"""Database module of Stalker.

Whenever stalker.db or something under it imported, the :func:`stalker.db.setup` becomes
available to let one set up the database.
"""
import logging
import os
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import Column, Table, Text, engine_from_config, text
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError

from stalker import (
    DateRangeMixin,
    Department,
    EntityType,
    Group,
    Permission,
    ReferenceMixin,
    Repository,
    ScheduleMixin,
    Status,
    StatusList,
    StatusMixin,
    Studio,
    Type,
    User,
    defaults,
    log,
)
from stalker.db.declarative import Base
from stalker.db.session import DBSession


logger: logging.Logger = log.get_logger(__name__)

# TODO: Try to get it from the API (it was not working inside a package before)
alembic_version: str = "9f9b88fef376"


def setup(settings: Optional[Dict[str, Any]] = None) -> None:
    """Connect the system to the given database.

    If the database is None then it sets up using the default database in the
    settings file.

    Args:
        settings (Dict[str, Any]): This is a dictionary which has keys prefixed
            with "sqlalchemy" and shows the settings. The most important one is
            the engine. The default is None, and in this case it uses the
            settings from stalker.config.Config.database_engine_settings
    """
    if settings is None:
        settings = defaults.database_engine_settings
        logger.debug("no settings given, using the default setting")

    # logger.debug(f"settings: {settings}")
    # create engine

    logger.debug(f"settings: {settings}")
    engine = engine_from_config(settings, "sqlalchemy.")

    logger.debug(f"engine: {engine}")

    # create the Session class
    DBSession.remove()
    DBSession.configure(bind=engine)

    # check alembic versions of the database
    # and raise an error if it is not matching with the system
    check_alembic_version()

    # create the database
    logger.debug("creating the tables")

    Base.metadata.create_all(engine)
    DBSession.commit()

    # update defaults
    update_defaults_with_studio()

    # create repo env variables
    create_repo_vars()


def update_defaults_with_studio() -> None:
    """Update the default values from Studio instance.

    Update only if a database and a Studio instance is present.
    """
    with DBSession.no_autoflush:
        studio = Studio.query.first()
        # studio = DBSession.query(Studio).first()
        logger.debug("studio: {}".format(studio))
        if studio:
            logger.debug("found a studio, updating defaults")
            studio.update_defaults()


def init() -> None:
    """Fill the database with default values."""
    logger.debug("initializing database")

    # register all Actions available for all SOM classes
    class_names = [
        "Asset",
        "AuthenticationLog",
        "Budget",
        "BudgetEntry",
        "Client",
        "Daily",
        "Department",
        "Entity",
        "EntityGroup",
        "File",
        "FilenameTemplate",
        "Good",
        "Group",
        "ImageFormat",
        "Invoice",
        "Message",
        "Note",
        "Page",
        "Payment",
        "Permission",
        "PriceList",
        "Project",
        "Repository",
        "Review",
        "Role",
        "Scene",
        "Sequence",
        "Shot",
        "SimpleEntity",
        "Status",
        "StatusList",
        "Structure",
        "Studio",
        "Tag",
        "Task",
        "Ticket",
        "TicketLog",
        "TimeLog",
        "Type",
        "User",
        "Vacation",
        "Variant",
        "Version",
    ]

    for class_name in class_names:
        _temp = __import__("stalker", globals(), locals(), [class_name], 0)
        class_ = eval("_temp.{}".format(class_name))
        register(class_)

    # create the admin if needed
    admin = None

    if defaults.auto_create_admin:
        admin = __create_admin__()

    # create statuses
    create_ticket_statuses()

    # create statuses for Tickets
    create_entity_statuses(
        entity_type="Daily",
        status_names=defaults.daily_status_names,
        status_codes=defaults.daily_status_codes,
        user=admin,
    )
    create_entity_statuses(
        entity_type="Project",
        status_names=defaults.project_status_names,
        status_codes=defaults.project_status_codes,
        user=admin,
    )
    create_entity_statuses(
        entity_type="Task",
        status_names=defaults.task_status_names,
        status_codes=defaults.task_status_codes,
        user=admin,
    )
    create_entity_statuses(
        entity_type="Review",
        status_names=defaults.review_status_names,
        status_codes=defaults.review_status_codes,
        user=admin,
    )

    # create alembic revision table
    create_alembic_table()

    logger.debug("finished initializing the database")


def create_repo_vars() -> None:
    """Create environment variables for all the repositories in the current database."""
    # get all the repositories
    all_repos = Repository.query.all()
    for repo in all_repos:
        os.environ[repo.env_var] = repo.path


def get_alembic_version() -> Union[None, str]:
    """Return the alembic version of the database.

    Returns:
        str: The alembic version.
    """
    # try to query the version value
    conn = DBSession.connection()
    engine = conn.engine
    if not engine.dialect.has_table(conn, "alembic_version"):
        return None

    sql_query = "select version_num from alembic_version"
    try:
        return DBSession.connection().execute(text(sql_query)).fetchone()[0]
    except (OperationalError, ProgrammingError, TypeError):
        DBSession.rollback()
        return None


def check_alembic_version() -> None:
    """Check the alembic version of the database.

    Raises:
        ValueError: If the alembic version is not matching with current version of
            Stalker.
    """
    current_alembic_version = get_alembic_version()
    logger.debug(f"current_alembic_version: {current_alembic_version}")
    if current_alembic_version and current_alembic_version != alembic_version:
        # invalidate the connection
        DBSession.connection().invalidate()

        # and raise a ValueError (which I'm not sure is the correct exception)
        raise ValueError(f"Please update the database to version: {alembic_version}")


def create_alembic_table() -> None:
    """Create the default alembic_version table.

    Also create the data so that any new database will be considered as the latest
    version.
    """
    # Now, this is not the correct way of doing this, there is a proper way of
    # doing it and it is explained nicely in the Alembic library documentation.
    #
    # But it is simply not working when Stalker is installed as a package.
    #
    # So as a workaround here we are doing it manually
    # don't forget to update the version_num (and the corresponding test
    # whenever a new alembic revision is created)

    version_num = alembic_version
    table_name = "alembic_version"
    conn = DBSession.connection()
    engine = conn.engine

    # check if the table is already there
    table = Table(
        table_name, Base.metadata, Column("version_num", Text), extend_existing=True
    )
    if not engine.dialect.has_table(conn, table_name):
        logger.debug("creating alembic_version table")

        # create the table no matter if it exists or not we need it either way
        Base.metadata.create_all(engine)

    # first try to query the version value
    sql_query = "select version_num from alembic_version"
    try:
        version_num = DBSession.connection().execute(text(sql_query)).fetchone()[0]
    except TypeError:
        logger.debug(f"inserting {version_num} to alembic_version table")
        # the table is there but there is no value so insert it
        ins = table.insert().values(version_num=version_num)
        DBSession.connection().execute(ins)
        DBSession.commit()
        logger.debug("alembic_version table is created and initialized")
    else:
        # the value is there do not touch the table
        logger.debug("alembic_version table is already there, not doing anything!")


def __create_admin__() -> User:
    """Create the admin.

    Returns:
        User: The admin user.
    """
    logger.debug("creating the default administrator user")

    # create the admin department
    admin_department = Department.query.filter_by(
        name=defaults.admin_department_name
    ).first()

    if not admin_department:
        admin_department = Department(name=defaults.admin_department_name)
        DBSession.add(admin_department)
        DBSession.commit()
        # create the admins group
    admins_group = Group.query.filter_by(name=defaults.admin_group_name).first()

    if not admins_group:
        admins_group = Group(name=defaults.admin_group_name)
        DBSession.add(admins_group)

    # check if there is already an admin in the database
    admin = User.query.filter_by(name=defaults.admin_name).first()
    if admin:
        # there should be an admin user do nothing
        logger.debug("there is an admin already")
        return admin
    else:
        admin = User(
            name=defaults.admin_name,
            login=defaults.admin_login,
            password=defaults.admin_password,
            email=defaults.admin_email,
            departments=[admin_department],
            groups=[admins_group],
        )

        DBSession.add(admin)
        DBSession.commit()

        # admin.created_by = admin
        # admin.updated_by = admin

        # update the department as created and updated by admin user
        admin_department.created_by = admin
        admin_department.updated_by = admin

        admins_group.created_by = admin
        admins_group.updated_by = admin

        DBSession.add(admin)
        DBSession.commit()

    return admin


def create_ticket_statuses() -> None:
    """Create the default ticket statuses."""
    # create as admin
    admin = User.query.filter(User.login == defaults.admin_name).first()

    # create statuses for Tickets
    ticket_names = defaults.ticket_status_names
    ticket_codes = defaults.ticket_status_codes
    create_entity_statuses("Ticket", ticket_names, ticket_codes, admin)

    # Again I hate doing this in this way
    types = Type.query.filter_by(target_entity_type="Ticket").all()
    t_names = [t.name for t in types]

    # create Ticket Types
    logger.debug("Creating Ticket Types")
    if "Defect" not in t_names:
        ticket_type_1 = Type(
            name="Defect",
            code="Defect",
            target_entity_type="Ticket",
            created_by=admin,
            updated_by=admin,
        )
        DBSession.add(ticket_type_1)

    if "Enhancement" not in t_names:
        ticket_type_2 = Type(
            name="Enhancement",
            code="Enhancement",
            target_entity_type="Ticket",
            created_by=admin,
            updated_by=admin,
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


def create_entity_statuses(
    entity_type: str = "",
    status_names: Optional[List[str]] = None,
    status_codes: Optional[List[str]] = None,
    user: Optional[User] = None,
) -> None:
    """Create the default task statuses.

    Args:
        entity_type (str): The entity type.
        status_names (List[str]): The list of status names.
        status_codes (List[str]): The list of status codes in the same order of the
            ``status_names`` args.
        user (stalker.model.auth.User): The :class:`stalker.model.auth.User` instance
            to use as the creator for the newly created data.

    Raises:
        ValueError: If entity_type, status_names or status_codes are empty.
    """
    if not entity_type:
        DBSession.rollback()
        raise ValueError("Please supply entity_type")

    if not status_names:
        DBSession.rollback()
        raise ValueError("Please supply status names")

    if not status_codes:
        DBSession.rollback()
        raise ValueError("Please supply status codes")

    # create statuses for entity
    logger.debug(f"Creating {entity_type} Statuses")

    with DBSession.no_autoflush:
        statuses = Status.query.filter(Status.name.in_(status_names)).all()

    logger.debug(f"status_names: {status_names}")
    logger.debug(f"statuses: {statuses}")
    status_names_in_db = list(map(lambda x: x.name, statuses))
    logger.debug(f"statuses_names_in_db: {status_names_in_db}")

    for name, code in zip(status_names, status_codes):
        if name not in status_names_in_db:
            logger.debug(f"Creating Status: {name} ({code})")
            new_status = Status(name=name, code=code, created_by=user, updated_by=user)
            statuses.append(new_status)
            DBSession.add(new_status)
        else:
            logger.debug(f"Status {name} ({code}) is already created skipping!")

    # create the Status List
    status_list = StatusList.query.filter(
        StatusList.target_entity_type == entity_type
    ).first()

    if status_list is None:
        logger.debug(f"No {entity_type} Status List found, creating new!")
        status_list = StatusList(
            name=f"{entity_type} Statuses",
            target_entity_type=entity_type,
            created_by=user,
            updated_by=user,
        )
    else:
        logger.debug(f"{entity_type} Status List already created, updating statuses")

    status_list.statuses = statuses
    DBSession.add(status_list)

    try:
        DBSession.commit()
    except (IntegrityError, OperationalError) as e:
        logger.debug(f"error in DBSession.commit, rolling back: {e}")
        DBSession.rollback()
    else:
        logger.debug(f"Created {entity_type} Statuses successfully")
        DBSession.flush()


def register(class_: Type) -> None:
    """Register the given class to the database.

    It is mainly used to create the :class:`.Action` s needed for the
    :class:`.User` s and :class:`.Group` s to be able to interact with the
    given class. Whatever class you have created needs to be registered.

    Example, let's say that you have a data class which is specific to your
    studio and it is not present in Stalker Object Model (SOM), so you need to
    extend SOM with a new data type. Here is a simple Data class inherited from
    the :class:`.SimpleEntity` class (which is the simplest class you should
    inherit your classes from or use more complex classes down to the
    hierarchy)::

      from sqlalchemy import Column, Integer, ForeignKey
      from sqlalchemy.orm import Mapped, mapped_column
      from stalker.models.entity import SimpleEntity

      class MyDataClass(SimpleEntity):
        '''This is an example class holding a studio specific data which is not
        present in SOM.
        '''

        __tablename__ = 'MyData'
        __mapper_arguments__ = {'polymorphic_identity': 'MyData'}

        my_data_id : Mapped[int] = mapped_column(
            'id',
            ForeignKey('SimpleEntities.c.id'),
            primary_key=True,
        )

    Now because Stalker is using Pyramid authorization mechanism it needs to be
    able to have an :class:`.Permission` about your new class, so you can
    assign this :class;`.Permission` to your :class:`.User` s or
    :class:`.Group` s. So you need to register your new class with
    :func:`stalker.db.register` like shown below::

    .. code-block: python

        from stalker.db import setup
        setup.register(MyDataClass)

    This will create the necessary Actions in the 'Actions' table on your
    database, then you can create :class:`.Permission` s and assign these to
    your :class:`.User` s and :class:`.Group` s so they are Allowed or Denied
    to do the specified Action.

    Args:
        class_ (Type): The class itself that needs to be registered.

    Raises:
        TypeError: If the class_ arg is not a ``type`` instance.
    """
    # create the Permissions
    permissions_db = Permission.query.all()

    if not isinstance(class_, type):
        raise TypeError("To register a class please supply the class itself.")

    # register the class name to entity_types table
    class_name = class_.__name__
    if not EntityType.query.filter_by(name=class_name).first():
        new_entity_type = EntityType(class_name)
        # update attributes
        if issubclass(class_, StatusMixin):
            new_entity_type.statusable = True
        if issubclass(class_, DateRangeMixin):
            new_entity_type.dateable = True
        if issubclass(class_, ScheduleMixin):
            new_entity_type.schedulable = True
        if issubclass(class_, ReferenceMixin):
            new_entity_type.accepts_references = True

        DBSession.add(new_entity_type)

    for action in defaults.actions:
        for access in ["Allow", "Deny"]:
            permission_obj = Permission(access, action, class_name)
            if permission_obj not in permissions_db:
                DBSession.add(permission_obj)

    try:
        DBSession.commit()
    except IntegrityError:
        DBSession.rollback()
