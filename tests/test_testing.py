# -*- coding: utf-8 -*-
"""stalker.testing module."""

import pytest
from tests.utils import get_server_details_from_url


@pytest.mark.parametrize(
    "url,expected",
    [
        (
            "postgresql://postgres:postgres@localhost:5432/stalker_test_e0b9bc6a",
            {
                "dialect": "postgresql",
                "username": "postgres",
                "password": "postgres",
                "hostname": "localhost",
                "port": "5432",
                "database_name": "stalker_test_e0b9bc6a",
            },
        ),
        (
            "postgresql://postgres:postgres@localhost/stalker_test_e0b9bc6a",
            {
                "dialect": "postgresql",
                "username": "postgres",
                "password": "postgres",
                "hostname": "localhost",
                "port": "",
                "database_name": "stalker_test_e0b9bc6a",
            },
        ),
    ],
)
def test_get_server_details_from_url(url, expected):
    """get_server_details_from_url."""
    assert get_server_details_from_url(url) == expected
