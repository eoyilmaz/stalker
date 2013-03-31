# -*- coding: utf-8 -*-
# Copyright (c) 2009-2013, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import logging
from pyramid.httpexceptions import HTTPServerError
from pyramid.view import view_config
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)

def log_param(request, param):
    if param in request.params:
        logger.debug('%s: %s' % (param, request.params[param]))
    else:
        logger.debug('%s not in params' % param)



# register exception views

from pyramid.response import  Response

@view_config(
   context=HTTPServerError 
)
def server_error(exc, request):
    msg = exc.args[0] if exc.args else ''
    response = Response('Server Error: %s' % msg)
    response.status_int = 500
    return response




























