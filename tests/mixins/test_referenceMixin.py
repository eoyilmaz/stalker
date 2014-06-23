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
from stalker.models.entity import Entity
from stalker.models.link import Link
from stalker.models.mixins import ReferenceMixin
from stalker.db.session import DBSession
from stalker.models.type import Type
from stalker.models.entity import SimpleEntity


class RefMixFooClass(SimpleEntity, ReferenceMixin):
    __tablename__ = "RefMixFooClasses"
    __mapper_args__ = {"polymorphic_identity": "RefMixFooClass"}
    refMixFooClass_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                               primary_key=True)

    def __init__(self, **kwargs):
        super(RefMixFooClass, self).__init__(**kwargs)


class ReferenceMixinTester(unittest.TestCase):
    """tests the ReferenceMixin
    """

    def setUp(self):
        """setup the test
        """
        # link type
        self.test_link_type = Type(
            name='Test Link Type',
            code='testlink',
            target_entity_type=Link,
        )

        # create a couple of Link objects
        self.test_link1 = Link(
            name="Test Link 1",
            type=self.test_link_type,
            full_path="test_path",
            filename="test_filename",
        )

        self.test_link2 = Link(
            name="Test Link 2",
            type=self.test_link_type,
            full_path="test_path",
            filename="test_filename",
        )

        self.test_link3 = Link(
            name="Test Link 3",
            type=self.test_link_type,
            full_path="test_path",
            filename="test_filename",
        )

        self.test_link4 = Link(
            name="Test Link 4",
            type=self.test_link_type,
            full_path="test_path",
            filename="test_filename",
        )

        self.test_entity1 = Entity(
            name="Test Entity 1",
        )

        self.test_entity2 = Entity(
            name="Test Entity 2",
        )

        self.test_links = [
            self.test_link1,
            self.test_link2,
            self.test_link3,
            self.test_link4,
        ]

        self.test_foo_obj = RefMixFooClass(name="Ref Mixin Test")

    def tearDown(self):
        """clean up the test
        """
        DBSession.remove()

    def test_references_attribute_accepting_empty_list(self):
        """testing if references attribute accepting empty lists
        """
        self.test_foo_obj.references = []

    def test_references_attribute_only_accepts_list_like_objects(self):
        """testing if references attribute accepts only list-like objects,
        (objects with __setitem__, __getitem__ methods
        """
        test_values = [1, 1.2, "a string"]

        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_foo_obj,
                "references",
                test_value
            )

    def test_references_attribute_accepting_only_lists_of_Link_instances(self):
        """testing if references attribute accepting only lists with Link
        instances and derivatives
        """
        test_value = [1, 2.2, ["a reference as list"], "some references"]

        self.assertRaises(
            TypeError,
            setattr,
            self.test_foo_obj,
            "references",
            test_value
        )

        # and test if it is accepting a proper list
        test_value = [self.test_link1, self.test_link2, self.test_link3]
        self.test_foo_obj.references = test_value
        self.assertEqual(
            sorted(test_value, key=lambda x: x.name),
            sorted(self.test_foo_obj.references, key=lambda x: x.name)
        )

    def test_references_attribute_elements_accepts_Links_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than an instance of Link or its derived classes to
        the references list
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_foo_obj, 'references',
            [self.test_entity1, self.test_entity2]
        )

    def test_references_attribute_working_properly(self):
        """testing if references attribute working properly
        """
        self.test_foo_obj.references = self.test_links
        self.assertEqual(self.test_foo_obj.references, self.test_links)

        test_value = [self.test_link1, self.test_link2]
        self.test_foo_obj.references = test_value
        self.assertEqual(
            sorted(self.test_foo_obj.references, key=lambda x: x.name),
            sorted(test_value, key=lambda x: x.name)
        )

    def test_references_application_test(self):
        """testing an example of ReferenceMixin usage
        """
        class GreatEntity(SimpleEntity, ReferenceMixin):
            __tablename__ = 'GreatEntities'
            __mapper_args__ = {
                "polymorphic_identity": "GreatEntity"
            }
            ge_id = Column('id', Integer, ForeignKey('SimpleEntities.id'),
                           primary_key=True)

        my_ge = GreatEntity(name="Test")
        # we should have a references attribute right now
        var = my_ge.references

        image_link_type = Type(
            name='Image',
            code='image',
            target_entity_type="Link"
        )
        new_link = Link(name="NewTestLink", full_path="nopath",
                        filename="nofilename", type=image_link_type)

        test_value = [new_link]

        my_ge.references = test_value

        self.assertEqual(my_ge.references, test_value)
