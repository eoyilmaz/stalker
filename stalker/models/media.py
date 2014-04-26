# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
from sqlalchemy import Column, Integer, ForeignKey
from stalker import Link


class Media(Link):
    """Holds information about image, video or audio files.

    :param int width: An integer value showing the width of this media. Only
      applicable to Image and Video files.

    :param int height: An integer value showing the height of this media. Only
      applicable to Image and Video files.

    :param timedelta duration: The duration of this media file. Applicable to
      Video and Audio files.

    :param int bitrate: Applicable to Video and Audio files, showing the

    :param mime_type: A :class:`.Type` instance showing the mime type of this
      media file. It is a synonym for ``type`` attribute.
    """

    __auto_name__ = True
    __mapper_args__ = {"polymorphic_identity": "Media"}
    __tablename__ = 'Medias'
    media_id = Column("id", Integer, ForeignKey("Links.id"), primary_key=True)

    def __init__(self,
                 width=None,
                 height=None,
                 duration=None,
                 bitrate=None,
                 **kwargs):
        super(Media, self).__init__(**kwargs)
