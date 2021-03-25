# -*- coding: utf-8 -*-

import copy
import unittest
import pytest
from sqlalchemy import Column, Integer, ForeignKey

from stalker.exceptions import CircularDependencyError
from stalker.models.entity import SimpleEntity
from stalker.models.mixins import DAGMixin

import logging

from stalker.testing import UnitTestDBBase

logging.getLogger('stalker.models.studio').setLevel(logging.DEBUG)


class DAGMixinFooMixedInClass(SimpleEntity, DAGMixin):
    """a class which derives from another which has and __init__ already
    """
    __tablename__ = "DAGMixinFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "DAGMixinFooMixedInClass"}
    dagMixinFooMixedInClass_id = Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )
    __id_column__ = 'dagMixinFooMixedInClass_id'

    def __init__(self, **kwargs):
        super(DAGMixinFooMixedInClass, self).__init__(**kwargs)
        DAGMixin.__init__(self, **kwargs)


class DAGMixinTestCase(unittest.TestCase):
    """tests the DAGMixin class
    """

    def setUp(self):
        """set the test up
        """
        self.kwargs = {
            'name': 'Test DAG Mixin'
        }

    def test_parent_argument_is_skipped(self):
        """testing if the parent attribute will be None if the parent argument
        is skipped
        """
        kwargs = copy.copy(self.kwargs)
        d = DAGMixinFooMixedInClass(**kwargs)
        assert d.parent is None

    def test_parent_argument_is_None(self):
        """testing if the parent attribute will be None if the parent argument
        is None
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['parent'] = None
        d = DAGMixinFooMixedInClass(**kwargs)
        assert d.parent is None

    def test_parent_argument_is_not_a_correct_class_instance(self):
        """testing if a TypeError will be raised if the parent argument is not
        in correct class
        """
        kwargs = copy.copy(self.kwargs)

        kwargs['parent'] = 'not a correct type'
        with pytest.raises(TypeError) as cm:
            d = DAGMixinFooMixedInClass(**kwargs)

        assert str(cm.value) == \
            'DAGMixinFooMixedInClass.parent should be an instance of ' \
            'DAGMixinFooMixedInClass class or derivative, not str'

    def test_parent_attribute_is_not_a_correct_class_instance(self):
        """testing if a TypeError will be raised if the parent attribute is set
        to a wrong class instance
        """
        kwargs = copy.copy(self.kwargs)
        d = DAGMixinFooMixedInClass(**kwargs)
        with pytest.raises(TypeError) as cm:
            d.parent = 'not a correct type'

        assert str(cm.value) == \
            'DAGMixinFooMixedInClass.parent should be an instance of ' \
            'DAGMixinFooMixedInClass class or derivative, not str'

    def test_parent_attribute_creates_a_cycle(self):
        """testing if a CircularDependency will be raised if a child is tried
        to be set as the parent.
        """
        kwargs = copy.copy(self.kwargs)
        d1 = DAGMixinFooMixedInClass(**kwargs)

        kwargs = copy.copy(self.kwargs)
        kwargs['parent'] = d1
        d2 = DAGMixinFooMixedInClass(**kwargs)

        with pytest.raises(CircularDependencyError) as cm:
            d1.parent = d2

        assert str(cm.value) == \
            '<Test DAG Mixin (DAGMixinFooMixedInClass)> ' \
            '(DAGMixinFooMixedInClass) and ' \
            '<Test DAG Mixin (DAGMixinFooMixedInClass)> ' \
            '(DAGMixinFooMixedInClass) creates a circular dependency in ' \
            'their "children" attribute'

    def test_parent_argument_is_working_properly(self):
        """testing if the parent argument is working properly
        """
        kwargs = copy.copy(self.kwargs)
        d1 = DAGMixinFooMixedInClass(**kwargs)

        kwargs = copy.copy(self.kwargs)
        kwargs['parent'] = d1

        d2 = DAGMixinFooMixedInClass(**kwargs)
        assert d1 == d2.parent

    def test_parent_attribute_is_working_properly(self):
        """testing if the parent attribute is working properly
        """
        kwargs = copy.copy(self.kwargs)
        d1 = DAGMixinFooMixedInClass(**kwargs)
        d2 = DAGMixinFooMixedInClass(**kwargs)
        assert d2.parent != d1
        d2.parent = d1
        assert d2.parent == d1

    def test_children_attribute_is_an_empty_list_by_default(self):
        """testing if the children attribute is an empty list by default
        """
        kwargs = copy.copy(self.kwargs)
        d = DAGMixinFooMixedInClass(**kwargs)
        assert d.children == []

    def test_children_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the children attribute is
        set to None
        """
        kwargs = copy.copy(self.kwargs)
        d = DAGMixinFooMixedInClass(**kwargs)
        with pytest.raises(TypeError) as cm:
            d.children = None

        assert str(cm.value) == \
            'Incompatible collection type: None is not list-like'

    def test_children_attribute_accepts_correct_class_instances_only(self):
        """testing if the children attribute accepts only correct class
        instances
        """
        kwargs = copy.copy(self.kwargs)
        d = DAGMixinFooMixedInClass(**kwargs)
        with pytest.raises(TypeError) as cm:
            d.children = ['not', 1, '', 'of', 'correct', 'instances']

        assert str(cm.value) == \
            'DAGMixinFooMixedInClass.children should be a list of ' \
            'DAGMixinFooMixedInClass (or derivative) instances, not str'

    def test_children_attribute_is_working_properly(self):
        """testing if the children attribute is working properly
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['name'] = 'Test DAG Mixin 1'
        d1 = DAGMixinFooMixedInClass(**kwargs)
        kwargs['name'] = 'Test DAG Mixin 2'
        d2 = DAGMixinFooMixedInClass(**kwargs)
        kwargs['name'] = 'Test DAG Mixin 3'
        d3 = DAGMixinFooMixedInClass(**kwargs)

        assert d1.children == []
        d1.children.append(d2)
        assert d1.children == [d2]
        d1.children = [d3]
        assert d1.children == [d3]

    def test_is_leaf_attribute_is_read_only(self):
        """testing if the is_leaf attribute is a read only attribute
        """
        kwargs = copy.copy(self.kwargs)
        d1 = DAGMixinFooMixedInClass(**kwargs)
        with pytest.raises(AttributeError) as cm:
            setattr(d1, 'is_leaf', 'this will not work')

        assert str(cm.value) == "can't set attribute"

    def test_is_leaf_attribute_is_working_properly(self):
        """testing if the is_leaf attribute is True for an instance without a
        child and False for another one with at least one child
        """
        kwargs = copy.copy(self.kwargs)
        d1 = DAGMixinFooMixedInClass(**kwargs)
        d2 = DAGMixinFooMixedInClass(**kwargs)
        d3 = DAGMixinFooMixedInClass(**kwargs)
        d1.children = [d2, d3]
        assert d1.is_leaf is False
        assert d2.is_leaf is True
        assert d3.is_leaf is True

    def test_is_root_attribute_is_read_only(self):
        """testing if the is_root attribute is a read only attribute
        """
        kwargs = copy.copy(self.kwargs)
        d1 = DAGMixinFooMixedInClass(**kwargs)
        with pytest.raises(AttributeError) as cm:
            setattr(d1, 'is_root', 'this will not work')

        assert str(cm.value) == "can't set attribute"

    def test_is_root_attribute_is_working_properly(self):
        """testing if the is_root attribute is True for an instance without a
        parent and False for another instance with a parent
        """
        kwargs = copy.copy(self.kwargs)
        d1 = DAGMixinFooMixedInClass(**kwargs)
        d2 = DAGMixinFooMixedInClass(**kwargs)
        d3 = DAGMixinFooMixedInClass(**kwargs)
        d1.children = [d2, d3]
        assert d1.is_root is True
        assert d2.is_root is False
        assert d3.is_root is False

    def test_is_container_attribute_is_read_only(self):
        """testing if the is_container attribute is a read only attribute
        """
        kwargs = copy.copy(self.kwargs)
        d1 = DAGMixinFooMixedInClass(**kwargs)
        with pytest.raises(AttributeError) as cm:
            setattr(d1, 'is_container', 'this will not work')

        assert str(cm.value) == "can't set attribute"

    def test_is_container_attribute_working_properly(self):
        """testing if the is_container attribute is True for an instance with
        at least one child and False for another with no child
        """
        kwargs = copy.copy(self.kwargs)
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

    def test_parents_property_is_read_only(self):
        """testing if the parents property is read-only
        """
        kwargs = copy.copy(self.kwargs)
        d1 = DAGMixinFooMixedInClass(**kwargs)
        with pytest.raises(AttributeError) as cm:
            setattr(d1, 'parents', 'this will not work')

        assert str(cm.value) == "can't set attribute"

    def test_parents_property_is_working_properly(self):
        """testing if the parents property is read-only
        """
        kwargs = copy.copy(self.kwargs)
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

    def test_walk_hierarchy_is_working_properly(self):
        """testing if the walk_hierarchy method is working properly
        """
        kwargs = copy.copy(self.kwargs)
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


class DAGMixinDBTestDBCase(UnitTestDBBase):
    """tests the DAGMixin class with a DB
    """

    def setUp(self):
        """set the test up
        """
        super(DAGMixinDBTestDBCase, self).setUp()
        self.kwargs = {
            'name': 'Test DAG Mixin'
        }

    def test_committing_data(self):
        """testing committing and retrieving data back
        """
        kwargs = copy.copy(self.kwargs)
        d1 = DAGMixinFooMixedInClass(**kwargs)
        d2 = DAGMixinFooMixedInClass(**kwargs)
        d3 = DAGMixinFooMixedInClass(**kwargs)
        d4 = DAGMixinFooMixedInClass(**kwargs)

        d1.children = [d2, d3]
        d2.children = [d4]

        from stalker.db.session import DBSession
        DBSession.add_all([d1, d2, d3, d4])
        DBSession.commit()

        del d1, d2, d3, d4

        all_data = DAGMixinFooMixedInClass.query.all()

        assert len(all_data) == 4
        assert isinstance(all_data[0], DAGMixinFooMixedInClass)
        assert isinstance(all_data[1], DAGMixinFooMixedInClass)
        assert isinstance(all_data[2], DAGMixinFooMixedInClass)
        assert isinstance(all_data[3], DAGMixinFooMixedInClass)

    def test_deleting_data(self):
        """testing deleting data
        """
        kwargs = copy.copy(self.kwargs)
        d1 = DAGMixinFooMixedInClass(**kwargs)
        d2 = DAGMixinFooMixedInClass(**kwargs)
        d3 = DAGMixinFooMixedInClass(**kwargs)
        d4 = DAGMixinFooMixedInClass(**kwargs)

        d1.children = [d2, d3]
        d2.children = [d4]

        from stalker.db.session import DBSession
        DBSession.add_all([d1, d2, d3, d4])
        DBSession.commit()

        DBSession.delete(d1)
        DBSession.commit()

        all_data = DAGMixinFooMixedInClass.query.all()
        assert len(all_data) == 0
