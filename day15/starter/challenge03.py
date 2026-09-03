# Day 15 - Challenge 3: 缓存描述符
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 实现自动缓存计算结果的描述符
# 参考 challenge.md

"""
缓存描述符挑战 — 自动缓存昂贵计算的结果

核心知识点:
- 缓存描述符
- 缓存失效策略
- 与 property 的对比
"""

import time
from typing import Callable, Any


class CachedProperty:
    """缓存属性描述符

    首次访问时计算并缓存，后续直接返回缓存值。

    支持缓存失效:
        - 手动失效: del obj.attr
        - TTL 失效: 指定过期时间
    """

    def __init__(self, func: Callable = None, ttl: float = None):
        """
        Args:
            func: 计算函数
            ttl: 缓存过期时间（秒），None 表示永不过期
        """
        # TODO: 存储 func, ttl
        self.func = func
        self.ttl = ttl
        self.name = None
        self.attr_name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.attr_name = f"_cached_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # TODO: 检查缓存是否存在且未过期
        # 过期或不存在则重新计算
        pass

    def __delete__(self, obj):
        """手动清除缓存"""
        # TODO: 从 obj.__dict__ 删除缓存
        pass


class ExpensiveCalculation:
    """演示类 — 有多个昂贵计算属性"""

    def __init__(self, data: list[int]):
        self.data = data

    @CachedProperty
    def sorted_data(self) -> list[int]:
        """排序后的数据（首次计算后缓存）"""
        print("  [计算 sorted_data...]")
        time.sleep(0.1)  # 模拟耗时
        return sorted(self.data)

    @CachedProperty(ttl=5.0)
    def statistics(self) -> dict:
        """统计数据（带 TTL 缓存）"""
        print("  [计算 statistics...]")
        time.sleep(0.1)
        n = len(self.data)
        s = sum(self.data)
        return {
            "count": n,
            "sum": s,
            "avg": s / n if n else 0,
            "min": min(self.data) if n else 0,
            "max": max(self.data) if n else 0,
        }

    @CachedProperty
    def total(self) -> int:
        """总和"""
        print("  [计算 total...]")
        return sum(self.data)


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 缓存描述符测试 ===")

    calc = ExpensiveCalculation([5, 3, 1, 4, 2])

    print("第一次访问 sorted_data:")
    print(f"  结果: {calc.sorted_data}")

    print("第二次访问（应该用缓存）:")
    print(f"  结果: {calc.sorted_data}")

    print("访问 statistics:")
    print(f"  结果: {calc.statistics}")

    # 手动清除缓存
    print("清除 sorted_data 缓存...")
    del calc.sorted_data
    print("重新访问:")
    print(f"  结果: {calc.sorted_data}")

    print("✅ Challenge 03 完成")
