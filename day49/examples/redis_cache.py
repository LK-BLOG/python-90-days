\"\"\"Redis缓存封装\"\"\"

import json
from typing import Any

try:
    import redis
except ImportError:
    redis = None


class RedisCache:
    \"\"\"Redis缓存封装\"\"\"

    def __init__(self, url: str = \"redis://localhost:6379\", prefix: str = \"cache:\"):
        if redis is None:
            raise ImportError(\"pip install redis\")
        self.client = redis.from_url(url, decode_responses=True)
        self.prefix = prefix

    def _key(self, key: str) -> str:
        return f\"{self.prefix}{key}\"

    def get(self, key: str) -> Any | None:
        data = self.client.get(self._key(key))
        if data is None:
            return None
        return json.loads(data)

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        self.client.setex(self._key(key), ttl, json.dumps(value, default=str))

    def delete(self, key: str) -> None:
        self.client.delete(self._key(key))

    def exists(self, key: str) -> bool:
        return self.client.exists(self._key(key)) > 0

    def mget(self, keys: list[str]) -> list[Any]:
        prefixed = [self._key(k) for k in keys]
        results = self.client.mget(prefixed)
        return [json.loads(r) if r else None for r in results]

    def mset(self, mapping: dict[str, Any], ttl: int = 3600) -> None:
        pipe = self.client.pipeline()
        for key, value in mapping.items():
            pipe.setex(self._key(key), ttl, json.dumps(value, default=str))
        pipe.execute()

    def incr(self, key: str, amount: int = 1) -> int:
        return self.client.incr(self._key(key), amount)

    def get_or_set(self, key: str, factory, ttl: int = 3600) -> Any:
        \"\"\"Cache-Aside模式\"\"\"
        value = self.get(key)
        if value is None:
            value = factory()
            self.set(key, value, ttl=ttl)
        return value
