# -*- coding: utf-8 -*-
"""Provides functionality to parse the version number from the VERSION file."""
import os
from typing import Union

VERSION: Union[None, str] = None
VERSION_FILE: str = os.path.join(os.path.dirname(__file__), "VERSION")
if os.path.isfile(VERSION_FILE):
    with open(VERSION_FILE, "r") as f:
        VERSION = f.read().strip()
__version__ = VERSION or "0.0.0"
"""str: The version of the package."""
