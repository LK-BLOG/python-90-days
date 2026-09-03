# Day 25 - Challenge 1: Debug 工具箱
# 难度: ⭐⭐
# 二分查找器、执行时间测量器、内存分析器、调用栈打印器

import time
import functools
import traceback
import tracemalloc
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


class DebugToolbox:
    """Debug 工具箱

    包含二分查找、计时、内存分析、调用栈等调试工具。
    """

    @staticmethod
    def bisect_find(data: list, predicate: Callable) -> int:
        """二分法在有序数据中定位问题元素

        Args:
            data: 有序数据列表
            predicate: 判断函数，返回 True 表示目标在右侧

        Returns:
            满足条件的第一个元素索引，-1 表示未找到
        """
        # TODO: 实现二分查找
        # predicate(data[mid]) == True 时往左找，否则往右
        ...

    @staticmethod
    def timeit(func: Callable[P, T]) -> Callable[P, T]:
        """计时装饰器，打印函数执行耗时

        用法：
            @DebugToolbox.timeit
            def slow_function():
                ...
        """
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # TODO: 记录开始时间，调用函数，打印耗时
            ...
        return wrapper

    @staticmethod
    def measure_memory(func: Callable[P, T]) -> Callable[P, T]:
        """内存测量装饰器，打印函数的内存分配情况

        用法：
            @DebugToolbox.measure_memory
            def memory_hungry():
                ...
        """
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # TODO: 启动 tracemalloc，调用函数，打印内存分配峰值
            ...
        return wrapper

    @staticmethod
    def print_call_stack(skip_frames: int = 1, max_frames: int = 20) -> None:
        """打印当前调用栈

        Args:
            skip_frames: 跳过的帧数（排除自身）
            max_frames: 最大显示帧数
        """
        # TODO: 使用 traceback 获取并格式化调用栈
        ...

    @staticmethod
    def binary_search_debug(data: list, target: Any) -> dict[str, Any]:
        """带详细日志的二分查找

        Args:
            data: 有序数据
            target: 查找目标

        Returns:
            包含 steps（查找步骤）、found（是否找到）、index（位置）的字典
        """
        # TODO: 实现带日志的二分查找，记录每一步的比较过程
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    # 测试二分查找
    data = list(range(0, 100, 2))  # [0, 2, 4, ..., 98]
    result = DebugToolbox.bisect_find(data, lambda x: x >= 50)
    print(f"第一个 >= 50 的索引: {result}")

    # 测试计时装饰器
    @DebugToolbox.timeit
    def slow_sum(n: int) -> int:
        return sum(range(n))

    slow_sum(1_000_000)

    # 测试调用栈
    DebugToolbox.print_call_stack()
