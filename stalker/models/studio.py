# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause


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
