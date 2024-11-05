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
specifically for Animation and VFX Studios. But it can be used for any kind of
projects from any other industry. Stalker is licensed under LGPL v3.

Features
========

Stalker has the following features:

 * Designed for **Animation and VFX Studios** (but not limited to).
 * OS independent, can work simultaneously with **Windows**, **macOS** and
   **Linux**.
 * Supplies excellent **Project Management** capabilities, i.e. scheduling and
   tracking tasks, milestones and deadlines (via **TaskJuggler**).
 * Powerful **Asset management** capabilities, allows tracking of asset
   references in shots, scenes, sequences and projects.
 * Customizable object model (**Stalker Object Model - SOM**).
 * Uses **TaskJuggler** as the project planing and tracking backend.
 * Mainly developed for **PostgreSQL** in mind but **SQLite3** is also
   supported.
 * Can be connected to all the major 3D animation packages like **Maya,
   Houdini, Nuke, Fusion, DaVinci Resolve, Blender** etc. and any application
   that has a Python API, and for **Adobe Suite** applications like
   **Adobe Photoshop** through ``win32com`` or ``comtypes`` libraries.
 * Developed with religious **TDD** practices.

Stalker is mainly build over the following OpenSource libraries:

 * Python
 * SQLAlchemy and Alembic
 * Jinja2
 * TaskJuggler

As Stalker is a Python library and doesn't supply any graphical UI you can use
other tools like `Stalker Pyramid`_ which is a Pyramid Web Application and
`Anima`_ which has PyQt/PySide UIs for applications like Houdini, Maya,
Blender, Nuke, Fusion, DaVinci Resolve, Photoshop and many more.

.. _`Stalker Pyramid`: https://github.com/eoyilmaz/stalker_pyramid
.. _`Anima`: https://github.com/eoyilmaz/anima

Installation
============

Simply use:

.. code-block:: shell

  pip install stalker

Examples
========

Let's play with **Stalker**.

Because Stalker uses SQLAlchemy, it is very easy to retrieve complex data.
Let's say that you want to query all the Shot Lighting tasks where a specific
asset is referenced:

.. code-block:: python

    from stalker import Asset, Shot, Version

    my_asset = Asset.query.filter_by(name="My Asset").first()
    refs = Version.query.filter_by(name="Lighting").filter(Version.inputs.contains(my_asset)).all()

Let's say you want to get all the tasks assigned to you in a specific Project:

.. code-block:: python

    from stalker import Project, Task, User

    me = User.query.filter_by(name="Erkan Ozgur Yilmaz").first()
    my_project = Project.query.filter_by(name="My Project").first() 
    query = Task.query.filter_by(project=my_project).filter(Task.resources.contains(me))
    my_tasks = query.all()

You can further query let's say your WIP tasks by adding more criteria to the ``query``
object:

.. code-block:: python

    from stalker import Status

    wip = Status.query.filter_by(code="WIP").first()
    query = query.filter_by(status=wip)
    my_wip_tasks = query.all()

and that's the way to get complex data in Stalker.

See more detailed examples in `API Tutorial`_.

.. _API Tutorial: https://pythonhosted.org/stalker/tutorial.html
