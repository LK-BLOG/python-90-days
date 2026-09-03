"""
Challenge 04: 生产者-消费者 - ProducerConsumer
"""
import asyncio
from typing import Any, List, Callable, Optional
from dataclasses import dataclass, field
from collections import deque
import time


@dataclass
class Stats:
    """统计信息"""
    produced: int = 0
    consumed: int = 0
    errors: int = 0
    start_time: float = 0.0
    
    @property
    def elapsed(self) -> float:
        return time.time() - self.start_time if self.start_time else 0


class AsyncBoundedQueue:
    """有界异步队列"""
    
    def __init__(self, maxsize: int = 10):
        self.maxsize = maxsize
        self._queue = deque()
        self._getters = deque()
        self._putters = deque()
    
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
    
    @property
    def qsize(self) -> int:
        return len(self._queue)
    
    @property
    def empty(self) -> bool:
        return len(self._queue) == 0
    
    @property
    def full(self) -> bool:
        return len(self._queue) >= self.maxsize


class ProducerConsumer:
    """生产者-消费者系统"""
    
    def __init__(self, num_producers: int = 2, num_consumers: int = 3,
                 queue_size: int = 10):
        self.num_producers = num_producers
        self.num_consumers = num_consumers
        self.queue = AsyncBoundedQueue(queue_size)
        self.stats = Stats()
        self._running = True
    
    async def producer(self, producer_id: int, items: List[Any]):
        """生产者"""
        # TODO: 实现
        for item in items:
            if not self._running:
                break
            await asyncio.sleep(0.1)  # 模拟生产耗时
            await self.queue.put(f"P{producer_id}_{item}")
            self.stats.produced += 1
            print(f"生产: P{producer_id}_{item}")
        
        # 放入哨兵值
        await self.queue.put(None)
    
    async def consumer(self, consumer_id: int):
        """消费者"""
        # TODO: 实现
        while self._running:
            item = await self.queue.get()
            if item is None:
                await self.queue.put(None)  # 传递给其他消费者
                break
            
            await asyncio.sleep(0.2)  # 模拟消费耗时
            self.stats.consumed += 1
            print(f"C{consumer_id} 消费: {item}")
    
    async def run(self, producer_data: List[List[Any]]):
        """运行系统"""
        # TODO: 实现
        self.stats.start_time = time.time()
        
        # 启动生产者和消费者
        producers = [
            asyncio.create_task(self.producer(i, data))
            for i, data in enumerate(producer_data)
        ]
        
        consumers = [
            asyncio.create_task(self.consumer(i))
            for i in range(self.num_consumers)
        ]
        
        await asyncio.gather(*producers)
        await asyncio.gather(*consumers)
        
        print(f"\n统计: 生产 {self.stats.produced}, 消费 {self.stats.consumed}")
        print(f"耗时: {self.stats.elapsed:.2f}秒")
    
    def stop(self):
        """停止系统"""
        self._running = False


if __name__ == "__main__":
    async def main():
        pc = ProducerConsumer(num_producers=2, num_consumers=3, queue_size=5)
        
        producer_data = [
            list(range(5)),  # 生产者1
            list(range(5)),  # 生产者2
        ]
        
        await pc.run(producer_data)
    
    asyncio.run(main())
