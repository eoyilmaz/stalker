#-*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
import stalker


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

required_packages = ["beaker", "jinja2", "sqlalchemy",]

setup(name="stalker",
      version=stalker.__version__,
      author="Erkan Ozgur Yilmaz",
      author_email="eoyilmaz@gmail.com",
      description=("A Production Asset Management (ProdAm) System"),
      long_description=read("README"),
      keywords=["production", "asset", "management", "vfx", "animation", "maya"
                "houdini", "nuke", "xsi"],
      packages=find_packages(exclude=["tests*"]),
      platforms=["any"],
      url="http://code.google.com/p/stalker/",
      license="http://www.opensource.org/licenses/bsd-license.php",
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Development Status :: 1 - Planning",
          "Intended Audience :: Developers",
          "Intended Audience :: End Users/Desktop",
          "Topic :: Database",
          "Topic :: Software Development",
          "Topic :: Utilities",
          "Topic :: Office/Business :: Scheduling",
      ],
      requires=required_packages,
      install_requires=required_packages,
)
