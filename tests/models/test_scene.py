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
from stalker import Scene


class SceneTester(UnitTestBase):
    """Tests stalker.models.scene.Scene class
    """

    def setUp(self):
        """setup the test
        """
        super(SceneTester, self).setUp()

        # create statuses
        from stalker import db, Status, StatusList
        self.test_status1 = Status(name="Status1", code="STS1")
        self.test_status2 = Status(name="Status2", code="STS2")
        self.test_status3 = Status(name="Status3", code="STS3")
        self.test_status4 = Status(name="Status4", code="STS4")
        self.test_status5 = Status(name="Status5", code="STS5")

        # create a test project, user and a couple of shots
        from stalker import Type
        self.project_type = Type(
            name="Test Project Type",
            code='test',
            target_entity_type='Project',
        )

        # create a status list for project
        self.project_status_list = StatusList(
            name="Project Statuses",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type='Project',
        )

        # create a repository
        self.repository_type = Type(
            name="Test Type",
            code='test',
            target_entity_type='Repository'
        )

        from stalker import Repository
        self.test_repository = Repository(
            name="Test Repository",
            type=self.repository_type,
        )

        # create projects
        from stalker import Project
        self.test_project = Project(
            name="Test Project 1",
            code='tp1',
            type=self.project_type,
            status_list=self.project_status_list,
            repository=self.test_repository,
        )

        self.test_project2 = Project(
            name="Test Project 2",
            code='tp2',
            type=self.project_type,
            status_list=self.project_status_list,
            repository=self.test_repository,
        )

        # the parameters
        self.kwargs = {
            "name": "Test Scene",
            'code': 'tsce',
            "description": "A test scene",
            "project": self.test_project,
        }

        # the test sequence
        self.test_scene = Scene(**self.kwargs)
        db.DBSession.add(self.test_scene)
        db.DBSession.commit()

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Scene class
        """
        self.assertFalse(Scene.__auto_name__)

    def test_shots_attribute_defaults_to_empty_list(self):
        """testing if the shots attribute defaults to an empty list
        """
        new_scene = Scene(**self.kwargs)
        self.assertEqual(new_scene.shots, [])

    def test_shots_attribute_is_set_None(self):
        """testing if a TypeError will be raised when the shots attribute will
        be set to None
        """
        with self.assertRaises(TypeError) as cm:
            self.test_scene.shots = None

        self.assertEqual(
            str(cm.exception),
            'Incompatible collection type: None is not list-like'
        )

    def test_shots_attribute_is_set_to_other_than_a_list(self):
        """testing if a TypeError will be raised when the shots attribute is
        tried to be set to something other than a list
        """
        test_value = [1, 1.2, "a string"]
        with self.assertRaises(TypeError) as cm:
            self.test_scene.shots = test_value

        self.assertEqual(
            str(cm.exception),
            'Scene.shots needs to be all stalker.models.shot.Shot instances, '
            'not int'
        )

    def test_shots_attribute_is_a_list_of_other_objects(self):
        """testing if a TypeError will be raised when the shots argument is a
        list of other type of objects
        """
        test_value = [1, 1.2, "a string"]
        with self.assertRaises(TypeError) as cm:
            self.test_scene.shots = test_value

        self.assertEqual(
            str(cm.exception),
            'Scene.shots needs to be all stalker.models.shot.Shot instances, '
            'not int'
        )

    def test_shots_attribute_elements_tried_to_be_set_to_non_Shot_object(self):
        """testing if a TypeError will be raised when the individual elements
        in the shots list tried to be set to something other than a Shot
        instance
        """
        with self.assertRaises(TypeError) as cm:
            self.test_scene.shots.append("a string")

        self.assertEqual(
            str(cm.exception),
            'Scene.shots needs to be all stalker.models.shot.Shot instances, '
            'not str'
        )

    def test_equality(self):
        """testing the equality of scenes
        """
        new_seq1 = Scene(**self.kwargs)
        new_seq2 = Scene(**self.kwargs)
        from stalker import Entity
        new_entity = Entity(**self.kwargs)

        self.kwargs["name"] = "a different scene"
        new_seq3 = Scene(**self.kwargs)

        self.assertTrue(new_seq1 == new_seq2)
        self.assertFalse(new_seq1 == new_seq3)
        self.assertFalse(new_seq1 == new_entity)

    def test_inequality(self):
        """testing the inequality of scenes
        """
        new_seq1 = Scene(**self.kwargs)
        new_seq2 = Scene(**self.kwargs)
        from stalker import Entity
        new_entity = Entity(**self.kwargs)

        self.kwargs["name"] = "a different scene"
        new_seq3 = Scene(**self.kwargs)

        self.assertFalse(new_seq1 != new_seq2)
        self.assertTrue(new_seq1 != new_seq3)
        self.assertTrue(new_seq1 != new_entity)

    def test_ProjectMixin_initialization(self):
        """testing if the ProjectMixin part is initialized correctly
        """
        from stalker import Status
        status1 = Status.query.filter_by(code="OH").first()

        from stalker import StatusList
        project_status_list = StatusList(
            name="Project Statuses", statuses=[status1],
            target_entity_type='Project'
        )

        from stalker import Type
        project_type = Type(
            name="Commercial",
            code='comm',
            target_entity_type='Project'
        )

        from stalker import Project
        new_project = Project(
            name="Test Project",
            code='tp',
            status=project_status_list[0],
            status_list=project_status_list,
            type=project_type,
            repository=self.test_repository
        )

        self.kwargs["project"] = new_project
        new_scene = Scene(**self.kwargs)
        self.assertEqual(new_scene.project, new_project)

    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ class attribute is False for
        Scene class.
        """
        self.assertEqual(Scene.__strictly_typed__, False)
