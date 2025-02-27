# -*- coding: utf-8 -*-
"""DAGMixin related tests."""

import copy
import sys

import pytest

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from stalker import log
from stalker.db.session import DBSession
from stalker.exceptions import CircularDependencyError
from stalker.models.entity import SimpleEntity
from stalker.models.mixins import DAGMixin

log.get_logger("stalker.models.studio")


class DAGMixinFooMixedInClass(SimpleEntity, DAGMixin):
    """A class which derives from another which has and __init__ already."""

    __tablename__ = "DAGMixinFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "DAGMixinFooMixedInClass"}
    dagMixinFooMixedInClass_id: Mapped[int] = mapped_column(
        "id", ForeignKey("SimpleEntities.id"), primary_key=True
    )
    __id_column__ = "dagMixinFooMixedInClass_id"

    def __init__(self, **kwargs):
        super(DAGMixinFooMixedInClass, self).__init__(**kwargs)
        DAGMixin.__init__(self, **kwargs)


@pytest.fixture(scope="function")
def dag_mixin_test_case():
    """Set up the DAGMixin class tests.

    Returns:
        dict: Test data.
    """
    data = {"kwargs": {"name": "Test DAG Mixin"}}
    return data


@pytest.fixture(scope="function")
def setup_dag_db(setup_postgresql_db):
    """Set up the test for DAGMixin.

    Returns:
        dict: Test data.
    """
    data = setup_postgresql_db
    data["kwargs"] = {"name": "Test DAG Mixin"}
    return data


def test_parent_argument_is_skipped(dag_mixin_test_case):
    """parent attribute is None if the parent argument is skipped."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d = DAGMixinFooMixedInClass(**kwargs)
    assert d.parent is None


def test_parent_argument_is_none(dag_mixin_test_case):
    """parent attribute is None if the parent argument is None."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = None
    d = DAGMixinFooMixedInClass(**kwargs)
    assert d.parent is None


def test_parent_argument_is_not_a_correct_class_instance(dag_mixin_test_case):
    """TypeError is raised if the parent argument is not correct type."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = "not a correct type"
    with pytest.raises(TypeError) as cm:
        _ = DAGMixinFooMixedInClass(**kwargs)

    assert str(cm.value) == (
        "DAGMixinFooMixedInClass.parent should be an instance of "
        "DAGMixinFooMixedInClass class or derivative, not str: 'not a correct type'"
    )


def test_parent_attribute_is_not_a_correct_class_instance(dag_mixin_test_case):
    """TypeError is raised if the parent attribute is set to a wrong class instance."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d = DAGMixinFooMixedInClass(**kwargs)
    with pytest.raises(TypeError) as cm:
        d.parent = "not a correct type"

    assert str(cm.value) == (
        "DAGMixinFooMixedInClass.parent should be an instance of "
        "DAGMixinFooMixedInClass class or derivative, not str: 'not a correct type'"
    )


def test_parent_attribute_creates_a_cycle(dag_mixin_test_case):
    """CircularDependency is raised if a child is tried to be set as the parent."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)

    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = d1
    d2 = DAGMixinFooMixedInClass(**kwargs)

    with pytest.raises(CircularDependencyError) as cm:
        d1.parent = d2

    assert (
        str(cm.value) == "<Test DAG Mixin (DAGMixinFooMixedInClass)> "
        "(DAGMixinFooMixedInClass) and "
        "<Test DAG Mixin (DAGMixinFooMixedInClass)> "
        "(DAGMixinFooMixedInClass) are in a circular dependency in "
        'their "children" attribute'
    )


def test_parent_argument_is_working_as_expected(dag_mixin_test_case):
    """parent argument is working as expected."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)

    kwargs = copy.copy(data["kwargs"])
    kwargs["parent"] = d1

    d2 = DAGMixinFooMixedInClass(**kwargs)
    assert d1 == d2.parent


def test_parent_attribute_is_working_as_expected(dag_mixin_test_case):
    """parent attribute is working as expected."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    d2 = DAGMixinFooMixedInClass(**kwargs)
    assert d2.parent != d1
    d2.parent = d1
    assert d2.parent == d1


def test_children_attribute_is_an_empty_list_by_default(dag_mixin_test_case):
    """children attribute is an empty list by default."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d = DAGMixinFooMixedInClass(**kwargs)
    assert d.children == []


def test_children_attribute_is_set_to_none(dag_mixin_test_case):
    """TypeError is raised if the children attribute is set to None."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d = DAGMixinFooMixedInClass(**kwargs)
    with pytest.raises(TypeError) as cm:
        d.children = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_children_attribute_accepts_correct_class_instances_only(dag_mixin_test_case):
    """children attribute accepts only correct class instances."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d = DAGMixinFooMixedInClass(**kwargs)
    with pytest.raises(TypeError) as cm:
        d.children = ["not", 1, "", "of", "correct", "instances"]

    assert str(cm.value) == (
        "DAGMixinFooMixedInClass.children should only contain instances of "
        "DAGMixinFooMixedInClass (or derivative), not str: 'not'"
    )


def test_children_attribute_is_working_as_expected(dag_mixin_test_case):
    """children attribute is working as expected."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    kwargs["name"] = "Test DAG Mixin 1"
    d1 = DAGMixinFooMixedInClass(**kwargs)
    kwargs["name"] = "Test DAG Mixin 2"
    d2 = DAGMixinFooMixedInClass(**kwargs)
    kwargs["name"] = "Test DAG Mixin 3"
    d3 = DAGMixinFooMixedInClass(**kwargs)

    assert d1.children == []
    d1.children.append(d2)
    assert d1.children == [d2]
    d1.children = [d3]
    assert d1.children == [d3]


def test_is_leaf_attribute_is_read_only(dag_mixin_test_case):
    """is_leaf attribute is a read only attribute."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    with pytest.raises(AttributeError) as cm:
        d1.is_leaf = "this will not work"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'is_leaf'",
    }.get(
        sys.version_info.minor,
        "property 'is_leaf' of 'DAGMixinFooMixedInClass' object has no setter",
    )

    assert str(cm.value) == error_message


def test_is_leaf_attribute_is_working_as_expected(dag_mixin_test_case):
    """is_leaf attribute is True for an instance without a child and False
    for another one with at least one child."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    d2 = DAGMixinFooMixedInClass(**kwargs)
    d3 = DAGMixinFooMixedInClass(**kwargs)
    d1.children = [d2, d3]
    assert d1.is_leaf is False
    assert d2.is_leaf is True
    assert d3.is_leaf is True


def test_is_root_attribute_is_read_only(dag_mixin_test_case):
    """is_root attribute is a read only attribute."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    with pytest.raises(AttributeError) as cm:
        d1.is_root = "this will not work"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'is_root'",
    }.get(
        sys.version_info.minor,
        "property 'is_root' of 'DAGMixinFooMixedInClass' object has no setter",
    )

    assert str(cm.value) == error_message


def test_is_root_attribute_is_working_as_expected(dag_mixin_test_case):
    """is_root is True for an instance without a parent and False otherwise."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    d2 = DAGMixinFooMixedInClass(**kwargs)
    d3 = DAGMixinFooMixedInClass(**kwargs)
    d1.children = [d2, d3]
    assert d1.is_root is True
    assert d2.is_root is False
    assert d3.is_root is False


def test_is_container_attribute_is_read_only(dag_mixin_test_case):
    """is_container attribute is a read only attribute."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    with pytest.raises(AttributeError) as cm:
        d1.is_container = "this will not work"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'is_container'",
    }.get(
        sys.version_info.minor,
        "property 'is_container' of 'DAGMixinFooMixedInClass' object has no setter",
    )

    assert str(cm.value) == error_message


def test_is_container_attribute_working_as_expected(dag_mixin_test_case):
    """is_container is True if at least one child exist and False otherwise."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    d2 = DAGMixinFooMixedInClass(**kwargs)
    d3 = DAGMixinFooMixedInClass(**kwargs)
    d4 = DAGMixinFooMixedInClass(**kwargs)

    d1.children = [d2, d3]
    d2.children = [d4]
    assert d1.is_container is True
    assert d2.is_container is True
    assert d3.is_container is False
    assert d4.is_container is False


def test_parents_property_is_read_only(dag_mixin_test_case):
    """parents property is read-only."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    with pytest.raises(AttributeError) as cm:
        d1.parents = "this will not work"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'parents'",
    }.get(
        sys.version_info.minor,
        "property 'parents' of 'DAGMixinFooMixedInClass' object has no setter",
    )

    assert str(cm.value) == error_message


def test_parents_property_is_working_as_expected(dag_mixin_test_case):
    """parents property is read-only."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    d2 = DAGMixinFooMixedInClass(**kwargs)
    d3 = DAGMixinFooMixedInClass(**kwargs)
    d4 = DAGMixinFooMixedInClass(**kwargs)

    d1.children = [d2, d3]
    d2.children = [d4]

    assert d1.parents == []
    assert d2.parents == [d1]
    assert d3.parents == [d1]
    assert d4.parents == [d1, d2]


def test_walk_hierarchy_is_working_as_expected(dag_mixin_test_case):
    """walk_hierarchy method is working as expected."""
    data = dag_mixin_test_case
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    d2 = DAGMixinFooMixedInClass(**kwargs)
    d3 = DAGMixinFooMixedInClass(**kwargs)
    d4 = DAGMixinFooMixedInClass(**kwargs)

    d1.children = [d2, d3]
    d2.children = [d4]

    entities_walked = []
    for e in d1.walk_hierarchy():
        entities_walked.append(e)
    assert entities_walked == [d1, d2, d4, d3]

    entities_walked = []
    for e in d1.walk_hierarchy(method=1):
        entities_walked.append(e)
    assert entities_walked == [d1, d2, d3, d4]

    entities_walked = []
    for e in d2.walk_hierarchy():
        entities_walked.append(e)
    assert entities_walked == [d2, d4]

    entities_walked = []
    for e in d3.walk_hierarchy():
        entities_walked.append(e)
    assert entities_walked == [d3]

    entities_walked = []
    for e in d4.walk_hierarchy():
        entities_walked.append(e)
    assert entities_walked == [d4]


def test_committing_data(setup_dag_db):
    """Committing and retrieving data back."""
    data = setup_dag_db
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    d2 = DAGMixinFooMixedInClass(**kwargs)
    d3 = DAGMixinFooMixedInClass(**kwargs)
    d4 = DAGMixinFooMixedInClass(**kwargs)

    d1.children = [d2, d3]
    d2.children = [d4]

    DBSession.add_all([d1, d2, d3, d4])
    DBSession.commit()

    del d1, d2, d3, d4

    all_data = DAGMixinFooMixedInClass.query.all()

    assert len(all_data) == 4
    assert isinstance(all_data[0], DAGMixinFooMixedInClass)
    assert isinstance(all_data[1], DAGMixinFooMixedInClass)
    assert isinstance(all_data[2], DAGMixinFooMixedInClass)
    assert isinstance(all_data[3], DAGMixinFooMixedInClass)


def test_deleting_data(setup_dag_db):
    """Deleting data."""
    data = setup_dag_db
    kwargs = copy.copy(data["kwargs"])
    d1 = DAGMixinFooMixedInClass(**kwargs)
    d2 = DAGMixinFooMixedInClass(**kwargs)
    d3 = DAGMixinFooMixedInClass(**kwargs)
    d4 = DAGMixinFooMixedInClass(**kwargs)

    d1.children = [d2, d3]
    d2.children = [d4]

    DBSession.add_all([d1, d2, d3, d4])
    DBSession.commit()

    DBSession.delete(d1)
    DBSession.commit()

    all_data = DAGMixinFooMixedInClass.query.all()
    assert len(all_data) == 0
