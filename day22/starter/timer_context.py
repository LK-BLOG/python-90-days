import time
from contextlib import contextmanager

# Exercise: Implement timer using contextmanager decorator

@contextmanager
def timer(label="block"):
    pass  # TODO

# Test
if __name__ == "__main__":
    with timer("my task"):
        time.sleep(0.1)