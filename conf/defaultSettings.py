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

STUDIO_DATABASE_ENGINE= 'sqlite3'
STUDIO_DATABASE_NAME = 'stalker_studio.db'
PROJECT_DATABASE_ENGINE = 'sqlite3'
PROJECT_DATABASE_NAME = ''

#
# the default projects path
#
PROJECTS_SERVERS = (
    # name , full path
    ('Imaj','M:/JOBs'),
    ('Stalker Development 1','/home/ozgur/Documents/Works/JOBs2'),
)

# 
# these are for new projects
# after creating the project you can change them from the interface
# 
SUPERUSER_NAME = 'admin'
SUPERUSER_EMAIL = 'admin@admin.com'