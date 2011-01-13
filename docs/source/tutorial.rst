Tutorial
********

Introduction
============

Using Stalker is all about interacting with a database by using the Stalker
Object Model. Stalker uses the powerfull `SQLAlchemy ORM`_.

.. _SQLAlchemy ORM: http://www.sqlalchemy.org/docs/orm/tutorial.html
 
This tutorial section let you familiarise with the Stalker Python API and
Stalker Object Model (SOM). If you used SQLAlchemy before you will feel at
home and if you aren't you will see that it is fun dealing with databases with
SOM.

Tutorial Part I - Basics
========================

Lets say that we just installed Stalker (as you are right now) and want to use
Stalker in our first project.

The first thing we are going to learn about is the to how to connect to the
database (default in-memory database nothing else is setup) so we can enter
information about our studio.

We are going to use the helper script to connect to the default database. Use
the following command to connect to the database::

  from stalker import db
  db.setup()

This will create an in-memory SQLite3 database, which is useless other than
testing purposes. To be able to get more out of Stalker we should give a proper
database information. The basic setup is to use a file based SQLite3 database::

  db.setup("sqlite:///M:\\studio.db") # assumed Windows

This command will do the following:
 1. setup the database connection, by creating an `engine`_
 2. create the SQLite3 database file if doesn't exist
 3. create a `session`_ instance
 4. do the `mapping`_
 
.. _session: http://www.sqlalchemy.org/docs/orm/session.html
.. _engine: http://www.sqlalchemy.org/docs/core/engines.html
.. _mapping: http://www.sqlalchemy.org/docs/orm/mapper_config.html

Lets continue by creating a user for yourself in the database. The first thing
we need to do is to import the :class:`~stalker.core.models.user.User` class in
to the current namespace::

  from stalker.core.models.user import User

then create the :class:`~stalker.core.models.user.User` object::

  myUser = User(first_name="Erkan Ozgur",
                last_name="Yilmaz",
                login_name="eoyilmaz",
                email="eoyilmaz@gmail.com",
                password="secret")

Then lets add a new :class:`~stalker.core.models.department.Department` object
to define your department::

  from satlker.core.models.department import Department
  tds_department = Department(name="TDs")

Now add your user to the department::

  tds_department.members.append(myUser)

We have created succesfully a :class:`~stalker.core.models.user.User` and a
:class:`~stalker.core.models.department.Department` and we assigned the user as
one of the member of the *TDs Department*.

For now, because we didn't tell Stalker to commit the changes, no data is saved
to the database. But it doesn't keep us using Stalker, as if these information
are in the database already. Lets show this by querying all the departments,
then getting the first one and gettings its first members name::

  print db.query(Department).first().members[0].first_name

this should print out "Erkan Ozgur". So even though we didn't commit the data
to the database, Stalker lets us use the ``db.query`` to get objects out of the 
database.

So lets send all these data to database::
  
  db.session.add(myUser)
  db.session.commit()

If you noticed, we have just added ``user1`` to the database and Stalker will
add all the connected object (like the department) to the database too.

Tutorial Part II - Getting Hot
==============================

Lets say that we have this new project comming and you want to start using
Stalker with it, lets create a :class:`~stalker.core.models.project.Project`
object for it::

  from stalker.core.models.project import Project
  new_project = Project(name="Funny Commercial")

Lets enter more information about this new project::

  from datetime import datetime
  from stalker.core.models.imageFormat import ImageFormat
  
  new_project.image_format = ImageFormat(name="HD 1080", width=1920, height=1080)
  new_project.fps = 25
  new_project.due = datetime(2011,2,15)
  new_project.lead = myUser

You can group projects by their types, by using a
:class:`~stalker.core.models.types.ProjectType` object::

  from stalker.core.models.types import ProjectType
  
  commercial_project_type = ProjectType(name="Commercial")
  new_project.type = commercial_project_type

To save all the data to the database::

  db.session.add(new_commercial)
  db.session.commit()

Again we've just added the ``new_project`` object to the database but Stalker
is smart enough to add all the connected objects to it.

Project objects contains :class:`~stalker.core.models.sequence.Sequence`
objects, so lets create one::

  from stalker.core.models.sequence import Sequence
  seq1 = Sequence(name="Sequence 1", code="SEQ1")
  
  # add it to the project
  new_project.sequences.append(seq1)

And Sequences contains :class:`~stalker.core.models.shot.Shot` objects::

  from stalker.core.models.shot import Shot
  
  sh001 = Shot(name="Shot 1", code="SH001")
  sh002 = Shot(name="Shot 2", code="SH002")
  sh003 = Shot(name="Shot 3", code="SH003")
  
  # assign them to the sequence
  seq1.shots.extend([sh001, sh002, sh003])

Tutorial Part III - Pipeline
============================

Infact we skipped a lot of stuff here to take little steps every time, for
example Stalker doesn't know much about the pipeline of those shots.

To simply specify the *Pipeline* we should create a couple of
:class:`~stalker.core.models.pipelineStep.PipelineStep`\ s and assign them to
an :class:`~stalker.core.models.types.AssetType` to group the same kind of
shots and make it easy next time to create that kind a shot::

  from stalker.core.models.pipelineStep import PipelineStep
  from stalker.core.models.types import AssetType
  
  # create the pipeline steps of a particular Shot asset
  previz    = PipelineStep(name="Previz"     , code="PRE")
  matchmove = PipelineStep(name="Match Move" , code="MM")
  anim      = PipelineStep(name="Animation"  , code="ANIM")
  light     = PipelineStep(name="Ligting"    , code="LIGHT")
  comp      = PipelineStep(name="Compositing", code="COMP")
  
  simple_shot_pipeline_steps = [previz, match, anim, light, comp]
  
  # assign them as the steps of "Shot" assets
  shot_asset_type = AssetType(name="Shot", steps=shot_pipeline_steps)
  
  # and set our shot objects asset_type to stho_asset_type
  # 
  # instead of writing down shot1.type = shot_asset_type
  # we are going to do something more interesting
  for shot in seq1.shots:
      shot.type = shot_asset_type

So by doing that we inform Stalker about the possible steps about one kind of
asset (*Shot* in our case).




