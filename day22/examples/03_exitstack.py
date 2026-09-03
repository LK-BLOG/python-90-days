from contextlib import ExitStack

class Resource:
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        print(f"Acquiring {self.name}")
        return self
    def __exit__(self, *args):
        print(f"Releasing {self.name}")

with ExitStack() as stack:
    resources = [stack.enter_context(Resource(f"res{i}")) for i in range(3)]
    print("All resources acquired")