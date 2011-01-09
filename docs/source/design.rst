Design
******

The design of Stalker is mentioned in the following sections.

Mission
=======

The project is about creating an Open Source Production Asset Management
(ProdAM) System called Stalker which is designed for Vfx/Animation Studios.
Stalker will be consisting of a framework and the interface those has been
build over that framework. Stalker will have a very flexible object model
design that lets the pipeline TDs to customize it in a wide variety of
perspectives. The out of the package installation will meet the basic needs of
majority of studios without too much effort.

Introduction
============

An Asset Management Systems' duty is to hold the data which are created by the
users of the system in an orginized manner, and let them quickly reach and find
their files. A Production Asset Management Systems' duty is, in addition to the
asset management systems', also handle the production steps and collaboration
of the users. If more information about this subject is needed, there are great
books about Digital Asset Management (DAM) Systems.

The usage of an asset management system in an animation/vfx studio is an
obligatory duty for the sake of the studio itself. Even the benefits of the
system becomes silly to be mentioned when compared to the lack of even a simple
system to organize stuff.

Every studio outside establishes and developes their own asset management
system. Stalker will try to be the framework that these proprietry asset
management systems will be build over. Thus reducing the work repeated on every
big projects start.

Concepts
========

There are a couple of design concepts those needs to be clarified before any
further explanation of Stalker.

Stalker Object Model (SOM)
--------------------------

Stalker has a very robust object model, which is called **Stalker Object
Model** or **SOM**. The idea behind SOM is to create a simple class hierarchy
which is both usable right out of the box and also expandable by the studios'
pipeline TDs. SOM is actually a little bit more complex than the basic possible
model, it is designed in this way just to be able to create a simple pipeline
to be able to build the system on it.

Lets look at how a simple studio works and try to create our asset management
concepts around it.

An animation/vfx studios duty is to complete a **Project**. A project,
generally is about to create a **Sequence** of **Shots** which are a series of
images those at the end converts to a movie. So a sequence in general contains
Shots. Shots are a special type of **Assets** which are related to a range of
time. So basically to complete a project the studio should complete the
sequences thus the shots.

We have considered Shots as a special form of assets, so assets have
**AssetTypes**, it is *Shot* for a Shot asset, and lets say, it is *Character*
for a character asset, or *Vehicle* for a vehicle asset (pretty straight).

AssetType also defines the **PipelineSteps** of that special asset type. For
example a Shot can have steps like *Animation*, *FX*, *Layout*, *Lighting*,
*Compositing* etc. and a character can have *Design*, *Model*, *Rig*, *Shading*
steps. All these steps defines differentiable **Tasks** those need to be done
sequently or in parallel to complete that shot or asset. Again, an asset or
shot has an asset type, which defines the steps thus tasks those needs to be
done.

A Task relates to a work, a work is a quantity of time spend or going to be
spend for that specific task. At the end of the work generally a **User**
creates **Versions** for a task. Versions are list of files showing the
different incarnations or the progress of a subject in the fileserver or in
Stalkers term the **Repository**. Also while creating those files to complete
the tasks a user should be booked. **Bookings** are special type of objects
holds information about how much time has been spent for a given task.

All the names those shown in bold fonts are a class in SOM. and there are a
series of other classes to accomodate the needs of a simple studio.

The inheritance diagram of the classes in the SOM is shown below:

.. include:: inheritance_diagram.rst

Stalker is a configurable and expandible system. Both of these feature allows
the system to have a flexible structure.

There are two levels of expansion, the first level is the simplest one, by just
adding different statuses, different assetTypes or these kind of things in
which Stalker's current design is ready to.

The second level of expansion is achieved by expanding the SOM. Expanding the
some includes creating new classes and database tables, and updating the old
ones which are already comming with Stalker. These expansion schemes are
further explained in How To Expand Stalker.

Features and Requirements
-------------------------
Features:

 1. Developed purely in Python (2.6 and over) using TDD (Test Driven
    Development) practices
 
 2. SQLAlchemy for the database back-end and ORM
 
 3. PyQt/PySide and web based user interfaces. All the interfaces designed in
    MVC structure.
 
 4. Jinja2 as the template engine
 
 5. Users are able to select their preferred database like PostgreSQL, MySQL,
    Oracle, SQLite etc. (whatever SQLAlchemy supports)
 
 6. It is possible to use both one or different databases for studio specific
    and project specific data. It is mostly beneficial when the setup uses
    SQLite. The project specific data could be kept in project folder as an
    SQLite db file and the studio specific data can be another SQLite db file
    or another database connection to PostgreSQL, MySQL, Oracle etc. databases.
    In an SQLite setup, the database can be backed up with the project folder
    itself.
 
 7. Configuration files lets the user to configure all the aspects of the
    asset/project management.
 
 8. Uses Jinja2 as the templating system for the file and folder naming
    convention will be used like:
    
    {repository.path}/{project.name}/assets/{asset.name}/{pipelineStep.name}/
    {asset.variation.name}/{asset.name}_{asset.type.name}_v{asset.version}.{
    asset.fileFormat.extension}
 
 9. file and folders and file sequences can be uploaded to the server as
    assets, and the server decides where to place the folder or file by using
    the templating system.
 
 10. The event system gives full control for every CRUD (create/insert, read,
     update, delete) by giving step like before insert, after insert callbacks.
 
 11. The messaging system allows the users collaborate more efficiently.

Usage Examples
--------------

Let's dance with Stalker a little bit.

When you first setup Stalker you will have nothing but an empty database. So
lets create some data and store them in the database.

First import some modules:

First of all import and setup the default database (an in-memory SQLite
database)

>>> from stalker import db # the database module
>>> db.setup()

By calling the :func:`~stalker.db.setup` we have created all the mappings for
SOM and also we have created the ``session`` object
which is stored under ``stalker.db.meta.session`` (this is used to have a
Singleton SQLAlchemy metadata).

Lets import the SOM which is stalker.core.models

>>> from stalker.core.models.user import User

Stalker comes with an *admin* user already defined in to it. To create other
things in the database we need to have the admin user by querying it.

>>> dbSession = db.meta.session
>>> admin = dbSession.query(User).filter_by(name="admin").first()

Lets create another user

>>> newUser = User(name="eoyilmaz",
                   login_name="eoyilmaz",
                   first_name="Erkan Ozgur",
                   last_name="Yilmaz",
                   password="secret",
                   email="eoyilmaz@gmail.com")

Save the data to the database

>>> session.add(newUser)
>>> session.commmit()

Create a query for users:

>>> query = session.query(user.User)

Get all the users:

>>> users = query.all()

or select a couple of users by filters:

>>> users = query.filter_by(name="Ozgur")

or select the first user matching query criteria:

>>> user_ozgur = query.filter_by(name="Ozgur").first()


***** UPDATE BELOW *****

Now add them to the project:

>>> newProject.users.append(users)

Save the new project to the database:

>>> mapper.session.save(newProject)
>>> mapper.session.flush()

Let's ask the tasks of one user:

>>> ozgur = query.filter_by(name="ozgur")
>>> tasks = ozgur.tasks

Get the on going tasks of this user:

>>> onGoingTasks = [task for task in ozgur.tasks if not task.isComplete]

Get the on going tasks of this user by using the database:

>>> taskQuery = mapper.sessison.query(user.User).filter_by(name="ozgur").join(task.Task).filter_by(status!="complete")
>>> onGoingTasks = taskQuery.all()

Get the "rig" tasks of ozgur:

>>> rigTasks =  taskQuery.join(pipelineStep.pipelineStep).filter_by(name="Rig").all()

As you see all the functionalities of SQLAlchemy is fully supported. At the end
all the models are plain old python objects (POPO) and the persistancy part is
handled with SQLAlchemy.

How To Customize Stalker
========================

This part explains the customization of Stalker.

How To Extend SOM
=================

This part explains how to extend Stalker Object Model or SOM.