# -*- coding: utf-8 -*-

import os
import subprocess
import tempfile
import datetime
import time
import csv

import pytz

from stalker.log import logging_level

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


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

    :param bool compute_resources: When set to True it will also consider
      :attr:`.Task.alternative_resources` attribute and will fill
      :attr:`.Task.computed_resources` attribute for each Task. With
      :class:`.TaskJugglerScheduler` when the total number of Task is around
      15k it will take around 7 minutes to generate this data, so by default it
      is False.
    :param int parsing_method: Choose between SQL (0) or Pure Python (1)
      parsing. The default is SQL.
    """

    def __init__(self,
                 studio=None,
                 compute_resources=False,
                 parsing_method=0,
                 projects=None):
        super(TaskJugglerScheduler, self).__init__(studio)

        self.tjp_content = ''

        self.temp_file_full_path = None
        self.temp_file_path = None
        self.temp_file_name = None

        self.tjp_file_full_path = None
        self.tjp_file = None

        self.csv_file_full_path = None
        self.csv_file = None

        self.compute_resources = compute_resources
        self.parsing_method = parsing_method

        self._projects = []
        self.projects = projects

    def _create_tjp_file(self):
        """creates the tjp file
        """
        self.temp_file_full_path = tempfile.mktemp(prefix='Stalker_')
        self.temp_file_path = os.path.dirname(self.temp_file_full_path)
        self.temp_file_name = os.path.basename(self.temp_file_full_path)
        self.tjp_file_full_path = self.temp_file_full_path + ".tjp"
        self.csv_file_full_path = self.temp_file_full_path + ".csv"

    def _create_tjp_file_content(self):
        """creates the tjp file content
        """
        from jinja2 import Template

        start = time.time()

        # use new way of doing it, it will just work with PostgreSQL
        import json
        from stalker import defaults
        from stalker.db.session import DBSession
        template = Template(defaults.tjp_main_template2)

        if not self.projects:
            project_ids = DBSession.connection().execute(
                'select id, code from "Projects"'
            ).fetchall()
        else:
            project_ids = [[project.id] for project in self.projects]

        sql_query = """select
    "Tasks".id,
    tasks.path,
    coalesce("Tasks".parent_id, "Tasks".project_id) as parent_id,
    tasks.entity_type,
    tasks.name,
    "Tasks".priority,
    "Tasks".schedule_timing,
    "Tasks".schedule_unit,
    "Tasks".schedule_model,
    "Tasks".allocation_strategy,
    "Tasks".persistent_allocation,
    tasks.depth,
    task_resources.resource_ids,
    task_alternative_resources.resource_ids as alternative_resource_ids,
    time_logs.time_log_array,
    task_dependencies.dependency_info,
    not exists (
       select 1
        from "Tasks" as "Child_Tasks"
        where "Child_Tasks".parent_id = "Tasks".id
    ) as is_leaf
from "Tasks"
join (
    with recursive recursive_task(id, parent_id, path_as_text, path, depth) as (
        select
            id,
            parent_id,
            id::text as path_as_text,
            array[project_id] as path,
            0
        from "Tasks"
        where parent_id is NULL and project_id = :id
    union all
        select
            task.id,
            task.parent_id,
            (parent.path_as_text || '-' || task.id) as path_as_text,
            (parent.path || task.parent_id) as path,
            parent.depth + 1 as depth
        from "Tasks" as task
        join recursive_task as parent on task.parent_id = parent.id
    ) select
        recursive_task.id,
        recursive_task.parent_id,
        recursive_task.path_as_text,
        recursive_task.path,
        "SimpleEntities".name as name,
        "SimpleEntities".entity_type,
        recursive_task.depth
    from recursive_task
    join "SimpleEntities" on recursive_task.id = "SimpleEntities".id
    --order by path_as_text
) as tasks on "Tasks".id = tasks.id

-- resources
left outer join (
    select
        task_id,
        array_agg(resource_id order by resource_id) as resource_ids
    from "Task_Resources"
    group by task_id
) as task_resources on "Tasks".id = task_resources.task_id

-- alternative resources
left outer join (
    select
        task_id,
        array_agg(resource_id order by resource_id) as resource_ids
    from "Task_Alternative_Resources"
    group by task_id
) as task_alternative_resources on "Tasks".id = task_alternative_resources.task_id

-- time logs
left outer join (
    select
        "TimeLogs".task_id,
        array_agg(('User_' || "TimeLogs".resource_id, to_char(cast("TimeLogs".start at time zone 'utc' as timestamp), 'YYYY-MM-DD-HH24:MI:00'), to_char(cast("TimeLogs".end at time zone 'utc' as timestamp), 'YYYY-MM-DD-HH24:MI:00'))) as time_log_array
    from "TimeLogs"
    group by task_id
) as time_logs on "Tasks".id = time_logs.task_id

-- dependencies
left outer join (
    select
        task_id,
        array_agg((tasks.alt_path, dependency_target, gap_timing, gap_unit, gap_model)) dependency_info
    from "Task_Dependencies"
    join (
        with recursive recursive_task(id, parent_id, alt_path) as (
            select
                id,
                parent_id,
                project_id::text as alt_path
            from "Tasks"
            where parent_id is NULL
        union all
            select
                task.id,
                task.parent_id,
                (parent.alt_path || '-' || task.parent_id) as alt_path
            from "Tasks" as task
            join recursive_task as parent on task.parent_id = parent.id
        ) select
            recursive_task.id,
            recursive_task.parent_id,
            recursive_task.alt_path || '-' || recursive_task.id as alt_path
        from recursive_task
        join "SimpleEntities" on recursive_task.id = "SimpleEntities".id
    ) as tasks on "Task_Dependencies".depends_to_id = tasks.id
    group by task_id
) as task_dependencies on "Tasks".id = task_dependencies.task_id

--order by "Tasks".id
order by path_as_text"""

        result_buffer = []
        num_of_records = 0

        # run it per project
        from sqlalchemy import text
        for pr in project_ids:
            p_id = pr[0]
            #p_code = pr[1]

            result = DBSession.connection().execute(text(sql_query), id=p_id)

            # start by adding the project first
            result_buffer.append(
                'task Project_%s "Project_%s" {' % (p_id, p_id)
            )

            # now start jumping around
            previous_level = 0
            for r in result.fetchall():
                # start by appending task tjp id first
                task_id = r[0]
                # path = r[1]
                # parent_id = r[2]
                # entity_type = r[3]
                #name = r[4]
                priority = r[5]
                schedule_timing = r[6]
                schedule_unit = r[7]
                schedule_model = r[8]
                allocation_strategy = r[9]
                persistent_allocation = r[10]
                depth = r[11] + 1
                resource_ids = r[12]
                alternative_resource_ids = r[13]
                time_log_array = r[14]
                dependency_info = r[15]
                is_leaf = r[16]

                tab = '  ' * depth

                # close the previous level if necessary
                for i in range(previous_level - depth + 1):
                    i_tab = '  ' * (previous_level - i)
                    result_buffer.append('%s}' % i_tab)

                result_buffer.append(
                    """%(tab)stask Task_%(id)s "Task_%(id)s" {""" % {
                        'tab': tab,
                        'id': task_id
                    }
                )

                # append priority if it is different then 500
                if priority != 500:
                    result_buffer.append(
                        '%s  priority %s' % (tab, priority))

                # append dependency information
                if dependency_info:
                    dep_buffer = ['%s  depends ' % tab]

                    json_data = json.loads(
                        dependency_info.replace('{', '[')
                        .replace('}', ']')
                        .replace('(', '')
                        .replace(')', '')
                    )  # it is an array of string

                    for i, dep in enumerate(json_data):
                        if i > 0:
                            dep_buffer.append(', ')

                        dep_full_ids, \
                            dependency_target, \
                            gap_timing, \
                            gap_unit, \
                            gap_model = dep.split(',')

                        dep_full_path = '.'.join(
                            map(lambda x: 'Task_%s' % x,
                                dep_full_ids.split('-'))
                        )
                        # fix for Project id
                        dep_full_path = 'Project_%s' % dep_full_path[5:]

                        dep_string = '%s {%s}' % (
                            dep_full_path, dependency_target)

                        dep_buffer.append(dep_string)

                    result_buffer.append(''.join(dep_buffer))

                # append schedule model and timing information
                # if this is a leaf task and has resources
                if is_leaf and resource_ids:
                    result_buffer.append(
                        '%s  %s %s%s' % (
                            tab, schedule_model, schedule_timing,
                            schedule_unit
                        )
                    )

                    resource_buffer = ['%s  allocate ' % tab]
                    for i, resource_id in enumerate(resource_ids):
                        if i > 0:
                            resource_buffer.append(', ')
                        resource_buffer.append('User_%s' % resource_id)

                        # now go through alternatives
                        if alternative_resource_ids:
                            resource_buffer.append(' { alternative ')
                            for j, alt_resource_id in \
                                    enumerate(alternative_resource_ids):
                                if j > 0:
                                    resource_buffer.append(', ')
                                resource_buffer.append(
                                    'User_%s' % alt_resource_id)

                            # set the allocation strategy
                            resource_buffer.append(
                                ' select %s' % allocation_strategy)

                            # is is persistent
                            if persistent_allocation:
                                resource_buffer.append(' persistent')
                            resource_buffer.append(' }')

                    result_buffer.append(''.join(resource_buffer))

                    # append any time log information
                    if time_log_array:
                        json_data = json.loads(
                            time_log_array.replace('{', '[')
                            .replace('}', ']')
                            .replace('(', '')
                            .replace(')', '')
                        )  # it is an array of string

                        for tlog in json_data:
                            user_id, t_start, t_end = tlog.split(',')
                            result_buffer.append(
                                '%s  booking %s %s - %s { overtime 2 }' % (
                                    tab, user_id, t_start, t_end
                                )
                            )

                previous_level = depth
                num_of_records += 1

            # and close the brackets per project
            depth = 0  # current depth is 0 (Project)
            # previous_level is the last task
            for i in range(previous_level - depth + 1):
                i_tab = '  ' * (previous_level - i)
                result_buffer.append('%s}' % i_tab)

        tasks_buffer = '\n'.join(result_buffer)

        import stalker
        self.tjp_content = template.render({
            'stalker': stalker,
            'studio': self.studio,
            'csv_file_name': self.temp_file_name,
            'csv_file_full_path': self.temp_file_full_path,
            'compute_resources': self.compute_resources,
            'tasks_buffer': tasks_buffer
        })

        logger.debug(
            'total number of records: %s' % num_of_records
        )

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
        computed_end values
        """
        parsing_start = time.time()

        logger.debug('csv_file_full_path : %s' % self.csv_file_full_path)
        if not os.path.exists(self.csv_file_full_path):
            logger.debug('could not find CSV file, '
                         'returning without updating db!')
            return

        from stalker import Task, Project
        from stalker.models.task import Task_Computed_Resources

        entity_ids = []
        update_data = []
        update_user_data = []

        with open(self.csv_file_full_path, 'r') as self.csv_file:
            csv_content = csv.reader(self.csv_file, delimiter=';')

            lines = [line for line in csv_content]
            lines.pop(0)

        for data in lines:
            id_line = data[0]

            entity_id = int(id_line.split('.')[-1].split('_')[-1])

            if entity_id:
                entity_ids.append(entity_id)
                start_date = datetime.datetime.strptime(
                    data[1], "%Y-%m-%d-%H:%M"
                )
                end_date = datetime.datetime.strptime(
                    data[2],
                    "%Y-%m-%d-%H:%M"
                )

                # implement time zone info
                start_date = start_date.replace(tzinfo=pytz.utc)
                end_date = end_date.replace(tzinfo=pytz.utc)

                # computed_resources
                if self.compute_resources:
                    if data[3] != '':
                        resources_data = map(
                            lambda x: x.split('_')[-1].split(')')[0],
                            data[3].split(',')
                        )
                        for rid in resources_data:
                            update_user_data.append({
                                'task_id': entity_id,
                                'resource_id': rid
                            })

                update_data.append({
                    'b_id': entity_id,
                    'start': start_date,
                    'end': end_date,
                    'computed_start': start_date,
                    'computed_end': end_date
                })

        from sqlalchemy import bindparam

        # update date values
        update_statement = Task.__table__.update()\
            .where(Task.__table__.c.id == bindparam('b_id'))\
            .values(
                start=bindparam('start'),
                end=bindparam('end'),
                computed_start=bindparam('computed_start'),
                computed_end=bindparam('computed_end')
            )
        from stalker.db.session import DBSession
        DBSession.connection().execute(
            update_statement,
            update_data
        )

        # update project dates
        update_project_statement = Project.__table__.update()\
            .where(Project.__table__.c.id == bindparam('b_id'))\
            .values(
                start=bindparam('start'),
                end=bindparam('end'),
                computed_start=bindparam('computed_start'),
                computed_end=bindparam('computed_end')
            )
        DBSession.connection().execute(
            update_project_statement,
            update_data
        )

        # update computed resources data
        # first delete everything
        if self.compute_resources:
            delete_resources_statement = Task_Computed_Resources.delete()

            update_resources_statement = Task_Computed_Resources.insert()\
                .values(
                    task_id=bindparam('task_id'),
                    resource_id=bindparam('resource_id')
                )

            DBSession.connection().execute(delete_resources_statement)
            DBSession.connection().execute(
                update_resources_statement,
                update_user_data
            )

        parsing_end = time.time()
        logger.debug(
            'completed parsing csv file in (SQL): %s seconds' %
            (parsing_end - parsing_start)
        )

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

        # create a tjp file
        self._create_tjp_file()

        # create tjp file content
        self._create_tjp_file_content()

        # fill it with data
        self._fill_tjp_file()

        logger.debug('tjp_file_full_path: %s' % self.tjp_file_full_path)

        # pass it to tj3
        from stalker import defaults
        if os.name == 'nt':
            logger.debug('tj3 using fallback mode for Windows!')
            command = '%s %s -o %s' % (
                defaults.tj_command,
                self.tjp_file_full_path,
                self.temp_file_path,
            )
            logger.debug('tj3 command: %s' % command)
            return_code = os.system(command)
            stderr_buffer = ''
        else:
            process = subprocess.Popen(
                [defaults.tj_command,
                 self.tjp_file_full_path,
                 '-o',
                 self.temp_file_path],
                stderr=subprocess.PIPE
            )

            # loop until process finishes and capture stderr output
            stderr_buffer = []
            while True:
                stderr = process.stderr.readline()

                if stderr == b'' and process.poll() is not None:
                    break

                if stderr != b'':
                    stderr = stderr.decode('utf-8').strip()
                    stderr_buffer.append(stderr)
                    logger.debug(stderr)

            # flatten the buffer
            stderr_buffer = '\n'.join(stderr_buffer)

            return_code = process.returncode

        if return_code:
            # there is an error
            raise RuntimeError(stderr_buffer)

        # read back the csv file
        self._parse_csv_file()

        logger.debug('tj3 return code: %s' % return_code)

        # remove the tjp file
        self._clean_up()

        return stderr_buffer

    def _validate_projects(self, projects):
        """validates the given projects value
        """
        if projects is None:
            projects = []

        msg = '%(class)s.projects should be a list of ' \
            'stalker.models.project.Project instances, not ' \
            '%(projects_class)s'

        if not isinstance(projects, list):
            raise TypeError(
                msg % {
                    'class': self.__class__.__name__,
                    'projects_class': projects.__class__.__name__
                }
            )

        from stalker import Project
        for item in projects:
            if not isinstance(item, Project):
                raise TypeError(
                    msg % {
                        'class': self.__class__.__name__,
                        'projects_class': item.__class__.__name__
                    }
                )

        return projects

    @property
    def projects(self):
        """getter for the _project attribute
        """
        return self._projects

    @projects.setter
    def projects(self, projects):
        """setter for the _project attribute
        """
        self._projects = self._validate_projects(projects)
