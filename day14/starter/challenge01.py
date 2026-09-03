# Day 14 - Challenge 1: 图形继承链
# 难度: ⭐⭐⭐☆☆
#
# 要求: 用 ABC 设计 Shape 继承体系
# 参考 challenge.md

"""
图形继承链挑战 — 用抽象基类 (ABC) 设计几何图形体系

核心知识点:
- ABC 和 @abstractmethod
- 抽象方法 vs 具体方法
- __eq__ 比较逻辑
"""

from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """图形抽象基类

    所有图形必须实现 area() 和 perimeter() 方法。
    """

    def __init__(self, color: str = "black"):
        # TODO: 设置颜色属性
        pass

    @abstractmethod
    def area(self) -> float:
        """计算面积（抽象方法）"""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """计算周长（抽象方法）"""
        pass

    def describe(self) -> str:
        """描述图形信息（具体方法，子类继承即可）"""
        return (f"{type(self).__name__}(color={self.color!r}) "
                f"area={self.area():.2f} perimeter={self.perimeter():.2f}")

    def __eq__(self, other) -> bool:
        """按面积比较两个图形是否相等"""
        if not isinstance(other, Shape):
            return NotImplemented
        return abs(self.area() - other.area()) < 1e-9

    def __lt__(self, other) -> bool:
        """按面积比较大小"""
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area() < other.area()

    def __repr__(self) -> str:
        return self.describe()


class Circle(Shape):
    """圆形"""

    def __init__(self, radius: float, color: str = "black"):
        # TODO: 调用父类 __init__，设置 radius（非负检查）
        pass

    def area(self) -> float:
        """π * r²"""
        # TODO: 实现
        pass

    def perimeter(self) -> float:
        """2 * π * r"""
        # TODO: 实现
        pass

    def __repr__(self) -> str:
        return f"Circle(radius={self.radius}, color={self.color!r})"


class Rectangle(Shape):
    """矩形"""

    def __init__(self, width: float, height: float, color: str = "black"):
        # TODO: 设置 width, height（正数检查）
        pass

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def is_square(self) -> bool:
        """是否为正方形"""
        # TODO: width == height
        pass

    def __repr__(self) -> str:
        return f"Rectangle({self.width}x{self.height}, color={self.color!r})"


class Triangle(Shape):
    """三角形"""

    def __init__(self, a: float, b: float, c: float, color: str = "black"):
        """三条边

        Args:
            a, b, c: 三边长度

        Raises:
            ValueError: 无法构成三角形
        """
        # TODO: 验证三角形不等式 (任意两边之和 > 第三边)
        pass

    def area(self) -> float:
        """海伦公式"""
        # TODO: s = (a+b+c)/2, area = sqrt(s(s-a)(s-b)(s-c))
        pass

    def perimeter(self) -> float:
        return self.a + self.b + self.c

    def is_right(self) -> bool:
        """是否为直角三角形"""
        # TODO: 检查 a²+b²=c²（排序后检查）
        pass

    def __repr__(self) -> str:
        return f"Triangle({self.a},{self.b},{self.c})"


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 图形继承链测试 ===")

    c = Circle(5)
    r = Rectangle(4, 6)
    t = Triangle(3, 4, 5)

    for s in [c, r, t]:
        print(s.describe())

    print(f"圆形 == 矩形? {c == r}")
    print(f"矩形是正方形? {r.is_square()}")
    print(f"三角形是直角? {t.is_right()}")

    print("✅ Challenge 01 完成")
