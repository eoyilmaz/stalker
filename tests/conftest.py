# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2017 Erkan Ozgur Yilmaz
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

import pytest


@pytest.fixture('module')
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
