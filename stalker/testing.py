# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
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


class UnitTestBase(unittest.TestCase):
    """the base for Stalker Pyramid Views unit tests
    """

    config = {
        'sqlalchemy.url':
            'postgresql://stalker_admin:stalker@localhost/stalker_test',
        'sqlalchemy.echo': False
    }

    def setUp(self):
        """setup test
        """
        import datetime
        from stalker import defaults
        defaults.timing_resolution = datetime.timedelta(hours=1)

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
        from stalker import User
        return User.query.filter(User.login == 'admin').first()


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