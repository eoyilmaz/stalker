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

import unittest


class MakePluralTestCase(unittest.TestCase):
    """tests stalker.models.make_plural() function
    """

    def test_make_plural_is_working_properly(self):
        """testing if stalker.models.make_plural() function is working properly
        """
        from stalker.models import make_plural
        test_words = [
            ('asset', 'assets'),
            ('client', 'clients'),
            ('department', 'departments'),
            ('entity', 'entities'),
            ('template', 'templates'),
            ('group', 'groups'),
            ('format', 'formats'),
            ('link', 'links'),
            ('session', 'sessions'),
            ('note', 'notes'),
            ('permission', 'permissions'),
            ('project', 'projects'),
            ('repository', 'repositories'),
            ('review', 'reviews'),
            ('scene', 'scenes'),
            ('sequence', 'sequences'),
            ('shot', 'shots'),
            ('status', 'statuses'),
            ('list', 'lists'),
            ('structure', 'structures'),
            ('studio', 'studios'),
            ('tag', 'tags'),
            ('task', 'tasks'),
            ('dependency', 'dependencies'),
            ('type', 'types'),
            ('bench', 'benches'),
            ('thief', 'thieves')
        ]
        for t, e in test_words:
            r = make_plural(t)
            self.assertEqual(r, e)


class DatetimeFunctionsTestCase(unittest.TestCase):
    """tests some utility functions
    """

    def test_utc_to_local_is_working_properly(self):
        """testing if utc_to_local() function is working properly
        """
        from stalker.models import utc_to_local
        import datetime
        import pytz
        local_now = datetime.datetime.now()
        utc_now = datetime.datetime.now(pytz.utc)

        utc_without_tz = datetime.datetime(
            utc_now.year,
            utc_now.month,
            utc_now.day,
            utc_now.hour,
            utc_now.minute,
        )
        local_from_utc = utc_to_local(utc_without_tz)

        self.assertEqual(local_from_utc.year, local_now.year)
        self.assertEqual(local_from_utc.month, local_now.month)
        self.assertEqual(local_from_utc.day, local_now.day)
        self.assertEqual(local_from_utc.hour, local_now.hour)
        self.assertEqual(local_from_utc.minute, local_now.minute)

    def test_local_to_utc_is_working_properly(self):
        """testing if local_to_utc() function is working properly
        """
        from stalker.models import local_to_utc
        import datetime
        import pytz
        local_now = datetime.datetime.now()
        utc_now = datetime.datetime.now(pytz.utc)

        utc_without_tz = datetime.datetime(
            utc_now.year,
            utc_now.month,
            utc_now.day,
            utc_now.hour,
            utc_now.minute,
        )
        utc_from_local = local_to_utc(local_now)

        self.assertEqual(utc_from_local.year, utc_without_tz.year)
        self.assertEqual(utc_from_local.month, utc_without_tz.month)
        self.assertEqual(utc_from_local.day, utc_without_tz.day)
        self.assertEqual(utc_from_local.hour, utc_without_tz.hour)
        self.assertEqual(utc_from_local.minute, utc_without_tz.minute)
