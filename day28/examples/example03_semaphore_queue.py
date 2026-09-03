"""示例3：Semaphore 和 Queue"""
import asyncio


async def fetch_with_semaphore(name: str, sem: asyncio.Semaphore):
    """使用信号量限制并发"""
    async with sem:
        print(f"开始 {name}")
        await asyncio.sleep(1)
        print(f"完成 {name}")


async def semaphore_example():
    """信号量示例"""
    print("=== Semaphore 示例 ===")
    
    # 限制最多3个并发
    sem = asyncio.Semaphore(3)
    
    tasks = [fetch_with_semaphore(f"task_{i}", sem) for i in range(10)]
    await asyncio.gather(*tasks)


async def producer(queue: asyncio.Queue, name: str):
    """生产者"""
    for i in range(5):
        await asyncio.sleep(0.5)
        item = f"{name}_item_{i}"
        await queue.put(item)
        print(f"生产: {item}")
    await queue.put(None)  # 哨兵值


async def consumer(name: str, queue: asyncio.Queue):
    """消费者"""
    while True:
        item = await queue.get()
        if item is None:
            await queue.put(None)  # 传递给其他消费者
            break
        print(f"{name} 消费: {item}")
        await asyncio.sleep(1)
        queue.task_done()


async def queue_example():
    """队列示例"""
    print("\n=== Queue 示例 ===")
    
    queue = asyncio.Queue(maxsize=5)
    
    # 启动生产者和消费者
    producer_task = asyncio.create_task(producer(queue, "P1"))
    consumer_tasks = [
        asyncio.create_task(consumer(f"C{i}", queue))
        for i in range(3)
    ]
    
    await producer_task
    await asyncio.gather(*consumer_tasks)


async def main():
    await semaphore_example()
    await queue_example()


if __name__ == "__main__":
    asyncio.run(main())
