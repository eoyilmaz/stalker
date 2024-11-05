.. _tutorial_query_update_delete_data_toplevel:

Querying, Updating and Deleting Data
====================================

Now that you've created some data, let's explore how to update and delete it.

Updating Data
-------------

Imagine you created a shot with incorrect information:

.. code-block:: python

    sh004 = Shot(
        code='SH004',
        project=new_project,
        sequences=[seq1]
    )
    DBSession.add(sh004)
    DBSession.commit()

Later, you realize you need to fix the code:

.. code-block:: python

    sh004.code = "SH005"
    DBsession.commit()

Retrieving Data
---------------

To retrieve a shot from the database, you can use a query:

.. code-block:: python

    wrong_shot = Shot.query.filter_by(code="SH005").first()

This retrieves the first shot with the code "SH005".

Updating Retrieved Data
-----------------------

If you need to modify the retrieve data:

.. code-block:: python

    wrong_shot.code = "SH004"  # Correct the code
    DBsession.commit()  # Save the changes

Deleting Data
-------------

To delete data, use the :meth:`DBSession.delete()` method:

.. code-block:: python

    DBsession.delete(wrong_shot)
    DBsession.commit()

After deleting data, you program variables might still hold references to the
deleted objects, but those objects no longer exist in the database.

.. code-block:: python

    wrong_shot = Shot.query.filter_by(code="SH005").first()
    print(wrong_shot) # This will print None

For More information
--------------------

For advanced update and delete options (like cascades) in SQLAlchemy, refer to
the official `SQLAlchemy documentation`_.

.. _SQLAlchemy documentation: http://www.sqlalchemy.org/docs/orm/session.html
