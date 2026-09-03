# -*- coding: utf-8 -*-
import time
def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # TODO: 指数退避重试
            pass
        return wrapper
    return decorator
