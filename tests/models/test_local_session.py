# -*- coding: utf-8 -*-
"""Tests for the LocalSession class."""

import datetime
import json
import os
import shutil
import tempfile

import pytest

import pytz

from stalker import LocalSession, User, defaults
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def setup_local_session_tester():
    """Set up the LocalSession related tests."""
    defaults["local_storage_path"] = tempfile.mktemp()
    yield
    shutil.rmtree(defaults.local_storage_path, True)


def test_save_serializes_the_class_itself(setup_local_session_tester):
    """save function serializes the class to the filesystem."""
    new_local_session = LocalSession()
    new_local_session.save()

    # check if a file is created in the users local storage
    assert os.path.exists(
        os.path.join(defaults.local_storage_path, defaults.local_session_data_file_name)
    )


def test_save_serializes_the_class_itself_with_real_data(setup_local_session_tester):
    """save function serializes the class to the filesystem."""
    new_local_session = LocalSession()
    new_local_session.logged_in_user_id = 1
    new_local_session.save()

    # check if a file is created in the users local storage
    assert os.path.exists(
        os.path.join(defaults.local_storage_path, defaults.local_session_data_file_name)
    )


def test_local_session_initialized_with_previous_session_data(
    setup_local_session_tester,
):
    """new LocalSession instance the class is restored from previous session."""
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
    assert local_session2.logged_in_user_id == logged_in_user_id


def test_delete_will_delete_the_session_cache(setup_local_session_tester):
    """LocalSession.delete() will delete the current cache file."""
    # create a new user
    new_user = User(
        name="Test User",
        login="test_user",
        email="test_user@users.com",
        password="secret",
    )

    # save it to the Database
    new_user.id = 1023
    assert new_user.id is not None

    # save it to the local storage
    local_session = LocalSession()
    local_session.store_user(new_user)

    # save the session
    local_session.save()

    # check if the file is created
    # check if a file is created in the users local storage
    assert os.path.exists(
        os.path.join(defaults.local_storage_path, defaults.local_session_data_file_name)
    )

    # now delete the session by calling delete()
    local_session.delete()

    # check if the file is gone
    # check if a file is created in the users local storage
    assert not os.path.exists(
        os.path.join(defaults.local_storage_path, defaults.local_session_data_file_name)
    )

    # delete a second time
    # this should not raise an OSError
    local_session.delete()


def test_local_session_will_not_use_the_stored_data_if_it_is_invalid(
    setup_postgresql_db,
):
    """LocalSession will not use the stored session if it is not valid anymore."""
    # create a new user
    new_user = User(
        name="Test User",
        login="test_user",
        email="test_user@users.com",
        password="secret",
    )

    # save it to the Database
    DBSession.add(new_user)
    DBSession.commit()
    assert new_user.id is not None

    # save it to the local storage
    local_session = LocalSession()
    local_session.store_user(new_user)

    # save the session
    local_session.save()

    # set the valid time to an early date
    local_session.valid_to = datetime.datetime.now(pytz.utc) - datetime.timedelta(10)

    # pickle the data
    data = json.dumps(
        {
            "valid_to": local_session.datetime_to_millis(local_session.valid_to),
            "logged_in_user_id": -1
        },
    )
    local_session._write_data(data)

    # now get it back with a new local_session
    local_session2 = LocalSession()

    assert local_session2.logged_in_user_id is None
    assert local_session2.logged_in_user is None


def test_logged_in_user_returns_the_stored_user_instance_from_last_time(
    setup_postgresql_db,
):
    """logged_in_user returns the logged in user."""
    # create a new user
    new_user = User(
        name="Test User",
        login="test_user",
        email="test_user@users.com",
        password="secret",
    )

    # save it to the Database
    DBSession.add(new_user)
    DBSession.commit()
    assert new_user.id is not None

    # save it to the local storage
    local_session = LocalSession()
    local_session.store_user(new_user)

    # save the session
    local_session.save()

    # now get it back with a new local_session
    local_session2 = LocalSession()

    assert local_session2.logged_in_user_id == new_user.id
    assert local_session2.logged_in_user == new_user
