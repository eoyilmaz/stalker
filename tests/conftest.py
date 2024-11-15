# -*- coding: utf-8 -*-
"""Configure tests."""
import datetime
import logging
import os
from subprocess import CalledProcessError

import pytest

from sqlalchemy.pool import NullPool

import stalker
import stalker.db.setup
from stalker import db, defaults, log, User
from stalker.config import Config
from stalker.db.session import DBSession

from tests.utils import create_random_db, tear_down_db

logger = logging.getLogger(__name__)
log.register_logger(logger)
log.set_level(logging.DEBUG)

HERE = os.path.dirname(__file__)


@pytest.fixture(scope="function")
def setup_sqlite3():
    """Set up in memory SQLite3 database for tests."""
    try:
        os.environ.pop(Config.env_key)
    except KeyError:
        # already removed
        pass

    # regenerate the defaults
    stalker.defaults.config_values = stalker.defaults.default_config_values.copy()
    stalker.defaults["timing_resolution"] = datetime.timedelta(hours=1)

    # Enable Debug logging
    log.set_level(logging.DEBUG)
    yield
    tear_down_db({})


@pytest.fixture
def get_data_file(request):
    """Request a specific datafile.

    Args:
        request: pytest.request object.

    Returns:
        str: Desired data file path.
    """
    if isinstance(request.param, str):
        return os.path.join(HERE, "data", request.param)
    elif isinstance(request.param, list):
        output = []
        for path in request.param:
            output.append(os.path.join(HERE, "data", path))
        return output


@pytest.fixture(scope="function")
def setup_postgresql_db():
    """Set up Postgresql database.

    Yields:
        dict: Test data storage.
    """
    data = {"config": {}, "database_url": None}

    # create a new database for this test only
    while True:
        try:
            data["database_url"] = create_random_db()
        except CalledProcessError:
            # in very rare cases the create_random_db generates an already
            # existing database name
            # call it again
            pass
        else:
            break

    # update the config
    data["config"]["sqlalchemy.url"] = data["database_url"]
    data["config"]["sqlalchemy.poolclass"] = NullPool

    try:
        os.environ.pop(Config.env_key)
    except KeyError:
        # already removed
        pass

    # regenerate the defaults
    stalker.defaults.config_values = stalker.defaults.default_config_values.copy()
    stalker.defaults["timing_resolution"] = datetime.timedelta(hours=1)

    # init database
    # remove anything beforehand
    stalker.db.setup.setup(data["config"])
    stalker.db.setup.init()

    yield data
    tear_down_db(data)
