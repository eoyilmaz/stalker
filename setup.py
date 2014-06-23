import os

from setuptools import setup, find_packages

import stalker

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()
CHANGES = open(os.path.join(here, 'CHANGELOG')).read()

requires = [
    'sqlalchemy>=0.8',
    'alembic',
    'jinja2',
]

setup(
    name='stalker',
    version=stalker.__version__,
    description='A Production Asset Management (ProdAM) System',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
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
    url='http://github.com/eoyilmaz/stalker',
    keywords=['production', 'asset', 'management', 'vfx', 'animation',
              'maya', 'houdini', 'nuke', 'fusion', 'softimage', 'blender',
              'vue'],
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('', [
            'COPYING',
            'COPYING.LESSER',
            'INSTALL',
            'MANIFEST.in',
            'README'
        ]),
    ],
    zip_safe=True,
    test_suite='stalker',
    install_requires=requires,
)

