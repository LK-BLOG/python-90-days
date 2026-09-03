# Exercise: Implement UniqueIterator
# Should skip duplicate elements

class UniqueIterator:
    def __init__(self, iterable):
        pass  # TODO

    def __iter__(self):
        pass  # TODO

    def __next__(self):
        pass  # TODO

# Test
if __name__ == "__main__":
    data = [1, 2, 2, 3, 3, 3, 4]
    result = list(UniqueIterator(data))
    print(result)  # [1, 2, 3, 4]