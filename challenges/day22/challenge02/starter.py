import time
from contextlib import contextmanager

@contextmanager
def timer(label="block"):
    pass  # TODO

# Test
if __name__ == "__main__":
    with timer("sleep"):
        time.sleep(0.1)