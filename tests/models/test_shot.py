# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest
from stalker import (Asset, Entity, Link, Project, Repository, Sequence, Shot,
                     Status, StatusList, Task, Type)

class ShotTester(unittest.TestCase):
    """Tests the Shot class
    """
    
    def setUp(self):
        """setup the test
        """
        class TestData(object):
            pass

        self.test_data = TestData()

        # statuses
        self.test_data.status_complete = Status(name="Complete", code="CMPLT")
        self.test_data.status_wip = Status(name="Work In Progress", code="WIP")
        self.test_data.status_waiting = Status(name="Waiting To Start",
                                               code="WTS")

        # status lists
        self.test_data.project_status_list = StatusList(
            name="Project Status List",
            statuses=[self.test_data.status_complete,
                      self.test_data.status_waiting,
                      self.test_data.status_wip],
            target_entity_type=Project,
            )

        self.test_data.sequence_status_list = StatusList(
            name="Project Status List",
            statuses=[self.test_data.status_complete,
                      self.test_data.status_waiting,
                      self.test_data.status_wip],
            target_entity_type=Sequence,
            )

        self.test_data.shot_status_list = StatusList(
            name="Shot Status List",
            statuses=[self.test_data.status_complete,
                      self.test_data.status_waiting,
                      self.test_data.status_wip],
            target_entity_type=Shot,
            )

        self.test_data.asset_status_list = StatusList(
            name="Asset Status List",
            statuses=[self.test_data.status_complete,
                      self.test_data.status_waiting,
                      self.test_data.status_wip],
            target_entity_type=Asset,
            )

        # types
        self.test_data.commercial_project_type = Type(
            name="Commercial Project",
            target_entity_type=Project,
            )

        self.test_data.character_asset_type = Type(
            name="Character",
            target_entity_type=Asset,
            )

        self.test_data.repository_type = Type(
            name="Test Repository Type",
            target_entity_type=Repository
        )

        # repository
        self.test_data.repository = Repository(
            name="Test Repository",
            type=self.test_data.repository_type,
            )

        # project and sequences
        self.test_data.project1 = Project(
            name="Test Project1",
            type=self.test_data.commercial_project_type,
            status_list=self.test_data.project_status_list,
            repository=self.test_data.repository,
            )

        self.test_data.sequence1 = Sequence(
            name="Test Seq1",
            project=self.test_data.project1,
            status_list=self.test_data.sequence_status_list,
            )

        self.test_data.sequence2 = Sequence(
            name="Test Seq2",
            project=self.test_data.project1,
            status_list=self.test_data.sequence_status_list,
            )

        self.test_data.sequence3 = Sequence(
            name="Test Seq3",
            project=self.test_data.project1,
            status_list=self.test_data.sequence_status_list,
            )

        self.test_data.asset1 = Asset(
            name="Test Asset1",
            project=self.test_data.project1,
            status_list=self.test_data.asset_status_list,
            type=self.test_data.character_asset_type,
            )

        self.test_data.asset2 = Asset(
            name="Test Asset2",
            project=self.test_data.project1,
            status_list=self.test_data.asset_status_list,
            type=self.test_data.character_asset_type,
            )

        self.test_data.asset3 = Asset(
            name="Test Asset3",
            project=self.test_data.project1,
            status_list=self.test_data.asset_status_list,
            type=self.test_data.character_asset_type,
            )

        self.test_data.cut_in_default = 1
        self.test_data.cut_duration_default = 1
        self.test_data.cut_out_default = 1

        self.kwargs = {
            "name": "SH123",
            "code": "SH123",
            "description": "This is a test Shot",
            "sequence": self.test_data.sequence1,
            "cut_in": 112,
            "cut_out": 149,
            "cut_duration": 123,
            "status": 0,
            "status_list": self.test_data.shot_status_list,
            #"assets": [self.test_data.asset1,
            #           self.test_data.asset2]
        }

        # create a mock shot object
        self.test_data.test_shot = Shot(**self.kwargs)


        #def test_name_attribute_is_a_uuid4_sequence(self):
        #"""testing if the name attribute is set to a proper uuid4 sequence
        #"""
        ## the length is 32 character
        #self.assertEqual(len(self.test_data.test_shot.name), 32)

        #import re

        ## and all the characters are in [0-9a-f] range
        #self.assertEqual(
        #re.sub("[0-9a-f]+","", self.test_data.test_shot.name), ""
        #)

        #def test_name_attribute_can_not_be_changed(self):
        #"""testing if the name attribute can not be changed
        #"""
        #test_value = "new_name"
        #before_value = self.test_data.test_shot.name
        #self.test_data.test_shot.name = test_value
        #self.assertEqual(self.test_data.test_shot.name, before_value)

    def test_sequence_argument_is_skipped(self):
        """testing if a TypeError will be raised when the sequence argument is
        skipped
        """
        self.kwargs.pop("sequence")
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_sequence_argument_is_None(self):
        """testing if a TypeError will be raised when the sequence argument is
        None
        """
        self.kwargs["sequence"] = None
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_sequence_argument_is_not_Sequence_instance(self):
        """testing if a TypeError will be raised when the given sequence
        argument is not an instance of stalker.models.sequence.Sequence
        """
        test_values = [1, 1.2, "sequence", ["a", "sequence"]]
        for test_value in test_values:
            self.kwargs["sequence"] = test_value
            self.assertRaises(TypeError, Shot, self.kwargs)

    def test_sequence_argument_already_has_a_shot_with_the_same_code(self):
        """testing if a ValueError will be raised when the given sequence
        argument already has a shot with the same code
        """
        # lets try to assign the shot to the mock_sequence2 which has another
        # shot with the same code
        self.kwargs["sequence"] = self.test_data.sequence2
        new_shot = Shot(**self.kwargs)
        self.assertRaises(ValueError, Shot, **self.kwargs)

        # this should not raise a ValueError
        self.kwargs["code"] = "DifferentCode"
        new_shot2 = Shot(**self.kwargs)

        #def test_sequence_attribute_is_read_only(self):
        #"""testing if the sequence attribute is read only
        #"""
        #self.assertRaises(AttributeError, setattr,self.test_data.test_shot,
        #"sequence", self.test_data.sequence2)

    def test_sequence_contains_shots(self):
        """testing if the current shot is going to be added to the sequence in
        the sequence object, so the Sequence.shots list will contain the
        current shot
        """
        self.assertIn(self.test_data.test_shot,
                      self.test_data.test_shot.sequence.shots)

    def test_sequence_argument_works_properly(self):
        """testing if the sequence argument works properly
        """
        self.assertEqual(self.test_data.test_shot.sequence,
                         self.kwargs["sequence"])
        
#    def test_code_argument_is_None(self):
#        """testing if a TypeError will be raised when the code argument is
#        None
#        """
#        self.kwargs["code"] = None
#        self.assertRaises(TypeError, Shot, **self.kwargs)

        #def test_code_attribute_is_None(self):
        #"""testing if a TypeError will be raised when the code argument is
        #None
        #"""
        #self.assertRaises(
        #TypeError,
        #setattr,
        #self.test_data.test_shot,
        #"code",
        #None
        #)

        #def test_code_argument_is_empty_string(self):
        #"""testing if the code attribute will be set to the same value with the
        #name when it is set to an empty string
        #"""
        #self.kwargs["code"] = ""
        #self.assertRaises(ValueError, Shot, **self.kwargs)

        #def test_code_attribute_is_empty_string(self):
        #"""testing if a ValueError will be raised when the code attribute is
        #empty string
        #"""
        #self.assertRaises(
        #ValueError,
        #setattr,
        #self.test_data.test_shot,
        #"code",
        #""
        #)

    def test_cut_in_argument_is_skipped_defaults_to_default_value(self):
        """testing if the cut_in argument is skipped the cut_in argument will
        be set to the default value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_in")
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_in, self.test_data.cut_in_default)

    def test_cut_in_argument_is_set_to_None_defaults_to_default_value(self):
        """testing if the cut_in argument is set to None the cut_in attribute
        is set to default value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = None
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_in, self.test_data.cut_in_default)

    def test_cut_in_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the cut_in argument is
        not an instance of int
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = "a string"
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_cut_in_attribute_is_not_integer(self):
        """testing if a TypeError will be used when the cut_in attribute is
        not an instance of int
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_data.test_shot,
            "cut_in",
            "a string"
        )

    def test_cut_in_argument_is_bigger_than_cut_out_argument(self):
        """testing if the cut_out attribute is updated when the cut_in
        argument is bigger than cut_out argument
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = self.kwargs["cut_out"] + 10
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)
        self.assertEqual(new_shot.cut_duration, 1)

    def test_cut_in_attribute_is_bigger_than_cut_out_attribute(self):
        """testing if the cut_out attribute is updated when the cut_in
        attribute is bigger than cut_out attribute
        """
        self.test_data.test_shot.cut_in = self.test_data.test_shot.cut_out + 10
        self.assertEqual(self.test_data.test_shot.cut_out,
                         self.test_data.test_shot.cut_in)
        self.assertEqual(self.test_data.test_shot.cut_duration, 1)

    def test_cut_out_argument_is_skipped_defaults_to_default_value(self):
        """testing if the cut_out argument is skipped the cut_out attribute
        will be set to the default value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_out")
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_out,
                         new_shot.cut_in + new_shot.cut_duration - 1)

    def test_cut_out_argument_is_set_to_None_defaults_to_default_value(self):
        """testing if the cut_out argument is set to None the cut_out attribute
        is set to default value
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = None
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_out,
                         new_shot.cut_in + new_shot.cut_duration - 1)

    def test_cut_out_attribute_is_set_to_None_defaults_to_default_value(self):
        """testing if the cut_out attribute is set to None it is going to be
        set to default value
        """
        self.test_data.test_shot.cut_out = None
        self.assertEqual(self.test_data.test_shot.cut_out,
                         self.test_data.test_shot.cut_in +\
                         self.test_data.test_shot.cut_duration - 1)

    def test_cut_out_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the cut_out argument is
        not an instance of int
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = "a string"
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_cut_out_attribute_is_not_integer(self):
        """testing if a TypeError will be used when the cut_out attribute is
        not an instance of int
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_data.test_shot,
            "cut_out",
            "a string"
        )

    def test_cut_out_argument_is_smaller_than_cut_in_argument(self):
        """testing if the cut_out attribute is updated when the cut_out
        argument is smaller than cut_in argument
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = self.kwargs["cut_in"] - 10
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)
        self.assertEqual(new_shot.cut_duration, 1)

    def test_cut_out_attribute_is_smaller_than_cut_in_attribute(self):
        """testing if the cut_out attribute is updated when it is smaller than
        cut_in attribute
        """
        self.test_data.test_shot.cut_out = self.test_data.test_shot.cut_in - 10
        self.assertEqual(self.test_data.test_shot.cut_out,
                         self.test_data.test_shot.cut_in)
        self.assertEqual(self.test_data.test_shot.cut_duration, 1)

    def test_cut_duration_argument_is_skipped(self):
        """testing if the cut_duration attribute will be calculated from the
        cut_in and cut_out attributes when the cut_duration argument is skipped
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_duration")
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration, new_shot.cut_out -
                                                new_shot.cut_in + 1)

    def test_cut_duration_argument_is_None(self):
        """testing if the value of cut_duration will be calculated from the
        cut_in and cut_out attributes.
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = None
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration, new_shot.cut_out -
                                                new_shot.cut_in + 1)

    def test_cut_duration_argument_is_not_instance_of_int(self):
        """testing if a TypeError will be raised when the cut_duration
        argument is not an instance of int
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = "a string"
        self.assertRaises(TypeError, Shot, **self.kwargs)

    def test_cut_duration_attribute_is_not_instance_of_int(self):
        """testing if a TypeError will be raised when the cut_duration
        attribute is not an instance of int
        """
        self.assertRaises(
            TypeError,
            setattr,
            self.test_data.test_shot,
            "cut_duration",
            "a string"
        )

    def test_cut_duration_attribute_will_be_updated_when_cut_in_attribute_changed(self):
        """testing if the cut_duration attribute will be updated when the
        cut_in attribute changed
        """
        self.test_data.test_shot.cut_in = 1
        self.assertEqual(
            self.test_data.test_shot.cut_duration,
            self.test_data.test_shot.cut_out - 
            self.test_data.test_shot.cut_in + 1
        )

    def test_cut_duration_attribute_will_be_updated_when_cut_out_attribute_changed(self):
        """testing if the cut_duration attribute will be updated when the
        cut_out attribute changed
        """
        self.test_data.test_shot.cut_out = 1000
        self.assertEqual(self.test_data.test_shot.cut_duration,
                         self.test_data.test_shot.cut_out -\
                         self.test_data.test_shot.cut_in + 1)

    def test_cut_duration_attribute_changes_cut_out_attribute(self):
        """testing if changes in cut_duration attribute will also affect
        cut_out value.
        """
        first_cut_out = self.test_data.test_shot.cut_out
        self.test_data.test_shot.cut_in
        self.test_data.test_shot.cut_duration = 245
        self.assertNotEquals(self.test_data.test_shot.cut_out, first_cut_out)
        self.assertEqual(self.test_data.test_shot.cut_out,
                         self.test_data.test_shot.cut_in +\
                         self.test_data.test_shot.cut_duration - 1)

    def test_cut_duration_attribute_is_zero(self):
        """testing if the cut_duration attribute will be set to 1 and the
        cut_out is updated to the same value with cut_in when the cut_duration
        attribute is set to zero
        """
        self.test_data.test_shot.cut_duration = 0
        self.assertEqual(self.test_data.test_shot.cut_out,
                         self.test_data.test_shot.cut_in)
        self.assertEqual(self.test_data.test_shot.cut_duration, 1)

    def test_cut_duration_attribute_is_negative(self):
        """testing if the cut_duration attribute will be set to 1  and the
        cut_out is updated to the same value with cut_in when the cut_duration
        attribute is set to a negative value
        """
        self.test_data.test_shot.cut_duration = -100
        self.assertEqual(self.test_data.test_shot.cut_out,
                         self.test_data.test_shot.cut_in)
        self.assertEqual(self.test_data.test_shot.cut_duration, 1)

    def test_cut_duration_argument_is_zero_and_cut_out_argument_is_skipped(self):
        """testing if the cut_duration attribute will be set to 1 and the
        cut_out is updated to the same value with cut_in when the cut_duration
        argument is zero and there is no cut_out argument given
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = 0
        self.kwargs.pop("cut_out")
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration, 1)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)

    def test_cut_duration_argument_is_negative_and_cut_out_argument_is_skipped(self):
        """testing if the cut_duration attribute is going to be set to 1 and
        the cut_out will be updated to the same value with the cut_in attribute
        when the cut_duration argument is given as zero and the cut_out
        argument is skipped
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = -10
        self.kwargs.pop("cut_out")
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration, 1)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)

    def test_cut_duration_argument_is_zero_and_cut_out_argument_is_not_None(self):
        """testing if the cut_duration attribute is going to be set to 1 and
        cut_output will be calculated from cut_in and cut_duration when the
        cut_duration argument is given as zero and there is a cut_out argument
        given
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = 0
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration, 1)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)

    def test_cut_duration_argument_is_negative_and_cut_out_argument_is_not_None(self):
        """testing if the cut_duration attribute is going to be set to 1 and
        cut_output will be calculated from cut_in and cut_duration when the
        cut_duration argument is given as negative and there is a cut_out
        argument given
        """
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = -100
        new_shot = Shot(**self.kwargs)
        self.assertEqual(new_shot.cut_duration, 1)
        self.assertEqual(new_shot.cut_out, new_shot.cut_in)

    def test_equality(self):
        """testing equality of shot objects
        """
        self.kwargs["code"] = "SH123A"
        new_shot1 = Shot(**self.kwargs)

        self.kwargs["sequence"] = self.test_data.sequence3
        new_shot2 = Shot(**self.kwargs)
        # an entity with the same parameters
        # just set the name to the code too
        self.kwargs["name"] = self.kwargs["code"]
        new_entity = Entity(**self.kwargs)

        # another shot with different code
        self.kwargs["code"] = "SHAnotherShot"
        new_shot3 = Shot(**self.kwargs)

        self.assertFalse(new_shot1 == new_shot2)
        self.assertFalse(new_shot1 == new_entity)
        self.assertFalse(new_shot1 == new_shot3)

    def test_inequality(self):
        """testing inequality of shot objects
        """
        self.kwargs["code"] = "SH123A"
        new_shot1 = Shot(**self.kwargs)

        self.kwargs["sequence"] = self.test_data.sequence3
        new_shot2 = Shot(**self.kwargs)
        # an entity with the same parameters
        # just set the name to the code too
        self.kwargs["name"] = self.kwargs["code"]
        new_entity = Entity(**self.kwargs)

        # another shot with different code
        self.kwargs["code"] = "SHAnotherShot"
        new_shot3 = Shot(**self.kwargs)

        self.assertTrue(new_shot1 != new_shot2)
        self.assertTrue(new_shot1 != new_entity)
        self.assertTrue(new_shot1 != new_shot3)

    def test_ReferenceMixin_initialization(self):
        """testing if the ReferenceMixin part is initialized correctly
        """
        link_type_1 = Type(name="Image", target_entity_type="Link")

        link1 = Link(name="Artwork 1", path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="a.jpg", type=link_type_1)

        link2 = Link(name="Artwork 2", path="/mnt/M/JOBs/TEST_PROJECT",
                     filename="b.jbg", type=link_type_1)

        references = [link1, link2]

        self.kwargs["code"] = "SH12314"
        self.kwargs["references"] = references

        new_shot = Shot(**self.kwargs)

        self.assertEqual(new_shot.references, references)

    def test_StatusMixin_initialization(self):
        """testing if the StatusMixin part is initialized correctly
        """
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Complete", code="CMPLT")

        status_list = StatusList(name="Project Statuses",
                                 statuses=[status1, status2],
                                 target_entity_type=Shot)

        self.kwargs["code"] = "SH12314"
        self.kwargs["status"] = 0
        self.kwargs["status_list"] = status_list

        new_shot = Shot(**self.kwargs)

        self.assertEqual(new_shot.status_list, status_list)

    def test_TaskMixin_initialization(self):
        """testing if the TaskMixin part is initialized correctly
        """
        status1 = Status(name="On Hold", code="OH")

        task_status_list = StatusList(name="Task Statuses",
                                      statuses=[status1],
                                      target_entity_type=Task)

        project_status_list = StatusList(
            name="Project Statuses", statuses=[status1],
            target_entity_type=Project
        )

        project_type = Type(
            name="Commercial",
            target_entity_type=Project
        )

        new_project = Project(
            name="Commercial",
            status_list=project_status_list,
            type=project_type,
            repository=self.test_data.repository,
            )

        self.kwargs["code"] = "SH12314"

        new_shot = Shot(**self.kwargs)

        task1 = Task(
            name="Modeling", status=0,
            status_list=task_status_list,
            project=new_project,
            task_of=new_shot,
            )

        task2 = Task(
            name="Lighting",
            status=0,
            status_list=task_status_list,
            project=new_project,
            task_of=new_shot,
            )

        tasks = [task1, task2]

        self.assertItemsEqual(new_shot.tasks, tasks)

    def test__repr__(self):
        """testing the represantation of Shot
        """
        self.assertEqual(
            self.test_data.test_shot.__repr__(),
            "<Shot (%s, %s)>" % (self.test_data.test_shot.code,
                                 self.test_data.test_shot.code)
        )

        #def test_plural_name(self):
        #"""testing the plural name of Shot class
        #"""
        #self.assertTrue(Shot.plural_name, "Shots")

    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ class attribute is False for
        Shot class
        """
        self.assertEqual(Shot.__strictly_typed__, False)

#    def test_assets_argument_is_skipped(self):
#        """testing if the assets attribute will be an empty list when the
#        assets argument is skipped
#        """
#        self.kwargs["code"] = "SHAnotherShot"
#        self.kwargs.pop("assets")
#        new_shot = Shot(**self.kwargs)
#        self.assertEqual(new_shot.assets, [])
#
#
#    def test_assets_argument_is_None(self):
#        """testing if the assets attribute will be an empty list when the
#        assets argument is None
#        """
#        self.kwargs["code"] = "SHAnotherShot"
#        self.kwargs["assets"] = None
#        new_shot = Shot(**self.kwargs)
#        self.assertEqual(new_shot.assets, [])
#
#
#    def test_assets_attribute_is_None(self):
#        """testing if a TypeError will be raised when the assets attribute is
#        set to None
#        """
#
#        self.assertRaises(TypeError, setattr, self.test_data.test_shot,
#                          "assets", None)
#
#
#    def test_assets_argument_is_not_a_list(self):
#        """testing if a TypeError will be raised when the assets argument is
#        not a list
#        """
#        self.kwargs["code"] = "SHAnotherShot"
#        self.kwargs["assets"] = 1
#        self.assertRaises(TypeError, Shot, **self.kwargs)
#
#
#    def test_assets_attribute_is_not_a_list(self):
#        """testing if a TypeError will be raised when the assets attribute is
#        set to a non list value
#        """
#
#        self.assertRaises(TypeError, setattr, self.test_data.test_shot,
#                          "assets", 1)
#
#
#    def test_assets_argument_is_not_a_list_of_Asset_instances(self):
#        """testing if a TypeError will be raised when the assets argument is
#        a list but not a list of Asset instances
#        """
#        self.kwargs["code"] = "SHAnotherShot"
#        self.kwargs["assets"] = [1, "a string", ["a", "list"]]
#        self.assertRaises(TypeError, Shot, **self.kwargs)
#
#
#    def test_assets_attribute_is_not_a_list_of_Asset_instances(self):
#        """testing if a TypeError will be raised when the assets attribute is
#        set to a list but not a list of Asset instances
#        """
#
#        self.assertRaises(TypeError, setattr, self.test_data.test_shot,
#                          "assets", [1, "a string", ["a", "list"]])
#
#
#    def test_assets_argument_is_a_list_of_Asset_instances(self):
#        """testing if the assets shots attribute will contain the current shot
#        when the assets argument is a list of Asset instances
#        """
#
#        self.kwargs["code"] = "SHAnotherShot"
#        self.kwargs["assets"] = [self.test_data.asset1, self.test_data.asset2]
#        new_shot = Shot(**self.kwargs)
#
#        self.assertIn(new_shot, self.test_data.asset1.shots)
#        self.assertIn(new_shot, self.test_data.asset2.shots)
#
#
#    def test_assets_attribute_is_a_list_of_Asset_instances(self):
#        """testing if the assets shots attribute will contain the current shot
#        when the assets attribute is set to a list of Asset instances
#        """
#
#        self.kwargs["code"] = "SHAnotherShot"
#        self.kwargs.pop("assets")
#        new_shot = Shot(**self.kwargs)
#        new_shot.assets = [self.test_data.asset1, self.test_data.asset2]
#
#        self.assertIn(new_shot, self.test_data.asset1.shots)
#        self.assertIn(new_shot, self.test_data.asset2.shots)
#
#
#    def test_assets_attribute_will_update_the_Asset_shot_attribute(self):
#        """testing if the assets attribute will update the Asset.shots
#        attribute
#        """
#
#        self.kwargs["code"] = "SHAnotherShot"
#        self.kwargs.pop("assets")
#        new_shot = Shot(**self.kwargs)
#
#        new_shot.assets = [self.test_data.asset1, self.test_data.asset2]
#
#        self.assertIn(new_shot, self.test_data.asset1.shots)
#        self.assertIn(new_shot, self.test_data.asset2.shots)
#
#        new_shot.assets = [self.test_data.asset3]
#
#        self.assertIn(new_shot, self.test_data.asset3.shots)
#        self.assertNotIn(new_shot, self.test_data.asset1.shots)
#        self.assertNotIn(new_shot, self.test_data.asset2.shots)
#
#        # now append a new asset
#        new_shot.assets.append(self.test_data.asset1)
#        self.assertIn(new_shot, self.test_data.asset1.shots)
#
#        # remove one
#        new_shot.assets.remove(self.test_data.asset3)
#        self.assertNotIn(new_shot, self.test_data.asset3.shots)
#
#        # pop one
#        new_shot.assets.pop()
#        self.assertNotIn(new_shot, self.test_data.asset1.shots)
#
#        # extend
#        new_shot.assets.extend([self.test_data.asset1,
#                                self.test_data.asset2,
#                                self.test_data.asset3])
#
#        self.assertIn(new_shot, self.test_data.asset1.shots)
#        self.assertIn(new_shot, self.test_data.asset2.shots)
#        self.assertIn(new_shot, self.test_data.asset3.shots)
