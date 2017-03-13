# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2017 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>
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
    subprocess.check_output(
        'psql -c "CREATE DATABASE %s;" -U postgres' % database_name,
        shell=True
    )


def create_random_db():
    """creates a random named PostgreSQL database

    :returns (str, str): db_url, db_name
    """
    # create a new database for this test only
    import uuid
    database_name = 'stalker_test_%s' % uuid.uuid4().hex[:4]
    database_url = \
        'postgresql://stalker_admin:stalker@localhost/%s' % database_name
    create_db(database_name)
    return database_url, database_name


def drop_db(database_name):
    """drops a PostgreSQL database
    """
    import subprocess
    import time

    while True:
        output = ''
        try:
            output = subprocess.check_output(
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


class UnitTestBase(unittest.TestCase):
    """the base for Stalker Pyramid Views unit tests
    """

    config = {}
    database_url = None
    database_name = None

    @classmethod
    def setUpClass(cls):
        """setup once
        """
        # create a new database for this test only
        cls.database_url, cls.database_name = create_random_db()

        # update the config
        cls.config['sqlalchemy.url'] = cls.database_url
        from sqlalchemy.pool import NullPool
        cls.config['sqlalchemy.poolclass'] = NullPool

    @classmethod
    def tearDownClass(cls):
        """tear down once
        """
        from stalker import db
        db.DBSession.close_all()
        drop_db(cls.database_name)

    def setUp(self):
        """setup test
        """
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
        db.setup(self.config)

        # remove anything beforehand
        db.init()

    def tearDown(self):
        """clean up the test
        """
        import datetime
        from stalker import db, defaults
        from stalker.db.declarative import Base

        # clean up test database
        db.DBSession.rollback()
        connection = db.DBSession.connection()
        engine = connection.engine
        connection.close()

        Base.metadata.drop_all(engine, checkfirst=True)
        db.DBSession.remove()

        defaults.timing_resolution = datetime.timedelta(hours=1)

    @property
    def admin(self):
        """returns the admin user
        """
        from stalker import User, defaults
        return User.query.filter(User.login == defaults.admin_login).first()


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
