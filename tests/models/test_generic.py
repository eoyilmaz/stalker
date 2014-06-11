# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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
