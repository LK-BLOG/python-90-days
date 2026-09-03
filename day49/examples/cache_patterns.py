\"\"\"缓存模式示例: Cache-Aside\"\"\"

import time
import random
import json
from typing import Any, Callable


class CacheAsideService:
    \"\"\"Cache-Aside模式实现\"\"\"

    def __init__(self, cache, db):
        self.cache = cache
        self.db = db

    def get(self, key: str, ttl: int = 300) -> Any | None:
        \"\"\"读: 先查缓存 → 命中返回 → 未命中查DB\"\"\"
        # 1. 查缓存
        value = self.cache.get(key)
        if value == \"__NULL__":
            return None
        if value is not None:
            return value

        # 2. 查DB
        value = self.db.get(key)

        # 3. 写入缓存
        if value is None:
            self.cache.set(key, \"__NULL__\", ttl=60)  # 防穿透
        else:
            jitter = random.randint(0, 30)  # 防雪崩
            self.cache.set(key, value, ttl=ttl + jitter)

        return value

    def set(self, key: str, value: Any) -> None:
        \"\"\"写: 更新DB → 删除缓存\"\"\"
        self.db.set(key, value)
        self.cache.delete(key)

    def delete(self, key: str) -> None:
        self.db.delete(key)
        self.cache.delete(key)


# 模拟DB和Cache
class MockDB:
    def __init__(self):
        self._data = {}
    def get(self, key):
        return self._data.get(key)
    def set(self, key, value):
        self._data[key] = value
    def delete(self, key):
        self._data.pop(key, None)


class MockCache:
    def __init__(self):
        self._data = {}
    def get(self, key):
        return self._data.get(key)
    def set(self, key, value, ttl=300):
        self._data[key] = value
    def delete(self, key):
        self._data.pop(key, None)


if __name__ == \"__main__\":
    db = MockDB()
    cache = MockCache()
    service = CacheAsideService(cache, db)

    # 写入
    db.set(\"user:1\", {\"name\": \"Alice\"})
    print(f\"First read (miss): {service.get('user:1')}\")
    print(f\"Second read (hit): {service.get('user:1')}\")
    print(f\"Cache contents: {cache._data}\")

    # 更新后删除缓存
    service.set(\"user:1\", {\"name\": \"Alice Updated\"})
    print(f\"After update: {service.get('user:1')}\")
