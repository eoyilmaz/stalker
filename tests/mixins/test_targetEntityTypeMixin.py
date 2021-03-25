# -*- coding: utf-8 -*-

import unittest
import pytest
from sqlalchemy import Column, Integer, ForeignKey
from stalker.models.mixins import TargetEntityTypeMixin
from stalker.models.project import Project
from stalker.models.entity import SimpleEntity


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
        with pytest.raises(TypeError) as cm:
            TargetEntityTypeMixedClass(**self.kwargs)

        assert str(cm.value) == \
            'TargetEntityTypeMixedClass.target_entity_type can not be None'

    def test_target_entity_type_argument_being_empty_string(self):
        """testing if a ValueError will be raised when the target_entity_type
        argument is given as None
        """
        self.kwargs["target_entity_type"] = ""
        with pytest.raises(ValueError) as cm:
            TargetEntityTypeMixedClass(**self.kwargs)

        assert str(cm.value) == \
            'TargetEntityTypeMixedClass.target_entity_type can not be empty'

    def test_target_entity_type_argument_being_None(self):
        """testing if a TypeError will be raised when the target_entity_type
        argument is given as None
        """

        self.kwargs["target_entity_type"] = None
        with pytest.raises(TypeError) as cm:
            TargetEntityTypeMixedClass(**self.kwargs)

        assert str(cm.value) == \
            'TargetEntityTypeMixedClass.target_entity_type can not be None'

    def test_target_entity_type_attribute_is_read_only(self):
        """testing if a AttributeError will be raised when the
        target_entity_type argument is tried to be set
        """
        # try to set the target_entity_type attribute and expect AttributeError
        with pytest.raises(AttributeError) as cm:
            self.test_object.target_entity_type = "Project"

        assert str(cm.value) == "can't set attribute"

    def test_target_entity_type_argument_accepts_classes(self):
        """testing if the target_entity_type argument accepts classes
        """

        self.kwargs["target_entity_type"] = TestClass
        new_object = TargetEntityTypeMixedClass(**self.kwargs)
        
        assert new_object.target_entity_type == "TestClass"
