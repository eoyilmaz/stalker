How to Install Stalker
**********************

This document will let you install and run Stalker.

Install Python
==============

Stalker is completely written with Python, so it requires Python. It currently
works with Python version 2.5 to 2.7.

Because Stalker is based on some other Python packages first you need to
install them. Follow the links below to read their documentation about install:
  
  1. `Sqlalchemy`_
  2. `Jinja2`_
  3. `Beaker`_

.. _Sqlalchemy: http://www.sqlalchemy.org/docs/intro.html#installing-sqlalchemy
.. _Jinja2: http://jinja.pocoo.org/
.. _Beaker: http://beaker.groovie.org/

or for the impatient one just run these commands in the shell, these will
install the latest versions of the packages::
  
  python easy_install -U sqlalchemy jinja2 beaker

To install Stalker there are couple of routes those you can choose to follow:
  
  * install it from PyPI/Cheese Shop:
    
    Just run the following command in your system shell::
    
      python easy_install -U stalker
  
  * install it from the tarball release file:
    
    1. Download the most recent tarball file from `download page`_
    
    .. _download page: http://pypi.python.org/pypi/stalker
  
  * installing the development version
    
    1. install `Mercurial`_
    2. hg clone https://stalker.googlecode.com/hg/ stalker
    3. cd stalker
    4. ln -s stalker /usr/lib/python2.X/site-packages
    
    the forth step is for linux/unix variants. As an alternative to it you can
    add the stalker folder to PYTHONPATH environment variable both in linux and
    Windows.
    
    .. _Mercurial: http://mercurial.selenic.com 
    
For developers
==============

Developers also need to install these packages:
  
  1. Nose
  2. Coverage
  3. Mocker
  4. Sphinx
  5. Pygments
  
  The following command will install them all::
    
    python easy_install nose coverage mocker sphinx pygments
  
  



