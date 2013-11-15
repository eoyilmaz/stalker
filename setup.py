import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()
CHANGES = open(os.path.join(here, 'CHANGELOG')).read()

requires = [
    'sqlalchemy>=0.8',
    'alembic',
    'jinja2',
    'unittest2',
    'mocker',
]

setup(
    name='stalker',
    version='0.2.3.1',
    description='A Production Asset Management (ProdAM) System',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
      "Programming Language :: Python",
      "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
      "Operating System :: OS Independent",
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "Intended Audience :: End Users/Desktop",
      "Topic :: Database",
      "Topic :: Software Development",
      "Topic :: Utilities",
      "Topic :: Office/Business :: Scheduling",
    ],
    author='Erkan Ozgur Yilmaz',
    author_email='eoyilmaz@gmail.com',
    url='http://code.google.com/p/stalker/',
    keywords=['production', 'asset', 'management', 'vfx', 'animation',
              'maya', 'houdini', 'nuke', 'fusion', 'softimage', 'blender',
              'vue'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    test_suite='stalker',
    install_requires=requires,
)

