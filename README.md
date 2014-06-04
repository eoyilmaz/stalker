About
=====

Stalker is an Open Source Production Asset Management (ProdAM) Library designed 
specifically for Animation and VFX Studios but can be used for any kind of
projects. Stalker is licensed under LGPL v2.1.

Features:
 * Designed for animation and VFX Studios.
 * Platform independent.
 * Default installation handles nearly all the asset and project management 
   needs of an animation and vfx studio.
 * Customizable with configuration scripts.
 * Customizable object model (Stalker Object Model - SOM).
 * Uses TaskJuggler as the project planing and tracking backend.
 * Can be used with any kind of databases supported by SQLAlchemy.
 * Can be connected to all the major 3d animation packages like Maya, Houdini,
   Nuke, Softimage, Vue, Blender etc. and any application that has a Python
   API.
 * Python 2.6+ and Python 3.0+ compatible.

Stalker is build over these other OpenSource projects:
 * Python
 * SQLAlchemy and Alembic
 * Jinja2
 * TaskJuggler

Stalker as a library has no graphical UI, it is a python library that gives you
the ability to build your pipeline on top of it. There are other python
packages like the Open Source Pyramid Web Application
[Stalker Pyramid](https://code.google.com/p/stalker-pyramid) and the Open
Source pipeline library [Anima](https://github.com/eoyilmaz/anima)
which has PyQt/PySide UIs for applications like Maya, Nuke, Houdini, Eyeon
Fusion, Photoshop etc.

Source
------

The latest development version is available in [GitHub
Stalker](https://github.com/eoyilmaz/stalker) or can be directly cloned with
the following command if you already have git installed::

  git clone https://github.com/eoyilmaz/stalker.git
