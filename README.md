[![license](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](http://www.gnu.org/licenses/lgpl-3.0)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/stalker.svg)](https://pypi.python.org/pypi/stalker)
[![Unit Tests](https://github.com/eoyilmaz/stalker/actions/workflows/pytest.yml/badge.svg)](https://github.com/eoyilmaz/stalker/actions/workflows/pytest.yml)
[![PyPI Version](https://img.shields.io/pypi/v/stalker.svg)](https://pypi.python.org/pypi/stalker)
[![PyPI Downloads](https://static.pepy.tech/badge/stalker)](https://pepy.tech/projects/stalker)

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

 * [Python](https://www.python.org)
 * [PostgreSQL](https://www.postgresql.org/)
 * [SQLAlchemy](https://www.sqlalchemy.org/)
 * [Jinja2](https://jinja.palletsprojects.com/en/stable/)
 * [TaskJuggler](https://taskjuggler.org/)

As Stalker is a Python library and doesn't supply any graphical UI you can use
other tools like [Stalker Pyramid](https://github.com/eoyilmaz/stalker_pyramid)
which is a Pyramid Web Application and [Anima](https://github.com/eoyilmaz/anima)
which has PyQt/PySide UIs for applications like Houdini, Maya, Blender, Nuke,
Fusion, DaVinci Resolve, Photoshop and many more.

Installation
============

Simply use:

```shell
pip install stalker
```

Examples
========

Let's play with **Stalker**.

Because Stalker uses SQLAlchemy, it is very easy to retrieve complex data.
Let's say that you want to query all the Shot Lighting tasks where a specific
asset is referenced:

```python
from stalker import Asset, File, Shot, Version

my_asset = Asset.query.filter_by(name="My Asset").first()
# Let's assume we have multiple Versions created for this Asset already
my_asset_version = my_asset.versions[0]
# get a file from that version
my_asset_version_file = my_asset_version.files[0]
# now get any other Lighting Versions that is referencing this file
refs = (
    Version.query
        .join(File, Version.files)
        .filter(Version.name=="Lighting")
        .filter(File.references.contains(my_asset_version_file))
        .all()
)
```

Let's say you want to get all the tasks assigned to you in a specific Project:

```python
from stalker import Project, Task, User

me = User.query.filter_by(name="Erkan Ozgur Yilmaz").first()
my_project = Project.query.filter_by(name="My Project").first() 
query = Task.query.filter_by(project=my_project).filter(Task.resources.contains(me))
my_tasks = query.all()
```

You can further query let's say your WIP tasks by adding more criteria to the ``query``
object:

```python
from stalker import Status

wip = Status.query.filter_by(code="WIP").first()
query = query.filter_by(status=wip)
my_wip_tasks = query.all()
```

and that's the way to get complex data in Stalker.

See more detailed examples in [API Tutorial](https://pythonhosted.org/stalker/tutorial.html).
