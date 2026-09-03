# Basic context manager with __enter__/__exit__

class Indenter:
    def __init__(self):
        self.level = 0

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, *args):
        self.level -= 1

    def print(self, msg):
        print("  " * self.level + msg)

with Indenter() as indent:
    indent.print("first")
    with indent:
        indent.print("second")
        with indent:
            indent.print("third")