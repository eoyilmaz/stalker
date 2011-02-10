.. stalker documentation master file, created by
   sphinx-quickstart on Sat Jul  3 13:41:00 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*******
Stalker
*******

=====
About
=====

Stalker is a Production Digital Asset Management (ProdAM) System designed
specifically for Animation and VFX Studios and licensed under BSD License.

Features:
 * Platform independent
 * Flexible design
 * Designed for animation and vfx studios
 * Default installation handles nearly all the asset management needs of an
   animation and vfx studio
 * Customisable with configuration scripts
 * Customisable object model (Stalker Object Model - SOM)
 * Integrated messaging system
 * Integrated production planing and tracking tools
 * PySide user interfaces
 * Can be used with any kind of databases supported by SQLAlchmey
 * Can be connected to all the major 3d animation packages like Maya, Houdini,
   Nuke, XSI, Vue, Blender etc. and any application that has a Python API
 * Can work as a stand-alone application

Stalker is build over these other OpenSource projects:
 * Python
 * SQLAlchemy
 * Jinja2
 * Beaker
 * PySide

Source
======

The latest development version is available in `Google Project page of
Stalker`_ or can be directly cloned with the following command if you already
have mercurial installed::

  hg clone https://stalker.googlecode.com/hg/ stalker

.. _Google Project page of Stalker: http://code.google.com/p/stalker/



Table of Contents
=================

.. toctree::
    :maxdepth: 2
    
    installation.rst
    tutorial.rst
    design.rst
    contribute.rst
    roadmap.rst


Summary
-------

.. autosummary::
   :toctree: generated/
   :nosignatures:
   
   stalker.db
   stalker.db.auth
   stalker.db.auth.authenticate
   stalker.db.auth.create_session
   stalker.db.auth.get_user
   stalker.db.auth.login
   stalker.db.auth.login_required
   stalker.db.auth.permission_required
   stalker.db.auth.logout
   stalker.db.mapper
   stalker.db.mixin
   stalker.db.mixin.ReferenceMixinDB
   stalker.db.mixin.StatusMixinDB
   stalker.db.tables
   stalker.db.setup
   stalker.core.models
   stalker.core.models.asset
   stalker.core.models.asset.Asset
   stalker.core.models.assetBase
   stalker.core.models.assetBase.AssetBase
   stalker.core.models.booking
   stalker.core.models.booking.Booking
   stalker.core.models.comment
   stalker.core.models.comment.Comment
   stalker.core.models.department
   stalker.core.models.department.Department
   stalker.core.models.entity
   stalker.core.models.entity.SimpleEntity
   stalker.core.models.entity.Entity
   stalker.core.models.entity.TypeEntity
   stalker.core.models.error
   stalker.core.models.error.LoginError
   stalker.core.models.group
   stalker.core.models.group.Group
   stalker.core.models.imageFormat
   stalker.core.models.imageFormat.ImageFormat
   stalker.core.models.link
   stalker.core.models.link.Link
   stalker.core.models.mixin
   stalker.core.models.mixin.ReferenceMixin
   stalker.core.models.mixin.StatusMixin
   stalker.core.models.pipelineStep
   stalker.core.models.pipelineStep.PipelineStep
   stalker.core.models.project
   stalker.core.models.project.Project
   stalker.core.models.repository
   stalker.core.models.repository.Repository
   stalker.core.models.sequence
   stalker.core.models.sequence.Sequence
   stalker.core.models.shot
   stalker.core.models.shot.Shot
   stalker.core.models.status
   stalker.core.models.status.Status
   stalker.core.models.status.StatusList
   stalker.core.models.structure
   stalker.core.models.structure.Structure
   stalker.core.models.tag
   stalker.core.models.tag.Tag
   stalker.core.models.task
   stalker.core.models.task.Task
   stalker.core.models.types
   stalker.core.models.types.AssetType
   stalker.core.models.types.ProjectType
   stalker.core.models.types.LinkType
   stalker.core.models.types.TypeTemplate
   stalker.core.models.user
   stalker.core.models.user.User
   stalker.core.models.version
   stalker.core.models.version.Version
   stalker.ext.validatedList
   stalker.ext.validatedList.ValidatedList

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

