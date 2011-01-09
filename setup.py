#-*- coding: utf-8 -*-

import os
from setuptools import setup
import stalker


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# COPIED FROM DJANGO

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
stalker_dir = 'stalker'

for dirpath, dirnames, filenames in os.walk(stalker_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])



setup(name="stalker",
      version=stalker.__version__,
      author="Erkan Ozgur Yilmaz",
      author_email="eoyilmaz@gmail.com",
      description=("Prodcution Asset Management System (ProdAm)"),
      long_description=read('README'),
      keywords=["production", "asset", "management"],
      packages = packages,
      data_files = data_files,
      platforms = ["any"],
      url="http://code.google.com/p/stalker/",
      license="http://www.opensource.org/licenses/bsd-license.php",
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: BSD License",
          "Operation System :: OS Independent",
          "Development Status :: 1 - Planning",
          "Intended Audience :: Developers",
          "Intended Audience :: End Users/Desktop",
          "Topic :: Database",
          "Topic :: Software Development",
          "Topic :: Utilities",
          "Topic :: Office/Business :: Scheduling",

      ],
)
