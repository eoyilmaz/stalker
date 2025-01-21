# -*- coding: utf-8 -*-
"""Enum classes are situated here."""

from enum import Enum, IntEnum
from typing import Union

from sqlalchemy import Enum as saEnum, Integer, TypeDecorator


class ScheduleConstraint(IntEnum):
    """The schedule constraint enum."""

    NONE = 0
    Start = 1
    End = 2
    Both = 3

    def __repr__(self) -> str:
        """Return the enum name for str().

        Returns:
            str: The name as the string representation of this
                ScheduleConstraint.
        """
        return self.name if self.name != "NONE" else "None"

    __str__ = __repr__

    @classmethod
    def to_constraint(
        cls, constraint: Union[int, str, "ScheduleConstraint"]
    ) -> "ScheduleConstraint":
        """Validate and return type enum from an input int or str value.

        Args:
            constraint (Union[str, ScheduleConstraint]): Input `constraint` value.

        Raises:
            TypeError: Input value type is invalid.
            ValueError: Input value is invalid.

        Returns:
            ScheduleConstraint: ScheduleConstraint value.
        """
        # Check if it's a valid str type for a constraint.
        if constraint is None:
            constraint = ScheduleConstraint.NONE

        if not isinstance(constraint, (int, str, ScheduleConstraint)):
            raise TypeError(
                "constraint should be a ScheduleConstraint enum value or an "
                "int or a str, "
                f"not {constraint.__class__.__name__}: '{constraint}'"
            )

        if isinstance(constraint, str):
            constraint_name_lut = dict(
                [
                    (c.name.lower(), c.name.title() if c.name != "NONE" else "NONE")
                    for c in cls
                ]
            )
            # also add int values
            constraint_lower_case = constraint.lower()
            if constraint_lower_case not in constraint_name_lut:
                raise ValueError(
                    "constraint should be a ScheduleConstraint enum value or "
                    "one of {}, not '{}'".format(
                        [e.name.title() for e in cls], constraint
                    )
                )

            # Return the enum status for the status value.
            return cls.__members__[constraint_name_lut[constraint_lower_case]]
        else:
            return ScheduleConstraint(constraint)


class ScheduleConstraintDecorator(TypeDecorator):
    """Store ScheduleConstraint as an integer and restore as ScheduleConstraint."""

    impl = Integer

    def process_bind_param(self, value, dialect) -> int:
        """Return the integer value of the ScheduleConstraint.

        Args:
            value (ScheduleConstraint): The ScheduleConstraint value.
            dialect (str): The name of the dialect.

        Returns:
            int: The value of the ScheduleConstraint.
        """
        # just return the value
        return value.value

    def process_result_value(self, value: int, dialect: str) -> ScheduleConstraint:
        """Return a ScheduleConstraint.

        Args:
            value (int): The integer value.
            dialect (str): The name of the dialect.

        Returns:
            ScheduleConstraint: ScheduleConstraint created from the DB data.
        """
        return ScheduleConstraint.to_constraint(value)


class TimeUnit(Enum):
    """The time unit enum."""

    Minute = "min"
    Hour = "h"
    Day = "d"
    Week = "w"
    Month = "m"
    Year = "y"

    def __str__(self) -> str:
        """Return the string representation.

        Returns:
            str: The string representation.
        """
        return str(self.value)

    @classmethod
    def to_unit(cls, unit: Union[str, "TimeUnit"]) -> "TimeUnit":
        """Convert the given unit value to a TimeUnit enum.

        Args:
            unit (Union[str, TimeUnit]): The value to convert to a
                TimeUnit.

        Raises:
            TypeError: Input value type is invalid.
            ValueError: Input value is invalid.

        Returns:
            TimeUnit: The enum.
        """
        if not isinstance(unit, (str, TimeUnit)):
            raise TypeError(
                "unit should be a TimeUnit enum value or one of {}, "
                "not {}: '{}'".format(
                    [u.name.title() for u in cls] + [u.value for u in cls],
                    unit.__class__.__name__,
                    unit,
                )
            )
        if isinstance(unit, str):
            unit_name_lut = dict([(u.name.lower(), u.name) for u in cls])
            unit_name_lut.update(dict([(u.value.lower(), u.name) for u in cls]))
            unit_lower_case = unit.lower()
            if unit_lower_case not in unit_name_lut:
                raise ValueError(
                    "unit should be a TimeUnit enum value or one of {}, "
                    "not '{}'".format(
                        [u.name.title() for u in cls] + [u.value for u in cls], unit
                    )
                )

            return cls.__members__[unit_name_lut[unit_lower_case]]

        return unit


class TimeUnitDecorator(TypeDecorator):
    """Store TimeUnit as an str and restore as TimeUnit."""

    impl = saEnum(*[u.value for u in TimeUnit], name="TimeUnit")

    def process_bind_param(self, value: TimeUnit, dialect: str) -> str:
        """Return the str value of the TimeUnit.

        Args:
            value (TimeUnit): The TimeUnit value.
            dialect (str): The name of the dialect.

        Returns:
            str: The value of the TimeUnit.
        """
        # just return the value
        return value.value

    def process_result_value(self, value: str, dialect: str) -> TimeUnit:
        """Return a TimeUnit.

        Args:
            value (str): The string value to convert to TimeUnit.
            dialect (str): The name of the dialect.

        Returns:
            TimeUnit: The TimeUnit which is created from the DB data.
        """
        return TimeUnit.to_unit(value)


class ScheduleModel(Enum):
    """The schedule model enum."""

    Effort = "effort"
    Duration = "duration"
    Length = "length"

    def __str__(self) -> str:
        """Return the string representation.

        Returns:
            str: The string representation.
        """
        return str(self.value)

    @classmethod
    def to_model(cls, model: Union[str, "ScheduleModel"]) -> "ScheduleModel":
        """Convert the given model value to a ScheduleModel enum.

        Args:
            model (Union[str, ScheduleModel]): The value to convert to a
                ScheduleModel.

        Raises:
            TypeError: Input value type is invalid.
            ValueError: Input value is invalid.

        Returns:
            ScheduleModel: The enum.
        """
        if not isinstance(model, (str, ScheduleModel)):
            raise TypeError(
                "model should be a ScheduleModel enum value or one of {}, "
                "not {}: '{}'".format(
                    [m.name.title() for m in cls] + [m.value for m in cls],
                    model.__class__.__name__,
                    model,
                )
            )
        if isinstance(model, str):
            model_name_lut = dict([(m.name.lower(), m.name) for m in cls])
            model_name_lut.update(dict([(m.value.lower(), m.name) for m in cls]))
            model_lower_case = model.lower()
            if model_lower_case not in model_name_lut:
                raise ValueError(
                    "model should be a ScheduleModel enum value or one of {}, "
                    "not '{}'".format(
                        [m.name.title() for m in cls] + [m.value for m in cls], model
                    )
                )

            return cls.__members__[model_name_lut[model_lower_case]]

        return model


class ScheduleModelDecorator(TypeDecorator):
    """Store ScheduleModel as a str and restore as ScheduleModel."""

    impl = saEnum(*[m.value for m in ScheduleModel], name="ScheduleModel")

    def process_bind_param(self, value, dialect) -> str:
        """Return the str value of the ScheduleModel.

        Args:
            value (ScheduleModel): The ScheduleModel value.
            dialect (str): The name of the dialect.

        Returns:
            str: The value of the ScheduleModel.
        """
        # just return the value
        return value.value

    def process_result_value(self, value: str, dialect: str) -> ScheduleModel:
        """Return a ScheduleModel.

        Args:
            value (str): The string value to convert to ScheduleModel.
            dialect (str): The name of the dialect.

        Returns:
            ScheduleModel: The ScheduleModel created from the DB data.
        """
        return ScheduleModel.to_model(value)


class DependencyTarget(Enum):
    """The dependency target enum."""

    OnStart = "onstart"
    OnEnd = "onend"

    def __str__(self) -> str:
        """Return the string representation.

        Returns:
            str: The string representation.
        """
        return str(self.value)

    @classmethod
    def to_target(cls, target: Union[str, "DependencyTarget"]) -> "DependencyTarget":
        """Convert the given target value to a DependencyTarget enum.

        Args:
            target (Union[str, DependencyTarget]): The value to convert to a
                DependencyTarget.

        Raises:
            TypeError: Input value type is invalid.
            ValueError: Input value is invalid.

        Returns:
            DependencyTarget: The enum.
        """
        if not isinstance(target, (str, DependencyTarget)):
            raise TypeError(
                "target should be a DependencyTarget enum value or one of {}, "
                "not {}: '{}'".format(
                    [t.name for t in cls] + [t.value for t in cls],
                    target.__class__.__name__,
                    target,
                )
            )
        if isinstance(target, str):
            target_name_lut = dict([(t.name.lower(), t.name) for t in cls])
            target_name_lut.update(dict([(t.value.lower(), t.name) for t in cls]))
            target_lower_case = target.lower()
            if target_lower_case not in target_name_lut:
                raise ValueError(
                    "target should be a DependencyTarget enum value or one of {}, "
                    "not '{}'".format(
                        [t.name for t in cls] + [t.value for t in cls], target
                    )
                )

            return cls.__members__[target_name_lut[target_lower_case]]

        return target


class DependencyTargetDecorator(TypeDecorator):
    """Store DependencyTarget as an enum and restore as DependencyTarget."""

    impl = saEnum(*[m.value for m in DependencyTarget], name="TaskDependencyTarget")

    def process_bind_param(self, value, dialect) -> str:
        """Return the str value of the DependencyTarget.

        Args:
            value (DependencyTarget): The DependencyTarget value.
            dialect (str): The name of the dialect.

        Returns:
            str: The value of the DependencyTarget.
        """
        # just return the value
        return value.value

    def process_result_value(self, value: str, dialect: str) -> DependencyTarget:
        """Return a DependencyTarget.

        Args:
            value (str): The string value to convert to DependencyTarget.
            dialect (str): The name of the dialect.

        Returns:
            DependencyTarget: The DependencyTarget created from str.
        """
        return DependencyTarget.to_target(value)


class TraversalDirection(IntEnum):
    """The traversal direction enum."""

    DepthFirst = 0
    BreadthFirst = 1

    def __repr__(self) -> str:
        """Return the enum name for str().

        Returns:
            str: The name as the string representation of this
                ScheduleConstraint.
        """
        return self.name if self.name != "NONE" else "None"

    __str__ = __repr__

    @classmethod
    def to_direction(
        cls, direction: Union[int, str, "TraversalDirection"]
    ) -> "TraversalDirection":
        """Convert the given direction value to a TraversalDirection enum.

        Args:
            direction (Union[int, str, TraversalDirection]): The value to
                convert to a TraversalDirection.

        Raises:
            TypeError: Input value type is invalid.
            ValueError: Input value is invalid.

        Returns:
            TraversalDirection: The enum.
        """
        if not isinstance(direction, (int, str, TraversalDirection)):
            raise TypeError(
                "direction should be a TraversalDirection enum value "
                "or one of {}, not {}: '{}'".format(
                    [d.name for d in cls] + [d.value for d in cls],
                    direction.__class__.__name__,
                    direction,
                )
            )
        if isinstance(direction, str):
            direction_name_lut = dict([(d.name.lower(), d.name) for d in cls])
            direction_name_lut.update(dict([(d.value, d.name) for d in cls]))
            direction_lower_case = direction.lower()
            if direction_lower_case not in direction_name_lut:
                raise ValueError(
                    "direction should be a TraversalDirection enum value or "
                    "one of {}, not '{}'".format(
                        [d.name for d in cls] + [d.value for d in cls],
                        direction,
                    )
                )

            return cls.__members__[direction_name_lut[direction_lower_case]]

        return direction
