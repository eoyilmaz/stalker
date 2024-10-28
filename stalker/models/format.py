# -*- coding: utf-8 -*-
"""Image format related classes and utility functions are situated here."""
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import validates

from stalker.log import get_logger
from stalker.models.entity import Entity

logger = get_logger(__name__)


class ImageFormat(Entity):
    """Common image formats for the :class:`.Project` s.

    Args:
        width (Union[int, float]): The width of the format, it cannot be zero or
            negative, if a float number is given it will be converted to integer.

        height (Union[int, float]): The height of the format, it cannot be zero or
            negative, if a float number is given it will be converted to integer.

        pixel_aspect ((Union[int, float])): The pixel aspect ratio of the current
            ImageFormat object, it cannot be zero or negative, and if given as an
            integer it will be converted to a float, the default value is 1.0.

        print_resolution (Union[int, float]): The print resolution of the ImageFormat
            given as DPI (dot-per-inch). It cannot be zero or negative.
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
        """,
    )

    height = Column(
        Integer,
        doc="""The height of this format

        * the height should be set to a positive non-zero integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception.
        """,
    )

    pixel_aspect = Column(
        Float,
        default="1.0",
        doc="""The pixel aspect ratio of this format.

        * the pixel_aspect should be set to a positive non-zero float
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception
        """,
    )

    print_resolution = Column(
        Float,
        default="300.0",
        doc="""The print resolution of this format

        * it should be set to a positive non-zero float or integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception.
        """,
    )

    def __init__(
        self, width=None, height=None, pixel_aspect=1.0, print_resolution=300, **kwargs
    ):
        super(ImageFormat, self).__init__(**kwargs)

        self.width = width
        self.height = height
        self.pixel_aspect = pixel_aspect
        self.print_resolution = print_resolution
        # self._device_aspect = 1.0

    @validates("width")
    def _validate_width(self, key, width):
        """Validate the given width.

        Args:
            key (str): The name of the validated column.
            width (Union[int, float]): The width value to be validated.

        Raises:
            TypeError: If the width is not an int or float.
            ValueError: If the width is 0 or a negative value.

        Returns:
            int: The validated width value.
        """
        if not isinstance(width, (int, float)):
            raise TypeError(
                "%s.width should be an instance of int or float not %s"
                % (self.__class__.__name__, width.__class__.__name__)
            )

        if width <= 0:
            raise ValueError(
                "%s.width cannot be zero or negative" % self.__class__.__name__
            )

        return int(width)

    @validates("height")
    def _validate_height(self, key, height):
        """Validate the given height.

        Args:
            key (str): The name of the validated column.
            height (Union[int, float]): The height value to be validated.

        Raises:
            TypeError: If the height is not an int or float.
            ValueError: If the height is 0 or a negative value.

        Returns:
            int: The validated height value.
        """
        if not isinstance(height, (int, float)):
            raise TypeError(
                "%s.height should be an instance of int or float not %s"
                % (self.__class__.__name__, height.__class__.__name__)
            )

        if height <= 0:
            raise ValueError(
                "%s.height cannot be zero or negative" % self.__class__.__name__
            )

        return int(height)

    @validates("pixel_aspect")
    def _validate_pixel_aspect(self, key, pixel_aspect):
        """Validate the given pixel aspect.

        Args:
            key (str): The name of the validated column.
            pixel_aspect (Union[int, float]): The pixel_aspect value to be validated.

        Raises:
            TypeError: If the given pixel_aspect value is not an int for float.
            ValueError: If the pixel_aspect is 0 or a negative value.

        Returns:
            float: The validated pixel_aspect value.
        """
        if not isinstance(pixel_aspect, (int, float)):
            raise TypeError(
                "%s.pixel_aspect should be an instance of int or float not %s"
                % (self.__class__.__name__, pixel_aspect.__class__.__name__)
            )

        if pixel_aspect <= 0:
            raise ValueError(
                "%s.pixel_aspect cannot be zero or a negative value"
                % self.__class__.__name__
            )

        return float(pixel_aspect)

    @validates("print_resolution")
    def _validate_print_resolution(self, key, print_resolution):
        """Validate the print resolution value.

        Args:
            key (str): The name of the validated column.
            print_resolution (Union[int, float]): The print_resolution value to be
                validated.

        Raises:
            TypeError: If the given print_resolution is not an int or float.
            ValueError: If the print_resolution is 0 or negative value.

        Returns:
            float: The validated print_resolution value.
        """
        if not isinstance(print_resolution, (int, float)):
            raise TypeError(
                "%s.print_resolution should be an instance of int or float "
                "not %s"
                % (self.__class__.__name__, print_resolution.__class__.__name__)
            )

        if print_resolution <= 0:
            raise ValueError(
                "%s.print_resolution cannot be zero or negative"
                % self.__class__.__name__
            )

        return float(print_resolution)

    @property
    def device_aspect(self):
        """Return the device aspect.

        Because the device_aspect is calculated from the width/height*pixel
        formula, this property is read-only.

        Returns:
            float: The device aspect ratio.
        """
        return float(self.width) / float(self.height) * self.pixel_aspect

    def __eq__(self, other):
        """Check if other is equal to this ImageFormat.

        Args:
            other (object): The object to check the equality of.

        Returns:
            bool: True if the other is an ImageFormat instance and the width, height and
                pixel_aspect values are all equal.
        """
        return (
            super(ImageFormat, self).__eq__(other)
            and isinstance(other, ImageFormat)
            and self.width == other.width
            and self.height == other.height
            and self.pixel_aspect == other.pixel_aspect
        )

    def __hash__(self):
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(ImageFormat, self).__hash__()
