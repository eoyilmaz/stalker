===============
Stalker Changes
===============

1.0.0
=====

* `Version.take_name` has been renamed to `Version.variant_name` to follow the
  industry standard (and then removed it completely as we now have `Variant`
  class for this).
* `Task.depends` renamed to `Task.depends_on`.
* `TaskDependency.task_depends_to` renamed to `TaskDependency.task_depends_on`.
* Modernized Stalker as a Python project. It is now fully PEP 517 compliant.
* Stalker now supports Python versions from 3.8 to 3.13.
* Stalker is now SQLAlchemy 2.x compliant.
* Stalker is now fully type hinted.
* Added GitHub actions for CI/CD practices.
* Updated validation messages to make them more consistently displaying the
  current type and the value of the validated attribute.
* Added Makefile workflow to help creating a virtualenv, building, installing,
  releasing etc. actions much more easier.
* Added `tox` config to run the test with Python 3.8 to 3.13.
* Increased test coverage to 99.76%.
* Updated documentation theme to `furo`.
* Renamed `OSX` to `macOS` where ever it is mentioned.
* `Scene` is now deriving from `Task`.
* `Shot.sequences` is now `Shot.sequence` and it is many-to-one.
* `Shot.scenes` is now `Shot.scene` and it is many-to-one.
* Added the `Variant` class to allow variants to be approved and managed
  individually.
* Added `Review.version` attribute to relate a `Version` instance to the
  review.
* Removed the `Version.variant_name` attribute. The migration alembic script
  will create `Variant` instances for each `Version.variant_name` under the
  container `Task` to hold the information.
* `Version._template_variables()` now finds the related `Asset`, `Shot` and
  `Sequence` values and passes them in the returned dictionary.
* All the enum values handled with arbitrary string lists or integer values are
  now proper enum classes. As a result we now have `ScheduleConstraint`,
  `TimeUnit`, `ScheduleModel`, `DependencyTarget`, `TraversalDirection`
  enum classes which are removing the need of using fiddly strings as enum
  values.
* `StatusList`s that are created for super classes can now be used with the
  derived classes, i.e. a status list created specifically for `Task` can now
  be used with `Asset`, `Shot`, `Sequence` and `Scenes` and any future `Task`
  derivatives.

0.2.27
======

* Fixed a bug in ``Task.responsible`` attribute. This change has also slightly
  changed how the ``Task.responsible`` attribute works. It still comes from the
  parent if the ``Task.responsible`` is empty or None, but when queried it
  causes the attribute to be filled with parent data. This is a slight change,
  but may break some workflows.

* Added ``ScheduleMixin.to_unit`` that converts the given ``seconds`` to the
  given ``unit`` in consideration of the given ``schedule_model``.

0.2.26
======

* ``Task.percent_complete`` value is now properly calculated for a parent Task
  that contains a mixed type of "effort", "duration" and "length" based tasks.

0.2.25.1
========

* **Update:** Updated the ``.travis.yml`` file to use PostgreSQL 13.3 and
  Ubuntu 20.04 Focal Fossa.
* **Update:** Updated the ``upload_to_pypi`` command to follow the current
  Python packaging guide.
* **Update:** Migrated from ``TravisCI.org`` to ``TravisCI.com``.
* **Update:** Re-enabled concurrent testing in ``.travis.yml``.

0.2.25
======

* **Update:** Stalker is now compatible with SQLAlchemy 1.4,
  psycopg2-binary 2.86 and Python 3.9+. But more work still needs to be done to
  make it SQLAlchemy 2.0 compatible.

0.2.24.3
========

This release is again mainly related to fixing failing tests.

0.2.24.2
========

This release is mainly related to cleaning up some complains that arose while
testing the library.

* **Fix:** Fixed two tests which are testing the ``stalker.db`` module to
  check the system against the correct Alembic revision id.

* **Update:** Removed the unnecessary ``pytest.skip`` commands in the
  ``Repository`` class tests which were shipping the tests if the OS is not
  Windows. But they should work fine under all OSes.

* **Update:** Updated all class documentation and removed the cancellation
  character (which was apparently not good for PEP8)

* **Fix:** Fixed some warnings about some regular expressions.


0.2.24.1
========

* **Fix:** Fixed ``stalker.db`` module to check for the correct Alembic
  revision id.


0.2.24
======

* **New:** ``Repository`` instances now have a ``code`` attribute which is
  used for generating the environment variables where in previous versions the
  ``id`` attribute has been used which caused difficulties in transferring the
  data to a different installation of Stalker. Also to make the system
  backwards compatible, Stalker will still set the old ``id`` based environment
  variables. But when asked for an environment variable it will return the
  ``code`` based one. The ``code`` argument as usual has to be initialized on
  ``Repository`` instance creation. That's why this version is slightly
  backwards incompatible and needs the database to be updated with Alembic
  (with the command ``alembic update head``).

* **Fix:** ``Repository`` methods ``is_in_repo`` and ``find_repo`` are now case
  insensitive for Windows paths.

* **Update:** Updated ``Project`` class documentation and included information
  about what is going to be deleted or how the delete operation will be
  cascaded when a ``Project`` instance is deleted.

0.2.23
======

* **Update:** Updated the ``setup.py`` to require ``psycopg2-binary`` instead
  of ``psycopg2``. Also updated the configuration files for Docker and Travis.
  This changes the requirement of psycopg2 to psycopg2-binary, which will make
  it easier to get the installation to complete on e.g. CentOS 7 without
  requiring pg_config.

0.2.22
======

* **Fix:** Fixed ``TaskJugglerScheduler.schedule()`` method to correctly decode
  byte data from ``sys.stderr`` to string for Python 3.x.

* **Fix:** Fixed a couple of tests for TaskJuggler.

* **Update:** Updated Classifiers information in ``setup.py``, removed Python
  versions 2.6, 3.0, 3.1 and 3.2 from supported Python versions.

* **Fix:** Removed Python 3.3 from TravisCI build which is not supported by
  ``pytest`` apparently.

* **Update:** Updated TravisCI config and removed Python 2.6 and added Python
  3.6.

* **Update:** Added a test case for an edge usage of FilenameTemplate.

* **Update:** Updated .gitignore file to ignore PyTest cache folder.

* **Update:** Updated the License file to correctly reflect the project license
  of LGPLv3.

* **Update:** Update copyright information.

* **New:** Created ``make_html.bat`` for Windows.

* **New:** Added support for Python wheel.


0.2.21
======

* **New:** Switched from ``nose`` + ``unittest`` to ``pytest`` as the main
  testing framework (with ``pytest-xdist`` tests complete 4x faster).

* **New:** Added ``DBSession.save()`` shortcut method for convenience which
  does an ``add`` or ``add_all`` (depending to the input) followed by a
  ``commit`` at once.

* **Update:** Updated the about page for a more appealing introduction to the
  library.

* **New:** Stalker now creates default ``StatusList`` for ``Project`` instances
  on database initialization.

* **Update:** SQLite3 support is back. In fact it was newer gone. For
  simplicity of first time users the default database is again SQLite3. It was
  dropped for the sake of adding more PostgreSQL oriented features. But then it
  is recognized that the system can handle both. Though a two new Variant had
  to be created for JSON and Datetime columns.

* **Update:** With the reintroduction of SQLite3, the new JSON type column in
  ``WorkingHours`` class has been upgraded to support SQLite3. So with SQLite3
  the column stores the data as TEXT but seamlessly convert them to JSON when
  ORM loads or commits the data.

* **New:** Added ``ConfigBase`` as a base class for ``Config`` to let it be
  used in other config classes.

* **Fix:** Fixed ``testing.create_db()`` and ``testing.drop_db()`` to fallback
  to ``subprocess.check_call`` method for Python 2.6.

* **Fix:** Fixed ``stalker.models.auth.User._validate_password()`` method to
  work with Python 2.6.

* **Update:** Updated all of the tests to use ``pytest`` style assertions to
  support Python 2.6 along with 2.7 and 3.0+.

* **Fix:** Fixed ``stalker.db.check_alembic_version()`` function to invalidate
  the connection, so it is not possible to continue with the current session,
  preventing users to ignore the raised ``ValueError`` when the
  ``alembic_version`` of the database is not matching the ``alembic_version``
  of Stalker's current version.


0.2.20
======

* **New:** Added ``goods`` attribute to the ``Client`` class. To allow special
  priced ``Goods`` to be created for individual clients.

* **Fix:** The ``WorkingHours`` class is now derived from ``Entity`` thus it is
  not stored in a ``PickleType`` column in ``Studio`` anymore. (issue: #44)

* **Update:** Updated ``appveyor.yml`` to match ``travis.yml``.


0.2.19
======

* **Update:** Updated the ``stalker.config.Config.database_engine_settings`` to
  point the test database.

* **Fix:** Fixed a bug in ``stalker.testing.UnitTestDBBase.setUp()`` where it
  was not considering the existence of the ``STALKER_PATH`` environment
  variable while doing the tests.

* **Update:** Removed debug message from ``db.setup()`` which was revealing the
  database password.

* **Update:** Updated the ``UnitTestDBBase``, it now creates its own test
  database, which allows all the tests to run in an individual database. Thus,
  the tests can now be run in ``multiprocess`` mode which speeds things a lot.

* **Fix:** Removed any module level imports of ``stalker.defaults`` variable,
  which can be changed by a Studio (or by tests) and should always be
  refreshed.

* **Update:** Removed the module level import of the
  ``stalker.db.session.DBSession`` in ``stalker.db``, so it is not possible to
  use ``db.DBSession`` anymore.

* **Update:** The import statements that imports ``stalker.defaults`` moved to
  local scopes to allow runtime changes to the ``defaults`` to be reflected
  correctly.

* **Update:** Added Python fall back mode to
  ``stalker.shot.Shot._check_code_availability()`` which runs when there is no
  database.

* **Update:** ``stalker.models.task.TimeLog._validate_task()`` is now getting
  the ``Status`` instances from the ``StatusList`` that is attached to the
  ``Task`` instance instead of doing a database query.

* **Update:** ``stalker.models.task.TimeLog._validate_resource()`` is now
  falling back to a Python implementation if there is no database connection.

* **Update:** ``stalker.models.task.Task._total_logged_seconds_getter()`` is
  now hundreds of times faster when there is a lot of ``TimeLog`` instances
  attached to the ``Task``.

* **Update:** In ``stalker.models.task.Task`` class, methods those were doing a
  database query to get the required ``Status`` instances are now using the
  attached ``StatusList`` instance to get them.

* **Fix:** A possible ``auto_flush`` is prevented in ``Ticket`` class.

* **Update:** ``Version.latest_version`` property is now able to fall back to a
  pure Python implementation when there is no database connection.

* **Update:** The default log level has been increased from ``DEBUG`` to
  ``INFO``.

* **Update:** In an attempt to speed up tests, a lot of tests that doesn't need
  an active Database has been updated to use the regular ``unittest.TestCase``
  instead of ``stalker.testing.TestBase`` and as a result running all of the
  tests are now 2x faster.

* **Fix:** ``TimeLogs`` are now correctly reflected in UTC in a tj3 file.

* **Fix:** Fixed a lot of tests which were raising Warnings and surprisingly
  considered as Errors in TravisCI.

* **Fix:** ``to_tjp`` methods of SOM classes that is printing a Datetime object
  are now printing the dates in UTC.

* **Fix:** Fixed ``stalker.models.auth.Permission`` to be hashable for Python
  3.

* **Fix:** Fixed ``stalker.models.auth.AuthenticationLog`` to be sortable for
  Python 3.

* **Fix:** Fixed ``stalker.models.version.Version.latest_version`` property for
  Python 3.

* **Fix:** Fixed tests of ``Permission`` class to check for correct exception
  messages in Python 3.

* **Update:** Replaced the ``assertEquals`` and ``assertNotEquals`` calls which
  are deprecated in Python 3 with ``assertEqual`` and ``assertNotEquals`` calls
  respectively.

* **Fix:** Fixed tests for ``User`` and ``Version`` classes to not to cause the
  ``id column is None`` warnings of SQLAlchemy to be emitted.


0.2.18
======

* **Update:** Support for DB backends other than Postgresql has been dropped.
  This is done to greatly benefit from a code that is highly optimized only
  for one DB backend. With This all of the tests should be inherited from the
  ``stalker.tests.UnitTestDBBase`` class.

* **New:** All the DateTime fields in Stalker are now TimeZone aware and
  Stalker stores the DateTime values in UTC. Naive datetime values are not
  supported anymore. You should use a library like ``pytz`` to supply timezone
  information as shown below::

    import datetime
    import pytz
    from stalker import db, SimpleEntity
    new_simple_entity = SimpleEntity(
        name='New Simple Entity',
        date_created = datetime.datetime.now(tzinfo=pytz.utc)
    )

* **Fix:** The default values for ``date_created`` and ``date_updated`` has now
  been properly set to a partial function that returns the current time.

* **Fix:** Previously it was possible to enter two TimeLogs for the same
  resource in the same datetime range by committing the data from two different
  sessions simultaneously. Thus the database was not aware that it should
  prevent that. Now with the new PostgreSQL only implementation and the
  ``ExcludeConstraint`` of PostgreSQL an ``IntegrityError`` is raised by the
  database backend when something like that happens.

* **Update:** All the tests those are checking the system against an Exception
  is being raised or not are now checking also the exception message.

* **Update:** In the ``TimeLog`` class, the raised ``OverBookedException``
  message has now been made clear by adding the start and end date values of
  the clashing TimeLog instance.

* **Update:** Removed the unnecessary ``computed_start`` and ``computed_end``
  columns from ``Task`` class, which are already defined in the
  ``DateRangeMixin`` which is a super for the Task class.

0.2.17.6
========

* **Fix:** Fixed a bug in ``ProjectMixin`` where a proper cascade was not
  defined and the ``Delete`` operations to the ``Projects`` table were not
  cascaded to the mixed-in classes properly.

0.2.17.5
========

* **Fix:** Fixed the ``image_format`` attribute implementation in ``Shot``
  class. Now it will not copy the value of ``Project.image_format`` directly on
  ``__init__`` but instead will only store the value if the ``image_format``
  argument in ``__init__`` or ``Shot.image_format`` attribute is set to
  something.

0.2.17.4
========

* **Update:** Updated the comment sections of all of the source files to
  correctly show that Stalker is LGPL v3 (not v2.1).

0.2.17.3
========

* **New:** Added ``Shot.fps`` attribute to hold the fps information per shot.
* **Update:** Added the necessary alembic revision to reflect the changes in
  the ``Version_Inputs`` table.

0.2.17.2
========

* **Fix:** Fixed ``Version_Inputs`` table to correctly take care of
  ``DELETE``s on the ``Versions`` table. So now it is possible to delete a
  ``Version`` instance without first cleaning the ``Link`` instances that is
  related to that ``Version`` instance.

* **Update:** Changed the ``id`` attribute name from ``info_id`` to ``log_id``
  in ``AuthenticationLog`` class.

* **Update:** Started moving towards PostgreSQL only implementation. Merged the
  ``DatabaseModelTester`` class and ``DatabaseModelsPostgreSQLTester`` class.

* **Fix:** Fixed an autoflush issue in
  ``stalker.models.review.Review.finalize_review_set()``.

0.2.17.1
========

* **Fix:** Fixed alembic revision

0.2.17
======

* **New:** Added ``AuthenticationLog`` class to hold user login/logout info.
* **New:** Added ``stalker.testing`` module to simplify testing setup.

0.2.16.4
========

* **Fix:** Fixed alembic revision.

0.2.16.3
========

* **New:** ``ProjectUser`` now also holds a new field called ``rate``. The
  default value is equal to the ``ProjectUser.user.rate``. It is a way to hold
  the rate of a user on a specific project.

* **New:** Added the ``Invoice`` class.

* **New:** Added the ``Payment`` class.

* **New:** Added two simple mixins ``AmountMixin`` and ``UnitMixin``.

* **Update:** ``Good`` class is now mixed in with the new ``UnitMixin`` class.

* **Update:** ``BudgetEntry`` class is now mixed in with the new
  ``AmountMixin`` and ``UnitMixin`` classes.

0.2.16.2
========

* **New:** ``Group`` permissions can now be set on ``__init__()`` with the
  ``permissions`` argument.

0.2.16.1
========

* **Fix:** As usual after a new release that changes database schema, fixed the
  corresponding Alembic revision (92257ba439e1).

0.2.16
======

* **New:** ``Budget`` instances are now statusable.

* **Update:** Updated documentation to include database migration instructions
  with Alembic.

0.2.15.2
========

* **Fix:** Fixed a typo in the error message in
  ``User._validate_email_format()`` method.

* **Fix:** Fixed a query-invoked auto-flush problem in
  ``Task.update_parent_statuses()`` method.

0.2.15.1
========

* **Fix:** Fixed alembic revision (f2005d1fbadc), it will now drop any existing
  constraints before re-creating them. And the downgrade function will not
  remove the constraints.

0.2.15
======

* **New:** ``db.setup()`` now checks for ``alembic_version`` before setting up
  a connection to the database and raises a ``ValueError`` if the database
  alembic version is not matching the current implementation of Stalker.

* **Fix:** ``db.init()`` sets the ``created_by`` and ``updated_by``
  attributes to ``admin`` user if there is one while creating entity statuses.

* **New:** Created ``create_sdist.cmd`` and ``upload_to_pypi.cmd`` for Windows.

* **New:** ``Project`` to ``Client`` relation is now a many-to-many relation,
  thus it is possible to set multiple Clients for each project with each client
  having their own roles in a specific project.

* **Update:** ``ScheduleMixin.schedule_timing`` attribute is now Nullable.

* **Update:** ``ScheduleMixin.schedule_unit`` attribute is now Nullable.

0.2.14
======

* **Fix:** Fixed ``Task.path`` to always return a path with forward slashes.

* **New:** Introducing ``EntityGroups`` that lets one to group a bunch of
  ``SimpleEntity`` instances together, it can be used in grouping tasks even if
  they are in different places on the project task hierarchy or even in
  different projects.

* **Update:** ``Task.percent_complete`` is now correctly calculated for a
  ``Duration`` based task by using the ``Task.start`` and ``Task.end``
  attribute values.

* **Fix:** Fixed ``stalker.models.task.update_time_log_task_parents_for_end()``
  event to work with SQLAlchemy v1.0.

* **New:** Added an option called ``__dag_cascade__`` to the ``DAGMixin`` to
  control cascades on mixed in class. The default value is "all, delete".
  Change it to "save-update, merge" if you don't want the children also be
  deleted when the parent is deleted.

* **Fix:** Fixed a bug in ``Version`` class that occurs when a version instance
  that is a parent of other version instances is deleted, the child versions
  are also deleted (fixed through DAGMixin class).

0.2.13.3
========

* **Fix:** Fixed a bug in ``Review.finalize_review_set()`` for tasks that are
  sent to review and still have some extra time were not clamped to their total
  logged seconds when the review set is all approved.

0.2.13.2
========

* **New:** Removed ``msrp``, ``cost`` and ``unit`` arguments from
  ``BudgetEntry.__init__()`` and added a new ``good`` argument to get all of
  the data from the related ``Good`` instance. But the ``msrp``, ``cost`` and
  ``unit`` attributes of ``BudgetEntry`` class are still there to store the
  values that may not correlate with the related ``Good`` in future.

0.2.13.1
========

* **Fix:** Fixed a bug in ``Review.finalize_review_set()`` which causes Task
  instances to not to get any status update if the revised task is a second
  degree dependee to that particular task.

0.2.13
======

* **New:** ``Project`` instances can now have multiple repositories. Thus the
  ``repository`` attribute is renamed to ``repositories``. And the order of the
  items in the ``repositories`` attribute is restored correctly.

* **New:** ``stalker.db.init()`` now automatically creates environment
  variables for each repository in the database.

* **New:** Added a new ``after_insert`` which listens ``Repository`` instance
  ``insert`` instances to automatically add environment variables for the newly
  inserted repositories.

* **Update:** ``Repository.make_relative()`` now handles paths with environment
  variables.

* **Fix:** Fixed ``TaskJugglerScheduler`` to correctly generate task absolute
  paths for PostgreSQL DB.

* **New:** ``Repository.path`` is now writable and sets the correct path
  (``linux_path``, ``windows_path``, or ``osx_path``) according to the current
  system.

* **New:** Setting either of the ``Repository.path``,
  ``Repository.linux_path``, ``Repository.windows_path``,
  ``Repository.osx_path`` attributes will update the related environment
  variable if the system and attribute are matching to each other, setting the
  ``linux_path`` on Linux or setting the ``windows_path`` on Windows or setting
  the ``osx_path`` on OSX will update the environment variable.

* **New:** Added ``Task.good`` attribute to easily connect tasks to ``Good``
  instances.

* **New:** Added new methods to ``Repository`` to help managing paths:

  * ``Repository.find_repo()`` to find a repo from a given path. This is a
    class method so it can be directly used with the Repository class.
  * ``Repository.to_os_independent_path()`` to convert the given path to a OS
    independent path which uses environment variables. Again this is a class
    method too so it can be directly used with the Repository class.
  * ``Repository.env_var`` a new property that returns the related environment
    variable name of a repo instance. This is an instance property::

    .. code=block:: python

      # with default settings
      repo  = Repository(...)
      repo.env_var  # should print something like "REPO131" which will be used
      #               in paths as "$REPO131"

* **Fix:** Fixed ``User.company_role`` attribute which is a relationship to
  the ``ClienUser`` to cascade ``all, delete-orphan`` to prevent
  AssertionErrors when a Client instance is removed from the ``User.companies``
  collection.

0.2.12.1
========

* **Update:** ``Version`` class is now mixed with the ``DAGMixin``, so all the
  parent/child relation is coming from the DAGMixin.

* **Update:** ``DAGMixin.walk_hierarchy()`` is updated to walk the hierarchy in
  ``Depth First`` mode by default (method=0) instead of ``Breadth First`` mode
  (method=1).

* **Fix:** Fixed ``alembic_revision`` on database initialization.

0.2.12
======

* **Fix:** Fixed importing of ``ProjectUser`` directly from ``stalker``
  namespace.

* **Fix:** Fixed importing of ``ClientUser`` directly from ``stalker``
  namespace.

* **New:** Added two new columns to the ``BudgetEntry`` class to allow more
  detailed info to be hold.

* **New:** Added a new Mixin called ``DAGMixin`` to create parent/child
  relation between mixed in class.

* **Update:** The ``Task`` class is now mixed with the ``DAGMixin``, so all the
  parent/child relation is coming from the DAGMixin.

* **New:** Added a new class called ``Good`` to hold details about the
  commercial items/services sold in the Studio.

* **New:** Added a new class called ``PriceList`` to create price lists from
  Goods.

0.2.11
======

* **New:** User instances now have a new attribute called ``rate`` to track
  their cost as a resource.

* **New:** Added two new classes called ``Budget`` and ``BudgetEntry`` to
  record Project budgets in a simple way.

* **New:** Added a new class called **Role** to manage user roles in different
  Departments, Clients and Projects.

* **New:** User and Department relation is updated to include the role of the
  user in that department in a more flexible way by using the newly introduced
  Role class and some association proxy tricks.

* **New:** Also updated the User to Project relation to include the role of the
  user in that Project by using an associated Role class.

* **Update:** Department.members attribute is renamed to **users** (and removed
  the *synonym* property).

* **Update:** Removed ``Project.lead`` attribute use ``Role`` instead.

* **Update:** Removed ``Department.lead`` attribute use ``Role`` instead.

* **Update:** Because the ``Project.lead`` attribute is removed, it is now
  possible to have tasks with no responsible.

* **Update:** Client to User relation is updated to use an association proxy
  which makes it possible to set a Role for each User for each Client it is
  assigned to.

* **Update:** Renamed User.company to User.companies as the relation is now
  able to handle more than one Client instances for the User company.

* **Update:** Task Status Workflow has been updated to convert the status of a
  DREV task to HREV instead of WIP when the dependent tasks has been set to
  CMPL. Also the timing of the task is expanded by the value of
  ``stalker.defaults.timing_resolution`` if it doesn't have any effort left
  (generally true for CMPL tasks) to allow the resource to review and decide if
  he/she needs more time to do any update on the task and also give a chance of
  setting the Task status to WIP by creating a time log.

* **New:** It is now possible to schedule only a desired set of projects by
  passing a **projects** argument to the TaskJugglerScheduler.

* **New:** Task.request_review() and Review.finalize() will not cap the timing
  of the task until it is approved and also Review.finalize() will extend the
  timing of the task if the total timing of the given revisions are not fitting
  in to the left timing.

0.2.10.5
========

* **Update:** TaskJuggler output is now written to debug output once per line.

0.2.10.4
========

* **New:** '@' character is now allowed in Entity nice name.

0.2.10.3
========

* **New:** '@' character is now allowed in Version take names.

0.2.10.2
========

* **Fix:** Fixed a bug in
  ``stalker.models.schedulers.TaskJugglerScheduler._create_tjp_file_content()``
  caused by non-ascii task names.

* **Fix:** Removed the residual ``RootFactory`` class reference from
  documentation.

* **New:** Added to new functions called ``utc_to_local`` and ``local_to_utc``
  for UTC to Local time and vice versa conversion.

0.2.10.1
========

* **Fix:** Fixed a bug where for a WIP Task with no time logs (apparently
  something went wrong) and no dependencies using
  ``Task.update_status_with_dependent_statuses()`` will convert the status to
  RTS.

0.2.10
======

* **New:** It is now possible to track the Edit information per Shot using the
  newly introduced ``source_in``, ``source_out`` and ``record_in`` along with
  existent ``cut_in`` and ``cut_out`` attributes.

0.2.9.2
=======

* **Fix:** Fixed MySQL initialization problem in ``stalker.db.init()``.

0.2.9.1
=======

* **New:** As usual, after a new release, fixed a bug in
  ``stalker.db.create_entity_statuses()`` caused by the behavioral change of
  the ``map`` built-in function in Python 3.

0.2.9
=====

* **New:** Added a new class called ``Daily`` which will help managing
  ``Version`` outputs (Link instances including Versions itself) as a group.

* **New:** Added a new status list for ``Daily`` class which contains two
  statuses called "Open" and "Closed".

* **Update:** Setting the ``Version.take_name`` to a value other than a string
  will now raise a ``TypeError``.

0.2.8.4
=======

* **Fix:** Fixed ``SimpleEntity._validate_name()`` method for unicode strings.

0.2.8.3
=======

* **Fix:** Fixed str/unicode errors due to the code written for Python3
  compatibility.

* **Update:** Removed ``Task.is_complete`` attribute. Use the status "CMPL"
  instead of this attribute.

0.2.8.2
=======

* **Fix:** Fixed ``stalker.db.create_alembic_table()`` again to prevent extra
  row insertion.

0.2.8.1.1
=========

* **Fix:** Fixed ``stalker.db.create_alembic_table()`` function to handle the
  situation where the table is already created.

0.2.8.1
=======

* **Fix:** Fixed ``stalker.db.create_alembic_table()`` function, it is not
  using the ``alembic`` library anymore to create the ``alembic_version``
  table, which was the proper way of doing it but it created a lot of problems
  when Stalker is installed as a package.

0.2.8
=====

* **Update:** Stalker is now Python3 compatible.

* **New:** Added a new class called ``Client`` which can be used to track down
  information about the clients of ``Projects``. Also added ``Project.client``
  and ``User.company`` attributes which are referencing a Client instance
  allowing to add clients as normal users.

* **New:** ``db.init()`` now creates ``alembic_version`` table and stamps the
  most recent version number to that table allowing newly initialized databases
  to be considered in head revision.

* **Fix:** Fixed ``Version._format_take_name()`` method. It is now possible to
  use multiple underscore characters in ``Version.take_name`` attribute.

0.2.7.6
=======

* **Update:** Removed ``TimeLog._expand_task_schedule_timing()`` method which
  was automatically adjusting the ``schedule_timing`` and ``schedule_unit`` of
  a Task to total duration of the TimeLogs of that particular task, thus
  increasing the schedule info with the entered time logs.

  But it was setting the ``schedule_timing`` to 0 in some certain cases and it
  was unnecessary because the main purpose of this method was to prevent
  TaskJuggler to raise any errors related to the inconsistencies between the
  schedule values and the duration of TimeLogs and TaskJuggler has never given
  a real error about that situation.

0.2.7.5
=======

* **Fix:** Fixed Task parent/child relationship, previously setting the parent
  of a task to None was cascading a delete operation due to the
  "all, delete-orphan" setting of the Task parent/child relationship, this is
  updated to be "all, delete" and it is now safe to set the parent to None
  without causing the task to be deleted.

0.2.7.4
=======

* **Fix:** Fixed the following columns column type from String to Text:

    * Permissions.class_name
    * SimpleEntities.description
    * Links.full_path
    * Structures.custom_template
    * FilenameTemplates.path
    * FilenameTemplates.filename
    * Tickets.summary
    * Wiki.title
    * Wiki.content

  and specified a size for the following columns:

    * SimpleEntities.html_class -> String(32)
    * SimpleEntities.html_style -> String(32)
    * FilenameTemplates.target_entity_type -> String(32)

  to be compatible with MySQL.

* **Update:** It is now possible to create TimeLog instances for a Task with
  PREV status.

0.2.7.3
=======

* **Fix:** Fixed ``Task.update_status_with_dependent_statuses()`` method for a
  Task where there is no dependency but the status is DREV. Now calling
  ``Task.update_status_with_dependent_statuses()`` will set the status to RTS
  if there is no ``TimeLog`` for that task and will set the status to WIP if
  the task has time logs.

0.2.7.2
=======

* **Update:** ``TaskJugglerScheduler`` is now 466x faster when dumping all the
  data to TJP file. So with this new update it is taking only 1.5 seconds to
  dump ~20k tasks to a valid TJP file where it was around ~10 minutes in
  previous implementation. The speed enhancements is available only to
  PostgreSQL dialect for now.

0.2.7.1
=======

* **Fix:** Fixed TimeLog output in one line per task in ``Task.to_tjp()``.

* **New:** Added ``TaskJugglerScheduler`` now accepts a new argument called
  ``compute_resources`` which when set to True will also consider
  `Task.alternative_resources` attribute and will fill
  ``Task.computed_resources`` attribute for each Task. With
  ``TaskJugglerScheduler`` when the total number of Task is around 15k it will
  take around 7 minutes to generate this data, so by default it is set to
  False.

0.2.7
=====

* **New:** Added ``efficiency`` attribute to ``User`` class. See User
  documentation for more info.

0.2.6.14
========

* **Fix:** Fixed an **autoflush** problem in ``Studio.schedule()`` method.

0.2.6.13
========

* **New:** Added ``Repository.make_relative()`` method, which makes the given
  path to relative to the repository root. It considers that the path is
  already in the repository. So for now, be careful about not to pass a path
  outside of the repository.

0.2.6.12
========

* **Update:** ``TaskJugglerScheduler.schedule()`` method now uses the
  ``Studio.start`` and ``Studio.end`` values for the scheduling range instead
  of the hardcoded dates.

0.2.6.11
========

* **Update:** ``Task.create_time_log()`` method now returns the created
  ``TimeLog`` instance.

0.2.6.10
========

* **Fix:** Fixed an ``autoflush`` issue in
  ``Task.update_status_with_children_statuses()`` method.

0.2.6.9
=======

* **Update:** ``Studio.is_scheduling`` and ``Studio.is_scheduling_by``
  attributes will not be updated or checked at the beginning of the
  ``Studio.schedule()`` method. It is the duty of the user to check those
  attributes before calling ``Studio.schedule()``. This is done in this way
  because without being able to do a db commit inside ``Studio.schedule()``
  method (which is the case with transaction managers which may be used in web
  applications like **Stalker Pyramid**) it is not possible to persist and thus
  use those variables. So, to be able to use those attributes meaningfully the
  user should set them. Those variables will be set to False and None
  accordingly by the ``Studio.schedule()`` method after the scheduling is done.

0.2.6.8
=======

* **Fix:** Fixed a deadlock in ``TaskJugglerScheduler.schedule()`` method
  related with the ``Popen.stderr.readlines()`` blocking the TaskJuggler
  process without being able to read the output buffer.

0.2.6.7
=======

* **Update:** ``TaskJugglerScheduler.schedule()`` is now using bulk inserts and
  updates which is way faster than doing it with pure Python. Use
  ``parsing_method`` (0: SQL, 1: Python) to choose between SQL or Pure Python
  implementation. Also updated ``Studio.schedule()`` to take in a
  ``parsing_method`` parameter.

0.2.6.6
=======

* **Update:** The ``cut_in``, ``cut_out`` and ``cut_duration`` attribute
  behaviour and the attribute order is updated in ``Shot`` class. So, if three
  of the values are given, then the ``cut_duration`` attribute value will be
  calculated from ``cut_in`` and ``cut_out`` attribute values. In any case
  ``cut_out`` precedes ``cut_duration``, and if none of them given ``cut_in``
  and ``cut_duration`` values will default to 1 and ``cut_out`` will be
  calculated by using ``cut_in`` and ``cut_duration``.

0.2.6.5
=======

* **New:** Entity to Note relation is now Many-to-Many. So one Note can now be
  assigned more than one Entity.

* **New:** Added alembic revision for ``Entity_Notes`` table creation and data
  migration from ``Notes`` table to ``Entity_Notes`` table. So all notes are
  preserved.

* **Fix:** Fixed ``Shot.cut_duration`` attribute initialization on ``Shot``
  instances restored from database.

* **Fix:** Fixed ``Studios.is_scheduling_by`` relationship configuration, which
  was wrongly referencing the ``Studios.last_scheduled_by_id`` column instead
  of ``Studios.is_scheduled_by_id`` column.

0.2.6.4
=======

* **New:** Added a ``Task.review_set(review_number)`` method to get the desired
  set of reviews. It will return the latest set of reviews if ``review_number``
  is skipped or it is None.

* **Update:** Removed ``Task.approve()`` it was making things complex than it
  should be.

0.2.6.3
=======

* **Fix:** Added ``Page`` to ``class_names`` in ``db.init()``.

* **Fix:** Fixed ``TimeLog`` tjp representation to use bot the ``start`` and
  ``end`` date values instead of the ``start`` and ``duration``. This is much
  better because it is independent from the timing resolution settings.

0.2.6.2
=======

* **Fix:** Fixed ``stalker.models.studio.schedule()`` method, and prevented it
  to call ``DBSession.commit()`` which causes errors if there is a transaction
  manager.

* **Fix:** Fixed ``stalker.models._parse_csv_file()`` method for empty
  computed resources list.

0.2.6.1
=======

* **New:** ``stalker.models.task.TimeLog`` instances are now checking if the
  dependency relation between the task that receives the time log and the tasks
  that the task depends on will be violated in terms of the start and end dates
  and raises a ``DependencyViolationError`` if it is the case.

0.2.6
=====

* **New:** Added ``stalker.models.wiki.Page`` class, for holding a per Project
  wiki.

0.2.5.5
=======

* **Fix:** ``Review.task`` attribute now accepts None but this is mainly done
  to allow its relation to the ``Task`` instance can be broken when it needs to
  be deleted without issuing a database commit.

0.2.5.4
=======

* **Update:** The following column names are updated:
  
  * ``Tasks._review_number`` to ``Tasks.review_number``
  * ``Tasks._schedule_seconds`` to ``Tasks.schedule_seconds``
  * ``Tasks._total_logged_seconds`` to ``Tasks.total_logged_seconds``
  * ``Reviews._review_number`` to ``Reviews.review_number``
  * ``Shots._cut_in`` to ``Shots.cut_in``
  * ``Shots._cut_out`` to ``Shots.cut_out``
  
  Also updated alembic migration to create columns with those names.

* **Update:** Updated Alembic revision ``433d9caaafab`` (the one related with
  stalker 2.5 update) to also include following updates:
  
  * Create StatusLists for Tasks, Asset, Shot and Sequences and add all the
    Statuses in the Task Status Workflow.
  * Remove ``NEW`` from all of the status lists of Task, Asset, Shot and
    Sequence.
  * Update all the ``PREV`` tasks to ``WIP`` to let them use the new Review
    Workflow.
  * Update the ``Tasks.review_number`` to 0 for all tasks.
  * Create StatusLists and Statuses (``NEW``, ``RREV``, ``APP``) for Reviews.
  * Remove any other status then defined in the Task Status Workflow from Task,
    Asset, Shot and Sequence status list.

0.2.5.3
=======

* **Fix:** Fixed a bug in ``Task`` class where trying to remove the
  dependencies will raise an ``AttributeError`` caused by the
  ``Task._previously_removed_dependent_tasks`` attribute.

0.2.5.2
=======

* **New:** Task instances now have two new properties called ``path`` and
  ``absolute_path``. As in Version instances, these are the rendered version
  of the related FilenameTemplate object in the related Project. The ``path``
  attribute is Repository root relative and ``absolute_path`` is the absolute
  path including the OS dependent Repository path.

* **Update:** Updated alembic revision with revision number "433d9caaafab" to
  also create Statuses introduced with Stalker v0.2.5.

0.2.5.1
=======

* **Update:** ``Version.__repr__`` results with a more readable string.

* **New:** Added a generalized generator called
  ``stalker.models.walk_hierarchy()`` that walks and yields the entities over
  the given attribute in DFS or BFS fashion.

* **New:** Added ``Task.walk_hierarchy()`` which iterates over the hierarchy of
  the task. It walks in a breadth first fashion. Use ``method=0`` to walk in
  depth first.

* **New:** Added ``Task.walk_dependencies()`` which iterates over the
  dependencies of the task. It walks in a breadth first fashion. Use
  ``method=0`` to walk in depth first.

* **New:** Added ``Version.walk_hierarchy()`` which iterates over the hierarchy
  of the version. It walks in a depth first fashion. Use ``method=1`` to walk
  in breadth first.

* **New:** Added ``Version.walk_inputs()`` which iterates over the inputs of
  the version. It walks in a depth first fashion. Use ``method=1`` to walk in
  breath first.

* **Update:** ``stalker.models.check_circular_dependency()`` function is now
  using ``stalker.models.walk_hierarchy()`` instead of recursion over itself,
  which makes it more robust in deep hierarchies.

* **Fix:** ``db.init()`` now updates the statuses of already created status
  lists for ``Task``, ``Asset``, ``Shot`` and ``Sequence`` classes.

0.2.5
=====

* **Update:** ``Revision`` class is renamed to ``Review`` and introduced a
  couple of new attributes.

* **New:** Added a new workflow called "Task Review Workflow". Please see the
  documentation about the new workflow.

* **Update:** ``Task.responsible`` attribute is now a list which allows
  multiple responsible to be set for a ``Task``.

* **New:** Because of the new "Task Review Workflow" task statuses which are
  normally created in Stalker Pyramid are now automatically created in Stalker
  database initialization. The new statuses are
  **Waiting For Dependency (WFD)**, **Ready To Start (RTS)**,
  **Work In Progress (WIP)**, **Pending Review (PREV)**,
  **Has Revision (HREV)**, **On Hold (OH)**, **Stopped (STOP)** and
  **Completed (CMPL)** are all used in ``Task``, ``Asset``, ``Shot`` and
  ``Sequence`` status lists by default.

* **New:** Because of the new "Task Review Workflow" also a status list for
  ``Review`` class is created by default. It contains the statuses of
  **New (NEW)**, **Requested Revision (RREV)** and **Approved (APP)**.

* **Fix:** ``Users.login`` column is now unique.

* **Update:** Ticket workflow in config is now using the proper status names
  instead of the lower case names of the statuses.

* **New:** Added a new exception called **StatusError** which states the entity
  status is not suitable for the action it is applied to.

* **New:** ``Studio`` instance now stores the scheduling state to the database
  to prevent two scheduling process to override each other. It also stores the
  last schedule message and the last schedule date and the id of the user who
  has done the scheduling.

* **New:** The **Task Dependency** relation is now using an
  **Association Object** instead of just a **Secondary Table**. The
  ``Task.depends`` and ``Task.dependent_of`` attributes are now
  *association_proxies*.

  Also added extra parameters like ``dependency_target``, ``gap_timing``,
  ``gap_unit`` and ``gap_model`` to the dependency relation. So all of the
  dependency relations are now able to hold those extra information.

  Updated the ``task_tjp_template`` to reflect the details of the dependencies
  that a task has.

* **New:** ``ScheduleMixin`` class now has some default class attributes that
  will allow customizations in inherited classes. This is mainly done for
  ``TaskDependency`` class and for ``the gap_timing``, ``gap_unit``,
  ``gap_model`` attributes which are in fact synonyms of ``schedule_timing``,
  ``schedule_unit`` and ``schedule_model`` attributes coming from the
  ``ScheduleMixin`` class. So by using the ``__default_schedule_attr_name__``
  Stalker is able to display error messages complaining about ``gap_timing``
  attribute instead of ``schedule_timing`` etc.

* **New:** Updating a task by calling ``Task.request_revision()`` will now set
  the ``TaskDependency.dependency_target`` to **'onstart'** for tasks those are
  depending to the revised task and updated to have a status of **DREV**,
  **OH** or **STOP**. Thus, TaskJuggler will be able to continue scheduling
  these tasks even if the tasks are now working together.

* **Update:** Updated the TaskJuggler templates to make the tjp output a little
  bit more readable.

* **New:** ``ScheduleMixin`` now creates more localized (to the mixed in class)
  column and enum type names in the mixed in classes.

  For example, it creates the ``TaskScheduleModel`` enum type for ``Task``
  class and for ``TaskDependency`` it creates ``TaskDependencyGapModel`` with
  the same setup following the ``{{class_name}}{{attr_name}}Model`` template.

  Also it creates ``schedule_model`` column for ``Task``, and ``gap_model`` for
  ``TaskDependency`` class.

* **Update:** Renamed the ``TaskScheduleUnit`` enum type name to ``TimeUnit``
  in ``ScheduleMixin``.

0.2.4
=====

* **New:** Added new class called ``Revision`` to hold info about Task
  revisions.

* **Update:** Renamed ``ScheduleMixin`` to ``DateRangeMixin``.

* **New:** Added a new mixin called ``ScheduleMixin`` (replacing the old one)
  which adds attributes like ``schedule_timing``, ``schedule_unit``,
  ``schedule_model`` and ``schedule_constraint``.

* **New:** Added ``Task.tickets`` and ``Task.open_tickets`` properties.

* **Update:** Removed unnecessary arguments (``project_lead``, ``tasks``,
  ``watching``, ``last_login``) from User class.

* **Update:** The ``timing_resolution`` attribute is moved from the
  ``DateRangeMixin`` to ``Studio`` class. So instances of classes like
  ``Project`` or ``Task`` will not have their own timing resolution anymore.

* **New:** The ``Studio`` instance now overrides the values on
  ``stalker.defaults`` on creation and on load, and also the ``db.setup()``
  function lets the first ``Studio`` instance that it finds to update the
  defaults. So it is now possible to use ``stalker.defaults`` all the time
  without worrying about the Studio settings.

* **Update:** The ``Studio.yearly_working_days`` value is now always an
  integer.

* **New:** Added a new method ``ScheduleMixin.least_meaningful_time_unit()`` to
  calculate the most appropriate timing unit and the value of the given seconds
  which represents an interval of time.
  
  So it will convert 3600 seconds to 1 hours, and 8424000 seconds to 1 years if
  it represents working time (``as_working_time=True``) or 2340 hours if it is
  representing the calendar time.

* **New:** Added a new method to ``ScheduleMixin`` called ``to_seconds()``. The
  ``to_seconds()`` method converts the given schedule info values
  (``schedule_timing``, ``schedule_unit``, ``schedule_model``) to seconds
  considering if the given ``schedule_model`` is work time based ('effort' or
  'length') or calendar time based ('duration').

* **New:** Added a new method to ``ScheduleMixin`` called ``schedule_seconds``
  which you may recognise from ``Task`` class. What it does is pretty much the
  same as in the ``Task`` class, it converts the given schedule info values to
  seconds.

* **Update:** In ``DateRangeMixin``, when the ``start``, ``end`` or
  ``duration`` arguments given so that the duration is smaller then the
  ``defaults.timing_resolution`` the ``defaults.timing_resolution`` will be
  used as the ``duration`` and the ``end`` will be recalculated by anchoring
  the ``start`` value.

* **New:** Adding a ``TimeLog`` to a ``Task`` and extending its schedule info
  values now will always use the least meaningful timing unit. So expanding a
  task from 16 hours to 18 hours will result a task with 2 days of schedule
  (considering the ``daily_working_hours = 9``).

* **Update:** Moved the ``daily_working_hours`` attribute from ``Studio`` class
  to ``WorkingHours`` class as it was much related to this one then ``Studio``
  class. Left a property with the same name in the ``Studio`` class, so it will
  still function as it was before but there will be no column in the database
  for that attribute anymore.

0.2.3.5
=======

* **Fix:** Fixed a bug in ``stalker.models.auth.LocalSession`` where stalker
  was complaining about "copy_reg" module, it seems that it is related to
  `this bug`_.

  .. _this bug: http://www.archivum.info/python-bugs-list@python.org/2007-04/msg00222.html

0.2.3.4
=======

* **Update:** Fixed a little bug in Link.extension property setter.

* **New:** Moved the stalker.models.env.EnvironmentBase class to
  "Anima Tools" python module.

* **Fix:** Fixed a bug in stalker.models.task.Task._responsible_getter() where
  it was always returning the greatest parents responsible as the responsible
  for the child task when the responsible is set to None for the child.

* **New:** Added ``stalker.models.version.Version.naming_parents`` which
  returns a list of parents starting from the closest parent Asset, Shot or
  Sequence.

* **New:** ``stalker.models.version.Version.nice_name`` now generates a name
  starting from the closest Asset, Shot or Sequence parent.

0.2.3.3
=======

* **New:** ``Ticket`` action methods (``resolve``, ``accept``, ``reassign``,
  ``reopen``) now return the created ``TicketLog`` instance.

0.2.3.2
=======

* **Update:** Added tests for negative or zero fps value in Project class.

* **Fix:** Minor fix to ``schedule_timing`` argument in Task class, where IDEs
  where assuming that the value passed to the ``schedule_timing`` should be
  integer where as it accepts floats also.

* **Update:** Removed ``bg_color`` and ``fg_color`` attributes (and columns)
  from Status class. Use SimpleEntity.html_class and SimpleEntity.html_style
  attributes instead.

* **New:** Added ``Project.open_tickets`` property.

0.2.3.1
=======

* **Fix:** Fixed an inconvenience in SimpleEntity.__init__() when a
  date_created argument with a value is later than datetime.datetime.now() is
  supplied and the date_updated argument is skipped or given as None, then the
  date_updated attribute value was generated from datetime.datetime.now() this
  was causing an unnecessary ValueError. This is fixed by directly copying the
  date_created value to date_updated value when it is skipped or None.

0.2.3
=====

* **New:** SimpleEntity now have two new attributes called ``html_style`` and
  ``html_class`` which can be used in storing cosmetic html values.

0.2.2.3
=======

* **Update:** Note.content attribute is now a synonym of the Note.description
  attribute.

0.2.2.2
=======

* **Update:** Studio.schedule() now returns information about how much did it
  take to schedule the tasks.

* **Update:** Studio.to_tjp() now returns information about how much did it
  take to complete the conversion.

0.2.2.1
=======

* **Fix:** Task.percent_complete() now calculates the percent complete
  correctly.

0.2.2
=====

* **Update:** Added cascade attributes to all necessary relations for all the
  classes.

* **Update:** The Version class is not mixed with the StatusMixin anymore. So
  the versions are not going to be statusable anymore. Also created alembic
  revision (a6598cde6b) for that update.

0.2.1.2
=======

* **Update:** TaskJugglerScheduler and the Studio classes are now returning the
  stderr message out of their ``schedule()`` methods.

0.2.1.1
=======

* **Fix:** Disabled some deep debug messages on
  TaskJugglerScheduler._parse_csv_file().

* **Fix:** Fixed a flush issue related to the Task.parent attribute which is
  lazily loaded in Task._schedule_seconds_setter().

0.2.1
=====

* **Fix:** As usual distutil thinks ``0.2.0`` is a lower version number than
  ``0.2.0.rc5`` (I should have read the documentation again and used
  ``0.2.0.c5`` instead of ``0.2.0.rc5``) so this is a dummy update to just to
  fix the version number.

0.2.0
=====

* **Update:** Vacation tjp template now includes the time values of the start
  and end dates of the Vacation instance.

0.2.0.rc5
=========

* **Update:** For a container task, ``Task.total_logged_seconds`` and
  ``Task.schedule_seconds`` attributes are now using the info of the child
  tasks. Also these attributes are cached to database, so instead of querying
  the child tasks all the time, the calculated data is cached and whenever a
  TimeLog is created or updated for a child task (which changes the
  ``total_logged_seconds`` for the child task) or the ``schedule_timing`` or
  ``schedule_unit`` attributes are updated, the cached values are updated on
  the parents. Allowing Stalker to display percent_complete info of a container
  task without loading any of its children.

* **New:** Added ``Task.percent_complete`` attribute, which calculates the
  percent of completeness of the task based on the
  ``Task.total_logged_seconds`` and ``Task.schedule_seconds`` attributes.

* **Fix:** Added ``TimeLog.__eq__()`` operator to more robustly check if the
  time logs are overlapping.

* **New:** Added ``Project.percent_complete``,
  ``Percent.total_logged_seconds`` and ``Project.schedule_seconds`` attributes.

* **Update:** ``ScheduleMixin._validate_dates()`` does not set the date values
  anymore, it just return the calculated and validated ``start``, ``end`` and
  ``duration`` values.

* **Update:** ``Vacation`` now can be created without a ``User`` instance,
  effectively making the ``Vacation`` a ``Studio`` wide vacation, which applies
  to all users.

* **Update:** ``Vacation.__strictly_typed__`` is updated to ``False``, so there
  is no need to create a ``Type`` instance to be able to create a ``Vacation``.

* **New:** ``Studio.vacations`` property now returns the ``Vacation`` instances
  which has no *user*.

* **Update:** ``Task.start`` and ``Task.end`` values are no more read from
  children Tasks for a container task over and over again but calculated
  whenever the start and end values of a child task are changed or a new child
  is appended or removed.

* **Update:** ``SimpleEntity.description`` validation routine doesn't convert
  the input to string anymore, but checks the given description value against
  being a string or unicode instance.

* **New:** Added ``Ticket.summary`` field.

* **Fix:** Fixed ``Link.extension``, it is now accepting unicode.

0.2.0.rc4
=========

* **New:** Added a new attribute to ``Version`` class called
  ``latest_version`` which holds the latest version in the version queue.

* **New:** To optimize the database connection times, ``stalker.db.setup()``
  will not try to initialize the database every time it is called anymore. This
  leads a ~4x speed up in database connection setup. To initialize a newly
  created database please use::

    # for a newly created database
    from stalker import db
    db.setup() # connects to database
    db.init()  # fills some default values to be used with Stalker

    # for any subsequent access just use (don't need to call db.init())
    db.setup()

* **Update:** Removed all ``__init_on_load()`` methods from all of the classes.
  It was causing SQLAlchemy to eagerly load relations, thus slowing down
  queries in certain cases (especially in ``Task.parent`` -> ``Task.children``
  relation).

* **Fix:** Fixed ``Vacation`` class tj3 format.

* **Fix:** ``Studio.now`` attribute was not properly working when the
  ``Studio`` instance has been restored from database.

0.2.0.rc3
=========

* **New:** Added a new attribute to ``Task`` class called ``responsible``.

* **Update:** Removed ``Sequence.lead_id`` use ``Task.reponsible`` instead.

* **Update:** Updated documentation to include documentation about
  Configuring Stalker with ``config.py``.

* **Update:** The ``duration`` argument in ``Task`` class is removed. It is
  somehow against the idea of having ``schedule_model`` and ``schedule_timing``
  arguments (``schedule_model='duration'`` is kind of the same).

* **Update:** Updated ``Task`` class documentation.

0.2.0.rc2
=========

* **New:** Added ``Version.created_with`` attribute to track the environment or
  host program name that a particular ``Version`` instance is created with.

0.2.0.rc1
=========

* **Update:** Moved the Pyramid part of the system to another package called
  ``stalker_pyramid``.

* **Fix:** Fixed ``setup.py`` where importing ``stalker`` to get the
  ``__version__`` variable causing problems.

0.2.0.b9
========

* **New:** Added ``Version.latest_published_version`` and
  ``Version.is_latest_published_version()``.

* **Fix:** Fixed ``Version.__eq__()``, now Stalker correctly distinguishes
  different Version instances.

* **New:** Added ``Repository.to_linux_path()``,
  ``Repository.to_windows_path()``, ``Repository.to_osx_path()`` and
  ``Repository.to_native_path()`` to the ``Repository`` class.

* **New:** Added ``Repository.is_in_repo(path)`` which checks if the given
  path is in this repo.

0.2.0.b8
========

* **Update:** Renamed **Version.version_of** attribute to **Version.task**.

* **Fix:** Fixed **Version.version_number** where it was not possible to have
  a version number bigger than 2.

* **Fix:** In **db.setup()** Ticket statuses are only created if there aren't
  any.

* **Fix:** Added **Vacation** class to the registered class list in
  stalker.db.

0.2.0.b7
========

* **Update:** **Task.schedule_constraint** is now reflected to the tjp file
  correctly.

* **Fix:** **check_circular_dependency()** now checks if the **entity** and
  the **other_entity** are the same.

* **Fix:** **Task.to_tjp()** now correctly add the dependent tasks of a
  container task.

* **Fix:** **Task.__eq__()** now correctly considers the parent, depends,
  resources, start and end dates.

* **Update:** **Task.priority** is now reflected in tjp file if it is
  different than the default value (500).

* **New::** Added a new class called **Vacation** to hold user vacations.

* **Update:** Removed dependencies to ``pyramid.security.Allow`` and
  ``pyramid.security.Deny`` in couple of packages.

* **Update:** Changed the way the ``stalker.defaults`` is created.

* **Fix:** **EnvironmentBase.get_version_from_full_path()**,
  **EnvironmentBase.get_versions_from_path()**,
  **EnvironmentBase.trim_repo_path()**, **EnvironmentBase.find_repo** methods
  are now working properly.

* **Update:** Added **Version.absolute_full_path** property which renders the
  absolute full path which also includes the repository path.

* **Update:** Added **Version.absolute_path** property which renders the
  absolute path which also includes the repository path.

0.2.0.b6
========

* **Fix:** Fixed **LocalSession._write_data()**, previously it was not
  creating the local session folder.

* **New:** Added a new method called **LocalSession.delete()** to remove the
  local session file.

* **Update:** **Link.full_path** can now be set to an empty string. This is
  updated in this way for **Version** class.

* **Update:** Updated the formatting of **SimpleEntity.nice_name**, it is now
  possible to have uppercase letters and camel case format will be preserved.

* **Update**: **Version.take_name** formatting is enhanced.

* **New**: **Task** class is now mixed in with **ReferenceMixin** making it
  unnecessary to have **Asset**, **Shot** and **Sequence** classes all mixed
  in individually. Thus removed the **ReferenceMixin** from **Asset**,
  **Shot** and **Sequence** classes.

* **Update**: Added **Task.schedule_model** validation and its tests.

* **New**: Added **ScheduleMixin.total_seconds** and
  **ScheduleMixin.computed_total_seconds**.

0.2.0.b5
========

* **New:** **Version** class now has two new attributes called ``parent`` and
  ``children`` which will be used in tracking of the history of Version
  instances and track which Versions are derived from which Version.

* **New:** **Versions** instances are now derived from **Link** class and not
  **Entity**.

* **Update:** Added new revisions to **alembic** to reflect the change in
  **Versions** table.

* **Update:** **Links.path** is renamed to **Links.full_path** and added
  three new attributes called **path**, **filename** and **extension**.

* **Update:** Added new revisions to alembic to reflect the change in
  **Links** table.

* **New:** Added a new class called **LocalSession** to store session data in
  users local filesystem. It is going to be replaced with some other system
  like **Beaker**.

* **Fix:** Database part of Stalker can now be imported without depending to
  **Pyramid**.

* **Fix:** Fixed documentation errors that **Sphinx** complained about.

0.2.0.b4
========

* No changes in SOM.

0.2.0.b3
========

* **Update:** FilenameTemplate's are not ``strictly typed`` anymore.

* **Update:** Removed the FilenameTemplate type initialization, FilenameTemplates
  do not depend on Types anymore.

* **Update:** Added back the ``plural_class_name`` (previously ``plural_name``)
  property to the ORMClass class, so all the classes in SOM now have this new
  property. 

* **Update:** Added ``accepts_references`` attribute to the EntityType class.

* **New:** The Link class has a new attribute called ``original_filename`` to
  store the original file names of link files.

* **New:** Added **alembic** to the project requirements.

* **New:** Added alembic migrations which adds the ``accepts_references`` column
  to ``EntityTypes`` table and ``original_name`` to the ``Links`` table.

0.2.0.b2
========

* Stalker is now compatible with Python 2.6.
* Task:

  * **Update:** Tasks now have a new attribute called ``watchers`` which holds a
    list of User instances watching the particular Task.

  * **Update:** Users now have a new attribute called ``watching`` which is a
    list of Task instances that this user is watching.

* TimeLog:

  * **Update:** TimeLog instances will expand Task.schedule_timing value
    automatically if the total amount of logged time is more than the
    schedule_timing value.

  * **Update:** TimeLogs are now considered while scheduling the task.

  * **Fix:** TimeLogs raises OverBookedError when appending the same TimeLog
    instance to the same resource.

* Auth:

  * **Fix:** The default ACLs for determining the permissions are now working
    properly.

0.2.0.b1
========

* WorkingHours.is_working_hour() is working now.

* WorkingHours class is moved from stalker.models.project to
  stalker.models.studio module.

* ``daily_working_hours`` attribute is moved from
  stalker.models.project.Project to stalker.models.studio.Studio class.

* Repository path variables now ends with a forward slash even if it is not
  given.

* Updated Project classes validation messages to correlate with Stalker
  standard.

* Implementation of the Studio class is finished. The scheduling works like a
  charm.

* It is now possible to use any characters in SimpleEntity.name and the derived
  classes.

* Booking class is renamed to TimeLog.

0.2.0.a10
=========

* Added new attribute to WorkingHours class called ``weekly_working_hours``,
  which calculates the weekly working hours based on the working hours defined
  in the instance.

* Task class now has a new attribute called ``schedule_timing`` which is
  replacing the ``effort``, ``length`` and ``duration`` attributes. Together
  with the ``schedule_model`` attribute it will be used in scheduling the Task.

* Updated the config system to the one used in oyProjectManager (based on
  Sphinx config system). Now to reach the defaults::

    # instead of doing the following
    from stalker.conf import defaults # not valid anymore
    
    # use this
    from stalker import defaults
  
  If the above idiom is used, the old ``defaults`` module behaviour is
  retained, so no code change is required other than the new lower case config
  variable names.

0.2.0.a9
========

* A new property called ``to_tjp`` added to the SimpleEntity class which needs
  to be implemented in the child and is going to be used in TaskJuggler
  integration.

* A new attribute called ``is_scheduled`` added to Task class and it is going
  to be used in Gantt charts. Where it will lock the class and will not try
  to snap it to anywhere if it is scheduled.

* Changed the ``resolution`` attribute name to ``timing_resolution`` to comply
  with TaskJuggler.

* ScheduleMixin:

  * Updated ScheduleMixin class documentation.

  * There are two new read-only attributes called ``computed_start`` and
    ``computed_end``. These attributes will be used in storing of the values
    calculated by TaskJuggler, and will be used in Gantt Charts if available.

  * Added ``computed_duration``.

* Task:

  * Arranged the TaskJuggler workflow.

  * The task will use the effort > length > duration attributes in `to_tjp`
    property.

* Changed the license of Stalker from BSD-2 to LGPL 2.1. Any version previous
  to 0.2.0.a9 will be still BSD-2 and any version from and including 0.2.0.a9
  will be distributed under LGPL 2.1 license.

* Added new types of classes called Schedulers which are going to be used in
  scheduling the tasks.

* Added TaskJugglerScheduler, it uses the given project and schedules its
  tasks.

0.2.0.a8
========

* TagSelect now can be filled by setting its ``value`` attribute (Ex:
  TagSelect.set('value', data))

* Added a new method called ``is_root`` to Task class. It is true for tasks
  where there are no parents.

* Added a new attribute called ``users`` to the Department class which is a
  synonym for the ``members`` attribute.

* Task:

  * Task class is now preventing one of the dependents to be set as the parent
    of a task.

  * Task class is now preventing one of the parents to be set as the one of the
    dependents of a task.

  * Fixed ``autoflush`` bugs in Task class.

* Fixed `admin` users department initialization.

* Added ``thumbnail`` attribute to the SimpleEntity class which is a reference
  to a Link instance, showing the path of the thumbnail.

* Fixed Circular Dependency bug in Task class, where a parent of a newly
  created task is depending to another task which is set as the dependee for
  this newly created task (T1 -> T3 -> T2 -> T1 (parent relation) -> T3 -> T2
  etc.).

0.2.0.a7
========

* Changed these default setting value names to corresponding new names:

  * ``DEFAULT_TASK_DURATION`` -> ``TASK_DURATION``
  * ``DEFAULT_TASK_PRIORITY`` -> ``TASK_PRIORITY``
  * ``DEFAULT_VERSION_TAKE_NAME`` -> ``VERSION_TAKE_NAME``
  * ``DEFAULT_TICKET_LABEL`` -> ``TICKET_LABEL``
  * ``DEFAULT_ACTIONS`` -> ``ACTIONS``
  * ``DEFAULT_BG_COLOR`` -> ``BG_COLOR``
  * ``DEFAULT_FG_COLOR`` -> ``FG_COLOR``

* stalker.conf.defaults:

  * Added default settings for project working hours (``WORKING_HOURS``,
    ``DAY_ORDER``, ``DAILY_WORKING_HOURS``)

  * Added a new variable for setting the task time resolution called
    ``TIME_RESOLUTION``.

* stalker.models.project.Project:

  * Removed Project.project_tasks attribute, use Project.tasks directly to get
    all the Tasks in that project. For root task you can do a quick query::

      Task.query.filter(Task.project==proj_id).filter(Task.parent==None).all()
    
    This will also return the Assets, Sequences and Shots in that project,
    which are also Tasks.

  * Users are now assigned to Projects by appending them to the Project.users
    list. This is done in this way to allow a reduced list of resources to be
    shown in the Task creation dialogs.

  * Added a new helper class for Project working hour management, called
    WorkingHours.

  * Added a new attribute to Project class called ``working_hours`` which holds
    stalker.models.project.WorkingHours instances to manage the Project working
    hours. It will directly be passed to TaskJuggler.

* stalker.models.task.Task:

  * Removed the Task.task_of attribute, use Task.parent to get the owner of
    this Task.

  * Task now has two new attributes called Task.parent and Task.children which
    allow more complex Task-to-Task relation.

  * Secondary table name for holding Task to Task dependency relation is
    renamed from ``Task_Tasks`` to ``Task_Dependencies``.

  * check_circular_dependency function is now accepting a third argument which
    is the name of the attribute to be investigated for circular relationship.
    It is done in that way to be able to use the same function in searching for
    circular relations both in parent/child and depender/dependee relations.

* ScheduleMixin:

  * Added a new attribute to ScheduleMixin for time resolution adjustment.
    Default value is 1 hour and can be set with
    stalker.conf.defaults.TIME_RESOLUTION. Any finer time than the resolution
    is rounded to the closest multiply of the resolution. It is possible to set
    it from microseconds to years. Although 1 hour is a very reasonable
    resolution which is also the default resolution for TaskJuggler.

  * ScheduleMixin now uses datetime.datetime for the start and end attributes.

  * Renamed the ``start_date`` attribute to ``start``.

  * Renamed the ``end_date`` attribute to ``end``

* Removed the TaskableEntity.

* Asset, Sequence and Shot classes are now derived from Task class allowing
  more complex Task relation combined with the new parent/child relation of
  Tasks. Use Asset.children or Asset.tasks to reach the child tasks of that
  asset (same with Sequence and Shot classes).

* stalker.models.shot.Shot:

  * Removed the sequence and introduced sequences attribute in Shot class. Now
    one shot can be in more than one Sequence. Allowing more complex
    Shot/Sequence relations..

  * Shots can now be created without a Sequence instance. The sequence
    attribute is just used to group the Shots.

  * Shots now have a new attribute called ``scenes``, holding Scene instances.
    It is created to group same shots occurring in the same scenes.

* In tests all the Warnings are now properly handled as Warnings.

* stalker.models.ticket.Ticket:

  * Ticket instances are now tied to Projects and it is now possible to create
    Tickets without supplying a Version. They are free now.

  * It is now possible to link any SimpleEntity to a Ticket.

  * The Ticket Workflow is now fully customizable. Use
    stalker.conf.defaults.TICKET_WORKFLOW dictionary to define the workflow and
    stalker.conf.defaults.TICKET_STATUS_ORDER for the order of the ticket
    statuses.

* Added a new class called ``Scene`` to manage Shots with another property.

* Removed the ``output_path`` attribute in FilenameTemplate class.

* Grouped the templates for each entity under a directory with the entity name.

0.2.0.a6
========

* Users now can have more than one Department.

* User instances now have two new properties for getting the user tickets
  (User.tickets) and the open tickets (User.open_tickets).

* New shortcut Task.project returns the Task.task_of.project value.

* Shot and Asset creation dialogs now automatically updated with the given
  Project instance info.

* User overview page is now reflection the new design.

0.2.0.a5
========

* The ``code`` attribute of the SimpleEntity is now introduced as a separate
  mixin. To let it be used by the classes it is really needed.

* The ``query`` method is now converted to a property so it is now possible to
  use it like a property as in the SQLAlchemy.orm.Session as shown below::

    from stalker import Project
    Project.query.all() # instead of Project.query().all()

* ScheduleMixin.due_date is renamed to ScheduleMixin.end_date.

* Added a new class attribute to SimpleEntity called ``__auto_name__`` which
  controls the naming of the instances and instances derived from SimpleEntity.
  If ``__auto_name__`` is set to True the ``name`` attribute of the instance
  will be automatically generated and it will have the following format::

    {{ClassName}}_{{UUID4}}
    
  Here are a couple of naming examples::

    Ticket_74bb46b0-29de-4f3e-b4e6-8bcf6aed352d
    Version_2fa5749e-8cdb-4887-aef2-6d8cec6a4faa

* Fixed an autoflush issue with SQLAlchemy in StatusList class. Now the status
  column is again not nullable in StatusMixin.

0.2.0.a4
========

* Added a new class called EntityType to hold all the available class names and
  capabilities.

* Version class now has a new attribute called ``inputs`` to hold the inputs of
  the current Version instance. It is a list of Link instances.

* FilenameTemplate classes ``path`` and ``filename`` attributes are no more
  converted to string, so given a non string value will raise TypeError.

* Structure.custom_template now only accepts strings and None, setting it to
  anything else will raise a TypeError.

* Two Type's for FilenameTemplate's are created by default when initializing
  the database, first is called "Version" and it is used to define
  FilenameTemplates which are used for placing Version source files. The second
  one is called "Reference" and it is used when injecting references to a given
  class. Along with the FilenameTemplate.target_entity_type this will allow one
  to create two different FilenameTemplates for one class::

    # first get the Types
    vers_type = Type.query()\
                .filter_by(target_entity_type="FilenameTemplate")\
                .filter_by(type="Version")\
                .first()
    
    ref_type = Type.query()\
               .filter_by(target_entity_type="FilenameTemplate")\
               .filter_by(type="Reference")\
               .first()
    
    # lets create a FilenameTemplate for placing Asset Version files.
    f_ver = FilenameTemplate(
        target_entity_type="Asset",
        type=vers_type,
        path="Assets/{{asset.type.code}}/{{asset.code}}/{{task.type.code}}",
        filename="{{asset.code}}_{{version.take_name}}_{{task.type.code}}_v{{'%03d'|version.version_number}}{{link.extension}}"
        output_path="{{version.path}}/Outputs/{{version.take_name}}"
    )
    
    # and now define a FilenameTemplate for placing Asset Reference files.
    # no need to have an output_path here...
    f_ref = FilenameTemplate(
        target_entity_type="Asset",
        type=ref_type,
        path="Assets/{{asset.type.code}}/{{asset.code}}/References",
        filename="{{link.type.code}}/{{link.id}}{{link.extension}}"
    )

* stalker.db.register() now accepts only real classes instead of class names.
  This way it can store more information about classes.

* Status.bg_color and Status.fg_color attributes are now simple integers. And
  the Color class is removed.

* StatusMixin.status is now a ForeignKey to a the Statuses table, thus it is a
  real Status instance instead of an integer showing the index of the Status in
  the related StatusList. This way the Status of the object will not change if
  the content of the StatusList is changed.

* Added new attribute Project.project_tasks which holds all the direct or
  indirect Tasks created for that project.

* User.login_name is renamed to User.login.

* Removed the ``first_name``, ``last_name`` and ``initials`` attributes from
  User class. Now the ``name`` and ``code`` attributes are going to be used,
  thus the ``name`` attribute is no more the equivalent of ``login`` and the
  ``code`` attribute is doing what was ``initials`` doing previously.

0.2.0.a3
========

* Status class now has two new attributes ``bg_color`` and ``fg_color`` to hold
  the UI colors of the Status instance. The colors are Color instances.

0.2.0.a2
========

* SimpleEntity now has an attribute called ``generic_data`` which can hold any
  kind of ``SOM`` object inside and it is a list.

* Changed the formatting rules for the ``name`` in SimpleEntity class, now it
  can start with a number, and it is not allowed to have multiple whitespace
  characters following each other.

* The ``source`` attribute in Version is renamed to ``source_file``.

* The ``version`` attribute in Version is renamed to ``version_number``.

* The ``take`` attribute in Version is renamed to ``take_name``.

* The ``version_number`` in Version is now generated automatically if it is
  skipped or given as None or it is too low where there is already a version
  number for the same Version series (means attached to the same Task and has
  the same ``take_name``.

* Moved the User class to ``stalker.models.auth module``.

* Removed the ``stalker.ext.auth`` module because it is not necessary anymore.
  Thus the User now handles all the password conversions by itself.

* ``PermissionGroup`` is renamed back to Group
  again to match with the general naming of the authorization concept.

* Created two new classes for the Authorization system, first one is called
  Permission and the second one is a Mixin which is called ACLMixin which adds
  ACLs to the mixed in class. For now, only the User and Group classes are
  mixed with this mixin by default.

* The declarative Base class of SQLAlchemy is now created by binding it to a
  ORMClass (a random name) which lets all the derived class to have a method
  called ``query`` which will bypass the need of calling
  ``DBSession.query(class_)`` but instead just call ``class_.query()``::

    from stalker.models.auth import User
    user_1 = User.query().filter_by(name='a user name').first()


0.2.0.a1
========

* Changed the ``db.setup`` arguments. It is now accepting a dictionary instead
  of just a string to comply with the SQLAlchemy scaffold and this dictionary
  should contain keys for the SQLAlchemy engine setup. There is another utility
  that comes with Pyramid to setup the database under the `scripts` folder, it
  is also working without any problem with stalker.db.

* The ``session`` variable is renamed to ``DBSession`` and is now a scopped
  session, so there is no need to use ``DBSession.commit`` it will be handled
  by the system it self.

* Even though the ``DBSession`` is using the Zope Transaction Manager extension
  normally, in the database tests no extension is used because the transaction
  manager was swallowing all errors and it was a little weird to try to catch
  this errors out of the ``with`` block.

* Refactored the code, all the models are now in separate python files, but can
  be directly imported from the main stalker module as shown::

    from stalker import User, Department, Task
  
  By using this kind of organization, both development and usage will be eased
  out.

* ``task_of`` now only accepts TaskableEntity instances.

* Updated the examples. It is now showing how to extend SOM correctly. 

* Updated the references to the SOM classes in docstrings and rst files.

* Removed the ``Review`` class. And introduced the much handier Ticket class.
  Now reviewing a data is the process of creating Ticket's to that data.

* The database is now initialized with a StatusList and a couple of Statuses
  appropriate for Ticket instances.

* The database is now initialized with two Type instances ('Enhancement' and
  'Defect') suitable for Ticket instances.

* StatusMixin now stores the status attribute as an Integer showing the index
  of the Status in the ``status_list`` attribute but when asked for the value
  of ``StatusMixin.status`` attribute it will return a proper Status instance
  and the attribute can be set with an integer or with a proper Status
  instance.
