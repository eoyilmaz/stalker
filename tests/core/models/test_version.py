#-*- coding: utf-8 -*-



import unittest
from stalker.conf import defaults
from stalker.core.models import (Version, Repository, Type, Project, Status,
                                 StatusList, Sequence, Shot, Task, Link,
                                 Review)






########################################################################
class VersionTester(unittest.TestCase):
    """tests stalker.core.models.Version class
    """
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # statuses
        self.test_status1 = Status(name="Status1", code="STS1")
        self.test_status2 = Status(name="Status2", code="STS2")
        self.test_status3 = Status(name="Status3", code="STS3")
        self.test_status4 = Status(name="Status4", code="STS4")
        self.test_status5 = Status(name="Status5", code="STS5")
        
        # status lists
        self.test_project_status_list = StatusList(
            name="Project Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Project,
        )
        
        self.test_sequence_status_list = StatusList(
            name="Sequence Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Sequence,
        )
        
        self.test_shot_status_list = StatusList(
            name="Shot Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Shot,
        )
        
        self.test_task_status_list = StatusList(
            name="Task Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Task,
        )
        
        self.test_version_status_list = StatusList(
            name="Version Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Version,
        )
        
        # repository
        self.test_repo = Repository(
            name="Test Repository",
        )
        
        # a project type
        self.test_project_type = Type(
            name="Test",
            target_entity_type=Project,
        )
        
        # create a project
        self.test_project = Project(
            name="Test Project",
            type=self.test_project_type,
            status_list=self.test_project_status_list,
            repository=self.test_repo,
        )
        
        # create a sequence
        self.test_sequence = Sequence(
            name="Test Sequence",
            code="SEQ1",
            project=self.test_project,
            status_list=self.test_sequence_status_list,
        )
        
        # create a shot
        self.test_shot1 = Shot(
            code="SH001",
            sequence=self.test_sequence,
            status_list=self.test_shot_status_list,
        )
        
        # create a group of Tasks for the shot
        self.test_task1 = Task(
            name="Task1",
            task_of=self.test_shot1,
            status_list=self.test_task_status_list,
        )
        
        # a Link for the source_file
        self.test_source_link = Link(
            name="Link1",
            path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/v001.ma",
        )
        
        # a Link for the ouput file
        self.test_output_link1 = Link(
            name="Output Link 1",
            path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/Outputs/"\
                 "SH001_beauty_v001.###.exr"
        )
        
        self.test_output_link2 = Link(
            name="Output Link 2",
            path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/Outputs/"\
                 "SH001_occ_v001.###.exr"
        )
        
        # now create a version for the Task
        self.kwargs = {
            "name": "Version1",
            "take": "TestTake",
            "source": self.test_source_link,
            "outputs": [self.test_output_link1,
                        self.test_output_link2,],
            "version_of": self.test_task1,
            "status_list": self.test_version_status_list,
            "version": 1,
        }
        
        # and the Version
        self.test_version = Version(**self.kwargs)
        
        # set the published to False
        self.test_version.published = False
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_skipped_defaults_to_default_value(self):
        """testing if the take argument is skipped the take attribute is going
        to be set to the default value which is
        stalker.conf.defaults.DEFAULT_VERSION_TAKE_NAME
        """
        
        self.kwargs.pop("take")
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.take, defaults.DEFAULT_VERSION_TAKE_NAME)
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_None(self):
        """testing if a TypeError will be raised when the take argument is None
        """
        
        self.kwargs["take"] = None
        self.assertRaises(TypeError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_None(self):
        """testing if a TypeError will be raised when the take attribute is set
        to None
        """
        
        self.assertRaises(TypeError, setattr, self.test_version, "take", None)
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_empty_string(self):
        """testing if a ValueError will be raised when the take argument is
        given as an empty string
        """
        
        self.kwargs["take"] = ""
        self.assertRaises(ValueError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_empty_string(self):
        """testing if a ValueError will be raised when the take attribute is
        set to an empty string
        """
        
        self.assertRaises(ValueError, setattr, self.test_version, "take", "")
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_not_a_string_will_be_converted_to_one(self):
        """testing if the given take argument is not a string will be converted
        to a proper string
        """
        
        test_values = [
            (1, "1"),
            (1.2, "12"),
            (["a list"], "alist"),
            ({"a": "dict"}, "adict")]
        
        for test_value in test_values:
            self.kwargs["take"] = test_value[0]
            new_version = Version(**self.kwargs)
            
            self.assertEqual(new_version.take, test_value[1])
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_not_a_string_will_be_converted_to_one(self):
        """testing if the given take attribute is not a string will be
        converted to a proper string
        """
        
        test_values = [
            (1, "1"),
            (1.2, "12"),
            (["a list"], "alist"),
            ({"a": "dict"}, "adict")]
        
        for test_value in test_values:
            self.test_version.take = test_value[0]
            self.assertEqual(self.test_version.take, test_value[1])
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take argument string
        is formatted to an empty string
        """
        
        self.kwargs["take"] = "##$½#$"
        self.assertRaises(ValueError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take argument string
        is formatted to an empty string
        """
        
        self.assertRaises(ValueError, setattr, self.test_version, "take",
                          "##$½#$")
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_skipped(self):
        """testing if a TypeError will be raised when the version argument is
        skipped
        """
        
        self.kwargs.pop("version")
        self.assertRaises(TypeError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_None(self):
        """testing if a TypeError will be raised when the version argument is
        None
        """
        
        self.kwargs["version"] = None
        self.assertRaises(TypeError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_version_attribute_is_None(self):
        """testing if a TypeError will be raised when the version attribute is
        set to None
        """
        
        self.assertRaises(TypeError, self.test_version, "version", None)
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_0(self):
        """testing if a ValueError will be raised when the version argument is
        0
        """
        
        self.kwargs["version"] = 0
        self.assertRaises(ValueError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_version_attribute_is_0(self):
        """testing if a ValueError will be raised when the version attribute is
        set to 0
        """
        
        self.assertRaises(ValueError, setattr, self.test_version, "version", 0)
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_negative(self):
        """testing if a ValueError will be raised when the version argument is
        negative
        """
        
        self.kwargs["version"] = -1
        self.assertRaises(ValueError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_version_attribute_is_negative(self):
        """testing if a ValueError will be raised when the version attribute is
        negative
        """
        
        self.assertRaises(ValueError, setattr, self.test_version, "version",
                          -1)
    
    
    
    ##----------------------------------------------------------------------
    #def test_published_attribute_is_set_to_non_bool_value(self):
        #"""testing if the published attribute is set to a non bool value will
        #be converted to a bool value
        #"""
        
        #test_value = "no bool value"
        #self.test_version.published = test_value
        #self.assertEqual(self.test_version.published, bool(test_value))
    
    
    
    ##----------------------------------------------------------------------
    #def test_published_attribute_defaults_to_false(self):
        #"""testing if the default value of published for newly created Versions
        #is False
        #"""
        
        #new_version = Version(**self.kwargs)
        #self.assertEqual(new_version.published, False)
    
    
    
    ##----------------------------------------------------------------------
    #def test_published_attribute_is_working_properly(self):
        #"""testing if the published attribute is working properly
        #"""
        
        #test_value = True
        #new_version = Version(**self.kwargs)
        #new_version.published = test_value
        #self.assertEqual(new_version.published, test_value)
        
        #test_value = False
        #new_version.published = test_value
        #self.assertEqual(new_version.published, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_version_of_argument_is_skipped(self):
        """testing if a TypeError will be raised when the version_of argument
        is skipped
        """
        
        self.kwargs.pop("version_of")
        self.assertRaises(TypeError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_version_of_argument_is_None(self):
        """testing if a TypeError will be raised when the version_of argument
        is None
        """
        
        self.kwargs["version_of"] = None
        self.assertRaises(TypeError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_version_of_attribute_is_None(self):
        """testing if a TypeError will be raised when the version_of attribute
        is None
        """
        self.assertRaises(TypeError, setattr, self.test_version,
                          "version_of", None)
    
    
    
    #----------------------------------------------------------------------
    def test_version_of_argument_is_not_a_Task(self):
        """testing if a TypeError will be raised when the version_of argumment
        is not a Task instance
        """
        
        self.kwargs["version_of"] = "a task"
        self.assertRaises(TypeError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_version_of_attribute_is_not_a_Task(self):
        """testing if a TypeError will be raised when the version_of attribute
        is not a Task instance
        """
        
        self.assertRaises(TypeError, setattr, self.test_version, "version_of",
                          "a task")
    
    
    
    #----------------------------------------------------------------------
    def test_version_of_attribute_is_working_properly(self):
        """testing if the version_of attribute is working properly
        """
        
        new_task = Task(
            name="New Test Task",
            task_of=self.test_shot1,
            status_list=self.test_task_status_list,
        )
        
        self.assertIsNot(self.test_version.version_of, new_task)
        
        self.test_version.version_of = new_task
        self.assertIs(self.test_version.version_of, new_task)
    
    
    
    #----------------------------------------------------------------------
    def test_source_argument_is_skipped(self):
        """testing if the source will be None when the source argument is
        skipped
        """
        
        self.kwargs.pop("source")
        new_version = Version(**self.kwargs)
        self.assertIs(new_version.source, None)
    
    
    
    #----------------------------------------------------------------------
    def test_source_argument_is_None(self):
        """testing if the source will be None when the source argument is None
        """
        
        self.kwargs["source"] = None
        new_version = Version(**self.kwargs)
        self.assertIs(new_version.source, None)
    
    
    
    #----------------------------------------------------------------------
    def test_source_argument_is_not_a_Link_instance(self):
        """testing if a TypeError will be raised when the source argument is
        not a stalker.core.models.Link instance
        """
        
        self.kwargs["source"] = 123123
        self.assertRaises(TypeError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_source_attribute_is_not_a_Link_instance(self):
        """testing if a TypeError will be raised when the source attribute is
        set to something other than a Link instance
        """
        
        self.assertRaises(TypeError, setattr, self.test_version, "source", 121)
    
    
    
    #----------------------------------------------------------------------
    def test_source_argument_is_working_properly(self):
        """testing if the source argument is working properly
        """
        
        new_source = Link(name="Test Link", path="none")
        self.kwargs["source"] = new_source
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.source, new_source)
    
    
    
    #----------------------------------------------------------------------
    def test_source_attribute_is_working_properly(self):
        """testing if the source attribute is working properly
        """
        new_source = Link(name="Test Link", path="empty string")
        self.assertNotEqual(self.test_version.source, new_source)
        self.test_version.source = new_source
        self.assertEqual(self.test_version.source, new_source)
    
    
    
    
    #----------------------------------------------------------------------
    def test_outputs_argument_is_skipped(self):
        """testing if the outputs attribute will be an empty list when the
        outputs argument is skipped
        """
        
        self.kwargs.pop("outputs")
        new_version = Version(**self.kwargs)
        self.assertEquals(new_version.outputs, [])
    
    
    
    #----------------------------------------------------------------------
    def test_outputs_argument_is_None(self):
        """testing if the outputs attribute will be an empty list when the
        outputs argument is None
        """
        
        self.kwargs["outputs"] = None
        new_version = Version(**self.kwargs)
        self.assertEquals(new_version.outputs, [])
    
    
    
    #----------------------------------------------------------------------
    def test_outputs_attribute_is_None(self):
        """testing if a TypeError will be raised when the outputs argument is
        set to None
        """
        
        self.assertRaises(TypeError, setattr, self.test_version, "outputs",
                          None)
    
    
    
    #----------------------------------------------------------------------
    def test_outputs_argument_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the outputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, "231123"]
        self.kwargs["outputs"] = test_value
        self.assertRaises(TypeError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_outputs_attribute_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the outputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, "231123"]
        self.assertRaises(TypeError, setattr, self.test_version, "outputs",
                          test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_outputs_attribute_is_working_properly(self):
        """testing if the outputs attribute is working properly
        """
        self.kwargs.pop("outputs")
        new_version = Version(**self.kwargs)
        
        self.assertNotIn(self.test_output_link1, new_version.outputs)
        self.assertNotIn(self.test_output_link2, new_version.outputs)
        
        new_version.outputs = [self.test_output_link1, self.test_output_link2]
        
        self.assertIn(self.test_output_link1, new_version.outputs)
        self.assertIn(self.test_output_link2, new_version.outputs)
    
    
    
    #----------------------------------------------------------------------
    def test_published_attribute_is_False_by_default(self):
        """tetsing if the published attribute is False by default
        """
        
        self.assertEquals(self.test_version.published, False)
    
    
    
    #----------------------------------------------------------------------
    def test_published_attribute_is_working_properly(self):
        """testing if the published attribute is working properly
        """
        
        self.test_version.published = True
        self.assertEquals(self.test_version.published, True)
        
        self.test_version.published = False
        self.assertEquals(self.test_version.published, False)
    
    
    