# -*- coding: utf-8 -*-

import os
import datetime
import logging


logger = logging.getLogger(__name__)

from stalker.log import logging_level
logger.setLevel(logging_level)


class ConfigBase(object):
    """Config abstraction

    Idea is coming from Sphinx config.
    """
    default_config_values = {}

    def __init__(self):
        self.config_values = self.default_config_values.copy()
        self.user_config = {}

        # the priority order is
        # stalker.config
        # config.py under .stalker_rc directory
        # config.py under $STALKER_PATH

        self._parse_settings()

    def _parse_settings(self):
        # for now just use $STALKER_PATH

        # try to get the environment variable
        if self.env_key not in os.environ:
            # don't do anything
            logger.debug("no environment key found for user settings")
        else:
            logger.debug("environment key found")

            resolved_path = os.path.expanduser(
                os.path.join(
                    os.environ[self.env_key],
                    "config.py"
                )
            )

            # using `while` is not safe to expand variables
            # so expand vars for 100 times which already is ridiculously
            # complex
            max_recursion = 100
            i = 0
            while '$' in resolved_path and i < max_recursion:
                resolved_path = os.path.expandvars(
                    resolved_path
                )
                i += 1

            try:
                logger.debug("importing user config")
                with open(resolved_path) as f:
                    exec(f.read(), self.user_config)
            except IOError:
                logger.warning("The $STALKER_PATH: %s doesn't exists! "
                               "skipping user config" % resolved_path)
            except SyntaxError as e:
                raise RuntimeError(
                    "There is a syntax error in your configuration file: %s" %
                    str(e)
                )
            finally:
                # append the data to the current settings
                logger.debug("updating system config")
                for key in self.user_config:
                    #if key in self.config_values:
                    self.config_values[key] = self.user_config[key]

    def __getattr__(self, name):
        return self.config_values[name]

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        return setattr(self, name, value)

    def __delitem__(self, name):
        # delattr(self, name)
        self.config_values.pop(name)

    def __contains__(self, name):
        return name in self.config_values


class Config(ConfigBase):
    """Holds system wide configuration variables. See
    `configuring stalker`_ for more detail.

    .. _configuring stalker: ../configure.html
    """
    env_key = "STALKER_PATH"

    default_config_values = dict(

        #
        # The default settings for the database, see sqlalchemy.create_engine
        # for possible parameters
        #
        database_engine_settings={
            "sqlalchemy.url": "sqlite://",
            "sqlalchemy.echo": False,
            # "sqlalchemy.pool_pre_ping": True,
        },

        database_session_settings={},
        # Local storage path
        local_storage_path=os.path.expanduser('~/.strc'),
        local_session_data_file_name='local_session_data',

        # Storage for uploaded files
        server_side_storage_path=os.path.expanduser('~/Stalker_Storage'),

        repo_env_var_template='REPO%(code)s',
        repo_env_var_template_old='REPO%(id)s',

        #
        # Tells Stalker to create an admin by default
        #
        auto_create_admin=True,

        #
        # these are for new projects
        # after creating the project you can change them from the interface
        #
        admin_name='admin',
        admin_login='admin',
        admin_password='admin',
        admin_email='admin@admin.com',
        admin_department_name='admins',
        admin_group_name='admins',

        # the default keyword which is going to be used in password scrambling
        key="stalker_default_key",

        version_take_name="Main",

        actions=['Create', 'Read', 'Update', 'Delete', 'List'],  # CRUDL

        # Tickets
        ticket_label="Ticket",

        # define the available actions per Status
        ticket_status_names=[
            'New', 'Accepted', 'Assigned', 'Reopened', 'Closed'
        ],

        ticket_status_codes=[
            'NEW', 'ACP', 'ASG', 'ROP', 'CLS'
        ],

        ticket_resolutions=[
            'fixed', 'invalid', 'wontfix', 'duplicate', 'worksforme', 'cantfix'
        ],

        ticket_workflow={
            'resolve': {
                'New': {
                    'new_status': 'Closed',
                    'action': 'set_resolution'
                },
                'Accepted': {
                    'new_status': 'Closed',
                    'action': 'set_resolution'
                },
                'Assigned': {
                    'new_status': 'Closed',
                    'action': 'set_resolution'
                },
                'Reopened': {
                    'new_status': 'Closed',
                    'action': 'set_resolution'
                },
            },
            'accept': {
                'New': {
                    'new_status': 'Accepted',
                    'action': 'set_owner'
                },
                'Accepted': {
                    'new_status': 'Accepted',
                    'action': 'set_owner'
                },
                'Assigned': {
                    'new_status': 'Accepted',
                    'action': 'set_owner'
                },
                'Reopened': {
                    'new_status': 'Accepted',
                    'action': 'set_owner'
                },
            },
            'reassign': {
                'New': {
                    'new_status': 'Assigned',
                    'action': 'set_owner'
                },
                'Accepted': {
                    'new_status': 'Assigned',
                    'action': 'set_owner'
                },
                'Assigned': {
                    'new_status': 'Assigned',
                    'action': 'set_owner'
                },
                'Reopened': {
                    'new_status': 'Assigned',
                    'action': 'set_owner'
                },
            },
            'reopen': {
                'Closed': {
                    'new_status': 'Reopened',
                    'action': 'del_resolution'
                }
            }
        },

        # Task Management
        timing_resolution=datetime.timedelta(hours=1),

        task_priority=500,

        working_hours={
            'mon': [[540, 1080]],  # 9:00 - 18:00
            'tue': [[540, 1080]],  # 9:00 - 18:00
            'wed': [[540, 1080]],  # 9:00 - 18:00
            'thu': [[540, 1080]],  # 9:00 - 18:00
            'fri': [[540, 1080]],  # 9:00 - 18:00
            'sat': [],  # saturday off
            'sun': [],  # sunday off
        },

        # this is strongly related with the working_hours settings,
        # this should match each other
        daily_working_hours=9,
        weekly_working_days=5,
        weekly_working_hours=45,
        yearly_working_days=261,  # math.ceil(5 * 52.1428)

        day_order=['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'],

        datetime_units=['min', 'h', 'd', 'w', 'm', 'y'],
        datetime_unit_names=['minute', 'hour', 'day', 'week', 'month', 'year'],

        datetime_units_to_timedelta_kwargs={
            'min': {'name': 'minutes', 'multiplier': 1},
            'h': {'name': 'hours', 'multiplier': 1},
            'd': {'name': 'days', 'multiplier': 1},
            'w': {'name': 'weeks', 'multiplier': 1},
            'm': {'name': 'days', 'multiplier': 30},
            'y': {'name': 'days', 'multiplier': 365}
        },

        task_status_names=[
            'Waiting For Dependency',
            'Ready To Start',
            'Work In Progress',
            'Pending Review',
            'Has Revision',
            'Dependency Has Revision',
            'On Hold',
            'Stopped',
            'Completed'
        ],

        task_status_codes=[
            'WFD',
            'RTS',
            'WIP',
            'PREV',
            'HREV',
            'DREV',
            'OH',
            'STOP',
            'CMPL'
        ],
    
        project_status_names=[
            'Ready To Start',
            'Work In Progress',
            'Completed'
        ],

        project_status_codes=[
            'RTS',
            'WIP',
            'CMPL'
        ],

        review_status_names=[
            'New',
            'Requested Revision',
            'Approved'
        ],
        review_status_codes=[
            'NEW',
            'RREV',
            'APP'
        ],

        daily_status_names=[
            'Open',
            'Closed'
        ],
        daily_status_codes=[
            'OPEN',
            'CLS'
        ],

        task_schedule_constraints=['none', 'start', 'end', 'both'],
        task_schedule_models=['effort', 'length', 'duration'],
        task_dependency_gap_models=['length', 'duration'],
        task_dependency_targets=['onend', 'onstart'],
        allocation_strategy=['minallocated', 'maxloaded', 'minloaded', 'order',
                             'random'],
        persistent_allocation=True,

        tjp_working_hours_template="""
{%- macro wh(wh, day) -%}
{%- if wh[day]|length %}    workinghours {{day}} {% for part in wh[day] -%}
    {%- if loop.index != 1%}, {% endif -%}
        {{"%02d"|format(part[0]//60)}}:{{"%02d"|format(part[0]%60)}} - {{"%02d"|format(part[1]//60)}}:{{"%02d"|format(part[1]%60)}}
    {%- endfor -%}
{%- else %}    workinghours {{day}} off
{%- endif -%}
{%- endmacro -%}
{{wh(workinghours, 'mon')}}
{{wh(workinghours, 'tue')}}
{{wh(workinghours, 'wed')}}
{{wh(workinghours, 'thu')}}
{{wh(workinghours, 'fri')}}
{{wh(workinghours, 'sat')}}
{{wh(workinghours, 'sun')}}""",

        tjp_studio_template="""
project {{ studio.tjp_id }} "{{ studio.tjp_id }}" {{ studio.start.date() }} - {{ studio.end.date() }} {
    timingresolution {{ '%i'|format((studio.timing_resolution.days * 86400 + studio.timing_resolution.seconds)//60|int) }}min
    now {{ studio.now.astimezone(utc).strftime('%Y-%m-%d-%H:%M') }}
    dailyworkinghours {{ studio.daily_working_hours }}
    weekstartsmonday
{{ studio.working_hours.to_tjp }}
    timeformat "%Y-%m-%d"
    scenario plan "Plan"
    trackingscenario plan
}
""",

        tjp_project_template="""
task {{project.tjp_id}} "{{project.tjp_id}}" {
    {% for task in project.root_tasks %}
        {{task.to_tjp}}
    {%- endfor %}
}
""",

        tjp_task_template="""
task {{task.tjp_id}} "{{task.tjp_id}}" {

    {% if task.priority != 500 -%}
        priority {{task.priority}}
    {%- endif %}

    {% if task.task_depends_to %}
        depends {# #}
        {%- for depends in task.task_depends_to %}
            {%- if loop.index != 1 %}, {% endif %}{{depends.to_tjp}}
        {%- endfor %}
    {%- endif -%}

    {%- if task.is_container -%}
        {% for child_task in task.children -%}
            {{ child_task.to_tjp }}
        {%- endfor %}
    {%- else %}
        {% if task.resources|length %}

            {% if task.schedule_constraint %}
                {% if task.schedule_constraint == 1 or task.schedule_constraint == 3 %}
                    start {{ task.start.astimezone(utc).strftime('%Y-%m-%d-%H:%M') }}
                {% endif %}
                {% if task.schedule_constraint == 2 or task.schedule_constraint == 3 -%}
                    end {{ task.end.astimezone(utc).strftime('%Y-%m-%d-%H:%M') }}
                {% endif %}
            {% endif %}

            {{task.schedule_model}} {{task.schedule_timing}}{{task.schedule_unit}}
            allocate {# #}
            {%- for resource in task.resources -%}
                {%- if loop.index != 1 %}, {% endif %}{{ resource.tjp_id }} {# #}
                {%- if task.alternative_resources %}{
                    alternative
                    {% for alt_res in task.alternative_resources -%}
                        {%-if loop.index != 1 %}, {% endif %}
                        {{- alt_res.tjp_id}}
                    {%- endfor -%}
                    {# #} select {{task.allocation_strategy}}
                    {% if task.persistent_allocation -%}
                        persistent
{# #}
                    {%- endif %}
                }
                {%- endif %}
            {%- endfor %}
        {%- endif %}
        {% for time_log in task.time_logs %}
            booking {{time_log.resource.tjp_id}} {{time_log.start.astimezone(utc).strftime('%Y-%m-%d-%H:%M:%S')}} - {{time_log.end.astimezone(utc).strftime('%Y-%m-%d-%H:%M:%S')}} { overtime 2 }
        {% endfor %}
    {% endif %}

}
""",

        tjp_task_dependency_template="""{{depends_to.tjp_abs_id}} { {{- dependency_target}}{%if gap_timing %} gap{{gap_model}} {{gap_timing}}{{gap_unit -}}{%endif -%}}""",

        tjp_department_template="""
resource {{department.tjp_id}} "{{department.tjp_id}}" {
{% for resource in department.users %}
    {{resource.to_tjp}}
{% endfor -%}
}
""",

        tjp_vacation_template='''vacation {{ vacation.start.astimezone(utc).strftime('%Y-%m-%d-%H:%M:%S') }} - {{ vacation.end.astimezone(utc).strftime('%Y-%m-%d-%H:%M:%S') }}''',

        tjp_user_template='''resource {{user.tjp_id}} "{{user.tjp_id}}" {
    efficiency {{user.efficiency}}
{% if user.vacations %}
{% for vacation in user.vacations %}
    {{vacation.to_tjp}}
{% endfor %}
{% endif -%} }''',

        tjp_main_template="""# Generated By Stalker v{{stalker.__version__}}
        {{studio.to_tjp}}

        # resources
        resource resources "Resources" {
        {%- for vacation in studio.vacations %}
            {{vacation.to_tjp}}
        {%- endfor %}
        {%- for user in studio.users %}
            {{user.to_tjp}}
        {%- endfor %}
        }

        # tasks
        {% for project in projects %}
            {{project.to_tjp}}
        {% endfor %}

        # reports
        taskreport breakdown "{{csv_file_name}}"{
            formats csv
            timeformat "%Y-%m-%d-%H:%M"
            columns id, start, end {%- if compute_resources %}, resources{% endif %}
        }
        """,

        tjp_main_template2="""# Generated By Stalker v{{stalker.__version__}}
        {{studio.to_tjp}}

        # resources
        resource resources "Resources" {
        {%- for vacation in studio.vacations %}
            {{vacation.to_tjp}}
        {%- endfor %}
        {%- for user in studio.users %}
            {{user.to_tjp}}
        {%- endfor %}
        }

# tasks
{{ tasks_buffer }}

# reports
taskreport breakdown "{{csv_file_name}}"{
    formats csv
    timeformat "%Y-%m-%d-%H:%M"
    columns id, start, end {%- if compute_resources %}, resources{% endif %}
}""",

        tj_command='tj3' if os.name == 'nt' else '/usr/local/bin/tj3',

        path_template='{{project.code}}/{%- for parent_task in parent_tasks -%}{{parent_task.nice_name}}/{%- endfor -%}',
        filename_template='{{task.entity_type}}_{{task.id}}_{{version.take_name}}_v{{"%03d"|format(version.version_number)}}',

        # --------------------------------------------
        # the following settings came from oyProjectManager
        sequence_format="%h%p%t %R",
        file_size_format="%.2f MB",
        date_time_format='%Y.%m.%d %H:%M',

        resolution_presets={
            "PC Video": [640, 480, 1.0],
            "NTSC": [720, 486, 0.91],
            "NTSC 16:9": [720, 486, 1.21],
            "PAL": [720, 576, 1.067],
            "PAL 16:9": [720, 576, 1.46],
            "HD 720": [1280, 720, 1.0],
            "HD 1080": [1920, 1080, 1.0],
            "1K Super 35": [1024, 778, 1.0],
            "2K Super 35": [2048, 1556, 1.0],
            "4K Super 35": [4096, 3112, 1.0],
            "A4 Portrait": [2480, 3508, 1.0],
            "A4 Landscape": [3508, 2480, 1.0],
            "A3 Portrait": [3508, 4960, 1.0],
            "A3 Landscape": [4960, 3508, 1.0],
            "A2 Portrait": [4960, 7016, 1.0],
            "A2 Landscape": [7016, 4960, 1.0],
            "50x70cm Poster Portrait": [5905, 8268, 1.0],
            "50x70cm Poster Landscape": [8268, 5905, 1.0],
            "70x100cm Poster Portrait": [8268, 11810, 1.0],
            "70x100cm Poster Landscape": [11810, 8268, 1.0],
            "1k Square": [1024, 1024, 1.0],
            "2k Square": [2048, 2048, 1.0],
            "3k Square": [3072, 3072, 1.0],
            "4k Square": [4096, 4096, 1.0],
        },

        default_resolution_preset="HD 1080",

        project_structure="""{% for shot in project.shots %}
                Shots/{{shot.code}}
                Shots/{{shot.code}}/Plate
                Shots/{{shot.code}}/Reference
                Shots/{{shot.code}}/Texture
            {% endfor %}
        {% for asset in project.assets%}
            {% set asset_path = project.full_path + '/Assets/' + asset.type.name + '/' + asset.code %}
            {{asset_path}}/Texture
            {{asset_path}}/Reference
        {% endfor %}
        """,

        thumbnail_format="jpg",
        thumbnail_quality=70,
        thumbnail_size=[320, 180],
    )
