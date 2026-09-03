# Day 16 - Challenge 5: 运算符重载
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 实现向量类的算术运算
# 参考 challenge.md

"""
运算符重载挑战 — 实现一个完整的向量类

支持所有算术运算和一元运算。
"""

import math
from typing import Union


class Vector:
    """二维向量类 — 完整的运算符重载

    支持:
        +, -, *, /, @ (点积), ** (幂)
        abs(), len(), bool()
        ==, !=, <, <=, >, >= (按模长)
        repr, str, format
    """

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    # ===== 算术运算 =====

    def __add__(self, other: Union["Vector", int, float]) -> "Vector":
        """向量加法"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        if isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        return NotImplemented

    def __sub__(self, other: Union["Vector", int, float]) -> "Vector":
        """向量减法"""
        # TODO: 实现
        pass

    def __mul__(self, scalar: Union[int, float]) -> "Vector":
        """标量乘法"""
        # TODO: 返回 Vector(self.x * scalar, self.y * scalar)
        pass

    def __rmul__(self, scalar) -> "Vector":
        """反向标量乘法 (5 * v)"""
        # TODO: return self * scalar
        pass

    def __truediv__(self, scalar: Union[int, float]) -> "Vector":
        """标量除法"""
        # TODO
        pass

    def __matmul__(self, other: "Vector") -> float:
        """点积 (v1 @ v2)"""
        # TODO: return self.x * other.x + self.y * other.y
        pass

    def __pow__(self, power: int) -> float:
        """向量的模的幂次 (v ** 2 = |v|²)"""
        # TODO: return self.magnitude ** power
        pass

    # ===== 一元运算 =====

    def __neg__(self) -> "Vector":
        """取反"""
        return Vector(-self.x, -self.y)

    def __abs__(self) -> float:
        """模长"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __bool__(self) -> bool:
        """非零向量为 True"""
        return self.x != 0 or self.y != 0

    # ===== 比较运算（按模长） =====

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return math.isclose(abs(self), abs(other), rel_tol=1e-9)

    def __lt__(self, other: "Vector") -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return abs(self) < abs(other)

    # ===== 属性 =====

    @property
    def magnitude(self) -> float:
        """模长"""
        return abs(self)

    @property
    def normalized(self) -> "Vector":
        """单位向量"""
        mag = self.magnitude
        if mag == 0:
            return Vector(0, 0)
        return self / mag

    def dot(self, other: "Vector") -> float:
        """点积"""
        return self @ other

    def cross(self, other: "Vector") -> float:
        """叉积 (2D 返回标量)"""
        return self.x * other.y - self.y * other.x

    def angle_with(self, other: "Vector") -> float:
        """与另一向量的夹角（弧度）"""
        cos_theta = (self @ other) / (self.magnitude * other.magnitude)
        return math.acos(max(-1, min(1, cos_theta)))

    # ===== 字符串表示 =====

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __format__(self, format_spec: str) -> str:
        if format_spec == "p":
            # 极坐标格式: (r, θ°)
            pass
        if format_spec == "":
            return f"({self.x:.2f}, {self.y:.2f})"
        return f"({self.x:{format_spec}}, {self.y:{format_spec}})"


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 运算符重载测试 ===")

    v1 = Vector(3, 4)
    v2 = Vector(1, 2)

    print(f"v1 = {v1}, v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 2 = {v1 * 2}")
    print(f"3 * v2 = {3 * v2}")
    print(f"v1 / 2 = {v1 / 2}")
    print(f"v1 @ v2 = {v1 @ v2}")  # 点积 = 11
    print(f"|v1| = {abs(v1)}")     # 5.0
    print(f"v1 ** 2 = {v1 ** 2}")  # 25.0
    print(f"v1 magnitude: {v1.magnitude}")
    print(f"v1 normalized: {v1.normalized}")
    print(f"v1 angle with v2: {math.degrees(v1.angle_with(v2)):.1f}°")

    print("✅ Challenge 05 完成")
