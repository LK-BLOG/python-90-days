"""
Day 16 - 魔术方法
===============================
练习：实现 Vector 类，覆盖常用魔术方法

要求：
- 支持算术运算 (__add__, __mul__, __neg__)
- 支持索引和切片 (__getitem__, __setitem__)
- 支持比较 (__eq__, __lt__)
- 支持字符串表示 (__repr__, __str__, __format__)
- 支持 len() / bool()

运行本文件测试你的实现是否正确。
"""

import math


class Vector:
    """N维向量

    支持的操作:
        v1 + v2          向量加法
        v1 * scalar      标量乘法
        v1 == v2         相等比较
        v1 < v2          按模比较
        v[0], v[1:3]     索引与切片
        len(v)           维度
        abs(v)           模（长度）
        repr(v) / str(v) 字符串表示
    """

    def __init__(self, *components):
        """初始化向量

        Args:
            *components: 各维度分量，如 Vector(1, 2, 3)

        TODO: 将分量存入元组（不可变）
        """
        # TODO: self._components = tuple(components)
        pass

    # ==================== 属性 ====================

    @property
    def dimensions(self) -> int:
        """向量维度"""
        # TODO: 返回维度数
        pass

    @property
    def magnitude(self) -> float:
        """向量的模（长度）"""
        # TODO: sqrt(sum(x^2 for x in components))
        pass

    # ==================== 算术运算 ====================

    def __add__(self, other):
        """向量加法

        TODO: 逐分量相加，维度不同抛 ValueError
        """
        pass

    def __sub__(self, other):
        """向量减法

        TODO: 逐分量相减
        """
        pass

    def __mul__(self, scalar):
        """标量乘法

        TODO: 每个分量乘以 scalar
        """
        pass

    def __rmul__(self, scalar):
        """反向标量乘法 (3 * v)"""
        # TODO: return self * scalar
        pass

    def __neg__(self):
        """取反 (-v)

        TODO: 每个分量取负
        """
        pass

    def __abs__(self) -> float:
        """abs(v) 返回模"""
        # TODO: return self.magnitude
        pass

    # ==================== 索引与切片 ====================

    def __getitem__(self, index):
        """支持 v[0], v[1:3] 等操作

        TODO: 支持整数索引和切片
        """
        pass

    def __setitem__(self, index, value):
        """支持 v[0] = 5

        TODO: 由于向量不可变，抛出 TypeError
        """
        pass

    # ==================== 比较 ====================

    def __eq__(self, other) -> bool:
        """v1 == v2  逐分量比较"""
        # TODO:
        pass

    def __lt__(self, other) -> bool:
        """v1 < v2  按模比较"""
        # TODO:
        pass

    def __le__(self, other) -> bool:
        return self == other or self < other

    # ==================== 表示 ====================

    def __len__(self) -> int:
        """len(v) 返回维度"""
        # TODO:
        pass

    def __bool__(self) -> bool:
        """非零向量为 True，零向量为 False"""
        # TODO:
        pass

    def __repr__(self) -> str:
        """开发者友好的表示: Vector(1, 2, 3)"""
        # TODO:
        pass

    def __str__(self) -> str:
        """用户友好的表示: (1, 2, 3)"""
        # TODO:
        pass

    def __format__(self, fmt) -> str:
        """支持 format(v, '.2f')"""
        # TODO: 格式化每个分量
        pass

    # ==================== 工具方法 ====================

    def dot(self, other) -> float:
        """点积"""
        # TODO: sum(a*b for a, b in zip(self, other))
        pass

    def normalize(self):
        """返回单位向量"""
        # TODO: self / abs(self)，零向量抛 ZeroDivisionError
        pass

    def to_tuple(self) -> tuple:
        return tuple(self._components) if hasattr(self, '_components') else ()


# ==================== 测试 ====================
if __name__ == '__main__':
    print('=' * 50)
    print('Day 16 练习: Vector 魔术方法')
    print('=' * 50)

    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)

    print(f'v1 = {v1}')
    print(f'v2 = {v2}')
    print(f'v1 + v2 = {v1 + v2}')
    print(f'v1 * 3 = {v1 * 3}')
    print(f'3 * v2 = {3 * v2}')
    print(f'|v1| = {abs(v1):.4f}')
    print(f'v1[0] = {v1[0]}')
    print(f'v1[1:] = {v1[1:]}')
    print(f'len(v1) = {len(v1)}')

    assert v1 + v2 == Vector(5, 7, 9), '加法错误'
    assert v1 * 3 == Vector(3, 6, 9), '乘法错误'
    assert v1[0] == 1 and v1[2] == 3, '索引错误'
    assert len(v1) == 3, '维度错误'
    assert abs(v1 - Vector(0, 0, 0)) == 0, '零向量错误'

    print('OK -- 所有测试通过!')
