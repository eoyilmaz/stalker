# -*- coding: utf-8 -*-
import datetime
import logging
import os
import pytest


HERE = os.path.dirname(__file__)


@pytest.fixture(scope='module')
def setup_sqlite3():
    """setup in memory SQLite3 database for tests
    """
    from stalker.config import Config
    try:
        os.environ.pop(Config.env_key)
    except KeyError:
        # already removed
        pass

    # regenerate the defaults
    import stalker
    stalker.defaults = Config()
    stalker.defaults.timing_resolution = datetime.timedelta(hours=1)

    # Enable Debug logging
    from stalker import logger
    logger.setLevel(logging.DEBUG)


@pytest.fixture
def get_data_file(request):
    """Request a specific datafile."""
    marker = request.node.get_closest_marker("data_file_name")
    if marker is None:
        data_file_name = ""
    else:
        data_file_name = marker.args[0]
    return os.path.join(HERE, "data", data_file_name)
