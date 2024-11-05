# -*- coding: utf-8 -*-
import datetime
import os
import platform
import re
import subprocess
import uuid

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import close_all_sessions

from stalker import log, defaults, User
from stalker.db.declarative import Base
from stalker.db.session import DBSession

logger = log.get_logger(__name__)
logger.setLevel(log.logging_level)


# {dialect}://{username}:{password}@{address}/{database_name}
DB_REGEX = re.compile(
    r"(?P<dialect>\w+)"
    r"://"
    r"(?P<username>\w+)"
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
    command="",
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
        psql_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={"PGPASSWORD": password}.update(os.environ)
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

    logger.debug("STDOUT BUFFER")
    logger.debug("=============")
    for line in stdout_buffer:
        logger.debug(line)

    logger.debug("STDERR BUFFER")
    logger.debug("=============")
    for line in stderr_buffer:
        logger.debug(line)

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
        command=command,
    )
    return database_url


def get_server_details_from_url(url):
    """Return database details from the given url.

    Args:
        url (str): Database url in
            dialect}://{user_name}:{password}@{address}/{database_name} format.

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
    command = "DROP DATABASE {};".format(database_name)

    run_db_command(
        database_name=database_name,
        dialect=dialect,
        hostname=hostname,
        port=port,
        username=username,
        password=password,
        command=command,
    )


class PlatformPatcher(object):
    """patches given callable"""

    def __init__(self):
        self.callable = None
        self.original = None

    def patch(self, desired_result):
        """Patch platform."""
        self.original = platform.system

        def f():
            return desired_result

        platform.system = f

    def restore(self):
        """restores the given callable_"""
        if self.original:
            platform.system = self.original


def tear_down_db(data):
    """Utility function to tear a test setup down."""
    # clean up test database
    DBSession.rollback()
    connection = DBSession.connection()
    engine = connection.engine
    connection.close()

    try:
        Base.metadata.drop_all(engine, checkfirst=True)
        DBSession.remove()
        close_all_sessions()
        db_kwargs = get_server_details_from_url(data["database_url"])
        drop_db(**db_kwargs)
    except OperationalError:
        pass
    finally:
        defaults["timing_resolution"] = datetime.timedelta(hours=1)


def get_admin_user():
    """Return admin user from database.

    Returns:
         stalker.User: The admin user
    """
    with DBSession.no_autoflush:
        return User.query.filter(User.login == defaults.admin_login).first()
