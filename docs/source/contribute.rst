How To Contribute
*****************

Stalker started as an Open Source project with the expactation of
contributions. The soul of the open source is to share the knowledge and
contribute.

These are the areas that you can contribute to:
 * Documentation
 * Testing the code
 * Writing the code
 * Creating user interface elements (graphics, icons etc.)

Development Style
=================
Stalker is developed strictly by following `TDD`_ practices. So every
participant should follow TDD metadologly. Skipping this steps is highly
prohibited. Every added code to the trunk should have a corresponding test and
the tests should be written before implementing a single line of code.

.. _TDD: http://en.wikipedia.org/wiki/Test-driven_development

`DRY`_ is also another methodology that a participant should follow. So nothing
should be repeated. If someting needs to be repeated, then it is a good sign
that this part needs to be in a special module, class or function.

.. _DRY: http:http://en.wikipedia.org/wiki/Don%27t_repeat_yourself

Testing
=======
As stated above all the code written should have a corresponding test.

Adding new features should start with design sketches. These sketches could be
plain text files or mind maps or anything that can express the thing in you
mind. While writing down these sketches, it should be kept in mind that these
files also could be used to generate the documentation of the system. So
writing down the sketches as rest files inside the docs is something very
meaningful.

The design should be followed by the tests. And the test should be followed by
the implemantation, and the implamantation should be followed by tests again,
until you are confident about your code and it is rock solid. Then the
refactoring phase can start, and because you have enough tests that will keep
your code doing a certain thing, you can freely change your code, because you
know that you code will do the same thing if it passes all the tests.

The first tests written should always fail by having:

  ::
    
    self.fail('the test is not implemented yet')

failures. This is something good to have. This will inform us that the test is
not written yet. So lets start adding the code that will pass the tests.

The test framework of Stalker is unitTest and nose to help testing.

These python modules should be installed to test Stalker properly:

 * Nose
 * Coverage
 * Mocker

The Mocker library should be used to isolate the currently tested part of the
code.

The coverage of the tests should be kept as close as possible to %100.

There is a helper script in the root of the project, called *doTests*. This is
a shell script for linux, which runs all the neccessary tests and prints the
tests results and the coverage table.

Code Style
==========
For the general coding style every participant should strictly follow `PEP 8`_
rules, and there are some extra rules as listed below:
 * Class names should start with an upper-case letter, function and method
   names should start with lower-case letter
 
 * The class definitions should be precided by 72 `#` characters, if you are
   using Wing IDE it is trivial cause Wing has these kind of templates:
   
   ::
     
     ########################################################################
     class StatusBase(object):
         """The StatusBase class
         """
         pass
     
 * The method or function definitions should be precided by 70 `-` characters,
   and the line should be commented out, again if you are using Wing IDE it
   does that automatically
   
   ::
   
     #----------------------------------------------------------------------
     def __init__(self, name, abbreviation, thumbnail=None):
     
         self._name = self._checkName(name)
     
     
 * There should be 3 spaces before and after functions and class methods:
   ::
   
           ########################################################################
           class StatusBase(object):
               """The StatusBase class
               """
               
               
               
               #----------------------------------------------------------------------
               def __init__(self, name, abbreviation, thumbnail=None):
                   
                   self._name = self._checkName(name)
               
               
               
               #----------------------------------------------------------------------
               def _checkName(self, name):
                   """checks the name attribute
                   """
                   
                   if name == '' or not isinstance(name, (str, unicode) ):
                       raise(ValueError("the name shouldn't be empty and it should be a \
                       str or unicode"))
                   
                   return name.title()
   
 * and also there should be 6 spaces before and after a class body
   ::
   
           #-*- coding: utf-8 -*-
           """
           Copyright (C) 2010  Erkan Ozgur Yilmaz
           
           This program is free software: you can redistribute it and/or modify
           it under the terms of the GNU General Public License as published by
           the Free Software Foundation, either version 3 of the License, or
           (at your option) any later version.
           
           This program is distributed in the hope that it will be useful,
           but WITHOUT ANY WARRANTY; without even the implied warranty of
           MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
           GNU General Public License for more details.
           
           You should have received a copy of the GNU General Public License
           along with this program.  If not, see <http://www.gnu.org/licenses/>
           """
           
           
           
           
           
           ########################################################################
           class A(object):
               pass
           
           
           
           
           
           
           ########################################################################
           class B(object):
               pass
        
        
        
        
        
           
 * any lines that may contain a code or comment can not be longer than 80
   characters, all the longer lines should be canceled with "\\" character and
   should continue properly from the line below
   
   ::
   
       #----------------------------------------------------------------------
       def _checkName(self, name):
           """checks the name attribute
           """
           
           if name == '' or not isinstance(name, (str, unicode) ):
               raise(ValueError("the name shouldn't be empty and it should be a \
               str or unicode"))
           
           return name.title()

If you are going to add a new python file (*.py), there is an empty py file
with the name empty_code_template_file.py under docs/_static. Before starting
anything, dublicate this file and place it under the folder you want. This
files has the neccessary shebang and the GPL 3 license text.

.. _PEP 8: http://www.python.org/dev/peps/pep-0008/

SCM - Mercurial (HG)
====================
The choice of SCM is Mercurial. Every developer should be familiar with it. It
is a good start to go the `Selenic Mercuial Site`_ and do the tutorial if you
don't feel familiar enough with hg.

.. _Selenic Mercuial Site: http://mercurial.selenic.com 
