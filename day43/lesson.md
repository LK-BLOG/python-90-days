# Day 43 课程：性能分析 & 优化

## 第一部分：性能测量工具

### 1.1 timeit — 微基准测试

`python
import timeit

# 基本用法
result = timeit.timeit('sum(range(1000))', number=10000)
print(f"耗时: {result:.4f}秒")

# 比较两种实现
t1 = timeit.timeit('[i**2 for i in range(1000)]', number=10000)
t2 = timeit.timeit('list(map(lambda x: x**2, range(1000)))', number=10000)
print(f"列表推导: {t1:.4f}s, map: {t2:.4f}s")

# 命令行
# python -m timeit "sum(range(1000))"
`

### 1.2 cProfile — 函数级分析

`python
import cProfile
import pstats

def slow_function():
    total = 0
    for i in range(100000):
        total += i ** 2
    return total

def another_slow():
    return sorted([i * 3 for i in range(50000)])

# 分析
cProfile.run('slow_function()', sort='cumulative')

# 详细分析
profiler = cProfile.Profile()
profiler.enable()
slow_function()
another_slow()
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')  # 按累计时间排序
stats.print_stats(20)  # 前 20 行
stats.print_callers()  # 调用者
`

### 1.3 line_profiler — 行级分析

`ash
pip install line_profiler
`

`python
# 用 @profile 装饰器标记函数
@profile
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item ** 2)
    total = sum(result)
    avg = total / len(result) if result else 0
    return avg

# 运行: kernprof -l -v script.py
`

---

## 第二部分：内存分析

### 2.1 tracemalloc

`python
import tracemalloc

tracemalloc.start()

# 你的代码
data = [i ** 2 for i in range(100000)]

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[内存排名前 5]")
for stat in top_stats[:5]:
    print(stat)
`

### 2.2 memory_profiler

`ash
pip install memory_profiler
`

`python
from memory_profiler import profile

@profile
def my_func():
    a = [i for i in range(100000)]    # ~4MB
    b = [i ** 2 for i in range(200000)]  # ~8MB
    del b                               # 释放
    return a

# 运行: python -m memory_profiler script.py
`

---

## 第三部分：常见优化策略

### 3.1 数据结构选择

`python
# 查找操作：set >> list
# list 查找: O(n)    set 查找: O(1)
big_list = list(range(1000000))
big_set = set(big_list)

%timeit 999999 in big_list   # ~3ms
%timeit 999999 in big_set     # ~0.0001ms

# 排序查找：bisect >> 线性
import bisect
sorted_list = sorted(big_list)
bisect.bisect_left(sorted_list, 999999)  # O(log n)
`

### 3.2 生成器 vs 列表

`python
# 列表：一次性占用所有内存
big_list = [i ** 2 for i in range(10000000)]  # ~80MB

# 生成器：按需生成，内存几乎为零
big_gen = (i ** 2 for i in range(10000000))   # ~100 bytes

# 转换为生成器
def process_large_file(filename):
    with open(filename) as f:
        for line in f:           # 逐行读取，不全部加载
            yield line.strip()
`

### 3.3 算法优化

`python
# 差：O(n²)
def find_duplicates(lst):
    duplicates = []
    for i, item in enumerate(lst):
        if item in lst[i+1:]:  # O(n) 查找
            duplicates.append(item)
    return duplicates

# 好：O(n)
def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
`

### 3.4 缓存

`python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 带过期时间的缓存
import time

_cache = {}
def cached(ttl=300):
    def decorator(func):
        def wrapper(*args):
            key = (func.__name__, args)
            if key in _cache:
                result, timestamp = _cache[key]
                if time.time() - timestamp < ttl:
                    return result
            result = func(*args)
            _cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator
`

---

## 第四部分：异步性能

`python
import asyncio
import httpx
import time

# 同步：一个一个请求
def sync_fetch(urls):
    results = []
    with httpx.Client() as client:
        for url in urls:
            resp = client.get(url)
            results.append(resp.json())
    return results

# 异步：并发请求
async def async_fetch(urls):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

# 连接池
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=10,
)
`

---

## 常见错误
1. 过早优化 -> 先分析，再优化
2. 用 list 做查找 -> 应该用 set
3. 全量加载大文件 -> 用生成器
4. 没用缓存 -> 重复计算

## 动手练习
1. 用 timeit 比较 list vs set 查找
2. 用 cProfile 找到代码瓶颈
3. 用 tracemalloc 分析内存使用
4. 优化一个慢函数
