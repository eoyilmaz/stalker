#-*- coding: utf-8 -*-

import unittest
from stalker import Entity, Note, Review, Tag, User

class EntityTester(unittest.TestCase):
    """tests the Entity class
    """
    
    def setUp(self):
        """seting up some proper values
        """
        # create a user
        self.test_user = User(
            first_name="Test",
            last_name="User",
            login_name="testuser",
            email="test@user.com",
            password="test"
        )

        # create some test Tag objects, not neccessarly needed but create them
        self.test_tag1 = Tag(name="Test Tag 1")
        self.test_tag2 = Tag(name="Test Tag 1") # make it equal to tag1
        self.test_tag3 = Tag(name="Test Tag 3")

        self.tags = [self.test_tag1, self.test_tag2]

        # create a couple of test Note objects
        self.test_note1 = Note(name="test note1", content="test note1")
        self.test_note2 = Note(name="test note2", content="test note2")
        self.test_note3 = Note(name="test note3", content="test note3")

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

    def test_notes_argument_being_omitted(self):
        """testing if no error raised when omitted the notes argument
        """
        self.kwargs.pop("notes")
        new_entity = Entity(**self.kwargs)

    def test_notes_argument_is_set_to_None(self):
        """testing if the notes attribute will be set to an empty list when the
        notes argument is set to None
        """
        self.kwargs["notes"] = None
        new_entity = Entity(**self.kwargs)
        self.assertEqual(new_entity.notes, [])

    def test_notes_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the notes attribute is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_entity, "notes", None)

    def test_notes_argument_set_to_something_other_than_a_list(self):
        """testing if a TypeError will be raised when setting the notes
        argument something other than a list
        """
        test_values = [1, 1.2, "a string note"]
        for test_value in test_values:
            self.kwargs["notes"] = test_value
            self.assertRaises(TypeError, Entity, **self.kwargs)

    def test_notes_attribute_set_to_something_other_than_a_list(self):
        """testing if a TypeError will be raised when setting the notes
        argument something other than a list
        """
        test_values = [1, 1.2, "a string note"]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_entity,
                "notes",
                test_value
            )

    def test_notes_argument_set_to_a_list_of_other_objects(self):
        """testing if a TypeError will be raised when trying to set the notes
        argument to a list of other kind of objects than Note objects
        """
        self.kwargs["notes"] = [1, 12.2, "this is a string",
            ["a list"], {"a": "note"}]
        self.assertRaises(TypeError, Entity, **self.kwargs)

    def test_notes_attribute_set_to_a_list_of_other_objects(self):
        """testing if a TypeError will be raised when trying to set the notes
        attribute to a list of other kind of objects than Note objects
        """
        test_value = [1, 12.2, "this is a string", ["a list"], {"a": "note"}]
        self.assertRaises(
            TypeError,
            setattr,
            self.test_entity,
            "notes",
            test_value
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
        self.assertRaises(
            TypeError,
            self.test_entity.notes.__setitem__,
            0,
            0
        )

    def test_tags_argument_being_omitted(self):
        """testing if nothing is raised when creating an entity without setting
        a tags argument
        """
        self.kwargs.pop("tags")
        # this should work without errors
        aNewEntity = Entity(**self.kwargs)

    def test_tags_argument_being_initialized_as_an_empty_list(self):
        """testing if nothing happens when tags argument an empty list
        """
        # this should work without errors
        self.kwargs.pop("tags")
        aNewEntity = Entity(**self.kwargs)
        expected_result = []
        self.assertEqual(aNewEntity.tags, expected_result)

    def test_tags_argument_set_to_something_other_than_a_list(self):
        """testing if a TypeError is going to be raised when initializing the
        tags with something other than a list
        """
        test_values = ["a tag", 1243, 12.12, {"a": "tag"}]
        for test_value in test_values:
            self.kwargs["tags"] = test_value
            self.assertRaises(TypeError, Entity, **self.kwargs)

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
        self.assertRaises(
            TypeError,
            self.test_entity.tags.__setitem__,
            0,
            0
        )

    def test_tags_attribute_set_to_None(self):
        """testing if a TypeError will be raised when the tags attribute is set
        to None
        """
        self.assertRaises(TypeError, setattr, self.test_entity, "tags", None)

    def test_equality(self):
        """testing equality of two entities
        """
        # create two entities with same parameters and check for equality
        entity1 = Entity(**self.kwargs)
        entity2 = Entity(**self.kwargs)

        self.kwargs["name"] = "another entity"
        self.kwargs["tags"] = [self.test_tag3]
        self.kwargs["notes"] = []
        entity3 = Entity(**self.kwargs)

        self.assertTrue(entity1 == entity2)
        self.assertFalse(entity1 == entity3)

    def test_inequality(self):
        """testing inequality of two entities
        """
        # change the tags and test it again, expect False
        entity1 = Entity(**self.kwargs)
        entity2 = Entity(**self.kwargs)

        self.kwargs["name"] = "another entity"
        self.kwargs["tags"] = [self.test_tag3]
        self.kwargs["notes"] = []
        entity3 = Entity(**self.kwargs)

        self.assertFalse(entity1 != entity2)
        self.assertTrue(entity1 != entity3)

    def test_reviews_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the reviews attribute
        is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_entity, "reviews",
                          None)

    def test_reviews_attribute_is_not_set_to_a_list(self):
        """testing if a TypeError will be raised when the reviews attribute is
        not set to a list instance
        """
        self.assertRaises(TypeError, setattr, self.test_entity, "reviews",
                          123)

    def test_reviews_attribute_is_not_accepting_anything_other_than_list_of_Reviews(self):
        """testing if a TypeError will be raised when the elements of the
        reivews attribute is set to something other than a Review
        """
        self.assertRaises(TypeError, setattr, self.test_entity, "reviews",
            [123])

    def test_reviews_attribute_is_working_properly(self):
        """testing if the reviews attribute is working properly
        """
        # create a couple of Reviews
        rev1 = Review(name="Test Rev 1", to=self.test_entity)
        rev2 = Review(name="Test Rev 2", to=self.test_entity)
        rev3 = Review(name="Test Rev 3", to=self.test_entity)

        # create a new Entity with no reviews
        new_entity = Entity(**self.kwargs)

        # now try to assign all thre rev1 to the new object
        # this should work fine
        test_reviews = [rev1, rev2, rev3]
        new_entity.reviews = test_reviews

        self.assertEqual(new_entity.reviews, test_reviews)

    def test_reviews_attribute_updates_the_to_attribute_in_the_Review_instance(self):
        """testing if the "to" attribute is updated with the current object
        when it is set
        """
        # create a couple of Reviews
        rev1 = Review(name="Test Rev 1", to=self.test_entity)
        rev2 = Review(name="Test Rev 2", to=self.test_entity)
        rev3 = Review(name="Test Rev 3", to=self.test_entity)

        # create a new Entity with no reviews
        new_entity = Entity(**self.kwargs)

        #print self.test_entity
        #print new_entity

        # now try to assign all the reviews to the new object
        new_entity.reviews = [rev1, rev2, rev3]

        # now check if the reviews "to" attribute is pointing to the correct
        # object
        self.assertEqual(rev1.to, new_entity)
        self.assertEqual(rev2.to, new_entity)
        self.assertEqual(rev3.to, new_entity)

        # check the reviews are in the reviews list
        self.assertIn(rev1, new_entity.reviews)
        self.assertIn(rev2, new_entity.reviews)
        self.assertIn(rev3, new_entity.reviews)

        # now try to remove the review from the reviews list and expect a
        # TypeError
        #print "trying to remove"
        #print "new_entity.reviews : %s" % new_entity.reviews
        #print rev1
        self.assertRaises(RuntimeError, new_entity.reviews.remove, rev1)

    def test_reviews_attribute_handles_assigning_the_same_review_twice(self):
        """testing if assigning the same review twice or more will not breake
        anything or raise any exception
        """
        # create a couple of Reviews
        rev1 = Review(name="Test Rev 1", to=self.test_entity)
        rev2 = Review(name="Test Rev 2", to=self.test_entity)
        rev3 = Review(name="Test Rev 3", to=self.test_entity)

        # now try to assign the same review again to the same object
        self.test_entity.reviews.append(rev1)

        # now try the reverse
        rev1.to = self.test_entity

        # the review should be in the list
        self.assertIn(rev1, self.test_entity.reviews)
