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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import datetime
import unittest2

from stalker import User
from stalker.models.studio import Vacation


class VacationTestCase(unittest2.TestCase):
    """tests the stalker.models.studio.Vacation class
    """

    def setUp(self):
        """setup the test
        """
        # create a user
        self.test_user = User(
            name='Test User',
            login='testuser',
            email='testuser@test.com',
            password='secret',
        )

        self.kwargs = {
            'start': datetime.datetime(2013, 6, 6, 10, 0),
            'end': datetime.datetime(2013, 6, 10, 19, 0)
        }

        self.test_vacation = Vacation(**self.kwargs)

