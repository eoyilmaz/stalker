.. _installation_toplevel:

============
Installation
============


How to Install Stalker
======================


This document will help you install and run Stalker.

Install Python
==============

Stalker is completely written with Python, so it requires Python. It currently
works with Python version 2.6 and 2.7. So you first need to have Python
installed in your system. On Linux and OSX there is a system wide Python
already installed. For Windows, you need to download the Python installer
suitable for your Windows operating system (32 or 64 bit) from `Python.org`_

.. _Python.org: http://www.python.org/

Install Stalker
===============

The easiest way to install the latest version of Stalker along with all its
dependencies is to use the `setuptools`. If your system doesn't have setuptools
(particularly Windows) you need to install `setuptools` by using `ez_setup`
bootstrap script.

Installing `setuptools` with `ez_setup`:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These steps are generally needed just for Windows. Linux and OSX users can skip
this part.

1. download `ez_setup.py`_
2. run the following command in the command prompt/shell/terminal::
  
    python ez_setup
  
  It will install or build the `setuptools` if there are no suitable installer
  for your operating system.

.. _ez_setup.py: http://peak.telecommunity.com/dist/ez_setup.py

Installing Stalker (All OSes):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After installing the `setuptools` you can run the following command::

  easy_install -U stalker

Now you have installed Stalker along with all its dependencies.

Checking the installation of Stalker
====================================

If everything went ok you should be able to import and check the version of
Stalker by using the Python prompt like this::
  
  >>> import stalker
  >>> stalker.__version__
  0.2.5

For developers
==============

It is highly recommended to create a VirtualEnv specific for Stalker
development. So to setup a virtualenv for Stalker::

  cd ~/Documents/development
  virtualenv --no-site-packages stalker

Then clone the repository (you need mercurial to do that)::

  cd stalker
  hg clone https://stalker.googlecode.com/hg/ stalker 

And then to setup the virtual environment for development::

  cd stalker
  ../bin/python setup.py develop

This command should install any dependent package to the virtual environment.

Installing a Database
=====================

Stalker uses a database to store all the data. The only database backend that
doesn't require any extra installation is SQLite3. You can setup Stalker to run
with an SQLite3 database. But it is much suitable to have a dedicated database
server in your studio. And it is recommended to use the same kind of database
backend both in development and production to reduce any compatibility problems
and any migration headaches.

Although Stalker is mainly tested and developed on SQLite3, the developers of
Stalker are using it in a studio environment where the main database is
PosgreSQL, and it is the recommended database for any application based on
Stalker. But, testing and using Stalker in any other database is encouraged. 

See the `SQLAlchemy documentation`_ for supported databases.

.. _SQLAlchemy documentation: http://www.sqlalchemy.org/docs/core/engines.html#supported-dbapis
