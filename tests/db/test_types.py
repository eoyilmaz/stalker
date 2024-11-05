# -*- coding: utf-8 -*-

import pytest

from sqlalchemy import Column, ForeignKey, Integer

from stalker.db.setup import init, setup
from stalker.db.session import DBSession
from stalker.db.types import GenericJSON
from stalker.models.entity import Entity


@pytest.fixture(scope="function")
def setup_db(setup_sqlite3):
    """setup test db."""
    class MyEntityClass(Entity):
        __tablename__ = "MyEntityClasses"
        __table_args__ = {
            "extend_existing": True,
        }
        __mapper_args__ = {
            "polymorphic_identity": "MyEntityClass",
        }
        my_entity_id = Column(
            "id", Integer, ForeignKey("Entities.id"), primary_key=True
        )
        data = Column(GenericJSON)

    # setup and initialize db
    setup()
    init()

    yield MyEntityClass


def test_json_encoded_dict_with_generic_data_stored(setup_db):
    """JSONEncodedDict with generic data."""
    MyEntityClass = setup_db

    my_entity = MyEntityClass()
    my_entity.data = {
        "some key": "and this is the value",
    }
    DBSession.add(my_entity)
    DBSession.commit()


def test_json_encoded_dict_with_generic_data_none_data_stored(setup_db):
    """JSONEncodedDict with generic data."""
    MyEntityClass = setup_db

    my_entity = MyEntityClass()
    my_entity.data = None
    DBSession.add(my_entity)
    DBSession.commit()


def test_json_encoded_dict_with_generic_data_retrieved(setup_db):
    """JSONEncodedDict with generic data."""
    MyEntityClass = setup_db

    test_data = {
        "some key": "and this is the value",
    }

    my_entity = MyEntityClass()
    my_entity.data = test_data
    DBSession.add(my_entity)
    DBSession.commit()

    del(my_entity)

    retrieved_data = MyEntityClass.query.first()
    assert retrieved_data.data == test_data

