.. _design_toplevel:

======
Design
======

This document explores Stalker, an open-source Python library designed for
production asset management.

Introduction
============

While primarily designed for VFX and animation studios, Stalker's flexible
architecture makes it adaptable to various industries.

An Asset Management (AM) System is responsible for organizing and storing data
created by users, ensuring easy accessibility. A Production Asset Management
(ProdAM) System extends the functionality of an AMS by managing production
steps, tasks, and enabling collaboration among team members.

Implementing an ProdAM System in an animation or VFX studio is crucial for
maintaining order and efficiency. The benefits of a well-organized system far
outweigh the initial setup effort.

Many studios develop their own custom ProdAM solutions. Stalker aims to provide
a solid foundation for these systems, reducing the need for redundant
development efforts.

Stalker focuses on organizing assets and tasks within projects,
streamlining workflows. It goes beyond basic asset management by incorporating
production steps and collaboration tools.

Concepts
========

There are a few key design concepts to understand before diving deeper into
Stalker.

Essentially, Stalker serves as the **Model** component in an **MTV**
(Model-Template-View) architecture. `Stalker Pyramid`_ provides the
*Template* and *View* components, defining the presentation layer and user
interface. Stalker itself focuses on defining the data structures and their
interactions.

Stalker Object Model (SOM)
--------------------------

Stalker's robust object model, the Stalker Object Model (SOM), provides a
flexible framework for building production pipelines. SOM is designed to be
both usable out-of-the-box and extensible to meet specific studio needs.

Lets look at how a studio simply works and try to create our asset management
concepts around it.

An animation of VFX studio's primary goal is to complete a :class:`.Project`.
This project involves creating a series of :class:`.Sequences`, each composed
of individual :class:`.Shot`\ s. These shots, in turn, often rely on reusable
:class:`.Asset`\ s.

To break down the work into manageable chunks, Projects, Sequences, Shots, and
Assets are further divided into :class:`.Task`\ s. These tasks often represent
specific pipeline steps like modeling, look development, rigging, animation,
lighting, and so on.

These tasks can be assigned to specific :class:`User`\ s and require a certain
amount of **effort** to complete. This effort is tracked using
:class:`.TimeLog`\ s.

As work progresses on a task, :class:`.Version`\ s are created to represent
different iterations or revisions of the output. These versions are linked to
files stored in a :class:`.Repository`.

All the names those shown in bold fonts are a class in SOM. and there are a
series of other classes to accommodate the needs of a :class:`.Studio`.

The inheritance diagram of the classes in the SOM is shown below:

.. include:: inheritance_diagram.rst

Stalker is a highly configurable and open-source system. This flexibility
allows for various customization options.

There are two main approaches to extending Stalker:

    1. **Simple Customization:** This involves adding or modifying existing
       entities like statuses, types, or other predefined elements. The current
       Stalker design is well-suited for this level of customization. More
       details can be found in the `How to Customize Stalker`_ section.

    2. **Extending the SOM:** This involves creating new classes and database
       tables, or modifying existing ones. This approach is more complex but
       allows for significant customization of Stalker's core functionality.
       Refer to the `How To Extend SOM`_ section for further guidance.

Features
--------

Stalker boasts a robust feature set designed to streamline your production
pipeline:

 1. **Pure Python:** Built entirely on Python 3.8 and above (continuously
    tested with Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13), utilizing rigorous
    Test Driven Development (TDD) practices for exceptional code quality (test
    coverage is 99.7%).

 2. **SQLAlchemy Integration:** Leverages SQLAlchemy for its database backend
    and Object-Relational Mapping (ORM) capabilities, ensuring efficient data
    management. Designed PostgreSQL (versions 14 to 17) in mind but not limited
    to it.

 3. **Jinja2 Templates:** Employs Jinja2 for flexible file and folder naming
    conventions. For a structured naming scheme it is possible to define
    templates like:

    {repository.path}/{project.code}/Assets/{asset.type.name}/{asset.code}/{asset.name}_{asset.type.name}_v{version.version_number:03d}.{version.extension}

 5. **Review Workflow:** Stalker incorporates a comprehensive task review
    workflow and a robust task status management system to ensure efficient and
    quality production.

 6. **Automated File Placement:** Upload files, folders, and even file
    sequences as versions. Stalker utilizes the defined templates to
    automatically determine their placement on the server, promoting
    organization.

 7. **Fine-Grained Event System:** Gain complete control over the CRUDL
    (Create, Read, Update, Delete, List) lifecycle. Define custom callbacks to
    execute before or after specific operations, enabling tailored behavior.

 8. **Embedded Ticketing System:** Streamline issue tracking and project
    discussions with a built-in ticketing system.

 9. **TaskJuggler Integration:** Integrate with TaskJuggler for enhanced task
    management capabilities, supporting basic task attributes.

 10. **Predefined Task Statuses:** Manage task progress efficiently with a
     pre-defined Task Status Workflow, providing a structured approach to
     tracking task completion stages.

For usage examples see :ref:`tutorial_toplevel`\ .

How To Customize Stalker
========================

Upcoming! This part will explain the customization of Stalker.

How To Extend SOM
=================

Upcoming! This part will explain how to extend Stalker Object Model or SOM.


.. _`Stalker Pyramid`: https://pypi.python.org/pypi/stalker_pyramid
