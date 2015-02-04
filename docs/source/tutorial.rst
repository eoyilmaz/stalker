.. _tutorial_toplevel:

============
API Tutorial
============

Introduction
============

Using Stalker along with Python is all about interacting with a database by
using the Stalker Object Model (SOM). Stalker uses the powerful `SQLAlchemy
ORM`_.

.. _SQLAlchemy ORM: http://www.sqlalchemy.org/docs/orm/tutorial.html

This tutorial section let you familiarise with the Stalker Python API and
Stalker Object Model (SOM). If you used SQLAlchemy before you will feel at
home and if you aren't you will see that it is fun dealing with databases with
SOM.

Part I - Basics
===============

Lets say that we just installed Stalker (as you are right now) and want to use
Stalker in our first project.

The first thing we are going to learn about is how to connect to the database
so we can enter information about our studio and the projects.

We are going to use a helper script to connect to the default database. Use the
following command to connect to the database::

  from stalker import db
  db.setup()

This will create an in-memory SQLite3 database, which is useless other than
testing purposes. To be able to get more out of Stalker we should give a proper
database information. The most basic setup is to use a file based SQLite3
database::

  db.setup({"sqlalchemy.url": "sqlite:///C:/studio.db"}) # assumed Windows

or::

  db.setup({"sqlalchemy.url": "sqlite:////home/ozgur/studio.db"}) # under linux or osx

.. ::
   This command will do the following:
    1. setup the database connection, by creating an `engine`_
    2. create the SQLite3 database file if doesn't exist
    3. create a `session`_ instance
    4. do the `mapping`_
    
   .. _session: http://www.sqlalchemy.org/docs/orm/session.html
   .. _engine: http://www.sqlalchemy.org/docs/core/engines.html
   .. _mapping: http://www.sqlalchemy.org/docs/orm/mapper_config.html

Then if this is the first time you are connecting to the database, then you
should initialize the database and create some defaults::

  db.init()

This will create some very important default data required for Stalker to work
properly. Although it will not break anything to call ``db.init()`` multiple
times it is needed only once (so you don't need to call it again when you close
your python shell and open up a new and fresh one).

Lets continue by creating a :class:`.Studio` for our self::

  from stalker import Studio
  my_studio = Studio(
      name='My Great Studio'
  )

For now don't care what a Studio is about. It will be explained later on this
tutorial.

Lets continue by creating a **User** for ourselves in the database. The first
thing we need to do is to import the :class:`.User` class in to the current
namespace::

  from stalker import User

then create the :class:`.User` object::

  me = User(
      name="Erkan Ozgur Yilmaz",
      login="eoyilmaz",
      email="some_email_address@gmail.com",
      password="secret",
      description="This is me"
  )

Now we have just created a user which represents us.

Lets create a new :class:`.Department` to define your department::

  from stalker import Department
  tds_department = Department(
      name="TDs",
      description="This is the TDs department"
  )

Now add your user to the department::

  tds_department.users.append(me)

or we can do it by using the User instance::

  me.departments.append(tds_department)

Even if you didn't do the latter, when you run::

  print(me.departments)
  # you should get something like
  # [<TDs (Department)>]

We have successfully created a :class:`.User` and a :class:`.Department` and we
assigned the user as one of the member of the **TDs Department**.

Because we didn't tell Stalker to commit the changes, no data has been saved to
the database yet. So lets send it the data to the database::

  db.DBSession.add(my_studio)
  db.DBSession.add(me)
  db.DBSession.add(tds_department)
  db.DBSession.commit()

As you see we have used the ``db.DBSession`` object to send the data to the
database. These information are in the database right now.

Lets try to get something back from the database by querying all the
departments, then getting the second one (the first department is always the
"admins" which is created by default) and getting its first members name::

  all_departments = Department.query.all()
  print(all_departments)
  # This should print something like
  # [<admins (Department)>, <TDs (Department)>]
  # "admins" department is created by default

  admins = all_departments[0]
  tds = all_departments[1]

  all_users = tds.users  # Department.users is a synonym for Department.members
                         # they are essentially the same attribute
  print(all_users[0])
  # this should print
  # <Erkan Ozgur Yilmaz ('eoyilmaz') (User)>

Part II/A - Creating Simple Data
================================

Lets say that we have this new commercial project coming and you want to start
using Stalker with it. So we need to create a :class:`.Project` object to hold
data about it.

A project instance needs to have a suitable :class:`.StatusList` (see
:ref:`status_and_status_lists_toplevel`) and it needs to be attached to a
:class:`.Repository` instance::

  # we will reuse the Statuses created by default (in db.init())
  from stalker import Status

  status_new = Status.query.filter_by(code='NEW').first()
  status_wip = Status.query.filter_by(code='WIP').first()
  status_cmpl = Status.query.filter_by(code='CMPL').first()

.. note::
   When the Stalker database is first initialized (with ``db.init()``) a set of
   :class:`.Status`\ es for :class:`.Task`\ s, :class:`.Asset`\ s,
   :class:`.Shot`\ s, :class:`.Sequence`\ s and :class:`.Ticket`\ s are created
   along with a :class:`.StatusList` for each of the data types. Up in this
   tutorial we have used those Statuses (new, wip and cmpl) created by default.

For now we have just created generic statuses. These :class:`.Status` instances
can be used with any kind of statusable objects. The idea behind is to define
the statuses only once, and use them in mixtures suitable for different type of
objects. So you can define all the possible Statuses for your entities, then
you can create a list of them for specific type of objects.

Lets create a :class:`.StatusList` suitable for :class:`.Project` instances::

  # a status list which is suitable for Project instances
  from stalker import StatusList, Project
  
  project_statuses = StatusList(
      name="Project Status List",
      statuses=[
          status_new,
          status_wip,
          status_cmpl
      ],
      target_entity_type=Project  # you can also use "Project" which is a str
  )

So we defined a status list which is suitable for Project instances. As you
see we didn't used all the generic Statuses in our ``project_statuses`` because
for a Project object we thought that these statuses are enough.

.. ::
  We also need to specify the type of the project, which is *commercial* in our
  case::
  
    from stalker import Type
    commercial_project_type = Type(
        name="Commercial Project",
        target_entity_type=Project
    )
  
  class:`~stalker.models.type.Type`\ s are generic entities that is accepted by
  any kind of entity created in Stalker. So in Stalker you can define a type
  for anything. But a couple of them, like the
  :class:`~stalker.models.project.Project` class, needs the type to be defined
  in the creation of the instance.

And finally, the :class:`.Repository`. The Repository (or Repo if you like) is
a path in our file server, where we place files and which is visible to all the
workstations/render farmers::

  from stalker import Repository
  
  # and the repository itself
  commercial_repo = Repository(
      name="Commercial Repository"
  )

:class:`.Repository` class will be explained in detail in upcoming sections.

So::

  new_project = Project(
      name="Fancy Commercial",
      code='FC',
      status_list=project_statuses,
      repositories=[commercial_repo],
  )

So we have created our project now.

Lets enter more information about this new project::

  import datetime
  from stalker import ImageFormat
  
  new_project.description = \
  """The commercial is about this fancy product. The
  client want us to have a shiny look with their
  product bla bla bla..."""

  new_project.image_format = ImageFormat(
      name="HD 1080",
      width=1920,
      height=1080
  )

  new_project.fps = 25
  new_project.end = datetime.date(2014, 5, 15)
  new_project.users.append(me)

Lets save all the new data to the database::

  db.DBSession.add(new_project)
  db.DBSession.commit()

As you see, even though we have created multiple objects (new_project,
statuses, status lists etc.) we've just added the ``new_project`` object to the
database, but don't worry all the related objects will be added to the
database.

A Project generally is group of :class:`.Task`\ s that needs to be completed. A
:class:`.Task` in Stalker is a type of entity where we define the total amount
of effort need to be done (or the duration or the length of the task, see
:class:`.Task` class documentation) to consider that Task as completed. All of
the tasks (leaf tasks in fact, coming next) has ``resources`` which defines the
:class:`.User`\ s who need to work on that task and complete it. This will all
be explained in :class:`.Task` class documentation.

For now you just need to now that :class:`.Asset`\ s, :class:`.Shot`\ s and
:class:`.Sequence`\ s in Stalker are derived from :class:`.Task` and they are
in fact other type of Tasks or a specialized version of Tasks.
 
So lets create a :class:`.Sequence`::

  from stalker import Sequence

  seq1 = Sequence(
      name="Sequence 1",
      code="SEQ1",
      project=new_project,
  )

And a Sequence generally has :class:`.Shot`\ s::

  from stalker import Shot

  sh001 = Shot(
      name='SH001',
      code='SH001',
      project=new_project,
      sequences=[seq1]
  )
  sh002 = Shot(
      code='SH002',
      project=new_project,
      sequences=[seq1]
  )
  sh003 = Shot(
      code='SH003',
      project=new_project,
      sequences=[seq1]
  )

send them to the database::

  db.DBSession.add_all([sh001, sh002, sh003])
  db.DBSession.commit()

.. note::
   Even though, in this tutorial we have created :class:`.Shot`\ s with one
   :class:`.Sequence` instance, it is not needed. You can create
   :class:`.Shot`\ s without any :class:`.Sequence` instance needed.
   
   For small projects like commercials, you may skip creating a Sequence at
   all.
   
   For bigger projects, like feature movies, it is a very good idea to use
   Sequences and then group the Shots under them.
   
   But again, a Shot can be connected to multiple sequences, which is useful if
   your shot, let say, is a kind of flashback and you will use this shot again
   without changing it at all, then this feature becomes handy.

Part II/B - Querying, Updating and Deleting Data
================================================

So far we just created some simple data. What about updating them. Let say that
we created a new shot with wrong info::

  sh004 = Shot(
      code='SH004',
      project=new_project,
      sequences=[seq1]
  )
  db.DBSession.add(sh004)
  db.DBSession.commit()

and you figured out that you have created and committed a wrong info and you
want to correct it::

  sh004.code = "SH005"
  db.DBSession.commit()

later on lets say you wanted to get the shot back from database::

  # first find the data
  wrong_shot = Shot.query.filter_by(code="SH005").first()
  
  # now update it
  wrong_shot.code = "SH004"
  
  # commit the changes to the database
  db.DBSession.commit()

and let say that you decided to delete the data::

  db.DBSession.delete(wrong_shot)
  db.DBSession.commit()

If you don't close your python session, your variable are still going to
contain the data but they do not exist in the database anymore::

  wrong_shot = Shot.query.filter_by(code="SH005").first()
  print(wrong_shot)
  # should print None

for more info about update and delete options (like cascades) in SQLAlchemy
please see the `SQLAlchemy documentation`_.

.. _SQLAlchemy documentation: http://www.sqlalchemy.org/docs/orm/session.html

Part III - Pipeline
===================

Up until now, we skipped a lot of stuff here to take little steps every time.
Even tough we have created users, departments, projects, sequences and shots,
Stalker still doesn't know much about our studio. For example, it doesn't have
any information about the **pipeline** that we are following and what steps we
do to complete those shots, thus to complete the project.

In Stalker, pipeline is managed by :class:`~stalker.models.task.Task`\ s. So
you create Tasks for Shots and then you can create dependencies between tasks.

So lets create a couple of tasks for one of the shots we have created before::

  from stalker import Task

  previs = Task(
      name="Previs",
      parent=sh001
  )
  
  matchmove = Task(
      name="Matchmove",
      parent=sh001
  )
  
  anim = Task(
      name="Animation",
      parent=sh001
  )
  
  lighting = Task(
      name="Lighting",
      parent=sh001
  )
  
  comp = Task(
      name="comp",
      parent=sh001
  )

Now create the dependencies between them::

  comp.depends = [lighting]
  lighting.depends = [anim]
  anim.depends = [previs, matchmove]

Stalker uses this dependency relation in scheduling these tasks. That is by
appending "lighting" task as one of the dependencies of comp, Stalker now know
that lighting should be completed to let the resource of the comp task start
working. The "Task Scheduling" will be explained in detail later on in this
tutorial.

Part IV - Task & Resource Management
====================================

Now we have a couple of Shots with couple of tasks inside it but we didn't
assign the tasks to anybody to let them complete this job.

Lets assign all this stuff to our self (for now :) )::

  previs.resources = [me]
  previs.schedule_timing = 10
  previs.schedule_unit = 'd'

  matchmove.resources = [me]
  matchmove.schedule_timing = 2
  matchmove.schedule_unit = 'd'

  anim.resources = [me]
  anim.schedule_timing = 5
  anim.schedule_unit = 'd'

  lighting.resources = [me]
  lighting.schedule_timing = 3
  lighting.schedule_unit = 'd'

  comp.resources = [me]
  comp.schedule_timing = 6
  comp.schedule_unit = 'h'

Now Stalker knows the hierarchy of the tasks and how much effort is needed to
complete this tasks. Stalker will use this information to solve the Scheduling
problem, and will tell you when to start and complete this tasks.

Lets commit the changes again::

  db.DBSession.commit()

If you noticed, this time we didn't add anything to the session, cause we have
added the ``sh001`` in a previous commit, and because all the objects are
attached to this shot object in some way, all the changes has been tracked and
added to the database.

Part V - Scheduling
===================

In previous sections of this tutorial we have created a :class:`.Shot` and then
created a couple of :class:`.Task`\ s to this shot and then assigned our self
as the resource of these tasks.

Stalker knows enough about our little project now, but we don't know where to
start the project from. That is which task should we start from.

In Stalker, defining the start and end dates of a Task (also of an Asset, Shot
and Sequence) is called "Scheduling". Stalker, with the help of `TaskJuggler`_,
can solve this problem and define when the resource should work on a specific
task.

.. warning::
   You should have `TaskJuggler`_ installed in your system, and you should have
   configured your Stalker installation to be able to find the ``tj3``
   executable.

   On a linux system this should be fairly straight forward, just install
   `TaskJuggler`_ and stalker will be able to use it.

   But for other OSes, like OSX and Windows, you should create an environment
   variable called ``STALKER_PATH`` and then place a file called ``config.py``
   inside the folder that this path is pointing at. And then add the following
   to this ``config.py``::

     tj_command = 'C:\\Path\\to\\tj3.exe'

   The default value for ``tj_command`` config variable is
   ``/usr/local/bin/tj3``, so if on a Linux or OSX system when you run::

     which tj3

   is returning this value (``/usr/local/bin/tj3``) you don't need to setup
   anything.

   .. _TaskJuggler: http://www.taskjuggler.org/

So, lets schedule our project by using the :class:`.Studio` instance that we
have created at the beginning of this tutorial::

  from stalker import TaskJugglerScheduler

  my_studio.scheduler = TaskJugglerScheduler()
  my_studio.duration = datetime.timedelta(days=365)  # we are setting the
  my_studio.schedule(scheduled_by=me)                # duration to 1 year just
                                                     # to be sure that TJ3
                                                     # will not complain
                                                     # about the project is not
                                                     # fitting in to the time
                                                     # frame.
  db.DBSession.commit()  # to reflect the change

This should take a little while depending to your projects size (around 1-2
seconds for this tutorial, but around ~15 min for a project with 15000+ tasks).

When it is finished all of your tasks now have their ``computed_start`` and
``computed_end`` values filled with proper data. Now check the start and end
values::

  print(previs.computed_start)     # 2014-04-02 16:00:00
  print(previs.computed_end)       # 2014-04-15 15:00:00

  print(matchmove.computed_start)  # 2014-04-15 15:00:00
  print(matchmove.computed_end)    # 2014-04-17 13:00:00

  print(anim.computed_start)       # 2014-04-17 13:00:00
  print(anim.computed_end)         # 2014-04-23 17:00:00
  
  print(lighting.computed_start)   # 2014-04-23 17:00:00
  print(lighting.computed_end)     # 2014-04-24 11:00:00

  print(comp.computed_start)       # 2014-04-24 11:00:00
  print(comp.computed_end)         # 2014-04-24 17:00:00

The dates are probably going to be different in your computer. But as you see
Stalker has computed the start and end date values for each of the tasks. They
are simply following one other, this is because we have entered only one
resource for each of the task.

You should know that "Scheduling" is a huge concept and it is greatly explained
in `TaskJuggler`_ documentation.

For a last thing you can check the ``to_tjp`` values of each data we have
created for now, so try running::

  print(my_studio.to_tjp)
  print(me.to_tjp)
  print(comp.to_tjp)
  print(new_project.to_tjp)

If you are familiar with TaskJuggler, you should recognize the output of each
``to_tjp`` variable. So essentially Stalker is mapping all of its data to a
TaskJuggler compatible string. A very small part of TaskJuggler directives are
currently supported. But it is enough to schedule very complex projects with
complex dependency relation and Task hierarchies. And with every new version of
Stalker the supported TaskJuggler directives are expanded.

Part VI - Asset Management
==========================

Now we have created a lot of things but other then storing all the data in the
database, we didn't do much. Stalker still doesn't have information about a lot
of things. For example, it doesn't know how to handle your asset versions
(:class:`.Version`) namely it doesn't know how to store your data that you are
going to create while completing these tasks.

So what we need to define is a place in our file structure. It doesn't need to
be a network shared directory but if you are not working alone than it means
that everyone needs to reach your data and the simplest way to do this is to
place your files in a network share, there are other alternatives like storing
your files locally and sharing your revisions with a Software Configuration
Management (SCM) system, Stalker doesn't support the latter right now.

We are going to see the first alternative, which uses a network share in our
fileserver, and this network share is called a :class:`.Repository` in Stalker.

A repository is a file path, preferably a path which is mapped or mounted to
the same path on every computer in your studio (also you can use ``autofs``
with an OpenLDAP server in which you can synchronize all off the mount points
on all of your workstations and render slaves at once).

In Stalker, you can have several repositories, let say one for Commercials and
another one for each big Movie projects.

You can define repositories and assign projects to those repositories.

We have already created a repository while creating our first project. But the
repository has missing information. A Repository object shows the path that we
create our projects into. Lets enter the paths for all the major operating
systems::

  commercial_repo.linux_path   = "/mnt/M/commercials"
  commercial_repo.osx_path     = "/Volumes/M/commercials"
  commercial_repo.windows_path = "M:/commercials"  # you can use reverse
                                                   # slashes (\\) if you want

And if you ask for the path to a repository object it will always give the
correct answer according to your operating system::

  print(commercial_repo.path)
  # under Windows outputs:
  # M:/commercials
  #
  # in Linux and variants:
  # /mnt/M/commercials
  #
  # and in OSX:
  # /Volumes/M/commercials

.. note::
  Stalker always uses forward slashes no matter what operating system you are
  using. It is like that even if you define your paths with reverse slashes
  (\\).

Assigning this repository to our project is not enough, Stalker still doesn't
know about the directory structure of this project. To explain the project
structure to Stalker we use a :class:`.Structure` instance::

  from stalker import Structure
  
  commercial_project_structure = Structure(
      name="Commercial Projects Structure"
  )
  
  # now assign this structure to our project
  new_project.structure = commercial_project_structure

.. versionadded:: 0.2.13

   Starting with Stalker version 0.2.13 :class:`.Project` instances can have
   **multiple** :class:`.Repository` instances attached. So you can create
   complex templates where you can for example store published versions on a
   different server/network share or you can setup so the outputs of a version
   (like the rendered files) are stored on a different server, and etc.

   *The following examples are updated in a simple way and examples showing*
   *the advantage of having multiple repositories will be added on later*
   *versions.*

Now we have created a very simple structure instance, but we still need to
create :class:`.FilenameTemplate` instances for Tasks which then will be used
by the :class:`.Version` instances to generate a consistent and meaningful path
and filename::

  from stalker import FilenameTemplate

  task_template = FilenameTemplate(
      name='Task Template for Commercials',
      target_entity_type='Task',
      path='$REPO{{project.repository.id}}/{{project.code}}/{%- for p in parent_tasks -%}{{p.nice_name}}/{%- endfor -%}',
      filename='{{version.nice_name}}_v{{"%03d"|format(version.version_number)}}'
  )

  # and append it to our project structure
  commercial_project_structure.templates.append(task_template)

  # commit to database
  db.DBSession.commit()  # no need to add anything, project is already on db

By defining a :class:`.FilenameTemplate` instance we have essentially told
Stalker how to store :class:`.Version` instances created for :class:`.Task`
entities in our :class:`.Repository`.

The data entered both to the ``path`` and ``filename`` arguments are `Jinja2`_
directives. The :class:`.Version` class knows how to render these templates
while calculating its ``path`` and ``filename`` attributes.

Also, if you noticed we have used an environment variable "$REPO" along with
the id of the first repository in the project "{{project.repository.id}}"
(attention! ``project.repository`` always shows the first repository in the
project), this is a new feature introduced with Stalker version 0.2.13. Stalker
creates environment variables on runtime for each of the repository whenever a
repository is created and inserted in to the DB or it will create environment
variables for already existing repositories upon a successful database
connection.

Lets create a :class:`.Version` instance for one of our tasks::

  from stalker import Version
  
  vers1 = Version(
      task=comp
  )

  # we need to update the paths
  vers1.update_paths()

  # check the path and filename
  print(vers1.path)                # '$REPO33/FC/SH001/comp'
  print(vers1.filename)            # 'SH001_comp_Main_v001'
  print(vers1.full_path)           # '$REPO33/FC/SH001/comp/SH001_comp_Main_v001'

  # now the absolute values, values with repository root
  # because I'm running this code in a Linux laptop, my results are using the
  # linux path of the repository
  print(vers1.absolute_path)       # '/mnt/M/commercials/FC/SH001/comp'
  print(vers1.absolute_full_path)  # '/mnt/M/commercials/FC/SH001/comp/SH001_comp_Main_v001'

  # check the version_number
  print(vers1.version_number)      # 1

  # commit to database
  db.DBSession.commit()

As you see, the :class:`.Version` instance magically knows where to place
itself and what to use as the filename. Thanks to Stalker it is now easy to
create version files where you don't have weird file names (ex:
'Shot1_comp_Final', 'Shot1_comp_Final_revised',
'Shot1_comp_Final_revised_Final', 'Shot1_comp_Final_revised_Final_real_final'
and the list goes on, we all know those filenames don't we :) ).

With Stalker the filename and path always follows strict rules.

Also by using the :attr:`.Version.is_published` attribute you can define which
of the versions are usable and which are versions that you are still working
on::

  vers1.is_published = False  # I still work on this version, this is not a
                              # usable one

Lets create another version for the same task and see what happens::

  # be sure that you've committed the previous version to the database
  # to let Stalker now what number to give for the next version
  vers2 = Version(task=comp)
  vers2.update_paths()  # this call probably will disappear in next version of
                        # Stalker, so Stalker will automatically update the
                        # paths on Version.__init__()

  print(vers2.version_number)  # 2
  print(vers2.filename)        # 'SH001_comp_Main_v002'

  # before creating a new version commit this one to db
  db.DBSession.commit()

  # now create a new version
  vers3 = Version(task=comp)
  vers3.update_paths()

  print(vers3.version_number)  # 3
  print(vers3.filename)        # 'SH001_comp_Main_v002'

Isn't that nice, Stalker increments the version number automatically.

Also you can query all the versions of a specific task by::

  # using pure Python
  vers_from_python = comp.versions  # [<FC_SH001_comp_Main_v001 (Version)>,
                                    #  <FC_SH001_comp_Main_v002 (Version)>,
                                    #  <FC_SH001_comp_Main_v003 (Version)>]

  # or using a query
  vers_from_query = Version.query.filter_by(task=comp).all()

  # again returns
  # [<FC_SH001_comp_Main_v001 (Version)>,
  #  <FC_SH001_comp_Main_v002 (Version)>,
  #  <FC_SH001_comp_Main_v003 (Version)>]

  assert vers_from_python == vers_from_query

.. _Jinja2: http://jinja.pocoo.org/

.. note::
   Stalker stores :attr:`.Version.path` and :attr:`.Version.filename`
   attributes in the database, so the values does not contain any OS specific
   path. It will only show the OS specific path on
   :attr:`.Version.absolute_path` and on :attr:`.Version.absolute_full_path`
   attributes by joining the :attr:`.Repository.path` with the path values from
   database momentarily.

You can also setup your project structure to have default directories::

  commercial_project_structure.custom_template = """
  Temp
  References
  References/Movies
  References/Images
  """

When the above template is executed each line will refer to a directory.

Part VII - Collaboration (not completed)
========================================

We came a lot from the start, but what is the use of an Production Asset
Management System if we can not communicate with our colleagues.

In Stalker you can communicate with others in the system, by:
  
  * Leaving a :class:`.Note` to anything created in
    Stalker (except you can not create a :class:`.Note` to another
    :class:`.Note` and to a :class:`.Tag`).
  * Sending a :class:`.Message` directly to them or to a group of users. (Not
    implemented yet).
  * Anyone can create a :class:`.Ticket` for a :class:`.Project`.
  * You can create wiki :class:`.Page`\ s per :class:`.Project`.

Part VIII - Extending SOM (coming)
==================================

This part will be covered soon

Conclusion
==========

In this tutorial, you have nearly learned a quarter of what Stalker supplies as
a Python library.

Stalker is a very flexible and powerful Production Asset Management system. As
of writing this tutorial it has been developed for the last 5 years (4 years
with the only developer being yours truly and for another 1 year where his wife
is also attended to the project) and it is currently been used in production of
a feature movie.

But it is only a Python library so it doesn't supply any graphical user
interface.

There are other projects, namely `Stalker Pyramid`_ and `Anima`_ that is using
Stalker in their back ends. `Stalker Pyramid`_ is an `Pyramid`_ based Web
application and `Anima`_ is a pipeline library.

You can clone their repositories to see how PyQt4 and PySide UIs are created
with Stalker (in Anima) and how it is used as the database model for a Web
application in `Stalker Pyramid`_.

.. _Stalker Pyramid: http://code.google.com/p/stalker-pyramid/
.. _Anima: https://github.com/eoyilmaz/anima
.. _Pyramid: http://www.pylonsproject.org/
