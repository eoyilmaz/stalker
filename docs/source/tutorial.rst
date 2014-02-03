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

Lets continue by creating a **User** for ourselves in the database. The first
thing we need to do is to import the :class:`.User` class in to the current
namespace::

  from stalker import User

then create the :class:`~stalker.models.user.User` object::

  myUser = User(
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

  tds_department.users.append(myUser)

or we can do it by using the User instance::

  myUser.department = tds_department

We have successfully created a :class:`.User` and a :class:`.Department` and we
assigned the user as one of the member of the **TDs Department**.

Because we didn't tell Stalker to commit the changes, no data has been saved to
the database yet. So lets send it the data to the database::

  db.session.add(myUser)
  db.session.add(tds_department)
  db.session.commit()

As you see we have used the ``db.session`` object to send the data to the
database. These information are in the database right now.

Lets try to get something back from the database by querying all the
departments, then getting the second one (the first department is always the
"admins" which is created by default) and getting its first members name::

  all_departments = Department.query.all()
  all_members = all_departments[1].members
  print all_members[0]

this should print out "<User (Erkan Ozgur Yilmaz ('eoyilmaz'))>".

Part II/A - Creating Simple Data
================================

Lets say that we have this new commercial project coming and you want to start
using Stalker with it. So we need to create a
:class:`~stalker.models.project.Project` object to hold data about it.

A project instance needs to have a suitable
:class:`~stalker.models.status.StatusList`
(see :ref:`status_and_status_lists_toplevel`) and it needs to be attached to a
:class:`~stalker.models.repository.Repository` instance::

  # lets create a couple of generic Statuses
  from stalker import Status
  
  status_waiting = Status(name="Waiting To Start", code="WTS")
  status_wip = Status(name="Work in Progress", code="WIP")
  status_pendrev = Status(name="Pending Review", code="PREV")
  status_approved = Status(name="Approved", code="APP")
  status_complete = Status(name="Complete", code="CMPLT")
  status_stopped = Status(name="Stopped", code="STOP")

For now we have just created generic statuses. These
:class:`~stalker.models.status.Status` instances can be used with any kind of
objects. The idea behind is to define the statuses only once, and use them in
mixtures suitable for different type of object. So you can define all the
possible Statuses for your entities, then you can create a list of them for
specific type of objects (Assets, Projects, Shots etc.).

Lets create a :class:`~stalker.models.status.StatusList` suitable for
:class:`~stalker.models.project.Project` instances::

  # a status list which is suitable for Project instances
  from stalker import StatusList, Project
  
  project_statuses = StatusList(
      name="Project Status List",
      statuses=[status_waiting,
                status_wip,
                status_stopped,
                status_complete],
      target_entity_type=Project
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

And finally, the :class:`~stalker.models.repository.Repository`. The Repository
(or Repo if you like) is a path in our file server, where we place files and
which is visible to all the workstations/render farmers::

  from stalker import Repository
  
  # and the repository itself
  commercial_repo = Repository(
    name="Commercial Repository",
  )

:class:`~stalker.models.repository.Repository` class will be explained in
detail in upcoming sections.

So::

  new_project = Project(
      name="Fancy Commercial",
      status_list=project_statuses,
      repository=commercial_repo,
  )

.. ::
  One of the biggest income of having the type set to something is to be able to
  filter the projects quickly. Think about querying "Commercials" and
  distinguishing them from the "Movie" projects or "Print" projects.

So we have created our project now.

Lets enter more information about this new project::

  import datetime
  from stalker import ImageFormat
  
  new_project.description = """The commercial is about this fancy product. The
                               client want us to have a shiny look with their
                               product bla bla bla..."""
  new_project.image_format = ImageFormat(name="HD 1080", width=1920, height=1080)
  new_project.fps = 25
  new_project.end = datetime.date(2011, 2, 15)
  new_project.lead = myUser

Lets save all the new data to the database::

  db.session.add(new_project)
  db.session.commit()

As you see, even though we have created multiple objects (new_project,
statuses, status lists etc.) we've just added the ``new_project`` object to the
database, but don't worry all the related objects will be added to the
database.

A Project generally contains :class:`~stalker.models.sequence.Sequence`\ s, so
lets create one, again we need to create a status list suitable for sequences
and a sequence should be initialized with a project instance::

  from stalker import Sequence
  
  seq_statuses = StatusList(
      name="Sequence Status List",
      statuses=[status_waiting,
                status_wip,
                status_stopped,
                status_complete],
      target_entity_type=Sequence,
  )
  
  seq1 = Sequence(
      name="Sequence 1",
      code="SEQ1",
      status_list = seq_statuses,
      project=new_project,
  )

And a Sequence generally has :class:`~stalker.models.shot.Shot`\ s::

  from stalker import Shot
  
  shot_statuses = StatusList(
      name="Shot Status List",
      statuses=[status_waiting,
                status_wip,
                status_stopped,
                status_pendrev,
                status_approved],
      target_entity_type=Shot,
  )
  
  sh001 = Shot(code="SH001", sequence=seq1, status_list=shot_statuses)
  sh002 = Shot(code="SH002", sequence=seq1, status_list=shot_statuses)
  sh003 = Shot(code="SH003", sequence=seq1, status_list=shot_statuses)

send them to the database::

  db.session.add_all([sh001, sh002, sh003])
  db.session.commit()

Part II/B - Querying, Updating and Deleting Data
================================================

So far we just created some simple data. What about updating them. Let say that
we created a new shot with wrong info::

  sh004 = Shot(code="SH005", sequence=seq1, status_list=shot_statuses)
  db.session.add(sh004)
  db.session.commit()

and you figured out that you have created and committed a wrong info and you
want to correct it::
  
  sh004.code = "SH004"
  db.session.commit()

but lets say that you don't have any variable holding the shot alread::
  
  # first find the data
  wrong_shot = db.query(Shot).filter_by(code="SH005").first()
  
  # now update it
  wrong_shot.code = "SH004"
  
  # commit the changes to the database
  db.session.commit()

and let say that you decided to delete the data::

  db.session.delete(wrong_shot)
  db.session.commit()

for more info about update and delete options (like cascades) in SQLAlchemy
please see the `SQLAlchemy documentation`_.

.. _SQLAlchemy documentation: http://www.sqlalchemy.org/docs/orm/session.html

Part III - Pipeline
===================

Up until now, we skipped a lot of stuff here to take little steps every time.
Eventough we have created users, departments, projects, sequences and shots,
Stalker still doesn't know much about our studio. For example, it doesn't have
any information about the **pipeline** that we are following and what steps we
do to complete those shots, thus to complete the project.

In Stalker, pipeline is managed by :class:`~stalker.models.task.Task`\ s. So
you create Tasks for Shots and then you can create dependencies between tasks.

So lets create a couple of tasks for one of the shots we have created before::

  from stalker import Task
  
  task_statuses = StatusList(
      name="Task Status List",
      statuses=[status_waiting,
                status_wip,
                status_pendrev,
                status_approved,
                status_complete],
      target_entity_type=Task
  )
  
  previs = Task(
      name="Previs of SH001",
      status_list=task_statuses,
      task_of=sh001
  )
  
  matchmove = Task(
      name="Matchmove of SH001",
      status_list=task_statuses,
      task_of=sh001
  )
  
  anim = Task(
      name="Animation",
      status_list=task_statuses,
      task_of=sh001
  )
  
  lighting = Task(
      name="Lighting",
      status_list=task_statuses,
      task_of=sh001
  )
  
  compositing = Task(
      name="Compositing",
      status_list=task_statuses,
      task_of=sh001
  )

Now create the dependecies::

  compositing.depends = [lighting]
  lighting.depends = [anim]
  anim.depends = [previs, matchmove]

For now the dependencies are only useful to have an information about the
relation of the tasks, but in the future releases of Stalker it is also going
to be used in the planned Project Scheduler.

Part IV - Task & Resource Management
====================================

Now we have a couple of Shots with couple of tasks inside it but we didn't
assign the tasks to anybody to let them finish this job.

Lets assign all this stuff to our self (for now :) )::

  previs.resources = [myUser]
  previs.effort = timedelta(days=1)
  
  matchmove.resources = [myUser]
  matchmove.effort = timedelta(days=2)
  
  anim.resources = [myUser]
  anim.effort = timedelta(2) # the default argument is days in timedelta
  
  lighting.resources = [myUser]
  lighting.effort = timdelta(hours=2)
  
  # one another way is to add the task to the users tasks
  # it will have the same effect of assign a user to a task
  myUser.tasks.append(comp)
  comp.effort = timedelta(days=2)

Now Stalker knows the hierarchy of the tasks. Next versions of Stalker will
have a ``Project Scheduler`` included to solve the task timings and create data
for things like Gantt Charts.

Lets commit the changes again::

  session.commit()

If you noticed, this time we didn't add anything to the session, cause we have
added the ``sh001`` in a previous commit, and because all the objects are
attached to this shot object in some way, all the changes has been tracked and
added to the database.

Part V - Asset Management
=========================

Now we have created a lot of things but other then storing all the data in the
database, we didn't do much. Stalker still doesn't have information about a lot
of things. For example, it doesn't know how to handle your asset versions
(:class:`~stalker.models.version.Version`) namely it doesn't know how to store
your data that you are going to create while completing this tasks.

So what we need to define is a place in our file structure. It doesn't need to
be a network shared directory but if you are not working alone than it means
that everyone needs to reach your data and the simplest way to do this is to
place your files in a network share or a SAN storage, there are other
alternatives like storing your files locally and sharing your revisions with a
Software Configuration Management (SCM) system. We are going to see the first
alternative, which uses a network share in our fileserver, and this network
share is called a :class:`~stalker.models.repository.Reposiory` in Stalker.

A repository is a file path, preferably a path which is mapped or mounted to
the same path on every computer in our studio. You can have several
repositories let say one for Commercials and another one for big Movie
projects. You can define repositories and assign projects to those
repositories. We have already created a repository while creating our first
project. But the repository has missing informations. A Repository object shows
the path that we create our projects into. Lets enter the paths for all the
major operating systems::
  
  commercial_repo.windows_path = "M:/PROJECTS"
  commercial_repo.linux_path   = "/mnt/M/PROJECTS"
  commercial_repo.osx_path     = "/Volumes/M/PROJECTS"

And if you ask for the path to a repository object it will always give the
correct answer according to your operating system::

  print repo1.path
  # under Windows outputs:
  # M:/PROJECTS
  # 
  # in Linux and variants:
  # /mnt/M/PROJECTS 
  # 
  # and in OSX:
  # /Volumes/M/PROJECTS
  #

.. note::
  Stalker always uses forward slashes no matter what operating system you are
  using.

Assigning this repository to our project is not enough, Stalker still doesn't
know about the project :class:`~stalker.models.structure.Structure`\ , or in
other words it doesn't have information about the folder structure about your
project. To explain the project structure we can use the
:class:`~stalker.models.structure.Structure` object::

  from stalker import Structure
  
  commercial_project_structure = Structure(
      name="Commercial Projects Structure",
      description="""This is a project structure, which can be used for simple
          commercial projects"""
  )
  
  # lets create the folder structure as a Jinja2 template
  custom_template = """
     {{ project.code }}
     {{ project.code }}/Assets
     {{ project.code }}/References/Storyboard
     {{ project.code }}/References/Videos
     {{ project.code }}/References/Images
     {{ project.code }}/Sequences"
     
     {% if project.sequences %}
         {% for sequence in project.sequences %}
             {% set seq_path = project.code + '/Sequences/' + sequence.code %}
             {{ seq_path }}
             {{ seq_path }}/Edit
             {{ seq_path }}/Edit/AnimaticStoryboard
             {{ seq_path }}/Edit/Export
             {{ seq_path }}/Shots
             
             {% if sequence.shots %}
                 {% for shot in sequence.shots %}
                     {% set shot_path = seq_path + '/SHOTS/' + shot.code %}
                     {{ shot_path }}
                 {% endfor %}
             {% endif %}
             
         {% endfor %}
     
     {% endif %}
     
     {{ project.code }}/References
  """
  
  commercial_project_structure.custom_template = custom_template
  
  # now assign this structure to our project
  new_project.structure = commercial_project_structure

Now we have entered a couple of `Jinja2`_ directives as a string. This template
will be used when creating the project structure.

.. :: by calling
  :func:`~stalker.models.project.Project.create`. It is safe to call the
  :func:`~stalker.models.project.Project.create` over and over or whenever you've
  added new data that will add some extra folders to the project structure.

.. _Jinja2: http://jinja.pocoo.org/

The above template will produce the following folders for our project::

  M:/PROJECTS/FANCY_COMMERCIAL
  M:/PROJECTS/FANCY_COMMERCIAL/Assets
  M:/PROJECTS/FANCY_COMMERCIAL/References
  M:/PROJECTS/FANCY_COMMERCIAL/References/Videos
  M:/PROJECTS/FANCY_COMMERCIAL/References/Images
  M:/PROJECTS/FANCY_COMMERCIAL/Sequences
  M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1
  M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Edit
  M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Edit/AnimaticStoryboard
  M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Edit/Export
  M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Storyboard
  M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Shots
  M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Shots/SH001
  M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Shots/SH002
  M:/PROJECTS/FANCY_COMMERCIAL/Sequences/SEQ1/Shots/SH003

We are still not done with defining the templates. Even though Stalker now
knows what is the project structure like, it is not aware of the placements of
individual :class:`~stalker.models.version.Version` files specific for a Task.
A :class:`~stalker.models.version.Version` is an object holding information
about every single iteration of one Task and has a connection to files in the
repository.

So before creating a new version for any kind of task, we need to tell Stalker
where to place the related files. This can be done by using a
:class:`~stalker.models.template.FilenameTemplate` object.

A :class:`~stalker.models.template.FilenameTemplate` object has information
about the path, the filename, and the target entity type to apply this template
to::

  from stalker import FilenameTemplate
  
  shot_version_template = FilenameTemplate(
      name="Shot Template",
      target_entity_type=Shot
  )
  
  # lets create the templates
  #
  # task = version.task
  # shot = task.part_of
  # asset = task.part_of
  # try:
  #     sequence = shot.sequence
  # except AttributeError:
  #     sequence = asset.sequences[0]
  # 
  # task_type = task.type
  # user = auth.get_user()
  #
  
  path_code = "Sequences/{{ sequence.code }}/Shots/{{ shot.code }}/{{ task_type.code }}"
  filename_code = "{{ shot.code }}_{{ version.take }}_{{ task_type.code }}_v{{ version.version }}"
  
  shot_version_template.path_code = path_code
  shot_version_template.filename_code = filename_code
  
  # now assign this template to our project structure
  # do you save the "structure1" we have created before
  commercial_project_structure.templates.append(shot_version_template)

Now Stalker knows "Kung-Fu". It can place any version related file to the
repository and organise your works. You can define all the templates for all
your entities independently.

Part VI - Collaboration (coming)
================================

We came a lot from the start, but what is the use of an Production Asset
Management System if we can not communicate with our colleagues.

In Stalker you can communicate with others in the system, by:
  
  * Leaving a :class:`~stalker.models.note.Note` to anything created in
    Stalker (except to notes and tags, you can not create a note to a note and
    to a tag)
  * Sending a :class:`~stalker.models.message.Message` directly to them or
    to a group of users
  * Anyone can create :class:`~stalker.models.ticket.Ticket`\ s to a
    :class:`~stalker.models.version.Version`

Part VII - Session Management (coming)
======================================

This part will be covered soon

Part VIII - Extending SOM (coming)
==================================

This part will be covered soon
