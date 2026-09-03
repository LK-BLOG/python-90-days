# Day 14 - Challenge 3: Mixin 工具箱
# 难度: ⭐⭐⭐☆☆
#
# 要求: 实现 JsonMixin, HashMixin, CloneMixin
# 参考 challenge.md

"""
Mixin 工具箱挑战 — 用 Mixin 为类注入通用功能

Mixin 设计原则:
- 单一职责
- 不依赖 __init__ 调用顺序
- 不使用实例属性（除非明确声明）
"""

import json
import copy
from typing import Any


class JsonMixin:
    """JSON 序列化 Mixin

    继承此类的类自动获得 to_json / from_json 方法。
    """

    def to_json(self, indent: int = 2) -> str:
        """将对象序列化为 JSON 字符串

        Returns:
            JSON 格式字符串

        Example:
            >>> class Person(JsonMixin):
            ...     def __init__(self, name, age):
            ...         self.name, self.age = name, age
            >>> Person("Alice", 25).to_json()
            '{"name": "Alice", "age": 25}'
        """
        # TODO: self.__dict__ -> json.dumps
        pass

    @classmethod
    def from_json(cls, json_str: str) -> "JsonMixin":
        """从 JSON 字符串反序列化

        Args:
            json_str: JSON 字符串

        Returns:
            类的实例
        """
        # TODO: json.loads -> cls(**data)
        pass

    def to_dict(self) -> dict:
        """转为字典"""
        # TODO: 返回 self.__dict__ 的深拷贝
        pass

    @classmethod
    def from_dict(cls, data: dict) -> "JsonMixin":
        """从字典创建实例"""
        return cls(**data)


class HashMixin:
    """自动哈希 Mixin

    根据指定属性自动生成 __hash__ 和 __eq__。
    """

    _hash_fields: tuple = ()  # 子类指定用于哈希的属性名

    def __hash__(self) -> int:
        """自动生成哈希值

        依赖子类定义 _hash_fields = ("field1", "field2")
        """
        if not self._hash_fields:
            raise NotImplementedError(
                f"{type(self).__name__} 必须定义 _hash_fields"
            )
        # TODO: tuple(getattr(self, f) for f in self._hash_fields) -> hash
        pass

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return hash(self) == hash(other)


class CloneMixin:
    """深拷贝 Mixin"""

    def clone(self) -> "CloneMixin":
        """创建对象的深拷贝

        Returns:
            独立副本
        """
        # TODO: copy.deepcopy(self)
        pass

    def shallow_clone(self) -> "CloneMixin":
        """浅拷贝"""
        # TODO: copy.copy(self)
        pass


# ===== 使用示例 =====
class Point(JsonMixin, HashMixin, CloneMixin):
    """二维点 — 同时使用三个 Mixin"""

    _hash_fields = ("x", "y")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, other: "Point") -> float:
        """到另一点的距离"""
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


# ---- 测试 ----
if __name__ == "__main__":
    print("=== Mixin 工具箱测试 ===")

    p1 = Point(3, 4)
    p2 = Point(3, 4)

    # JsonMixin
    json_str = p1.to_json()
    print(f"JSON: {json_str}")
    p3 = Point.from_json(json_str)
    print(f"反序列化: {p3}")

    # HashMixin
    print(f"hash(p1) == hash(p2): {hash(p1) == hash(p2)}")
    print(f"p1 == p2: {p1 == p2}")
    print(f"距离: {p1.distance_to(Point(0, 0))}")

    # CloneMixin
    p4 = p1.clone()
    p4.x = 999
    print(f"原始: {p1}, 克隆: {p4}")

    print("✅ Challenge 03 完成")
