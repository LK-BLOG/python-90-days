"""示例5：同步 vs 异步性能对比"""
import asyncio
import time


def sync_fetch(n: int):
    """模拟同步请求"""
    time.sleep(1)
    return f"sync_{n}"


async def async_fetch(n: int):
    """模拟异步请求"""
    await asyncio.sleep(1)
    return f"async_{n}"


async def async_main():
    """异步主函数"""
    tasks = [async_fetch(i) for i in range(10)]
    return await asyncio.gather(*tasks)


def sync_main():
    """同步主函数"""
    results = []
    for i in range(10):
        results.append(sync_fetch(i))
    return results


if __name__ == "__main__":
    N = 10
    
    print(f"=== 性能对比 ({N} 个任务) ===")
    
    # 同步
    start = time.time()
    sync_results = sync_main()
    sync_time = time.time() - start
    print(f"同步: {sync_time:.2f}秒")
    
    # 异步
    start = time.time()
    async_results = asyncio.run(async_main())
    async_time = time.time() - start
    print(f"异步: {async_time:.2f}秒")
    
    print(f"\n提升: {sync_time/async_time:.1f}x")
