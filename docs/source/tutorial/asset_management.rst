.. _tutorial_asset_management_toplevel:

Asset Management
================

Now that we've created projects, tasks and resources, it's time to manage the
files generated during production.

File Storage and Repository setup
---------------------------------

Contrary to a Source Code Management (SCM) System where revisions to a file is
handled incrementally, Stalker handles file versions all together. Meaning
that, all the versions that are created for individual tasks
(:class:`.Version`) are individual files stored in a shared location accessible
to everyone in your studio. This location is called a :class:`.Repository` in
Stalker.

Defining Repository Paths
-------------------------

A repository can be a network share or a locally mounted directory. You can
define multiple repositories for different project types or needs. We've
already created a repository while creating our first project. But the
repository has missing information. Here's how to define paths for a commercial
project repository::

.. code-block:: python

    commercial_repo.linux_path   = "/mnt/M/commercials"
    commercial_repo.macos_path   = "/Volumes/M/commercials"
    commercial_repo.windows_path = "M:/commercials"
    # Stalker automatically corrects backslashes (\) to forward slashes (/)

And if you ask for the path to a repository object, it will always return the
correct path according to your operating system:

.. code-block:: python

    print(commercial_repo.path)

You'll get the appropriate path based on your OS:

* **Windows:** M:/commercials
* **Linux:** /mnt/M/commercials
* **macOS:** /Volumes/M/commercials

This ensures consistent file path handling across different platforms.

.. note::

  Stalker consistently uses forward slashes (/) in path definitions, regardless
  of the operating system. This applies even if you initially specify paths
  with backward slashes (\\).


Assigning Repository to Project
-------------------------------

Connecting a repository to your project lets Stalker know where project files
are stored. However, it still needs information about the project's specific
directory structure.

Defining Project Structure
--------------------------

A :class:`.Structure` object defines the directory hierarchy for your project
within the repository. We create a structure named "Commercial Projects
Structure" and assign it to our project:

.. code-block:: python

    from stalker import Structure

    commercial_project_structure = Structure(
        name="Commercial Projects Structure"
    )

    # now assign this structure to our project
    new_project.structure = commercial_project_structure

.. versionadded:: 0.2.13

   Starting with Stalker version 0.2.13, :class:`.Project` instances can be
   associated with multiple :class:`.Repository` instances. This allows for
   more flexible file management, such as storing published versions on a
   separate server or directing rendered outputs to a different location.

   While the following examples are simplified, future versions will showcase
   the full potential of multiple repositories.

Creating Filename Templates
---------------------------

Next we create :class:`.FilenameTemplate` instances. These templates define how
filenames and paths will be generated for :class:`.Version` instances
associated with tasks.

Here, we create a :class:`.FilenameTemplate` named "Task Template for
Commercials" that uses `Jinja2`_ syntax for the ``path`` and ``filename``
arguments. The :class:`.Version` class knows how to render these templates
while calculating its ``path`` and ``filename`` attributes:

.. code-block:: python

    from stalker import FilenameTemplate

    task_template = FilenameTemplate(
        name='Task Template for Commercials',
        target_entity_type='Task',
        path='$REPO{{project.repository.code}}/{{project.code}}/{%- for p in parent_tasks -%}{{p.nice_name}}/{%- endfor -%}',
        filename='{{version.nice_name}}_v{{"%03d"|format(version.version_number)}}'
    )

  # Append the template to the project structure
  commercial_project_structure.templates.append(task_template)

  # No need to add anything as the project is already in the database
  DBsession.commit()

Explanation of the Template:

* ``$REPO{{project.repository.code}}``: This references the first repository
  assigned to the project. Importantly, this uses an environment variable
  ``$REPO``. Stalker dynamically creates environment variables for each
  repository upon database connection or creation, simplifying path definitions
  within templates.

* ``{{project.code}}``: This represent the project code and it is guaranteed to
  be file system safe.

* ``{%- for p in parent_tasks -%}{{p.nice_name}}/{%- endfor -%}``: This loop
  iterates over parent tasks, creating subdirectories for each.

* ``{{version.nice_name}}_v{{"%03d"|format(version.version_number)}}``: This
  defines the filename format with version number padding.

Creating and Managing Versions
------------------------------

Now, let's create a :class:`.Version`` instance for the "comp" task:

.. code-block:: python

    from stalker import Version

    vers1 = Version(task=comp)

    # Update paths using the template
    vers1.update_paths()

    print(vers1.path)                # '$REPO33/FC/SH001/comp'
    print(vers1.filename)            # 'SH001_comp_Main_v001'
    print(vers1.full_path)           # '$REPO33/FC/SH001/comp/SH001_comp_Main_v001'

    # Absolute paths with repository root based on your OS
    print(vers1.absolute_path)       # '/mnt/M/commercials/FC/SH001/comp'
    print(vers1.absolute_full_path)  # '/mnt/M/commercials/FC/SH001/comp/SH001_comp_Main_v001'

    # Get version number (automatically incremented)
    print(vers1.version_number)      # 1

    # commit to database
    DBsession.commit()

Stalker automatically generates a consistent path and filename for the version
based on the template. 

Stalker eliminates the need for those cumbersome and confusing file naming
conventions like ``Shot1_comp_Final``, ``Shot1_comp_Final_revised``,
``Shot1_comp_Final_revised_Final``,
``Shot1_comp_Final_revised_Final_real_final`` ...and the list goes on,
we've all experienced the frustration of such naming conventions, haven't we
😊.. It ensures a consistent and organized file structure, making asset
management significantly more efficient.

The :attr:`.Version.is_published` attribute within the :class:`.Version` class
helps differentiate between finalized and in-progress versions. Setting
:attr:`.is_published` to ``True`` flags a version as ready for use or review.

.. code-block:: python

    vers1.is_published = False  # This version is still being worked on

Automatic Version Numbering
---------------------------

Stalker automatically increments version numbers for each new version created
for the same task. This ensures you always have the latest iteration readily
identified.

.. code-block:: python

    vers2 = Version(task=comp)
    vers2.update_paths()

    print(vers2.version_number)  # Output: 2
    print(vers2.filename)        # Output: 'SH001_comp_Main_v002'

    vers3 = Version(task=comp)
    vers3.update_paths()

    print(vers3.version_number)  # Output: 3
    print(vers3.filename)        # Output: 'SH001_comp_Main_v003'

Querying Versions
-----------------

You can retrieve all versions associated with a specific task using either
using the :attr:`.Task.versions` attribute or by doing a database query.

.. code-block:: python

    # using pure Python
    vers_from_python = comp.versions
    # [<FC_SH001_comp_Main_v001 (Version)>,
    #  <FC_SH001_comp_Main_v002 (Version)>,
    #  <FC_SH001_comp_Main_v003 (Version)>]

    # # Using SQLAlchemy query
    vers_from_query = Version.query.filter_by(task=comp).all()

    # again returns
    # [<FC_SH001_comp_Main_v001 (Version)>,
    #  <FC_SH001_comp_Main_v002 (Version)>,
    #  <FC_SH001_comp_Main_v003 (Version)>]

    # Both methods return a list of Version objects
    assert vers_from_python == vers_from_query

.. _Jinja2: http://jinja.pocoo.org/

.. note::

   Stalker stores :attr:`.Version.path` and :att:`.Version.filename` attribute
   values within the database, independent of your operating system. The
   :attr:`.Version.absolute_path` and :attr:`.Version.absolute_full_path`
   attributes provide OS-specific paths by combining the
   :attr:`.Repository.path` with the database values momentarily.

You can define default directories within your project structure using custom templates.

.. code-block:: python

    commercial_project_structure.custom_template = """
    Temp
    References
    References/Movies
    References/Images
    """

When executed, this template will generate the following directory structure:

.. code-block:: shell

    Temp
    References
        Movies
        Images
