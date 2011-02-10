========
Tutorial
========

Introduction
============

Using Stalker is all about interacting with a database by using the Stalker
Object Model. Stalker uses the powerfull `SQLAlchemy ORM`_.

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

  db.setup("sqlite:///M:\\studio.db") # assumed Windows

This command will do the following:
 1. setup the database connection, by creating an `engine`_
 2. create the SQLite3 database file if doesn't exist
 3. create a `session`_ instance
 4. do the `mapping`_
 
.. _session: http://www.sqlalchemy.org/docs/orm/session.html
.. _engine: http://www.sqlalchemy.org/docs/core/engines.html
.. _mapping: http://www.sqlalchemy.org/docs/orm/mapper_config.html

Lets continue by creating a **User** for ourselfs in the database. The first
thing we need to do is to import the :class:`~stalker.core.models.user.User`
class in to the current namespace::

  from stalker.core.models.user import User

then create the :class:`~stalker.core.models.user.User` object::

  myUser = User(first_name="Erkan Ozgur",
                last_name="Yilmaz",
                login_name="eoyilmaz",
                email="eoyilmaz@gmail.com",
                password="secret",
                description="This is me")

Our studio possibly has **Departments**. Lets add a new
:class:`~stalker.core.models.department.Department` object to define your
department::

  from satlker.core.models.department import Department
  tds_department = Department(name="TDs",
                              description="This is the TDs department")

Now add your user to the department::

  tds_department.members.append(myUser)

We have created succesfully a :class:`~stalker.core.models.user.User` and a
:class:`~stalker.core.models.department.Department` and we assigned the user as
one of the member of the **TDs Department**.

For now, because we didn't tell Stalker to commit the changes, no data has been
saved to the database yet. But it doesn't keep us using Stalker, as if these
information are in the database already. Lets show this by querying all the
departments, then getting the first one and gettings its first members name::

  all_departments = db.query(Department).all()
  all_members_of_dep = all_departments[0].members
  print all_members[0].first_name

this should print out "Erkan Ozgur". So even though we didn't commit the data
to the database, Stalker lets us use the ``db.query`` to get objects out of the 
database.

So lets send all these data to database::
  
  db.session.add(myUser)
  db.session.add(tds_department)
  db.session.commit()

Now all the data is persisted in the database.

Part II - Creating Simple Data
==============================

Lets say that we have this new project comming and you want to start using
Stalker with it. So create a :class:`~stalker.core.models.project.Project`
object to hold data about it::

  from stalker.core.models.project import Project
  new_project = Project(name="Fancy Commercial")

Lets enter more information about this new project::

  from datetime import datetime
  from stalker.core.models.imageFormat import ImageFormat
  
  new_project.description = """The commercial is about this fancy product. The
                               client want us to have a shinny look with their
                               product bla bla bla..."""
  new_project.image_format = ImageFormat(name="HD 1080", width=1920, height=1080)
  new_project.fps = 25
  new_project.due = datetime(2011,2,15)
  new_project.lead = myUser

Grouping your projects by their types is one of the best thing that lets you
filter them later. Think about querying "Commercials" and distinguishing them
from the "Movie" projects or "Print" projects. To accomplish this you can use a
:class:`~stalker.core.models.types.ProjectType` object::

  from stalker.core.models.types import ProjectType
  
  commercial_project_type = ProjectType(name="Commercial")
  new_project.type = commercial_project_type

To save all the data to the database::

  db.session.add(new_project)
  db.session.commit()

Eventhough we have created multiple objects (new_project,
commercial_project_type) we've just added the ``new_project`` object, don't
worry Stalker is smart enough to add all the connected objects to the database.

A Project generally contains :class:`~stalker.core.models.sequence.Sequence`\
s, so lets create one::

  from stalker.core.models.sequence import Sequence
  seq1 = Sequence(name="Sequence 1", code="SEQ1")
  
  # add it to the project
  new_project.sequences.append(seq1)

And a Sequence generally has :class:`~stalker.core.models.shot.Shot`\ s::

  from stalker.core.models.shot import Shot
  
  sh001 = Shot(name="Shot 1", code="SH001")
  sh002 = Shot(name="Shot 2", code="SH002")
  sh003 = Shot(name="Shot 3", code="SH003")
  
  # assign them to the sequence
  seq1.shots.extend([sh001, sh002, sh003])

Part III - Pipeline
===================

Until now, we skipped a lot of stuff here to take little steps every time.
Eventough we have created users, departments, projects, sequences and shots,
Stalker still doesn't know much about our studio. For example, it doesn't have
any information about the pipeline that we are following and what steps we do
to complete those shots, thus to complete the project.

Lets try to explain the **Shot Pipeline** we are following to Stalker.

A pipeline is a group of
:class:`~stalker.core.models.pipelineStep.PipelineStep`\ s. And we follow these
steps for one specific :class:`~stalker.core.models.types.AssetType`. So a
**Shot** has a different pipeline than a **Character** or an **Environment**
asset.

Lets create the pipeline steps we need::
  
  from stalker.core.models.pipelineStep import PipelineStep
  
  previs      = PipelineStep(name="Previs"     , code="PREVIS")
  matchmove   = PipelineStep(name="Match Move" , code="MM")
  anim        = PipelineStep(name="Animation"  , code="ANIM")
  layout      = PipelineStep(name="Layout"     , code="LAYOUT")
  light       = PipelineStep(name="Ligting"    , code="LIGHT")
  comp        = PipelineStep(name="Compositing", code="COMP")




.. will think about this part later, it is making the tutorial unnecessarily
   complex
    
    design      = PipelineStep(name="Design"     , code="DESIGN")
    model       = PipelineStep(name="Model"      , code="MODEL")
    rig         = PipelineStep(name="Rig"        , code="RIG")
    shading     = PipelineStep(name="Shading"    , code="SHADING")
    matte_paint = PipelineStep(name="Matte Paint", code="MATTE")




and create a the Shot asset type::
  
  from stalker.core.models.types import AssetType
  
  # the order of the PipelineSteps are not important
  shot_pSteps = [previs, match, anim, layout, light, comp]
  
  # create the asset type
  shot_asset_type = AssetType(name="Shot", steps=shot_pSteps)
  
  # and set our shot objects asset_type to shot_asset_type
  # 
  # instead of writing down shot1.type = shot_asset_type
  # we are going to do something more interesting
  # (eventhough it is inefficient)
  
  for shot in seq1.shots:
      shot.type = shot_asset_type
  
  
  
  
.. this part is make things complex
  from stalker.core.models.types import AssetType
  
  # the order of the PipelineSteps are not important
  simple_shot_pSteps = [previs, match, anim, layout, light, comp]
  character_pSteps   = [design, model, rig, shading]
  prop_pSteps        = [design, model, shading]
  env_pSteps         = [design, model, shading, matte_paint]
  
  # create the asset types
  shot_asset_type      = AssetType(name="Shot"       , steps=shot_pSteps)
  character_asset_type = AssetType(name="Character"  , steps=character_pSteps)
  prop_asset_type      = AssetType(name="Prop"       , steps=prop_pSteps)
  env_asset_type       = AssetType(name="Environment", steps=env_pSteps)
  
  # and set our shot objects asset_type to shot_asset_type
  # 
  # instead of writing down shot1.type = shot_asset_type
  # we are going to do something more interesting
  for shot in seq1.shots:
      shot.type = shot_asset_type




So by doing that we informed Stalker about the steps of one kind of asset
(**Shot** in our case).

Part IV - Task & Resource Management
====================================

Now we have a couple of Shots with couple of steps inside it but we didn't
created any :class:`~stalker.core.models.task.Task` to let somebody to finish
this job.

Lets assign all this stuff to our self (for now)::

  from datetime import timedelta
  from stalker.core.models.task import Task
  
  previs_task = Task(
                    name="Previs",
                    resources=[myUser],
                    bid=timedelta(days=1),
                    pipeline_step=previs
                )
  
  mm_task     = Task(
                    name="Match Move",
                    resources=[myUser],
                    bid=timedelta(days=2),
                    pipeline_step=matchmove
                )
  
  anim_task   = Task(
                    name="Animation",
                    resources=[myUser],
                    bid=timedelta(days=2),
                    pipeline_step=anim
                )
  
  layout_task = Task(
                    name="Layout",
                    resources=[myUser],
                    bid=timdelta(hours=2),
                    pipeline_step=layout
                )
  
  light_task  = Task(
                    name="Lighting",
                    resources=[myUser],
                    bid=timedelta(days=2),
                    pipeline_step=light
                )
  
  comp_task   = Task(
                    name="Compositing",
                    resources=[myUser],
                    bid=timedelta(days=2),
                    pipeline_step=comp
                )

Now we are created all the tasks, but they are not connected to our Shots yet.
Lets connect them to the ``shot001``::
  
  sh001.tasks = [previs_task,
                 mm_task,
                 anim_task,
                 layout_task,
                 light_task,
                 comp_task]

And one of the good sides of the tasks are, dependencies can be defined between
them, so Stalker nows which job should be done before the others::
  
  # animation needs match moving and previs to be finished
  anim_task.depends = [mm_task, previs_task]
  
  # compositing can not start before anything rendered or animated
  comp_task.depends = [light_task, anim_task]
  
  # lighting can not be done before the layout is finished
  light_task.depends = [layout_task]

Now Stalker nows the hierarchy of the tasks. Next versions of Stalker will have
a ``Scheduler`` included to solve the task timings and create data for things
like Gantt Charts.

Lets commit the changes again::

  session.commit()

If you noticed, this time we didn't add anything to the session, cause we have
added the ``new_project`` in a previous commit, and because all the objects are
attached to the project object in some way, Stalker can track this changes and
add the missing related objects to the database.

Part V - Asset Management
=========================

Now we have created a lot of things but other then storing all the data in the
database, we didn't do much. Stalker still doesn't have information about a lot
of things. For example, it doesn't know how to handle your asset versions
(:class:`~stalker.core.models.version.Version`) namely it doesn't know how to
store your data that you are going to create while completing this tasks.

A fileserver in Stalkers' term is called a
:class:`~stalker.core.models.repository.Repository`. Repositories stores the
information about the fileservers in your system. You can have several file
servers let say one for Commercials and other one for big Movie projects. You
can define repositories and assign projects to those repositories. Lets create
one repository for our commercial project::

  from stalker.core.models.repository import Repository
  repo1 = Repository(
      name="Commercial Repository",
      description="""This is where the commercial projects are going to be
      stored"""
  )


A Repository object could show the root path of the repository according to
your operating system. Lets enter the paths for all the major operating
systems::
  
  repo1.windows_path = "M:\\PROJECTS"
  repo1.linux_path   = "/mnt/M"
  repo1.osx_path     = "/Volumes/M"

And if you ask a repository object for the path of the repository it will
always give the correct answer accroding to your operating system::

  print repo1.path
  # outputs:
  # if you are running the command on a computer with Windows it will output:
  #
  # M:\PROJECTS
  # 
  # and for Linux:
  # /mnt/M 
  # 
  # for OSX:
  # /Volumes/M
  #

Assigning this repository to our project or vice versa is not enough, Stalker
still doesn't know about the project
:class:`~stalker.core.models.structure.Structure`\ , or in other words it
doesn't have information about the folder structure about your project. To
explain the project structure we can use the
:class:`~stalker.core.models.structure.Structure` object::

  from stalker.core.models.structure import Structure
  
  commercial_project_structure = Structure(
      name="Commercial Projects Structure",
      description="""This is a project structure, which can be used for simple
          commercial projects"""
  )
  
  # lets create the folder structure as a Jinja2 template
  project_template = """
     {{ project.code }}
     {{ project.code }}/Assets
     {{ project.code }}/Sequences"
     
     {% if project.sequences %}
         {% for sequence in project.sequences %}
             {% set seq_path = project.code + '/Sequences/' + sequence.code %}
             {{ seq_path }}
             {{ seq_path }}/Edit
             {{ seq_path }}/Edit/AnimaticStoryboard
             {{ seq_path }}/Edit/Export
             {{ seq_path }}/Storyboard
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
  
  commercial_project_structure.project_template = project_template
  
  # now assign this structure to our project
  new_project.structure = commercial_project_structure
  
  
Now we have entered a couple of `Jinja2`_ directives as a string. This template
will be used when creating the project structure by calling
:func:`~stalker.core.models.project.Project.create`. It is safe to call the
:func:`~stalker.core.models.project.Project.create` over and over or whenever
you've added new data that will add some extra folders to the project
structure.

.. _Jinja2: http://jinja.pocoo.org/

The above template will produce the following folders for our project::

  M:/PROJECTS/FANCY_COMMERCIAL
  M:/PROJECTS/FANCY_COMMERCIAL/Assets
  M:/PROJECTS/FANCY_COMMERCIAL/References
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
indivudual asset :class:`~stalker.core.models.version.Version` files specific
for an :class:`~stalker.core.models.types.AssetType`. An asset
:class:`~stalker.core.models.version.Version` is an object holding information
about every single iteration of one asset and has a connection to files in the
repository. So before creating a new version for any kind of asset, we need to
tell Stalker where to place the related files. This can be done by using a
:class:`~stalker.core.models.types.TypeTemplate` object.

A :class:`~stalker.core.models.types.TypeTemplate` object has information about
the path, the filename, and the Type of the asset to apply this template to::

  from stalker.core.models.types import TypeTemplate
  
  shot_version_template = TypeTemplate(name="Shot Template")
  
  
  # lets create the templates
  #
  # shot = version.asset
  # asset = version.asset
  # if shot is not None:
  #     sequence = shot.sequence
  # task = version.task
  # pipeline_step = task.pipeline_step
  # user = auth.get_user()
  # 
  path_code = "Sequences/{{ sequence.code }}/Shots/{{ shot.code }}/{{ pipeline_step.code }}"
  filename_code = "{{ shot.code }}_{{ version.take }}_{{ pipeline_step.code }}_v{{ version.version }}"
  
  # we can use the shot_asset_type we have previously defined
  shot_version_template.type = shot_asset_type
  shot_version_template.path_code = path_code
  shot_version_template.filename_code = filename_code
  
  # now assign this template to our project structure
  # do you remember the "structure1" we have created before
  commercial_project_structure.assetTemplates.append(shot_version_template)

Now Stalker knows "Kung-Fu". It can place any version related file to the
repository and orginize your works. You can define all the templates for all
your assetTypes independently, or you can use a common template for them etc.

Part VI - Collaboration
=======================

We came a lot from the start, but what is the use of an Production Asset
Management System if we can not communicate with our colleagues.

In Stalker you can communicate with others in the system, by:
  
  * Leaving a :class:`~stalker.core.models.note.Note` to anything created in
    Stalker (except to notes and tags, you can not create a note to a note and
    to a tag)
  * Sending a :class:`~stalker.core.models.message.Message` directly to them or
    to a group of users
  * If you are a lead of a project or a sequence, then by placing a
    :class:`~stalker.core.models.review.Review` to their works

Part VII - Session Management (comming)
=======================================

This part will be covered soon

Part VIII - Extending SOM (commming)
====================================

This part will be covered soon