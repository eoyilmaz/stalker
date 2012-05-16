# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
from stalker.db.session import DBSession
from stalker.models.auth import User

def groupfinder(userid, request):
    # return the group of the given User object
    user_obj = DBSession.query(User).filter(User.login_name==userid).first()
    
    if user_obj:
        return user_obj.permission_groups
    
    return []
