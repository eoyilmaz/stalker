# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import os
import subprocess
import tempfile
import datetime
import time
import csv

import stalker
from stalker import defaults
from stalker.models.entity import Entity

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SchedulerBase(object):
    """This is the base class for schedulers.

    All the schedulers should be derived from this class.
    """

    def __init__(self, studio=None):
        self._studio = None
        self.studio = studio

    def _validate_studio(self, studio_in):
        """validates the given studio_in value
        """
        if studio_in is not None:
            from stalker import Studio
            if not isinstance(studio_in, Studio):
                raise TypeError(
                    '%s.studio should be an instance of '
                    'stalker.models.studio.Studio, not %s' %
                    (self.__class__.__name__, studio_in.__class__.__name__)
                )
        return studio_in

    @property
    def studio(self):
        """studio getter
        """
        return self._studio

    @studio.setter
    def studio(self, studio_in):
        """studio setter
        """
        self._studio = self._validate_studio(studio_in)

    def schedule(self):
        """the main scheduling function should be implemented in the
        derivatives
        """
        raise NotImplementedError


class TaskJugglerScheduler(SchedulerBase):
    """This is the main scheduler for Stalker right now.

    This class prepares the data for TaskJuggler and let it solve the
    scheduling problem, and then retrieves the solved date and resource data
    back.

    TaskJugglerScheduler needs a :class:`.Studio` instance to work with, it
    will create a .tjp file and then solve the tasks and restore the
    computed_start and computed_end dates and the computed_resources
    attributes for each task.

    Stalker will pass all its data to TaskJuggler by creating a tjp file that
    TaskJuggler can parse. This tjp file has all the Projects, Tasks, Users,
    Departments, TimeLogs, Vacations and everything that TJ need for solving
    the tasks. With every new version of it, Stalker tries to cover more and
    more TaskJuggler directives.

    .. note::
       .. versionadded:: 0.2.5
          Alternative Resources

       Stalker is now able to pass alternative resources to TaskJuggler.
       Although, per resource alternatives are not yet possible, it will be
       implemented in future versions of Stalker.

    .. note::
       .. versionadded:: 0.2.5
          Task Dependency Relation Attributes

       Stalker now can use 'gapduration', 'gaplength', 'onstart' and 'onend'
       TaskJuggler directives for each dependent task of a task. Use the
       TaskDependency instance in Task.task_dependency attribute to control how
       a particular task is depending to another task.

    .. warning::
       **Task.computed_resources Attribute Content**

       After the scheduling is finished, TaskJuggler will create a ``csv``
       report that TaskJugglerScheduler will parse. This csv file contains the
       ``id``, ``start date``, ``end date`` and ``resources`` data. The
       resources reported back by TJ will be stored in
       :attr:`.Task.computed_resources` attribute.

       TaskJuggler will put all the resources who may have entered a
       :class:`.TimeLog` previously to the csv file. But the resources from the
       csv file may not be in :attr:`.Task.resources` or
       :attr:`.Task.alternative_resources` anymore. Because of that,
       TaskJugglerScheduler will only store the resources those are both in csv
       file and in :attr:`.Task.resources` or
       :attr:`.Task.alternative_resources` attributes.

    Stalker will export each Project to tjp as the highest task in the
    hierarchy and all the projects will be combined in to the same tjp file.
    Combining all the Projects in one tjp file has a very nice side effect,
    projects using the same resources will respect their allocations to the
    resource. So that when a TaskJugglerScheduler instance is used to schedule
    the project, all projects are scheduled together.

    The following table shows which Stalker data type is converted to which
    TaskJuggler type:
    
      +------------+-------------+
      | Stalker    | TaskJuggler |
      +============+=============+
      | Studio     | Project     |
      +------------+-------------+
      | Project    | Task        |
      +------------+-------------+
      | Task       | Task        |
      +------------+-------------+
      | Asset      | Task        |
      +------------+-------------+
      | Shot       | Task        |
      +------------+-------------+
      | Sequence   | Task        |
      +------------+-------------+
      | Departmemt | Resource    |
      +------------+-------------+
      | User       | Resource    |
      +------------+-------------+
      | TimeLog    | Booking     |
      +------------+-------------+
      | Vacation   | Vacation    |
      +------------+-------------+
      

    """

    def __init__(self, studio=None):
        super(TaskJugglerScheduler, self).__init__(studio)

        self.tjp_content = ''

        self.temp_file_full_path = None
        self.temp_file_path = None
        self.temp_file_name = None

        self.tjp_file_full_path = None
        self.tjp_file = None

        self.csv_file_full_path = None
        self.csv_file = None

    def _create_tjp_file(self):
        """creates the tjp file
        """
        self.temp_file_full_path = tempfile.mktemp(prefix='Stalker_')
        self.temp_file_name = os.path.basename(self.temp_file_full_path)
        self.tjp_file_full_path = self.temp_file_full_path + ".tjp"
        self.csv_file_full_path = self.temp_file_full_path + ".csv"

    def _create_tjp_file_content(self):
        """creates the tjp file content
        """
        from jinja2 import Template

        template = Template(defaults.tjp_main_template)

        start = time.time()
        self.tjp_content = template.render({
            'stalker': stalker,
            'studio': self.studio,
            'csv_file_name': self.temp_file_name,
            'csv_file_full_path': self.temp_file_full_path
        })
        end = time.time()
        logger.debug(
            'rendering the whole tjp file took : %s seconds' % (end - start)
        )

    def _fill_tjp_file(self):
        """fills the tjp file with content
        """
        with open(self.tjp_file_full_path, 'w+') as self.tjp_file:
            self.tjp_file.write(self.tjp_content)

    def _delete_tjp_file(self):
        """deletes the temp tjp file
        """
        try:
            os.remove(self.tjp_file_full_path)
        except OSError:
            pass

    def _delete_csv_file(self):
        """deletes the temp csv file
        """
        try:
            os.remove(self.csv_file_full_path)
        except OSError:
            pass

    def _clean_up(self):
        """removes the temp files
        """
        self._delete_tjp_file()
        self._delete_csv_file()

    def _parse_csv_file(self):
        """parses back the csv file and fills the tasks with computes_start and
        computed end values
        """
        logger.debug('csv_file_full_path : %s' % self.csv_file_full_path)
        from stalker import User  #, Task
        # from stalker.db import DBSession

        with open(self.csv_file_full_path, 'r') as self.csv_file:
            csv_content = csv.reader(self.csv_file, delimiter=';')
            lines = [line for line in csv_content]
            lines.pop(0)
            for data in lines:
                id_line = data[0]
                entity_id = int(id_line.split('.')[-1].split('_')[-1])
                entity = Entity.query.filter(Entity.id == entity_id).first()
                # tasks = Task.__table__
                if entity:
                    start_date = datetime.datetime.strptime(
                        data[1], "%Y-%m-%d-%H:%M"
                    )
                    end_date = datetime.datetime.strptime(
                        data[2],
                        "%Y-%m-%d-%H:%M"
                    )

                    # computed_resources
                    resources_data = map(
                        lambda x: x.split('_')[-1].split(')')[0],
                        data[3].split(',')
                    )
                    computed_resources = \
                        User.query.filter(User.id.in_(resources_data)).all()

                    entity.computed_start = start_date
                    entity.computed_end = end_date
                    entity.computed_resources = computed_resources
                    # update_statement = tasks.update().values({
                    #     tasks.c.start: start_date,
                    #     tasks.c.end: end_date,
                    #     tasks.c.computed_start: start_date,
                    #     tasks.c.computed_end: end_date
                    # }).where(tasks.c.id == entity_id)
                    # DBSession.connection().execute(update_statement)
        logger.debug('completed parsing csv file')

    def schedule(self):
        """Does the scheduling.
        """
        # check the studio attribute
        from stalker import Studio

        if not isinstance(self.studio, Studio):
            raise TypeError(
                '%s.studio should be an instance of '
                'stalker.models.studio.Studio, not %s' %
                (self.__class__.__name__, self.studio.__class__.__name__)
            )

        # ********************************************************************
        # TODO: remove the hardcoded datetime
        #
        # Adjust Studio.start:
        # 1- Looking at the earliest TimeLog entry for all of the active
        #    Projects. If, there are no TimeLogs, use today 0:00.
        # 2- Update the Studio.start if the project that have the earliest
        #    TimeLog has been deactivated.
        #
        # Adjust Studio.end:
        # 1- If the Studio.end is None, set it to Studio.start
        # 2- Add 1 month to Studio.end
        # 3- Schedule it.
        # 4- If TaskJuggler complains about that some of the tasks doesn't fit
        #    in to the time range, or some of the task marked as non scheduled,
        #    increment the Studio.end by 2 months.
        # 5- If TaskJuggler complains again then increment 3 months, and then
        #    5, 8, 13, 21... that is the fibonacci series.
        # 6- When TaskJuggler is successful on scheduling the projects, reset
        #    the increment counter, and use this new date until TJ starts to
        #    complain again.
        #
        self.studio._start = datetime.datetime(2013, 1, 1)
        self.studio._end = datetime.datetime(2016, 1, 1)
        #for project in self.studio.active_projects:
        #    for root_task in project.root_tasks:
        #        if root_task.start < self.studio.start:
        #            self.studio.start = root_task.start
        #        if root_task.end > self.studio.end:
        #            self.studio.end = root_task.end

        # now for safety multiply the duration by 2
        #self.studio.end = (self.studio.end - self.studio.start) * 5 + \
        #                  self.studio.start

        # create a tjp file
        self._create_tjp_file()

        # create tjp file content
        self._create_tjp_file_content()

        # fill it with data
        self._fill_tjp_file()

        logger.debug('tjp_file_full_path: %s' % self.tjp_file_full_path)

        # pass it to tj3
        process = subprocess.Popen(
            [defaults.tj_command,
             self.tjp_file_full_path],
            stderr=subprocess.PIPE
        )
        # wait it to complete
        process.wait()

        stderr = process.stderr.readlines()

        if process.returncode:
            # there is an error
            raise RuntimeError(stderr)

        # read back the csv file
        self._parse_csv_file()

        logger.debug('tj3 return code: %s' % process.returncode)
        logger.debug('tj3 output: %s' % stderr)

        # remove the tjp file
        #self._clean_up()

        return stderr
