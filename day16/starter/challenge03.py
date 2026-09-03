# Day 16 - Challenge 3: 自定义容器
# 难度: ⭐⭐⭐⭐☆
#
# 要求: 实现 __len__, __getitem__, __contains__, __iter__
# 参考 challenge.md

"""
自定义容器挑战 — 让你的类表现得像内置容器

核心知识点:
- __len__: len() 支持
- __getitem__: 索引和切片
- __contains__: in 运算符
- __iter__: for 循环迭代
"""

from typing import Any, Iterator


class SortedList:
    """有序列表 — 插入后自动排序的容器

    支持所有容器协议方法。
    """

    def __init__(self, items: list = None):
        self._data: list = sorted(items) if items else []

    def add(self, item: Any) -> None:
        """添加元素并保持排序"""
        # TODO: 二分查找插入位置 -> insert
        # 提示: 用 bisect 模块或手动二分
        pass

    def remove(self, item: Any) -> bool:
        """移除元素"""
        # TODO: 查找 -> 删除 -> 返回是否成功
        pass

    def __len__(self) -> int:
        """支持 len()"""
        return len(self._data)

    def __getitem__(self, index):
        """支持索引和切片

        Args:
            index: int 索引或 slice 对象

        Returns:
            单个元素或新的 SortedList

        Raises:
            IndexError: 索引越界
        """
        # TODO: 支持 sl[0], sl[1:3] 等操作
        # 切片时返回新的 SortedList
        pass

    def __setitem__(self, index, value):
        """支持赋值 sl[0] = 5"""
        # TODO: 注意赋值后需要重新排序
        pass

    def __delitem__(self, index):
        """支持 del sl[0]"""
        # TODO: 删除元素
        pass

    def __contains__(self, item) -> bool:
        """支持 in 运算符"""
        # TODO: 可以用二分查找提升效率
        return item in self._data

    def __iter__(self) -> Iterator:
        """支持 for 循环"""
        return iter(self._data)

    def __reversed__(self) -> Iterator:
        """支持 reversed()"""
        return reversed(self._data)

    def __bool__(self) -> bool:
        """支持 bool() 和 if 判断"""
        return len(self._data) > 0

    def __repr__(self) -> str:
        return f"SortedList({self._data})"

    def __eq__(self, other) -> bool:
        if isinstance(other, SortedList):
            return self._data == other._data
        if isinstance(other, list):
            return self._data == sorted(other)
        return NotImplemented


# ---- 测试 ----
if __name__ == "__main__":
    print("=== 自定义容器测试 ===")

    sl = SortedList([5, 3, 1, 4, 2])
    print(f"初始: {sl}")  # [1, 2, 3, 4, 5]
    print(f"长度: {len(sl)}")

    sl.add(3)
    print(f"添加3: {sl}")  # [1, 2, 3, 3, 4, 5]

    print(f"索引: sl[2] = {sl[2]}")
    print(f"切片: sl[1:4] = {sl[1:4]}")

    print(f"3 in sl: {3 in sl}")
    print(f"6 in sl: {6 in sl}")

    for item in sl:
        print(f"  遍历: {item}")

    print(f"反转: {list(reversed(sl))}")
    print(f"bool(空): {bool(SortedList())}")

    print("✅ Challenge 03 完成")
