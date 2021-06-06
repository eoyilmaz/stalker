|travis| |license| |pyversion| |pypiversion| |wheel|

.. |travis| image:: https://travis-ci.com/eoyilmaz/stalker.svg?branch=master
    :target: https://travis-ci.com/eoyilmaz/stalker
    :alt: Travis-CI Build Status

.. |license| image:: https://img.shields.io/badge/License-LGPL%20v3-blue.svg
     :target: http://www.gnu.org/licenses/lgpl-3.0
     :alt: License

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/stalker.svg
     :target: https://pypi.python.org/pypi/stalker
     :alt: Supported Python versions

.. |pypiversion| image:: https://img.shields.io/pypi/v/stalker.svg
     :target: https://pypi.python.org/pypi/stalker
     :alt: PyPI Version

.. |wheel| image:: https://img.shields.io/pypi/wheel/stalker.svg
     :target: https://pypi.python.org/pypi/stalker
     :alt: Wheel Support



=====
About
=====

Stalker is an Open Source Production Asset Management (ProdAM) Library designed 
specifically for Animation and VFX Studios but can be used for any kind of
projects. Stalker is licensed under LGPL v3.

Features
========

Stalker has the following features:

 * Designed for **Animation and VFX Studios**.
 * Platform independent.
 * Default installation handles nearly all the asset and project management 
   needs of an animation and vfx studio.
 * Customizable with configuration scripts.
 * Customizable object model (**Stalker Object Model - SOM**).
 * Uses **TaskJuggler** as the project planing and tracking backend.
 * Mainly developed for **PostgreSQL** in mind but **SQLite3** is also
   supported.
 * Can be connected to all the major 3D animation packages like **Maya,
   Houdini, Nuke, Fusion, Softimage, Blender** etc. and any application that
   has a Python API. And with applications like **Adobe Photoshop** which does
   not have a direct Python API but supports ``win32com`` or ``comtypes``.
 * Mainly developed for **Python 3.0+** and **Python 2.7** is fully supported.
 * Developed with **TDD** practices.

Stalker is build over these other OpenSource projects:

 * Python
 * SQLAlchemy and Alembic
 * Jinja2
 * TaskJuggler

Stalker as a library has no graphical UI, it is a python library that gives you
the ability to build your pipeline on top of it. There are other python
packages like the Open Source Pyramid Web Application `Stalker Pyramid`_ and
the Open Source pipeline library `Anima`_ which has PyQt/PySide/PySide2 UIs for
applications like Maya, Nuke, Houdini, Fusion, Photoshop etc.

.. _`Stalker Pyramid`: https://github.com/eoyilmaz/stalker_pyramid
.. _`Anima`: https://github.com/eoyilmaz/anima

Installation
============

Use::

  pip install stalker


Examples
========

Let's play with **Stalker**.

Initialize the database and fill with some default data:

.. code:: python

    from stalker import db
    db.setup()
    db.init()

Create a ``User``:

.. code:: python

    from stalker.db.session import DBSession
    from stalker import User
    me = User(
        name='Erkan Ozgur Yilmaz',
        login='erkanozgur',
        email='my_email@gmail.com',
        password='secretpass'
    )

    # Save the user to database
    DBSession.save(me)

Create a ``Repository`` for project files to be saved under:

.. code:: python

    from stalker import Repository
    repo = Repository(
        name='Commercial Projects Repository',
        windows_path='Z:/Projects',
        linux_path='/mnt/Z/Projects',
        osx_path='/Volumes/Z/Projects'
    )

Create a ``FilenameTemplate`` (to be used as file naming convention):

.. code:: python

    from stalker import FilenameTemplate

    task_template = FilenameTemplate(
        name='Standard Task Filename Template',
        target_entity_type='Task',  # This is for files saved for Tasks
        path='{{project.repository.path}}/{{project.code}}/'
             '{%- for parent_task in parent_tasks -%}'
             '{{parent_task.nice_name}}/'
             '{%- endfor -%}',  # This is Jinja2 template code
        filename='{{version.nice_name}}_v{{"%03d"|format(version.version_number)}}'
    )

Create a ``Structure`` that uses this template:

.. code:: python

    from stalker import Structure
    standard_folder_structure = Structure(
        name='Standard Project Folder Structure',
        templates=[task_template],
        custom_template='{{project.code}}/References'  # If you need extra folders
    )

Now create a ``Project`` that uses this structure and will be placed under the
repository:

.. code:: python

    from stalker import Project
    new_project = Project(
        name='Test Project',
        code='TP',
        structure=standard_folder_structure,
        repositories=[repo],  # if you have more than one repository you can do it
    )

Define the project resolution:

.. code:: python

    from stalker import ImageFormat
    hd1080 = ImageFormat(
        name='1080p',
        width=1920,
        height=1080
    )

Set the project resolution:

.. code:: python

    new_project.image_format = hd1080

    # Save the project and all the other data it is connected to it
    DBSession.save(new_project)

Create Assets, Shots and other Tasks:

.. code:: python

    from stalker import Task, Asset, Shot, Type

    # define Character asset type
    char_type = Type(name='Character', code='CHAR', target_entity_type='Asset')

    character1 = Asset(
        name='Character 1',
        code='CHAR1',
        type=char_type,
        project=new_project
    )

    # Save the Asset
    DBSession.save(character1)

    model = Task(
        name='Model',
        parent=character1
    )

    rigging = Task(
        name='Rig',
        parent=character1,
        depends=[model],  # For project management, define that Rig can not start
                          # before Model ends.
    )

    # Save the new tasks
    DBSession.save([model, rigging])

    # A shot and some tasks for it
    shot = Shot(
        name='SH001',
        code='SH001',
        project=new_project
    )

    # Save the Shot
    DBSession.save(shot)

    animation = Task(
        name='Animation',
        parent=shot,
    )

    lighting = Task(
        name='Lighting',
        parent=shot,
        depends=[animation], # Lighting can not start before Animation ends,
        schedule_timing=1,
        schedule_unit='d',  # The task expected to take 1 day to complete
        resources=[me]
    )
    DBSession.save([animation, lighting])

Let's create versions for the Animation task.

.. code-block:: python

    from stalker import Version

    new_version = Version(task=animation)
    new_version.update_paths()  # to render the naming convention template
    new_version.extension = '.ma'  # let's say that we have created under Maya

Let's check how the version path is rendered:

.. code-block:: python

    assert new_version.absolute_full_path == \
        "Z:/Projects/TP/SH001/Animation/SH001_Animation_Main_v001.ma"
    assert new_version.version_number == 1

Create a new version and check that the version number increased automatically:

.. code-block:: python

    new_version2 = Version(task=animation)
    new_version2.update_paths()  # to render the naming convention template
    new_version2.extension = '.ma'  # let's say that we have created under Maya

    assert new_version2.version_number == 2

See more detailed example in `API Tutorial`_.

.. _API Tutorial: https://pythonhosted.org/stalker/tutorial.html
