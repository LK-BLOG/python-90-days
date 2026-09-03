from contextlib import contextmanager
import time

@contextmanager
def timer(label="block"):
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"{label}: {elapsed:.4f}s")

with timer("sleep"):
    time.sleep(0.1)