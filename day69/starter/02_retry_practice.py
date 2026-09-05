# -*- coding: utf-8 -*-
"""Day 69：带退避策略的AI请求重试装饰器。"""
from functools import wraps
from time import sleep
from typing import Callable, Any

def retry_practice(max_retries: int = 3, delay: float = 0.1):
    """失败后按次数重试，最终保留原始异常。"""
    def deco(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error = None
            # TODO：加入指数退避、可重试异常白名单和日志
            for attempt in range(max_retries + 1):
                try: return func(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
                    if attempt < max_retries: sleep(delay * (attempt + 1))
            raise last_error
        return wrapper
    return deco

if __name__ == "__main__": print("请用@retry_practice()装饰一个可能失败的函数")
