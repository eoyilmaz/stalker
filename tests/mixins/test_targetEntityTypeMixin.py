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

from sqlalchemy import Column, Integer, ForeignKey
from stalker.models.mixins import TargetEntityTypeMixin
from stalker.models.project import Project
from stalker.models.entity import SimpleEntity
from stalker.testing import UnitTestBase


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


class TargetEntityMixinTester(UnitTestBase):
    """Tests the TargetEntityMixin
    """
    def setUp(self):
        """setup the test
        """
        super(TargetEntityMixinTester, self).setUp()

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
        with self.assertRaises(TypeError) as cm:
            TargetEntityTypeMixedClass(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'TargetEntityTypeMixedClass.target_entity_type can not be None'
        )
    
    def test_target_entity_type_argument_being_empty_string(self):
        """testing if a ValueError will be raised when the target_entity_type
        argument is given as None
        """

        self.kwargs["target_entity_type"] = ""
        with self.assertRaises(ValueError) as cm:
            TargetEntityTypeMixedClass(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'TargetEntityTypeMixedClass.target_entity_type can not be empty'
        )

    def test_target_entity_type_argument_being_None(self):
        """testing if a TypeError will be raised when the target_entity_type
        argument is given as None
        """

        self.kwargs["target_entity_type"] = None
        with self.assertRaises(TypeError) as cm:
            TargetEntityTypeMixedClass(**self.kwargs)

        self.assertEqual(
            str(cm.exception),
            'TargetEntityTypeMixedClass.target_entity_type can not be None'
        )

    def test_target_entity_type_attribute_is_read_only(self):
        """testing if a AttributeError will be raised when the
        target_entity_type argument is tried to be set
        """
        # try to set the target_entity_type attribute and expect AttributeError
        with self.assertRaises(AttributeError) as cm:
            self.test_object.target_entity_type = "Project"

        self.assertEqual(
            str(cm.exception),
            "can't set attribute"
        )

    def test_target_entity_type_argument_accepts_classes(self):
        """testing if the target_entity_type argument accepts classes
        """

        self.kwargs["target_entity_type"] = TestClass
        new_object = TargetEntityTypeMixedClass(**self.kwargs)
        
        self.assertEqual(new_object.target_entity_type, "TestClass")
