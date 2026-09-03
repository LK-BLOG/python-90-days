# Day 28 - Challenge 4: 生产者-消费者
# 难度: ⭐⭐⭐⭐
# 多个生产者、多个消费者、有限缓冲区、优雅退出

import asyncio
import time
import random
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Task:
    """任务对象"""
    id: int
    data: Any
    created_at: float = 0.0
    processed_at: float = 0.0
    worker_id: int = 0


class BoundedBuffer:
    """有限缓冲区（有界队列包装）"""

    def __init__(self, max_size: int = 10):
        """初始化

        Args:
            max_size: 缓冲区最大容量
        """
        self.max_size = max_size
        # TODO: 创建 asyncio.Queue
        self._queue: asyncio.Queue = None
        self._total_produced = 0
        self._total_consumed = 0

    async def put(self, item: Any) -> None:
        """放入一个项目（满时等待）"""
        # TODO: await self._queue.put(item)
        ...

    async def get(self) -> Any:
        """取出一个项目（空时等待）"""
        # TODO: return await self._queue.get()
        ...

    def task_done(self) -> None:
        """标记一个项目已处理完成"""
        ...

    @property
    def stats(self) -> dict:
        return {
            "size": self._queue.qsize() if self._queue else 0,
            "produced": self._total_produced,
            "consumed": self._total_consumed,
        }


class Producer:
    """生产者"""

    def __init__(self, producer_id: int, buffer: BoundedBuffer,
                 num_items: int = 10):
        """初始化

        Args:
            producer_id: 生产者 ID
            buffer: 共享缓冲区
            num_items: 要生产的项目数
        """
        self.producer_id = producer_id
        self.buffer = buffer
        self.num_items = num_items

    async def produce(self) -> None:
        """生产任务"""
        # TODO: 循环生产 num_items 个任务
        # TODO: 模拟生产延迟
        # TODO: 放入缓冲区
        ...


class Consumer:
    """消费者"""

    def __init__(self, consumer_id: int, buffer: BoundedBuffer,
                 process_func: Callable = None):
        """初始化

        Args:
            consumer_id: 消费者 ID
            buffer: 共享缓冲区
            process_func: 处理函数
        """
        self.consumer_id = consumer_id
        self.buffer = buffer
        self.process_func = process_func or self._default_process
        self.processed: list[Task] = []

    async def consume(self, stop_event: asyncio.Event = None) -> None:
        """持续消费任务

        Args:
            stop_event: 停止信号事件
        """
        # TODO: 循环从缓冲区获取任务
        # TODO: 处理任务
        # TODO: 收到停止信号时优雅退出
        ...

    @staticmethod
    def _default_process(task: Task) -> Any:
        """默认处理函数"""
        time.sleep(random.uniform(0.01, 0.05))  # 模拟处理时间
        return f"processed_{task.id}"


class ProducerConsumerSystem:
    """生产者-消费者系统"""

    def __init__(self, num_producers: int = 2, num_consumers: int = 3,
                 buffer_size: int = 5, items_per_producer: int = 10):
        """初始化

        Args:
            num_producers: 生产者数量
            num_consumers: 消费者数量
            buffer_size: 缓冲区大小
            items_per_producer: 每个生产者的项目数
        """
        # TODO: 创建缓冲区、生产者、消费者
        self.buffer = BoundedBuffer(buffer_size)
        self.producers = [
            Producer(i, self.buffer, items_per_producer)
            for i in range(num_producers)
        ]
        self.consumers = [
            Consumer(i, self.buffer)
            for i in range(num_consumers)
        ]
        self._stop_event = asyncio.Event()

    async def run(self) -> dict:
        """运行系统

        Returns:
            运行统计信息
        """
        # TODO: 启动所有生产者和消费者
        # TODO: 等待所有生产者完成
        # TODO: 等待缓冲区清空后停止消费者
        # TODO: 汇总统计信息
        ...


# ==================== 测试 ====================
if __name__ == "__main__":
    async def main():
        system = ProducerConsumerSystem(
            num_producers=2,
            num_consumers=3,
            buffer_size=5,
            items_per_producer=8,
        )
        stats = await system.run()
        print(f"运行统计: {stats}")

    asyncio.run(main())
