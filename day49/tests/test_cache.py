\"\"\"Day 49: 缓存策略测试\"\"\"

import time
import pytest


def test_memory_cache_basic():
    from memory_cache import MemoryCache

    cache = MemoryCache(maxsize=5, default_ttl=1)
    cache.set(\"key1\", \"value1\")
    assert cache.get(\"key1\") == \"value1\"


def test_memory_cache_ttl():
    from memory_cache import MemoryCache

    cache = MemoryCache(default_ttl=0.1)
    cache.set(\"key1\", \"value1\")
    time.sleep(0.2)
    assert cache.get(\"key1\") is None


def test_memory_cache_lru():
    from memory_cache import MemoryCache

    cache = MemoryCache(maxsize=2)
    cache.set(\"a\", 1)
    cache.set(\"b\", 2)
    cache.set(\"c\", 3)  # 淘汰 a

    assert cache.get(\"a\") is None
    assert cache.get(\"c\") == 3


def test_memory_cache_stats():
    from memory_cache import MemoryCache

    cache = MemoryCache()
    cache.set(\"a\", 1)
    cache.get(\"a\")  # hit
    cache.get(\"b\")  # miss

    info = cache.cache_info()
    assert info[\"hits\"] == 1
    assert info[\"misses\"] == 1


def test_multi_level_cache():
    from multi_level import MultiLevelCache

    cache = MultiLevelCache()
    cache.set(\"key\", \"value\", l1_ttl=60, l2_ttl=3600)

    # L1 hit
    assert cache.get(\"key\") == \"value\"

    # 清L1, L2 hit
    cache.l1.delete(\"key\")
    assert cache.get(\"key\") == \"value\"  # 从L2加载并回填L1


def test_cache_aside():
    from cache_patterns import CacheAsideService, MockDB, MockCache

    db, cache = MockDB(), MockCache()
    service = CacheAsideService(cache, db)

    db.set(\"user:1\", {\"name\": \"Alice\"})
    assert service.get(\"user:1\") == {\"name\": \"Alice\"}
    assert cache.get(\"user:1\") is not None  # 缓存了
