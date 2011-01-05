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
   stalker.models
   stalker.models.asset
   stalker.models.asset.Asset
   stalker.models.assetBase
   stalker.models.assetBase.AssetBase
   stalker.models.booking
   stalker.models.booking.Booking
   stalker.models.comment
   stalker.models.comment.Comment
   stalker.models.department
   stalker.models.department.Department
   stalker.models.entity
   stalker.models.entity.SimpleEntity
   stalker.models.entity.Entity
   stalker.models.entity.StatusedEntity
   stalker.models.group
   stalker.models.group.Group
   stalker.models.imageFormat
   stalker.models.imageFormat.ImageFormat
   stalker.models.pipelineStep
   stalker.models.pipelineStep.PipelineStep
   stalker.models.project
   stalker.models.project.Project
   stalker.models.reference
   stalker.models.reference.Reference
   stalker.models.repository
   stalker.models.repository.Repository
   stalker.models.sequence
   stalker.models.sequence.Sequence
   stalker.models.shot
   stalker.models.shot.Shot
   stalker.models.status
   stalker.models.status.Status
   stalker.models.status.StatusList
   stalker.models.structure
   stalker.models.structure.Structure
   stalker.models.tag
   stalker.models.tag.Tag
   stalker.models.task
   stalker.models.task.Task
   stalker.models.template
   stalker.models.template.Template
   stalker.models.typeEntity
   stalker.models.typeEntity.AssetType
   stalker.models.typeEntity.ReferenceType
   stalker.models.user
   stalker.models.user.User
   stalker.models.version
   stalker.models.version.Version


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

