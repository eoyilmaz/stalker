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


from stalker.models.entity import SimpleEntity


class Studio(SimpleEntity):
    """Manage all the studio information at once.
    
    With Stalker you can manage all you Studio data by using this class. Studio
    knows all the projects, all the departments, all the users and ever thing
    about the studio. But the most important part of the Studio is that it can
    schedule all the Projects by using TaskJuggler.
    
    Studio class is kind of the database itself::
      
      studio = Studio()
      
      # simple data
      studio.projects
      studio.active_projects
      studio.inactive_projects
      studio.departments
      studio.users
      
      # project management
      studio.to_tjp          # a tjp representation of the studio with all
                             # its projects, departments and resources etc.
      
      studio.schedule_active_projects() # schedules all the active projects at
                                        # once
    
    """
    
    pass
