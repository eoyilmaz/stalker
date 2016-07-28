.. upgrade_db_toplevel:

==================
Upgrading Database
==================

Introduction
============

From time to time, with new releases of Stalker, your Stalker database may need
to be upgraded. This is done with the `Alembic`_ library, which is a database
migration library for `SQLAlchemy`_.

.. _Alembic: http://alembic.zzzcomputing.com/en/latest/
.. _SQLAlchemy: http://www.sqlalchemy.org

Instructions
============

The upgrade is easy, just run the following command on the root of the stalker
installation directory::

  # for Windows
  ..\Scripts\alembic.exe upgrade head

  # for Linux or OSX
  ../bin/alembic upgrade head

  # this should output something like that:
  #
  # INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
  # INFO  [alembic.runtime.migration] Will assume transactional DDL.
  # INFO  [alembic.runtime.migration] Running upgrade 745b210e6907 -> f2005d1fbadc, added ProjectClients

That's it, your database is now migrated to the latest version.