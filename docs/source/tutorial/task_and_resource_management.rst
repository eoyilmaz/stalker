.. _tutorial_task_resource_management_toplevel:

Task and Resource Management
============================

Now that we have created shots and tasks, we need to assign resources (users)
to these tasks to complete the work.

Let's assign ourselves to all the tasks:

.. code-block:: python

    previs.resources = [me]
    previs.schedule_timing = 10
    previs.schedule_unit = 'd'

    matchmove.resources = [me]
    matchmove.schedule_timing = 2
    matchmove.schedule_unit = 'd'

    anim.resources = [me]
    anim.schedule_timing = 5
    anim.schedule_unit = 'd'

    lighting.resources = [me]
    lighting.schedule_timing = 3
    lighting.schedule_unit = 'd'

    comp.resources = [me]
    comp.schedule_timing = 6
    comp.schedule_unit = 'h'

Here, we've assigned ourselves as the resource for each task and specified the
estimated time to complete the task using ``schedule_timing`` and
``schedule_unit`` attributes.

Saving Changes
--------------

To save these changes to the database:

.. code-block:: python

    DBsession.commit()

Note that we didn't explicitly add any new object to the session. Since all the
tasks are related to the ``sh001`` shot, which is already tracked by the
session, SQLAlchemy will automatically track and save the changes to the
database.

With this information, Stalker can now schedule these tasks, taking info
account dependencies and resource availability. This will help you plan and
manage your project more efficiently.
