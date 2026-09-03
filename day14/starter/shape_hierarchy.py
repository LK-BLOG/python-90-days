"""
Day 14 - OOP深入② 继承体系
===============================
练习：用 ABC 抽象基类构建 Shape 继承体系

要求：
- Shape 作为抽象基类，定义 area/perimeter 抽象方法
- Circle、Rectangle 继承并实现具体逻辑
- 理解抽象方法强制子类实现的机制

运行本文件测试你的实现是否正确。
"""

from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """图形抽象基类

    所有图形都必须实现 area() 和 perimeter()。

    属性:
        name (str): 图形名称
        color (str): 颜色
    """

    def __init__(self, name, color='black'):
        self.name = name
        self.color = color

    @abstractmethod
    def area(self) -> float:
        """计算面积

        TODO: 子类必须实现
        """
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """计算周长

        TODO: 子类必须实现
        """
        pass

    def describe(self) -> str:
        """返回图形描述（已实现）"""
        return (
            f'{self.name} [{self.color}] -- '
            f'面积={self.area():.2f}, 周长={self.perimeter():.2f}'
        )

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name!r}, color={self.color!r})'


class Circle(Shape):
    """圆形

    Args:
        radius (float): 半径

    TODO: 实现 area() 和 perimeter()
        - area = pi * r^2
        - perimeter = 2 * pi * r
    """

    def __init__(self, radius, color='red'):
        super().__init__(name='Circle', color=color)
        if radius <= 0:
            raise ValueError('半径必须大于 0')
        self.radius = radius

    def area(self) -> float:
        # TODO: 返回面积
        pass

    def perimeter(self) -> float:
        # TODO: 返回周长
        pass


class Rectangle(Shape):
    """矩形

    Args:
        width (float): 宽度
        height (float): 高度

    TODO: 实现 area() 和 perimeter()
        - area = width * height
        - perimeter = 2 * (width + height)

    额外挑战: 实现 is_square() 判断是否为正方形
    """

    def __init__(self, width, height, color='blue'):
        super().__init__(name='Rectangle', color=color)
        if width <= 0 or height <= 0:
            raise ValueError('宽高必须大于 0')
        self.width = width
        self.height = height

    def area(self) -> float:
        # TODO: 返回面积
        pass

    def perimeter(self) -> float:
        # TODO: 返回周长
        pass

    def is_square(self) -> bool:
        # TODO: 判断是否为正方形
        pass


# ==================== 测试 ====================
if __name__ == '__main__':
    print('=' * 50)
    print('Day 14 练习: Shape 继承体系')
    print('=' * 50)

    shapes = [
        Circle(5, color='red'),
        Rectangle(4, 6, color='blue'),
        Rectangle(5, 5, color='green'),
    ]

    for s in shapes:
        print(s.describe())

    c = Circle(5)
    assert abs(c.area() - 78.5398) < 0.01, f'Circle area wrong: {c.area()}'
    assert abs(c.perimeter() - 31.4159) < 0.01, f'Circle perimeter wrong: {c.perimeter()}'

    r = Rectangle(4, 6)
    assert r.area() == 24
    assert r.perimeter() == 20

    sq = Rectangle(5, 5)
    assert sq.is_square() == True

    print('OK -- 所有测试通过!')
