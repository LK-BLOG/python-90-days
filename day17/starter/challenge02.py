# Day 17 - Challenge 2: frozen 数据
# 难度: ⭐⭐⭐☆☆
#
# 要求: 创建不可变的数据类
# 参考 challenge.md

"""
frozen 数据挑战 — 创建不可变的、可哈希的数据类

核心知识点:
- frozen=True
- __hash__ 自动生成
- 不可变对象的优势
"""

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True, order=True)
class Point:
    """不可变二维点 — frozen=True

    - 不能修改属性
    - 自动生成 __hash__
    - order=True 自动生成比较方法
    """

    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        """到另一点的距离"""
        # TODO: 计算欧几里得距离
        pass

    def manhattan_distance(self, other: "Point") -> float:
        """曼哈顿距离"""
        return abs(self.x - other.x) + abs(self.y - other.y)

    def midpoint(self, other: "Point") -> "Point":
        """中点"""
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)


@dataclass(frozen=True)
class Color:
    """不可变颜色"""

    r: int = 0
    g: int = 0
    b: int = 0

    def __post_init__(self):
        # frozen=True 下需要用 object.__setattr__ 来修改
        # 或者直接在 __init_subclass__ 中校验
        for val in (self.r, self.g, self.b):
            if not 0 <= val <= 255:
                raise ValueError(f"RGB 值必须在 0-255 之间")

    def blend(self, other: "Color", ratio: float = 0.5) -> "Color":
        """混合两种颜色"""
        # TODO: 线性插值
        pass

    def to_hex(self) -> str:
        """转为十六进制"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    @classmethod
    def from_hex(cls, hex_str: str) -> "Color":
        """从十六进制创建"""
        # TODO: 解析 #rrggbb
        pass


@dataclass(frozen=True)
class Config:
    """不可变配置对象"""

    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    tags: Tuple[str, ...] = ()  # 用 tuple 而非 list（因为 frozen）

    def replace(self, **kwargs) -> "Config":
        """创建修改后的新实例（因为原对象不可变）

        Returns:
            修改后的新 Config

        Example:
            new_cfg = cfg.replace(port=9090, debug=True)
        """
        # TODO: dataclasses.replace(self, **kwargs)
        pass


# ---- 测试 ----
if __name__ == "__main__":
    print("=== frozen dataclass 测试 ===")

    p1 = Point(1, 2)
    p2 = Point(4, 6)
    print(f"距离: {p1.distance_to(p2):.2f}")
    print(f"中点: {p1.midpoint(p2)}")
    print(f"hash: {hash(p1)}")

    # 可以放入 set
    points = {p1, p2, Point(1, 2)}  # Point(1,2) 与 p1 重复
    print(f"去重后数量: {len(points)}")  # 2

    c1 = Color(255, 128, 0)
    c2 = Color(0, 128, 255)
    print(f"混合: {c1.blend(c2).to_hex()}")

    cfg = Config(port=9090)
    cfg2 = cfg.replace(debug=True)
    print(f"原配置: {cfg}")
    print(f"新配置: {cfg2}")

    print("✅ Challenge 02 完成")
