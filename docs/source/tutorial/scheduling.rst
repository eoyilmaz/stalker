.. _tutorial_scheduling_toplevel:

Scheduling
==========

Now that we've defined tasks, resources, and dependencies, let's schedule our
project!


TaskJuggler Integration
-----------------------

Stalker utilizes `TaskJuggler`_ to solve scheduling problems and determine when
resources should work on specific tasks.

.. warning::

   * Ensure you have `TaskJuggler`_ installed on your system.

   * Configure Stalker to locate the ``tj3`` executable:

     * **Linux:** This is usually straightforward under Linux, just install
       `TaskJuggler`_ and Stalker will be able to use it.

     * **macOS & Windows:** Create a ``STALKER_PATH`` environment variable
       pointing to a folder containing a ``config.py`` file. Add the following
       line to ``config.py``:

       .. code-block:: python

            tj_command = r"C:\Path\to\tj3.exe"

   The default value for ``tj_command`` is ``/usr/local/bin/tj3``. If you run
   ``which tj3`` on Linux or macOS and it returns this value, no additional
   setup is needed.

   .. _TaskJuggler: http://www.taskjuggler.org/

Scheduling Your Project
-----------------------

Let's schedule our project using the :class:`.Studio` instance that we've
created at the beginning of this tutorial:

.. code-block:: python

    from stalker import TaskJugglerScheduler

    my_studio.scheduler = TaskJugglerScheduler()
    # Set a large duration (e.g., 1 year) to avoid TaskJuggler complaining the
    # project is not fitting into the time frame.
    my_studio.duration = datetime.timedelta(days=365)
    my_studio.schedule(scheduled_by=me)
    DBsession.commit()  # Save changes

This process might take a few seconds for small project or long for larger
ones.

Viewing Scheduled Dates
-----------------------

Once completed, each task will have its ``computed_start`` and ``computed_end``
values populated:

.. code-block:: python

    for task in [previs, matchmove, anim, lighting, comp]:
        print("{:16s} {} -> {}".format(
            task.name,
            task.computed_start,
            task.computed_end
        ))

Outputs:

.. code-block:: shell

    Previs           2024-04-02 16:00 -> 2024-04-15 15:00
    Matchmove        2024-04-15 15:00 -> 2024-04-17 13:00
    Animation        2024-04-17 13:00 -> 2024-04-23 17:00
    Lighting         2024-04-23 17:00 -> 2024-04-24 11:00
    Comp             2024-04-24 11:00 -> 2024-04-24 17:00

Understanding the Output
------------------------

The output will display start and end dates for each task, reflecting the
dependencies. In this example, since each task has only one assigned resource
(you), they follow one another.

Further Explorations
--------------------

Scheduling is complex topic. For in-depth information, refer to the
`TaskJuggler`_ documentation.


TaskJuggler Project Representation
----------------------------------

You can check the ``to_tjp`` values of the data objects:

.. code-block:: python

    print(my_studio.to_tjp)
    print(me.to_tjp)
    print(comp.to_tjp)
    print(new_project.to_tjp)

If you're familiar with TaskJuggler, you'll recognize the output format.
Stalker maps its data to TaskJuggler-compatible strings. Although, Stalker is
currently supporting a subset of directives, it is enough for scheduling
complex projects with intricate dependencies and hierarchies. Support for
additional TaskJuggler directives will grow with future Stalker versions.
