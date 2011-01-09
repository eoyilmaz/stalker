.. stalker documentation master file, created by
   sphinx-quickstart on Sat Jul  3 13:41:00 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to stalker's documentation!
===================================

Stalker is an OpenSource Production Digital Asset Manager (ProdAM) licensed
under BSD License and designed specially for Animation and VFX Studios.

Stalker consists of several parts:
 * Stalker Object Model (SOM)
 * Database Module
 * Extensions
 * UI

The design of the Stalker is tried to be kept as flexible as possible. So one
can extend Stalker as much as possible by using configuration files.

Stalker is build over these other OpenSource projects:
 * Python
 * SQLAlchemy
 * PyQt or PySide (not sure for now)
 * JQuery
 * Jinja

Contents:

.. toctree::
   :maxdepth: 2
   
   install.rst
   design.rst
   contribute.rst
   roadmap.rst

Summary
=======

.. autosummary::
   :toctree: generated/
   :nosignatures:
   
   stalker
   stalker.db
   stalker.db.auth
   stalker.db.auth.authenticate
   stalker.db.auth.create_session
   stalker.db.auth.get_user
   stalker.db.auth.login
   stalker.db.auth.logout
   stalker.db.mapper
   stalker.db.meta
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
   stalker.core.models.entity.StatusedEntity
   stalker.core.models.group
   stalker.core.models.group.Group
   stalker.core.models.imageFormat
   stalker.core.models.imageFormat.ImageFormat
   stalker.core.models.link
   stalker.core.models.link.Link
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
   stalker.core.models.template
   stalker.core.models.template.Template
   stalker.core.models.typeEntity
   stalker.core.models.typeEntity.AssetType
   stalker.core.models.typeEntity.LinkType
   stalker.core.models.typeEntity.ProjectType
   stalker.core.models.typeEntity.TypeEntity
   stalker.core.models.user
   stalker.core.models.user.User
   stalker.core.models.version
   stalker.core.models.version.Version


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

