# Day 16 - Challenge 2: 分数比较器
# 难度: ⭐⭐⭐☆☆
#
# 要求: 实现富比较运算符
# 参考 challenge.md

"""
分数比较器挑战 — 实现所有富比较运算符

核心知识点:
- __lt__, __le__, __gt__, __ge__, __eq__, __ne__
- functools.total_ordering 装饰器
- 分数运算
"""

from math import gcd
from functools import total_ordering


@total_ordering  # 只需实现 __eq__ 和 __lt__，自动补全其余比较
class Fraction:
    """分数类 — 完整的比较和运算支持

    Attributes:
        numerator: 分子
        denominator: 分母（始终 > 0，负号在分子上）
    """

    def __init__(self, numerator: int, denominator: int = 1):
        """初始化分数

        Args:
            numerator: 分子
            denominator: 分母（不能为0）

        Raises:
            ZeroDivisionError: 分母为0
        """
        # TODO:
        # 1. 检查分母不为0
        # 2. 约分（用 gcd）
        # 3. 负号统一在分子上
        pass

    def __eq__(self, other) -> bool:
        """相等比较"""
        if not isinstance(other, Fraction):
            return NotImplemented
        # TODO: 比较 numerator 和 denominator
        pass

    def __lt__(self, other: "Fraction") -> bool:
        """小于比较"""
        if not isinstance(other, Fraction):
            return NotImplemented
        # TODO: 通分后比较分子
        pass

    def __add__(self, other: "Fraction") -> "Fraction":
        """加法: a/b + c/d = (ad + bc) / bd"""
        # TODO: 实现分数加法
        pass

    def __sub__(self, other: "Fraction") -> "Fraction":
        """减法"""
        # TODO
        pass

    def __mul__(self, other: "Fraction") -> "Fraction":
        """乘法: a/b * c/d = ac/bd"""
        # TODO
        pass

    def __truediv__(self, other: "Fraction") -> "Fraction":
        """除法: a/b / c/d = ad/bc"""
        # TODO
        pass

    def __neg__(self) -> "Fraction":
        """取负"""
        return Fraction(-self.numerator, self.denominator)

    @property
    def float_value(self) -> float:
        """转为浮点数"""
        return self.numerator / self.denominator

    def __repr__(self) -> str:
        return f"Fraction({self.numerator}, {self.denominator})"

    def __str__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"

    def __format__(self, format_spec: str) -> str:
        if format_spec == "f":
            return f"{self.float_value:.2f}"
        return str(self)


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 分数比较器测试 ===")

    f1 = Fraction(1, 2)
    f2 = Fraction(3, 4)
    f3 = Fraction(2, 4)

    print(f"f1 = {f1}")
    print(f"f2 = {f2}")
    print(f"f1 == f3: {f1 == f3}")  # True (1/2 == 2/4)
    print(f"f1 < f2: {f1 < f2}")
    print(f"f1 + f2 = {f1 + f2}")  # 5/4
    print(f"f1 * f2 = {f1 * f2}")  # 3/8
    print(f"f1 - f2 = {f1 - f2}")  # -1/4
    print(f"f2 / f1 = {f2 / f1}")  # 3/2
    print(f"float(f1) = {f1.float_value}")
    print(f"format(f1, 'f') = {f1:f}")

    print("✅ Challenge 02 完成")
