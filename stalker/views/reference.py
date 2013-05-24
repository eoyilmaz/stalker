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

from pyramid.httpexceptions import HTTPOk, HTTPServerError
from pyramid.view import view_config
from stalker import Link, Entity
from stalker.db import DBSession
from stalker.views import upload_file_to_server


view_config(
    route_name='upload_reference'
)
def upload_reference(request):
    """called when uploading a reference
    """

    entity_id = request.matchdict.get('entity_id')
    entity = Entity.query.filter_by(id=entity_id).first()

    # check if entity accepts references
    try:
        if not entity.accepts_references:
            raise HTTPServerError()
    except AttributeError as e:
        raise HTTPServerError(msg=e.message)

    filename, file_path = upload_file_to_server(request, 'link')

    # create a Link and assign it to the given Referencable Entity
    new_link = Link(
        full_path= file_path,
        original_filename=filename
    )

    # assign it as a reference
    entity.references.append(new_link)

    DBSession.add(new_link)

    return HTTPOk()
