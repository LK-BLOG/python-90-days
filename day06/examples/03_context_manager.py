# -*- coding: utf-8 -*-
from contextlib import contextmanager

@contextmanager
def timer(label):
    import time
    start = time.time()
    yield
    print(f"{label}: {time.time()-start:.2f}s")

with timer("处理"):
    import time
    time.sleep(0.5)
