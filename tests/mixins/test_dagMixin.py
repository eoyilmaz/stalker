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

import unittest

from sqlalchemy import Column, Integer, ForeignKey

from stalker import db
from stalker.exceptions import CircularDependencyError
from stalker.models.entity import SimpleEntity
from stalker.models.mixins import DAGMixin

import logging
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
        # db.setup({'sqlalchemy.url': 'sqlite:///:memory:'})

        self.kwargs = {
            'name': 'Test DAG Mixin'
        }

    def tearDown(self):
        """clean up the test
        """
        # DBSession.remove()

    def test_parent_argument_is_skipped(self):
        """testing if the parent attribute will be None if the parent argument
        is skipped
        """
        d = DAGMixinFooMixedInClass(**self.kwargs)
        self.assertTrue(d.parent is None)

    def test_parent_argument_is_None(self):
        """testing if the parent attribute will be None if the parent argument
        is None
        """
        self.kwargs['parent'] = None
        d = DAGMixinFooMixedInClass(**self.kwargs)
        self.assertTrue(d.parent is None)

    def test_parent_argument_is_not_a_correct_class_instance(self):
        """testing if a TypeError will be raised if the parent argument is not
        in correct class
        """
        self.kwargs['parent'] = 'not a correct type'
        with self.assertRaises(TypeError) as cm:
            d = DAGMixinFooMixedInClass(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'DAGMixinFooMixedInClass.parent should be an instance of '
            'DAGMixinFooMixedInClass class or derivative, not str'
        )

    def test_parent_attribute_is_not_a_correct_class_instance(self):
        """testing if a TypeError will be raised if the parent attribute is set
        to a wrong class instance
        """
        d = DAGMixinFooMixedInClass(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            d.parent = 'not a correct type'

        self.assertEqual(
            str(cm.exception),
            'DAGMixinFooMixedInClass.parent should be an instance of '
            'DAGMixinFooMixedInClass class or derivative, not str'
        )

    def test_parent_attribute_creates_a_cycle(self):
        """testing if a CircularDependency will be raised if a child is tried
        to be set as the parent.
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)

        self.kwargs['parent'] = d1
        d2 = DAGMixinFooMixedInClass(**self.kwargs)

        with self.assertRaises(CircularDependencyError) as cm:
            d1.parent = d2

        self.assertEqual(
            str(cm.exception),
            '\'<Test DAG Mixin (DAGMixinFooMixedInClass)> '
            '(DAGMixinFooMixedInClass) and '
            '<Test DAG Mixin (DAGMixinFooMixedInClass)> '
            '(DAGMixinFooMixedInClass) creates a circular dependency in their '
            '"children" attribute\''
        )

    def test_parent_argument_is_working_properly(self):
        """testing if the parent argument is working properly
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        self.kwargs['parent'] = d1

        d2 = DAGMixinFooMixedInClass(**self.kwargs)
        self.assertEqual(d1, d2.parent)

    def test_parent_attribute_is_working_properly(self):
        """testing if the parent attribute is working properly
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        d2 = DAGMixinFooMixedInClass(**self.kwargs)
        self.assertNotEqual(d2.parent, d1)
        d2.parent = d1
        self.assertEqual(d2.parent, d1)

    def test_children_attribute_is_an_empty_list_by_default(self):
        """testing if the children attribute is an empty list by default
        """
        d = DAGMixinFooMixedInClass(**self.kwargs)
        self.assertEqual(d.children, [])

    def test_children_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the children attribute is
        set to None
        """
        d = DAGMixinFooMixedInClass(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            d.children = None

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: None is not list-like'
        )

    def test_children_attribute_accepts_correct_class_instances_only(self):
        """testing if the children attribute accepts only correct class
        instances
        """
        d = DAGMixinFooMixedInClass(**self.kwargs)
        with self.assertRaises(TypeError) as cm:
            d.children = ['not', 1, '', 'of', 'correct', 'instances']

        self.assertEqual(
            str(cm.exception),
            'DAGMixinFooMixedInClass.children should be a list of '
            'DAGMixinFooMixedInClass (or derivative) instances, not str'
        )

    def test_children_attribute_is_working_properly(self):
        """testing if the children attribute is working properly
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        d2 = DAGMixinFooMixedInClass(**self.kwargs)
        d3 = DAGMixinFooMixedInClass(**self.kwargs)

        self.assertEqual(d1.children, [])
        d1.children.append(d2)
        self.assertEqual(d1.children, [d2])
        d1.children = [d3]
        self.assertEqual(d1.children, [d3])

    def test_is_leaf_attribute_is_read_only(self):
        """testing if the is_leaf attribute is a read only attribute
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        with self.assertRaises(AttributeError) as cm:
            setattr(d1, 'is_leaf', 'this will not work')

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

    def test_is_leaf_attribute_is_working_properly(self):
        """testing if the is_leaf attribute is True for an instance without a
        child and False for another one with at least one child
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        d2 = DAGMixinFooMixedInClass(**self.kwargs)
        d3 = DAGMixinFooMixedInClass(**self.kwargs)
        d1.children = [d2, d3]
        self.assertFalse(d1.is_leaf)
        self.assertTrue(d2.is_leaf)
        self.assertTrue(d3.is_leaf)

    def test_is_root_attribute_is_read_only(self):
        """testing if the is_root attribute is a read only attribute
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        with self.assertRaises(AttributeError) as cm:
            setattr(d1, 'is_root', 'this will not work')

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

    def test_is_root_attribute_is_working_properly(self):
        """testing if the is_root attribute is True for an instance without a
        parent and False for another instance with a parent
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        d2 = DAGMixinFooMixedInClass(**self.kwargs)
        d3 = DAGMixinFooMixedInClass(**self.kwargs)
        d1.children = [d2, d3]
        self.assertTrue(d1.is_root)
        self.assertFalse(d2.is_root)
        self.assertFalse(d3.is_root)

    def test_is_container_attribute_is_read_only(self):
        """testing if the is_container attribute is a read only attribute
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        with self.assertRaises(AttributeError) as cm:
            setattr(d1, 'is_container', 'this will not work')

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

    def test_is_container_attribute_working_properly(self):
        """testing if the is_container attribute is True for an instance with
        at least one child and False for another with no child
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        d2 = DAGMixinFooMixedInClass(**self.kwargs)
        d3 = DAGMixinFooMixedInClass(**self.kwargs)
        d4 = DAGMixinFooMixedInClass(**self.kwargs)

        d1.children = [d2, d3]
        d2.children = [d4]
        self.assertTrue(d1.is_container)
        self.assertTrue(d2.is_container)
        self.assertFalse(d3.is_container)
        self.assertFalse(d4.is_container)

    def test_parents_property_is_read_only(self):
        """testing if the parents property is read-only
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        with self.assertRaises(AttributeError) as cm:
            setattr(d1, 'parents', 'this will not work')

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

    def test_parents_property_is_working_properly(self):
        """testing if the parents property is read-only
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        d2 = DAGMixinFooMixedInClass(**self.kwargs)
        d3 = DAGMixinFooMixedInClass(**self.kwargs)
        d4 = DAGMixinFooMixedInClass(**self.kwargs)

        d1.children = [d2, d3]
        d2.children = [d4]

        self.assertEqual(d1.parents, [])
        self.assertEqual(d2.parents, [d1])
        self.assertEqual(d3.parents, [d1])
        self.assertEqual(d4.parents, [d1, d2])

    def test_walk_hierarchy_is_working_properly(self):
        """testing if the walk_hierarchy method is working properly
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        d2 = DAGMixinFooMixedInClass(**self.kwargs)
        d3 = DAGMixinFooMixedInClass(**self.kwargs)
        d4 = DAGMixinFooMixedInClass(**self.kwargs)

        d1.children = [d2, d3]
        d2.children = [d4]

        entities_walked = []
        for e in d1.walk_hierarchy():
            entities_walked.append(e)
        self.assertEqual(entities_walked, [d1, d2, d4, d3])

        entities_walked = []
        for e in d1.walk_hierarchy(method=1):
            entities_walked.append(e)
        self.assertEqual(entities_walked, [d1, d2, d3, d4])

        entities_walked = []
        for e in d2.walk_hierarchy():
            entities_walked.append(e)
        self.assertEqual(entities_walked, [d2, d4])

        entities_walked = []
        for e in d3.walk_hierarchy():
            entities_walked.append(e)
        self.assertEqual(entities_walked, [d3])

        entities_walked = []
        for e in d4.walk_hierarchy():
            entities_walked.append(e)
        self.assertEqual(entities_walked, [d4])


class DAGMixinDBTestCase(unittest.TestCase):
    """tests the DAGMixin class with a DB
    """

    def setUp(self):
        """set the test up
        """
        db.setup({'sqlalchemy.url': 'sqlite:///:memory:'})

        self.kwargs = {
            'name': 'Test DAG Mixin'
        }

    def tearDown(self):
        """clean up the test
        """
        db.DBSession.remove()

    def test_committing_data(self):
        """testing committing and retrieving data back
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        d2 = DAGMixinFooMixedInClass(**self.kwargs)
        d3 = DAGMixinFooMixedInClass(**self.kwargs)
        d4 = DAGMixinFooMixedInClass(**self.kwargs)

        d1.children = [d2, d3]
        d2.children = [d4]

        db.DBSession.add_all([d1, d2, d3, d4])
        db.DBSession.commit()

        del d1, d2, d3, d4

        all_data = DAGMixinFooMixedInClass.query.all()

        self.assertEqual(len(all_data), 4)
        self.assertTrue(isinstance(all_data[0], DAGMixinFooMixedInClass))
        self.assertTrue(isinstance(all_data[1], DAGMixinFooMixedInClass))
        self.assertTrue(isinstance(all_data[2], DAGMixinFooMixedInClass))
        self.assertTrue(isinstance(all_data[3], DAGMixinFooMixedInClass))

    def test_deleting_data(self):
        """testing deleting data
        """
        d1 = DAGMixinFooMixedInClass(**self.kwargs)
        d2 = DAGMixinFooMixedInClass(**self.kwargs)
        d3 = DAGMixinFooMixedInClass(**self.kwargs)
        d4 = DAGMixinFooMixedInClass(**self.kwargs)

        d1.children = [d2, d3]
        d2.children = [d4]

        db.DBSession.add_all([d1, d2, d3, d4])
        db.DBSession.commit()

        db.DBSession.delete(d1)
        db.DBSession.commit()

        all_data = DAGMixinFooMixedInClass.query.all()
        self.assertEqual(len(all_data), 0)
