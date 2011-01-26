#-*- coding: utf-8 -*-
"""
In this example we are going to extend the Stalker Object Model (SOM) with two
new type of classes which are derived from the
:class:`~stalker.core.models.entity.Entity` class.

One of our new classes is going to hold information about Camera, or more
spesifically it will hold the information of the Camera used on the set for a
shooting. The Camera class should hold these information:
 
 * The make of the camera
 * The model of the camera
 * spesifications like:
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
:class:`~stakler.core.models.mixin.ReferenceMixin` in this example, which is
explained in other examples, we are going to use simple STRINGs for the web
page links.

And because we don't want to again make things complex we are not
going to touch the :class:`~stalker.core.models.shot.Shot` class which probably
will benefit these two classes. In normal circumstances we would like to
introduce a new class which derives from the original
:class:`~stalker.core.models.shot.Shot` and add these Camera and Lens
relations to it. But again to not to make things complex we are just going to
settle with these two.

Don't foreget that, for the sake of brevity we are skipping a lot of things
while creating these classes, first of all we are not doing any validation on
the data given to us. Secondly we are not using any properties, but we are
giving the bare class variables to the users of our classes. And because we are
not using any properties we are mapping the tables directly to our classes
without setting up any synonyms for our attributes.
"""



from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import mapper, relationship

from stalker import db
from stalker.db import tables
from stalker.core.models.entity import Entity






########################################################################
class Camera(Entity):
    """The Camera class holds basic information about the Camera used on the
    sets.
    
    :param make: the make of the camera
    
    :param model: the model of the camera
    
    :param aperture_gate: the aperture gate opening distance
    
    :param horizontal_film_back: the horizantal length of the filmback
    
    :param vertical_film_back: the vertical length of the filmback
    
    :param cropping_factor: the cropping factor of the camera
    
    :param web_page: the web page of the camera
    
    """
    
    #----------------------------------------------------------------------
    def __init__(self,
                 make="",
                 model="",
                 aperture_gate=0,
                 horizontal_film_back=0,
                 vertical_film_back=0,
                 cropping_factor=1.0,
                 web_page="",
                 **kwargs):
        
        # pass all the extra data to Entity
        super(Camera, self).__init__(**kwargs)
        
        self.make = make
        self.model = model
        self.aperture_gate = aperture_gate
        self.horizontal_film_back = horizontal_film_back
        self.vertical_film_back = vertical_film_back
        self.cropping_factor = cropping_factor
        self.web_page = web_page






########################################################################
class Lens(Entity):
    """The Lens class holds data about lenses used in shootings
    
    :param make: the make of the lens
    
    :param model: the model of the lens
    
    :param min_focal_length: the min_focal_length
    
    :param max_focal_length: the max_focal_length
    
    :param web_page: the product web page
    """
    
    #----------------------------------------------------------------------
    def __init__(self,
                 make="",
                 model="",
                 min_focal_length=0,
                 max_focal_length=0,
                 web_page="",
                 **kwargs
                 ):
        
        # pass all the extra data to Entity
        super(Lens, self).__init__(**kwargs)
        
        self.make = make
        self.model = model
        self.min_focal_length = min_focal_length
        self.max_focal_length = max_focal_length
        self.web_page = web_page



#----------------------------------------------------------------------
def setup():
    """this is the setup method for Stalker to call to learn about how to
    persist our classes.
    """
    
    metadata = db.metadata
    
    # Camera
    cameras_table = Table(
        "cameras", metadata,
        Column(
            "id",
            Integer,
            ForeignKey(tables.entities.c.id),
            primary_key=True
        ),
        Column("make", String),
        Column("model", String),
        Column("aperture_gate", Float(precision=4)),
        Column("horizontal_film_back", Float(presicion=4)),
        Column("vertical_film_back", Float(precision=4)),
        Column("cropping_factor", Float(precision=4)),
        Column("web_page", String),
    )
    
    # Lens
    lenses_table = Table(
        "lenses", metadata,
        Column(
            "id",
            Integer,
            ForeignKey(tables.entities.c.id),
            primary_key=True
        ),
        Column("make", String),
        Column("model", String),
        Column("min_focal_length", Float(precision=1)),
        Column("max_focal_length", Float(precision=1)),
        Column("web_page", String),
    )
    
    # map Camera
    mapper(
        Camera,
        cameras_table,
        inherits=Camera.__base__,
        polymorphic_identity=Camera.entity_type,
    )
    
    # map Lens
    mapper(
        Lens,
        lenses_table,
        inherits=Lens.__base__,
        polymorphic_identity=Lens.entity_type,
    )
    
    # now we have extended SOM with two new classes
