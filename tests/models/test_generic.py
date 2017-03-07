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

from stalker.testing import UnitTestBase


class MakePluralTestCase(UnitTestBase):
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
