"""Rects all act the same, but take four of the possible eight attributes and calculate the rest."""

from __future__ import annotations

from typing import NamedTuple, Optional
from pyglet.math import Vec2
from arcade.types import AsFloat


class AnchorPoint:
    BOTTOM_LEFT = Vec2(0.0, 0.0)
    BOTTOM_CENTER = Vec2(0.5, 0.0)
    BOTTOM_RIGHT = Vec2(1.0, 0.0)
    CENTER_LEFT = Vec2(0.0, 0.5)
    CENTER = Vec2(0.5, 0.5)
    CENTER_RIGHT = Vec2(1.0, 0.5)
    TOP_LEFT = Vec2(0.0, 1.0)
    TOP_CENTER = Vec2(0.5, 1.0)
    TOP_RIGHT = Vec2(1.0, 1.0)


class Rect(NamedTuple):
    """Rects define a rectangle, with several convenience properties and functions.

    This object is immutable by design. It provides no setters, and is a NamedTuple subclass.

    Attempts to implement all Rectangle functions used in the library, with the notable exception
    of `.scale()`, as that function was ill-defined and assumed a bottom-left anchor point, something
    that should be accounted for if `.scale()` is to be reimplemented.

    Rectangles cannot rotate by design, since this complicates their implmentation a lot."""
    left: float
    right: float
    bottom: float
    top: float
    width: float
    height: float
    x: float
    y: float

    @property
    def center_x(self) -> float:
        """Backwards-compatible alias."""
        return self.x

    @property
    def center_y(self) -> float:
        """Backwards-compatible alias."""
        return self.y

    @property
    def center(self) -> Vec2:
        return Vec2(self.x, self.y)

    @property
    def bottom_left(self) -> Vec2:
        return Vec2(self.left, self.bottom)

    @property
    def position(self) -> Vec2:
        """Backwards-compatible alias."""
        return self.bottom_left

    @property
    def bottom_right(self) -> Vec2:
        return Vec2(self.right, self.bottom)

    @property
    def top_left(self) -> Vec2:
        return Vec2(self.left, self.top)

    @property
    def top_right(self) -> Vec2:
        return Vec2(self.right, self.top)

    @property
    def bottom_center(self) -> Vec2:
        return Vec2(self.x, self.bottom)

    @property
    def right_center(self) -> Vec2:
        return Vec2(self.right, self.y)

    @property
    def top_center(self) -> Vec2:
        return Vec2(self.x, self.top)

    @property
    def left_center(self) -> Vec2:
        return Vec2(self.left, self.y)

    @property
    def size(self) -> Vec2:
        return Vec2(self.width, self.height)

    def at_position(self, position: Vec2) -> Rect:
        """Returns new Rect which is moved to put `position` at it's center."""
        return XYWH(position.x, position.y, self.width, self.height)

    def move(self, dx: AsFloat = 0.0, dy: AsFloat = 0.0) -> Rect:
        """Returns new Rect which is moved by `dx` and `dy`."""
        return XYWH(self.x + dx, self.y + dy, self.width, self.height)

    def resize(self, new_size: Vec2, anchor: Vec2 = AnchorPoint.CENTER) -> Rect:
        anchor_x = self.left + anchor.x * self.width
        anchor_y = self.bottom + anchor.y * self.height

        ratio_x = new_size.x / self.width
        ratio_y = new_size.y / self.height

        adjusted_left = anchor_x + (self.left - anchor_x) * ratio_x
        adjusted_right = anchor_x + (self.right - anchor_x) * ratio_x
        adjusted_top = anchor_y + (self.top - anchor_y) * ratio_y
        adjusted_bottom = anchor_y + (self.bottom - anchor_y) * ratio_y

        return LRBT(adjusted_left, adjusted_right, adjusted_top, adjusted_bottom)

    def scale(self, new_scale: float, anchor: Vec2 = AnchorPoint.CENTER) -> Rect:
        anchor_x = self.left + anchor.x * self.width
        anchor_y = self.bottom + anchor.y * self.height

        adjusted_left = anchor_x + (self.left - anchor_x) * new_scale
        adjusted_right = anchor_x + (self.right - anchor_x) * new_scale
        adjusted_top = anchor_y + (self.top - anchor_y) * new_scale
        adjusted_bottom = anchor_y + (self.bottom - anchor_y) * new_scale

        return LRBT(adjusted_left, adjusted_right, adjusted_top, adjusted_bottom)

    def align_top(self, value: AsFloat) -> Rect:
        """Returns new Rect, which is aligned to the top."""
        diff_y = value - self.top
        return self.move(dy=diff_y)

    def align_bottom(self, value: AsFloat) -> Rect:
        """Returns new Rect, which is aligned to the bottom."""
        diff_y = value - self.bottom
        return self.move(dy=diff_y)

    def align_left(self, value: AsFloat) -> Rect:
        """Returns new Rect, which is aligned to the left."""
        diff_x = value - self.left
        return self.move(dx=diff_x)

    def align_right(self, value: AsFloat) -> Rect:
        """Returns new Rect, which is aligned to the right."""
        diff_x = value - self.right
        return self.move(dx=diff_x)

    def align_center(self, value: Vec2) -> Rect:
        """Returns new Rect, which is aligned to the center x and y."""
        diff_x = value.x - self.center_x
        diff_y = value.y - self.center_y
        return self.move(dx=diff_x, dy=diff_y)

    def align_center_x(self, value: AsFloat) -> Rect:
        """Returns new Rect, which is aligned to the center_x."""
        diff_x = value - self.center_x
        return self.move(dx=diff_x)

    def align_center_y(self, value: AsFloat) -> Rect:
        """Returns new Rect, which is aligned to the center_y."""
        diff_y = value - self.center_y
        return self.move(dy=diff_y)

    def min_size(
            self,
            width: Optional[AsFloat] = None,
            height: Optional[AsFloat] = None
    ) -> Rect:
        """
        Sets the size to at least the given min values.
        """
        left = self.left
        bottom = self.bottom
        width = max(width or 0.0, self.width)
        height = max(height or 0.0, self.height)
        return LBWH(left, bottom, width, height)

    def max_size(
            self,
            width: Optional[AsFloat] = None,
            height: Optional[AsFloat] = None
    ) -> Rect:
        """
        Limits the size to the given max values.
        """
        left = self.left
        bottom = self.bottom
        width = min(width or float("inf"), self.width)
        height = min(height or float("inf"), self.height)
        return LBWH(left, bottom, width, height)

    def union(self, other: Rect) -> Rect:
        """
        Returns a new Rect that is the union of this rect and another.
        The union is the smallest rectangle that contains these two rectangles.
        """
        left = min(self.left, other.left)
        right = max(self.right, other.right)
        bottom = min(self.bottom, other.bottom)
        top = max(self.top, other.top)
        return LRBT(left, right, bottom, top)

    def __or__(self, other: Rect) -> Rect:
        return self.union(other)

    def overlaps(self, other: Rect) -> bool:
        u = self | other
        return u.width > 0 or u.height > 0

    def intersect(self, other: Rect) -> Rect | None:
        """
        Returns a new Rect that is the overlaping portion of this Rect and another.
        This will return None if no such rectangle exists.
        """
        intersecting = self.collides(other)
        if not intersecting:
            return None
        left = max(self.left, other.left)
        right = min(self.right, other.right)
        bottom = max(self.bottom, other.bottom)
        top = min(self.top, other.top)
        return LRBT(left, right, bottom, top)

    def collides(self, other: Rect) -> bool:
        return (self.right >= other.left and other.right >= self.left) and \
            (self.top >= other.bottom and other.top >= self.bottom)

    def __and__(self, other: Rect) -> Rect | None:
        return self.intersect(other)

    def point_in_rect(self, point: Vec2) -> bool:
        return (self.left < point.x < self.right) and (self.bottom < point.y < self.top)

    def to_points(self) -> tuple[Vec2, Vec2, Vec2, Vec2]:
        return (
            Vec2(self.left, self.bottom),
            Vec2(self.left, self.top),
            Vec2(self.right, self.top),
            Vec2(self.right, self.bottom)
        )

    def to_tuple(self) -> tuple[float, ...]:
        """Returns the bare tuple used to create this Rect."""
        return self.__class__.from_rect(self)

    # Subclass-only methods
    @staticmethod
    def from_rect(rect: Rect) -> tuple[float, ...]:
        return (rect.left, rect.right, rect.top, rect.bottom,
                rect.width, rect.height, rect.x, rect.y)

    @staticmethod
    def as_new_attrs(*args: tuple[AsFloat]) -> tuple[AsFloat, ...]:
        """Takes an incomplete signature and returns all attributes needed to create a new Rect."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return (f"<Rect LRBT({self.left}, {self.right}, {self.bottom}, {self.top})"
                f" XYWH({self.x}, {self.y}, {self.width}, {self.height})>")

    def __str__(self) -> str:
        repr(self)


class LRBT(Rect):
    def __new__(cls, left: AsFloat, right: AsFloat, bottom: AsFloat, top: AsFloat) -> Rect:
        rect = cls.as_new_attrs(left, right, bottom, top)
        return Rect.__new__(cls, *rect)

    def __init__(self, left: AsFloat, right: AsFloat, bottom: AsFloat, top: AsFloat):
        ...

    @staticmethod
    def from_rect(rect: Rect) -> tuple[float, float, float, float]:
        return (rect.left, rect.right, rect.bottom, rect.top)

    @staticmethod
    def as_new_attrs(left: AsFloat, right: AsFloat, bottom: AsFloat, top: AsFloat) -> tuple[AsFloat, ...]:
        width = right - left
        height = top - bottom
        x = left + (width / 2)
        y = bottom + (height / 2)
        return (left, right, bottom, top, width, height, x, y)


class LBWH(Rect):
    def __new__(cls, left: AsFloat, bottom: AsFloat, width: AsFloat, height: AsFloat) -> Rect:
        rect = cls.as_new_attrs(left, bottom, width, height)
        return Rect.__new__(cls, *rect)

    def __init__(self, left: AsFloat, bottom: AsFloat, width: AsFloat, height: AsFloat):
        ...

    @staticmethod
    def from_rect(rect: Rect) -> tuple[float, float, float, float]:
        return (rect.left, rect.bottom, rect.width, rect.height)

    @staticmethod
    def as_new_attrs(left: AsFloat, bottom: AsFloat, width: AsFloat, height: AsFloat) -> tuple[AsFloat, ...]:
        right = left + width
        top = bottom + height
        x = left + (width / 2)
        y = bottom + (height / 2)
        return (left, right, bottom, top, width, height, x, y)


class XYWH(Rect):
    def __new__(cls, x: AsFloat, y: AsFloat, width: AsFloat, height: AsFloat) -> Rect:
        rect = cls.to_rect_attrs(x, y, width, height)
        return Rect.__new__(cls, *rect)

    def __init__(self, x: AsFloat, y: AsFloat, width: AsFloat, height: AsFloat):
        ...

    @staticmethod
    def from_rect(rect: Rect) -> tuple[float, float, float, float]:
        return (rect.x, rect.y, rect.width, rect.height)

    @staticmethod
    def to_rect_attrs(x: AsFloat, y: AsFloat, width: AsFloat, height: AsFloat) -> tuple[AsFloat, ...]:
        left = x - (width / 2)
        right = x + (width / 2)
        bottom = y - (width / 2)
        top = y + (width / 2)
        return (left, right, bottom, top, width, height, x, y)


class XYRR(Rect):
    def __new__(cls, x: AsFloat, y: AsFloat, half_width: AsFloat, half_height: AsFloat) -> Rect:
        rect = cls.to_rect_attrs(x, y, half_width, half_height)
        return Rect.__new__(cls, *rect)

    def __init__(self, x: AsFloat, y: AsFloat, half_width: AsFloat, half_height: AsFloat):
        ...

    @staticmethod
    def from_rect(rect: Rect) -> tuple[float, float, float, float]:
        return (rect.x, rect.y, rect.width / 2, rect.height / 2)

    @staticmethod
    def to_rect_attrs(x: AsFloat, y: AsFloat, half_width: AsFloat, half_height: AsFloat) -> tuple[AsFloat, ...]:
        left = x - half_width
        right = x + half_width
        bottom = y - half_width
        top = y + half_width
        return (left, right, bottom, top, half_width * 2, half_height * 2, x, y)


class Viewport(Rect):
    def __new__(cls, x: int, y: int, width: int, height: int):
        rect = cls.to_rect_attrs(x, y, width, height)
        return Rect.__new__(cls, *rect)

    def __init__(self, x: int, y: int, width: int, height: int):
        ...

    @staticmethod
    def from_rect(rect: Rect) -> tuple[int, int, int, int]:
        return (int(rect.x), int(rect.y), int(rect.width), int(rect.height))

    @staticmethod
    def to_rect_attrs(x: int, y: int, width: int, height: int) -> tuple[AsFloat, ...]:
        left = x - (width / 2)
        right = x + (width / 2)
        bottom = y - (width / 2)
        top = y + (width / 2)
        return (left, right, bottom, top, width, height, x, y)


# Make a LRBT
r = LRBT(10, 20, 10, 20)

print(type(r))  # <class '__main__.LRBT'>
assert r.left == 10
assert r.right == 20
assert r.bottom == 10
assert r.top == 20
assert r.center == Vec2(15, 15)
assert r.size == Vec2(10, 10)

# Make sure we can construct bare tuples
assert LRBT.from_rect(r) == (10, 20, 10, 20)

s = LRBT(10, 15, 10, 15)
s = s.move(2, 3)
LRBT.from_rect(s)  # (12, 17, 13, 18)
