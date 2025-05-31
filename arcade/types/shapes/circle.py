from __future__ import annotations

import math
from typing import Any, NamedTuple, TypedDict

from pyglet.math import Vec2

from arcade.types.numbers import AsFloat
from arcade.types.vector_like import AnchorPoint, Point2

CircleParams = tuple[AsFloat, AsFloat, AsFloat]

class CircleKwargs(TypedDict):
    x: float
    y: float
    diameter: float
    radius: float
    left: float
    right: float
    bottom: float
    top: float

class Circle(NamedTuple):
    x: float
    y: float
    diameter: float
    radius: float
    left: float
    right: float
    bottom: float
    top: float

    @property
    def width(self) -> float:
        """It's an alias for `Circle.diameter`. What did you think? It's a circle."""
        return self.diameter

    @property
    def height(self) -> float:
        """It's an alias for `Circle.diameter`. What did you think? It's a circle."""
        return self.diameter

    @property
    def center(self) -> Vec2:
        """Returns a :py:class:`~pyglet.math.Vec2` representing the center of the circle."""
        return Vec2(self.x, self.y)

    @property
    def bottom_left(self) -> Vec2:
        """
        Returns a :py:class:`~pyglet.math.Vec2` representing the
        bottom-left of the square that circumscribes the circle.
        """
        return Vec2(self.left, self.bottom)

    @property
    def bottom_right(self) -> Vec2:
        """
        Returns a :py:class:`~pyglet.math.Vec2` representing the
        bottom-right of the square that circumscribes the circle.
        """
        return Vec2(self.right, self.bottom)

    @property
    def top_left(self) -> Vec2:
        """
        Returns a :py:class:`~pyglet.math.Vec2` representing the
        top-left of the square that circumscribes the circle.
        """
        return Vec2(self.left, self.top)

    @property
    def top_right(self) -> Vec2:
        """
        Returns a :py:class:`~pyglet.math.Vec2` representing the
        top-right of the square that circumscribes the circle.
        """
        return Vec2(self.right, self.top)

    @property
    def bottom_center(self) -> Vec2:
        """
        Returns a :py:class:`~pyglet.math.Vec2` representing the
        bottom-center of the circle.
        """
        return Vec2(self.x, self.bottom)

    @property
    def center_right(self) -> Vec2:
        """
        Returns a :py:class:`~pyglet.math.Vec2` representing the
        center-right of the circle.
        """
        return Vec2(self.right, self.y)

    @property
    def top_center(self) -> Vec2:
        """
        Returns a :py:class:`~pyglet.math.Vec2` representing the
        top-center of the circle.
        """
        return Vec2(self.x, self.top)

    @property
    def center_left(self) -> Vec2:
        """Returns a :py:class:`~pyglet.math.Vec2` representing the center-left of the circle."""
        return Vec2(self.left, self.y)

    @property
    def area(self) -> float:
        """The area of the circle in square pixels."""
        return math.pi * (self.radius ** 2)

    def at_position(self, position: Point2) -> Circle:
        """Returns a new :py:class:`Circle` which is moved to put `position` at its center."""
        x, y = position
        return XYR(x, y, self.radius)

    def move(self, dx: AsFloat = 0.0, dy: AsFloat = 0.0) -> Circle:
        """
        Returns a new :py:class:`Circle` which is moved by `dx` in the
        x-direction and `dy` in the y-direction.
        """
        return XYR(self.x + dx, self.y + dy, self.radius)

    def point_in_circle(self, point: Point2) -> bool:
        """Returns ``True`` if ``point`` is inside this circle.

        Args:
            point: A tuple of :py:class:`int` or :py:class:`float` values.
        """
        px, py = point
        dx = px - self.x
        dy = py - self.y
        distance_squared = dx * dx + dy * dy
        return distance_squared <= self.radius ** 2

    def point_in_bounds(self, point: Point2) -> bool:
        """Returns ``True`` if ``point`` is inside this circle excluding the boundaries.

        Args:
            point: A tuple of :py:class:`int` or :py:class:`float` values.
        """
        px, py = point
        dx = px - self.x
        dy = py - self.y
        distance_squared = dx * dx + dy * dy
        return distance_squared <= self.radius ** 2

    def __contains__(self, point: Point2 | Any) -> bool:
        """Shorthand for :py:meth:`rect.point_in_rect(point) <point_in_rect>`.

        Args:
            point: A tuple of :py:class:`int` or :py:class:`float` values.
        """
        from arcade.utils import is_iterable

        if not is_iterable(point):
            return False

        return self.point_in_circle(point)

    @property
    def xyr(self) -> CircleParams:
        """Provides a tuple in the format (x, y, radius)."""
        return (self.x, self.y, self.radius)

    @property
    def xyd(self) -> CircleParams:
        """Provides a tuple in the format (x, y, diameter)."""
        return (self.x, self.y, self.diameter)

    @property
    def lbr(self) -> CircleParams:
        """Provides a tuple in the format (left, bottom, radius)."""
        return (self.left, self.bottom, self.radius)

    @property
    def lbd(self) -> CircleParams:
        """Provides a tuple in the format (left, bottom, diameter)."""
        return (self.left, self.bottom, self.diameter)


def XYR(x: AsFloat, y: AsFloat, radius: AsFloat) -> Circle:
    return Circle(
        x,
        y,
        radius * 2,
        radius,
        x - radius,
        x + radius,
        y - radius,
        y + radius
    )

def XYD(x: AsFloat, y: AsFloat, diameter: AsFloat) -> Circle:
    radius = diameter / 2
    return Circle(
        x,
        y,
        diameter,
        radius,
        x - radius,
        x + radius,
        y - radius,
        y + radius
    )

def LBR(left: AsFloat, bottom: AsFloat, radius: AsFloat) -> Circle:
    x = left + radius
    y = bottom + radius
    return Circle(
        x,
        y,
        radius * 2,
        radius,
        left,
        x + radius,
        bottom,
        y + radius
    )

def LBD(left: AsFloat, bottom: AsFloat, diameter: AsFloat) -> Circle:
    radius = diameter / 2
    x = left + radius
    y = bottom + radius
    return Circle(
        x,
        y,
        diameter,
        radius,
        left,
        x + radius,
        bottom,
        y + radius
    )
