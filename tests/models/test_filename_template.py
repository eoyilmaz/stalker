# -*- coding: utf-8 -*-

import unittest
import pytest
from stalker import FilenameTemplate
from stalker.testing import UnitTestDBBase


class FilenameTemplateTester(unittest.TestCase):
    """tests the stalker.models.template.FilenameTemplate class
    """

    def setUp(self):
        """setup the test
        """
        super(FilenameTemplateTester, self).setUp()
        from stalker import Type, Asset, FilenameTemplate
        self.kwargs = {
            "name": "Test FilenameTemplate",
            "type": Type(
                name="Test Type",
                code='tt',
                target_entity_type="FilenameTemplate"
            ),
            "path": "ASSETS/{{asset.code}}/{{task.type.code}}/",
            "filename": "{{asset.code}}_{{version.take}}_{{task.type.code}}_" \
                        "{{version.version}}_{{user.initials}}",
            "output_path": "",
            "target_entity_type": 'Asset',
        }
        self.filename_template = FilenameTemplate(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Asset class
        """
        from stalker import FilenameTemplate
        assert FilenameTemplate.__auto_name__ is False

    def test_filename_template_is_not_strictly_typed(self):
        """testing if the FilenameTemplate class is not strictly typed
        """
        self.kwargs.pop("type")
        # no errors
        ft = FilenameTemplate(**self.kwargs)
        assert isinstance(ft, FilenameTemplate)

    def test_target_entity_type_argument_is_skipped(self):
        """testing if a TypeError will be raised when the target_entity_type
        argument is skipped
        """
        self.kwargs.pop("target_entity_type")
        with pytest.raises(TypeError) as cm:
            FilenameTemplate(**self.kwargs)

        assert str(cm.value) == \
            'FilenameTemplate.target_entity_type can not be None'

    def test_target_entity_type_argument_is_None(self):
        """testing if a TypeError will be raised when the target_entity_type
        argument is given as None
        """
        self.kwargs["target_entity_type"] = None
        with pytest.raises(TypeError) as cm:
            FilenameTemplate(**self.kwargs)

        assert str(cm.value) == \
            'FilenameTemplate.target_entity_type can not be None'

    def test_target_entity_type_attribute_is_read_only(self):
        """testing if a AttributeError will be raised when the
        target_entity_type attribute is tried to be changed
        """
        with pytest.raises(AttributeError) as cm:
            self.filename_template.target_entity_type = "Asset"

        assert str(cm.value) == "can't set attribute"

    def test_target_entity_type_argument_accepts_Classes(self):
        """testing if the target_entity_type can be set to a class directly
        """
        self.kwargs["target_entity_type"] = 'Asset'
        new_filenameTemplate = FilenameTemplate(**self.kwargs)

    def test_target_entity_type_attribute_is_converted_to_a_string_if_given_as_a_class(self):
        """testing if the target_entity_type attribute is converted when the
        target_entity_type is given as a class
        """
        self.kwargs["target_entity_type"] = 'Asset'
        ft = FilenameTemplate(**self.kwargs)
        assert ft.target_entity_type == "Asset"

    def test_path_argument_is_skipped(self):
        """testing if nothing happens when the path argument is skipped
        """
        self.kwargs.pop("path")
        ft = FilenameTemplate(**self.kwargs)
        assert isinstance(ft, FilenameTemplate)

    def test_path_argument_skipped_path_attribute_is_empty_string(self):
        """testing if the path attribute is an empty string if the
        path argument is skipped
        """
        self.kwargs.pop("path")
        ft = FilenameTemplate(**self.kwargs)
        assert ft.path == ""

    def test_path_argument_is_None_path_attribute_is_empty_string(self):
        """testing if the path attribute is an empty string when the
        path argument is None
        """
        self.kwargs["path"] = None
        ft = FilenameTemplate(**self.kwargs)
        assert ft.path == ""

    def test_path_argument_is_empty_string(self):
        """testing if nothing happens when the path argument is empty
        string
        """
        self.kwargs["path"] = ""
        ft = FilenameTemplate(**self.kwargs)
        assert isinstance(ft, FilenameTemplate)

    def test_path_attribute_is_empty_string(self):
        """testing if nothing happens when the path attribute is set to
        empty string
        """
        self.filename_template.path = ""

    def test_path_argument_is_not_string(self):
        """testing if a TypeError will be raised when the path argument is not
        a string
        """
        test_value = list("a list from a string")
        self.kwargs["path"] = test_value
        with pytest.raises(TypeError) as cm:
            FilenameTemplate(**self.kwargs)

        assert str(cm.value) == \
            'FilenameTemplate.path attribute should be string not list'

    def test_path_attribute_is_not_string(self):
        """testing if a TypeError will be raised when the path attribute is not
        set to a string
        """
        test_value = list("a list from a string")
        with pytest.raises(TypeError) as cm:
            self.filename_template.path = test_value

        assert str(cm.value) == \
            'FilenameTemplate.path attribute should be string not list'

    def test_filename_argument_is_skipped(self):
        """testing if nothing happens when the filename argument is skipped
        """
        self.kwargs.pop("filename")
        ft = FilenameTemplate(**self.kwargs)
        assert isinstance(ft, FilenameTemplate)

    def test_filename_argument_skipped_filename_attribute_is_empty_string(self):
        """testing if the filename attribute is an empty string if the
        filename argument is skipped
        """
        self.kwargs.pop("filename")
        ft = FilenameTemplate(**self.kwargs)
        assert ft.filename == ""

    def test_filename_argument_is_None_filename_attribute_is_empty_string(self):
        """testing if the filename attribute is an empty string when the
        filename argument is None
        """
        self.kwargs["filename"] = None
        ft = FilenameTemplate(**self.kwargs)
        assert ft.filename == ""

    def test_filename_argument_is_empty_string(self):
        """testing if nothing happens when the filename argument is empty
        string
        """
        self.kwargs["filename"] = ""
        ft = FilenameTemplate(**self.kwargs)
        assert isinstance(ft, FilenameTemplate)

    def test_filename_attribute_is_empty_string(self):
        """testing if nothing happens when the filename attribute is set to
        empty string
        """
        self.filename_template.filename = ""

    def test_filename_argument_is_not_string(self):
        """testing if a TypeError will be raised when filename argument is not
        string
        """
        test_value = list("a list from a string")
        self.kwargs["filename"] = test_value
        with pytest.raises(TypeError) as cm:
            FilenameTemplate(**self.kwargs)

        assert str(cm.value) == \
            'FilenameTemplate.filename attribute should be string not list'

    def test_filename_attribute_is_not_string(self):
        """testing if the given value converted to string for the filename
        attribute
        """
        test_value = list("a list from a string")
        with pytest.raises(TypeError) as cm:
            self.filename_template.filename = test_value

        assert str(cm.value) == \
            'FilenameTemplate.filename attribute should be string not list'

    def test_equality(self):
        """testing the equality of FilenameTemplate objects
        """
        ft1 = FilenameTemplate(**self.kwargs)

        from stalker import Entity
        new_entity = Entity(**self.kwargs)

        self.kwargs["target_entity_type"] = "Entity"
        ft2 = FilenameTemplate(**self.kwargs)

        self.kwargs["path"] = "different path"
        ft3 = FilenameTemplate(**self.kwargs)

        self.kwargs["filename"] = "different filename"
        ft4 = FilenameTemplate(**self.kwargs)

        assert self.filename_template == ft1
        assert not self.filename_template == new_entity
        assert not ft1 == ft2
        assert not ft2 == ft3
        assert not ft3 == ft4

    def test_inequality(self):
        """testing the inequality of FilenameTemplate objects
        """
        ft1 = FilenameTemplate(**self.kwargs)

        from stalker import Entity
        new_entity = Entity(**self.kwargs)

        self.kwargs["target_entity_type"] = "Entity"
        ft2 = FilenameTemplate(**self.kwargs)

        self.kwargs["path"] = "different path"
        ft3 = FilenameTemplate(**self.kwargs)

        self.kwargs["filename"] = "different filename"
        ft4 = FilenameTemplate(**self.kwargs)

        assert not self.filename_template != ft1
        assert self.filename_template != new_entity
        assert ft1 != ft2
        assert ft2 != ft3
        assert ft3 != ft4


class FilenameTemplateDBTestDBCase(UnitTestDBBase):
    """Tests the stalker.models.task.Task class with a DB
    """

    def setUp(self):
        """run once
        """
        super(self.__class__, self).setUp()

    def test_naming_case(self):
        """Test the case where naming should contain both Sequence Shot and
        other stuff
        (this is based on https://github.com/eoyilmaz/anima/issues/23)
        """
        from stalker.db.session import DBSession
        from stalker import Project, Task, Sequence, Shot, FilenameTemplate, \
            Version, Structure

        ft = FilenameTemplate(
            name='Normal Naming Convention',
            target_entity_type='Task',
            path='$REPO{{project.repository.id}}/{{project.code}}/{%- for parent_task in parent_tasks -%}{{parent_task.nice_name}}/{%- endfor -%}',
            filename="""{%- for p in parent_tasks -%}
                {%- if p.entity_type == 'Sequence' -%}
                    {{p.name}}
                {%- elif p.entity_type == 'Shot' -%}
                    _{{p.name}}{{p.children[0].name}}
                {%- endif -%}
            {%- endfor -%}
            {%- set fx = parent_tasks[-2] -%}
            _{{fx.name}}_{{version.take_name}}_v{{"%02d"|format(version.version_number)}}""",
        )
        DBSession.add(ft)

        st = Structure(
            name='Normal Project Structure',
            templates=[ft]
        )
        DBSession.add(st)

        test_project = Project(
            name='test001',
            code='test001',
            structure=st
        )
        DBSession.add(test_project)
        DBSession.commit()

        seq_task = Task(
            name='seq',
            project=test_project
        )
        DBSession.add(seq_task)

        ep101 = Sequence(
            name='ep101',
            code='ep101',
            parent=seq_task
        )
        DBSession.add(ep101)

        shot_task = Task(
            name='shot',
            parent=ep101
        )
        DBSession.add(shot_task)

        s001 = Shot(
            name='s001',
            code='s001',
            parent=shot_task
        )
        DBSession.add(s001)

        c001 = Task(
            name='c001',
            parent=s001
        )
        DBSession.add(c001)

        effects_scene = Task(
            name='effectScenes',
            parent=c001
        )
        DBSession.add(effects_scene)

        fxA = Task(
            name='fxA',
            parent=effects_scene
        )
        DBSession.add(fxA)

        maya = Task(
            name='maya',
            parent=fxA
        )
        DBSession.add(maya)
        DBSession.commit()

        v = Version(task=maya)
        v.update_paths()
        v.extension = '.ma'
        DBSession.add(v)
        DBSession.commit()

        assert v.filename == 'ep101_s001c001_fxA_Main_v01.ma'

