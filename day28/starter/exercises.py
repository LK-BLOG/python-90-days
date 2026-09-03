"""
Day 28 练习：asyncio 异步编程

请完成以下练习：
1. 编写协程函数
2. 使用并发执行
3. 实现异步 HTTP 客户端
4. 实现生产者-消费者模式
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from collections import deque


# 练习 1：基础协程

async def async_add(a: int, b: int, delay: float = 0) -> int:
    """异步加法
    
    TODO: 实现
    - 等待 delay 秒
    - 返回 a + b
    """
    pass


async def async_fetch_data(name: str, delay: float) -> Dict[str, Any]:
    """异步获取数据
    
    TODO: 实现
    - 模拟异步操作
    - 返回 {"name": name, "timestamp": 时间戳}
    """
    pass


# 练习 2：并发执行

async def run_concurrently(tasks_count: int = 5) -> List[str]:
    """并发执行多个任务
    
    TODO: 实现
    - 使用 create_task
    - 并发执行
    - 返回所有结果
    """
    pass


async def run_with_timeout(coro, timeout: float) -> Any:
    """带超时的协程
    
    TODO: 实现
    - 使用 asyncio.wait_for
    - 超时返回默认值
    """
    pass


# 练习 3：Semaphore 并发控制

async def fetch_with_semaphore(name: str, sem: asyncio.Semaphore) -> str:
    """使用信号量的异步操作
    
    TODO: 实现
    - 获取信号量
    - 模拟异步操作
    - 释放信号量
    """
    pass


# 练习 4：生产者-消费者

class AsyncQueue:
    """异步队列
    
    TODO: 实现以下功能
    - put: 放入元素（阻塞如果队列满）
    - get: 取出元素（阻塞如果队列空）
    - task_done: 标记任务完成
    - join: 等待所有任务完成
    """
    
    def __init__(self, maxsize: int = 0):
        self.maxsize = maxsize
        self._queue = deque()
        self._getters = deque()
        self._putters = deque()
        self._unfinished_tasks = 0
        self._finished = asyncio.Event()
        self._finished.set()
    
    async def put(self, item: Any):
        """放入元素"""
        # TODO: 实现
        # 如果队列满，等待
        pass
    
    async def get(self) -> Any:
        """取出元素"""
        # TODO: 实现
        # 如果队列空，等待
        pass
    
    def task_done(self):
        """标记任务完成"""
        # TODO: 实现
        pass
    
    async def join(self):
        """等待所有任务完成"""
        # TODO: 实现
        pass


async def producer(queue: AsyncQueue, producer_id: int, items: List):
    """生产者"""
    # TODO: 实现
    for item in items:
        await asyncio.sleep(0.1)  # 模拟生产耗时
        await queue.put(f"P{producer_id}_{item}")
        print(f"生产: P{producer_id}_{item}")
    await queue.put(None)  # 哨兵值


async def consumer(name: str, queue: AsyncQueue):
    """消费者"""
    # TODO: 实现
    while True:
        item = await queue.get()
        if item is None:
            await queue.put(None)  # 传递给其他消费者
            break
        await asyncio.sleep(0.2)  # 模拟消费耗时
        print(f"{name} 消费: {item}")
        queue.task_done()


# 练习 5：异步缓存

class AsyncCache:
    """异步缓存
    
    TODO: 实现
    - TTL 缓存
    - 异步获取
    - 缓存失效
    """
    
    def __init__(self, ttl: float = 60.0):
        self.ttl = ttl
        self._cache = {}
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        # TODO: 实现
        # 检查是否存在
        # 检查是否过期
        pass
    
    async def set(self, key: str, value: Any):
        """设置缓存"""
        # TODO: 实现
        pass
    
    async def get_or_fetch(self, key: str, fetch_func) -> Any:
        """获取缓存或从源获取"""
        # TODO: 实现
        # 先查缓存
        # 没有则调用 fetch_func
        # 结果存入缓存
        pass


if __name__ == "__main__":
    print("Day 28 练习 - asyncio 异步编程")
    
    # 测试基础协程
    print("\n=== 基础协程 ===")
    
    # 测试并发执行
    print("\n=== 并发执行 ===")
    
    # 测试生产者-消费者
    print("\n=== 生产者-消费者 ===")
