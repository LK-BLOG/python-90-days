"""示例2：gather 和 wait"""
import asyncio
import time


async def fetch(name: str, delay: float) -> str:
    """模拟异步操作"""
    print(f"开始 {name}")
    await asyncio.sleep(delay)
    print(f"完成 {name}")
    return f"{name}: 完成 (耗时 {delay}s)"


async def gather_example():
    """gather 示例"""
    print("=== gather 示例 ===")
    
    results = await asyncio.gather(
        fetch("A", 2),
        fetch("B", 1),
        fetch("C", 3),
    )
    
    print(f"\n结果: {results}")


async def wait_example():
    """wait 示例"""
    print("\n=== wait 示例 ===")
    
    tasks = {
        asyncio.create_task(fetch("A", 2)),
        asyncio.create_task(fetch("B", 1)),
        asyncio.create_task(fetch("C", 3)),
    }
    
    # 等待所有完成
    done, pending = await asyncio.wait(tasks)
    print(f"\n所有完成: {[t.result() for t in done]}")
    
    # 重新创建任务
    tasks = {
        asyncio.create_task(fetch("D", 2)),
        asyncio.create_task(fetch("E", 1)),
        asyncio.create_task(fetch("F", 3)),
    }
    
    # 等待第一个完成
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    print(f"第一个完成: {[t.result() for t in done]}")


async def as_completed_example():
    """as_completed 示例"""
    print("\n=== as_completed 示例 ===")
    
    tasks = [
        fetch("X", 3),
        fetch("Y", 1),
        fetch("Z", 2),
    ]
    
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"完成: {result}")


async def main():
    start = time.time()
    
    await gather_example()
    await wait_example()
    await as_completed_example()
    
    print(f"\n总耗时: {time.time() - start:.2f}秒")


if __name__ == "__main__":
    asyncio.run(main())
