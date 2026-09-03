from contextlib import ExitStack

class Resource:
    def __init__(self, name):
        self.name = name
        self.active = False

    def open(self):
        self.active = True
        return self

    def close(self):
        self.active = False

class ResourcePool:
    def __init__(self, max_resources=3):
        self.max_resources = max_resources
        self.resources = []

    def acquire(self, name):
        pass  # TODO

    def __enter__(self):
        pass  # TODO

    def __exit__(self, *args):
        pass  # TODO: release all

# Test
if __name__ == "__main__":
    with ResourcePool(3) as pool:
        pool.acquire("db1")
        pool.acquire("db2")
        print("All resources acquired")