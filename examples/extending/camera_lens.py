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
"""
In this example we are going to extend the Stalker Object Model (SOM) with two
new type of classes which are derived from the
:class:`stalker.models.entity.Entity` class.

One of our new classes is going to hold information about Camera, or more
specifically it will hold the information of the Camera used on the set for a
shooting. The Camera class should hold these information:

 * The make of the camera
 * The model of the camera
 * specifications like:
   * aperture gate
   * horizontal film back size
   * vertical film back size
   * cropping factor
 * media it uses (film or digital)
 * The web page of the product if available

The other class is going to be the Lens. A Lens class should hold these
information:

 * The make of the lens
 * The model of the lens
 * min focal length
 * max focal length (for zooms, it will be the same for prime lenses)
 * The web page of the product if available

To make this example simple and to not introduce the
:class:`~stalker.models.mixins.ReferenceMixin` in this example, which is
explained in other examples, we are going to use simple STRINGs for the web
page links of the manufacturer.

And because we don't want to again make things complex we are not
going to touch the :class:`stalker.models.shot.Shot` class which probably
will benefit these two classes. In normal circumstances we would like to
introduce a new class which derives from the original
:class:`stalker.models.shot.Shot` and add these Camera and Lens
relations to it. But again to not to make things complex we are just going to
settle with these two.

Don't forget that, for the sake of brevity we are skipping a lot of things
while creating these classes, first of all we are not doing any validation on
the data given to us. Secondly we are not using any properties, but we are
giving the bare class variables to the users of our classes. And because we are
not using any properties we are mapping the tables directly to our classes
without setting up any synonyms for our attributes.
"""

from sqlalchemy import Column, Integer, Float, ForeignKey, String
from stalker import Entity


class Camera(Entity):
    """The Camera class holds basic information about the Camera used on the
    sets.

    :param make: the make of the camera

    :param model: the model of the camera

    :param aperture_gate: the aperture gate opening distance

    :param horizontal_film_back: the horizontal length of the film back

    :param vertical_film_back: the vertical length of the film back

    :param web_page: the web page of the camera
    """

    __tablename__ = 'Cameras'
    __mapper_args__ = {'polymorphic_identity': 'Camera'}

    camera_id = Column('id', Integer, ForeignKey('Entities.id'),
                       primary_key=True)
    make = Column(String)
    model = Column(String)
    aperture_gate = Column(Float(precision=4), default=0)
    horizontal_film_back = Column(Float(presicion=4), default=0)
    vertical_film_back = Column(Float(precision=4), default=0)
    web_page = Column(String)

    def __init__(self,
                 make="",
                 model="",
                 aperture_gate=0,
                 horizontal_film_back=0,
                 vertical_film_back=0,
                 web_page="",
                 **kwargs):
        # pass all the extra data to the super (which is Entity)
        super(Camera, self).__init__(**kwargs)

        self.make = make
        self.model = model
        self.aperture_gate = aperture_gate
        self.horizontal_film_back = horizontal_film_back
        self.vertical_film_back = vertical_film_back
        self.web_page = web_page


class Lens(Entity):
    """The Lens class holds data about lenses used in shootings

    :param make: the make of the lens

    :param model: the model of the lens

    :param min_focal_length: the min_focal_length

    :param max_focal_length: the max_focal_length

    :param web_page: the product web page
    """

    __tablename__ = 'Lenses'
    __mapper_args__ = {'polymorphic_identity': 'Lens'}

    lens_id = Column('id', Integer, ForeignKey('Entities.id'),
                     primary_key=True)
    make = Column(String)
    model = Column(String)
    min_focal_length = Column(Float(precision=1))
    max_focal_length = Column(Float(precision=1))
    web_page = Column(String)

    def __init__(self,
                 make="",
                 model="",
                 min_focal_length=0,
                 max_focal_length=0,
                 web_page="",
                 **kwargs):
        # pass all the extra data to the super (which is Entity)
        super(Lens, self).__init__(**kwargs)

        self.make = make
        self.model = model
        self.min_focal_length = min_focal_length
        self.max_focal_length = max_focal_length
        self.web_page = web_page

# now we have extended SOM with two new classes
