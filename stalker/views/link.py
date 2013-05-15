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
import uuid
import os
from pyramid.httpexceptions import HTTPOk
from pyramid.view import view_config
from stalker import defaults, Link, Entity


view_config(
    route_name='upload_reference'
)
def upload_reference(request):
    """called when uploading a reference

    Uses the hex representation of a uuid4 sequence as the filename.

    The first two digits of the uuid4 is used for the first folder name,
    there are 256 possible variations, then the third and fourth characters
    are used for the second folder name (again 256 other possibilities) and
    then the uuid4 sequence with the original file extension generates the
    filename.

    The extension is used on purpose where OSes like windows can infer the file
    type from the extension.

    {{server_side_storage_path}}/{{uuid4[:2]}}/{{uuid4[2:4]}}//{{uuuid4}}.extension

    """
    
    entity_id = request.matchdict.get('entity_id')
    entity = Entity.query.filter_by(id=entity_id).first()
    
    # check if entity accepts references
    
    
    # get the filename
    link = request.POST.get('link')
    filename = link.filename
    extension = os.path.splitext(filename)[1]
    input_file = link.file

    # upload it to the stalker server side storage path

    new_filename = uuid.uuid4().hex + extension

    first_folder = new_filename[:2]
    second_folder = new_filename[2:4]

    file_path = os.path.join(
        defaults.server_side_storage_path,
        first_folder,
        second_folder,
        new_filename
    )

    # write down to a temp file first
    temp_file_path = file_path + '~'

    output_file = open(temp_file_path, 'wb') # TODO: guess ascii or binary mode    

    input_file.seek(0)
    while True: # TODO: use 'with'
        data = input_file.read(2<<16)
        if not data:
            break
        output_file.write(data)
    output_file.close()

    # data is written completely, rename temp file to original file
    os.rename(temp_file_path, file_path)
    
    
    # create a Link and assign it to the given Referencable Entity
    new_link = Link(
        path = file_path,
        original_filename=filename
    )
    
    # assign it as a reference
    
    return HTTPOk()


