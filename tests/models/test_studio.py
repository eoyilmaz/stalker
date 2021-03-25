# -*- coding: utf-8 -*-

import pytest

from stalker.testing import UnitTestDBBase
from stalker import SchedulerBase


class DummyScheduler(SchedulerBase):
    """this is a dummy scheduler to be used in tests
    """

    def __init__(self, studio=None, callback=None):
        SchedulerBase.__init__(self, studio)
        self.callback = callback

    def schedule(self):
        """call the callback function before finishing
        """
        if self.callback:
            self.callback()


class StudioTester(UnitTestDBBase):
    """tests the stalker.models.studio.Studio class
    """

    def setUp(self):
        """setup the test
        """
        super(StudioTester, self).setUp()

        from stalker import User

        self.test_user1 = User(
            name='User 1',
            login='user1',
            email='user1@users.com',
            password='password'
        )
        from stalker.db.session import DBSession
        DBSession.add(self.test_user1)

        self.test_user2 = User(
            name='User 2',
            login='user2',
            email='user2@users.com',
            password='password'
        )
        DBSession.add(self.test_user2)

        self.test_user3 = User(
            name='User 3',
            login='user3',
            email='user3@users.com',
            password='password'
        )
        DBSession.add(self.test_user3)

        from stalker import Department
        self.test_department1 = Department(
            name='Test Department 1'
        )
        DBSession.add(self.test_department1)

        self.test_department2 = Department(
            name='Test Department 2'
        )
        DBSession.add(self.test_department2)

        from stalker import Repository
        self.test_repo = Repository(
            name='Test Repository',
            code='TR',
            windows_path='T:/',
            linux_path='/mnt/T/',
            osx_path='/Volumes/T/'
        )
        DBSession.add(self.test_repo)

        # create a couple of projects
        from stalker import Project
        self.test_project1 = Project(
            name='Test Project 1',
            code='TP1',
            repository=self.test_repo
        )
        DBSession.add(self.test_project1)

        from stalker import Project
        self.test_project2 = Project(
            name='Test Project 2',
            code='TP2',
            repository=self.test_repo
        )
        DBSession.add(self.test_project2)

        # an inactive project
        self.test_project3 = Project(
            name='Test Project 3',
            code='TP3',
            repository=self.test_repo
        )
        self.test_project3.active = False
        DBSession.save(self.test_project3)

        # create assets and shots
        from stalker import Type
        self.test_asset_type = Type(
            name='Character',
            code='Char',
            target_entity_type='Asset'
        )
        DBSession.add(self.test_asset_type)

        from stalker import Asset, Shot, Task
        self.test_asset1 = Asset(
            name='Test Asset 1',
            code='TA1',
            project=self.test_project1,
            type=self.test_asset_type
        )
        DBSession.add(self.test_asset1)

        self.test_asset2 = Asset(
            name='Test Asset 2',
            code='TA2',
            project=self.test_project2,
            type=self.test_asset_type
        )
        DBSession.add(self.test_asset2)

        # shots
        # for project 1
        self.test_shot1 = Shot(
            code='shot1',
            project=self.test_project1,
        )
        DBSession.add(self.test_shot1)

        self.test_shot2 = Shot(
            code='shot2',
            project=self.test_project1,
        )
        DBSession.add(self.test_shot2)

        # for project 2
        self.test_shot3 = Shot(
            code='shot3',
            project=self.test_project2,
        )
        DBSession.add(self.test_shot3)

        self.test_shot4 = Shot(
            code='shot4',
            project=self.test_project2,
        )
        DBSession.add(self.test_shot4)

        # for project 3
        self.test_shot5 = Shot(
            code='shot5',
            project=self.test_project3,
        )
        DBSession.add(self.test_shot5)

        #########################################################
        # tasks for projects
        self.test_task1 = Task(
            name='Project Planing',
            project=self.test_project1,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=10,
            schedule_unit='d'
        )
        DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='Project Planing',
            project=self.test_project2,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=10,
            schedule_unit='d'
        )
        DBSession.add(self.test_task2)

        self.test_task3 = Task(
            name='Project Planing',
            project=self.test_project3,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=5,
            schedule_unit='d'
        )
        DBSession.add(self.test_task3)

        # for shots

        # Shot 1
        self.test_task4 = Task(
            name='Match Move',
            parent=self.test_shot1,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=2,
            schedule_unit='d',
        )
        DBSession.add(self.test_task4)

        self.test_task5 = Task(
            name='FX',
            parent=self.test_shot1,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task4],
            schedule_timing=2,
            schedule_unit='d',
        )
        DBSession.add(self.test_task5)

        self.test_task6 = Task(
            name='Lighting',
            parent=self.test_shot1,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task4, self.test_task5],
            schedule_timing=3,
            schedule_unit='d',
        )
        DBSession.add(self.test_task6)

        self.test_task7 = Task(
            name='Comp',
            parent=self.test_shot1,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task6],
            schedule_timing=3,
            schedule_unit='d',
        )
        DBSession.add(self.test_task7)

        # Shot 2
        self.test_task8 = Task(
            name='Match Move',
            parent=self.test_shot2,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            schedule_timing=2,
            schedule_unit='d',
        )
        DBSession.add(self.test_task8)

        self.test_task9 = Task(
            name='FX',
            parent=self.test_shot2,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            depends=[self.test_task8],
            schedule_timing=2,
            schedule_unit='d',
        )
        DBSession.add(self.test_task9)

        self.test_task10 = Task(
            name='Lighting',
            parent=self.test_shot2,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task8, self.test_task9],
            schedule_timing=3,
            schedule_unit='d',
        )
        DBSession.add(self.test_task10)

        self.test_task11 = Task(
            name='Comp',
            parent=self.test_shot2,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task10],
            schedule_timing=4,
            schedule_unit='d',
        )
        DBSession.add(self.test_task11)

        # Shot 3
        self.test_task12 = Task(
            name='Match Move',
            parent=self.test_shot3,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=2,
            schedule_unit='d',
        )
        DBSession.add(self.test_task12)

        self.test_task13 = Task(
            name='FX',
            parent=self.test_shot3,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            depends=[self.test_task12],
            schedule_timing=2,
            schedule_unit='d',
        )
        DBSession.add(self.test_task13)

        self.test_task14 = Task(
            name='Lighting',
            parent=self.test_shot3,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            depends=[self.test_task12, self.test_task13],
            schedule_timing=3,
            schedule_unit='d',
        )
        DBSession.add(self.test_task14)

        self.test_task15 = Task(
            name='Comp',
            parent=self.test_shot3,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            depends=[self.test_task14],
            schedule_timing=4,
            schedule_unit='d',
        )
        DBSession.add(self.test_task15)

        # Shot 4
        self.test_task16 = Task(
            name='Match Move',
            parent=self.test_shot4,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            schedule_timing=2,
            schedule_unit='d',
        )
        DBSession.add(self.test_task16)

        self.test_task17 = Task(
            name='FX',
            parent=self.test_shot4,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task16],
            schedule_timing=2,
            schedule_unit='d',
        )
        DBSession.add(self.test_task17)

        self.test_task18 = Task(
            name='Lighting',
            parent=self.test_shot4,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task16, self.test_task17],
            schedule_timing=3,
            schedule_unit='d',
        )
        DBSession.add(self.test_task18)

        self.test_task19 = Task(
            name='Comp',
            parent=self.test_shot4,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task18],
            schedule_timing=4,
            schedule_unit='d',
        )
        DBSession.add(self.test_task19)

        # Shot 5
        self.test_task20 = Task(
            name='Match Move',
            parent=self.test_shot5,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            schedule_timing=2,
            schedule_unit='d',
        )
        DBSession.add(self.test_task20)

        self.test_task21 = Task(
            name='FX',
            parent=self.test_shot5,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            depends=[self.test_task20],
            schedule_timing=2,
            schedule_unit='d',
        )
        DBSession.add(self.test_task21)

        self.test_task22 = Task(
            name='Lighting',
            parent=self.test_shot5,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            depends=[self.test_task20, self.test_task21],
            schedule_timing=3,
            schedule_unit='d',
        )
        DBSession.add(self.test_task22)

        self.test_task23 = Task(
            name='Comp',
            parent=self.test_shot5,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            depends=[self.test_task22],
            schedule_timing=4,
            schedule_unit='d',
        )
        DBSession.add(self.test_task23)

        ####################################################
        # For Assets

        # Asset 1
        self.test_task24 = Task(
            name='Design',
            parent=self.test_asset1,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
        )
        DBSession.add(self.test_task24)

        self.test_task25 = Task(
            name='Model',
            parent=self.test_asset1,
            depends=[self.test_task24],
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=15,
            schedule_unit='d',
        )
        DBSession.add(self.test_task25)

        self.test_task26 = Task(
            name='LookDev',
            parent=self.test_asset1,
            depends=[self.test_task25],
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
        )
        DBSession.add(self.test_task26)

        self.test_task27 = Task(
            name='Rig',
            parent=self.test_asset1,
            depends=[self.test_task25],
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
        )
        DBSession.add(self.test_task27)

        # Asset 2
        self.test_task28 = Task(
            name='Design',
            parent=self.test_asset2,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
        )
        DBSession.add(self.test_task28)

        self.test_task29 = Task(
            name='Model',
            parent=self.test_asset2,
            depends=[self.test_task28],
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            schedule_timing=15,
            schedule_unit='d',
        )
        DBSession.add(self.test_task29)

        self.test_task30 = Task(
            name='LookDev',
            parent=self.test_asset2,
            depends=[self.test_task29],
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
        )
        DBSession.add(self.test_task30)

        self.test_task31 = Task(
            name='Rig',
            parent=self.test_asset2,
            depends=[self.test_task29],
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
        )
        DBSession.add(self.test_task31)

        # TODO: Add Milestones
        import datetime
        self.kwargs = dict(
            name='Studio',
            daily_working_hours=8,
            timing_resolution=datetime.timedelta(hours=1)
        )

        from stalker import Studio
        self.test_studio = Studio(**self.kwargs)
        DBSession.add(self.test_studio)
        DBSession.commit()

    def test_working_hours_argument_is_skipped(self):
        """testing if the default working hours will be used when the
        working_hours argument is skipped
        """
        self.kwargs['name'] = 'New Studio'
        try:
            self.kwargs.pop('working_hours')  # pop if there are any
        except KeyError:
            pass

        from stalker import Studio, WorkingHours
        new_studio = Studio(**self.kwargs)
        assert new_studio.working_hours == WorkingHours()

    def test_working_hours_argument_is_None(self):
        """testing if the a WorkingHour instance with default settings will be
        used if the working_hours argument is skipped
        """
        self.kwargs['name'] = 'New Studio'
        self.kwargs['working_hours'] = None
        from stalker import Studio, WorkingHours
        new_studio = Studio(**self.kwargs)
        assert new_studio.working_hours == WorkingHours()

    def test_working_hours_attribute_is_None(self):
        """testing if a WorkingHour instance will be created with the default
        values if the working_hours attribute is set to None
        """
        from stalker import WorkingHours
        self.test_studio.working_horus = None
        assert self.test_studio.working_hours == WorkingHours()

    def test_working_hours_argument_is_not_a_working_hours_instance(self):
        """testing if a TypeError will be raised if the working_hours argument
        value is not a WorkingHours instance
        """
        self.kwargs['working_hours'] = 'not a working hours instance'
        self.kwargs['name'] = 'New Studio'
        from stalker import Studio
        with pytest.raises(TypeError) as cm:
            Studio(**self.kwargs)

        assert str(cm.value) == \
            'Studio.working_hours should be a ' \
            'stalker.models.studio.WorkingHours instance, not str'

    def test_working_hours_attribute_is_not_a_working_hours_instance(self):
        """testing if a TypeError will be raised if the working_hours attribute
        is set to a value which is not a WorkingHours instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_studio.working_hours = 'not a working hours instance'

        assert str(cm.value) == \
            'Studio.working_hours should be a ' \
            'stalker.models.studio.WorkingHours instance, not str'

    def test_working_hours_argument_is_working_properly(self):
        """testing if the working_hours argument value is passed to the
        working_hours attribute without any problem
        """
        self.kwargs['name'] = 'New Studio'
        from stalker import Studio, WorkingHours
        wh = WorkingHours(
            working_hours={
                'mon': [[60, 900]]
            }
        )

        self.kwargs['working_hours'] = wh
        new_studio = Studio(**self.kwargs)
        assert new_studio.working_hours == wh

    def test_working_hours_attribute_is_working_properly(self):
        """testing if the working_hours attribute is working properly
        """
        from stalker import WorkingHours
        new_working_hours = WorkingHours(
            working_hours={
                'mon': [[60, 1200]]  # they were doing all the jobs in
                                     # Monday :))
            }
        )
        assert self.test_studio.working_hours != new_working_hours
        self.test_studio.working_hours = new_working_hours
        assert self.test_studio.working_hours == new_working_hours

    def test_tjp_id_attribute_returns_a_plausible_id(self):
        """testing if the tjp_id is returning something meaningful
        """
        self.test_studio.id = 432
        assert self.test_studio.tjp_id == 'Studio_432'

    def test_projects_attribute_is_read_only(self):
        """testing if the project attribute is a read only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_studio.projects = [self.test_project1]

        assert str(cm.value) == "can't set attribute"

    def test_projects_attribute_is_working_properly(self):
        """testing if the projects attribute is working properly
        """
        assert \
            sorted(self.test_studio.projects, key=lambda x: x.name) == \
            sorted(
                [self.test_project1, self.test_project2, self.test_project3],
                key=lambda x: x.name
            )

    def test_active_projects_attribute_is_read_only(self):
        """testing if the active_projects attribute is a read only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_studio.active_projects = [self.test_project1]

        assert str(cm.value) == "can't set attribute"

    def test_active_projects_attribute_is_working_properly(self):
        """testing if the active_projects attribute is working properly
        """
        assert \
            sorted(self.test_studio.active_projects, key=lambda x: x.name) == \
            sorted([self.test_project1, self.test_project2],
                   key=lambda x: x.name)

    def test_inactive_projects_attribute_is_read_only(self):
        """testing if the inactive_projects attribute is a read only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_studio.inactive_projects = [self.test_project1]

        assert str(cm.value) == "can't set attribute"

    def test_inactive_projects_attribute_is_working_properly(self):
        """testing if the inactive_projects attribute is working properly
        """
        assert \
            sorted(self.test_studio.inactive_projects, key=lambda x: x.name) \
            == sorted([self.test_project3], key=lambda x: x.name)

    def test_departments_attribute_is_read_only(self):
        """testing if the departments attribute is a read only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_studio.departments = [self.test_project1]

        assert str(cm.value) == "can't set attribute"

    def test_departments_attribute_is_working_properly(self):
        """testing if the departments attribute is working properly
        """
        from stalker import Department
        admins_dep = \
            Department.query.filter(Department.name == 'admins').first()
        assert admins_dep is not None
        assert \
            sorted(self.test_studio.departments, key=lambda x: x.name) == \
            sorted([self.test_department1, self.test_department2, admins_dep],
                   key=lambda x: x.name)

    def test_users_attribute_is_read_only(self):
        """testing if the users attribute is a read only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_studio.users = [self.test_project1]

        assert str(cm.value) == "can't set attribute"

    def test_users_attribute_is_working_properly(self):
        """testing if the users attribute is working properly
        """
        # don't forget the admin
        from stalker import User
        admin = User.query.filter_by(name='admin').first()
        assert admin is not None
        assert \
            sorted(self.test_studio.users, key=lambda x: x.name) == \
            sorted([admin, self.test_user1, self.test_user2, self.test_user3],
                   key=lambda x: x.name)

    def test_to_tjp_attribute_is_read_only(self):
        """testing if the to_tjp attribute is a read only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_studio.to_tjp = "some text"

        assert str(cm.value) == "can't set attribute"

    def test_now_argument_is_skipped(self):
        """testing if the now attribute will use the rounded
        datetime.datetime.now(pytz.utc) value when the now argument is skipped
        """
        try:
            self.kwargs.pop('now')
        except KeyError:
            pass

        import datetime
        import pytz
        from stalker import Studio
        new_studio = Studio(**self.kwargs)
        assert new_studio.now == \
            new_studio.round_time(datetime.datetime.now(pytz.utc))

    def test_now_argument_is_None(self):
        """testing if the now attribute will use the rounded
        datetime.datetime.now(pytz.utc) value when the now argument is None
        """
        import datetime
        import pytz
        from stalker import Studio
        self.kwargs['now'] = None
        new_studio = Studio(**self.kwargs)
        assert new_studio.now == \
            new_studio.round_time(datetime.datetime.now(pytz.utc))

    def test_now_attribute_is_None(self):
        """testing if the now attribute will be equal to the rounded value of
        datetime.datetime.now(pytz.utc) if it is set to None
        """
        import pytz
        import datetime
        self.test_studio.now = None
        assert self.test_studio.now == \
            self.test_studio.round_time(datetime.datetime.now(pytz.utc))

    def test_now_argument_is_not_a_datetime_instance(self):
        """testing if a TypeError will be raised when the now argument is not
        a datetime.datetime instance
        """
        from stalker import Studio
        self.kwargs['now'] = 'not a datetime instance'
        with pytest.raises(TypeError) as cm:
            Studio(**self.kwargs)

        assert str(cm.value) == \
            'Studio.now attribute should be an instance of ' \
            'datetime.datetime, not str'

    def test_now_attribute_is_set_to_a_value_other_than_datetime_instance(self):
        """testing if a TypeError will be raised when the now attribute is set
        to a value other than a datetime.datetime instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_studio.now = 'not a datetime instance'

        assert str(cm.value) == \
            'Studio.now attribute should be an instance of ' \
            'datetime.datetime, not str'

    def test_now_argument_is_working_properly(self):
        """testing if the now argument value is passed to the now attribute
        properly
        """
        import datetime
        import pytz
        from stalker import Studio
        self.kwargs['now'] = \
            datetime.datetime(2013, 4, 15, 21, 9, tzinfo=pytz.utc)
        expected_now = \
            datetime.datetime(2013, 4, 15, 21, 0, tzinfo=pytz.utc)
        new_studio = Studio(**self.kwargs)
        assert new_studio.now == expected_now

    def test_now_attribute_is_working_properly(self):
        """testing if the now attribute is working properly
        """
        import datetime
        import pytz
        self.test_studio.now = \
            datetime.datetime(2013, 4, 15, 21, 11, tzinfo=pytz.utc)
        expected_now = \
            datetime.datetime(2013, 4, 15, 21, 0, tzinfo=pytz.utc)
        assert self.test_studio.now == expected_now

    def test_now_attribute_is_working_properly_case2(self):
        """testing if the now attribute is working properly
        """
        import datetime
        import pytz
        from stalker import Studio
        self.test_studio._now = None
        expected_now = \
            Studio.round_time(datetime.datetime.now(pytz.utc))
        assert self.test_studio.now == expected_now

    def test_to_tjp_attribute_is_working_properly(self):
        """testing if the to_tjp attribute is working properly
        """
        import datetime
        import pytz
        self.test_studio.start = \
            datetime.datetime(2013, 4, 15, 17, 40, tzinfo=pytz.utc)
        self.test_studio.end = \
            datetime.datetime(2013, 6, 30, 17, 40, tzinfo=pytz.utc)
        self.test_studio.working_hours[0] = [[540, 1080]]
        self.test_studio.working_hours[1] = [[540, 1080]]
        self.test_studio.working_hours[2] = [[540, 1080]]
        self.test_studio.working_hours[3] = [[540, 1080]]
        self.test_studio.working_hours[4] = [[540, 1080]]
        self.test_studio.working_hours[5] = [[540, 720]]
        self.test_studio.working_hours[6] = []

        from jinja2 import Template

        expected_tjp_template = Template("""
project Studio_{{studio.id}} "Studio_{{studio.id}}" 2013-04-15 - 2013-06-30 {
    timingresolution 60min
    now {{ studio.now.strftime('%Y-%m-%d-%H:%M') }}
    dailyworkinghours 8
    weekstartsmonday
    workinghours mon 09:00 - 18:00
    workinghours tue 09:00 - 18:00
    workinghours wed 09:00 - 18:00
    workinghours thu 09:00 - 18:00
    workinghours fri 09:00 - 18:00
    workinghours sat 09:00 - 12:00
    workinghours sun off
    timeformat "%Y-%m-%d"
    scenario plan "Plan"
    trackingscenario plan
}
""")

        expected_tjp = expected_tjp_template.render({
            'studio': self.test_studio
        })
        # print('-----------------------------------')
        # print(expected_tjp)
        # print('-----------------------------------')
        # print(self.test_studio.to_tjp)
        # print('-----------------------------------')
        assert self.test_studio.to_tjp == expected_tjp

    def test_scheduler_attribute_can_be_set_to_None(self):
        """testing if the scheduler attribute can be set to None
        """
        self.test_studio.scheduler = None

    def test_scheduler_attribute_accepts_Scheduler_instances_only(self):
        """testing if a TypeError will be raised when the scheduler attribute
        is set to a value which is not a scheduler instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_studio.scheduler = 'not a Scheduler instance'

        assert str(cm.value) == \
            'Studio.scheduler should be an instance of ' \
            'stalker.models.scheduler.SchedulerBase, not str'

    def test_scheduler_attribute_is_working_properly(self):
        """testing if the scheduler attribute is working properly
        """
        from stalker import TaskJugglerScheduler
        tj_s = TaskJugglerScheduler()
        self.test_studio.scheduler = tj_s
        assert self.test_studio.scheduler == tj_s

    def test_schedule_will_not_work_without_a_scheduler(self):
        """testing if a RuntimeError will be raised when the scheduler
        attribute is not set to a Scheduler instance and schedule is called
        """
        self.test_studio.scheduler = None
        with pytest.raises(RuntimeError) as cm:
            self.test_studio.schedule()

        assert str(cm.value) == \
            'There is no scheduler for this Studio, please assign a ' \
            'scheduler to the Studio.scheduler attribute, before calling ' \
            'Studio.schedule()'

    def test_schedule_will_schedule_the_tasks_with_the_given_scheduler(self):
        """testing if the schedule method will schedule the tasks with the
        given scheduler
        """
        import datetime
        import pytz
        from stalker import TaskJugglerScheduler
        tj_scheduler = TaskJugglerScheduler(compute_resources=True)
        self.test_studio.now = \
            datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
        self.test_studio.start = \
            datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
        self.test_studio.end = \
            datetime.datetime(2013, 7, 30, 0, 0, tzinfo=pytz.utc)

        # just to be sure that it is not creating any issue on schedule
        self.test_task25.task_depends_to[0].dependency_target = 'onstart'
        self.test_task25.resources = [self.test_user2]

        self.test_studio.scheduler = tj_scheduler
        self.test_studio.schedule()
        from stalker.db.session import DBSession
        DBSession.commit()

        # now check the timings of the tasks are all adjusted

        # Projects
        # print("%s:self.test_project" % self.test_project1.id)
        # print("%s:self.test_project2" % self.test_project2.id)
        # print("%s:self.test_project3" % self.test_project3.id)

        # print("%s:self.test_asset1" % self.test_asset1.id)
        # print("%s:self.test_asset2" % self.test_asset2.id)

        # print("%s:self.test_shot1.id" % self.test_shot1.id)
        # print("%s:self.test_shot2.id" % self.test_shot2.id)
        # print("%s:self.test_shot3.id" % self.test_shot3.id)
        # print("%s:self.test_shot4.id" % self.test_shot4.id)
        # print("%s:self.test_shot5.id" % self.test_shot5.id)

        # print("%s:self.test_task1.id" % self.test_task1.id)
        # print("%s:self.test_task2.id" % self.test_task2.id)
        # print("%s:self.test_task3.id" % self.test_task3.id)
        # print("%s:self.test_task4.id" % self.test_task4.id)
        # print("%s:self.test_task5.id" % self.test_task5.id)
        # print("%s:self.test_task6.id" % self.test_task6.id)
        # print("%s:self.test_task7.id" % self.test_task7.id)
        # print("%s:self.test_task8.id" % self.test_task8.id)
        # print("%s:self.test_task9.id" % self.test_task9.id)

        # print("%s:self.test_task10.id" % self.test_task10.id)
        # print("%s:self.test_task11.id" % self.test_task11.id)
        # print("%s:self.test_task12.id" % self.test_task12.id)
        # print("%s:self.test_task13.id" % self.test_task13.id)
        # print("%s:self.test_task14.id" % self.test_task14.id)
        # print("%s:self.test_task15.id" % self.test_task15.id)
        # print("%s:self.test_task16.id" % self.test_task16.id)
        # print("%s:self.test_task17.id" % self.test_task17.id)
        # print("%s:self.test_task18.id" % self.test_task18.id)
        # print("%s:self.test_task19.id" % self.test_task19.id)

        # print("%s:self.test_task20.id" % self.test_task20.id)
        # print("%s:self.test_task21.id" % self.test_task21.id)
        # print("%s:self.test_task22.id" % self.test_task22.id)
        # print("%s:self.test_task23.id" % self.test_task23.id)
        # print("%s:self.test_task24.id" % self.test_task24.id)
        # print("%s:self.test_task25.id" % self.test_task25.id)
        # print("%s:self.test_task26.id" % self.test_task26.id)
        # print("%s:self.test_task27.id" % self.test_task27.id)
        # print("%s:self.test_task28.id" % self.test_task28.id)
        # print("%s:self.test_task29.id" % self.test_task29.id)
        # print("%s:self.test_task30.id" % self.test_task30.id)
        # print("%s:self.test_task31.id" % self.test_task31.id)


        # print('self.test_project1.computed_start: %s' % self.test_project1.computed_start)
        # print('self.test_project1.computed_end: %s' % self.test_project1.computed_end)
        # print('self.test_asset1.computed_start: %s' % self.test_asset1.computed_start)
        # print('self.test_asset1.computed_end: %s' % self.test_asset1.computed_end)
        # print('self.test_asset1.computed_resources: %s' % self.test_asset1.computed_resources)
        # print('self.test_task24.computed_start: %s' % self.test_task24.computed_start)
        # print('self.test_task24.computed_end: %s' % self.test_task24.computed_end)
        # print('self.test_task24.computed_resources: %s' % self.test_task24.computed_resources)
        # print('self.test_task25.computed_start: %s' % self.test_task25.computed_start)
        # print('self.test_task25.computed_end: %s' % self.test_task25.computed_end)
        # print('self.test_task25.computed_resources: %s' % self.test_task25.computed_resources)
        # print('self.test_task26.computed_start: %s' % self.test_task26.computed_start)
        # print('self.test_task26.computed_end: %s' % self.test_task26.computed_end)
        # print('self.test_task26.computed_resources: %s' % self.test_task26.computed_resources)
        # print('self.test_task27.computed_start: %s' % self.test_task27.computed_start)
        # print('self.test_task27.computed_end: %s' % self.test_task27.computed_end)
        # print('self.test_task27.computed_resources: %s' % self.test_task27.computed_resources)
        # print('self.test_shot2.computed_start: %s' % self.test_shot2.computed_start)
        # print('self.test_shot2.computed_end: %s' % self.test_shot2.computed_end)
        # print('self.test_shot2.computed_resources: %s' % self.test_shot2.computed_resources)
        # print('self.test_task8.computed_start: %s' % self.test_task8.computed_start)
        # print('self.test_task8.computed_end: %s' % self.test_task8.computed_end)
        # print('self.test_task8.computed_resources: %s' % self.test_task8.computed_resources)
        # print('self.test_task9.computed_start: %s' % self.test_task9.computed_start)
        # print('self.test_task9.computed_end: %s' % self.test_task9.computed_end)
        # print('self.test_task9.computed_resources: %s' % self.test_task9.computed_resources)
        # print('self.test_task10.computed_start: %s' % self.test_task10.computed_start)
        # print('self.test_task10.computed_end: %s' % self.test_task10.computed_end)
        # print('self.test_task10.computed_resources: %s' % self.test_task10.computed_resources)
        # print('self.test_task11.computed_start: %s' % self.test_task11.computed_start)
        # print('self.test_task11.computed_end: %s' % self.test_task11.computed_end)
        # print('self.test_task11.computed_resources: %s' % self.test_task11.computed_resources)
        # print('self.test_shot1.computed_start: %s' % self.test_shot1.computed_start)
        # print('self.test_shot1.computed_end: %s' % self.test_shot1.computed_end)
        # print('self.test_shot1.computed_resources: %s' % self.test_shot1.computed_resources)
        # print('self.test_task4.computed_start: %s' % self.test_task4.computed_start)
        # print('self.test_task4.computed_end: %s' % self.test_task4.computed_end)
        # print('self.test_task4.computed_resources: %s' % self.test_task4.computed_resources)
        # print('self.test_task5.computed_start: %s' % self.test_task5.computed_start)
        # print('self.test_task5.computed_end: %s' % self.test_task5.computed_end)
        # print('self.test_task5.computed_resources: %s' % self.test_task5.computed_resources)
        # print('self.test_task6.computed_start: %s' % self.test_task6.computed_start)
        # print('self.test_task6.computed_end: %s' % self.test_task6.computed_end)
        # print('self.test_task6.computed_resources: %s' % self.test_task6.computed_resources)
        # print('self.test_task7.computed_start: %s' % self.test_task7.computed_start)
        # print('self.test_task7.computed_end: %s' % self.test_task7.computed_end)
        # print('self.test_task7.computed_resources: %s' % self.test_task7.computed_resources)
        # print('self.test_task1.computed_start: %s' % self.test_task1.computed_start)
        # print('self.test_task1.computed_end: %s' % self.test_task1.computed_end)
        # print('self.test_task1.computed_resources: %s' % self.test_task1.computed_resources)
        # print('self.test_asset2.computed_start: %s' % self.test_asset2.computed_start)
        # print('self.test_asset2.computed_end: %s' % self.test_asset2.computed_end)
        # print('self.test_asset2.computed_resources: %s' % self.test_asset2.computed_resources)
        # print('self.test_task28.computed_start: %s' % self.test_task28.computed_start)
        # print('self.test_task28.computed_end: %s' % self.test_task28.computed_end)
        # print('self.test_task28.computed_resources: %s' % self.test_task28.computed_resources)
        # print('self.test_task29.computed_start: %s' % self.test_task29.computed_start)
        # print('self.test_task29.computed_end: %s' % self.test_task29.computed_end)
        # print('self.test_task29.computed_resources: %s' % self.test_task29.computed_resources)
        # print('self.test_task30.computed_start: %s' % self.test_task30.computed_start)
        # print('self.test_task30.computed_end: %s' % self.test_task30.computed_end)
        # print('self.test_task30.computed_resources: %s' % self.test_task30.computed_resources)
        # print('self.test_task31.computed_start: %s' % self.test_task31.computed_start)
        # print('self.test_task31.computed_end: %s' % self.test_task31.computed_end)
        # print('self.test_task31.computed_resources: %s' % self.test_task31.computed_resources)
        # print('self.test_shot3.computed_start: %s' % self.test_shot3.computed_start)
        # print('self.test_shot3.computed_end: %s' % self.test_shot3.computed_end)
        # print('self.test_shot3.computed_resources: %s' % self.test_shot3.computed_resources)
        # print('self.test_task12.computed_start: %s' % self.test_task12.computed_start)
        # print('self.test_task12.computed_end: %s' % self.test_task12.computed_end)
        # print('self.test_task12.computed_resources: %s' % self.test_task12.computed_resources)
        # print('self.test_task13.computed_start: %s' % self.test_task13.computed_start)
        # print('self.test_task13.computed_end: %s' % self.test_task13.computed_end)
        # print('self.test_task13.computed_resources: %s' % self.test_task13.computed_resources)
        # print('self.test_task14.computed_start: %s' % self.test_task14.computed_start)
        # print('self.test_task14.computed_end: %s' % self.test_task14.computed_end)
        # print('self.test_task14.computed_resources: %s' % self.test_task14.computed_resources)
        # print('self.test_task15.computed_start: %s' % self.test_task15.computed_start)
        # print('self.test_task15.computed_end: %s' % self.test_task15.computed_end)
        # print('self.test_task15.computed_resources: %s' % self.test_task15.computed_resources)
        # print('self.test_shot4.computed_start: %s' % self.test_shot4.computed_start)
        # print('self.test_shot4.computed_end: %s' % self.test_shot4.computed_end)
        # print('self.test_shot4.computed_resources: %s' % self.test_shot4.computed_resources)
        # print('self.test_task16.computed_start: %s' % self.test_task16.computed_start)
        # print('self.test_task16.computed_end: %s' % self.test_task16.computed_end)
        # print('self.test_task16.computed_resources: %s' % self.test_task16.computed_resources)
        # print('self.test_task17.computed_start: %s' % self.test_task17.computed_start)
        # print('self.test_task17.computed_end: %s' % self.test_task17.computed_end)
        # print('self.test_task17.computed_resources: %s' % self.test_task17.computed_resources)
        # print('self.test_task18.computed_start: %s' % self.test_task18.computed_start)
        # print('self.test_task18.computed_end: %s' % self.test_task18.computed_end)
        # print('self.test_task18.computed_resources: %s' % self.test_task18.computed_resources)
        # print('self.test_task19.computed_start: %s' % self.test_task19.computed_start)
        # print('self.test_task19.computed_end: %s' % self.test_task19.computed_end)
        # print('self.test_task19.computed_resources: %s' % self.test_task19.computed_resources)
        # print('self.test_task2.computed_start: %s' % self.test_task2.computed_start)
        # print('self.test_task2.computed_end: %s' % self.test_task2.computed_end)
        # print('self.test_task2.computed_resources: %s' % self.test_task2.computed_resources)

        # self.test_project
        assert self.test_project1.computed_start == \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)

        assert self.test_project1.computed_end == \
            datetime.datetime(2013, 6, 24, 16, 0, tzinfo=pytz.utc)

        # self.test_asset1
        assert self.test_asset1.computed_start == \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)

        assert self.test_asset1.computed_end == \
            datetime.datetime(2013, 5, 17, 18, 0, tzinfo=pytz.utc)

        assert self.test_asset1.computed_resources == []

        # self.test_task24
        assert self.test_task24.computed_start == \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)

        assert self.test_task24.computed_end == \
            datetime.datetime(2013, 4, 26, 17, 0, tzinfo=pytz.utc)

        possible_resources = \
            [self.test_user1, self.test_user2, self.test_user3]
        assert len(self.test_task24.computed_resources) == 1
        assert self.test_task24.computed_resources[0] in possible_resources

        # self.test_task25
        assert self.test_task25.computed_start == \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)

        assert self.test_task25.computed_end == \
            datetime.datetime(2013, 5, 3, 12, 0, tzinfo=pytz.utc)

        assert len(self.test_task25.computed_resources) == 1
        assert self.test_task25.computed_resources[0] in possible_resources

        # self.test_task26
        assert self.test_task26.computed_start == \
            datetime.datetime(2013, 5, 6, 11, 0, tzinfo=pytz.utc)

        assert self.test_task26.computed_end == \
            datetime.datetime(2013, 5, 17, 10, 0, tzinfo=pytz.utc)

        assert len(self.test_task26.computed_resources) == 1
        assert self.test_task26.computed_resources[0] in possible_resources

        # self.test_task27
        assert self.test_task27.computed_start == \
            datetime.datetime(2013, 5, 7, 10, 0, tzinfo=pytz.utc)

        assert self.test_task27.computed_end == \
            datetime.datetime(2013, 5, 17, 18, 0, tzinfo=pytz.utc)

        assert len(self.test_task27.computed_resources) == 1
        assert self.test_task27.computed_resources[0] in possible_resources

        # self.test_shot2
        assert self.test_shot2.computed_start == \
            datetime.datetime(2013, 4, 26, 17, 0, tzinfo=pytz.utc)

        assert self.test_shot2.computed_end == \
            datetime.datetime(2013, 6, 20, 10, 0, tzinfo=pytz.utc)

        assert self.test_shot2.computed_resources == []

        # self.test_task8
        assert self.test_task8.computed_start == \
            datetime.datetime(2013, 4, 26, 17, 0, tzinfo=pytz.utc)

        assert self.test_task8.computed_end == \
            datetime.datetime(2013, 4, 30, 15, 0, tzinfo=pytz.utc)

        assert len(self.test_task8.computed_resources) == 1
        assert self.test_task8.computed_resources[0] in possible_resources

        # self.test_task9
        assert self.test_task9.computed_start == \
            datetime.datetime(2013, 5, 30, 17, 0, tzinfo=pytz.utc)

        assert self.test_task9.computed_end == \
            datetime.datetime(2013, 6, 3, 15, 0, tzinfo=pytz.utc)

        assert len(self.test_task9.computed_resources) == 1
        assert self.test_task9.computed_resources[0] in possible_resources

        # self.test_task10
        assert self.test_task10.computed_start == \
            datetime.datetime(2013, 6, 5, 13, 0, tzinfo=pytz.utc)

        assert self.test_task10.computed_end == \
            datetime.datetime(2013, 6, 10, 10, 0, tzinfo=pytz.utc)

        assert len(self.test_task10.computed_resources) == 1
        assert self.test_task10.computed_resources[0] in possible_resources

        # self.test_task11
        assert self.test_task11.computed_start == \
            datetime.datetime(2013, 6, 14, 14, 0, tzinfo=pytz.utc)

        assert self.test_task11.computed_end == \
            datetime.datetime(2013, 6, 20, 10, 0, tzinfo=pytz.utc)

        assert len(self.test_task11.computed_resources) == 1
        assert self.test_task11.computed_resources[0] in possible_resources

        # self.test_shot1
        assert self.test_shot1.computed_start == \
            datetime.datetime(2013, 5, 16, 11, 0, tzinfo=pytz.utc)

        assert self.test_shot1.computed_end == \
            datetime.datetime(2013, 6, 24, 16, 0, tzinfo=pytz.utc)

        assert self.test_shot1.computed_resources == []

        # self.test_task4
        assert self.test_task4.computed_start == \
            datetime.datetime(2013, 5, 16, 11, 0, tzinfo=pytz.utc)

        assert self.test_task4.computed_end == \
            datetime.datetime(2013, 5, 17, 18, 0, tzinfo=pytz.utc)

        assert len(self.test_task4.computed_resources) == 1
        assert self.test_task4.computed_resources[0] in possible_resources

        # self.test_task5
        assert self.test_task5.computed_start == \
            datetime.datetime(2013, 6, 5, 13, 0, tzinfo=pytz.utc)

        assert self.test_task5.computed_end == \
            datetime.datetime(2013, 6, 7, 11, 0, tzinfo=pytz.utc)

        assert len(self.test_task5.computed_resources) == 1
        assert self.test_task5.computed_resources[0] in possible_resources

        # self.test_task6
        assert self.test_task6.computed_start == \
            datetime.datetime(2013, 6, 11, 17, 0, tzinfo=pytz.utc)

        assert self.test_task6.computed_end == \
            datetime.datetime(2013, 6, 14, 14, 0, tzinfo=pytz.utc)

        assert len(self.test_task6.computed_resources) == 1
        assert self.test_task6.computed_resources[0] in possible_resources

        # self.test_task7
        assert self.test_task7.computed_start == \
            datetime.datetime(2013, 6, 20, 10, 0, tzinfo=pytz.utc)

        assert self.test_task7.computed_end == \
            datetime.datetime(2013, 6, 24, 16, 0, tzinfo=pytz.utc)

        assert len(self.test_task7.computed_resources) == 1
        assert self.test_task7.computed_resources[0] in possible_resources

        # self.test_task1
        assert self.test_task1.computed_start == \
            datetime.datetime(2013, 5, 17, 10, 0, tzinfo=pytz.utc)

        assert self.test_task1.computed_end == \
            datetime.datetime(2013, 5, 29, 18, 0, tzinfo=pytz.utc)

        assert len(self.test_task1.computed_resources) == 1
        assert self.test_task1.computed_resources[0] in possible_resources

        # self.test_project2
        # assert self.test_project2.computed_start == \
        #     datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
        #
        # assert self.test_project2.computed_end == \
        #     datetime.datetime(2013, 6, 18, 12, 0, tzinfo=pytz.utc)
        #
        # assert self.test_project2.computed_resources == []

        # self.test_asset2
        assert self.test_asset2.computed_start == \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)

        assert self.test_asset2.computed_end == \
            datetime.datetime(2013, 5, 30, 17, 0, tzinfo=pytz.utc)

        assert self.test_asset2.computed_resources == []

        # self.test_task28
        assert self.test_task28.computed_start == \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)

        assert self.test_task28.computed_end == \
            datetime.datetime(2013, 4, 26, 17, 0, tzinfo=pytz.utc)

        assert len(self.test_task28.computed_resources) == 1
        assert self.test_task28.computed_resources[0] in possible_resources

        # self.test_task29
        assert self.test_task29.computed_start == \
            datetime.datetime(2013, 4, 26, 17, 0, tzinfo=pytz.utc)

        assert self.test_task29.computed_end == \
            datetime.datetime(2013, 5, 16, 11, 0, tzinfo=pytz.utc)

        assert len(self.test_task29.computed_resources) == 1
        assert self.test_task29.computed_resources[0] in possible_resources

        # self.test_task30
        assert self.test_task30.computed_start == \
            datetime.datetime(2013, 5, 20, 9, 0, tzinfo=pytz.utc)

        assert self.test_task30.computed_end == \
            datetime.datetime(2013, 5, 30, 17, 0, tzinfo=pytz.utc)

        assert len(self.test_task30.computed_resources) == 1
        assert self.test_task30.computed_resources[0] in possible_resources

        # self.test_task31
        assert self.test_task31.computed_start == \
            datetime.datetime(2013, 5, 20, 9, 0, tzinfo=pytz.utc)

        assert self.test_task31.computed_end == \
            datetime.datetime(2013, 5, 30, 17, 0, tzinfo=pytz.utc)

        assert len(self.test_task31.computed_resources) == 1
        assert self.test_task31.computed_resources[0] in possible_resources

        # self.test_shot3
        assert self.test_shot3.computed_start == \
            datetime.datetime(2013, 4, 30, 15, 0, tzinfo=pytz.utc)

        assert self.test_shot3.computed_end == \
            datetime.datetime(2013, 6, 20, 10, 0, tzinfo=pytz.utc)

        assert self.test_shot3.computed_resources == []

        # self.test_task12
        assert self.test_task12.computed_start == \
            datetime.datetime(2013, 4, 30, 15, 0, tzinfo=pytz.utc)

        assert self.test_task12.computed_end == \
            datetime.datetime(2013, 5, 2, 13, 0, tzinfo=pytz.utc)

        assert len(self.test_task12.computed_resources) == 1
        assert self.test_task12.computed_resources[0] in possible_resources

        # self.test_task13
        assert self.test_task13.computed_start == \
            datetime.datetime(2013, 5, 30, 17, 0, tzinfo=pytz.utc)

        assert self.test_task13.computed_end == \
            datetime.datetime(2013, 6, 3, 15, 0, tzinfo=pytz.utc)

        assert len(self.test_task13.computed_resources) == 1
        assert self.test_task13.computed_resources[0] in possible_resources

        # self.test_task14
        assert self.test_task14.computed_start == \
            datetime.datetime(2013, 6, 7, 11, 0, tzinfo=pytz.utc)

        assert self.test_task14.computed_end == \
            datetime.datetime(2013, 6, 11, 17, 0, tzinfo=pytz.utc)

        assert len(self.test_task14.computed_resources) == 1
        assert self.test_task14.computed_resources[0] in possible_resources

        # self.test_task15
        assert self.test_task15.computed_start == \
            datetime.datetime(2013, 6, 14, 14, 0, tzinfo=pytz.utc)

        assert self.test_task15.computed_end == \
            datetime.datetime(2013, 6, 20, 10, 0, tzinfo=pytz.utc)

        assert len(self.test_task15.computed_resources) == 1
        assert self.test_task15.computed_resources[0] in possible_resources

        # self.test_shot4
        assert self.test_shot4.computed_start == \
            datetime.datetime(2013, 5, 2, 13, 0, tzinfo=pytz.utc)

        assert self.test_shot4.computed_end == \
            datetime.datetime(2013, 6, 24, 16, 0, tzinfo=pytz.utc)

        assert self.test_shot4.computed_resources == []

        # self.test_task16
        assert self.test_task16.computed_start == \
            datetime.datetime(2013, 5, 2, 13, 0, tzinfo=pytz.utc)

        assert self.test_task16.computed_end == \
            datetime.datetime(2013, 5, 6, 11, 0, tzinfo=pytz.utc)

        assert len(self.test_task16.computed_resources) == 1
        assert self.test_task16.computed_resources[0] in possible_resources

        # self.test_task17
        assert self.test_task17.computed_start == \
            datetime.datetime(2013, 6, 3, 15, 0, tzinfo=pytz.utc)

        assert self.test_task17.computed_end == \
            datetime.datetime(2013, 6, 5, 13, 0, tzinfo=pytz.utc)

        assert len(self.test_task17.computed_resources) == 1
        assert self.test_task17.computed_resources[0] in possible_resources

        # self.test_task18
        assert self.test_task18.computed_start == \
            datetime.datetime(2013, 6, 10, 10, 0, tzinfo=pytz.utc)

        assert self.test_task18.computed_end == \
            datetime.datetime(2013, 6, 12, 16, 0, tzinfo=pytz.utc)

        assert len(self.test_task18.computed_resources) == 1
        assert self.test_task18.computed_resources[0] in possible_resources

        # self.test_task19
        assert self.test_task19.computed_start == \
            datetime.datetime(2013, 6, 19, 11, 0, tzinfo=pytz.utc)

        assert self.test_task19.computed_end == \
            datetime.datetime(2013, 6, 24, 16, 0, tzinfo=pytz.utc)

        assert len(self.test_task19.computed_resources) == 1
        assert self.test_task19.computed_resources[0] in possible_resources

        # self.test_task2
        assert self.test_task2.computed_start == \
            datetime.datetime(2013, 5, 30, 9, 0, tzinfo=pytz.utc)

        assert self.test_task2.computed_end == \
            datetime.datetime(2013, 6, 11, 17, 0, tzinfo=pytz.utc)

        assert len(self.test_task2.computed_resources) == 1
        assert self.test_task2.computed_resources[0] in possible_resources

    def test_schedule_will_schedule_only_the_tasks_of_the_given_projects_with_the_given_scheduler(self):
        """testing if the schedule method will schedule the tasks of the given
        projects with the given scheduler
        """
        from stalker import Project, Task, TaskJugglerScheduler
        # create a dummy Project to schedule
        dummy_project = Project(
            name='Dummy Project',
            code='DP',
            repository=self.test_repo
        )

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

        tj_scheduler = TaskJugglerScheduler(
            compute_resources=True,
            projects=[dummy_project]
        )

        import datetime
        import pytz
        self.test_studio.now = \
            datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
        self.test_studio.start = \
            datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
        self.test_studio.end = \
            datetime.datetime(2013, 7, 30, 0, 0, tzinfo=pytz.utc)

        self.test_studio.scheduler = tj_scheduler
        self.test_studio.schedule()
        DBSession.commit()

        # now check the timings of the tasks are all adjusted
        assert dt1.computed_start == \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)

        assert dt1.computed_end == \
            datetime.datetime(2013, 4, 16, 13, 0, tzinfo=pytz.utc)

        assert dt2.computed_start == \
            datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)

        assert dt2.computed_end == \
            datetime.datetime(2013, 4, 16, 13, 0, tzinfo=pytz.utc)

        # self.test_project
        assert self.test_project1.computed_start is None
        assert self.test_project1.computed_end is None

        # self.test_asset1
        assert self.test_asset1.computed_start is None
        assert self.test_asset1.computed_end is None

        assert self.test_asset1.computed_resources == \
            self.test_asset1.resources

        # self.test_task24
        assert self.test_task24.computed_start is None
        assert self.test_task24.computed_end is None

        assert self.test_task24.computed_resources == \
            self.test_task24.resources

        # self.test_task25
        assert self.test_task25.computed_start is None
        assert self.test_task25.computed_end is None

        assert self.test_task25.computed_resources == \
            self.test_task25.resources

        # self.test_task26
        assert self.test_task26.computed_start is None
        assert self.test_task26.computed_end is None

        assert self.test_task26.computed_resources == \
            self.test_task26.resources

        # self.test_task27
        assert self.test_task27.computed_start is None
        assert self.test_task27.computed_end is None

        assert self.test_task27.computed_resources == \
            self.test_task27.resources

        # self.test_shot2
        assert self.test_shot2.computed_start is None
        assert self.test_shot2.computed_end is None

        assert self.test_shot2.computed_resources == \
            self.test_shot2.resources

        # self.test_task8
        assert self.test_task8.computed_start is None
        assert self.test_task8.computed_end is None

        assert self.test_task8.computed_resources == self.test_task8.resources

        # self.test_task9
        assert self.test_task9.computed_start is None
        assert self.test_task9.computed_end is None

        assert self.test_task9.computed_resources == self.test_task9.resources

        # self.test_task10
        assert self.test_task10.computed_start is None
        assert self.test_task10.computed_end is None

        assert self.test_task10.computed_resources == \
            self.test_task10.resources

        # self.test_task11
        assert self.test_task11.computed_start is None
        assert self.test_task11.computed_end is None

        assert self.test_task11.computed_resources == \
            self.test_task11.resources

        # self.test_shot1
        assert self.test_shot1.computed_start is None
        assert self.test_shot1.computed_end is None

        assert self.test_shot1.computed_resources == self.test_shot1.resources

        # self.test_task4
        assert self.test_task4.computed_start is None
        assert self.test_task4.computed_end is None

        assert self.test_task4.computed_resources == self.test_task4.resources

        # self.test_task5
        assert self.test_task5.computed_start is None
        assert self.test_task5.computed_end is None

        assert self.test_task5.computed_resources == self.test_task5.resources

        # self.test_task6
        assert self.test_task6.computed_start is None
        assert self.test_task6.computed_end is None

        assert self.test_task6.computed_resources == self.test_task6.resources

        # self.test_task7
        assert self.test_task7.computed_start is None
        assert self.test_task7.computed_end is None

        assert self.test_task7.computed_resources == self.test_task7.resources

        # self.test_task1
        assert self.test_task1.computed_start is None
        assert self.test_task1.computed_end is None

        assert self.test_task1.computed_resources == self.test_task1.resources

        # self.test_asset2
        assert self.test_asset2.computed_start is None
        assert self.test_asset2.computed_end is None

        assert self.test_asset2.computed_resources == \
            self.test_asset2.resources

        # self.test_task28
        assert self.test_task28.computed_start is None
        assert self.test_task28.computed_end is None

        assert self.test_task28.computed_resources == \
            self.test_task28.resources

        # self.test_task29
        assert self.test_task29.computed_start is None
        assert self.test_task29.computed_end is None

        assert self.test_task29.computed_resources == \
            self.test_task29.resources

        # self.test_task30
        assert self.test_task30.computed_start is None
        assert self.test_task30.computed_end is None

        assert self.test_task30.computed_resources == \
            self.test_task30.resources

        # self.test_task31
        assert self.test_task31.computed_start is None
        assert self.test_task31.computed_end is None

        assert self.test_task31.computed_resources == \
            self.test_task31.resources

        # self.test_shot3
        assert self.test_shot3.computed_start is None
        assert self.test_shot3.computed_end is None

        assert self.test_shot3.computed_resources == \
            self.test_shot3.resources

        # self.test_task12
        assert self.test_task12.computed_start is None
        assert self.test_task12.computed_end is None

        assert self.test_task12.computed_resources == \
            self.test_task12.resources

        # self.test_task13
        assert self.test_task13.computed_start is None
        assert self.test_task13.computed_end is None

        assert self.test_task13.computed_resources == \
            self.test_task13.resources

        # self.test_task14
        assert self.test_task14.computed_start is None
        assert self.test_task14.computed_end is None

        assert self.test_task14.computed_resources == \
            self.test_task14.resources

        # self.test_task15
        assert self.test_task15.computed_start is None
        assert self.test_task15.computed_end is None

        assert self.test_task15.computed_resources == \
            self.test_task15.resources

        # self.test_shot4
        assert self.test_shot4.computed_start is None
        assert self.test_shot4.computed_end is None

        assert self.test_shot4.computed_resources == self.test_shot4.resources

        # self.test_task16
        assert self.test_task16.computed_start is None
        assert self.test_task16.computed_end is None

        assert self.test_task16.computed_resources == \
            self.test_task16.resources

        # self.test_task17
        assert self.test_task17.computed_start is None
        assert self.test_task17.computed_end is None

        assert self.test_task17.computed_resources == \
            self.test_task17.resources

        # self.test_task18
        assert self.test_task18.computed_start is None
        assert self.test_task18.computed_end is None

        assert self.test_task18.computed_resources == \
            self.test_task18.resources

        # self.test_task19
        assert self.test_task19.computed_start is None
        assert self.test_task19.computed_end is None

        assert self.test_task19.computed_resources == \
            self.test_task19.resources

        # self.test_task2
        assert self.test_task2.computed_start is None
        assert self.test_task2.computed_end is None

        assert self.test_task2.computed_resources == \
            self.test_task2.resources

    def test_is_scheduling_will_be_False_after_scheduling_is_done(self):
        """testing if the is_scheduling attribute will be back to False when
        the scheduling is finished
        """
        import datetime
        import pytz
        # use a dummy scheduler
        self.test_studio.now = \
            datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
        self.test_studio.start = \
            datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
        self.test_studio.end = \
            datetime.datetime(2013, 7, 30, 0, 0, tzinfo=pytz.utc)

        def callback():
            assert self.test_studio.is_scheduling is True

        dummy_scheduler = DummyScheduler(callback=callback)

        self.test_studio.scheduler = dummy_scheduler
        assert self.test_studio.is_scheduling is False

        # with v0.2.6.9 it is now the users duty to set is_scheduling to True
        self.test_studio.is_scheduling = True

        self.test_studio.schedule()
        assert self.test_studio.is_scheduling is False

    def test_schedule_will_store_schedule_info_in_database(self):
        """testing if the schedule method will store the schedule info in
        database
        """
        import datetime
        import pytz
        from stalker import Studio, TaskJugglerScheduler
        tj_scheduler = TaskJugglerScheduler()
        self.test_studio.now = \
            datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
        self.test_studio.start = \
            datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
        self.test_studio.end = \
            datetime.datetime(2013, 7, 30, 0, 0, tzinfo=pytz.utc)

        self.test_studio.scheduler = tj_scheduler
        self.test_studio.schedule(scheduled_by=self.test_user1)

        assert self.test_studio.last_scheduled_by == self.test_user1

        last_schedule_message = self.test_studio.last_schedule_message
        last_scheduled_at = self.test_studio.last_scheduled_at
        last_scheduled_by = self.test_studio.last_scheduled_by

        assert last_schedule_message is not None
        assert last_scheduled_at is not None
        assert last_scheduled_by is not None

        from stalker.db.session import DBSession
        DBSession.add(self.test_studio)
        DBSession.commit()

        # delete the studio instance and retrieve it back and check if it has
        # the info
        del self.test_studio

        studio = Studio.query.first()

        assert studio.is_scheduling is False
        assert \
            datetime.datetime.now(pytz.utc) - studio.scheduling_started_at < \
            datetime.timedelta(minutes=1)
        assert studio.last_schedule_message == last_schedule_message
        assert studio.last_scheduled_at == last_scheduled_at
        assert studio.last_scheduled_by == last_scheduled_by

        assert studio.last_scheduled_by_id == self.test_user1.id
        assert studio.last_scheduled_by == self.test_user1

    def test_vacation_attribute_is_read_only(self):
        """testing if the vacation attribute is a read-only attribute
        """
        with pytest.raises(AttributeError) as cm:
            self.test_studio.vacations = 'some random value'

        assert str(cm.value) == "can't set attribute"

    def test_vacation_attribute_returns_studio_vacation_instances(self):
        """Testing if the vacation attribute is returning the Vacation
        instances with no user set.
        """
        import datetime
        import pytz
        from stalker import Vacation

        vacation1 = Vacation(
            start=datetime.datetime(2013, 8, 2, tzinfo=pytz.utc),
            end=datetime.datetime(2013, 8, 10, tzinfo=pytz.utc)
        )
        vacation2 = Vacation(
            start=datetime.datetime(2013, 8, 11, tzinfo=pytz.utc),
            end=datetime.datetime(2013, 8, 20, tzinfo=pytz.utc)
        )
        vacation3 = Vacation(
            user=self.test_user1,
            start=datetime.datetime(2013, 8, 11, tzinfo=pytz.utc),
            end=datetime.datetime(2013, 8, 20, tzinfo=pytz.utc)
        )
        from stalker.db.session import DBSession
        DBSession.add_all([vacation1, vacation2, vacation3])
        DBSession.commit()

        assert \
            sorted(self.test_studio.vacations, key=lambda x: x.name) == \
            sorted([vacation1, vacation2], key=lambda x: x.name)

    def test_timing_resolution_argument_skipped(self):
        """testing if the timing_resolution attribute will be set to the
        default value from the defaults.timing_resolution if timing_resolution
        argument is skipped
        """
        from stalker import defaults, Studio
        try:
            self.kwargs.pop('timing_resolution')
        except KeyError:
            pass

        studio = Studio(**self.kwargs)
        assert studio.timing_resolution == defaults.timing_resolution

    def test_timing_resolution_argument_is_None(self):
        """testing if the timing_resolution attribute will be set to the
        default value from the default.timing_resolution if timing_resolution
        argument is None
        """
        from stalker import defaults, Studio
        self.kwargs['timing_resolution'] = None
        studio = Studio(**self.kwargs)
        assert studio.timing_resolution == defaults.timing_resolution

    def test_timing_resolution_attribute_is_set_to_None(self):
        """testing if the timing_resolution attribute will be set to the
        default value from the defaults.timing_resolution if it is set to None
        """
        import datetime
        from stalker import defaults, Studio
        self.kwargs['timing_resolution'] = datetime.timedelta(minutes=5)
        studio = Studio(**self.kwargs)
        # check start conditions
        assert studio.timing_resolution == self.kwargs['timing_resolution']
        studio.timing_resolution = None
        assert studio.timing_resolution == defaults.timing_resolution

    def test_timing_resolution_argument_is_not_a_timedelta_instance(self):
        """testing if a TypeError will be raised when the timing_resolution
        argument is not a datetime.timedelta instance
        """
        from stalker import Studio
        self.kwargs['timing_resolution'] = 'not a timedelta instance'
        with pytest.raises(TypeError) as cm:
            Studio(**self.kwargs)

        assert str(cm.value) == \
            'Studio.timing_resolution should be an instance of ' \
            'datetime.timedelta not, str'

    def test_timing_resolution_attribute_is_not_a_timedelta_instance(self):
        """testing if a TypeError will be raised when the timing_resolution
        attribute is not a datetime.timedelta instance
        """
        from stalker import Studio
        new_foo_obj = Studio(**self.kwargs)
        with pytest.raises(TypeError) as cm:
            new_foo_obj.timing_resolution = 'not a timedelta instance'

        assert str(cm.value) == \
            'Studio.timing_resolution should be an instance of ' \
            'datetime.timedelta not, str'

    def test_timing_resolution_argument_is_working_properly(self):
        """testing if the timing_resolution argument value is passed to
        timing_resolution attribute correctly
        """
        import datetime
        from stalker import Studio
        self.kwargs['timing_resolution'] = datetime.timedelta(minutes=5)
        studio = Studio(**self.kwargs)
        assert studio.timing_resolution == self.kwargs['timing_resolution']

    def test_timing_resolution_attribute_is_working_properly(self):
        """testing if the timing_resolution attribute is working properly
        """
        import datetime
        from stalker import Studio
        studio = Studio(**self.kwargs)
        res = studio
        new_res = datetime.timedelta(hours=1, minutes=30)
        assert res != new_res
        studio.timing_resolution = new_res
        assert studio.timing_resolution == new_res
