# Day 14 - Challenge 4: 接口检查系统
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 用 ABC 和 Protocol 实现鸭子类型检查
# 参考 challenge.md

"""
接口检查系统挑战 — 学习两种接口定义方式

- ABC: 非结构化子类型（必须显式继承）
- Protocol: 结构化子类型（只要有相同方法即可）
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


# ===== 方式一: ABC 非结构化接口 =====

class Drawable(ABC):
    """可绘制接口（ABC 版）"""

    @abstractmethod
    def draw(self) -> str:
        """绘制对象，返回描述字符串"""
        pass

    @abstractmethod
    def bounding_box(self) -> tuple[float, float, float, float]:
        """返回边界框 (x, y, width, height)"""
        pass

    def draw_with_border(self) -> str:
        """带边框的绘制（具体方法）"""
        return f"[{self.draw()}]"


# ===== 方式二: Protocol 结构化接口 =====

@runtime_checkable
class Serializable(Protocol):
    """可序列化协议 — 无需继承，只要有对应方法即可"""

    def to_dict(self) -> dict:
        """转为字典"""
        ...

    def from_dict(cls, data: dict) -> "Serializable":
        """从字典恢复"""
        ...


@runtime_checkable
class Comparable(Protocol):
    """可比较协议"""

    def __lt__(self, other) -> bool:
        ...

    def __eq__(self, other) -> bool:
        ...


# ===== 实现类 =====

class Circle(Drawable):
    """圆形 — 实现 Drawable"""

    def __init__(self, x: float, y: float, radius: float):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self) -> str:
        return f"Circle(center=({self.x},{self.y}), r={self.radius})"

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (self.x - self.radius, self.y - self.radius,
                self.radius * 2, self.radius * 2)


class Square(Drawable):
    """正方形 — 实现 Drawable"""

    def __init__(self, x: float, y: float, size: float):
        self.x = x
        self.y = y
        self.size = size

    def draw(self) -> str:
        return f"Square(pos=({self.x},{self.y}), size={self.size})"

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.size, self.size)


# 鸭子类型：不需要继承 Serializable，只要有 to_dict/from_dict 即可
class PointDuck:
    """鸭子类型 — 不继承 Serializable 但满足协议"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, data: dict) -> "PointDuck":
        return cls(**data)


# ===== 接口检查工具 =====

def check_interface(obj, interface) -> tuple[bool, list[str]]:
    """检查对象是否满足接口

    Args:
        obj: 要检查的对象
        interface: ABC 类或 Protocol

    Returns:
        (是否满足, 缺失的方法列表)
    """
    missing = []
    # TODO: 获取接口要求的所有抽象方法
    # 检查 obj 是否有这些方法
    pass


def enforce_interface(obj, interface) -> None:
    """强制类型检查

    Raises:
        TypeError: 不满足接口时抛出
    """
    # TODO: 调用 check_interface -> 不满足则 raise TypeError
    pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 接口检查系统测试 ===")

    c = Circle(0, 0, 5)
    s = Square(10, 10, 3)

    # ABC 检查
    for shape in [c, s]:
        print(shape.draw_with_border())
        print(f"  bbox: {shape.bounding_box()}")

    # Protocol 检查
    duck = PointDuck(1, 2)
    print(f"duck 是 Serializable? {isinstance(duck, Serializable)}")
    print(f"duck 是 Comparable? {isinstance(duck, Comparable)}")

    # 接口验证
    ok, missing = check_interface(c, Drawable)
    print(f"Circle 满足 Drawable? {ok} (missing: {missing})")

    print("✅ Challenge 04 完成")
