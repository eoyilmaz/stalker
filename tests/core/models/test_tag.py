# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest
from stalker.core.models import Tag, SimpleEntity


class TagTest(unittest.TestCase):
    """testing the Tag class
    """


    def setUp(self):
        """setup the test
        """

        self.kwargs = {
            "name": "a test tag",
            "description": "this is a test tag",
            }

        # create another SimpleEntity with kwargs for __eq__ and __ne__ tests
        self.simple_entity = SimpleEntity(**self.kwargs)


    def test_tag_init(self):
        """testing if tag inits properly
        """

        # this should work without any error
        a_tag_object = Tag(**self.kwargs)


    def test_equality(self):
        """testing the equality of two Tags
        """

        a_tag_object1 = Tag(**self.kwargs)
        a_tag_object2 = Tag(**self.kwargs)

        self.kwargs["name"] = "a new test Tag"
        self.kwargs["description"] = "this is a new test Tag"

        a_tag_object3 = Tag(**self.kwargs)

        self.assertTrue(a_tag_object1 == a_tag_object2)
        self.assertFalse(a_tag_object1 == a_tag_object3)
        self.assertFalse(a_tag_object1 == self.simple_entity)


    def test_inequality(self):
        """testing the inequality of two Tags
        """

        a_tag_object1 = Tag(**self.kwargs)
        a_tag_object2 = Tag(**self.kwargs)

        self.kwargs["name"] = "a new test Tag"
        self.kwargs["description"] = "this is a new test Tag"

        a_tag_object3 = Tag(**self.kwargs)

        self.assertFalse(a_tag_object1 != a_tag_object2)
        self.assertTrue(a_tag_object1 != a_tag_object3)
        self.assertTrue(a_tag_object1 != self.simple_entity)



        #
        #def test_plural_name(self):
        #"""testing the plural name of Tag class
        #"""

        #self.assertTrue(Tag.plural_name, "Tags")
    
    
