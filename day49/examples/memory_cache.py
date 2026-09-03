\"\"\"TTL + LRU内存缓存\"\"\"

import time
import threading
from collections import OrderedDict
from typing import Any


class MemoryCache:
    \"\"\"支持TTL和LRU的内存缓存\"\"\"

    def __init__(self, maxsize: int = 128, default_ttl: int = 300):
        self._cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self._maxsize = maxsize
        self._default_ttl = default_ttl
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Any | None:
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None

            value, expiry = self._cache[key]
            if time.time() > expiry:
                del self._cache[key]
                self._misses += 1
                return None

            # LRU: 移到末尾
            self._cache.move_to_end(key)
            self._hits += 1
            return value

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        with self._lock:
            if key in self._cache:
                del self._cache[key]
            elif len(self._cache) >= self._maxsize:
                # LRU淘汰: 删除最老的
                self._cache.popitem(last=False)

            expiry = time.time() + (ttl or self._default_ttl)
            self._cache[key] = (value, expiry)

    def delete(self, key: str) -> None:
        with self._lock:
            self._cache.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def cache_info(self) -> dict:
        total = self._hits + self._misses
        return {
            \"hits\": self._hits,
            \"misses\": self._misses,
            \"size\": len(self._cache),
            \"maxsize\": self._maxsize,
            \"hit_rate\": self._hits / total if total > 0 else 0,
        }


if __name__ == \"__main__\":
    cache = MemoryCache(maxsize=3, default_ttl=5)

    cache.set(\"a\", 1)
    cache.set(\"b\", 2)
    cache.set(\"c\", 3)

    print(f\"Get a: {cache.get('a')}\")  # 1
    cache.set(\"d\", 4)  # 淘汰 b (LRU)

    print(f\"Get b: {cache.get('b')}\")  # None (淘汰)
    print(f\"Get d: {cache.get('d')}\")  # 4
    print(f\"Info: {cache.cache_info()}\")
