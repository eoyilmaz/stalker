# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

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
TIME_RESOLUTION = datetime.timedelta(hours=1)
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

TJP_WORKING_HOURS_TEMPLATE = """{% macro wh(wh, day)
-%}{%
    if wh[day]|length
        %}workinghours {{day}} {%
        for part in wh[day]
            %}{%
            if loop.index != 1
                %}, {%
            endif
            %}{{"%02d"|format(part[0]//60)}}:{{"%02d"|format(part[0]%60)}} - {{"%02d"|format(part[1]//60)}}:{{"%02d"|format(part[1]%60)}}{%
        endfor
        %}{%
    else
        %}workinghours {{day}} off{%
    endif %}{%-
endmacro
%}{{wh(workinghours, 'mon')}}
{{wh(workinghours, 'tue')}}
{{wh(workinghours, 'wed')}}
{{wh(workinghours, 'thu')}}
{{wh(workinghours, 'fri')}}
{{wh(workinghours, 'sat')}}
{{wh(workinghours, 'sun')}}"""

TJP_PROJECT_TEMPLATE = """project {{ project.code }} "{{ project.name }}" {{ project.start }} {{ project.end }} {
    now {{ now }}
    dailyworkinghours {{ project.daily_working_hours }}
    weekstartsmonday
    {{ project.working_hours.to_tjp }}
    timeformat "%Y-%m-%d"
    scenario plan "Plan"
    trackingscenario plan
}
"""

TJP_TASK_TEMPLATE = """task {{task.code}} "{{task.name}}"{
    {% if task.is_container %}
        {% for child_task in task.children %}
            {{ child_task.to_tjp }}
        {% endfor %}
    {% else %}
        effort {{task.effort}}h
        {% for resource in task.resources %}
        allocate resource
        {% endfor %}
        {% for depends in task.depends %}
        depends {{depends.tjp_id}}
        {% endfor %}
    {% endif %}
}
"""

TJP_DEPARTMENT_TEMPLATE = '''resource {{department.tjp_id}} "{{department.name}}" { {%
for resource in department.users %}
    {{resource.to_tjp}}{%
endfor %}
}'''

TJP_USER_TEMPLATE = '''resource {{user.login}} "{{user.name}}"'''

TJP_MAIN_TEMPLATE = """# Generated By Stalker v{{stalker.version}}
{{project.to_tjp}}

resource resources "Resources" {
    {% for department in departments %}
        {{department.to_tjp}}
    {% endfor %}
    # list users with no departments
    
    resource no_dep "No Departments" {
        {% for user in no_dep_users %}
            {{user.to_tjp}}
        {% endfor %}
    }
}

task {{project.code}} "{{project.name}}"{
    {% for task in project.tasks %}
    {{task.tjp}}
    {% endfor %}
}
"""
