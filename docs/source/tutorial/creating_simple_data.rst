.. _tutorial_creating_simple_data_toplevel:

Creating Simple Data
====================

Let's imagine you're starting a new commercial project and want to use Stalker.
The first step is to create a :class:`.Project` object to store project
information.

Project setup
-------------

.. versionadded:: 0.2.24.2

   Starting with Stalker v0.2.24.2, you no longer need to manually create
   :class:`.StatusList` instances for :class:`.Project` objects. The
   :func:`stalker.db.setup.init()` function will automatically create them
   during database initialization.

.. note::
   When the Stalker database is first initialized (with ``db.setup.init()``), a
   set of default :class:`.Status` instances for :class:`.Task`,
   :class:`.Asset`, :class:`.Shot`, :class:`.Sequence`, :class:`.Ticket` and
   :class:`.Variant` classes are created, along with their respective
   :class:`.StatusList` instances.

Creating a Repository
---------------------

To create a project, we first need to create a :class:`.Repository`.
The Repository (or Repo) is a directory on your file server, where project
files are stored and accessible to all workstations and render farm computers:

.. code-block:: python

    from stalker import Repository

    commercial_repo = Repository(
        name="Commercial Repository",
        code="CR"
    )

.. versionadded:: 0.2.24

   Starting with Stalker version 0.2.24 :class:`.Repository` instances have a
   :attr:`stalker.models.repository.Repository.code` attribute to help
   generate universal paths across operating systems and Stalker installations.

:class:`.Repository` class will be explained in detail in upcoming sections.

Creating a Project
------------------

Now, let's create the project:

.. code-block:: python

    new_project = Project(
        name="Fancy Commercial",
        code='FC',
        repositories=[commercial_repo],
    )

Adding Project Details
----------------------

Let's add more details to the project:

.. code-block:: python

    import tzlocal
    import datetime
    from stalker import ImageFormat

    new_project.description = (
        "The commercial is about this fancy product. The "
        "client want us to have a shiny look with their "
        "product bla bla bla..."
    )

    new_project.image_format = ImageFormat(
        name="HD 1080",
        width=1920,
        height=1080
    )

    new_project.fps = 25
    local_tz = tzlocal.get_localzone()
    new_project.end = datetime.datetime(2024, 5, 15, tzinfo=local_tz)
    new_project.users.append(me)

Saving the Project
------------------

To save the project and its associated data to the database:

.. code-block:: python

    DBSession.add(new_project)
    DBSession.commit()

Even though we've created multiple objects (project, repository etc.), we only
need to add the ``new_project`` object to the database. Stalker will handle the
relationships and save the related objects automatically.

.. note::

   Starting with Stalker v0.2.18, all the datetime information must include
   timezone information. In the example, we've used the local timezone.

Creating Sequences and Shots
----------------------------

A :class:`.Project` is typically composed of :class:`.Task` instances, which
represent units of work that need to be completed. A :class:`.Task` in Stalker
defines the total `effort` required to be considered finished. Tasks can also
be `duration` or `length` based, in which case they define the required time
to be considered finished. Leaf tasks, the final tasks in a task hierarchy,
are assigned to specific :class:`.User` instances who are responsible for
completing them. More details about :class:`.Task` and its attributes can be
found in the :class:`.Task` class documentation. :class:`.Asset`,
:class:`.Shot` and :class:`.Sequences` are specialized types of Tasks.

Let's create a :class:`.Sequence`:

.. code-block:: python

    from stalker import Sequence

    seq1 = Sequence(
        name="Sequence 1",
        code="SEQ1",
        project=new_project,
    )

And some :class:`.Shot`\ s withing the sequence:

.. code-block:: python

    from stalker import Shot

    sh001 = Shot(
        name='SH001',
        code='SH001',
        project=new_project,
        sequences=[seq1]
    )
    sh002 = Shot(
        code='SH002',
        project=new_project,
        sequences=[seq1]
    )
    sh003 = Shot(
        code='SH003',
        project=new_project,
        sequences=[seq1]
    )

Save the changes to the database:

.. code-block:: python

    DBsession.add_all([sh001, sh002, sh003])
    DBsession.commit()

.. note::

   * While we've created :class:`.Shot` objects with a :class:`.Sequence`
     instance, it's not strictly necessary. You can create :class:`.Shot`
     objects without assigning them to a Sequence.

   * For smaller projects like commercials, you might skip creating sequences
     altogether.

   * For larger projects like feature films, using sequences to group shots is
     recommended.
