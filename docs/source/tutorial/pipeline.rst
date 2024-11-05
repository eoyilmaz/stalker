.. _tutorial_pipeline_toplevel:

Pipeline
========

So far, we've covered the basics of creating data in Stalker. However. to fully
utilize Stalker's power, we need to define our studio's **pipeline**. This
involves creating tasks and establishing dependencies between them.

Creating Tasks
--------------

Let's create some :class:`.Task`\ s for one of the shots we created earlier:

.. code-block:: python

    from stalker import Task

    previs = Task(
        name="Previs",
        parent=sh001
    )

    matchmove = Task(
        name="Matchmove",
        parent=sh001
    )

    anim = Task(
        name="Animation",
        parent=sh001
    )

    lighting = Task(
        name="Lighting",
        parent=sh001
    )

    comp = Task(
        name="Comp",
        parent=sh001
    )

Defining Dependencies
---------------------

Now, let's define the dependencies between these tasks:

.. code-block:: python

    comp.depends_on = [lighting]
    lighting.depends_on = [anim]
    anim.depends_on = [previs, matchmove]

By establishing these dependencies, we're telling Stalker that certain tasks
need to be completed before others can begin. For example, the "Comp" task
depends on the "Lighting" task, meaning the "Lighting" task must be finished
before the "Comp" task can start. Stalker uses these dependencies to schedule
tasks effectively. 

We'll delve deeper into task scheduling and other pipeline-related concepts
later in this tutorial.
