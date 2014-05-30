.. _design_toplevel:

======
Design
======

The design of Stalker is mentioned in the following sections.

Introduction
============

Stalker is an Open Source Production Asset Management Library. Although it is
designed VFX and Animation studios in mind, its flexible Project Management
muscles will allow it to be used in a wide variety of fields.

An Asset Management Systems' duty is to hold the data which are created by the
users of the system in an organised manner, and let them quickly reach and find
their files. A Production Asset Management Systems' duty is, in addition to the
asset management systems', also handle the production steps or tasks and
allow the users of the system to collaborate. If more information about this
subject is needed, there are great books about Digital Asset Management (DAM)
Systems.

The usage of an asset management system in an animation/vfx studio is a must
for the sake of the studio itself. Even the benefits of the system becomes
silly to be mentioned when compared to the lack of even a simple system to
organise stuff.

Every studio outside establishes and develops their own asset management
system. Stalker will try to be the framework that these proprietary asset
management systems will be build over. Thus reducing the work repeated on every
big projects' start.

Concepts
========

There are a couple of design concepts those needs to be clarified before any
further explanation of Stalker.

Stalker on itself basically is the **Model** in an **MTV** system (where the
`Stalker Pyramid`_ is the *Template* and *View*). So it defines the data and
the interaction of the data with itself.

Because the idea behind Stalker was to build an open source library that any
studio using it can build their own pipeline on top of it, it is designed to
stay simple and solid at the same time. So the UI and other stuff is ripped off
from the original Stalker package and moved to another Pyramid web application
called `Stalker Pyramid`_.

.. _`Stalker Pyramid`: https://pypi.python.org/pypi/stalker_pyramid

Stalker Object Model (SOM)
--------------------------

Stalker has a very robust object model, which is called
**Stalker Object Model** or **SOM**. The idea behind SOM is to create a class
hierarchy which is both usable right out of the box and also expandable by the
studios' developers. SOM is actually a little bit more complex than a basic
possible model, it is designed in this way just to be able to create a simple
pipeline to be able to build the system over it.

Lets look at how a simple studio works and try to create our asset management
concepts around it.

An animation/vfx studios duty is to complete a :class:`.Project`. A project,
generally is about to create a :class:`.Sequence` of :class:`.Shot`\ s which
are a series of images those at the end converts to a movie. So a sequence in
general contains Shots. And Shots can use :class:`.Asset`\ s. So basically to
complete a project the studio should complete the shots and assets needed by
those shots.

Furthermore all the Projects, Sequences, Shots or Assets are divided in to
different :class:`.Task`\ s those need to be done sequentially or in parallel
to complete that project.

A Task relates to a work, a work is a quantity of time spent or going to be
spend for that specific task. The time spent on the course of completion of a
Task can be recorded with :class:`.TimeLog`\ s. TimeLogs show the total time
spent by an artist for a certain Task. So it holds information about how much
**effort** has been spent to complete a Task.

During the completion of the Task or at the end of the work a **User** creates
:class:`.Versions` for that particular Task. Versions are the different
incarnations or the progress of the resultant product, and it is connected to
files in the fileserver or in Stalkers term the :class:`.Repository`.

All the names those shown in bold fonts are a class in SOM. and there are a
series of other classes to accommodate the needs of a :class:`.Studio`.

The inheritance diagram of the classes in the SOM is shown below:

.. include:: inheritance_diagram.rst

Stalker is a configurable and expandable and most importantly it is an
open source system. All of these features allows the system to have a flexible
structure.

There are two levels of expansion, the first level is the simplest one, by just
adding different statuses, different types or these kind of things in
which Stalker's current design is ready to. This is explained in `How To
Customize Stalker`_.

The second level of expansion is achieved by expanding the SOM. Expanding the
SOM includes creating new classes and database tables, and updating the old
ones which are already coming with Stalker. These expansion schemes are
further explained in `How To Extend SOM`_.

Features
--------

 1. Developed purely in Python (2.6 and over) using TDD (Test Driven
    Development) practices

 2. SQLAlchemy for the database back-end and ORM

 3. Uses Jinja2 as the template system for the file and folder naming
    convention, it is possible to use templates like:

    {repository.path}/{project.code}/Assets/{asset.type.name}/{asset.code}/
    {asset.name}_{asset.type.name}_v{version.version_number}.{version.extension}
 
 4. File and folders and file sequences can be uploaded to the server as
    assets, and the server decides where to place the folder or file by using
    the template system.

 5. The event system gives full control for every CRUDL (create/insert, read,
    update, delete and list) by giving step like before insert, after insert
    call-backs.
 
 6. The messaging system allows the users collaborate efficiently.

 7. Has an embedded Ticket system.

 8. Uses TaskJuggler as the task management backend and supports basic Task
    attributes.

 9. Has a predefined workflow for task statuses called Task Status Workflow
    which manages the statuses of a Task during the project completion.

For usage examples see :ref:`tutorial_toplevel`\ .

How To Customize Stalker
========================

This part explains the customization of Stalker.


How To Extend SOM
=================

This part explains how to extend Stalker Object Model or SOM.

Creating Data
=============

There are some examples here, to create simple data.

Creating a Project
------------------

To create a Project, we need:

1. A Repository
2. A Structure object to define the file structure of the Project:
3. FilenameTemplates for Task, Asset, Shot, Sequence types, to define the
   placement of the Versions created for them.
4. An ImageFormat to define the output size of the project.
5. A StatusList with enough Statuses that will define the desired Project
   Statuses. Stalker doesn't have a Project Status Workflow, yet! so define
   yours.
6. If desired we can also add a Type for the Project to distinguish commercials
   from Feature Film projects.
7. We need to create a user as the lead for the project.

Here is the code::

  from stalker import (db, Repository, Structure, FilenameTemplate, StatusList,
                       Status, Task, User)

  # first setup the database connection (assuming that you have a config.py
  # defined, so we do not need to supply a database address)
  db.setup()
  
  # initialize the database just for the first time
  db.init()  # run this only for the first time, subsequent runs will not
             # create any errors, but it is unnecessary

  # re-use Statuses NEW, WIP and CMPL from default statuses
  status_new = Status.query.filter_by(code='NEW').first()
  status_wip = Status.query.filter_by(code='WIP').first()
  status_cmpl = Status.query.filter_by(code='CMPL').first()
  
  # and create a new one
  status_on_air = Status(name='On Air', code='OA')

  # status list for project
  project_status_list = StatusList(
      name='Project Statuses',
      target_entity_type='Project',
      statuses=[
          status_new,
          status_wip,
          status_cmpl,
          status_on_air
      ],
  )

  image_format_hd = ImageFormat(
      name="HD",
      width=1920,
      height=1080,
  )

  commercial_type = Type(
    name='Commercial',
    code='COMM',
    target_entity_type='Project'
  )

  repo = Repository(
      name='Commercials Repo',
      linux_path='/mnt/T/Commercials/',
      windows_path='T:/Commercials/',
      osx_path='/Volumes/T/Commercials/'
  )

  commercial_structure = Structure(
      name='Commercial Project Structure',
      code=''
  )

  lead = User(
      name='Erkan Ozgur Yilmaz',
      login='eoyilmaz',
      email='eoyilmaz@stalker.com',
      password='secret'
  )

  # lets create the Project
  proj1 = Project(
      name='Test Project',
      code='TP',
      description="This is the first project",
      lead=lead,
      image_format=image_format_hd,
      fps=25,
      type=commercial_type,
      structure=commercial_structure,
      repository=repo,
      status_list=project_status_list,
      status=status_new
  )

  # just add the project to the database
  db.DBSession.add(proj1)

  # and commit the data to database
  db.DBSession.commit()

It may seem too much for just creating a Project, but it is for the first time
only. For a second project, we can use the previous Repository, Structure,
Lead, StatusList etc.

Create a Task
-------------

Because we have a project now lets create a task for this project::

  # connect to the database if you have not done yet
  db.setup()

  # create a new user as the resource for the task
  resource1 = User(
      name='User1',
      login='user1',
      email='user@users.com',
      password='secret'
  )

  # now create the task
  task1 = Task(
      name='Task1',
      description="This is our first Task, and it is about, creating "
                  "something fancy",
      resources=[resource1],
      schedule_timing=1,
      schedule_unit='d',
      schedule_model='effort',
      project=proj1
  )
  # we do not need to supply a StatusList for the Task, statuses for tasks are
  # created by default when we called db.init() in previous example

  # add it to the database
  db.DBSession.add(task1)

  # and commit
  db.DBSession.commit()

Now we have created a simple Task and assigned it to the resource1. Lets check
the status of the Task::

  print(task1.status)
  # this should print something like <Ready To Start (RTS) (Status)>
  # stating that our task is ready to start working on.

