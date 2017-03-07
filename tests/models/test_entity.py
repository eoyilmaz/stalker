# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>

from stalker.testing import UnitTestBase
from stalker import Entity


class EntityTester(UnitTestBase):
    """tests the Entity class
    """

    def setUp(self):
        """setting up some proper values
        """
        super(EntityTester, self).setUp()

        # create a user
        from stalker import db, User
        self.test_user = User(
            name="Test User",
            login="testuser",
            email="test@user.com",
            password="test"
        )
        db.DBSession.add(self.test_user)

        # create some test Tag objects, not necessarily needed but create them
        from stalker import Tag
        self.test_tag1 = Tag(name="Test Tag 1")
        self.test_tag2 = Tag(name="Test Tag 1")  # make it equal to tag1
        self.test_tag3 = Tag(name="Test Tag 3")
        db.DBSession.add_all([self.test_tag1, self.test_tag2, self.test_tag3])

        self.tags = [self.test_tag1, self.test_tag2]

        # create a couple of test Note objects
        from stalker import Note
        self.test_note1 = Note(name="test note1", content="test note1")
        self.test_note2 = Note(name="test note2", content="test note2")
        self.test_note3 = Note(name="test note3", content="test note3")
        db.DBSession.add_all([
            self.test_note1, self.test_note2, self.test_note3
        ])

        self.notes = [self.test_note1, self.test_note2]

        self.kwargs = {
            "name": "Test Entity",
            "description": "This is a test entity, and this is a proper \
            description for it",
            "created_by": self.test_user,
            "updated_by": self.test_user,
            "tags": self.tags,
            "notes": self.notes,
        }

        # create a proper SimpleEntity to use it later in the tests
        self.test_entity = Entity(**self.kwargs)
        db.DBSession.add(self.test_entity)
        db.DBSession.commit()

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to False for
        Entity class
        """
        self.assertTrue(Entity.__auto_name__)

    def test_notes_argument_being_omitted(self):
        """testing if no error raised when omitted the notes argument
        """
        import copy
        kwargs = copy.copy(self.kwargs)
        kwargs.pop("notes")
        new_entity = Entity(**kwargs)
        self.assertTrue(isinstance(new_entity, Entity))

    def test_notes_argument_is_set_to_None(self):
        """testing if the notes attribute will be set to an empty list when the
        notes argument is set to None
        """
        import copy
        kwargs = copy.copy(self.kwargs)
        kwargs["notes"] = None
        new_entity = Entity(**kwargs)
        self.assertEqual(new_entity.notes, [])

    def test_notes_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the notes attribute is
        set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_entity.notes = None

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: None is not list-like'
        )

    def test_notes_argument_set_to_something_other_than_a_list(self):
        """testing if a TypeError will be raised when setting the notes
        argument something other than a list
        """
        import copy
        kwargs = copy.copy(self.kwargs)
        kwargs['notes'] = ["a string note"]
        with self.assertRaises(TypeError) as cm:
            Entity(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'Entity.note should be a stalker.models.note.Note instance, not '
            'str'
        )

    def test_notes_attribute_set_to_something_other_than_a_list(self):
        """testing if a TypeError will be raised when setting the notes
        argument something other than a list
        """
        with self.assertRaises(TypeError) as cm:
                self.test_entity.notes = ["a string note"]

        self.assertEqual(
            str(cm.exception),
            'Entity.note should be a stalker.models.note.Note instance, not '
            'str'
        )

    def test_notes_argument_set_to_a_list_of_other_objects(self):
        """testing if a TypeError will be raised when trying to set the notes
        argument to a list of other kind of objects than Note objects
        """
        import copy
        kwargs = copy.copy(self.kwargs)
        kwargs["notes"] = \
            [1, 12.2, "this is a string"]

        with self.assertRaises(TypeError) as cm:
            Entity(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'Entity.note should be a stalker.models.note.Note instance, '
            'not int'
        )

    def test_notes_attribute_set_to_a_list_of_other_objects(self):
        """testing if a TypeError will be raised when trying to set the notes
        attribute to a list of other kind of objects than Note objects
        """
        test_value = [1, 12.2, "this is a string"]
        with self.assertRaises(TypeError) as cm:
            self.test_entity.notes = test_value

        self.assertEqual(
            str(cm.exception),
            'Entity.note should be a stalker.models.note.Note instance, not '
            'int'
        )

    def test_notes_attribute_works_properly(self):
        """testing if the notes attribute works properly
        """
        test_value = [self.test_note3]
        self.test_entity.notes = test_value
        self.assertEqual(self.test_entity.notes, test_value)

    def test_notes_attribute_element_is_set_to_something_other_than_a_note_object(self):
        """testing if a TypeError will be raised when trying to assign an
        element to the notes list which is not an instance of Note
        """
        with self.assertRaises(TypeError) as cm:
            self.test_entity.notes[0] = 0

        self.assertEqual(
            str(cm.exception),
            'Entity.note should be a stalker.models.note.Note instance, not '
            'int'
        )

    def test_tags_argument_being_omitted(self):
        """testing if nothing is raised when creating an entity without setting
        a tags argument
        """
        import copy
        kwargs = copy.copy(self.kwargs)
        kwargs.pop("tags")
        # this should work without errors
        new_entity = Entity(**kwargs)
        self.assertTrue(isinstance(new_entity, Entity))

    def test_tags_argument_being_initialized_as_an_empty_list(self):
        """testing if nothing happens when tags argument an empty list
        """
        # this should work without errors
        import copy
        kwargs = copy.copy(self.kwargs)
        kwargs.pop("tags")
        new_entity = Entity(**kwargs)
        expected_result = []
        self.assertEqual(new_entity.tags, expected_result)

    def test_tags_argument_set_to_something_other_than_a_list(self):
        """testing if a TypeError is going to be raised when initializing the
        tags with something other than a list
        """
        import copy
        kwargs = copy.copy(self.kwargs)
        kwargs["tags"] = ["a tag", 1243, 12.12]
        with self.assertRaises(TypeError) as cm:
            Entity(**kwargs)

        self.assertEqual(
            str(cm.exception),
            'Entity.tag should be a stalker.models.tag.Tag instance, not str'
        )

    def test_tags_attribute_works_properly(self):
        """testing if tags attribute works properly
        """
        test_value = [self.test_tag1]
        self.test_entity.tags = test_value
        self.assertEqual(self.test_entity.tags, test_value)

    def test_tags_attribute_element_is_set_to_something_other_than_a_tag_object(self):
        """testing if a TypeError will be raised when trying to assign an
        element to the tags list which is not an instance of Tag
        """
        with self.assertRaises(TypeError) as cm:
            self.test_entity.tags[0] = 0

        self.assertEqual(
            str(cm.exception),
            'Entity.tag should be a stalker.models.tag.Tag instance, not int'
        )

    def test_tags_attribute_set_to_None(self):
        """testing if a TypeError will be raised when the tags attribute is set
        to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_entity.tags = None

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: None is not list-like'
        )

    def test_equality(self):
        """testing equality of two entities
        """
        # create two entities with same parameters and check for equality
        import copy
        kwargs = copy.copy(self.kwargs)

        entity1 = Entity(**kwargs)
        entity2 = Entity(**kwargs)

        kwargs["name"] = "another entity"
        kwargs["tags"] = [self.test_tag3]
        kwargs["notes"] = []
        entity3 = Entity(**kwargs)

        self.assertTrue(entity1 == entity2)
        self.assertFalse(entity1 == entity3)

    def test_inequality(self):
        """testing inequality of two entities
        """
        # change the tags and test it again, expect False
        import copy
        kwargs = copy.copy(self.kwargs)
        entity1 = Entity(**kwargs)
        entity2 = Entity(**kwargs)

        kwargs["name"] = "another entity"
        kwargs["tags"] = [self.test_tag3]
        kwargs["notes"] = []
        entity3 = Entity(**kwargs)

        self.assertFalse(entity1 != entity2)
        self.assertTrue(entity1 != entity3)
