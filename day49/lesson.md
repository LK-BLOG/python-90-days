# Day 49 课程：缓存策略

## 第一部分：缓存基础

### 1.1 什么是缓存
缓存 = 把数据存一份副本，下次要的时候直接拿，不用重新算/查。

### 1.2 缓存层次（从近到远）
`
L1: 进程内缓存（dict/变量）    — 纳秒级
L2: 本地内存缓存（LRU/TTL）   — 微秒级
L3: 分布式缓存（Redis/Memcached） — 毫秒级
L4: CDN缓存                    — 毫秒级
L5: 数据库（不算缓存但最慢）    — 毫秒-秒级
`

---

## 第二部分：缓存模式

### 2.1 Cache-Aside（旁路缓存）
`
读：先查缓存 → 命中返回 → 未命中查DB → 写入缓存
写：更新DB → 删除缓存
`
最常用的模式，应用自己控制缓存。

### 2.2 Write-Through（写穿透）
`
写：同时写缓存和DB（缓存层负责同步）
`
数据一致性好，但写延迟增加。

### 2.3 Write-Behind（写回）
`
写：先写缓存 → 异步批量写DB
`
写性能最高，但有数据丢失风险。

### 2.4 Read-Through
`
读：查缓存 → 未命中时缓存层自动查DB
`
对应用透明，但实现复杂。

---

## 第三部分：缓存问题

### 3.1 缓存穿透
**问题：** 查询不存在的数据，每次都打到DB。
**解决：** 布隆过滤器 / 缓存空值（短TTL）。

`python
def get_user(user_id: int) -> dict | None:
    # 先查缓存（包括空值缓存）
    cached = cache.get(f"user:{user_id}")
    if cached == "__NULL__":
        return None
    if cached:
        return cached

    # 查DB
    user = db.query(f"SELECT * FROM users WHERE id={user_id}")

    if user is None:
        cache.set(f"user:{user_id}", "__NULL__", ttl=60)  # 缓存空值
    else:
        cache.set(f"user:{user_id}", user, ttl=3600)

    return user
`

### 3.2 缓存雪崩
**问题：** 大量缓存同时过期，所有请求打到DB。
**解决：** TTL加随机偏移。

`python
import random

def cache_set_with_jitter(key: str, value: any, base_ttl: int = 3600):
    jitter = random.randint(0, 300)
    cache.set(key, value, ttl=base_ttl + jitter)
`

### 3.3 缓存击穿
**问题：** 热点key过期，瞬间大量请求打到DB。
**解决：** 分布式锁 / singleflight。

`python
import threading

class SingleFlight:
    def __init__(self):
        self._inflight: dict[str, threading.Event] = {}
        self._results: dict[str, Any] = {}
        self._lock = threading.Lock()

    def do(self, key: str, func):
        with self._lock:
            if key in self._inflight:
                # 等待其他线程的结果
                self._inflight[key].wait()
                return self._results[key]

            event = threading.Event()
            self._inflight[key] = event

        try:
            result = func()
            with self._lock:
                self._results[key] = result
            return result
        finally:
            with self._lock:
                event.set()
                del self._inflight[key]
`

---

## 第四部分：Python缓存实现

### 4.1 functools.lru_cache
`python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    # 模拟耗时计算
    return sum(i * i for i in range(n))

# 调用缓存
result = expensive_computation(1000000)  # 首次计算
result = expensive_computation(1000000)  # 缓存命中

# 统计
print(expensive_computation.cache_info())

# 清除缓存
expensive_computation.cache_clear()
`

### 4.2 TTL缓存
`python
from cachetools import TTLCache, LRUCache

# TTL缓存：条目存活时间有限
ttl_cache = TTLCache(maxsize=100, ttl=300)  # 最多100个条目，300秒过期

# LRU缓存：满了淘汰最久未使用的
lru_cache = LRUCache(maxsize=1000)
`

### 4.3 Redis缓存
`python
import json
import redis

class RedisCache:
    def __init__(self, url: str = "redis://localhost:6379"):
        self.client = redis.from_url(url)

    def get(self, key: str) -> Any:
        data = self.client.get(key)
        if data is None:
            return None
        return json.loads(data)

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        self.client.setex(key, ttl, json.dumps(value))

    def delete(self, key: str) -> None:
        self.client.delete(key)

    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0
`

---

## 第五部分：多级缓存

`python
class MultiLevelCache:
    def __init__(self, l2_cache=None):
        self.l1 = {}  # 进程内缓存
        self.l1_ttl: dict[str, float] = {}
        self.l2 = l2_cache  # Redis等

    def get(self, key: str) -> Any:
        # L1
        if key in self.l1:
            if time.time() < self.l1_ttl.get(key, 0):
                return self.l1[key]
            else:
                del self.l1[key]

        # L2
        if self.l2:
            value = self.l2.get(key)
            if value is not None:
                self.l1[key] = value
                self.l1_ttl[key] = time.time() + 60
                return value

        return None

    def set(self, key: str, value: Any, l1_ttl: int = 60, l2_ttl: int = 3600):
        self.l1[key] = value
        self.l1_ttl[key] = time.time() + l1_ttl
        if self.l2:
            self.l2.set(key, value, ttl=l2_ttl)
`

---

## 本课总结

| 概念 | 说明 |
|------|------|
| Cache-Aside | 应用控制，最常用 |
| Write-Through | 同步写，一致性好 |
| Write-Behind | 异步写，性能高 |
| 穿透 | 不存在的key，缓存空值 |
| 雪崩 | 同时过期，加随机TTL |
| 击穿 | 热点key过期，singleflight |
| lru_cache | Python内置LRU缓存 |
| Redis | 分布式缓存 |
