# Day 28 - Challenge 1: 异步基础练习
# 难度: ⭐⭐
# 编写协程、create_task、gather、异常处理

import asyncio
import time
from typing import Any


async def async_add(a: int, b: int, delay: float = 0.1) -> int:
    """异步加法（模拟异步操作）

    Args:
        a: 第一个加数
        b: 第二个加数
        delay: 模拟异步延迟

    Returns:
        两数之和
    """
    # TODO: await asyncio.sleep(delay) 模拟异步操作
    ...


async def async_fetch_data(url: str, timeout: float = 5.0) -> dict:
    """模拟异步获取数据

    Args:
        url: 数据 URL
        timeout: 超时时间

    Returns:
        模拟的数据字典

    Raises:
        asyncio.TimeoutError: 超时
    """
    # TODO: 模拟网络请求，支持超时
    ...


async def run_concurrently() -> list[Any]:
    """使用 create_task 并发执行多个协程

    Returns:
        所有任务的结果列表
    """
    # TODO: 创建多个 task，用 create_task 并发执行
    # TODO: 等待所有任务完成
    ...


async def run_with_gather() -> list[Any]:
    """使用 asyncio.gather 获取结果

    Returns:
        所有协程的结果列表
    """
    # TODO: 用 gather 同时运行多个协程
    ...


async def run_with_exceptions() -> list[dict[str, Any]]:
    """并发执行并处理异常

    Returns:
        每个任务的结果或错误信息
    """
    # TODO: 用 gather(return_exceptions=True)
    # TODO: 分类处理成功和失败的结果
    ...


async def demo_basics():
    """演示 asyncio 基础用法"""
    print("=== 单个协程 ===")
    result = await async_add(1, 2)
    print(f"1 + 2 = {result}")

    print("\n=== 并发执行 ===")
    start = time.time()
    results = await run_concurrently()
    elapsed = time.time() - start
    print(f"并发结果: {results}")
    print(f"耗时: {elapsed:.2f}s（应该接近单个任务的延迟）")

    print("\n=== 异常处理 ===")
    results = await run_with_exceptions()
    for r in results:
        print(f"  {r}")


# ==================== 测试 ====================
if __name__ == "__main__":
    asyncio.run(demo_basics())
