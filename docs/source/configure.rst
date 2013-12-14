.. _configuration_toplevel:

.. _configuring_stalker:

Configuring Stalker
===================

To configure Stalker and make it fit to your Studios need you should use the
``config.py`` file as mentioned in next sections.

config.py File
--------------

Stalker uses the ``config.py`` to let one to customize the system config.

The ``config.py`` file is searched in a couple of places through the system:
    
  * under "~/.strc/" directory (not yet)
  * under "$STALKER_PATH"

The first path is a folder in the users home dir. The second one is a path
defined by the ``STALKER_PATH`` environment variable.

Defining the ``config.py`` by using the environment variable gives the most
customizable and consistent setup through the studio. You can set
``STALKER_PATH`` to a shared folder in your fileserver where all the users can
access.

Because, ``config.py`` is a regular Python code which is executed by
Stalker, you can do anything you were doing in a normal Python
script. This is very handy (also dangerous!) if you have another source of
information which is reachable by a Python script.

If there is no ``STALKER_PATH`` variable in your current environment or it is
not showing an existing path or there is no ``config.py`` file the system will
use the system defaults.

Config Variables
----------------

Variables which can be set in ``config.py`` are as follows:

.. confval:: actions

   Actions for authorization system. These are used to create ACLs. Stalker
   uses `CRUDL`_ system. Default value is::

     actions = ['Create', 'Read', 'Update', 'Delete', 'List'] #CRUDL

   .. _CRUDL: http://en.wikipedia.org/wiki/Create,_read,_update_and_delete

.. confval:: auto_create_admin

   Tells Stalker to create an admin by default. Default value is::

     auto_create_admin = True

.. confval:: admin_name

   The default admin user name. Default value is::

     admin_name = 'admin'

.. confval:: admin_login

   The default admin login. Default value is::

     admin_login = 'admin'

.. confval:: admin_password

   The default admin password. Default value is::

     admin_password = 'admin'

.. confval:: admin_email

   The default email for admin user. Default value is::

     admin_email = 'admin@admin.com'

.. confval:: admin_department_name

   The default department name for admin. Default value is::

     admin_department_name = 'admins'

.. confval:: admin_group_name

   The default admin permission group name. Default value is::

     admin_group_name = 'admins'

.. confval:: database_engine_settings

   A dictionary of config values. The default value is::

     database_engine_settings = {
         "sqlalchemy.url": "sqlite:///:memory:",
         "sqlalchemy.echo": False,
     }

.. confval:: database_session_settings
   
   This value is not used.

.. confval:: local_storage_path

   The local storage path for Stalker.

     local_storage_path = os.path.expanduser('~/.strc')   

.. confval:: local_session_data_file_name

   The per user or local session file name. It is used for storing logged in
   user info. The default value is::

     local_session_data_file_name = 'local_session_data'

.. confval:: server_side_storage_path

   Storage for uploaded files. This used by `Stalker Pyramid`_ and shows the
   server side storage path. Will be moved to Stalker Pyramid in later
   versions. Not used by Stalker by default. Default value is::

     server_side_storage_path = os.path.expanduser('~/Stalker_Storage')

   .. _`Stalker Pyramid`: https://pypi.python.org/pypi/stalker_pyramid

.. confval:: key

   The default keyword which is going to be used in password scrambling.
   Default value is::

     key = "stalker_default_key"

.. confval:: version_take_name

   The default take name for :class:`~stalker.models.version.Version`
   instances. Default value is::

     version_take_name = "Main"

.. confval:: status_bg_color

   Default background color for :class:`~stalker.models.status.Status`
   instances. Default value is::

     status_bg_color = 0xffffff

.. confval:: status_fg_color

   Default foreground color for :class:`~stalker.models.status.Status`
   instances. Default value is::

     status_fg_color = 0x000000
 
.. confval:: ticket_label

   Default ticket label. Used by :class:`~stalker.models.ticket.Ticket` when
   generating a ticket name. Default value is::

     ticket_label = "Ticket"

.. confval:: ticket_status_order

   Defines the ticket statuses and the order of them. Default value is::

     ticket_status_order = [
         'new', 'accepted', 'assigned', 'reopened', 'closed'
     ]

.. confval:: ticket_resolutions

   Defines the default ticket resolutions. Default value is::

     ticket_resolutions = [
         'fixed', 'invalid', 'wontfix', 'duplicate', 'worksforme', 'cantfix'
     ]

.. confval:: ticket_workflow

   Defines the default ticket workflow. It is a dictionary of actions. Shows
   the new status per action. Default value is::

     ticket_workflow = {
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

.. confval:: timing_resolution

   Defines the default timing resolution for classes which are mixed with
   :class:`~stalker.models.mixins.DateRangeMixin`\ . Stalker uses the
   TaskJuggler default timing resolution which is 1 hour::

     timing_resolution = datetime.timedelta(hours=1)

.. confval:: task_duration

   Defines the default task duration. If only a start or end value is entered
   for a :class:`~stalker.models.task.Task` then Stalker calculates the other
   value by adding or subtracting the default task duration value from it.
   Default value is 1 hour::

     task_duration = datetime.timedelta(hours=1)


.. confval:: task_priority

   Defines the default task priority. This is used by TaskJuggler to prioritize
   tasks. Should be a number between 0 and 1000. Default value is 500::

     task_priority = 500

.. confval:: working_hours

   Defines the default weekly working hours per week day. Stalker uses the
   TaskJuggler default value of 9am to 6pm. The values entered are minutes from
   midnight, and it is a list of lists of two integers. Each list of two
   integers shows a working hour interval. Default value is::

     working_hours = {
       'mon': [[540, 1080]], # 9:00 - 18:00
       'tue': [[540, 1080]], # 9:00 - 18:00
       'wed': [[540, 1080]], # 9:00 - 18:00
       'thu': [[540, 1080]], # 9:00 - 18:00
       'fri': [[540, 1080]], # 9:00 - 18:00
       'sat': [], # saturday off
       'sun': [], # sunday off
     }

.. confval:: daily_working_hours

   Defines the default daily working hour. This is strongly related with the
   ``working_hours``, ``weekly_working_hours``, ``weekly_working_days`` and
   ``yearly_working_days`` settings and shows a mean value of daily working
   hour. Default value is 9::

     daily_working_hours = 9

.. confval:: weekly_working_hours

   Defines the default weekly working hour. This is strongly related with the
   ``working_hours``, ``daily_working_hours``, ``weekly_working_days`` and
   ``yearly_working_days`` settings. Default value is 45::

     weekly_working_hours = 45

.. confval:: weekly_working_days

   Defines the default weekly working days. This is strongly related with the
   ``working_hours``, ``daily_working_hours``, ``weekly_working_hours`` and
   ``yearly_working_days`` settings. Default value is 5::

     weekly_working_days = 5

.. confval:: yearly_working_days

   Defines the default yearly working days. This is strongly related with the
   ``working_hours``, ``daily_working_hours``, ``weekly_working_hours`` and
   ``weekly_working_days`` settings. Default value is 260.714 which equals
   ``weekly_working_days`` * 52.1428::

     yearly_working_days = 260.714

.. confval:: day_order

   Defines the order of the week days. Default value uses European system::

     day_order = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

.. confval:: datetime_units

   Defines the date and time units. The order should match the
   ``datetime_unit_names`` setting. Default value is::

     datetime_units = ['min', 'h', 'd', 'w', 'm', 'y']

.. confval:: datetime_unit_names

   Defines the names of date and time units. The order should match the
   ``datetime_units`` setting. Default value is::

     datetime_unit_names = ['minute', 'hour', 'day', 'week', 'month', 'year']

.. confval:: datetime_units_to_timedelta_kwargs

   Defines the conversion ratios of each date and time unit. Default value is::

     datetime_units_to_timedelta_kwargs = {
         'min': {'name': 'minutes', 'multiplier': 1},
         'h'  : {'name': 'hours'  , 'multiplier': 1},
         'd'  : {'name': 'days'   , 'multiplier': 1},
         'w'  : {'name': 'weeks'  , 'multiplier': 1},
         'm'  : {'name': 'days'   , 'multiplier': 30},
         'y'  : {'name': 'days'   , 'multiplier': 365}
     }

.. confval:: task_schedule_models

   Defines the default schedule models. These are highly related with
   TaskJuggler, so anything entered here should exist in TaskJuggler. Default
   value is::

     task_schedule_models = ['effort', 'length', 'duration']

.. confval:: task_schedule_constraints

   Defines the default schedule constraints. The order also defines a binary
   number corresponding to each value (00: none, 01: start, 10:end, 11:both)
   and used in defining which side of a Task is constrained to a date. Also
   used by TaskJuggler to constrain the start or end or both dates of a task to
   a certain date. Also a Task with schedule_constraint is set to 2 (both) is
   considered a **duration** task even if its schedule_model is set to
   **effort** or **length**. Default value is::

     task_schedule_constraints = ['none', 'start', 'end', 'both']

.. confval:: tjp_working_hours_template

   Defines a Jinja2 template for converting
   :class:`~stalker.models.studio.WorkingHours` instances to a TaskJuggler
   compatible string. By default Stalker converts a WorkingHours instance to a
   ``workinghours`` statement in TaskJuggler. Default value is::

     tjp_working_hours_template = """{% macro wh(wh, day) -%}
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

.. confval:: tjp_studio_template

   Defines a Jinja2 template for converting a
   :class:`~stalker.models.studio.Studio` instance to a TaskJuggler compatible
   string. By default Stalker converts a Studio instance to a ``project``
   statement in TaskJuggler. Default value is::

     tjp_studio_template = """project {{ studio.tjp_id }} "{{ studio.name }}" {{ studio.start.date() }} - {{ studio.end.date() }} {
         timingresolution {{ '%i'|format((studio.timing_resolution.days * 86400 + studio.timing_resolution.seconds)//60|int) }}min
         now {{ studio.now.strftime('%Y-%m-%d-%H:%M') }}
         dailyworkinghours {{ studio.daily_working_hours }}
         weekstartsmonday
     {{ studio.working_hours.to_tjp }}
         timeformat "%Y-%m-%d"
         scenario plan "Plan"
         trackingscenario plan
     }
     """

.. confval:: tjp_project_template

   Defines a Jinja2 template for converting a
   :class:`~stalker.models.project.Project` instance to a TaskJuggler
   compatible string. By default Stalker converts a Project instance to a
   ``task`` statement in TaskJuggler. Default value is::

     tjp_project_template = """task {{project.tjp_id}} "{{project.name}}" {
         {% for task in project.root_tasks %}
             {{task.to_tjp}}
         {% endfor %}
     }
     """

.. confval:: tjp_task_template

   Defines a Jinja2 template for converting a
   :class:`~stalker.models.task.Task` instance to a TaskJuggler compatible
   string. By default Stalker converts a Task to a ``task`` statement in
   TaskJuggler. Default value is::

     tjp_task_template = """task {{task.tjp_id}} "{{task.name}}" {
     {% if task.priority != 500 -%}priority {{task.priority}}{%- endif %}
     {%- if task.depends %}
         depends {% for depends in task.depends %}
         {%- if loop.index != 1 %}, {% endif %}{{depends.tjp_abs_id}}
     {%- endfor -%}
     {%- endif -%}
     {%- if task.is_container -%}
         {%- for child_task in task.children %}
             {{ child_task.to_tjp }}
         {%- endfor %}
     {%- else %}
         {% if task.resources|length -%}
         {% if task.schedule_constraint %}
             {%- if task.schedule_constraint == 1 or task.schedule_constraint == 3 -%}
                 start {{ task.start.strftime('%Y-%m-%d-%H:%M') }}
             {%- endif %}
             {%- if task.schedule_constraint == 2 or task.schedule_constraint == 3 %}
                 end {{ task.end.strftime('%Y-%m-%d-%H:%M') }}
             {%- endif -%}
         {% endif %}
         {{task.schedule_model}} {{task.schedule_timing}}{{task.schedule_unit}}
         allocate {% for resource in task.resources -%}
             {%-if loop.index != 1 %}, {% endif %}{{resource.tjp_id}}{% endfor %}
         {%- endif -%}
         {% for time_log in task.time_logs %}
         booking {{time_log.resource.tjp_id}} {{time_log.start.strftime('%Y-%m-%d-%H:%M:%S')}} +{{'%i'|format(time_log.duration.days*24 + time_log.duration.seconds/3600)}}h { overtime 2 }
         {%- endfor -%}
     {% endif %}
     }
     """

.. confval:: tjp_department_template

   Defines a Jinja2 template for converting a
   :class:`~stalker.models.department.Department` instance to a TaskJuggler
   compatible string. By default Stalker converts a Department to a
   ``resource`` statement in TaskJuggler. Default value is::

     tjp_department_template = '''resource {{department.tjp_id}} "{{department.name}}" {
     {%- for resource in department.users %}
         {{resource.to_tjp}}
     {%- endfor %}
     }'''

.. confval:: tjp_vacation_template

   Defines a Jinja2 template for converting a
   :class:`~stalker.models.vacation.Vacation` instance to a TaskJuggler
   compatible string. By default Stalker converts a Vacation instance to a
   ``vacation`` statement in TaskJuggler. Default value is::

     tjp_vacation_template = '''vacation {{ vacation.start.strftime('%Y-%m-%d-%H:%M') }}, {{ vacation.end.strftime('%Y-%m-%d-%H:%M') }}'''

.. confval:: tjp_user_template

   Defines a Jinja2 template for converting a
   :class:`~stalker.models.auth.User` instance to a TaskJuggler ``resource``
   statement. Default value is::

     tjp_user_template = '''resource {{user.tjp_id}} "{{user.name}}"{% if user.vacations %} {
         {% for vacation in user.vacations -%}
             {{vacation.to_tjp}}
         {% endfor -%}
     }{% endif %}'''

.. confval:: tjp_main_template

   Defines a Jinja2 template for converting all the information coming from
   Stalker to a TaskJuggler compatible ``tjp`` file. Default value is::

     tjp_main_template = """# Generated By Stalker v{{stalker.__version__}}
     {{studio.to_tjp}}
     
     # resources
     resource resources "Resources" {
     {%- for user in studio.users %}
         {{user.to_tjp}}
     {%- endfor %}
     }
     
     # tasks
     {% for project in studio.active_projects %}
         {{project.to_tjp}}
     {% endfor %}
     
     # reports
     taskreport breakdown "{{csv_file_full_path}}"{
         formats csv
         timeformat "%Y-%m-%d-%H:%M"
         columns id, start, end
     }
     """

.. confval:: tj_command

   Defines the TaskJuggler command. Stalker uses this configuration value to
   call TaskJugglers ``tj3`` command.

     tj_command = '/usr/local/bin/tj3',

.. confval:: path_template

   Defines a default value for path template for
   :class:`~stalker.models.template.FilenameTemplate` instances to be used by
   :class:`~stalker.models.version.Version` instances. This value is not used
   yet. Default value is::

     path_template = '{{project.code}}/{%- for parent_task in parent_tasks -%}{{parent_task.nice_name}}/{%- endfor -%}'

.. confval:: filename_template

   Defines a default value for filename template for
   :class:`~stalker.models.template.FilenameTemplate` instances to be used by
   :class:`~stalker.models.version.Version` instances. This value is not used
   yet. Default value is::

     filename_template = '{{task.entity_type}}_{{task.id}}_{{version.take_name}}_v{{"%03d"|format(version.version_number)}}'

.. confval:: sequence_format

   Defines the default file sequence format to be used with `PySeq`_. This
   value is not used yet. Default value is::

     sequence_format = "%h%p%t %R"

   Fore details about the format see the `PySeq documentation`_.
   
   .. _PySeq: http://rsgalloway.github.com/pyseq/
   .. _PySeq documentation: http://rsgalloway.github.com/pyseq/

.. confval:: file_size_format

   Defines the default file size format to be used in UI. Default value is::

     file_size_format = "%.2f MB"

.. confval:: date_time_format

   Defines the default datetime format to be used in UI and string
   representations of datetime.datetime instances. Default value is::

     date_time_format = '%Y.%m.%d %H:%M'

.. confval:: resolution_presets

   Defines default resolution presets. This value is not used yet. Default
   value is::

     resolution_presets = {
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
     }

.. confval:: default_resolution_preset

   Defines the default resolution preset fro new Projects. This value is not
   used yet. Default value is::

     default_resolution_preset = "HD 1080"

.. confval:: project_structure

   Defines the default project structure. This value is not used by Stalker.
   Default value is::

     project_structure = """{% for shot in project.shots %}
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
     """

.. confval:: thumbnail_format

   Defines the default thumbnail format. This value is not used by Stalker.
   Default value is::

     thumbnail_format = "jpg"

.. confval:: thumbnail_quality

   Defines the default thumbnail quality. This value is not used by Stalker.
   Default value is::

     thumbnail_quality = 70

.. confval:: thumbnail_size
   
   Defines the defaul thumbnail size. This value is not used by Stalker.
   Default value is::

     thumbnail_size = [320, 180]
