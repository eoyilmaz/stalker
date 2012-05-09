# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest

from sqlalchemy import Column, Integer, ForeignKey
from stalker.models import (Project, SimpleEntity, TargetEntityTypeMixin)

class TestClass(object):
    pass

class TargetEntityTypeMixedClass(SimpleEntity, TargetEntityTypeMixin):
    __tablename__ = "TarEntMixClasses"
    __mapper_args__ = {"polymorphic_identity": "TarEntMixClass"}
    tarMixClass_id = Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )

    def __init__(self, **kwargs):
        super(TargetEntityTypeMixedClass, self).__init__(**kwargs)
        TargetEntityTypeMixin.__init__(self, **kwargs)

class TargetEntityMixinTester(unittest.TestCase):
    """Tests the TargetEntityMixin
    """
    def setUp(self):
        """setup the test
        """

        self.kwargs = {
            "name": "Test object",
            "target_entity_type": Project
        }

        self.test_object = TargetEntityTypeMixedClass(**self.kwargs)
    
    def test_target_entity_type_argument_is_skipped(self):
        """testing if a TypeError will be raised when the target_entity_type 
        argument is skipped
        """
        
        self.kwargs.pop("target_entity_type")
        self.assertRaises(TypeError, TargetEntityTypeMixedClass, **self.kwargs)
    
    def test_target_entity_type_argument_being_empty_string(self):
        """testing if a ValueError will be raised when the target_entity_type
        argument is given as None
        """

        self.kwargs["target_entity_type"] = ""
        self.assertRaises(ValueError, TargetEntityTypeMixedClass, **self.kwargs)

    def test_target_entity_type_argument_being_None(self):
        """testing if a TypeError will be raised when the target_entity_type
        argument is given as None
        """

        self.kwargs["target_entity_type"] = None
        self.assertRaises(TypeError, TargetEntityTypeMixedClass, **self.kwargs)

    def test_target_entity_type_attribute_is_read_only(self):
        """testing if a AttributeError will be raised when the
        target_entity_type argument is tried to be set
        """

        # try to set the target_entity_type attribute and expect AttributeError
        self.assertRaises(
            AttributeError,
            setattr,
            self.test_object,
            "target_entity_type",
            "Project"
        )

    def test_target_entity_type_argument_accepts_classes(self):
        """testing if the target_entity_type argument accepts classes
        """

        self.kwargs["target_entity_type"] = TestClass
        new_object = TargetEntityTypeMixedClass(**self.kwargs)
        
        self.assertEqual(new_object.target_entity_type, "TestClass")
