# -*- coding: utf-8 -*-
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时: {time.time()-start:.4f}s")
        return result
    return wrapper

@timer
def slow():
    time.sleep(0.5)
    return "done"

print(slow())
