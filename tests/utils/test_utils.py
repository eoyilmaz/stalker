# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest
from stalker import utils


class UtilsTester(unittest.TestCase):
    """tests the stalker.utils
    """


    def test_path_to_exec(self):
        """testing if a correct string will be returned with path_to_exec
        """

        full_path = "stalker.core.models.Asset"

        expected_result = ("from stalker.core.models import Asset",
                           "stalker.core.models",
                           "Asset")

        self.assertEqual(
            utils.path_to_exec(full_path),
            expected_result
        )
