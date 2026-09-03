\"\"\"缓存装饰器\"\"\"

import json
import functools
import hashlib
from typing import Any, Callable

try:
    import redis
    _redis = redis.from_url(\"redis://localhost:6379/0\", decode_responses=True)
except Exception:
    _redis = None


def cache_response(ttl: int = 300, prefix: str = \"\"):
    \"\"\"缓存API响应的装饰器\"\"\"

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if _redis is None:
                return await func(*args, **kwargs)

            # 生成缓存key
            key_data = f\"{func.__name__}:{args}:{kwargs}\"
            cache_key = f\"{prefix}{hashlib.md5(key_data.encode()).hexdigest()}\"

            # 查缓存
            cached = _redis.get(cache_key)
            if cached:
                return json.loads(cached)

            # 执行函数
            result = await func(*args, **kwargs)

            # 写缓存
            _redis.setex(cache_key, ttl, json.dumps(result, default=str))
            return result

        # 缓存管理
        wrapper.invalidate = lambda: _redis and _redis.delete(
            *[k for k in _redis.scan_iter(f\"{prefix}*\")]
        )
        return wrapper
    return decorator


def invalidate_cache(prefix: str):
    \"\"\"缓存失效\"\"\"
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            if _redis:
                keys = list(_redis.scan_iter(f\"cache:{prefix}*\"))
                if keys:
                    _redis.delete(*keys)
            return result
        return wrapper
    return decorator
