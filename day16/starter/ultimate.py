# Day 16 - Ultimate: 魔术方法终极挑战
# 难度: ⭐⭐⭐⭐⭐
#
# 要求: 设计一个支持所有魔术方法的数学表达式类
# 参考 ultimate_challenge.md

"""
魔术方法终极挑战 — 设计一个表达式类，支持运算符链式组合

目标: 实现 Expression 类，可以链式构建数学表达式
"""

from __future__ import annotations
from typing import Union
import math


class Expression:
    """数学表达式类 — 支持运算符重载的表达式树

    Example:
        x = Expression.var("x")
        expr = (x + 3) * (x - 1)
        expr.evaluate(x=2)  # (2+3)*(2-1) = 5
        expr.to_string()     # "(x + 3) * (x - 1)"
    """

    def __init__(self, op: str = "", *children):
        self.op = op
        self.children = list(children)
        self.value = None  # 常量值

    @classmethod
    def const(cls, value: float) -> "Expression":
        """创建常量表达式"""
        expr = cls()
        expr.value = value
        return expr

    @classmethod
    def var(cls, name: str) -> "Expression":
        """创建变量表达式"""
        expr = cls()
        expr.op = name
        return expr

    def __add__(self, other) -> "Expression":
        other = other if isinstance(other, Expression) else Expression.const(other)
        return Expression("+", self, other)

    def __sub__(self, other) -> "Expression":
        other = other if isinstance(other, Expression) else Expression.const(other)
        return Expression("-", self, other)

    def __mul__(self, other) -> "Expression":
        other = other if isinstance(other, Expression) else Expression.const(other)
        return Expression("*", self, other)

    def __truediv__(self, other) -> "Expression":
        other = other if isinstance(other, Expression) else Expression.const(other)
        return Expression("/", self, other)

    def __neg__(self) -> "Expression":
        return Expression("-", Expression.const(0), self)

    def evaluate(self, **variables) -> float:
        """求值"""
        # TODO: 递归求值
        if self.value is not None:
            return self.value
        # 变量
        if self.op in variables:
            return variables[self.op]
        # 运算
        left = self.children[0].evaluate(**variables)
        right = self.children[1].evaluate(**variables)
        ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
               "*": lambda a, b: a * b, "/": lambda a, b: a / b}
        return ops[self.op](left, right)

    def to_string(self) -> str:
        """转为可读字符串"""
        if self.value is not None:
            return str(self.value)
        if not self.children:
            return self.op
        left = self.children[0].to_string()
        right = self.children[1].to_string()
        return f"({left} {self.op} {right})"

    def __repr__(self) -> str:
        return self.to_string()

    def __str__(self) -> str:
        return self.to_string()


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 魔术方法终极挑战 ===")

    x = Expression.var("x")
    expr = (x + 3) * (x - 1)
    print(f"表达式: {expr}")
    print(f"evaluate(x=2): {expr.evaluate(x=2)}")
    print(f"evaluate(x=5): {expr.evaluate(x=5)}")

    expr2 = (x ** 2) if hasattr(x, '__pow__') else (x * x)
    print(f"x²: {expr2.to_string()}")

    print("✅ Ultimate 完成")
