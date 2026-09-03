# Day 28 - Challenge 2: 并发计算器
# 难度: ⭐⭐⭐
# 并发计算多个数学运算、结果聚合、超时控制、性能统计

import asyncio
import math
import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ComputationResult:
    """单次计算结果"""
    task_name: str
    result: Any = None
    elapsed_ms: float = 0.0
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None


@dataclass
class Stats:
    """性能统计"""
    total_tasks: int = 0
    successful: int = 0
    failed: int = 0
    total_time_ms: float = 0.0
    avg_time_ms: float = 0.0
    max_time_ms: float = 0.0


class ConcurrentCalculator:
    """并发计算器

    并发执行多个数学运算，收集结果并统计性能。
    """

    def __init__(self, max_concurrent: int = 10, timeout: float = 30.0):
        """初始化

        Args:
            max_concurrent: 最大并发数
            timeout: 总超时时间
        """
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def compute_one(self, name: str, func: Callable, *args, **kwargs) -> ComputationResult:
        """执行单个计算任务

        Args:
            name: 任务名称
            func: 计算函数
            *args, **kwargs: 函数参数

        Returns:
            ComputationResult 对象
        """
        # TODO: 使用 semaphore 限制并发
        # TODO: 记录执行时间
        # TODO: 捕获异常
        ...

    async def compute_batch(self, tasks: list[tuple[str, Callable, tuple, dict]]) -> list[ComputationResult]:
        """批量并发计算

        Args:
            tasks: [(名称, 函数, 位置参数, 关键字参数), ...] 列表

        Returns:
            所有计算结果列表
        """
        # TODO: 用 asyncio.gather 并发执行所有任务
        # TODO: 设置总超时
        ...

    def aggregate(self, results: list[ComputationResult]) -> dict:
        """聚合计算结果

        Args:
            results: 计算结果列表

        Returns:
            包含成功/失败统计和汇总的字典
        """
        # TODO: 统计成功/失败数
        # TODO: 计算平均/最大耗时
        ...

    @staticmethod
    def fibonacci(n: int) -> int:
        """计算第 n 个斐波那契数"""
        if n <= 1:
            return n
        return ConcurrentCalculator.fibonacci(n - 1) + ConcurrentCalculator.fibonacci(n - 2)


# ==================== 测试 ====================
if __name__ == "__main__":
    async def main():
        calc = ConcurrentCalculator(max_concurrent=5, timeout=10.0)

        # 准备一批计算任务
        tasks = [
            (f"fib({n})", ConcurrentCalculator.fibonacci, (n,), {})
            for n in range(25, 36)
        ]

        results = await calc.compute_batch(tasks)
        stats = calc.aggregate(results)
        print(f"完成 {stats['total_tasks']} 个任务")
        print(f"成功: {stats['successful']}, 失败: {stats['failed']}")
        print(f"总耗时: {stats['total_time_ms']:.1f}ms")

    asyncio.run(main())
