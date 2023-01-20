# -*- coding: utf-8 -*-
"""Helper classes for testing
"""
import datetime
import logging
import os
import re
import subprocess
import unittest
import uuid
from subprocess import CalledProcessError

from sqlalchemy.pool import NullPool

import stalker
from stalker import db, log
from stalker.config import Config

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)

# {dialect}://{username}:{password}@{address}/{database_name}
DB_REGEX = re.compile(
    r"(?P<dialect>[\w]+)"
    r"://"
    r"(?P<username>[\w]+)"
    r":"
    r"(?P<password>[\w\s#?!$%^&*\-]+)"
    r"@*"
    r"(?P<hostname>[\w.]+)"
    r":*"
    r"(?P<port>\d*)"
    r"/*"
    r"(?P<database_name>[\w_\-]*)"
)


def run_db_command(
    database_name="testdb",
    dialect="postgresql",
    hostname="localhost",
    port=5432,
    username="postgres",
    password="postgres",
    command=""
):
    """Run db command on a Postgres database.

    Args:
        database_name (str): The database name to create.
        dialect (str): The database dialect, default is postgresql and currently nothing
            else is supported.
        hostname (str): The DB server hostname, default is 'localhost'.
        port (int): The port number, default is 5432.
        username (str): The username, default is 'postgres'.
        password (str): The password, default is 'postgres'.
        command (str): The command to run.

    Returns:
        str: The database url.
    """
    if port == "":
        port = 5432

    psql_command = [
        "psql",
        "--host",
        hostname,
        "--port",
        str(port),
        "--username",
        username,
        "--no-password",
        "--command",
        command,
    ]

    proc = subprocess.Popen(
        psql_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout_buffer = []
    stderr_buffer = []
    while True:
        stdout = proc.stdout.readline().strip()
        stderr = proc.stderr.readline().strip()
        if not isinstance(stdout, str):
            stdout = stdout.decode("utf-8", "replace")
        if not isinstance(stderr, str):
            stderr = stderr.decode("utf-8", "replace")

        if stdout == "" and stderr == "" and proc.poll() is not None:
            break

        if stdout != "":
            stdout_buffer.append(stdout)
        if stderr != "":
            stderr_buffer.append(stderr)

    return stdout_buffer, stderr_buffer


def create_db(
    database_name="testdb",
    dialect="postgresql",
    hostname="localhost",
    port=5432,
    username="postgres",
    password="postgres",
):
    """Create a new Postgres database.

    Args:
        database_name (str): The database name to create.
        dialect (str): The database dialect, default is postgresql and currently nothing
            else is supported.
        hostname (str): The DB server hostname, default is 'localhost'.
        port (int): The port number, default is 5432.
        username (str): The username, default is 'postgres'.
        password (str): The password, default is 'postgres'.

    Returns:
        str: The database url.
    """
    logger.debug("Creating Database: {}".format(database_name))
    if port == "":
        port = 5432  # use default

    database_url = (
        f"{dialect}://{username}:{password}@{hostname}:{port}/{database_name}"
    )

    command = "CREATE DATABASE {};".format(database_name)
    run_db_command(
        database_name=database_name,
        dialect=dialect,
        hostname=hostname,
        port=port,
        username=username,
        password=password,
        command=command
    )
    return database_url


def get_server_details_from_url(url):
    """Return database details from the given url.

    Args:
        url (str): Database url in {dialect}://{user_name}:{password}@{address}/{database_name}
            format.

    Returns:
        dict: Returns a dictionary with "dialect", "user_name", "password", "address",
            "database_name" keys.
    """
    return_val = dict()
    match = DB_REGEX.match(url)
    if match:
        return_val = match.groupdict()
    return return_val


def create_random_db():
    """creates a random named Postgres database

    :returns (str): db_url
    """
    # create a new database for this test only
    database_url = os.environ.get(
        "STALKER_TEST_DB", "postgresql://postgres:postgres@localhost/testdb"
    )
    database_name = "stalker_test_{}".format(uuid.uuid4().hex[:8])

    # get server details
    db_kwargs = get_server_details_from_url(database_url)

    # replace database name
    db_kwargs["database_name"] = database_name

    return create_db(**db_kwargs)


def drop_db(
    database_name="testdb",
    dialect="postgresql",
    hostname="localhost",
    port=5432,
    username="postgres",
    password="postgres",
):
    """Drop the given Postgres database.

    Args:
        database_name (str): The database name to create.
        dialect (str): The database dialect, default is postgresql and currently nothing
            else is supported.
        hostname (str): The DB server hostname, default is 'localhost'.
        port (Union[str, int]): The port number, default is 5432.
        username (str): The username, default is 'postgres'.
        password (str): The password, default is 'postgres'.
    """
    logger.debug("Dropping Database: {}".format(database_name))
    command = "DROP   DATABASE {};".format(database_name)

    run_db_command(
        database_name=database_name,
        dialect=dialect,
        hostname=hostname,
        port=port,
        username=username,
        password=password,
        command=command
    )


class UnitTestDBBase(unittest.TestCase):
    """the base for Stalker Pyramid Views unit tests"""

    def __init__(self, *args, **kwargs):
        super(UnitTestDBBase, self).__init__(*args, **kwargs)
        self.config = {}
        self.database_url = None

    def setUp(self):
        """setup once"""
        # create a new database for this test only
        while True:
            try:
                self.database_url = create_random_db()
            except CalledProcessError:
                # in very rare cases the create_random_db generates an already
                # existing database name
                # call it again
                pass
            else:
                break

        # update the config
        self.config["sqlalchemy.url"] = self.database_url
        self.config["sqlalchemy.poolclass"] = NullPool

        try:
            os.environ.pop(Config.env_key)
        except KeyError:
            # already removed
            pass

        # regenerate the defaults
        stalker.defaults = Config()
        stalker.defaults.timing_resolution = datetime.timedelta(hours=1)

        # init database
        # remove anything beforehand
        db.setup(self.config)
        db.init()

    def tearDown(self):
        """clean up the test"""
        from stalker import defaults
        from stalker.db.declarative import Base
        from stalker.db.session import DBSession

        # clean up test database
        DBSession.rollback()
        connection = DBSession.connection()
        engine = connection.engine
        connection.close()

        from sqlalchemy.exc import OperationalError

        try:
            Base.metadata.drop_all(engine, checkfirst=True)
            DBSession.remove()
            DBSession.close_all()
            db_kwargs = get_server_details_from_url(self.database_url)
            drop_db(**db_kwargs)
        except OperationalError:
            pass
        finally:
            defaults.timing_resolution = datetime.timedelta(hours=1)

    @property
    def admin(self):
        """returns the admin user"""
        from stalker import defaults, User
        from stalker.db.session import DBSession

        with DBSession.no_autoflush:
            return User.query.filter(User.login == defaults.admin_login).first()


class PlatformPatcher(object):
    """patches given callable"""

    def __init__(self):
        self.callable = None
        self.original = None

    def patch(self, desired_result):
        """ """
        import platform

        self.original = platform.system

        def f():
            return desired_result

        platform.system = f

    def restore(self):
        """restores the given callable_"""
        if self.original:
            import platform

            platform.system = self.original
