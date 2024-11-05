.. _tutorial_basics_toplevel:

Basics
======

Imagine you've just installed Stalker and want to integrate it into your first
project. The first step involves connecting to the database to store
information about your studio and projects.

Connecting to the Database
--------------------------

A helper function is provided for connecting to the default database. Use the
following command:

.. code-block:: python

    from stalker.db.setup import setup
    setup({"sqlalchemy.url": "sqlite:///"})

This creates an in-memory SQLite3 database, suitable only for testing. For
practical use, consider a file-based SQLite3 database:

.. code-block:: python

    # Windows
    setup({"sqlalchemy.url": "sqlite:///C:/studio.db"})

    # Linux or macOS
    setup({"sqlalchemy.url": "sqlite:////home/ozgur/studio.db"})


This command will do the following:

1. **Database Connection:** Creates an `engine`_ to establish the connection.
2. **Database Creation:** Creates the SQLite3 database file if doesn't exist.
3. **Session Creation:** Creates a `session`_ instance for interacting with the
   database.
4. **Mapping:** Defines how SOM classes `map`_ to database tables (see
   SQLAlchemy documentation for details).

.. _session: http://www.sqlalchemy.org/docs/orm/session.html
.. _engine: http://www.sqlalchemy.org/docs/core/engines.html
.. _map: http://www.sqlalchemy.org/docs/orm/mapper_config.html

.. note::

   While SQLite3 support was officially dropped in Stalker v0.2.18, it's still
   possible to use SQLite3 databases with Stalker. However, PostgreSQL (versions
   14 to 17) is the recommended database backend.

Database Initialization
-----------------------

On your initial connection, use `db.init()` to create essential default data
for Stalker to function properly:

.. code-block:: python

    db.init()

This is a one-time operation; subsequent calls to `db.init()` won't break
anything, but they're unnecessary.

Creating a Studio
-----------------

Let's create a :class:`.Studio` object to represent your studio:

.. code-block:: python

    from stalker import Studio
    my_studio = Studio(
        name='My Great Studio'
    )

We'll explain the concept of :class:`.Studio` later in the tutorial.

Creating a User
---------------

Now, let's create a :class:`.User` object representing yourself in the
database:

1. Import the :class:`.User` class:

   .. code-block:: python

        from stalker import User

2. Create the :class:`.User` object:

   .. code-block:: python

        me = User(
            name="Erkan Ozgur Yilmaz",
            login="eoyilmaz",
            email="some_email_address@gmail.com",
            password="secret",
            description="This is me"
        )

This creates a user object that represents you.

Creating and Assigning a Department
-----------------------------------

1. Import the :class:`.Department` class:

   .. code-block:: python

        from stalker import Department

2. Create a :class:`.Department` object:

   .. code-block:: python

        tds_department = Department(
            name="TDs",
            description="This is the TDs department"
        )

3. Assign yourself to the department:

There are two ways to do this:

* Using the :class:`.Department` object:

  .. code-block:: python

    tds_department.users.append(me)

* Using the :class:`.User` object:

  .. code-block:: python

    me.departments.append(tds_department)

Both methods achieve the same result.

Verifying Department Assignment
-------------------------------

You can verify the assignment by printing the :attr:`.User.departments` for
your user:

.. code-block:: python

    print(me.departments)
    # Output: [<TDs (Department)>]

Saving Data to the Database
---------------------------

So far, the data hasn't been saved to the database yet. To commit the changes,
use the :class:`.DBSession` object:

.. code-block:: python

    from stalker.db.session import DBSession

    DBSession.add(my_studio)
    DBSession.add(me)
    DBSession.add(tds_department)
    DBSession.commit()

Retrieving Data
---------------

Let's retrieve data from the database. Here, we'll fetch all departments, get
the second one (excluding the default `admins` department), and print the name
of its first member:

.. code-block:: python

    all_departments = Department.query.all()
    print(all_departments)
    # Output: [<admins (Department)>, <TDs (Department)>]
    # "admins" department is created by default

    admins = all_departments[0]
    tds = all_departments[1]

    all_users = tds.users  # Department.users is a "synonym" for Department.members
    #                        they are essentially the same attribute

    print(all_users[0])
    # Output: <Erkan Ozgur Yilmaz ('eoyilmaz') (User)>

This retrieves and prints the information.
