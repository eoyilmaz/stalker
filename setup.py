#-*- coding: utf-8 -*-

from distutils.core import setup
setup(name='stalker',
      version='0.0.1.alpha',
      author='Erkan Ozgur Yilmaz',
      author_email='eoyilmaz@gmail.com',
      packages = [ '',
                   'conf',
                   'db',
                   'docs',
                   'extensions',
                   'models',
                   'tests',
                   'tests.models',
                   'utils'],
      package_dir={'':''},
      package_data={'':''},
      platforms = ['any'],
      url='http://code.google.com/p/stalker/',
      license='http://www.opensource.org/licenses/bsd-license.php',
      )
