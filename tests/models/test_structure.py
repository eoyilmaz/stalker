# -*- coding: utf-8 -*-

import unittest

import pytest

from stalker import Structure


class StructureTester(unittest.TestCase):
    """tests the stalker.models.structure.Structure class
    """

    def setUp(self):
        """setting up the tests
        """
        super(StructureTester, self).setUp()

        from stalker import Type
        vers_type = Type(
            name="Version",
            code='vers',
            target_entity_type="FilenameTemplate"
        )

        ref_type = Type(
            name="Reference",
            code='ref',
            target_entity_type="FilenameTemplate"
        )

        # type templates
        from stalker import FilenameTemplate
        self.asset_template = FilenameTemplate(
            name="Test Asset Template",
            target_entity_type="Asset",
            type=vers_type
        )

        self.shot_template = FilenameTemplate(
            name="Test Shot Template",
            target_entity_type="Shot",
            type=vers_type
        )

        self.reference_template = FilenameTemplate(
            name="Test Reference Template",
            target_entity_type="Link",
            type=ref_type
        )

        self.test_templates = [self.asset_template,
                               self.shot_template,
                               self.reference_template]

        self.test_templates2 = [self.asset_template]

        self.custom_template = "a custom template"

        self.test_type = Type(
            name="Commercial Structure",
            code='comm',
            target_entity_type='Structure',
        )

        # keyword arguments
        self.kwargs = {
            "name": "Test Structure",
            "description": "This is a test structure",
            "templates": self.test_templates,
            "custom_template": self.custom_template,
            "type": self.test_type,
        }
        self.test_structure = Structure(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Structure class
        """
        assert Structure.__auto_name__ is False

    def test_custom_template_argument_can_be_skipped(self):
        """testing if the custom_template argument can be skipped
        """
        self.kwargs.pop("custom_template")
        new_structure = Structure(**self.kwargs)
        assert new_structure.custom_template == ""

    def test_custom_template_argument_is_None(self):
        """testing if no error will be raised when the custom_template argument
        is None.
        """
        self.kwargs["custom_template"] = None
        new_structure = Structure(**self.kwargs)
        assert new_structure.custom_template == ""

    def test_custom_template_argument_is_empty_string(self):
        """testing if no error will be raised when the custom_template argument
        is an empty string
        """
        self.kwargs["custom_template"] = ""
        new_structure = Structure(**self.kwargs)
        assert new_structure.custom_template == ""

    def test_custom_template_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the custom_template
        argument is not a string
        """
        self.kwargs['custom_template'] = ["this is not a string"]
        with pytest.raises(TypeError) as cm:
            Structure(**self.kwargs)

        assert str(cm.value) == \
            'Structure.custom_template should be a string not list'

    def test_custom_template_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the custom_template
        attribute is not a string
        """
        with pytest.raises(TypeError) as cm:
            self.test_structure.custom_template = ['this is not a string']

        assert str(cm.value) == \
            'Structure.custom_template should be a string not list'

    def test_templates_argument_can_be_skipped(self):
        """testing if no error will be raised when the templates argument is
        skipped
        """
        self.kwargs.pop("templates")
        new_structure = Structure(**self.kwargs)
        assert isinstance(new_structure, Structure)

    def test_templates_argument_can_be_None(self):
        """testing if no error will be raised when the templates argument is
        None
        """
        self.kwargs["templates"] = None
        new_structure = Structure(**self.kwargs)
        assert isinstance(new_structure, Structure)

    def test_templates_attribute_cannot_be_set_to_None(self):
        """testing if a TypeError will be raised when the templates attribute
        is set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_structure.templates = None

        assert str(cm.value) == \
            'Incompatible collection type: None is not list-like'

    def test_templates_argument_only_accepts_list(self):
        """testing if a TypeError will be raised when the given templates
        argument is not a list
        """
        self.kwargs["templates"] = 1
        with pytest.raises(TypeError) as cm:
            Structure(**self.kwargs)

        assert str(cm.value) == \
            'Incompatible collection type: int is not list-like'

    def test_templates_attribute_only_accepts_list_1(self):
        """testing if a TypeError will be raised when the templates attribute
        is tried to be set to an object which is not a list instance.
        """
        with pytest.raises(TypeError) as cm:
            self.test_structure.templates = 1.121

        assert str(cm.value) == \
            'Incompatible collection type: float is not list-like'

    def test_templates_attribute_is_working_properly(self):
        """testing if templates attribute is working properly
        """
        # test the correct value
        self.test_structure.templates = self.test_templates
        assert self.test_structure.templates == self.test_templates

    def test_templates_argument_accepts_only_list_of_FilenameTemplate_instances(self):
        """testing if a TypeError will be raised when the templates argument is
        a list but the elements are not all instances of FilenameTemplate
        class.
        """
        test_value = [1, 1.2, "a string"]
        self.kwargs["templates"] = test_value
        with pytest.raises(TypeError) as cm:
            Structure(**self.kwargs)

        assert str(cm.value) == \
            'All the elements in the Structure.templates should be a ' \
            'stalker.models.template.FilenameTemplate instance not int'

    def test_templates_argument_is_working_properly(self):
        """testing if the templates argument value is correctly passed to the
        templates attribute
        """
        # test the correct value
        self.kwargs["templates"] = self.test_templates
        new_structure = Structure(**self.kwargs)
        assert new_structure.templates ==self.test_templates

    def test_templates_attribute_accpets_only_list_of_FilenameTemplate_instances(self):
        """testing if a TypeError will be raised when the templates attribute
        is a list but the elements are not all instances of FilenameTemplate
        class.
        """
        test_value = [1, 1.2, "a string"]
        with pytest.raises(TypeError) as cm:
            self.test_structure.templates = test_value

        assert str(cm.value) == \
            'All the elements in the Structure.templates should be a ' \
            'stalker.models.template.FilenameTemplate instance not int'

    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ is False
        """
        assert Structure.__strictly_typed__ is False

    def test_equality_operator(self):
        """testing equality of two Structure objects
        """
        new_structure2 = Structure(**self.kwargs)

        self.kwargs["custom_template"] = "a test custom template"
        new_structure3 = Structure(**self.kwargs)

        self.kwargs["custom_template"] = self.test_structure.custom_template
        self.kwargs["templates"] = self.test_templates2
        new_structure4 = Structure(**self.kwargs)

        assert self.test_structure == new_structure2
        assert not self.test_structure == new_structure3
        assert not self.test_structure == new_structure4

    def test_inequality_operator(self):
        """testing inequality of two Structure objects
        """
        new_structure2 = Structure(**self.kwargs)

        self.kwargs["custom_template"] = "a test custom template"
        new_structure3 = Structure(**self.kwargs)

        self.kwargs["custom_template"] = self.test_structure.custom_template
        self.kwargs["templates"] = self.test_templates2
        new_structure4 = Structure(**self.kwargs)

        assert not self.test_structure != new_structure2
        assert self.test_structure != new_structure3
        assert self.test_structure != new_structure4

    def test_plural_class_name(self):
        """testing the plural name of Structure class
        """
        assert self.test_structure.plural_class_name == "Structures"

    # def test_hash_value(self):
    #     """testing if the hash value is correctly calculated
    #     """
    #     assert \
    #         hash(self.test_structure) == \
    #         hash(self.test_structure.id) +
    #         2 * hash(self.test_structure.name) +
    #         3 * hash(self.test_structure.entity_type)
