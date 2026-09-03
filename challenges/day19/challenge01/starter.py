# Challenge 01: Range Iterator
# Implement MyRange(start, stop, step)

class MyRange:
    def __init__(self, *args):
        pass  # TODO: parse start, stop, step

    def __iter__(self):
        pass  # TODO

    def __next__(self):
        pass  # TODO

# Test
if __name__ == "__main__":
    print(list(MyRange(5)))
    print(list(MyRange(1, 5)))
    print(list(MyRange(0, 10, 2)))