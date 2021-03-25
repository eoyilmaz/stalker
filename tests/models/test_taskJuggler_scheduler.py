# -*- coding: utf-8 -*-

import os

import pytest
import pytz
import datetime
from stalker import TaskJugglerScheduler
from stalker.testing import UnitTestDBBase


class TaskJugglerSchedulerDBTester(UnitTestDBBase):
    """tests the stalker.models.scheduler.TaskJugglerScheduler class
    """

    def setUp(self):
        """set up the test
        """
        super(self.__class__, self).setUp()

        # create departments
        from stalker import Department
        self.test_dep1 = Department(name='Dep1')
        self.test_dep2 = Department(name='Dep2')

        # create resources
        from stalker import User
        self.test_user1 = User(
            login='user1',
            name='User1',
            email='user1@users.com',
            password='1234',
            departments=[self.test_dep1]
        )
        from stalker.db.session import DBSession
        DBSession.add(self.test_user1)

        self.test_user2 = User(
            login='user2',
            name='User2',
            email='user2@users.com',
            password='1234',
            departments=[self.test_dep1]
        )
        DBSession.add(self.test_user2)

        self.test_user3 = User(
            login='user3',
            name='User3',
            email='user3@users.com',
            password='1234',
            departments=[self.test_dep2]
        )
        DBSession.add(self.test_user3)

        self.test_user4 = User(
            login='user4',
            name='User4',
            email='user4@users.com',
            password='1234',
            departments=[self.test_dep2]
        )
        DBSession.add(self.test_user4)

        # user with two departments
        self.test_user5 = User(
            login='user5',
            name='User5',
            email='user5@users.com',
            password='1234',
            departments=[self.test_dep1, self.test_dep2]
        )
        DBSession.add(self.test_user5)

        # user with no departments
        self.test_user6 = User(
            login='user6',
            name='User6',
            email='user6@users.com',
            password='1234'
        )
        DBSession.add(self.test_user6)

        # repository
        from stalker import Repository
        self.test_repo = Repository(
            name='Test Repository',
            code='TR',
            linux_path='/mnt/T/',
            windows_path='T:/',
            osx_path='/Volumes/T/'
        )
        DBSession.add(self.test_repo)

        # statuses
        from stalker import Status
        self.test_status1 = Status(name='Status 1', code='STS1')
        self.test_status2 = Status(name='Status 2', code='STS2')
        self.test_status3 = Status(name='Status 3', code='STS3')
        self.test_status4 = Status(name='Status 4', code='STS4')
        self.test_status5 = Status(name='Status 5', code='STS5')
        DBSession.add_all([
            self.test_status1, self.test_status2, self.test_status3,
            self.test_status4, self.test_status5
        ])

        # create one project
        from stalker import Project
        self.test_proj1 = Project(
            name='Test Project 1',
            code='TP1',
            repository=self.test_repo,
            start=datetime.datetime(2013, 4, 4, tzinfo=pytz.utc),
            end=datetime.datetime(2013, 5, 4, tzinfo=pytz.utc)
        )
        DBSession.add(self.test_proj1)
        self.test_proj1.now = datetime.datetime(2013, 4, 4, tzinfo=pytz.utc)

        # create two tasks with the same resources
        from stalker import Task
        self.test_task1 = Task(
            name='Task1',
            project=self.test_proj1,
            resources=[self.test_user1, self.test_user2],
            alternative_resources=[
                self.test_user3, self.test_user4, self.test_user5
            ],
            schedule_model=0,
            schedule_timing=50,
            schedule_unit='h',
        )
        DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='Task2',
            project=self.test_proj1,
            resources=[self.test_user1, self.test_user2],
            alternative_resources=[
                self.test_user3, self.test_user4, self.test_user5
            ],
            depends=[self.test_task1],
            schedule_model=0,
            schedule_timing=60,
            schedule_unit='h',
            priority=800
        )
        DBSession.save(self.test_task2)

    def test_tjp_file_is_created(self):
        """testing if the tjp file is correctly created
        """
        # create the scheduler
        tjp_sched = TaskJugglerScheduler()
        tjp_sched.projects = [self.test_proj1]

        tjp_sched._create_tjp_file()
        tjp_sched._create_tjp_file_content()
        tjp_sched._fill_tjp_file()

        # check
        assert os.path.exists(tjp_sched.tjp_file_full_path)

        # clean up the test
        tjp_sched._clean_up()

    def test_tjp_file_content_is_correct(self):
        """testing if the tjp file content is correct
        """
        # enter a couple of time logs
        from stalker import TimeLog
        tlog1 = TimeLog(
            resource=self.test_user1,
            task=self.test_task1,
            start=datetime.datetime(2013, 4, 16, 6, 0, tzinfo=pytz.utc),
            end=datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
        )
        from stalker.db.session import DBSession
        DBSession.add(tlog1)
        DBSession.commit()

        tjp_sched = TaskJugglerScheduler()
        from stalker import Studio
        test_studio = Studio(
            name='Test Studio',
            timing_resolution=datetime.timedelta(minutes=30)
        )
        test_studio.daily_working_hours = 9

        test_studio.id = 564
        test_studio.start = \
            datetime.datetime(2013, 4, 16, 0, 7, tzinfo=pytz.utc)
        test_studio.end = datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc)
        test_studio.now = datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
        tjp_sched.studio = test_studio

        tjp_sched._create_tjp_file()
        tjp_sched._create_tjp_file_content()

        assert TimeLog.query.all() != []

        import jinja2
        expected_tjp_template = jinja2.Template(
            """# Generated By Stalker v{{stalker.__version__}}
        
project Studio_564 "Studio_564" 2013-04-16 - 2013-06-30 {
    timingresolution 30min
    now 2013-04-16-00:00
    dailyworkinghours 9
    weekstartsmonday
    workinghours mon 09:00 - 18:00
    workinghours tue 09:00 - 18:00
    workinghours wed 09:00 - 18:00
    workinghours thu 09:00 - 18:00
    workinghours fri 09:00 - 18:00
    workinghours sat off
    workinghours sun off
    timeformat "%Y-%m-%d"
    scenario plan "Plan"
    trackingscenario plan
}

        # resources
        resource resources "Resources" {
            resource User_3 "User_3" {
    efficiency 1.0
}
            resource User_{{user1.id}} "User_{{user1.id}}" {
    efficiency 1.0
}
            resource User_{{user2.id}} "User_{{user2.id}}" {
    efficiency 1.0
}
            resource User_{{user3.id}} "User_{{user3.id}}" {
    efficiency 1.0
}
            resource User_{{user4.id}} "User_{{user4.id}}" {
    efficiency 1.0
}
            resource User_{{user5.id}} "User_{{user5.id}}" {
    efficiency 1.0
}
            resource User_{{user6.id}} "User_{{user6.id}}" {
    efficiency 1.0
}
        }

# tasks
task Project_{{proj.id}} "Project_{{proj.id}}" {
  task Task_{{task1.id}} "Task_{{task1.id}}" {
    effort 50.0h
    allocate User_{{user1.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }, User_{{user2.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }
    booking User_{{user1.id}} 2013-04-16-06:00:00 - 2013-04-16-09:00:00 { overtime 2 }
  }
  task Task_{{task2.id}} "Task_{{task2.id}}" {
    priority 800
    depends Project_{{proj.id}}.Task_{{task1.id}} {onend}
    effort 60.0h
    allocate User_{{user1.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }, User_{{user2.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }
  }
}

# reports
taskreport breakdown "{{csv_path}}"{
    formats csv
    timeformat "%Y-%m-%d-%H:%M"
    columns id, start, end
}
""")
        import stalker
        expected_tjp_content = expected_tjp_template.render(
            {
                'stalker': stalker,
                'studio': test_studio,
                'csv_path': tjp_sched.temp_file_name,
                'user1': self.test_user1,
                'user2': self.test_user2,
                'user3': self.test_user3,
                'user4': self.test_user4,
                'user5': self.test_user5,
                'user6': self.test_user6,
                'proj': self.test_proj1,
                'task1': self.test_task1,
                'task2': self.test_task2,
            }
        )

        self.maxDiff = None
        tjp_content = tjp_sched.tjp_content
        # print tjp_content
        tjp_sched._clean_up()
        # print(expected_tjp_content)
        # print('----------------')
        # print(tjp_content)
        assert tjp_content == expected_tjp_content

    def test_schedule_will_not_work_when_the_studio_attribute_is_None(self):
        """testing if a TypeError will be raised when the studio attribute is
        None
        """
        tjp_sched = TaskJugglerScheduler()
        tjp_sched.studio = None
        with pytest.raises(TypeError) as cm:
            tjp_sched.schedule()

        assert str(cm.value) == \
            'TaskJugglerScheduler.studio should be an instance of ' \
            'stalker.models.studio.Studio, not NoneType'

    def test_tasks_are_correctly_scheduled(self):
        """testing if the tasks are correctly scheduled
        """
        tjp_sched = TaskJugglerScheduler(compute_resources=True)
        from stalker import Studio
        test_studio = Studio(
            name='Test Studio',
            now=datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
        )
        test_studio.start = \
            datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
        test_studio.end = \
            datetime.datetime(2013, 4, 30, 0, 0, tzinfo=pytz.utc)
        test_studio.daily_working_hours = 9
        from stalker.db.session import DBSession
        DBSession.add(test_studio)

        tjp_sched.studio = test_studio
        tjp_sched.schedule()
        DBSession.commit()

        # check if the task and project timings are all adjusted
        assert \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc) == \
            self.test_proj1.computed_start
        assert \
            datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc) == \
            self.test_proj1.computed_end

        possible_resources = [
            self.test_user1, self.test_user2, self.test_user3, self.test_user4,
            self.test_user5
        ]
        assert \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc) == \
            self.test_task1.computed_start
        assert \
            datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc) == \
            self.test_task1.computed_end

        assert len(self.test_task1.computed_resources) == 2
        assert self.test_task1.computed_resources[0] in possible_resources
        assert self.test_task1.computed_resources[1] in possible_resources

        assert \
            datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc) == \
            self.test_task2.computed_start
        assert \
            datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc) == \
            self.test_task2.computed_end

        assert len(self.test_task2.computed_resources) == 2
        assert self.test_task2.computed_resources[0] in possible_resources
        assert self.test_task2.computed_resources[1] in possible_resources

    def test_tasks_are_correctly_scheduled_when_compute_resources_is_False(self):
        """testing if the tasks are correctly scheduled when the compute
        resources is False
        """
        tjp_sched = TaskJugglerScheduler(compute_resources=False)
        from stalker import Studio
        test_studio = Studio(
            name='Test Studio',
            now=datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
        )
        test_studio.start = \
            datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
        test_studio.end = datetime.datetime(2013, 4, 30, 0, 0, tzinfo=pytz.utc)
        test_studio.daily_working_hours = 9
        from stalker.db.session import DBSession
        DBSession.add(test_studio)

        tjp_sched.studio = test_studio
        tjp_sched.schedule()
        DBSession.commit()

        # check if the task and project timings are all adjusted
        assert \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc) == \
            self.test_proj1.computed_start
        assert \
            datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc) == \
            self.test_proj1.computed_end

        assert \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc) == \
            self.test_task1.computed_start
        assert \
            datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc) == \
            self.test_task1.computed_end
        assert len(self.test_task1.computed_resources) == 2
        assert self.test_task1.computed_resources[0] in \
            [self.test_user1, self.test_user2, self.test_user3,
             self.test_user4, self.test_user5]
        assert self.test_task1.computed_resources[1] in \
            [self.test_user1, self.test_user2, self.test_user3,
             self.test_user4, self.test_user5]

        assert \
            datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc) == \
            self.test_task2.computed_start
        assert \
            datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc) == \
            self.test_task2.computed_end
        assert len(self.test_task2.computed_resources) == 2
        assert self.test_task2.computed_resources[0] in \
            [self.test_user1, self.test_user2, self.test_user3,
             self.test_user4, self.test_user5]
        assert self.test_task2.computed_resources[1] in \
            [self.test_user1, self.test_user2, self.test_user3,
             self.test_user4, self.test_user5]

    def test_tasks_are_correctly_scheduled_when_compute_resources_is_True(self):
        """testing if the tasks are correctly scheduled when the compute
        resources is True
        """
        tjp_sched = TaskJugglerScheduler(compute_resources=True)
        from stalker import Studio
        test_studio = Studio(
            name='Test Studio',
            now=datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
        )
        test_studio.start = \
            datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
        test_studio.end = datetime.datetime(2013, 4, 30, 0, 0, tzinfo=pytz.utc)
        test_studio.daily_working_hours = 9
        from stalker.db.session import DBSession
        DBSession.add(test_studio)

        tjp_sched.studio = test_studio
        tjp_sched.schedule()
        DBSession.commit()

        possible_resources = [
            self.test_user1, self.test_user2, self.test_user3, self.test_user4,
            self.test_user5
        ]

        # check if the task and project timings are all adjusted
        assert \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc) == \
            self.test_proj1.computed_start
        assert \
            datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc) == \
            self.test_proj1.computed_end

        assert \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc) == \
            self.test_task1.computed_start
        assert \
            datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc) == \
            self.test_task1.computed_end
        assert len(self.test_task1.computed_resources) == 2
        assert self.test_task1.computed_resources[0] in possible_resources
        assert self.test_task1.computed_resources[1] in possible_resources

        assert \
            datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc) == \
            self.test_task2.computed_start
        assert \
            datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc) == \
            self.test_task2.computed_end
        assert self.test_task2.computed_resources[0] in possible_resources
        assert self.test_task2.computed_resources[1] in possible_resources

    def test_tasks_of_given_projects_are_correctly_scheduled(self):
        """testing if the tasks of given projects are correctly scheduled
        """
        # create a dummy project
        # create a dummy Project to schedule
        from stalker import Project
        dummy_project = Project(
            name='Dummy Project',
            code='DP',
            repository=self.test_repo
        )

        from stalker import Task
        dt1 = Task(
            name='Dummy Task 1',
            project=dummy_project,
            schedule_timing=4,
            schedule_unit='h',
            resources=[self.test_user1]
        )

        dt2 = Task(
            name='Dummy Task 2',
            project=dummy_project,
            schedule_timing=4,
            schedule_unit='h',
            resources=[self.test_user2]
        )
        from stalker.db.session import DBSession
        DBSession.add_all([dummy_project, dt1, dt2])
        DBSession.commit()

        tjp_sched = TaskJugglerScheduler(compute_resources=True,
                                         projects=[dummy_project])
        from stalker import Studio
        test_studio = Studio(
            name='Test Studio',
            now=datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
        )
        test_studio.start = \
            datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
        test_studio.end = datetime.datetime(2013, 4, 30, 0, 0, tzinfo=pytz.utc)
        test_studio.daily_working_hours = 9
        DBSession.add(test_studio)
        DBSession.commit()

        tjp_sched.studio = test_studio
        tjp_sched.schedule()
        DBSession.commit()

        # check if the task and project timings are all adjusted
        assert self.test_proj1.computed_start is None
        assert self.test_proj1.computed_end is None

        assert self.test_task1.computed_start is None
        assert self.test_task1.computed_end is None
        assert self.test_task1.computed_resources == \
            [self.test_user1, self.test_user2]

        assert self.test_task2.computed_start is None
        assert self.test_task2.computed_end is None
        assert self.test_task2.computed_resources == \
            [self.test_user1, self.test_user2]

        assert \
            dt1.computed_start == \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
        assert \
            dt1.computed_end == \
            datetime.datetime(2013, 4, 16, 13, 0, tzinfo=pytz.utc)

        assert \
            dt2.computed_start == \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
        assert \
            dt2.computed_end == \
            datetime.datetime(2013, 4, 16, 13, 0, tzinfo=pytz.utc)

    def test_projects_argument_is_skipped(self):
        """testing if the projects attribute will be an empty list if the
        projects argument is skipped
        """
        tjp_sched = TaskJugglerScheduler(compute_resources=True)
        assert tjp_sched.projects == []

    def test_projects_argument_is_None(self):
        """testing if the projects attribute will be an empty list if the
        projects argument is None
        """
        tjp_sched = TaskJugglerScheduler(compute_resources=True, projects=None)
        assert tjp_sched.projects == []

    def test_projects_attribute_is_set_to_None(self):
        """testing if the projects attribute will be an empty list if it is set
        to None
        """
        tjp_sched = TaskJugglerScheduler(compute_resources=True)
        tjp_sched.projects = None
        assert tjp_sched.projects == []

    def test_projects_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the projects argument
        value is not a list
        """
        with pytest.raises(TypeError) as cm:
            TaskJugglerScheduler(compute_resources=True,
                                 projects='not a list of projects')

        assert str(cm.value) == \
            'TaskJugglerScheduler.projects should be a list of ' \
            'stalker.models.project.Project instances, not str'

    def test_projects_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the projects attribute
        is set to something else than a list
        """
        tjp = TaskJugglerScheduler(compute_resources=True)
        with pytest.raises(TypeError) as cm:
            tjp.projects = 'not a list of projects'

        assert str(cm.value) == \
            'TaskJugglerScheduler.projects should be a list of ' \
            'stalker.models.project.Project instances, not str'

    def test_projects_argument_is_not_a_list_of_all_projects(self):
        """testing if a TypeError will be raised when the elements in the
        projects argument is not all Project instances
        """
        with pytest.raises(TypeError) as cm:
            TaskJugglerScheduler(compute_resources=True,
                                 projects=['not', 1, [], 'of', 'projects'])

        assert str(cm.value) == \
            'TaskJugglerScheduler.projects should be a list of ' \
            'stalker.models.project.Project instances, not str'

    def test_projects_attribute_is_not_list_of_all_projects(self):
        """testing if a TypeError will be raised when the elements in the
        projects attribute is not all Project instances
        """
        tjp = TaskJugglerScheduler(compute_resources=True)
        with pytest.raises(TypeError) as cm:
            tjp.projects = ['not', 1, [], 'of', 'projects']

        assert str(cm.value) == \
            'TaskJugglerScheduler.projects should be a list of ' \
            'stalker.models.project.Project instances, not str'

    def test_projects_argument_is_working_properly(self):
        """testing if the projects argument value is correctly passed to the
        projects attribute
        """
        from stalker import Project
        dp1 = Project(
            name='Dummy Project',
            code='DP',
            repository=self.test_repo
        )

        dp2 = Project(
            name='Dummy Project',
            code='DP',
            repository=self.test_repo
        )

        tjp = TaskJugglerScheduler(compute_resources=True,
                                   projects=[dp1, dp2])

        assert tjp.projects == [dp1, dp2]

    def test_projects_attribute_is_working_properly(self):
        """testing if the projects attribute is working properly
        """
        from stalker import Project
        dp1 = Project(
            name='Dummy Project',
            code='DP',
            repository=self.test_repo
        )

        dp2 = Project(
            name='Dummy Project',
            code='DP',
            repository=self.test_repo
        )

        tjp = TaskJugglerScheduler(compute_resources=True)
        tjp.projects = [dp1, dp2]

        assert tjp.projects == [dp1, dp2]

    def test_tjp_file_content_is_correct_2(self):
        """testing if the tjp file content is correct
        """
        tjp_sched = TaskJugglerScheduler()
        from stalker import Studio
        test_studio = Studio(
            name='Test Studio',
            timing_resolution=datetime.timedelta(minutes=30)
        )
        test_studio.daily_working_hours = 9

        test_studio.id = 564
        test_studio.start = \
            datetime.datetime(2013, 4, 16, 0, 7, tzinfo=pytz.utc)
        test_studio.end = \
            datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc)
        test_studio.now = \
            datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
        tjp_sched.studio = test_studio

        tjp_sched._create_tjp_file()
        tjp_sched._create_tjp_file_content()

        import jinja2

        expected_tjp_template = jinja2.Template(
            """# Generated By Stalker v{{stalker.__version__}}
        
project Studio_564 "Studio_564" 2013-04-16 - 2013-06-30 {
    timingresolution 30min
    now 2013-04-16-00:00
    dailyworkinghours 9
    weekstartsmonday
    workinghours mon 09:00 - 18:00
    workinghours tue 09:00 - 18:00
    workinghours wed 09:00 - 18:00
    workinghours thu 09:00 - 18:00
    workinghours fri 09:00 - 18:00
    workinghours sat off
    workinghours sun off
    timeformat "%Y-%m-%d"
    scenario plan "Plan"
    trackingscenario plan
}

        # resources
        resource resources "Resources" {
            resource User_3 "User_3" {
    efficiency 1.0
}
            resource User_{{user1.id}} "User_{{user1.id}}" {
    efficiency 1.0
}
            resource User_{{user2.id}} "User_{{user2.id}}" {
    efficiency 1.0
}
            resource User_{{user3.id}} "User_{{user3.id}}" {
    efficiency 1.0
}
            resource User_{{user4.id}} "User_{{user4.id}}" {
    efficiency 1.0
}
            resource User_{{user5.id}} "User_{{user5.id}}" {
    efficiency 1.0
}
            resource User_{{user6.id}} "User_{{user6.id}}" {
    efficiency 1.0
}
        }

# tasks
task Project_{{proj1.id}} "Project_{{proj1.id}}" {
  task Task_{{task1.id}} "Task_{{task1.id}}" {
    effort 50.0h
    allocate User_{{user1.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }, User_{{user2.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }
  }
  task Task_{{task2.id}} "Task_{{task2.id}}" {
    priority 800
    depends Project_{{proj1.id}}.Task_{{task1.id}} {onend}
    effort 60.0h
    allocate User_{{user1.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }, User_{{user2.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }
  }
}

# reports
taskreport breakdown "{{csv_path}}"{
    formats csv
    timeformat "%Y-%m-%d-%H:%M"
    columns id, start, end
}""")
        import stalker
        expected_tjp_content = expected_tjp_template.render(
            {
                'stalker': stalker,
                'studio': test_studio,
                'csv_path': tjp_sched.temp_file_name,
                'user1': self.test_user1,
                'user2': self.test_user2,
                'user3': self.test_user3,
                'user4': self.test_user4,
                'user5': self.test_user5,
                'user6': self.test_user6,
                'proj1': self.test_proj1,
                'task1': self.test_task1,
                'task2': self.test_task2,
            }
        )

        self.maxDiff = None
        tjp_content = tjp_sched.tjp_content
        # print tjp_content
        tjp_sched._clean_up()
        assert tjp_content == expected_tjp_content
