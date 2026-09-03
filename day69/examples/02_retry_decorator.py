# -*- coding: utf-8 -*-
import time, random
def retry(max_retries=3, delay=1):
    def deco(func):
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try: return func(*args, **kwargs)
                except Exception as e:
                    if i == max_retries-1: raise
                    w = delay * (2**i) + random.uniform(0,1)
                    print(f"Retry {i+1}: {e}, wait {w:.1f}s")
                    time.sleep(w)
        return wrapper
    return deco
