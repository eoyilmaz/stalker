# -*- coding: utf-8 -*-
"""Helper classes for testing
"""

import unittest
import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


def create_db(database_name):
    """creates new PostgreSQL database
    """
    logger.debug('creating database: %s' % database_name)
    import subprocess

    # fallback to check_call for Python 2.6
    try:
        process_caller = subprocess.check_output
    except AttributeError:
        process_caller = subprocess.check_call

    process_caller(
        'psql -c "CREATE DATABASE %s;" -U postgres' % database_name,
        shell=True
    )


def create_random_db():
    """creates a random named PostgreSQL database

    :returns (str, str): db_url, db_name
    """
    # create a new database for this test only
    import uuid
    database_name = 'stalker_test_%s' % uuid.uuid4().hex[:8]
    database_url = 'postgresql://stalker_admin:stalker@localhost/%s' % database_name
    create_db(database_name)
    return database_url, database_name


def drop_db(database_name):
    """drops a PostgreSQL database
    """
    import subprocess
    import time

    # fallback to check_call for Python 2.6
    try:
        process_caller = subprocess.check_output
    except AttributeError:
        process_caller = subprocess.check_call

    while True:
        output = ''
        try:
            output = process_caller(
                'psql -c "DROP DATABASE %s;" -U postgres' % database_name,
                # stderr=subprocess.PIPE,
                shell=True
            )
        except subprocess.CalledProcessError as e:
            # sleep for 1 seconds and run again
            logger.debug(output)
            logger.debug(str(e))
            time.sleep(1)
        else:
            return


class UnitTestDBBase(unittest.TestCase):
    """the base for Stalker Pyramid Views unit tests
    """

    def __init__(self, *args, **kwargs):
        super(UnitTestDBBase, self).__init__(*args, **kwargs)
        self.config = {}
        self.database_url = None
        self.database_name = None

    def setUp(self):
        """setup once
        """
        # create a new database for this test only
        from subprocess import CalledProcessError

        while True:
            try:
                self.database_url, self.database_name = create_random_db()
            except CalledProcessError:
                # in very rare cases the create_random_db generates an already
                # existing database name
                # call it again
                pass
            else:
                break

        # update the config
        self.config['sqlalchemy.url'] = self.database_url
        from sqlalchemy.pool import NullPool
        self.config['sqlalchemy.poolclass'] = NullPool

        import os
        from stalker.config import Config
        try:
            os.environ.pop(Config.env_key)
        except KeyError:
            # already removed
            pass

        # regenerate the defaults
        import stalker
        stalker.defaults = Config()

        import datetime
        stalker.defaults.timing_resolution = datetime.timedelta(hours=1)

        # init database
        from stalker import db
        # remove anything beforehand
        db.setup(self.config)
        db.init()

    def tearDown(self):
        """clean up the test
        """
        import datetime
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
            drop_db(self.database_name)
        except OperationalError:
            pass
        finally:
            defaults.timing_resolution = datetime.timedelta(hours=1)

    @property
    def admin(self):
        """returns the admin user
        """
        from stalker import defaults, User
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            return User.query\
                .filter(User.login == defaults.admin_login)\
                .first()


class PlatformPatcher(object):
    """patches given callable
    """

    def __init__(self):
        self.callable = None
        self.original = None

    def patch(self, desired_result):
        """
        """
        import platform
        self.original = platform.system

        def f():
            return desired_result

        platform.system = f

    def restore(self):
        """restores the given callable_
        """
        if self.original:
            import platform
            platform.system = self.original
