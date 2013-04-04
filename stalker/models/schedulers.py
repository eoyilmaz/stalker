# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
# 
# This file is part of Stalker.
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
import subprocess
import tempfile


class SchedulerBase(object):
    """This is the base class for schedulers.
    
    All the schedulers should be derived from this class.
    """
    def __init__(self, projects=None):
        self.projects = projects if projects else []
    
    def schedule(self):
        """the main scheduling function should be implemented in the
        derivatives
        """
        raise NotImplementedError


class TaskJugglerScheduler(SchedulerBase):
    """This is the main scheduler for Stalker right now.
    
    Integrates Stalker and TaskJuggler together by using TaskJugglerScheduler
    to solve the scheduling problem.
    
    TaskJugglerScheduler needs a list of
    :class:`~stalker.models.project.Project` instances to work with. TJS will
    combine them in to one .tjp file and then solve them and restore the task
    computed_start and computed_end dates. Combining all the Projects in one
    tjp file has a very nice side effect, projects using the same resources
    will respect their allocations to the resource.
    """
    
    
    def schedule(self):
        """does the scheduling
        """
        # create a tjp file
        tjp_file_path = tempfile.mktemp() + ".tjp"
        
        # fill it with data
        
        # pass it to tj3
        # wait it to complete
        # read back the csv file



