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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import os
import pickle
import shutil
import tempfile
import datetime
import unittest2

from stalker import defaults, db, User
from stalker.db import DBSession
from stalker.models.auth import LocalSession


class LocalSessionTester(unittest2.TestCase):
    """tests LocalSession class
    """

    @classmethod
    def setUpClass(cls):
        """setting up the test in class level
        """
        DBSession.remove()
        DBSession.configure(extension=None)

    @classmethod
    def tearDownClass(cls):
        """clean up the test in class level
        """
        DBSession.remove()
        DBSession.configure(extension=None)

    def setUp(self):
        """setup the test
        """
        DBSession.remove()
        db.setup()
        defaults.local_storage_path = tempfile.mktemp()

    def tearDown(self):
        """cleans the test environment
        """
        shutil.rmtree(
            defaults.local_storage_path,
            True
        )

    def test_save_serializes_the_class_itself(self):
        """testing if the save function serializes the class to the filesystem
        """
        new_local_session = LocalSession()
        new_local_session.save()

        # check if a file is created in the users local storage
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    defaults.local_storage_path,
                    defaults.local_session_data_file_name
                )
            )
        )

    def test_LocalSession_initialized_with_previous_session_data(self):
        """testing if the when creating a new LocalSession instance the class
        is restored from previous time
        """
        # test data
        logged_in_user_id = -10

        # create a local_session
        local_session = LocalSession()

        # store some data
        local_session.logged_in_user_id = logged_in_user_id
        local_session.save()

        # now create a new LocalSession
        local_session2 = LocalSession()

        # now try to get the data back
        self.assertEqual(
            local_session2.logged_in_user_id,
            logged_in_user_id
        )

    def test_logged_in_user_returns_the_stored_User_instance_from_last_time(self):
        """testing if logged_in_user returns the logged in user
        """
        # create a new user
        new_user = User(
            name='Test User',
            login='test_user',
            email='test_user@users.com',
            password='secret'
        )

        # save it to the Database
        DBSession.add(new_user)
        DBSession.commit()

        self.assertIsNotNone(new_user.id)

        # save it to the local storage
        local_session = LocalSession()
        local_session.store_user(new_user)

        # save the session
        local_session.save()

        # now get it back with a new local_session
        local_session2 = LocalSession()

        self.assertEqual(
            local_session2.logged_in_user_id,
            new_user.id
        )

        self.assertEqual(
            local_session2.logged_in_user,
            new_user
        )

    def test_LocalSession_will_not_use_the_stored_data_if_it_is_invalid(self):
        """testing if the LocalSession will not use the stored session if it is
        not valid anymore
        """
        # create a new user
        new_user = User(
            name='Test User',
            login='test_user',
            email='test_user@users.com',
            password='secret'
        )

        # save it to the Database
        DBSession.add(new_user)
        DBSession.commit()

        self.assertIsNotNone(new_user.id)

        # save it to the local storage
        local_session = LocalSession()
        local_session.store_user(new_user)

        # save the session
        local_session.save()

        # set the valid time to an early date
        local_session.valid_to = \
            datetime.datetime.now() - datetime.timedelta(10)

        # pickle the data
        local_session._write_data(pickle.dumps(local_session, -1))

        # now get it back with a new local_session
        local_session2 = LocalSession()

        self.assertEqual(
            local_session2.logged_in_user_id, None
        )

        self.assertIsNone(local_session2.logged_in_user)

    def test_delete_will_delete_the_session_cache(self):
        """testing if the LocalSession.delete() will delete the currect cache
        file
        """
        # create a new user
        new_user = User(
            name='Test User',
            login='test_user',
            email='test_user@users.com',
            password='secret'
        )

        # save it to the Database
        DBSession.add(new_user)
        DBSession.commit()

        self.assertIsNotNone(new_user.id)

        # save it to the local storage
        local_session = LocalSession()
        local_session.store_user(new_user)

        # save the session
        local_session.save()

        # check if the file is created
        # check if a file is created in the users local storage
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    defaults.local_storage_path,
                    defaults.local_session_data_file_name
                )
            )
        )

        # now delete the session by calling delete()
        local_session.delete()

        # check if the file is gone
        # check if a file is created in the users local storage
        self.assertFalse(
            os.path.exists(
                os.path.join(
                    defaults.local_storage_path,
                    defaults.local_session_data_file_name
                )
            )
        )
