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

import logging

from pyramid.httpexceptions import HTTPOk
from pyramid.view import view_config

from stalker.db import DBSession
from stalker import log, Studio, WorkingHours
from stalker.views import get_time, PermissionChecker

logger = logging.getLogger(__name__)
log.logging_level = logging.DEBUG
logger.setLevel(log.logging_level)


@view_config(
    route_name='dialog_create_studio',
    renderer='templates/studio/dialog_create_studio.jinja2'
)
def create_studio_dialog(request):
    """creates the content of the create_studio_dialog
    """
    return {
        'mode': 'CREATE',
        'has_permission': PermissionChecker(request)
    }


@view_config(
    route_name='dialog_update_studio',
    renderer='templates/studio/dialog_create_studio.jinja2'
)
def update_studio_dialog(request):
    """updates the given studio
    """
    return {
        'mode': 'UPDATE',
        'has_permission': PermissionChecker(request),
        'studio': Studio.query.first()
    }


@view_config(
    route_name='create_studio'
)
def create_studio(request):
    """creates the studio
    """
    name = request.params.get('name', None)
    dwh = request.params.get('dwh', None)
    wh_mon_start = get_time(request, 'mon_start')
    wh_mon_end   = get_time(request, 'mon_end')
    wh_tue_start = get_time(request, 'tue_start')
    wh_tue_end   = get_time(request, 'tue_end')
    wh_wed_start = get_time(request, 'wed_start')
    wh_wed_end   = get_time(request, 'wed_end')
    wh_thu_start = get_time(request, 'thu_start')
    wh_thu_end   = get_time(request, 'thu_end')
    wh_fri_start = get_time(request, 'fri_start')
    wh_fri_end   = get_time(request, 'fri_end')
    wh_sat_start = get_time(request, 'sat_start')
    wh_sat_end   = get_time(request, 'sat_end')
    wh_sun_start = get_time(request, 'sun_start')
    wh_sun_end   = get_time(request, 'sun_end')
    
    if name and dwh:
        # create new studio
        studio = Studio(
            name=name,
            daily_working_hours=int(dwh)
        )
        wh = WorkingHours()
        
        def set_wh_for_day(day, start, end):
            if start != end:
                wh[day] = [[start.seconds/60, end.seconds/60]]
            else:
                wh[day] = []
        
        set_wh_for_day('mon', wh_mon_start, wh_mon_end)
        set_wh_for_day('tue', wh_tue_start, wh_tue_end)
        set_wh_for_day('wed', wh_wed_start, wh_wed_end)
        set_wh_for_day('thu', wh_thu_start, wh_thu_end)
        set_wh_for_day('fri', wh_fri_start, wh_fri_end)
        set_wh_for_day('sat', wh_sat_start, wh_sat_end)
        set_wh_for_day('sun', wh_sun_start, wh_sun_end)
        
        studio.working_hours = wh
        
        DBSession.add(studio)
        # Commit will be handled by the zope transaction extension
        
    return HTTPOk()

