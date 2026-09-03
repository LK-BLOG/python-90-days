# Day 28 课程：asyncio 异步编程

## 模块一：异步编程基础

### 1.1 什么是异步编程

同步代码按顺序执行，遇到 I/O（网络、文件）会阻塞等待。
异步代码在等待 I/O 时可以执行其他任务，提高效率。

```python
# 同步：10个请求串行，每个1秒，共10秒
# 异步：10个请求并发，共约1秒
```

### 1.2 async/await 语法

```python
import asyncio

# 定义协程函数
async def say_hello(name: str, delay: float):
    """异步函数（协程）"""
    print(f"Hello, {name}!")
    await asyncio.sleep(delay)  # 异步等待
    print(f"Goodbye, {name}!")

# 运行协程
async def main():
    # 串行执行
    await say_hello("Alice", 1)
    await say_hello("Bob", 1)
    # 总时间：约2秒

asyncio.run(main())
```

### 1.3 事件循环

```python
import asyncio

# 方式1：asyncio.run()（推荐）
async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

asyncio.run(main())

# 方式2：手动管理事件循环
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()
```

---

## 模块二：并发执行

### 2.1 asyncio.create_task()

```python
import asyncio

async def fetch_data(name: str, delay: float):
    print(f"开始获取 {name}")
    await asyncio.sleep(delay)
    print(f"完成 {name}")
    return f"{name} 的数据"

async def main():
    # 创建任务（并发执行）
    task1 = asyncio.create_task(fetch_data("A", 2))
    task2 = asyncio.create_task(fetch_data("B", 1))
    task3 = asyncio.create_task(fetch_data("C", 3))
    
    # 等待所有任务完成
    result1 = await task1
    result2 = await task2
    result3 = await task3
    
    print(f"结果: {result1}, {result2}, {result3}")
    # 总时间：约3秒（最慢的任务）

asyncio.run(main())
```

### 2.2 asyncio.gather()

```python
import asyncio

async def fetch(name: str, delay: float):
    await asyncio.sleep(delay)
    return f"{name}: done"

async def main():
    # 并发执行多个协程
    results = await asyncio.gather(
        fetch("A", 2),
        fetch("B", 1),
        fetch("C", 3),
    )
    
    for result in results:
        print(result)

asyncio.run(main())
```

### 2.3 asyncio.wait()

```python
import asyncio

async def task(name: str, delay: float):
    await asyncio.sleep(delay)
    return f"{name} completed"

async def main():
    tasks = {
        asyncio.create_task(task("A", 2)),
        asyncio.create_task(task("B", 1)),
        asyncio.create_task(task("C", 3)),
    }
    
    # 等待所有完成
    done, pending = await asyncio.wait(tasks)
    
    for t in done:
        print(t.result())
    
    # 等待第一个完成
    done, pending = await asyncio.wait(
        tasks, return_when=asyncio.FIRST_COMPLETED
    )
    
    for t in done:
        print(f"第一个完成: {t.result()}")

asyncio.run(main())
```

### 2.4 as_completed()

```python
import asyncio

async def fetch(name: str, delay: float):
    await asyncio.sleep(delay)
    return f"{name}: done"

async def main():
    tasks = [
        fetch("A", 3),
        fetch("B", 1),
        fetch("C", 2),
    ]
    
    # 按完成顺序获取结果
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"完成: {result}")

asyncio.run(main())
```

---

## 模块三：并发控制

### 3.1 Semaphore

```python
import asyncio

async def fetch(name: str, sem: asyncio.Semaphore):
    async with sem:  # 获取信号量
        print(f"开始 {name}")
        await asyncio.sleep(1)
        print(f"完成 {name}")

async def main():
    # 限制最多3个并发
    sem = asyncio.Semaphore(3)
    
    tasks = [fetch(f"task_{i}", sem) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

### 3.2 asyncio.Queue

```python
import asyncio

async def producer(queue: asyncio.Queue):
    for i in range(10):
        await asyncio.sleep(0.5)
        await queue.put(f"item_{i}")
        print(f"生产: item_{i}")
    await queue.put(None)  # 哨兵值

async def consumer(name: str, queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            await queue.put(None)  # 传递给其他消费者
            break
        print(f"{name} 消费: {item}")
        await asyncio.sleep(1)
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=5)
    
    # 启动生产者和消费者
    producer_task = asyncio.create_task(producer(queue))
    consumer_tasks = [
        asyncio.create_task(consumer(f"consumer_{i}", queue))
        for i in range(3)
    ]
    
    await producer_task
    await asyncio.gather(*consumer_tasks)

asyncio.run(main())
```

---

## 模块四：异步上下文管理器和迭代器

### 4.1 async with

```python
import asyncio

class AsyncDatabase:
    """异步数据库连接"""
    
    async def connect(self):
        print("连接数据库...")
        await asyncio.sleep(1)
        print("已连接")
    
    async def disconnect(self):
        print("断开连接...")
        await asyncio.sleep(0.5)
    
    async def query(self, sql: str):
        await asyncio.sleep(0.5)
        return f"结果: {sql}"
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

async def main():
    async with AsyncDatabase() as db:
        result = await db.query("SELECT * FROM users")
        print(result)

asyncio.run(main())
```

### 4.2 async for

```python
import asyncio

class AsyncCounter:
    """异步计数器"""
    
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop
        self.current = start
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        
        await asyncio.sleep(0.1)
        value = self.current
        self.current += 1
        return value

async def main():
    async for num in AsyncCounter(0, 5):
        print(num)

asyncio.run(main())
```

---

## 模块五：异步 HTTP - aiohttp

### 5.1 安装

```bash
pip install aiohttp
```

### 5.2 基础用法

```python
import aiohttp
import asyncio

async def fetch_url(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            status = response.status
            data = await response.text()
            return status, data

async def main():
    status, data = await fetch_url("https://httpbin.org/get")
    print(f"状态: {status}")
    print(f"数据: {data[:100]}...")

asyncio.run(main())
```

### 5.3 并发请求

```python
import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent",
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        for url, result in zip(urls, results):
            print(f"{url}: {result}")

asyncio.run(main())
```

### 5.4 带限速的并发

```python
import aiohttp
import asyncio

async def fetch_with_limit(session, url, semaphore):
    async with semaphore:
        async with session.get(url) as response:
            return await response.json()

async def main():
    semaphore = asyncio.Semaphore(5)  # 最多5个并发
    
    urls = [f"https://httpbin.org/get?id={i}" for i in range(20)]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_limit(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)
        
        print(f"完成 {len(results)} 个请求")

asyncio.run(main())
```

---

## 模块六：异步文件 I/O

### 6.1 aiofiles

```bash
pip install aiofiles
```

```python
import aiofiles
import asyncio

async def async_read(filepath: str):
    async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
        content = await f.read()
        return content

async def async_write(filepath: str, content: str):
    async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
        await f.write(content)

async def main():
    # 写入
    await async_write("test.txt", "Hello, Async!")
    
    # 读取
    content = await async_read("test.txt")
    print(content)

asyncio.run(main())
```

---

## 模块七：同步 vs 异步性能对比

```python
import asyncio
import aiohttp
import requests
import time

# 同步版本
def sync_fetch(urls):
    start = time.time()
    for url in urls:
        requests.get(url)
    return time.time() - start

# 异步版本
async def async_fetch(urls):
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        await asyncio.gather(*tasks)
    return time.time() - start

# 对比
urls = [f"https://httpbin.org/get?id={i}" for i in range(20)]

sync_time = sync_fetch(urls)
async_time = asyncio.run(async_fetch(urls))

print(f"同步: {sync_time:.2f}秒")
print(f"异步: {async_time:.2f}秒")
print(f"提升: {sync_time/async_time:.1f}x")
```

---

## 模块八：常见模式

### 8.1 超时控制

```python
import asyncio

async def slow_task():
    await asyncio.sleep(10)
    return "done"

async def main():
    try:
        result = await asyncio.wait_for(slow_task(), timeout=5)
    except asyncio.TimeoutError:
        print("任务超时")

asyncio.run(main())
```

### 8.2 重试机制

```python
import asyncio

async def fetch_with_retry(url: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)

async def main():
    result = await fetch_with_retry("https://httpbin.org/get")
    print(result)

asyncio.run(main())
```

---

## 常见错误汇总

| 错误 | 原因 | 解决 |
|------|------|------|
| `RuntimeError: This event loop is already running` | 在已运行的循环中调用 run | 使用 await 或 create_task |
| `TypeError: ... is not a coroutine function` | 忘记 async | 给函数加 async |
| `RuntimeWarning: coroutine was never awaited` | 协程未 await | 使用 await 或 create_task |
| `CancelledError` | 任务被取消 | 处理取消异常 |
| `asyncio` 在 Jupyter 中的问题 | Jupyter 已有事件循环 | 使用 nest_asyncio 或 await |
