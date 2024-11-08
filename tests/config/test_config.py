# -*- coding: utf-8 -*-
"""stalker.config module."""
import datetime
import logging
import os
import shutil
import sys
import tempfile

import pytest

from stalker import defaults, config
from stalker.db.session import DBSession
from stalker.models.studio import Studio

logger = logging.getLogger("stalker")
logger.setLevel(logging.DEBUG)


@pytest.fixture(scope="function")
def prepare_config_file():
    """Set up the test."""
    # so we need a temp directory to be specified as our config folder
    temp_config_folder = tempfile.mkdtemp()

    # we should set the environment variable
    os.environ["STALKER_PATH"] = temp_config_folder

    config_full_path = os.path.join(temp_config_folder, "config.py")
    yield config_full_path
    shutil.rmtree(temp_config_folder)


def test_config_variable_updates_with_user_config(prepare_config_file):
    """database_file_name will be updated by the user config."""
    # now create a config.py file and fill it with the desired values
    # like database_file_name = "test_value.db"
    config_full_path = prepare_config_file
    test_value = ".test_value.db"
    config_file = open(config_full_path, "w")
    config_file.writelines(
        [
            "#-*- coding: utf-8 -*-\n",
            f'database_engine_settings = "{test_value}"\n',
        ]
    )
    config_file.close()

    # now import the config.py and see if it updates the
    # database_file_name variable
    conf = config.Config()

    assert test_value == conf.database_engine_settings


def test_config_variable_does_create_new_variables_with_user_config(
    prepare_config_file,
):
    """config will be updated by the user config by adding new variables."""
    config_full_path = prepare_config_file

    # now create a config.py file and fill it with the desired values
    # like database_file_name = "test_value.db"
    test_value = ".test_value.db"
    config_file = open(config_full_path, "w")
    config_file.writelines(
        ["#-*- coding: utf-8 -*-\n", 'test_value = "' + test_value + '"\n']
    )
    config_file.close()

    # now import the config.py and see if it updates the
    # database_file_name variable
    conf = config.Config()

    assert conf.test_value == test_value


def test_env_variable_with_vars_module_import_with_shortcuts(prepare_config_file):
    """module path has shortcuts like ~ and other env variables."""
    config_full_path = prepare_config_file
    temp_config_folder = os.path.dirname(config_full_path)
    splits = os.path.split(temp_config_folder)
    var1 = splits[0]
    var2 = os.path.sep.join(splits[1:])

    os.environ["var1"] = var1
    os.environ["var2"] = var2
    os.environ["STALKER_PATH"] = "$var1/$var2"

    test_value = "sqlite3:///.test_value.db"
    config_file = open(config_full_path, "w")
    config_file.writelines(
        ["#-*- coding: utf-8 -*-\n", 'database_url = "' + test_value + '"\n']
    )
    config_file.close()

    # now import the config.py and see if it updates the
    # database_file_name variable
    conf = config.Config()

    assert test_value == conf.database_url


def test_env_variable_with_deep_vars_module_import_with_shortcuts(prepare_config_file):
    """module path has multiple shortcuts like ~ and other env variables."""
    config_full_path = prepare_config_file
    temp_config_folder = os.path.dirname(config_full_path)
    splits = os.path.split(temp_config_folder)
    var1 = splits[0]
    var2 = os.path.sep.join(splits[1:])
    var3 = os.path.join("$var1", "$var2")

    os.environ["var1"] = var1
    os.environ["var2"] = var2
    os.environ["var3"] = var3
    os.environ["STALKER_PATH"] = "$var3"

    test_value = "sqlite:///.test_value.db"
    config_file = open(config_full_path, "w")
    config_file.writelines(
        ["#-*- coding: utf-8 -*-\n", 'database_url = "' + test_value + '"\n']
    )
    config_file.close()

    # now import the config.py and see if it updates the
    # database_file_name variable
    conf = config.Config()

    assert test_value == conf.database_url


def test_non_existing_path_in_environment_variable():
    """non-existing path situation will be handled gracefully by warning the user."""
    os.environ["STALKER_PATH"] = "/tmp/non_existing_path"
    config.Config()


def test_syntax_error_in_settings_file(prepare_config_file):
    """RuntimeError will be raised when there are syntax errors in the config.py file."""
    config_full_path = prepare_config_file
    temp_config_folder = os.path.dirname(config_full_path)

    # now create a config.py file and fill it with the desired values
    # like database_file_name = "test_value.db"
    # but do a syntax error on purpose, like forgetting the last quote sign
    test_value = ".test_value.db"
    config_file = open(config_full_path, "w")
    config_file.writelines(
        ["#-*- coding: utf-8 -*-\n", 'database_file_name = "' + test_value + "\n"]
    )
    config_file.close()

    # now import the config.py and see if it updates the
    # database_file_name variable
    with pytest.raises(RuntimeError) as cm:
        config.Config()

    error_message = {
        8: "There is a syntax error in your configuration file: "
        "EOL while scanning string literal (<string>, line 2)",
        9: "There is a syntax error in your configuration file: "
        "EOL while scanning string literal (<string>, line 2)",
    }.get(
        sys.version_info.minor,
        "There is a syntax error in your configuration file: "
        "unterminated string literal (detected at line 2) (<string>, line 2)",
    )

    assert str(cm.value) == error_message


def test___setattr___cannot_set_config_values_directly(prepare_config_file):
    """config.Config.__setattr__() method cannot set config values directly."""
    c = config.Config()
    test_value = 1
    c.daily_working_hours = test_value
    assert c.config_values["daily_working_hours"] != test_value


def test___getattr___is_working_as_expected(prepare_config_file):
    """config.Config.__getattr__() method is working as expected."""
    c = config.Config()
    assert c.admin_name == "admin"


def test___getitem___is_working_as_expected(prepare_config_file):
    """config.Config.__getitem__() method is working as expected."""
    c = config.Config()
    assert c["admin_name"] == "admin"


def test___setitem__is_working_as_expected(prepare_config_file):
    """config.Config.__setitem__() method is working as expected."""
    c = config.Config()
    test_value = "administrator"
    assert c["admin_name"] != test_value
    c["admin_name"] = test_value
    assert c["admin_name"] == test_value


def test___delitem__is_working_as_expected(prepare_config_file):
    """config.Config.__delitem__() method is working as expected."""
    c = config.Config()
    assert c["admin_name"] is not None
    del c["admin_name"]
    assert "admin_name" not in c


def test___contains___is_working_as_expected(prepare_config_file):
    """config.Config.__contains__() method is working as expected."""
    c = config.Config()
    assert "admin_name" in c


def test_update_with_studio_is_working_as_expected(setup_postgresql_db):
    """default values are updated with the Studio if there is a DB and a Studio."""
    # check the defaults are still using them self
    assert defaults.timing_resolution == datetime.timedelta(hours=1)

    studio = Studio(
        name="Test Studio", timing_resolution=datetime.timedelta(minutes=15)
    )
    DBSession.add(studio)
    DBSession.commit()

    # now check it again
    assert defaults.timing_resolution == studio.timing_resolution


def test_old_style_repo_env_does_not_exist_anymore():
    """repo_env_var_template_old doesn't exist anymore."""
    assert "repo_env_var_template_old" not in defaults.config_values
