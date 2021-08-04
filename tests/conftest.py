# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope='module')
def setup_sqlite3():
    """setup in memory SQLite3 database for tests
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

    # Enable Debug logging
    import logging
    from stalker import logger
    logger.setLevel(logging.DEBUG)
