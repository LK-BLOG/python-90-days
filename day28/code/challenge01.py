"""
Challenge 01: 异步基础练习 - AsyncBasics
"""
import asyncio
import time
from typing import List, Any


async def async_sleep(delay: float, result: Any = None) -> Any:
    """异步等待"""
    await asyncio.sleep(delay)
    return result


async def fetch_data(name: str, delay: float) -> dict:
    """模拟异步数据获取"""
    await asyncio.sleep(delay)
    return {"name": name, "timestamp": time.time()}


async def run_concurrently(n: int = 5) -> List[dict]:
    """并发执行 n 个任务"""
    # TODO: 实现
    # 使用 create_task 或 gather
    pass


async def run_with_timeout(coro, timeout: float, default=None) -> Any:
    """带超时的协程"""
    # TODO: 实现
    # 使用 asyncio.wait_for
    pass


async def retry(coro_func, max_retries: int = 3, delay: float = 1.0):
    """重试装饰器"""
    # TODO: 实现
    pass


if __name__ == "__main__":
    async def main():
        print("=== 并发执行 ===")
        results = await run_concurrently(5)
        print(f"结果: {results}")
    
    asyncio.run(main())
