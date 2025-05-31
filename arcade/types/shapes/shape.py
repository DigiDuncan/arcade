from typing import Protocol
from pyglet.math import Vec2, Vec3
from arcade.types.numbers import AsFloat

class Shape2D(Protocol):
    x: AsFloat
    y: AsFloat
    left: AsFloat
    right: AsFloat
    top: AsFloat
    bottom: AsFloat
    width: AsFloat
    height: AsFloat

    # These will usually be properties but the type checker hates us
    center: Vec2
    top_left: Vec2
    top_right: Vec2
    bottom_left: Vec2
    bottom_right: Vec2
    size: Vec2

    def __contains__(self, point: Vec2) -> bool: ...
    def to_points(self) -> tuple[Vec2, ...]: ...
    def from_kwargs(self, **kwargs: AsFloat): ...

    kwargs: dict[str, AsFloat]

class Shape3D(Protocol):
    x: AsFloat
    y: AsFloat
    z: AsFloat
    left: AsFloat
    right: AsFloat
    top: AsFloat
    bottom: AsFloat
    near: AsFloat
    far: AsFloat
    width: AsFloat
    height: AsFloat
    depth: AsFloat

    # These will usually be properties but the type checker hates us
    center: Vec3
    bottom_left_near: Vec3
    bottom_left_far: Vec3
    bottom_right_near: Vec3
    bottom_right_far: Vec3
    top_left_near: Vec3
    top_left_far: Vec3
    top_right_near: Vec3
    top_right_far: Vec3
    size: Vec3

    def __contains__(self, point: Vec3) -> bool: ...
    def to_points(self) -> tuple[Vec3, ...]: ...
    def from_kwargs(self, **kwargs: AsFloat): ...

    kwargs: dict[str, AsFloat]

Shape = Shape2D | Shape3D
