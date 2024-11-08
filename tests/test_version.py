# -*- coding: utf-8 -*-
import os

# Local Imports
import stalker
from stalker import version


def test_version_number_is_correct():
    """version.VERSION is correct."""
    version_file_path = os.path.join(os.path.dirname(stalker.__file__), "VERSION")
    with open(version_file_path) as f:
        expected_version = f.read().strip()
    assert expected_version == version.__version__


def test_version_number_as_a_module_level_variable():
    """stalker.__version__ exists and value is correct."""
    assert version.__version__ == stalker.__version__
