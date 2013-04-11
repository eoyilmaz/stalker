# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import datetime

#
# The default settings for the database, see sqlalchemy.create_engine for
# possible parameters
# 
DATABASE_ENGINE_SETTINGS = {
    "sqlalchemy.url": "sqlite:///:memory:",
    "sqlalchemy.echo": False,
}

DATABASE_SESSION_SETTINGS = {}

#
# Tells Stalker to create an admin by default
#
AUTO_CREATE_ADMIN = True

# 
# these are for new projects
# after creating the project you can change them from the interface
# 
ADMIN_NAME = 'Admin'
ADMIN_LOGIN = 'admin'
ADMIN_CODE = 'adm'
ADMIN_PASSWORD = 'admin'
ADMIN_EMAIL = 'admin@admin.com'
ADMIN_DEPARTMENT_NAME = 'admins'
ADMIN_GROUP_NAME = 'admins'


# the default keyword which is going to be used in password scrambling
KEY = "stalker_default_key"

VERSION_TAKE_NAME = "Main"

TICKET_LABEL = "Ticket"

ACTIONS = ['Create', 'Read', 'Update', 'Delete', 'List'] #CRUDL

STATUS_BG_COLOR = 0xffffff
STATUS_FG_COLOR = 0x000000

# Task Management
TIMING_RESOLUTION = datetime.timedelta(hours=1)
TASK_DURATION = datetime.timedelta(days=10)
TASK_PRIORITY = 500

WORKING_HOURS = {
  'mon': [[570, 1110]], # 9:30 - 18:30
  'tue': [[570, 1110]], # 9:30 - 18:30
  'wed': [[570, 1110]], # 9:30 - 18:30
  'thu': [[570, 1110]], # 9:30 - 18:30
  'fri': [[570, 1110]], # 9:30 - 18:30
  'sat': [], # saturday off
  'sun': [], # sunday off
}

DAY_ORDER = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

DAILY_WORKING_HOURS = 8

# define the available actions per Status
TICKET_STATUS_ORDER = ['new', 'accepted', 'assigned', 'reopened', 'closed']

TICKET_RESOLUTIONS = [
    'fixed', 'invalid', 'wontfix', 'duplicate', 'worksforme', 'cantfix'
]

TICKET_WORKFLOW = {
    # Action #OLD STATUS # NEW STATUS
    'resolve' : {
        'new': {
            'new_status': 'closed',
            'action': 'set_resolution'
        },
        'accepted': {
            'new_status': 'closed',
            'action': 'set_resolution'
        },
        'assigned': {
            'new_status': 'closed',
            'action': 'set_resolution'
        },
        'reopened': {
            'new_status': 'closed',
            'action': 'set_resolution'
        },
    },
    'accept' : {
        'new': {
            'new_status': 'accepted',
            'action': 'set_owner'
        },
        'accepted': {
            'new_status': 'accepted',
            'action': 'set_owner'
        },
        'assigned': {
            'new_status': 'accepted',
            'action': 'set_owner'
        },
        'reopened': {
            'new_status': 'accepted',
            'action': 'set_owner'
        },
    },
    'reassign': {
        'new': {
            'new_status': 'assigned',
            'action': 'set_owner'
        },
        'accepted': {
            'new_status': 'assigned',
            'action': 'set_owner'
        },
        'assigned': {
            'new_status': 'assigned',
            'action': 'set_owner'
        },
        'reopened': {
            'new_status': 'assigned',
            'action': 'set_owner'
        },
    },
    'reopen': {
        'closed': {
            'new_status': 'reopened',
            'action': 'del_resolution'
        }
    }
}

TASK_SCHEDULE_MODELS = ['EFFORT', 'LENGTH', 'DURATION']
TASK_SCHEDULE_CONSTRAINTS = ['NONE', 'START', 'END', 'BOTH']

TJP_WORKING_HOURS_TEMPLATE = """{% macro wh(wh, day) -%}
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
{{wh(workinghours, 'sun')}}"""

TJP_PROJECT_TEMPLATE = """project {{ project.tjp_id }} "{{ project.name }}" {{ project.start.date() }} - {{ project.end.date() }} {
    timingresolution {{ '%i'|format(project.timing_resolution.total_seconds()//60|int) }}min
    now {{ now }}
    dailyworkinghours {{ project.daily_working_hours }}
    weekstartsmonday
{{ project.working_hours.to_tjp }}
    timeformat "%Y-%m-%d"
    scenario plan "Plan"
    trackingscenario plan
}
"""

TJP_TASK_TEMPLATE = """task {{task.tjp_id}} "{{task.name}}" {
{%- if task.is_container -%}
    {%- for child_task in task.children %}
{{ child_task.to_tjp }}
    {%- endfor %}
{%- else %}
    {{defaults.TASK_SCHEDULE_MODELS[task.schedule_model].lower()}} {{task.schedule_timing_day}}d {{task.schedule_timing_hour}}h
    allocate {% for resource in task.resources -%}
        {%-if loop.index != 1 %}, {% endif %}{{resource.tjp_id}}
    {%- endfor %}
    {%- if task.depends %}
    depends {% for depends in task.depends %}
        {%- if loop.index != 1 %}, {% endif %}{{depends.tjp_abs_id}}
    {%- endfor -%}
    {%- endif -%}
{% endif %}
}
"""

TJP_DEPARTMENT_TEMPLATE = '''resource {{department.tjp_id}} "{{department.name}}" {
{%- for resource in department.users %}
    {{resource.to_tjp}}
{%- endfor %}
}'''

TJP_USER_TEMPLATE = '''resource {{user.tjp_id}} "{{user.name}}"'''

TJP_MAIN_TEMPLATE = """# Generated By Stalker v{{stalker.__version__}}
{{project.to_tjp}}

# resources
resource resources "Resources" {
{%- for user in users %}
    {{user.to_tjp}}
{%- endfor %}
}

# tasks
task {{project.tjp_id}} "{{project.name}}"{
    {% for task in project.root_tasks %}
    {{task.to_tjp}}
    {% endfor %}
}

# bookings

# reports
taskreport breakdown "{{csv_file_full_path}}"{
    formats csv
    timeformat "%Y-%m-%d-%H:%M"
    columns id, start, end
}
"""

TJ_COMMAND = '/usr/local/bin/tj3'
