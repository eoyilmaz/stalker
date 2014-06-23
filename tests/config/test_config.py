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

import os
import shutil
import tempfile
import datetime
import unittest
import logging
import stalker

logger = logging.getLogger("stalker")
logger.setLevel(logging.DEBUG)


class ConfigTester(unittest.TestCase):
    """test the system configuration
    """

    def setUp(self):
        """setup the test
        """
        # so we need a temp directory to be specified as our config folder
        self.temp_config_folder = tempfile.mkdtemp()

        # we should set the environment variable
        os.environ["STALKER_PATH"] = self.temp_config_folder

        self.config_full_path = os.path.join(
            self.temp_config_folder, "config.py"
        )

    def tearDown(self):
        """clean up the test
        """
        from stalker.db import DBSession
        DBSession.remove()

        # and remove the temp directory
        shutil.rmtree(self.temp_config_folder)
        # restore defaults.timing_resolution
        stalker.defaults.timing_resolution = datetime.timedelta(hours=1)

    def test_config_variable_updates_with_user_config(self):
        """testing if the database_file_name will be updated by the user
        config
        """
        # now create a config.py file and fill it with the desired values
        # like database_file_name = "test_value.db"
        test_value = ".test_value.db"
        config_file = open(self.config_full_path, "w")
        config_file.writelines([
            "#-*- coding: utf-8 -*-\n",
            'database_engine_settings = "%s"\n' % test_value
        ])
        config_file.close()

        # now import the config.py and see if it updates the
        # database_file_name variable
        from stalker import config
        conf = config.Config()

        self.assertEqual(test_value, conf.database_engine_settings)

    def test_config_variable_does_create_new_variables_with_user_config(self):
        """testing if the config will be updated by the user config by adding
        new variables
        """
        # now create a config.py file and fill it with the desired values
        # like database_file_name = "test_value.db"
        test_value = ".test_value.db"
        config_file = open(self.config_full_path, "w")
        config_file.writelines(["#-*- coding: utf-8 -*-\n",
                                'test_value = "' + test_value + '"\n'])
        config_file.close()

        # now import the config.py and see if it updates the
        # database_file_name variable
        from stalker import config
        conf = config.Config()

        #self.assertRaises(KeyError, getattr, conf, "test_value")
        self.assertEqual(conf.test_value, test_value)

    def test_env_variable_with_vars_module_import_with_shortcuts(self):
        """testing if the module path has shortcuts like ~ and other env
        variables
        """
        splits = os.path.split(self.temp_config_folder)
        var1 = splits[0]
        var2 = os.path.sep.join(splits[1:])

        os.environ["var1"] = var1
        os.environ["var2"] = var2
        os.environ["STALKER_PATH"] = "$var1/$var2"

        test_value = "sqlite3:///.test_value.db"
        config_file = open(self.config_full_path, "w")
        config_file.writelines(["#-*- coding: utf-8 -*-\n",
                                'database_url = "' + test_value + '"\n'])
        config_file.close()

        # now import the config.py and see if it updates the
        # database_file_name variable
        from stalker import config
        conf = config.Config()

        self.assertEqual(test_value, conf.database_url)

    def test_env_variable_with_deep_vars_module_import_with_shortcuts(self):
        """testing if the module path has multiple shortcuts like ~ and other
        env variables
        """
        splits = os.path.split(self.temp_config_folder)
        var1 = splits[0]
        var2 = os.path.sep.join(splits[1:])
        var3 = os.path.join("$var1", "$var2")

        os.environ["var1"] = var1
        os.environ["var2"] = var2
        os.environ["var3"] = var3
        os.environ["STALKER_PATH"] = "$var3"

        test_value = "sqlite:///.test_value.db"
        config_file = open(self.config_full_path, "w")
        config_file.writelines(["#-*- coding: utf-8 -*-\n",
                                'database_url = "' + test_value + '"\n'])
        config_file.close()

        # now import the config.py and see if it updates the
        # database_file_name variable
        from stalker import config
        conf = config.Config()

        self.assertEqual(test_value, conf.database_url)

    def test_non_existing_path_in_environment_variable(self):
        """testing if the non existing path situation will be handled
        gracefully by warning the user
        """
        os.environ["STALKER_PATH"] = "/tmp/non_existing_path"
        from stalker import config
        config.Config()

    def test_syntax_error_in_settings_file(self):
        """testing if a RuntimeError will be raised when there are syntax
        errors in the config.py file
        """
        # now create a config.py file and fill it with the desired values
        # like database_file_name = "test_value.db"
        # but do a syntax error on purpose, like forgetting the last quote sign
        test_value = ".test_value.db"
        config_file = open(self.config_full_path, "w")
        config_file.writelines(["#-*- coding: utf-8 -*-\n",
                                'database_file_name = "' + test_value + '\n'])
        config_file.close()

        # now import the config.py and see if it updates the
        # database_file_name variable
        from stalker import config
        self.assertRaises(RuntimeError, config.Config)

    def test_update_with_studio_is_working_properly(self):
        """testing if the default values are updated with the Studio instance
        if there is a database connection and there is a Studio in there
        """
        import datetime
        from stalker import db, defaults
        from stalker.db.session import DBSession
        from stalker.models.studio import Studio

        db.setup()
        db.init()

        # check the defaults are still using them self
        self.assertEqual(
            defaults.timing_resolution,
            datetime.timedelta(hours=1)
        )

        studio = Studio(
            name='Test Studio',
            timing_resolution=datetime.timedelta(minutes=15)
        )
        DBSession.add(studio)
        DBSession.commit()

        # now check it again
        self.assertEqual(
            defaults.timing_resolution,
            studio.timing_resolution
        )
