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

from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import validates

from stalker.models.entity import Entity

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class ImageFormat(Entity):
    """Common image formats for the :class:`.Project`\ s.

    :param width: The width of the format, it cannot be zero or negative, if a
      float number is given it will be converted to integer

    :param height: The height of the format, it cannot be zero or negative, if
      a float number is given it will be converted to integer

    :param pixel_aspect: The pixel aspect ratio of the current ImageFormat
      object, it can not be zero or negative, and if given as an integer it
      will be converted to a float, the default value is 1.0

    :param print_resolution: The print resolution of the ImageFormat given as
      DPI (dot-per-inch). It can not be zero or negative
    """
    __auto_name__ = False
    __tablename__ = "ImageFormats"
    __mapper_args__ = {"polymorphic_identity": "ImageFormat"}

    imageFormat_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )

    width = Column(
        Integer,
        doc="""The width of this format.

        * the width should be set to a positive non-zero integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception.
        """
    )

    height = Column(
        Integer,
        doc="""The height of this format

        * the height should be set to a positive non-zero integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception.
        """
    )

    pixel_aspect = Column(
        Float,
        default="1.0",
        doc="""The pixel aspect ratio of this format.

        * the pixel_aspect should be set to a positive non-zero float
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception
        """
    )

    print_resolution = Column(
        Float,
        default="300.0",
        doc="""The print resolution of this format

        * it should be set to a positive non-zero float or integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception.
        """
    )

    def __init__(self,
                 width=None,
                 height=None,
                 pixel_aspect=1.0,
                 print_resolution=300,
                 **kwargs):
        super(ImageFormat, self).__init__(**kwargs)

        self.width = width
        self.height = height
        self.pixel_aspect = pixel_aspect
        self.print_resolution = print_resolution
        # self._device_aspect = 1.0

    @validates("width")
    def _validate_width(self, key, width):
        """validates the given width
        """
        if not isinstance(width, (int, float)):
            raise TypeError(
                "%s.width should be an instance of int or float not %s" %
                (self.__class__.__name__, width.__class__.__name__)
            )

        if width <= 0:
            raise ValueError(
                "%s.width shouldn't be zero or negative" %
                self.__class__.__name__
            )

        return int(width)

    @validates("height")
    def _validate_height(self, key, height):
        """validates the given height
        """
        if not isinstance(height, (int, float)):
            raise TypeError(
                "%s.height should be an instance of int or float not %s" %
                (self.__class__.__name__, height.__class__.__name__)
            )

        if height <= 0:
            raise ValueError(
                "%s.height shouldn't be zero or negative" %
                self.__class__.__name__
            )

        return int(height)

    @validates("pixel_aspect")
    def _validate_pixel_aspect(self, key, pixel_aspect):
        """validates the given pixel aspect
        """

        if not isinstance(pixel_aspect, (int, float)):
            raise TypeError(
                "%s.pixel_aspect should be an instance of int or float not %s"
                % (self.__class__.__name__, pixel_aspect.__class__.__name__)
            )

        if pixel_aspect <= 0:
            raise ValueError(
                "%s.pixel_aspect can not be zero or a negative value" %
                self.__class__.__name__
            )

        return float(pixel_aspect)

    @validates("print_resolution")
    def _validate_print_resolution(self, key, print_resolution):
        """validates the print resolution
        """

        if not isinstance(print_resolution, (int, float)):
            raise TypeError(
                "%s.print_resolution should be an instance of int or float "
                "not %s" %
                (self.__class__.__name__, print_resolution.__class__.__name__)
            )

        if print_resolution <= 0:
            raise ValueError(
                "%s.print_resolution should not be zero or negative" %
                self.__class__.__name__
            )

        return float(print_resolution)

    @property
    def device_aspect(self):
        """returns the device aspect

        because the device_aspect is calculated from the width/height*pixel
        formula, this property is read-only.
        """
        return float(self.width) / float(self.height) * self.pixel_aspect

    def __eq__(self, other):
        """the equality operator
        """
        return super(ImageFormat, self).__eq__(other) and \
            isinstance(other, ImageFormat) and \
            self.width == other.width and \
            self.height == other.height and \
            self.pixel_aspect == other.pixel_aspect

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(ImageFormat, self).__hash__()
