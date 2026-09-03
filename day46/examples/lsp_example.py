\"\"\"里氏替换原则示例\"\"\"

from abc import ABC, abstractmethod
from typing import Protocol


# ===== 违反LSP =====
class RectangleBad:
    def __init__(self, width: float = 0, height: float = 0):
        self._width = width
        self._height = height

    @property
    def width(self): return self._width

    @width.setter
    def width(self, value): self._width = value

    @property
    def height(self): return self._height

    @height.setter
    def height(self, value): self._height = value

    def area(self) -> float:
        return self._width * self._height


class SquareBad(RectangleBad):
    \"\"\"正方形强行继承长方形 → 违反LSP\"\"\"

    @RectangleBad.width.setter
    def width(self, value):
        self._width = value
        self._height = value

    @RectangleBad.height.setter
    def height(self, value):
        self._width = value
        self._height = value


# ===== 遵循LSP =====
class Shape(Protocol):
    def area(self) -> float: ...
    def describe(self) -> str: ...


class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def describe(self) -> str:
        return f\"Rectangle({self.width}x{self.height})\"

    def __repr__(self):
        return self.describe()


class Square:
    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return self.side ** 2

    def describe(self) -> str:
        return f\"Square({self.side})\"

    def __repr__(self):
        return self.describe()


class Circle:
    import math

    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return Circle.math.pi * self.radius ** 2

    def describe(self) -> str:
        return f\"Circle(r={self.radius})\"


def total_area(shapes: list[Shape]) -> float:
    \"\"\"任何Shape都能正常工作\"\"\"
    return sum(s.area() for s in shapes)


if __name__ == \"__main__\":
    shapes = [Rectangle(5, 4), Square(5), Circle(3)]
    for s in shapes:
        print(f\"{s}: area={s.area():.2f}\")
    print(f\"Total: {total_area(shapes):.2f}\")
