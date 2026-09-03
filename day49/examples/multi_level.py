\"\"\"多级缓存实现\"\"\"

import time
import json
import threading
from typing import Any, Callable


class MemoryL1Cache:
    \"\"\"L1: 进程内缓存\"\"\"

    def __init__(self, maxsize: int = 256, default_ttl: int = 60):
        self._data: dict[str, tuple[Any, float]] = {}
        self._maxsize = maxsize
        self._default_ttl = default_ttl
        self._lock = threading.Lock()

    def get(self, key: str) -> Any | None:
        with self._lock:
            if key not in self._data:
                return None
            value, expiry = self._data[key]
            if time.time() > expiry:
                del self._data[key]
                return None
            return value

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        with self._lock:
            if len(self._data) >= self._maxsize:
                # 简单LRU: 删最早的
                oldest = min(self._data, key=lambda k: self._data[k][1])
                del self._data[oldest]
            self._data[key] = (value, time.time() + (ttl or self._default_ttl))

    def delete(self, key: str) -> None:
        with self._lock:
            self._data.pop(key, None)


class MockRedisL2Cache:
    \"\"\"L2: 模拟Redis缓存\"\"\"

    def __init__(self):
        self._data: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Any | None:
        if key in self._data:
            value, expiry = self._data[key]
            if time.time() <= expiry:
                return value
            del self._data[key]
        return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        self._data[key] = (value, time.time() + ttl)

    def delete(self, key: str) -> None:
        self._data.pop(key, None)


class MultiLevelCache:
    \"\"\"多级缓存: L1(内存) + L2(Redis)\"\"\"

    def __init__(self, l1: MemoryL1Cache | None = None, l2: MockRedisL2Cache | None = None):
        self.l1 = l1 or MemoryL1Cache()
        self.l2 = l2 or MockRedisL2Cache()
        self._stats = {\"l1_hit\": 0, \"l2_hit\": 0, \"miss\": 0}

    def get(self, key: str) -> Any | None:
        # L1
        value = self.l1.get(key)
        if value is not None:
            self._stats[\"l1_hit\"] += 1
            return value

        # L2
        value = self.l2.get(key)
        if value is not None:
            self._stats[\"l2_hit\"] += 1
            self.l1.set(key, value, ttl=60)  # 回填L1
            return value

        self._stats[\"miss\"] += 1
        return None

    def set(self, key: str, value: Any, l1_ttl: int = 60, l2_ttl: int = 3600) -> None:
        self.l1.set(key, value, ttl=l1_ttl)
        self.l2.set(key, value, ttl=l2_ttl)

    def delete(self, key: str) -> None:
        self.l1.delete(key)
        self.l2.delete(key)

    def stats(self) -> dict:
        total = sum(self._stats.values())
        return {
            **self._stats,
            \"total\": total,
            \"l1_rate\": self._stats[\"l1_hit\"] / total if total else 0,
            \"l2_rate\": self._stats[\"l2_hit\"] / total if total else 0,
            \"miss_rate\": self._stats[\"miss\"] / total if total else 0,
        }


if __name__ == \"__main__\":
    cache = MultiLevelCache()

    # 第一次: 全miss
    cache.set(\"user:1\", {\"name\": \"Alice\", \"email\": \"alice@test.com\"})
    val = cache.get(\"user:1\")
    print(f\"L1 hit: {val}\")

    # 清L1, 从L2恢复
    cache.l1.delete(\"user:1\")
    val = cache.get(\"user:1\")
    print(f\"L2 hit + L1回填: {val}\")

    print(f\"Stats: {cache.stats()}\")
