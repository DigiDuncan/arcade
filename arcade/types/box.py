"""
Box is a stub named tuples which acts as the 3D partner to arcade.Box
"""

from __future__ import annotations

from typing import NamedTuple, TypedDict

from pyglet.math import Vec3

from arcade.types.numbers import AsFloat
from arcade.types.rect import LBWH, Rect
from arcade.types.vector_like import Point3


class BoxKwargs(TypedDict):
    """Annotates a plain :py:class:`dict` of :py:class:`Box` arguments.

    This is only meaningful as a type annotation during type checking.
    For example, the :py:meth:`Box.kwargs <arcade.types.Box.kwargs>`
    property returns an ordinary will actually be a :py:class:`dict`
    of :py:class:`Box` field names to :py:class:`float` values.

    To learn more, please see:

    * :py:class:`.Box`
    * :py:class:`typing.TypedDict`

    """

    left: float
    right: float
    bottom: float
    top: float
    near: float
    far: float
    width: float
    height: float
    depth: float
    x: float
    y: float
    z: float


class Box(NamedTuple):
    """A 3D box, with several convenience properties and functions.

    This object is immutable by design. It provides no setters, and is a NamedTuple
    subclass.

    Boxes cannot rotate by design, since this complicates their implementation
    a lot.

    You probably don't want to create one of these directly, and should instead use
    a helper method, like :py:func:`.LBWH`, :py:func:`.LRBT`, :py:func:`.XYWH`, or
    :py:func:`.Viewport`.

    You can also use :py:meth:`.from_kwargs` to create a Box from keyword arguments.
    """

    left: float
    right: float

    bottom: float
    top: float

    near: float
    far: float

    width: float
    height: float
    depth: float

    x: float
    y: float
    z: float

    @property
    def center_x(self) -> float:
        """Backwards-compatible alias for :py:attr:`.x`."""
        return self.x

    @property
    def center_y(self) -> float:
        """Backwards-compatible alias for :py:attr:`.y`."""
        return self.y

    @property
    def center_z(self) -> float:
        """Backwards-compatible alias for :py:attr:`.z`."""
        return self.z

    @property
    def center(self) -> Vec3:
        """Returns a :py:class:`~pyglet.math.Vec3` representing the center of the box."""
        return Vec3(self.x, self.y, self.z)

    @property
    def bottom_left_near(self) -> Vec3:
        """
        Returns a :py:class:`~pyglet.math.Vec3` representing the
        bottom-left-near corner of the box.
        """
        return Vec3(self.left, self.bottom, self.near)

    @property
    def bottom_left_far(self) -> Vec3:
        """
        Returns a :py:class:`~pyglet.math.Vec3` representing the
        bottom-left-far corner of the box.
        """
        return Vec3(self.left, self.bottom, self.far)

    @property
    def bottom_right_near(self) -> Vec3:
        """
        Returns a :py:class:`~pyglet.math.Vec3` representing the
        bottom-right-near corner of the box.
        """
        return Vec3(self.right, self.bottom, self.near)

    @property
    def bottom_right_far(self) -> Vec3:
        """
        Returns a :py:class:`~pyglet.math.Vec3` representing the
        bottom-right-far corner of the box.
        """
        return Vec3(self.right, self.bottom, self.far)

    @property
    def top_left_near(self) -> Vec3:
        """
        Returns a :py:class:`~pyglet.math.Vec3` representing the
        top-left-near corner of the box.
        """
        return Vec3(self.left, self.top, self.near)

    @property
    def top_left_far(self) -> Vec3:
        """
        Returns a :py:class:`~pyglet.math.Vec3` representing the
        top-left-far corner of the box.
        """
        return Vec3(self.left, self.top, self.far)

    @property
    def top_right_near(self) -> Vec3:
        """
        Returns a :py:class:`~pyglet.math.Vec3` representing the
        top-right-near corner of the box.
        """
        return Vec3(self.right, self.top, self.near)

    @property
    def top_right_far(self) -> Vec3:
        """
        Returns a :py:class:`~pyglet.math.Vec3` representing the
        top-right-far corner of the box.
        """
        return Vec3(self.right, self.top, self.far)

    @property
    def near_face(self) -> Rect:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        near face of the box.
        """
        return LBWH(self.left, self.bottom, self.width, self.height)

    @property
    def far_face(self) -> Rect:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        far face of the box.
        """
        return LBWH(self.left, self.bottom, self.width, self.height)

    @property
    def left_face(self) -> Rect:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        left face of the box.
        """
        return LBWH(self.near, self.bottom, self.depth, self.height)

    @property
    def right_face(self) -> Rect:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        right face of the box.
        """
        return LBWH(self.near, self.bottom, self.depth, self.height)

    @property
    def top_face(self) -> Rect:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        top face of the box.
        """
        return LBWH(self.left, self.near, self.width, self.depth)

    @property
    def bottom_face(self) -> Rect:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        bottom face of the box.
        """
        return LBWH(self.left, self.near, self.width, self.depth)

    @property
    def near_face_center(self) -> Vec3:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        center of the near face of the box.
        """
        return Vec3(self.x, self.y, self.near)

    @property
    def far_face_center(self) -> Vec3:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        center of the far face of the box.
        """
        return Vec3(self.x, self.y, self.far)

    @property
    def left_face_center(self) -> Vec3:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        center of the left face of the box.
        """
        return Vec3(self.left, self.y, self.z)

    @property
    def right_face_center(self) -> Vec3:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        center of the right face of the box.
        """
        return Vec3(self.right, self.y, self.z)

    @property
    def top_face_center(self) -> Vec3:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        center of the top face of the box.
        """
        return Vec3(self.x, self.top, self.z)

    @property
    def bottom_face_center(self) -> Vec3:
        """
        Returns a :py:class:`~arcade.Rect` representing the
        center of the bottom face of the box.
        """
        return Vec3(self.x, self.top, self.z)

    @property
    def size(self) -> Vec3:
        """Returns a :py:class:`~pyglet.math.Vec3` representing the size of the box."""
        return Vec3(self.width, self.height, self.depth)

    @property
    def volume(self) -> float:
        """The volume of the box in cubic pixels."""
        return self.width * self.height * self.depth

    def at_position(self, position: Point3) -> Box:
        """Returns a new :py:class:`Box` which is moved to put `position` at its center."""
        x, y, z = position
        return XYZWHD(x, y, z, self.width, self.height, self.depth)

    def move(self, dx: AsFloat = 0.0, dy: AsFloat = 0.0, dz: AsFloat = 0.0) -> Box:
        """
        Returns a new :py:class:`Box` which is moved by `dx` in the
        x-direction,`dy` in the y-direction, and `dz` in the z-direction.
        """
        return XYZWHD(self.x + dx, self.y + dy, self.z + dz, self.width, self.height, self.depth)

    def union(self, other: Box) -> Box:
        """Get the smallest Box encapsulating both this one and ``other``."""
        left = min(self.left, other.left)
        right = max(self.right, other.right)
        bottom = min(self.bottom, other.bottom)
        top = max(self.top, other.top)
        near = min(self.near, other.near)
        far = max(self.far, other.far)
        return LRBTNF(left, right, bottom, top, near, far)

    def __or__(self, other: Box) -> Box:
        """Shorthand for :py:meth:`rect.union(other) <union>`.

        Args:
            other: Another :py:class:`Box` instance.
        """
        return self.union(other)

    def intersection(self, other: Box) -> Box | None:
        """Return a :py:class:`Box` of the overlap if any exists.

        If the two :py:class:`Box` instances do not intersect, this
        method will return ``None`` instead.

        Args:
            other: Another :py:class:`Box` instance.
        """
        intersecting = self.overlaps(other)
        if not intersecting:
            return None
        left = max(self.left, other.left)
        right = min(self.right, other.right)
        bottom = max(self.bottom, other.bottom)
        top = min(self.top, other.top)
        near = max(self.near, other.near)
        far = min(self.far, other.far)
        return LRBTNF(left, right, bottom, top, near, far)

    def overlaps(self, other: Box) -> bool:
        """Returns ``True`` if `other` overlaps with ``self``.

        Args:
            other: Another :py:class:`Box` instance.
        """

        return (
            (other.width + self.width) / 2.0 > abs(self.x - other.x)
            and (other.height + self.height) / 2.0 > abs(self.y - other.y)
            and (other.depth + self.depth) / 2.0 > abs(self.z - other.z)
        )

    def __and__(self, other: Box) -> Box | None:
        """Shorthand for :py:meth:`Box.intersection(other) <interesection>`.

        Args:
            other: Another :py:class:`Box` instance.
        """
        return self.intersection(other)

    def point_in_box(self, point: Point3) -> bool:
        x, y, z = point
        return (
            (self.left <= x <= self.right)
            and (self.bottom <= y <= self.top)
            and (self.near <= z <= self.far)
        )

    def __contains__(self, point: Point3) -> bool:
        """Shorthand for :py:meth:`Box.point_in_box(point) <point_in_box>`.

        Args:
            point: A tuple of :py:class:`int` or :py:class:`float` values.
        """
        return self.point_in_box(point)

    def to_points(self) -> tuple[Vec3, Vec3, Vec3, Vec3, Vec3, Vec3, Vec3, Vec3]:
        """Return a new :py:class:`tuple` of this rectangle's corner points.

        The points will be ordered as follows:

        #. :py:meth:`bottom_left_near`
        #. :py:meth:`top_left_near`
        #. :py:meth:`top_right_near`
        #. :py:meth:`bottom_right_near`
        #. :py:meth:`bottom_left_far`
        #. :py:meth:`top_left_far`
        #. :py:meth:`top_right_far`
        #. :py:meth:`bottom_right_far`

        """
        left = self.left
        bottom = self.bottom
        right = self.right
        top = self.top
        near = self.near
        far = self.far
        return (
            Vec3(left, bottom, near),
            Vec3(left, top, near),
            Vec3(right, top, near),
            Vec3(right, bottom, near),
            Vec3(left, bottom, far),
            Vec3(left, top, far),
            Vec3(right, top, far),
            Vec3(right, bottom, far),
        )

    def __str__(self) -> str:
        return (
            f"<{self.__class__.__name__} LRBTNT({self.left}, {self.right}, {self.bottom}, {self.top},"
            f"{self.near}, {self.far})"
            f" XYZWHD({self.x}, {self.y}, {self.z} {self.width}, {self.height}, {self.depth})>"
        )

    def __bool__(self) -> bool:
        """Returns True if volume is not 0, else False."""
        return self.width != 0 and self.height != 0 and self.depth != 0


def XYZWHD(x: float, y: float, z: float, width: float, height: float, depth: float) -> Box:
    h_width = width / 2
    h_height = height / 2
    h_depth = depth / 2
    return Box(
        x - h_width,
        x + h_width,
        y - h_height,
        y + h_height,
        z - h_depth,
        z + h_depth,
        width,
        height,
        depth,
        x,
        y,
        z,
    )


def LRBTNF(left: float, right: float, bottom: float, top: float, near: float, far: float) -> Box:
    width = right - left
    height = top - bottom
    depth = far - near

    return Box(
        left,
        right,
        bottom,
        top,
        near,
        far,
        width,
        height,
        depth,
        left + width / 2.0,
        bottom + height / 2.0,
        near + depth / 2.0,
    )
