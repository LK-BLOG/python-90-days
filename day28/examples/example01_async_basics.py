"""示例1：asyncio 基础"""
import asyncio
import time


async def say_hello(name: str, delay: float):
    """简单的协程"""
    print(f"[{time.strftime('%H:%M:%S')}] Hello, {name}!")
    await asyncio.sleep(delay)
    print(f"[{time.strftime('%H:%M:%S')}] Goodbye, {name}!")


async def main():
    print("=== 串行执行 ===")
    start = time.time()
    
    await say_hello("Alice", 1)
    await say_hello("Bob", 1)
    
    print(f"串行耗时: {time.time() - start:.2f}秒")
    
    print("\n=== 并发执行 ===")
    start = time.time()
    
    # 创建任务并发执行
    task1 = asyncio.create_task(say_hello("Alice", 1))
    task2 = asyncio.create_task(say_hello("Bob", 1))
    
    # 等待所有任务完成
    await task1
    await task2
    
    print(f"并发耗时: {time.time() - start:.2f}秒")


if __name__ == "__main__":
    asyncio.run(main())
