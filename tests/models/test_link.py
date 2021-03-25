# -*- coding: utf-8 -*-

import os
import unittest
import pytest
from stalker import Link


class LinkTester(unittest.TestCase):
    """tests the :class:`stalker.models.link.Link` class
    """

    def setUp(self):
        """setup the test
        """
        super(LinkTester, self).setUp()

        # create a mock LinkType object
        from stalker import Type
        self.test_link_type1 = Type(
            name='Test Type 1',
            code='test type1',
            target_entity_type='Link',
        )
        self.test_link_type2 = Type(
            name='Test Type 2',
            code='test type2',
            target_entity_type='Link',
        )

        self.kwargs = {
            'name': 'An Image Link',
            'full_path': 'C:/A_NEW_PROJECT/td/dsdf/'
                         '22-fdfffsd-32342-dsf2332-dsfd-3.exr',
            'original_filename': 'this_is_an_image.jpg',
            'type': self.test_link_type1
        }

        self.test_link = Link(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to False for
        Link class
        """
        assert Link.__auto_name__ is True

    def test_full_path_argument_is_None(self):
        """testing if setting the full_path argument to None will set the
        full_path attribute to an empty string
        """
        self.kwargs['full_path'] = None
        new_link = Link(**self.kwargs)
        assert new_link.full_path == ''

    def test_full_path_attribute_is_set_to_None(self):
        """testing if setting the full_path attribute to None will set its
        value to an empty string
        """
        self.test_link.full_path = ''

    def test_full_path_argument_is_empty_an_empty_string(self):
        """testing if setting the full_path attribute will be an empty string
        if full_path argument is an empty string
        """
        self.kwargs['full_path'] = ''
        new_link = Link(**self.kwargs)
        assert new_link.full_path == ''

    def test_full_path_attribute_is_set_to_empty_string(self):
        """testing if setting the full_path attribute value will be an empty
        string if it is set to an empty string
        """
        self.test_link.full_path = ''
        assert self.test_link.full_path == ''

    def test_full_path_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the full_path argument is
        not a string
        """
        test_value = 1
        self.kwargs["full_path"] = test_value
        with pytest.raises(TypeError) as cm:
            Link(**self.kwargs)

        assert str(cm.value) == \
            'Link.full_path should be an instance of string not int'

    def test_full_path_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised when the full_path attribute
        is not a string instance
        """
        test_value = 1
        with pytest.raises(TypeError) as cm:
            self.test_link.full_path = test_value

        assert str(cm.value) == \
            'Link.full_path should be an instance of string not int'

    def test_full_path_windows_to_other_conversion(self):
        """testing if the full_path is stored in internal format
        """
        windows_path = 'M:\\path\\to\\object'
        expected_result = 'M:/path/to/object'

        self.test_link.full_path = windows_path
        assert self.test_link.full_path == expected_result

    def test_original_filename_argument_is_None(self):
        """testing if the original_filename attribute value will be set to the
        filename part of the full_path attribute if the original_filename
        argument is None
        """
        self.kwargs['original_filename'] = None
        new_link = Link(**self.kwargs)
        filename = os.path.basename(new_link.full_path)
        assert new_link.original_filename == filename

    def test_original_filename_attribute_is_set_to_None(self):
        """testing if the original_filename attribute value will be equal to
        the filename part of the full_path if it is set to None
        """
        self.test_link.original_filename = None
        filename = os.path.basename(self.test_link.full_path)
        assert self.test_link.original_filename == filename

    def test_original_filename_argument_is_empty_string(self):
        """testing if setting the original_filename argument to an empty string
        will set the original_filename attribute value to the filename part of
        the full_path
        """
        self.kwargs['original_filename'] = ''
        new_link = Link(**self.kwargs)
        filename = os.path.basename(new_link.full_path)
        assert new_link.original_filename == filename

    def test_original_filename_attribute_set_to_empty_string(self):
        """testing if setting the original_filename attribute to an empty
        string will set its value to filename part of the full_path attribute
        """
        self.test_link.original_filename = ''
        filename = os.path.basename(self.test_link.full_path)
        assert self.test_link.original_filename == filename

    def test_original_filename_argument_accepts_string_only(self):
        """testing if original_filename argument accepts string only and raises
        TypeError for other types
        """
        test_value = 1
        self.kwargs['original_filename'] = test_value
        with pytest.raises(TypeError) as cm:
            Link(**self.kwargs)

        assert str(cm.value) == \
            'Link.original_filename should be an instance of str and not int'

    def test_original_filename_attribute_accepts_string_only(self):
        """testing if original_filename attribute accepts string only and
        raises TypeError for other types
        """
        test_value = 1.1
        with pytest.raises(TypeError) as cm:
            self.test_link.original_filename = test_value

        assert str(cm.value) == \
            'Link.original_filename should be an instance of str and not float'

    def test_original_filename_argument_is_working_properly(self):
        """testing if the original_filename argument is working properly
        """
        assert self.kwargs['original_filename'] == \
            self.test_link.original_filename

    def test_original_filename_attribute_is_working_properly(self):
        """testing if the original_filename attribute is working properly
        """
        new_value = 'this_is_the_original_filename.jpg'
        assert self.test_link.original_filename != new_value
        self.test_link.original_filename = new_value
        assert self.test_link.original_filename == new_value

    def test_equality_of_two_links(self):
        """testing the equality operator
        """
        # with same parameters
        mock_link1 = Link(**self.kwargs)
        assert self.test_link == mock_link1

        # with different parameters
        self.kwargs['type'] = self.test_link_type2
        mock_link2 = Link(**self.kwargs)

        assert not self.test_link == mock_link2

    def test_inequality_of_two_links(self):
        """testing the inequality operator
        """
        # with same parameters
        mock_link1 = Link(**self.kwargs)
        assert self.test_link == mock_link1

        # with different parameters
        self.kwargs['type'] = self.test_link_type2
        mock_link2 = Link(**self.kwargs)

        assert not self.test_link != mock_link1
        assert self.test_link != mock_link2

    def test_plural_class_name(self):
        """testing the plural name of Link class
        """
        assert self.test_link.plural_class_name == "Links"

    # def test___strictly_typed___is_True(self):
        # """testing if the __strictly_typed__ class attribute is True
        # """
        # assert Link.__strictly_typed__ is True

    def test_path_attribute_is_set_to_None(self):
        """testing if a TypeError will be raised when the path attribute is set
        to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_link.path = None

        assert str(cm.value) == 'Link.path can not be set to None'

    def test_path_attribute_is_set_to_empty_string(self):
        """testing if a ValueError will be raised when the path attribute is
        set to an empty string
        """
        with pytest.raises(ValueError) as cm:
            self.test_link.path = ''

        assert str(cm.value) == 'Link.path can not be an empty string'

    def test_path_attribute_is_set_to_a_value_other_then_string(self):
        """testing if a TypeError will be raised when the path attribute is set
        to a value other than string
        """
        with pytest.raises(TypeError) as cm:
            self.test_link.path = 1

        assert str(cm.value) == \
            'Link.path should be an instance of str, not int'

    def test_path_attribute_value_comes_from_full_path(self):
        """testing if the path attribute value is calculated from the full_path
        attribute
        """
        assert self.test_link.path == 'C:/A_NEW_PROJECT/td/dsdf'

    def test_path_attribute_updates_the_full_path_attribute(self):
        """testing if the path attribute is updating the full_path attribute
        properly
        """
        test_value = '/mnt/some/new/path'
        expected_full_path = '/mnt/some/new/path/' \
                             '22-fdfffsd-32342-dsf2332-dsfd-3.exr'

        assert self.test_link.path != test_value
        self.test_link.path = test_value
        assert self.test_link.path == test_value
        assert self.test_link.full_path == expected_full_path

    def test_filename_attribute_is_set_to_None(self):
        """testing if the filename attribute will be an empty string if it is
        set a None
        """
        self.test_link.filename = None
        assert self.test_link.filename == ''

    def test_filename_attribute_is_set_to_a_value_other_then_string(self):
        """testing if a TypeError will be raised when the filename attribute is
        set to a value other than string
        """
        with pytest.raises(TypeError) as cm:
            self.test_link.filename = 3

        assert str(cm.value) == \
            'Link.filename should be an instance of str, not int'

    def test_filename_attribute_is_set_to_empty_string(self):
        """testing if the filename value can be set to an empty string
        """
        self.test_link.filename = ''
        assert self.test_link.filename == ''

    def test_filename_attribute_value_comes_from_full_path(self):
        """testing if the filename attribute value is calculated from the
        full_path attribute
        """
        assert self.test_link.filename == '22-fdfffsd-32342-dsf2332-dsfd-3.exr'

    def test_filename_attribute_updates_the_full_path_attribute(self):
        """testing if the filename attribute is updating the full_path
        attribute properly
        """
        test_value = 'new_filename.tif'
        assert self.test_link.filename != test_value
        self.test_link.filename = test_value
        assert self.test_link.filename == test_value
        assert self.test_link.full_path == \
            'C:/A_NEW_PROJECT/td/dsdf/new_filename.tif'

    def test_filename_attribute_changes_also_the_extension(self):
        """testing if the filename attribute also changes the extension
        attribute
        """
        assert self.test_link.extension != '.an_extension'
        self.test_link.filename = 'some_filename_and.an_extension'
        assert self.test_link.extension == '.an_extension'

    def test_extension_attribute_is_set_to_None(self):
        """testing if the extension will be an empty string if it is set to
        None
        """
        self.test_link.extension = None
        assert self.test_link.extension == ''

    def test_extension_attribute_is_set_to_empty_string(self):
        """testing if the value of the extension can be set to an empty string
        """
        self.test_link.extension = ''
        assert self.test_link.extension == ''

    def test_extension_attribute_is_set_to_a_value_other_then_string(self):
        """testing if a TypeError will be raised when the extension attribute
        is set to a value other than string
        """
        with pytest.raises(TypeError) as cm:
            self.test_link.extension = 123

        assert str(cm.value) == \
            'Link.extension should be an instance of str, not int'

    def test_extension_attribute_value_comes_from_full_path(self):
        """testing if the extension attribute value is calculated from the
        full_path attribute
        """
        assert self.test_link.extension == '.exr'

    def test_extension_attribute_updates_the_full_path_attribute(self):
        """testing if the extension attribute is updating the full_path
        attribute properly
        """
        test_value = '.iff'
        assert self.test_link.extension != test_value
        self.test_link.extension = test_value
        assert self.test_link.extension == test_value
        assert self.test_link.full_path == \
            'C:/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.iff'

    def test_extension_attribute_updates_the_full_path_attribute_with_the_dot(self):
        """testing if the extension attribute is updating the full_path
        attribute properly even if a dot is not given as the first character
        """
        test_value = 'iff'
        expected_value = '.iff'
        assert self.test_link.extension != test_value
        self.test_link.extension = test_value
        assert self.test_link.extension == expected_value
        assert self.test_link.full_path == \
            'C:/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.iff'

    def test_extension_attribute_will_also_change_the_filename_attribute(self):
        """testing if the extension attribute is updating the filename
        attribute
        """
        test_value = '.targa'
        expected_value = '22-fdfffsd-32342-dsf2332-dsfd-3.targa'
        assert self.test_link.filename != expected_value
        self.test_link.extension = test_value
        assert self.test_link.filename == expected_value
