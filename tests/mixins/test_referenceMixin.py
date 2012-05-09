# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

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
            name="Test Link Type",
            target_entity_type=Link,
            )

        # create a couple of mock Link objects
        self.test_link1 = Link(
            name="Test Link 1",
            type=self.test_link_type,
            path="test_path",
            filename="test_filename",
            )

        self.test_link2 = Link(
            name="Test Link 2",
            type=self.test_link_type,
            path="test_path",
            filename="test_filename",
            )

        self.test_link3 = Link(
            name="Test Link 3",
            type=self.test_link_type,
            path="test_path",
            filename="test_filename",
            )

        self.test_link4 = Link(
            name="Test Link 4",
            type=self.test_link_type,
            path="test_path",
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


    def test_references_attribute_only_accepts_listlike_objects(self):
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


    def test_references_attribute_accepting_only_lists_of_Entity_instances(self):
        """testing if references attribute accepting only lists with Entity
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

        test_value = [self.test_entity1, self.test_entity2, self.test_link1]
        self.test_foo_obj.references = test_value
        self.assertItemsEqual(test_value, self.test_foo_obj.references)


    def test_references_attribute_working_properly(self):
        """testing if references attribute working properly
        """

        self.test_foo_obj.references = self.test_links
        self.assertEqual(self.test_foo_obj.references, self.test_links)

        test_value = [self.test_entity1, self.test_entity2]
        self.test_foo_obj.references = test_value
        self.assertItemsEqual(self.test_foo_obj.references, test_value)


    def test_references_attribute_elements_accepts_Entity_only(self):
        """testing if a TypeError will be raised when trying to assign
        something other than an instance of Entity or its derived classes to
        the references list
        """

        # append
        self.assertRaises(
            TypeError,
            self.test_foo_obj.references.append,
            0
        )


    def test_references_application_test(self):
        """testing an example of ReferenceMixin usage
        """

        class GreatEntity(SimpleEntity, ReferenceMixin):
            pass

        myGreatEntity = GreatEntity(name="Test")
        # we should have a references attribute right now
        myGreatEntity.references

        image_link_type = Type(name="Image", target_entity_type="Link")
        new_link = Link(name="NewTestLink", path="nopath",
                        filename="nofilename", type=image_link_type)

        test_value = [new_link]

        myGreatEntity.references = test_value

        self.assertEqual(myGreatEntity.references, test_value)






