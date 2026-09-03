# Day 14 - Ultimate: 继承体系终极挑战
# 难度: ⭐⭐⭐⭐⭐
#
# 要求: 设计一个完整的图形渲染系统，综合运用 ABC、Mixin、多继承
# 参考 ultimate_challenge.md

"""
图形渲染系统终极挑战 — 综合运用继承体系的所有知识

设计:
- Shape 抽象基类
- Renderable Mixin (渲染能力)
- Transformable Mixin (变换能力)
- 具体图形类组合多重继承
"""

from abc import ABC, abstractmethod
import math


# ===== Mixin =====

class Renderable:
    """可渲染 Mixin"""

    def render(self) -> str:
        """渲染为 SVG 片段"""
        # TODO: 根据图形类型生成 SVG
        pass

    def render_ascii(self) -> str:
        """渲染为 ASCII 字符画"""
        pass


class Transformable:
    """可变换 Mixin"""

    def translate(self, dx: float, dy: float) -> None:
        """平移"""
        pass

    def scale(self, factor: float) -> None:
        """缩放"""
        pass

    def rotate(self, degrees: float) -> None:
        """旋转"""
        pass


# ===== 基类 =====

class Shape(ABC, Renderable, Transformable):
    """图形基类 — 继承 ABC + 两个 Mixin"""

    @abstractmethod
    def area(self) -> float: ...
    @abstractmethod
    def perimeter(self) -> float: ...
    @abstractmethod
    def centroid(self) -> tuple[float, float]: ...


# ===== 具体图形 =====

class Circle(Shape):
    def __init__(self, cx: float, cy: float, r: float):
        self.cx = cx
        self.cy = cy
        self.r = r

    def area(self) -> float:
        return math.pi * self.r ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.r

    def centroid(self) -> tuple[float, float]:
        return (self.cx, self.cy)


class Rect(Shape):
    def __init__(self, x: float, y: float, w: float, h: float):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def area(self) -> float:
        return self.w * self.h

    def perimeter(self) -> float:
        return 2 * (self.w + self.h)

    def centroid(self) -> tuple[float, float]:
        return (self.x + self.w/2, self.y + self.h/2)


# ===== 渲染管理器 =====

class Renderer:
    """渲染管理器 — 支持批量渲染"""

    def __init__(self):
        self.shapes: list[Shape] = []

    def add(self, shape: Shape) -> None:
        self.shapes.append(shape)

    def render_all(self, fmt: str = "ascii") -> str:
        """渲染所有图形"""
        # TODO: 遍历 shapes，调用 render_ascii 或 render
        pass

    def sort_by_area(self) -> list[Shape]:
        """按面积排序"""
        # TODO: sorted(self.shapes, key=lambda s: s.area())
        pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 图形渲染系统终极挑战 ===")

    renderer = Renderer()
    renderer.add(Circle(0, 0, 5))
    renderer.add(Rect(0, 0, 10, 5))

    for s in renderer.shapes:
        print(f"{type(s).__name__}: area={s.area():.2f}, perimeter={s.perimeter():.2f}")

    print("✅ Ultimate 完成")
